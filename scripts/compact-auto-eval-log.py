#!/usr/bin/env python3
"""
compact-auto-eval-log.py — Compaction script for auto-eval-log.jsonl.

The auto-eval pipeline writes every evaluation result to /opt/data/state/auto-eval-log.jsonl
via eval-auto-trigger.py. Without rotation, this file grows unboundedly
(observed: 422 MB with 924K entries from disabled watchdog crons).

This script:
  1. Reads the current auto-eval-log.jsonl
  2. Filters out entries from disabled-cron agents that are >24h old
  3. Writes a compacted version
  4. Atomically swaps it in (writes to .tmp, renames)

Should run daily via cron. Idempotent.

Created: 2026-09-03 (AIW token audit followup).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("/opt/data/state/auto-eval-log.jsonl")
JOBS_FILE = Path("/opt/data/.hermes/cron/jobs.json")
BACKUP_DIR = Path("/opt/data/state")


def get_disabled_agent_names() -> set:
    """Return agent directory names (without aiw- prefix) for disabled cron jobs."""
    if not JOBS_FILE.exists():
        return set()
    data = json.loads(JOBS_FILE.read_text())
    disabled = set()
    for j in data.get("jobs", []):
        if j.get("enabled") or j.get("no_agent") or not j.get("model"):
            continue
        name = j["name"].replace("aiw-", "")
        disabled.add(name)
    return disabled


def main() -> int:
    if not LOG_FILE.exists():
        print(f"LOG_FILE not found: {LOG_FILE}")
        return 0

    disabled = get_disabled_agent_names()
    cutoff = datetime.now(timezone.utc).timestamp() - 24 * 3600

    keep_count = 0
    remove_count = 0
    keep_bytes = 0
    remove_bytes = 0

    tmp_path = LOG_FILE.with_suffix(".jsonl.tmp")
    with LOG_FILE.open() as src, tmp_path.open("w") as dst:
        for line in src:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                entry = json.loads(line)
                agent = entry.get("agent", "")
                ts_str = entry.get("ts", "")
                if not ts_str:
                    keep_count += 1
                    keep_bytes += len(line) + 1
                    dst.write(line + "\n")
                    continue
                # Parse ts (ISO 8601)
                try:
                    entry_ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()
                except (ValueError, AttributeError):
                    keep_count += 1
                    keep_bytes += len(line) + 1
                    dst.write(line + "\n")
                    continue

                if agent in disabled and entry_ts < cutoff:
                    remove_count += 1
                    remove_bytes += len(line) + 1
                else:
                    keep_count += 1
                    keep_bytes += len(line) + 1
                    dst.write(line + "\n")
            except json.JSONDecodeError:
                # Keep malformed lines as-is
                keep_count += 1
                keep_bytes += len(line) + 1
                dst.write(line + "\n")

    # Atomic swap
    if remove_count > 0:
        backup = BACKUP_DIR / f"auto-eval-log.jsonl.pre-compact-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.bak"
        try:
            shutil.copy2(LOG_FILE, backup)
        except Exception:
            pass
        shutil.move(str(tmp_path), str(LOG_FILE))
        print(f"Compacted: removed {remove_count} entries ({remove_bytes//1024} KB)")
        print(f"Kept: {keep_count} entries ({keep_bytes//1024} KB)")
        print(f"Backup: {backup}")
    else:
        tmp_path.unlink()
        print(f"No entries to remove (kept {keep_count})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
