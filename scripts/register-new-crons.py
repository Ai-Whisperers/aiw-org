#!/usr/bin/env python3
"""Register new cron jobs for Phase 1+2 implementation plan.

Built Phase 7 R5 (implementation plan §4 Phase 1.2, 1.4, 2.4, 2.7).

Adds 4 new no-agent crons:
  1. aiw-dora-metrics-weekly       (Monday 09:00 UTC) — DORA aggregator
  2. aiw-slo-tracker-daily         (daily 08:00 UTC)   — SLO tracker
  3. aiw-citation-audit-weekly     (Sunday 22:00 UTC)  — citation-coverage-enforcer
  4. aiw-org-chart-review          (1st of quarter, 09:00 UTC) — quarterly review

Writes to BOTH /opt/data/cron/jobs.json and /opt/data/.hermes/cron/jobs.json
(per cron-sync invariant).

Usage:
    python3 scripts/register-new-crons.py            # add all (idempotent)
    python3 scripts/register-new-crons.py --dry-run # print what would be added
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

CANON_JOBS = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY_JOBS = Path("/opt/data/cron/jobs.json")

NEW_CRONS = [
    {
        "name": "aiw-dora-metrics-weekly",
        "script": "/opt/data/agents/scripts/dora-metrics-aggregator.py",
        "schedule": {"kind": "cron", "expression": "0 9 * * 1", "display": "Mon 09:00 UTC"},
        "description": "Compute DORA 4-metrics from git log + cron errors. Built Phase 7 R5 (Plan §4 Phase 1.2).",
    },
    {
        "name": "aiw-slo-tracker-daily",
        "script": "/opt/data/agents/scripts/slo-error-budget-tracker.py",
        "schedule": {"kind": "cron", "expression": "0 8 * * *", "display": "daily 08:00 UTC"},
        "description": "Compute per-service SLO + error budget. Built Phase 7 R5 (Plan §4 Phase 1.4).",
    },
    {
        "name": "aiw-citation-audit-weekly",
        "script": "/opt/data/agents/scripts/citation-coverage-enforcer.py",
        "schedule": {"kind": "cron", "expression": "0 22 * * 0", "display": "Sun 22:00 UTC"},
        "description": "Scan research/ for citation coverage; write state. Built Phase 7 R5 (Plan §4 Phase 2.4).",
    },
    {
        "name": "aiw-org-chart-review",
        "script": "/opt/data/agents/scripts/org-chart-review.py",
        "schedule": {"kind": "cron", "expression": "0 9 1 1,4,7,10 *", "display": "1st of quarter 09:00 UTC"},
        "description": "Quarterly org chart review; flag re-orgs. Built Phase 7 R5 (Plan §4 Phase 2.7).",
    },
]


def cron_template(spec: dict) -> dict:
    """Build a full cron job entry matching existing schema."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": uuid.uuid4().hex[:12],
        "name": spec["name"],
        "prompt": "",
        "skills": [],
        "skill": None,
        "model": "primary",
        "provider": "litellm",
        "base_url": None,
        "script": spec["script"],
        "no_agent": True,
        "context_from": None,
        "schedule": spec["schedule"],
        "schedule_display": spec["schedule"]["display"],
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "created_at": now,
        "next_run_at": None,
        "last_run_at": None,
        "last_status": None,
        "last_error": None,
        "last_delivery_error": None,
        "deliver": "local",
        "origin": None,
        "enabled_toolsets": None,
        "workdir": "/opt/data/agents",
        "fire_claim": None,
        "description": spec.get("description", ""),
    }


def has_cron(jobs: list, name: str) -> bool:
    return any(j.get("name") == name for j in jobs)


def register(dry_run: bool = False) -> int:
    canon = json.loads(CANON_JOBS.read_text())
    gateway = json.loads(GATEWAY_JOBS.read_text())

    canon_jobs = canon.get("jobs", [])
    gateway_jobs = gateway.get("jobs", [])

    added = 0
    skipped = 0
    missing_scripts = []

    for spec in NEW_CRONS:
        # Check if the script exists
        if not Path(spec["script"]).exists():
            missing_scripts.append(spec["script"])
            print(f"  SKIP {spec['name']}: script missing ({spec['script']})")
            skipped += 1
            continue

        new_job = cron_template(spec)

        # Canonical
        if has_cron(canon_jobs, spec["name"]):
            print(f"  SKIP {spec['name']}: already in canon")
            skipped += 1
        else:
            if not dry_run:
                canon_jobs.append(new_job)
            print(f"  ADD {spec['name']} → canon")
            added += 1

        # Gateway
        if has_cron(gateway_jobs, spec["name"]):
            print(f"  SKIP {spec['name']}: already in gateway")
        else:
            if not dry_run:
                gateway_jobs.append(dict(new_job))  # copy
            print(f"  ADD {spec['name']} → gateway")
            added += 1

    if not dry_run and added > 0:
        now = datetime.now(timezone.utc).isoformat()
        canon["updated_at"] = now
        gateway["updated_at"] = now
        CANON_JOBS.write_text(json.dumps(canon, indent=2))
        GATEWAY_JOBS.write_text(json.dumps(gateway, indent=2))
        print(f"\n  → Wrote both jobs.json files ({added} new entries)")

    print(f"\n{added} added, {skipped} skipped, {len(missing_scripts)} missing scripts")

    if missing_scripts and not dry_run:
        print("\nWARNING: Some scripts are missing — those crons will be skipped.")
        print("Run with --dry-run to see what would be added without modifying files.")
        return 1

    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Register crons")
    p.add_argument("--dry-run", action="store_true", help="Show what would be added")
    args = p.parse_args(argv)
    return register(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())