#!/usr/bin/env python3
"""fix_intake_cron_args.py - Fix arg-error crons via wrapper scripts.

The cron-runner (/opt/hermes/cron/scheduler.py) does NOT support args
in the 'script' field. It passes only [python_exe, str(path)] to
subprocess.run. So you can't write:

    "script": "/opt/data/scripts/intake.py --dept research"

because the whole string is treated as ONE path.

Fix: create wrapper scripts at /opt/data/scripts/ that hardcode the
args, then update the cron entries to point at the wrappers.

This PR ships:
- /opt/data/scripts/intake-{sales,finance,operations,research,
  engineering,people,board}.sh — 7 wrappers, each `exec intake.py
  --dept <name> --process`
- /opt/data/scripts/eval-gate-decisions-summary.sh — 1 wrapper,
  picks 'eval-gate-runner' as the agent

Cron registry updates: each affected job's 'script' field is changed
to point at the corresponding wrapper.

Idempotent. Dry-run by default; --apply to write.
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


# Map old script ('/opt/data/scripts/intake.py') -> new wrapper script
# (per-dept or per-purpose).
SCRIPT_FIXES = {
    "aiw-intake-sales-10min": "/opt/data/scripts/intake-sales.sh",
    "aiw-intake-finance-10min": "/opt/data/scripts/intake-finance.sh",
    "aiw-intake-operations-10min": "/opt/data/scripts/intake-operations.sh",
    "aiw-intake-research-10min": "/opt/data/scripts/intake-research.sh",
    "aiw-intake-engineering-10min": "/opt/data/scripts/intake-engineering.sh",
    "aiw-intake-people-10min": "/opt/data/scripts/intake-people.sh",
    "aiw-intake-board-10min": "/opt/data/scripts/intake-board.sh",
    "aiw-eval-gate-decisions-summary": "/opt/data/scripts/eval-gate-decisions-summary.sh",
}


def patch(apply: bool = False) -> int:
    changes = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            name = j.get("name")
            if name not in SCRIPT_FIXES:
                continue
            new_script = SCRIPT_FIXES[name]
            old_script = j.get("script", "")
            if old_script == new_script:
                continue
            print(f"[{cp}] {name}: script -> {new_script}")
            if apply:
                j["script"] = new_script
            changes += 1
        if apply and changes:
            cp.write_text(json.dumps(data, indent=2) + "\n")
    if not apply:
        print(f"\nDRY RUN: {changes} cron entries would change. Re-run with --apply.")
    elif changes:
        print(f"\nApplied {changes} changes.")
    else:
        print("\nNo changes needed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
