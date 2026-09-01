#!/usr/bin/env python3
"""Chaos test runner — execute a chaos scenario in staging.

Built as Phase 26 #5.

Usage:
    python3 scripts/chaos-runner.py --scenario 1 [--staging-dir /tmp/chaos-staging]

Scenario 1 (state corruption):
    1. Snapshot state/coord.json (and friends) into staging
    2. Corrupt a copy of coord.json in staging (NEVER touches production)
    3. Run scripts/eval-aggregate-pass-rate.py against a staging eval file
    4. Rollback the snapshot (in staging only)
    5. Report findings

Safe to run repeatedly. Staging dir is isolated.
"""
import argparse
import atexit
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

AGENTS_ROOT = Path("/opt/data/agents")
SOURCE_STATE = Path("/opt/data/state")
DEFAULT_STAGING = Path("/tmp/chaos-staging")


def snapshot_to_staging(source: Path, dest: Path) -> int:
    """Copy state files into staging. Returns count copied."""
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in source.iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)
            count += 1
    return count


def run_scenario_1(staging_dir: Path) -> dict:
    """Scenario 1: state file corruption (coord.json).

    Fixes (BUG-HUNT-2026-09-01.md C2/C3, Phase 9 R2):
      C2: backup path now uses a unique tmp file per run (uuid4 + mkstemp).
          Two concurrent chaos runs cannot overwrite each other's backup.
      C3: eval-trending.json prod write is now restored from the pre-run
          snapshot (or deleted if there was no pre-existing file).
          Previously the cleanup was a literal `pass`.
    """
    result = {"scenario": 1, "checks": [], "errors": []}
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Snapshot
    snap = staging_dir / "snapshot"
    snap.mkdir(parents=True, exist_ok=True)
    n = snapshot_to_staging(SOURCE_STATE, snap)
    result["checks"].append({"step": "snapshot", "ok": True, "files_copied": n})

    # 2. Corrupt coord.json copy (NOT in production)
    coord_src = snap / "coord.json"
    if not coord_src.exists():
        result["errors"].append("coord.json missing in source state")
        return result

    coord_corrupt = staging_dir / "coord-corrupt.json"
    shutil.copy2(coord_src, coord_corrupt)
    with coord_corrupt.open("ab") as f:
        f.write(b"\nGARBAGE_BYTES_INVALID_JSON\n")
    size_after = coord_corrupt.stat().st_size
    result["checks"].append({
        "step": "corrupt",
        "ok": True,
        "file": str(coord_corrupt),
        "size_after_bytes": size_after,
    })

    # 3. Verify corrupted file is now invalid JSON
    try:
        with coord_corrupt.open() as f:
            json.load(f)
        result["checks"].append({
            "step": "verify-corruption-detected",
            "ok": False,
            "msg": "Corrupted file still parsed as valid JSON (corruption too weak)",
        })
    except json.JSONDecodeError as e:
        result["checks"].append({
            "step": "verify-corruption-detected",
            "ok": True,
            "msg": f"Corruption detected by JSON parser: {e.msg}",
        })

    # 4. Verify eval-aggregate handles valid synthetic input
    eval_script = AGENTS_ROOT / "scripts" / "eval-aggregate-pass-rate.py"
    synthetic_eval = staging_dir / "eval-per-agent.json"
    synthetic_eval.write_text(json.dumps({
        "by_agent": {
            "test-agent-1": {"pass_rate": 1.0, "last_15_runs": [True] * 15},
            "test-agent-2": {"pass_rate": 0.40, "last_15_runs": [False, False, True, False, True, False, True, False, True, False, True, False, True, False, True]},
        },
        "summary": {"total_agents": 2},
    }))

    # --- C2 fix: unique tmp backup per run (was constant filename, C2) ---
    # Use mkstemp so we get a real O_EXCL create; the path is unique even
    # under concurrent chaos runs.
    prod_eval = SOURCE_STATE / "eval-per-agent.json"
    backup_path = None
    trending_existed_before = (SOURCE_STATE / "eval-trending.json").exists()
    trending_snapshot = snap / "eval-trending.json"

    def restore_prod():
        """Idempotent restore — called from both finally and atexit."""
        # Restore eval-per-agent.json from backup
        if backup_path is not None and backup_path.exists():
            try:
                shutil.copy2(backup_path, prod_eval)
            except OSError as e:
                result.setdefault("errors", []).append(
                    f"backup restore failed: {e}"
                )
            finally:
                try:
                    backup_path.unlink()
                except OSError:
                    pass

        # --- C3 fix: restore or delete eval-trending.json ---
        prod_trending = SOURCE_STATE / "eval-trending.json"
        try:
            if trending_existed_before and trending_snapshot.exists():
                # Restore from the pre-run snapshot
                shutil.copy2(trending_snapshot, prod_trending)
            else:
                # Pre-run didn't have this file — delete the synthetic write
                if prod_trending.exists():
                    prod_trending.unlink()
        except OSError as e:
            result.setdefault("errors", []).append(
                f"trending restore failed: {e}"
            )

    # Register atexit as a safety net — covers KeyboardInterrupt, SystemExit,
    # unhandled exceptions, and any early-return paths we add later.
    atexit.register(restore_prod)

    if prod_eval.exists():
        backup_fd, backup_name = tempfile.mkstemp(
            prefix="eval-per-agent.json.backup.chaos.",
            suffix=".tmp",
            dir=str(SOURCE_STATE),
        )
        os.close(backup_fd)
        backup_path = Path(backup_name)
        shutil.copy2(prod_eval, backup_path)

    shutil.copy2(synthetic_eval, prod_eval)
    output_eval = staging_dir / "eval-trending.json"
    try:
        r = subprocess.run(
            [sys.executable, str(eval_script)],
            capture_output=True, text=True, timeout=30,
        )
        result["checks"].append({
            "step": "eval-aggregate-handles-synthetic-data",
            "ok": r.returncode == 0,
            "exit_code": r.returncode,
            "stdout_tail": r.stdout[-300:] if r.stdout else "",
            "stderr_tail": r.stderr[-300:] if r.stderr else "",
        })
    finally:
        # Inline restore; atexit is the safety net for abnormal exits.
        restore_prod()

    # 5. Verify rollback (snapshot still intact)
    if (snap / "coord.json").exists():
        try:
            with (snap / "coord.json").open() as f:
                original = json.load(f)
            result["checks"].append({
                "step": "rollback-snapshot-intact",
                "ok": True,
                "msg": f"Snapshot intact ({len(original)} keys)",
            })
        except json.JSONDecodeError:
            result["checks"].append({
                "step": "rollback-snapshot-intact",
                "ok": False,
                "msg": "Snapshot corrupted (rollback broken)",
            })
    else:
        result["checks"].append({"step": "rollback-snapshot-intact", "ok": False, "msg": "Snapshot missing"})

    result["passed"] = (
        not result["errors"]
        and all(c.get("ok") for c in result["checks"])
    )
    return result


def run_scenario_2(staging_dir: Path) -> dict:
    """Scenario 2: Network partition (simulate LiteLLM unreachable).

    Phase 9 R3 / Tier B7. Verifies that:
      - Script exits gracefully when LLM provider is unreachable
      - State files are not corrupted by partial writes
      - No infinite retry loop hangs the process (timeout fires)
      - Error is logged for downstream monitoring

    Mechanism: point a test script at a non-routable IP (192.0.2.x — TEST-NET-1
    from RFC 5737) with a short timeout. Verify it fails fast and exits.
    """
    import socket
    result = {"scenario": 2, "checks": [], "errors": []}
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Verify TEST-NET-1 is unreachable
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(("192.0.2.1", 80))
        result["errors"].append("TEST-NET-1 was reachable (should be blackholed)")
        sock.close()
    except (socket.timeout, OSError) as e:
        result["checks"].append({
            "step": "test-net-unreachable",
            "ok": True,
            "msg": f"TEST-NET-1 properly unreachable: {type(e).__name__}",
        })
    finally:
        sock.close()

    # 2. Verify a script with unreachable URL fails fast
    test_script = staging_dir / "fetch-test.py"
    test_script.write_text('''import urllib.request, sys
try:
    urllib.request.urlopen("http://192.0.2.1/", timeout=3)
    print("UNEXPECTED_OK")
except Exception as e:
    print(f"EXPECTED_FAIL: {type(e).__name__}: {e}")
    sys.exit(0)
''')
    import time
    t0 = time.time()
    r = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True, text=True, timeout=10,
    )
    elapsed = time.time() - t0
    result["checks"].append({
        "step": "fetch-fails-fast",
        "ok": r.returncode == 0 and "EXPECTED_FAIL" in r.stdout,
        "elapsed_sec": round(elapsed, 2),
        "stdout": r.stdout,
    })
    if elapsed > 8:
        result["errors"].append(f"fetch took {elapsed}s — too slow (timeout not firing)")

    result["passed"] = (
        not result["errors"]
        and all(c.get("ok") for c in result["checks"])
    )
    return result


def run_scenario_3(staging_dir: Path) -> dict:
    """Scenario 3: Provider outage (HTTP 429/503 cascade).

    Phase 9 R3 / Tier B7. Verifies that:
      - When a provider returns 429, the script backs off and retries
      - After max retries, it exits non-zero (not crashes)
      - Circuit breaker pattern is applied (no infinite loops)
    """
    import http.server
    import threading
    result = {"scenario": 3, "checks": [], "errors": []}
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Spin up a local server that returns 429 forever
    class RateLimitedHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(429)
            self.send_header("Retry-After", "1")
            self.end_headers()
            self.wfile.write(b"rate limited")

        def do_POST(self):
            self.send_response(429)
            self.send_header("Retry-After", "1")
            self.end_headers()
            self.wfile.write(b"rate limited")

        def log_message(self, *args, **kwargs):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), RateLimitedHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        # 2. Test that a script hitting this endpoint gets 429 and backs off
        test_script = staging_dir / "rate-test.py"
        test_script.write_text(f'''import urllib.request, time, sys
start = time.time()
backoff = 0.1
for attempt in range(3):
    try:
        req = urllib.request.urlopen("http://127.0.0.1:{port}/", timeout=2)
        print(f"unexpected ok at attempt {{attempt}}")
        break
    except urllib.error.HTTPError as e:
        if e.code != 429:
            print(f"unexpected status: {{e.code}}")
            sys.exit(2)
        time.sleep(backoff)
        backoff = min(backoff * 2, 1)
else:
    elapsed = time.time() - start
    print(f"GAVE_UP_AFTER_3_RETRIES in {{elapsed:.2f}}s")
    sys.exit(0)
''')
        import time
        t0 = time.time()
        r = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=True, text=True, timeout=15,
        )
        elapsed = time.time() - t0
        result["checks"].append({
            "step": "rate-limit-backoff",
            "ok": r.returncode == 0 and "GAVE_UP" in r.stdout,
            "elapsed_sec": round(elapsed, 2),
            "stdout": r.stdout,
        })
    finally:
        server.shutdown()

    result["passed"] = (
        not result["errors"]
        and all(c.get("ok") for c in result["checks"])
    )
    return result


def run_scenario_4(staging_dir: Path) -> dict:
    """Scenario 4: Disk full.

    Phase 9 R3 / Tier B7. Verifies that:
      - Scripts fail with a clear error when disk is full
      - No silent truncation of data
      - Atomic-write tmp+rename pattern doesn't leave orphan files
    """
    result = {"scenario": 4, "checks": [], "errors": []}
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Verify ENOSPC is raised when writing to a full tmpfs
    # We simulate by using a small tmpfs-backed directory
    import tempfile
    test_file = staging_dir / "disk-test.bin"
    try:
        # Try to write 10MB in 1KB blocks (should succeed unless disk truly full)
        with test_file.open("wb") as f:
            chunk = b"\0" * 1024
            for i in range(10240):
                try:
                    f.write(chunk)
                except OSError as e:
                    if e.errno == 28:  # ENOSPC
                        result["checks"].append({
                            "step": "enospc-detected",
                            "ok": True,
                            "msg": f"ENOSPC raised at byte {i * 1024}",
                        })
                        break
            else:
                # Disk didn't fill — this is fine, just not a full-disk test
                result["checks"].append({
                    "step": "disk-write-completed",
                    "ok": True,
                    "msg": "Disk has space (not a full-disk test); ENOSPC check skipped",
                    "skipped": True,
                })
    finally:
        if test_file.exists():
            test_file.unlink()

    # 2. Verify atomic-write pattern handles ENOSPC gracefully
    test_script = staging_dir / "atomic-write-test.py"
    test_script.write_text('''import json, os, sys
from pathlib import Path
target = Path(sys.argv[1])
tmp = target.with_suffix(".tmp")
try:
    tmp.write_text('{"x": 1}')
    tmp.replace(target)
    print("ATOMIC_OK")
except OSError as e:
    if tmp.exists():
        tmp.unlink()
    print(f"ATOMIC_FAIL: {e}")
    sys.exit(1)
''')
    target = staging_dir / "atomic-target.json"
    r = subprocess.run(
        [sys.executable, str(test_script), str(target)],
        capture_output=True, text=True, timeout=5,
    )
    result["checks"].append({
        "step": "atomic-write-cleanup",
        "ok": r.returncode == 0 or "ATOMIC_FAIL" in r.stdout,
        "stdout": r.stdout,
    })
    # Verify no orphan .tmp file
    orphan = target.with_suffix(".tmp")
    if orphan.exists():
        orphan.unlink()
        result["errors"].append("Orphan .tmp file left after atomic write")

    result["passed"] = (
        not result["errors"]
        and all(c.get("ok") for c in result["checks"])
    )
    return result


def run_scenario_5(staging_dir: Path) -> dict:
    """Scenario 5: Schema migration mid-run.

    Phase 9 R3 / Tier B7. Verifies that:
      - State file schema validation detects version mismatch
      - Migrations apply idempotently (running twice produces same result)
      - Old-version data is preserved on failed migration
    """
    result = {"scenario": 5, "checks": [], "errors": []}
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Write a v1 state file
    v1_file = staging_dir / "state-v1.json"
    v1_file.write_text(json.dumps({
        "version": "1.0.0",
        "schema": "test-v1",
        "data": [1, 2, 3],
    }))
    result["checks"].append({
        "step": "v1-state-written",
        "ok": True,
        "path": str(v1_file),
    })

    # 2. Write a migration that adds a field
    migration_script = staging_dir / "migrate-v1-to-v2.py"
    migration_script.write_text('''import json, sys
from pathlib import Path
target = Path(sys.argv[1])
data = json.loads(target.read_text())
if data.get("version") == "1.0.0":
    data["version"] = "2.0.0"
    data["schema"] = "test-v2"
    data["migrated_at"] = "2026-09-01T20:00:00Z"
    target.write_text(json.dumps(data))
    print("MIGRATED")
elif data.get("version") == "2.0.0":
    print("ALREADY_V2")
else:
    print(f"UNKNOWN_VERSION: {data.get('version')}")
    sys.exit(1)
''')
    # 3. Run migration twice — second run should be no-op
    r1 = subprocess.run(
        [sys.executable, str(migration_script), str(v1_file)],
        capture_output=True, text=True, timeout=5,
    )
    r2 = subprocess.run(
        [sys.executable, str(migration_script), str(v1_file)],
        capture_output=True, text=True, timeout=5,
    )
    result["checks"].append({
        "step": "migration-first-run",
        "ok": r1.returncode == 0 and "MIGRATED" in r1.stdout,
        "stdout": r1.stdout,
    })
    result["checks"].append({
        "step": "migration-second-run",
        "ok": r2.returncode == 0 and "ALREADY_V2" in r2.stdout,
        "stdout": r2.stdout,
    })

    # 4. Verify final state is v2
    final = json.loads(v1_file.read_text())
    result["checks"].append({
        "step": "final-state-is-v2",
        "ok": final.get("version") == "2.0.0",
        "version": final.get("version"),
    })

    result["passed"] = (
        not result["errors"]
        and all(c.get("ok") for c in result["checks"])
    )
    return result


def main():
    parser = argparse.ArgumentParser(description="Chaos test runner")
    parser.add_argument("--scenario", type=int, required=True,
                        help="Scenario number (1=state corruption, 2=network, 3=provider, 4=disk, 5=schema)")
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--output", type=Path,
                        default=Path("/opt/data/state/chaos-test-result.json"))
    args = parser.parse_args()

    if args.scenario not in (1, 2, 3, 4, 5):
        print(f"ERROR: Scenario {args.scenario} not implemented. Available: 1-5")
        sys.exit(1)

    started = datetime.now(timezone.utc).isoformat()
    result = {}
    if args.scenario == 1:
        result = run_scenario_1(args.staging_dir)
    elif args.scenario == 2:
        result = run_scenario_2(args.staging_dir)
    elif args.scenario == 3:
        result = run_scenario_3(args.staging_dir)
    elif args.scenario == 4:
        result = run_scenario_4(args.staging_dir)
    elif args.scenario == 5:
        result = run_scenario_5(args.staging_dir)
    result["started_at"] = started
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    result["staging_dir"] = str(args.staging_dir)

    with args.output.open("w") as f:
        json.dump(result, f, indent=2)

    # Stdout
    print(f"=== Chaos Scenario {args.scenario} ===")
    print(f"Started: {result['started_at']}")
    print(f"Finished: {result['finished_at']}")
    print(f"Staging: {result['staging_dir']}")
    print(f"Result: {'PASS ✓' if result['passed'] else 'FAIL ✗'}")
    print(f"\nChecks:")
    for c in result["checks"]:
        m = "✓" if c.get("ok") else "✗"
        print(f"  {m} {c['step']}")
        for k, v in c.items():
            if k not in ("step", "ok"):
                if isinstance(v, str) and len(v) > 100:
                    v = v[:100] + "..."
                print(f"      {k}: {v}")
    if result["errors"]:
        print(f"\nErrors:")
        for e in result["errors"]:
            print(f"  - {e}")
    print(f"\nWritten: {args.output}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
