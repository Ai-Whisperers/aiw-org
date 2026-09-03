#!/usr/bin/env python3
"""aiw-eval-post-brief-hook.py — Wire eval-gate.py as an automatic post-brief hook.

Watches every /opt/data/agents/<dept>/outbox/*.md file. When a new brief appears
(or is modified), runs the existing 9-check /opt/data/agents-v2/eval-gate.py
scorer against it, then:

  (1) Appends a score footer to the brief ("## Eval-gate: X/9 PASS").
  (2) Appends the result to /opt/data/state/eval-per-agent.json with
      timestamp + agent + score (idempotent — re-runs do not double-append).
  (3) If score < 7, posts a warning via Evolution API (best-effort; logs if
      the API is unreachable).

Designed to be invoked both:
  - as a long-lived poller (python3 aiw-eval-post-brief-hook.py --poll)
  - as a one-shot sweep (python3 aiw-eval-post-brief-hook.py) — the default
    cron registration uses this mode every 5 minutes.

Stdlib only. Does NOT touch /opt/data/agents-v2/eval-gate.py — it shells out to
the existing 9-check scorer.

Last review: 2026-08-26 (gap #10 — post-brief eval-gate wiring).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

AGENTS_DIR = Path("/opt/data/agents")
EVAL_GATE = Path("/opt/data/agents/scripts/eval-gate.py")
EVAL_STATE = Path("/opt/data/state/eval-per-agent.json")
LOG_PATH = Path("/opt/data/logs/aiw-eval-post-brief-hook.log")

POLL_INTERVAL_SECS = 30
ALERT_THRESHOLD = 7  # below this is a warning
MAX_SCORE = 9        # eval-gate.py produces 9 checks

# Evolution API — same env-var pattern as cron-error-watchdog.py
EVOLUTION_URL = os.environ.get("EVOLUTION_URL", "https://evolution.paragu-ai.com")
EVOLUTION_KEY = os.environ.get("EVOLUTION_KEY", "")
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT", "")

# Footer marker — used to detect "already scored" so the hook is idempotent.
FOOTER_PREFIX = "## Eval-gate:"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    """Append a timestamped line to the log file. Stdout also for cron pickup."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass  # never let logging break the run
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# State IO
# ---------------------------------------------------------------------------

def load_state() -> dict:
    """Load eval-per-agent.json; tolerate empty/missing."""
    if not EVAL_STATE.exists():
        return {
            "version": "1.0.0",
            "schema": "per-agent-eval-v1",
            "ts": datetime.now(timezone.utc).isoformat(),
            "total": 0,
            "passed": 0,
            "failed": 0,
            "by_agent": {},
        }
    try:
        return json.loads(EVAL_STATE.read_text(encoding="utf-8"))
    except Exception:
        # Corrupted: back it up and start fresh rather than blowing up.
        try:
            EVAL_STATE.rename(EVAL_STATE.with_suffix(".json.corrupt"))
        except Exception:
            pass
        return {
            "version": "1.0.0",
            "schema": "per-agent-eval-v1",
            "ts": datetime.now(timezone.utc).isoformat(),
            "total": 0,
            "passed": 0,
            "failed": 0,
            "by_agent": {},
        }


def save_state(state: dict) -> None:
    """Atomic-ish write: write to .tmp then rename."""
    state["ts"] = datetime.now(timezone.utc).isoformat()
    EVAL_STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = EVAL_STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(EVAL_STATE)


# ---------------------------------------------------------------------------
# Eval-gate invocation
# ---------------------------------------------------------------------------

def run_eval_gate(brief_path: Path, dry_run: bool = False) -> dict | None:
    """Invoke eval-gate.py on a brief. Returns the parsed JSON block.

    The existing eval-gate.py writes a SQLite row + prints human output.
    For post-brief hook purposes we parse the score from stdout (last
    "Score: X/Y" line) and from exit code (0=PASS, 2=FAIL).
    """
    if not EVAL_GATE.exists():
        log(f"ERROR: eval-gate.py not found at {EVAL_GATE}")
        return None

    if dry_run:
        return {
            "score": 0,
            "max_score": MAX_SCORE,
            "pass_rate": 0.0,
            "verdict": "DRY-RUN",
            "checks": [],
            "ts": datetime.now(timezone.utc).isoformat(),
            "_dry_run": True,
        }

    try:
        proc = subprocess.run(
            [sys.executable, str(EVAL_GATE), str(brief_path)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        log(f"ERROR: eval-gate timed out on {brief_path}")
        return None
    except Exception as e:
        log(f"ERROR: eval-gate failed on {brief_path}: {e}")
        return None

    score = None
    max_score = None
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if line.startswith("Score:"):
            # "Score: 7/9 = 78%"
            try:
                head = line.split("Score:", 1)[1].strip()
                frac = head.split("=", 1)[0].strip()  # "7/9"
                num, den = frac.split("/")
                score = int(num.strip())
                max_score = int(den.strip())
            except Exception:
                pass

    if score is None:
        log(f"WARN: could not parse score from eval-gate stdout ({brief_path})")
        return None

    verdict = "PASS" if proc.returncode == 0 else "FAIL"
    pass_rate = score / max_score if max_score else 0.0
    return {
        "score": score,
        "max_score": max_score,
        "pass_rate": pass_rate,
        "verdict": verdict,
        "ts": datetime.now(timezone.utc).isoformat(),
        "_raw_returncode": proc.returncode,
    }


# ---------------------------------------------------------------------------
# Brief footer
# ---------------------------------------------------------------------------

def brief_already_scored(brief_path: Path) -> bool:
    """Check the brief for an existing footer so we don't double-append."""
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception:
        return False
    return FOOTER_PREFIX in text


def append_footer(brief_path: Path, result: dict, agent_name: str, dry_run: bool) -> bool:
    """Append the eval-gate footer to the brief. Idempotent."""
    if dry_run:
        return True
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception as e:
        log(f"ERROR: cannot read brief {brief_path}: {e}")
        return False

    if FOOTER_PREFIX in text:
        # Already scored — replace the previous footer so scores stay current
        lines = text.splitlines()
        kept = [l for l in lines if not l.startswith(FOOTER_PREFIX)]
        text = "\n".join(kept).rstrip() + "\n"

    footer = (
        f"\n{FOOTER_PREFIX} {result['score']}/{result['max_score']} {result['verdict']} "
        f"(agent={agent_name}, ts={result['ts']})\n"
    )
    try:
        with brief_path.open("a", encoding="utf-8") as f:
            f.write(footer)
    except Exception as e:
        log(f"ERROR: cannot write footer to {brief_path}: {e}")
        return False
    return True


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

def send_evolution_alert(message: str) -> bool:
    """Best-effort Evolution POST. Never raises; returns False on any failure."""
    if not EVOLUTION_KEY or not ALERT_RECIPIENT:
        return False
    try:
        req = urllib.request.Request(
            f"{EVOLUTION_URL}/message/sendText/{ALERT_RECIPIENT}",
            data=json.dumps({"text": message}).encode(),
            headers={
                "apikey": EVOLUTION_KEY,
                "Content-Type": "application/json",
            },
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, Exception):
        return False


def maybe_alert(agent_name: str, brief_path: Path, result: dict, dry_run: bool = False) -> None:
    if result["score"] >= ALERT_THRESHOLD:
        return
    msg = (
        f"⚠️ eval-gate LOW score: {agent_name} scored {result['score']}/"
        f"{result['max_score']} {result['verdict']} on {Path(brief_path).name}"
    )
    if dry_run:
        log(f"ALERT (dry-run, suppressed): {msg}")
        return
    sent = send_evolution_alert(msg)
    log(f"ALERT: {msg} (sent={sent})")


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_outbox_dirs() -> list[Path]:
    """All agent outbox directories under /opt/data/agents/."""
    outboxes: list[Path] = []
    if not AGENTS_DIR.exists():
        return outboxes
    for child in sorted(AGENTS_DIR.iterdir()):
        if not child.is_dir():
            continue
        outbox = child / "outbox"
        if outbox.is_dir():
            outboxes.append(outbox)
    return outboxes


def discover_briefs(limit_mtime: float | None = None) -> list[tuple[str, Path]]:
    """Return [(agent_name, brief_path), ...] for every .md in every outbox.

    If limit_mtime is set, only briefs with mtime >= limit_mtime are returned
    (used by the poll loop to pick up only new files since last sweep).
    """
    found: list[tuple[str, Path]] = []
    for outbox in discover_outbox_dirs():
        agent_name = outbox.parent.name
        try:
            entries = sorted(outbox.glob("*.md"))
        except Exception:
            continue
        for brief in entries:
            if limit_mtime is not None:
                try:
                    if brief.stat().st_mtime < limit_mtime:
                        continue
                except Exception:
                    continue
            found.append((agent_name, brief))
    return found


# ---------------------------------------------------------------------------
# Core sweep
# ---------------------------------------------------------------------------

def sweep_once(dry_run: bool = False, log_each: bool = True) -> dict:
    """Run one full pass over every outbox. Returns a small summary dict."""
    state = load_state()
    briefs = discover_briefs()

    scored = 0
    skipped = 0
    failed = 0
    alerted = 0

    for agent_name, brief_path in briefs:
        result = run_eval_gate(brief_path, dry_run=dry_run)
        if result is None:
            failed += 1
            continue

        # Append footer to brief (idempotent)
        if not append_footer(brief_path, result, agent_name, dry_run=dry_run):
            failed += 1
            continue

        # Update eval-per-agent.json (idempotent — append within the per-agent array)
        if not dry_run:
            bucket = state.setdefault("by_agent", {}).setdefault(agent_name, [])
            entry = {
                "agent": agent_name,
                "brief_path": str(brief_path),
                "score": result["score"],
                "max_score": result["max_score"],
                "pass_rate": result.get("pass_rate"),
                "verdict": result["verdict"],
                "ts": result["ts"],
            }
            # Cap per-agent history at the last 10 entries to keep file lean
            bucket.append(entry)
            if len(bucket) > 10:
                bucket[:] = bucket[-10:]

            state["total"] = state.get("total", 0) + 1
            if result["verdict"] == "PASS":
                state["passed"] = state.get("passed", 0) + 1
            else:
                state["failed"] = state.get("failed", 0) + 1

        scored += 1

        # Alert on low score
        if result["score"] < ALERT_THRESHOLD:
            maybe_alert(agent_name, brief_path, result, dry_run=dry_run)
            alerted += 1

        if log_each:
            log(
                f"scored {agent_name}/{brief_path.name}: "
                f"{result['score']}/{result['max_score']} {result['verdict']}"
            )

    if not dry_run:
        save_state(state)

    return {
        "scanned": len(briefs),
        "scored": scored,
        "skipped": skipped,
        "failed": failed,
        "alerted": alerted,
        "dry_run": dry_run,
    }


# ---------------------------------------------------------------------------
# Poll mode
# ---------------------------------------------------------------------------

def poll_loop(dry_run: bool = False) -> int:
    """Long-lived poller — runs sweep_once() every POLL_INTERVAL_SECS.

    Tracks the last mtime seen so each tick only checks new/modified files.
    Returns 0 on clean shutdown via SIGTERM.
    """
    log(f"poll loop starting (interval={POLL_INTERVAL_SECS}s, dry_run={dry_run})")
    last_seen_mtime = time.time() - POLL_INTERVAL_SECS  # look back one tick on start
    try:
        while True:
            briefs = discover_briefs(limit_mtime=last_seen_mtime)
            if briefs:
                # Run sweep on the full set (sweep_once is already idempotent)
                # but we tighten the log noise to just the new ones.
                log(f"poll: {len(briefs)} new/modified brief(s) since last tick")
                summary = sweep_once(dry_run=dry_run, log_each=True)
                log(f"poll summary: {summary}")
            time.sleep(POLL_INTERVAL_SECS)
    except KeyboardInterrupt:
        log("poll loop interrupted, exiting")
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="aiw-eval-post-brief-hook.py",
        description=(
            "Post-brief eval-gate hook. Polls /opt/data/agents/<dept>/outbox/ "
            "for new .md files, runs the existing 9-check eval-gate.py on "
            "each one, appends a score footer to the brief, and updates "
            "/opt/data/state/eval-per-agent.json. Alerts via Evolution API "
            "if score < 7."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 aiw-eval-post-brief-hook.py              # one-shot sweep\n"
            "  python3 aiw-eval-post-brief-hook.py --dry-run    # preview, no writes\n"
            "  python3 aiw-eval-post-brief-hook.py --poll       # long-lived poller\n"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Score briefs and log what would happen, but do NOT write to the "
             "brief files or eval-per-agent.json.",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        help="Run as a long-lived poller, sweeping every 30s instead of one-shot.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-brief log lines (summary line still printed).",
    )
    args = parser.parse_args()

    if args.dry_run:
        log("=== DRY RUN — no writes will be made ===")

    if args.poll:
        return poll_loop(dry_run=args.dry_run)

    summary = sweep_once(dry_run=args.dry_run, log_each=not args.quiet)
    log(f"sweep summary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
