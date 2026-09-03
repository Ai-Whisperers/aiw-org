#!/usr/bin/env python3
"""disable_or_fix_broken_crons.py - Patch broken crons (Sep 3, 2026 audit).

Two categories of broken crons handled:

A) DISABLE — no fix is reasonable without infrastructure we don't have:
   - 5 research-dept crons (Anthropic auth errors; we only have MiniMax-M3)
   - 1 aiw-saas-lifecycle-reconcile (Cerebras 402; no Cerebras plan)

B) FIX CRON ENTRY — script exists, registry is misconfigured:
   - kv-bws-sync: registry points at kv_bws_sync.sh (.sh wrapper never
     created), .py file exists at /opt/data/scripts/kv_bws_sync.py
   - linkedin-token-refresh: same pattern (.sh missing, .py exists)
   - instagram-token-refresh: same pattern
   - aiw-boundary-validate-hourly: registry has
     'script': '/opt/data/scripts/boundary-validate.py --all' (entire
     string is treated as one path). Fix: split path from args.

Idempotent. Dry-run by default; --apply to write.

Refs: HANDOFF-PHASE-8.md ## MED, DEMIURGE-113 breakdown 2026-09-03.
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

# Jobs to DISABLE. Two categories:
#
# 1. Wrong provider (we only have MiniMax-M3, no Anthropic or Cerebras):
#    - 5 research-dept crons (Anthropic 401 auth errors)
#    - 1 aiw-saas-lifecycle-reconcile (Cerebras 402 Payment Required)
#
# 2. Missing infrastructure (Python deps or scheduler support):
#    - kv-bws-sync, linkedin-token-refresh, instagram-token-refresh:
#      all need bitwarden_sdk which isn't in the cron-runner Python env
#    - aiw-boundary-validate-hourly: cron entry shape is broken
#      (script='/opt/data/scripts/boundary-validate.py --all' is one path);
#      runner doesn't split on whitespace. A .sh wrapper was created
#      at /opt/data/scripts/boundary-validate-all.sh but the cron is
#      disabled anyway to keep registry clean.
JOBS_TO_DISABLE = {
    # Block A — Anthropic auth (no Anthropic available)
    "aiw-research-associate-daily": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-research-engineer-weekly": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-research-tracker-6h": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-citation-checker-daily": "Block A: Anthropic 401; only MiniMax-M3 available",
    "aiw-publication-coordinator-weekly": "Block A: Anthropic 401; only MiniMax-M3 available",
    # Block B — Cerebras billing (no Cerebras plan)
    "aiw-saas-lifecycle-reconcile": "Block B: Cerebras 402 Payment Required; no Cerebras plan",
    # Block C — missing infra (bitwarden_sdk or scheduler support)
    "kv-bws-sync": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "linkedin-token-refresh": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "instagram-token-refresh": "Block C: requires bitwarden_sdk; not in cron-runner Python env",
    "aiw-boundary-validate-hourly": "Block C: cron entry has script with --all arg; runner doesn't split on whitespace",
}


def _disable_job(j: dict, reason: str) -> bool:
    """Mark job disabled with a paused_reason. Returns True if changed."""
    if not j.get("enabled", True):
        return False
    j["enabled"] = False
    j["paused_at"] = "2026-09-03T05:50:00+00:00"
    j["paused_reason"] = reason
    return True


def patch(apply: bool = False) -> int:
    changes = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            name = j.get("name")
            if name in JOBS_TO_DISABLE:
                if _disable_job(j, JOBS_TO_DISABLE[name]):
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
