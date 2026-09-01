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


# Pattern 3: Compact eval-gate-decisions if > 1MB (more aggressive than log-rotation)
EVAL_GATE_COMPACT_THRESHOLD_KB = 1024  # 1MB
EVAL_GATE_KEEP_LINES = 500

def fix_eval_gate_compaction(dry_run: bool = False) -> dict:
    """Compact eval-gate-decisions.ndjson if it exceeds 1MB.

    This is a more aggressive version of log-rotation specifically for
    eval-gate-decisions, which grows 100+ entries/day under heavy use.
    """
    log = STATE_DIR / "eval-gate-decisions.ndjson"
    if not log.exists():
        return {"pattern": "eval-gate-compaction", "action": "skip", "reason": "log missing"}
    size = log.stat().st_size
    threshold_bytes = EVAL_GATE_COMPACT_THRESHOLD_KB * 1024
    if size < threshold_bytes:
        return {"pattern": "eval-gate-compaction", "action": "skip",
                "reason": f"size {round(size/1024, 1)}KB < threshold {EVAL_GATE_COMPACT_THRESHOLD_KB}KB"}
    if dry_run:
        return {"pattern": "eval-gate-compaction", "action": "would-compact",
                "size_kb": round(size / 1024, 1),
                "would_keep": EVAL_GATE_KEEP_LINES}
    # Archive + truncate
    archive_name = log.with_suffix(f".{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.archive")
    shutil.copy2(log, archive_name)
    lines = log.read_text().splitlines()
    keep = lines[-EVAL_GATE_KEEP_LINES:] if len(lines) > EVAL_GATE_KEEP_LINES else lines
    log.write_text("\n".join(keep) + "\n")
    return {"pattern": "eval-gate-compaction", "action": "applied",
            "size_kb_before": round(size / 1024, 1),
            "lines_kept": len(keep),
            "archive": str(archive_name)}


# Pattern 4: Deduplicate cron-error entries (same job + same error repeatedly)
def fix_cron_error_dedup(dry_run: bool = False) -> dict:
    """Remove duplicate consecutive cron error entries (same job+error).

    Cron watchdog sometimes logs the same failure repeatedly within minutes.
    Keep only the first occurrence of each (job, error) tuple.
    """
    watchdog = STATE_DIR / "cron-error-watchdog.json"
    if not watchdog.exists():
        return {"pattern": "cron-error-dedup", "action": "skip", "reason": "watchdog missing"}
    try:
        data = json.loads(watchdog.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return {"pattern": "cron-error-dedup", "action": "skip", "reason": f"parse error: {e}"}
    details = data.get("details", [])
    if not details:
        return {"pattern": "cron-error-dedup", "action": "skip", "reason": "no details"}
    # Keep first occurrence of each (name, error) tuple
    seen = set()
    unique = []
    duplicates = 0
    for entry in details:
        key = (entry.get("name"), entry.get("last_error"))
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(entry)
    if duplicates == 0:
        return {"pattern": "cron-error-dedup", "action": "skip",
                "reason": f"no duplicates (total={len(details)})"}
    if dry_run:
        return {"pattern": "cron-error-dedup", "action": "would-dedup",
                "duplicates": duplicates, "would_keep": len(unique)}
    data["details"] = unique
    data["jobs_in_error"] = len(unique)
    watchdog.write_text(json.dumps(data, indent=2))
    return {"pattern": "cron-error-dedup", "action": "applied",
            "duplicates_removed": duplicates, "kept": len(unique)}


# Pattern 5: Refresh schema drafts (Phase 30 G6) for stale state files
SCHEMA_REFRESH_AGE_DAYS = 30  # only refresh schemas where state is "fresh"

def fix_schema_refresh(dry_run: bool = False) -> dict:
    """Refresh out-of-date JSON schemas from live state files.

    For each schema in /opt/data/agents/schemas/, check if the corresponding
    state file has fields the schema doesn't know about. If so, log a
    recommendation (don't auto-modify — Kiki must review).
    """
    schema_dir = Path("/opt/data/agents/schemas")
    state_dirs = [Path("/opt/data/agents/state"), Path("/opt/data/state")]
    findings = []
    for schema_file in schema_dir.glob("*.schema.json"):
        schema_name = schema_file.name.replace(".schema.json", ".json")
        state_file = None
        for d in state_dirs:
            candidate = d / schema_name
            if candidate.exists():
                state_file = candidate
                break
        if not state_file:
            continue
        try:
            schema = json.loads(schema_file.read_text())
            state = json.loads(state_file.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(state, dict):
            continue
        schema_props = set(schema.get("properties", {}).keys())
        state_fields = set(state.keys())
        unknown = state_fields - schema_props
        if not unknown:
            continue
        if schema.get("additionalProperties") is True:
            continue  # schema is lenient
        findings.append({
            "schema": str(schema_file),
            "state": str(state_file),
            "unknown_fields": sorted(unknown),
            "count": len(unknown),
        })
    if not findings:
        return {"pattern": "schema-refresh", "action": "skip", "reason": "no schema gaps"}
    # Don't auto-modify schemas — too risky. Just report.
    return {"pattern": "schema-refresh", "action": "reported",
            "findings_count": len(findings),
            "findings": findings[:5],  # cap output
            "note": "manual review required (schemas not auto-modified)"}


PATTERNS = {
    "stale-cron": fix_stale_cron_errors,
    "log-rotation": fix_log_rotation,
    "eval-gate-compaction": fix_eval_gate_compaction,
    "cron-error-dedup": fix_cron_error_dedup,
    "schema-refresh": fix_schema_refresh,
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
