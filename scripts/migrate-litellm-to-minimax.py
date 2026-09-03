#!/usr/bin/env python3
"""
migrate-litellm-to-minimax.py — Switch all litellm-primary jobs to minimax-oauth + MiniMax-M3.

Background: The litellm aliases (primary=Cerebras, fast=Nvidia, reasoning=timeout)
are ALL broken as of 2026-09-03 (Cerebras 402 Payment Required, Nvidia NIM 410 Gone).
This script migrates jobs that use these aliases to use the working minimax-oauth
provider with explicit MiniMax-M3 model.

Job list is hardcoded because the set of broken-alias jobs was determined at
the time of the audit. For new jobs, prefer provider=minimax-oauth + model=MiniMax-M3
from the start.

Idempotent. Reports what it changed.

Created: 2026-09-03 (AIW litellm-all-broken migration).
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

CANONICAL = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY = Path("/opt/data/cron/jobs.json")

# Jobs that need migration from litellm (broken) to minimax-oauth + MiniMax-M3
# Updated 2026-09-03 from /opt/data/.hermes/cron/jobs.json
TARGETS = {
    "aiw-delivery-tracker-monly",
    "aiw-academic-liaison-weekly",
    "aiw-instructional-designer-weekly",
    "aiw-ip-patent-specialist-monthly",
    "aiw-curator-evolver-weekly",
    "aiw-homunculus-weekly",
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not CANONICAL.exists():
        print(f"ERROR: {CANONICAL} not found", file=sys.stderr)
        return 1

    data = json.loads(CANONICAL.read_text())
    jobs = data["jobs"]

    migrated = []
    for j in jobs:
        if j["name"] in TARGETS and j.get("enabled"):
            old = (j.get("provider"), j.get("model"))
            if old == ("minimax-oauth", "MiniMax-M3"):
                continue  # Already migrated
            j["provider"] = "minimax-oauth"
            j["model"] = "MiniMax-M3"
            j["_last_modified_by"] = "migrate-litellm-to-minimax.py"
            j["_last_modified"] = "2026-09-03T16:40:00+00:00"
            migrated.append((j["name"], old, (j["provider"], j["model"])))

    if args.dry_run:
        print(f"[DRY-RUN] Would migrate {len(migrated)} jobs:")
    else:
        print(f"Migrated {len(migrated)} jobs:")
    for n, old, new in migrated:
        print(f"  {n}: {old} -> {new}")

    if migrated and not args.dry_run:
        tmp = CANONICAL.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(CANONICAL)
        shutil.copy2(CANONICAL, GATEWAY)
        print(f"\nCron registry updated (canonical + gateway)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
