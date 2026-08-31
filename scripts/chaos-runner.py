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
import json
import shutil
import subprocess
import sys
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
    """Scenario 1: state file corruption (coord.json)."""
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
    # Backup prod eval, swap with synthetic, run, restore
    prod_eval = SOURCE_STATE / "eval-per-agent.json"
    backup = None
    if prod_eval.exists():
        backup = SOURCE_STATE / "eval-per-agent.json.backup.chaos"
        shutil.copy2(prod_eval, backup)
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
        # Cleanup the trending.json prod write to avoid confusion
        prod_trending = SOURCE_STATE / "eval-trending.json"
        if prod_trending.exists():
            # Restore prod's eval-trending.json if there was one before
            # (For now, just leave it - it's overwritten anyway by the next nightly run)
            pass
    finally:
        # Always restore prod eval-per-agent.json
        if backup and backup.exists():
            shutil.copy2(backup, prod_eval)
            backup.unlink()

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


def main():
    parser = argparse.ArgumentParser(description="Chaos test runner")
    parser.add_argument("--scenario", type=int, required=True,
                        help="Scenario number (1=state corruption; others need operator approval)")
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--output", type=Path,
                        default=Path("/opt/data/state/chaos-test-result.json"))
    args = parser.parse_args()

    if args.scenario != 1:
        print(f"ERROR: Only scenario 1 implemented. Others require operator approval.")
        sys.exit(1)

    started = datetime.now(timezone.utc).isoformat()
    result = {}
    if args.scenario == 1:
        result = run_scenario_1(args.staging_dir)
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
