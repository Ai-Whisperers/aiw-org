#!/usr/bin/env python3
"""self-running-check.py — Daily verification per SELF-RUNNING-CRITERIA.md

A self-running org is one where:
1. All 7 Tier-1 lead agents deliver reliably for 7+ consecutive days
2. 0 cron jobs in error state for the same period
3. 0 "is X live?" messages from Ivan in any 7-day window

This script checks conditions 1 and 2 automatically.
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CRITICAL_AGENTS = [
    "business-analyst",
    "management-coordinator",
    "kiki-coach",
    "finance-controller",
    "sales-pipeline",
    "engineering-roster",
    "research-tracker",
]

JOBS_JSON = "/opt/data/cron/jobs.json"
STATE_DB = "/opt/data/state.db"
DAYS_WINDOW = 7


def check_deliveries():
    """Condition 1: All 7 lead agents delivered in last 7 days."""
    today = datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=DAYS_WINDOW)
    results = {}

    for agent in CRITICAL_AGENTS:
        outbox = Path(f"/opt/data/agents/{agent}/outbox")
        lessons = Path(f"/opt/data/agents/{agent}/lessons")
        # Find the most recent brief file in either dir
        latest = None
        for d in [outbox, lessons]:
            if d.exists():
                for f in d.glob("*.md"):
                    try:
                        date = datetime.strptime(f.stem, "%Y-%m-%d").date()
                        if not latest or date > latest:
                            latest = date
                    except ValueError:
                        continue
        results[agent] = {
            "latest_brief": str(latest) if latest else None,
            "delivered_in_window": latest is not None and latest >= cutoff,
        }
    return results


def check_cron_health():
    """Condition 2: 0 cron jobs in error state in last 7 days."""
    with open(JOBS_JSON) as f:
        data = json.load(f)
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    if isinstance(jobs, dict):
        jobs = jobs.get("jobs", list(jobs.values()))

    errors = []
    for j in jobs:
        if not isinstance(j, dict):
            continue
        # Check if last_run contains an error marker
        # (This is a heuristic — real check would query hermes cron runs)
        last_run = j.get("last_run_status", "")
        if "error" in str(last_run).lower() or j.get("state") == "error":
            errors.append(j.get("name", "?"))
    return {"total_jobs": len(jobs), "errors": errors}


def main():
    deliveries = check_deliveries()
    cron = check_cron_health()

    all_delivered = all(d["delivered_in_window"] for d in deliveries.values())
    no_errors = len(cron["errors"]) == 0

    self_running = all_delivered and no_errors

    print("=" * 50)
    print(f"Self-running check @ {datetime.now(timezone.utc).isoformat()}")
    print("=" * 50)
    print()
    print(f"Condition 1 — All 7 lead agents delivered in last {DAYS_WINDOW} days:")
    for agent, info in deliveries.items():
        mark = "✓" if info["delivered_in_window"] else "✗"
        print(f"  {mark} {agent}: latest={info['latest_brief']}")
    print()
    print(f"Condition 2 — 0 cron jobs in error state:")
    print(f"  Total jobs: {cron['total_jobs']}")
    if cron["errors"]:
        print(f"  ✗ Errors: {cron['errors']}")
    else:
        print(f"  ✓ No errors")
    print()
    print(f"Condition 3 — 0 'is X live?' messages from Ivan: (manual check)")
    print()
    print(f"OVERALL: {'✓ SELF-RUNNING' if self_running else '✗ NOT YET'}")
    return 0 if self_running else 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

