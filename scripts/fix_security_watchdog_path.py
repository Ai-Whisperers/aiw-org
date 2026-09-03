#!/usr/bin/env python3
"""fix_security_watchdog_path.py - Fix aiw-security-watchdog-30min outbox path.

The cron registry at /opt/data/.hermes/cron/jobs.json references the
correct PROMPT.md path (under 04-engineering/) but the OUTBOX write
path is the ghost directory at /opt/data/agents/security-watchdog-30min/
instead of /opt/data/agents/04-engineering/security-watchdog-30min/.

Effect: every 30 min the agent writes to the ghost dir, accumulating
~70KB/day of orphan output that the canonical outbox should be
receiving.

This script rewrites the cron entry's outbox path. Idempotent.

Usage:
    python scripts/fix_security_watchdog_path.py             # dry-run
    python scripts/fix_security_watchdog_path.py --apply     # write changes

Refs: HANDOFF-PHASE-8.md CRITICAL #1
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CRON_PATHS = [
    Path("/opt/data/.hermes/cron/jobs.json"),
    Path("/opt/data/cron/jobs.json"),
]

OLD_OUTBOX_FRAGMENT = "/opt/data/agents/security-watchdog-30min/outbox/"
NEW_OUTBOX_FRAGMENT = "/opt/data/agents/04-engineering/security-watchdog-30min/outbox/"

TARGET_JOB_NAME = "aiw-security-watchdog-30min"


def patch(apply: bool = False) -> int:
    changes = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            if j.get("name") != TARGET_JOB_NAME:
                continue
            prompt = j.get("prompt", "")
            if OLD_OUTBOX_FRAGMENT in prompt and NEW_OUTBOX_FRAGMENT not in prompt:
                new_prompt = prompt.replace(OLD_OUTBOX_FRAGMENT, NEW_OUTBOX_FRAGMENT)
                print(f"[{cp}] {j['name']}: patching outbox path")
                print(f"  OLD: ...{OLD_OUTBOX_FRAGMENT[-50:]}")
                print(f"  NEW: ...{NEW_OUTBOX_FRAGMENT[-50:]}")
                if apply:
                    j["prompt"] = new_prompt
                changes += 1
            elif NEW_OUTBOX_FRAGMENT in prompt:
                pass
            else:
                print(f"[{cp}] {j['name']}: prompt does not reference outbox path - skipping")
        if apply and changes:
            cp.write_text(json.dumps(data, indent=2) + "\n")
    if not apply:
        print(f"\nDRY RUN: {changes} jobs would change. Re-run with --apply.")
    elif changes:
        print(f"\nApplied {changes} changes.")
    else:
        print(f"\nNo changes needed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
