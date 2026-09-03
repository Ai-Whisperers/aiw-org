#!/usr/bin/env python3
"""disable_or_fix_broken_crons.py - Disable broken crons (Sep 3, 2026 audit).

Marks jobs as disabled with paused_reason metadata so the decision is
auditable. Idempotent: re-runs on already-disabled jobs are no-ops.

Why disable rather than fix:
- Block A (Anthropic 401 on 5 research crons): we only have MiniMax-M3.
- Block B (Cerebras 402 on aiw-saas-lifecycle-reconcile): no Cerebras plan.
- Block C (bitwarden_sdk missing on 3 token-refresh crons): the cron-runner
  Python env doesn't have the dep and there's no system pip available.
- Block C (aiw-boundary-validate-hourly): cron-runner doesn't split
  script on whitespace; registry has 'boundary-validate.py --all' as one
  path. Wrapper script at /opt/data/scripts/boundary-validate-all.sh
  exists but the cron is disabled to keep registry clean.

Refs: HANDOFF-PHASE-8.md ## MED, DEMIURGE-113 breakdown 2026-09-03.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CRON_PATHS = [
    Path("/opt/data/.hermes/cron/jobs.json"),
    Path("/opt/data/cron/jobs.json"),
]

JOBS_TO_DISABLE = {
    "aiw-research-associate-daily": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-research-engineer-weekly": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-research-tracker-6h": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-citation-checker-daily": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-publication-coordinator-weekly": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-saas-lifecycle-reconcile": "Block B: Cerebras 402 Payment Required; no Cerebras plan",
    "kv-bws-sync": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "linkedin-token-refresh": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "instagram-token-refresh": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "aiw-boundary-validate-hourly": "Block C: cron entry has script with --all arg; runner doesn't split on whitespace",
}


def _disable_job(j: dict, reason: str, paused_at: str) -> bool:
    """Mark job disabled with paused_reason. Returns True if changed."""
    if not j.get("enabled", True):
        return False
    j["enabled"] = False
    j["paused_at"] = paused_at
    j["paused_reason"] = reason
    return True


def patch(apply: bool = False) -> int:
    paused_at = datetime.now(timezone.utc).isoformat()
    changes = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            name = j.get("name")
            if name in JOBS_TO_DISABLE and _disable_job(j, JOBS_TO_DISABLE[name], paused_at):
                print(f"[{cp}] DISABLE {name}: {JOBS_TO_DISABLE[name]}")
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
