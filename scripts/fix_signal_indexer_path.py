#!/usr/bin/env python3
"""fix_signal_indexer_path.py - Fix aiw-signal-indexer cron script path.

The cron-runner policy restricts script paths to /opt/data/scripts/.
The script lives at /opt/data/agents/scripts/build-signal-index.sh,
outside the policy. The cron entry is rejected on every run:

    Blocked: script path resolves outside the scripts directory
    (/opt/data/scripts): '/opt/data/agents/scripts/build-signal-index.sh'

This script:
  1. Copies the script from /opt/data/agents/scripts/ to
     /opt/data/scripts/ (the canonical location).
  2. Updates the cron entry's script: field.
  3. Adds a backward-compat symlink at the original location pointing
     at the new canonical path.

Idempotent: re-running on an already-fixed system is a no-op.

Usage:
    python scripts/fix_signal_indexer_path.py             # dry-run
    python scripts/fix_signal_indexer_path.py --apply     # write changes

Refs: HANDOFF-PHASE-8.md CRITICAL #2
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

CRON_PATHS = [
    Path("/opt/data/.hermes/cron/jobs.json"),
    Path("/opt/data/cron/jobs.json"),
]

OLD_SCRIPT = Path("/opt/data/agents/scripts/build-signal-index.sh")
NEW_SCRIPT = Path("/opt/data/scripts/build-signal-index.sh")

TARGET_JOB_NAME = "aiw-signal-indexer"


def patch(apply: bool = False) -> int:
    changes = 0

    # Step 1: ensure NEW_SCRIPT exists.
    if OLD_SCRIPT.exists() and not NEW_SCRIPT.exists():
        print(f"Copying {OLD_SCRIPT} -> {NEW_SCRIPT}")
        if apply:
            NEW_SCRIPT.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(OLD_SCRIPT, NEW_SCRIPT)
            NEW_SCRIPT.chmod(0o755)
        changes += 1

    # Step 2: add backward-compat symlink at OLD_SCRIPT location.
    if OLD_SCRIPT.exists() and not OLD_SCRIPT.is_symlink():
        backup = OLD_SCRIPT.with_suffix(OLD_SCRIPT.suffix + ".real")
        print(f"Symlinking {OLD_SCRIPT} -> {NEW_SCRIPT}")
        print(f"  (backup of original at {backup})")
        if apply:
            shutil.move(str(OLD_SCRIPT), str(backup))
            OLD_SCRIPT.symlink_to(NEW_SCRIPT)
        changes += 1

    # Step 3: update cron entries.
    for cp in CRON_PATHS:
        if not cp.exists():
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            if j.get("name") != TARGET_JOB_NAME:
                continue
            if j.get("script") == str(OLD_SCRIPT):
                print(f"[{cp}] {j['name']}: updating script path")
                print(f"  OLD: {OLD_SCRIPT}")
                print(f"  NEW: {NEW_SCRIPT}")
                if apply:
                    j["script"] = str(NEW_SCRIPT)
                changes += 1
            elif j.get("script") == str(NEW_SCRIPT):
                pass  # already correct
            else:
                print(f"[{cp}] {j['name']}: script field is neither OLD nor NEW — skipping")
        if apply and changes:
            cp.write_text(json.dumps(data, indent=2) + "\n")

    if not apply:
        print(f"\nDRY RUN: {changes} operations would happen. Re-run with --apply.")
    elif changes:
        print(f"\nApplied {changes} operations.")
    else:
        print(f"\nNo changes needed (already correct).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
