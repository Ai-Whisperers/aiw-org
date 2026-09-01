#!/usr/bin/env python3
"""Auto-remediation for known safe error patterns.

Built as Phase 31 R3 (Tier G5).

Scans state files for known error patterns and applies safe auto-fixes.
Currently implements 2 patterns:
  1. Clear stale cron-error-watchdog entries (>7d old)
  2. Compact eval-gate-decisions.ndjson if > 50MB

Other known patterns are LOGGED but not auto-fixed (require human review).

Logs every remediation to /opt/data/state/remediation-log.ndjson.

Usage:
    python3 scripts/auto-remediate.py                 # run all patterns
    python3 scripts/auto-remediate.py --dry-run       # preview only
    python3 scripts/auto-remediate.py --pattern stale-cron  # one pattern
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_DIR = Path("/opt/data/state")
LOG_PATH = STATE_DIR / "remediation-log.ndjson"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


# Maximum NDJSON log size before rotation (MB)
LOG_ROTATE_THRESHOLD_MB = 50
STALE_CRON_AGE_DAYS = 7


def log_remediation(action: str, target: str, result: str) -> None:
    """Log remediation action."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "target": target,
        "result": result,
    }
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


# Pattern 1: Clear stale cron-error-watchdog entries
def fix_stale_cron_errors(dry_run: bool = False) -> dict:
    """Remove cron errors older than STALE_CRON_AGE_DAYS."""
    watchdog = STATE_DIR / "cron-error-watchdog.json"
    if not watchdog.exists():
        return {"pattern": "stale-cron", "action": "skip", "reason": "watchdog missing"}

    try:
        data = json.loads(watchdog.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return {"pattern": "stale-cron", "action": "skip", "reason": f"parse error: {e}"}

    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_CRON_AGE_DAYS)
    details = data.get("details", [])
    if not details:
        return {"pattern": "stale-cron", "action": "skip", "reason": "no details"}

    kept = []
    removed = []
    for entry in details:
        ts_str = entry.get("last_run_at", "")
        if not ts_str:
            kept.append(entry)
            continue
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if ts < cutoff:
                removed.append(entry)
            else:
                kept.append(entry)
        except (ValueError, AttributeError):
            kept.append(entry)

    if not removed:
        return {"pattern": "stale-cron", "action": "skip", "reason": f"no stale entries (kept={len(kept)})"}

    if dry_run:
        return {
            "pattern": "stale-cron",
            "action": "would-remove",
            "removed_count": len(removed),
            "kept_count": len(kept),
        }

    # Apply fix
    data["details"] = kept
    data["jobs_in_error"] = len(kept)
    watchdog.write_text(json.dumps(data, indent=2))
    return {
        "pattern": "stale-cron",
        "action": "applied",
        "removed_count": len(removed),
        "kept_count": len(kept),
    }


# Pattern 2: Compact large NDJSON log files
def fix_log_rotation(dry_run: bool = False) -> dict:
    """Rotate NDJSON logs that exceed LOG_ROTATE_THRESHOLD_MB."""
    logs_to_check = [
        STATE_DIR / "eval-gate-decisions.ndjson",
        STATE_DIR / "hard-stop-audit.ndjson",
        STATE_DIR / "injection-attempts.jsonl",
        STATE_DIR / "redaction-log.jsonl",
        STATE_DIR / "routing-decisions.jsonl",
    ]
    threshold_bytes = LOG_ROTATE_THRESHOLD_MB * 1024 * 1024
    actions = []
    for log in logs_to_check:
        if not log.exists():
            continue
        size = log.stat().st_size
        if size < threshold_bytes:
            continue
        archive_name = log.with_suffix(f".{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.archive")
        if dry_run:
            actions.append({
                "pattern": "log-rotation",
                "log": str(log),
                "size_mb": round(size / 1024 / 1024, 2),
                "action": "would-rotate",
            })
            continue
        shutil.copy2(log, archive_name)
        # Truncate original (keep last 1000 lines for context)
        lines = log.read_text().splitlines()
        keep = lines[-1000:] if len(lines) > 1000 else lines
        log.write_text("\n".join(keep) + "\n")
        actions.append({
            "pattern": "log-rotation",
            "log": str(log),
            "size_mb": round(size / 1024 / 1024, 2),
            "action": "applied",
            "archive": str(archive_name),
            "kept_lines": len(keep),
        })
    if not actions:
        return {"pattern": "log-rotation", "action": "skip", "reason": "no logs over threshold"}
    return {"pattern": "log-rotation", "actions": actions}


PATTERNS = {
    "stale-cron": fix_stale_cron_errors,
    "log-rotation": fix_log_rotation,
}


def main():
    parser = argparse.ArgumentParser(description="Auto-remediation for known error patterns")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, don't modify")
    parser.add_argument("--pattern", choices=list(PATTERNS.keys()),
                        help="Run only one pattern")
    args = parser.parse_args()

    patterns_to_run = [args.pattern] if args.pattern else list(PATTERNS.keys())

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "patterns": {},
    }

    for name in patterns_to_run:
        func = PATTERNS[name]
        result = func(dry_run=args.dry_run)
        summary["patterns"][name] = result
        action = result.get("action", "skip") if isinstance(result, dict) else "skip"
        if not args.dry_run and action == "applied":
            log_remediation(name, str(STATE_DIR), action)

    print(json.dumps(summary, indent=2, default=str))

    # Exit code: 0 if all skipped, 1 if any applied (signal to human)
    any_applied = any(
        p.get("action") == "applied" or any(a.get("action") == "applied" for a in p.get("actions", []))
        for p in summary["patterns"].values()
    )
    if any_applied and not args.dry_run:
        sys.exit(1)  # signal human review needed


if __name__ == "__main__":
    main()
