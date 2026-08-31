#!/usr/bin/env python3
"""Cost reporting per cron — correlate jobs.json with cost-tracker.json.

Built as Phase 26 #10.

Reads:
  - /opt/data/.hermes/cron/jobs.json (cron definitions)
  - /opt/data/state/cost-tracker.json (per-agent costs)

Outputs:
  - /opt/data/state/cost-per-cron.json (per-cron cost breakdown)
  - Stdout summary

Schema of cost-per-cron.json:
    {
      "computed_at": "<ISO>",
      "total_jobs": <int>,
      "matched_jobs": <int>,
      "total_daily_usd": <float>,
      "top_10_by_daily": [{"cron_name": str, "daily_usd": float, "monthly_usd": float}, ...],
      "uncategorized": [{"cron_name": str}, ...],
      "no_cost_data": [{"cron_name": str, "runs_per_day": float}, ...]
    }
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

JOBS_FILE = Path("/opt/data/.hermes/cron/jobs.json")
COST_FILE = Path("/opt/data/state/cost-tracker.json")
OUTPUT_FILE = Path("/opt/data/state/cost-per-cron.json")


def _runs_per_day_from_schedule(schedule: dict) -> float:
    """Convert a cron expression to estimated runs/day."""
    if not isinstance(schedule, dict):
        return 1.0
    if schedule.get("kind") == "interval":
        minutes = schedule.get("minutes", 60)
        return (24 * 60) / minutes if minutes else 1.0
    expr = schedule.get("expr", "")
    # Naive parser: split on whitespace
    parts = expr.split()
    if len(parts) != 5:
        return 1.0
    minute, hour, dom, month, dow = parts

    # Start with 1, multiply by day-of-week factor, hour factor, minute factor
    runs_per_day = 1.0

    # DOW-based (weekly crons)
    if dow != "*":
        # Single weekday like "1" or list like "1,3,5"
        days = dow.split(",")
        runs_per_day = len(days) / 7

    # Hour-based
    hour_count = 1
    if hour != "*":
        if "," in hour:
            hour_count = len(hour.split(","))
        elif "/" in hour:
            a, b = hour.split("/")
            start = int(a) if a.isdigit() else 0
            step = int(b)
            hour_count = max(1, (24 - start) // step)
        else:
            hour_count = 1  # specific hour, doesn't multiply
    runs_per_day *= hour_count

    # Minute-based
    minute_count = 1
    if minute != "*":
        if "," in minute:
            minute_count = len(minute.split(","))
        elif "/" in minute:
            a, b = minute.split("/")
            start = int(a) if a.isdigit() else 0
            step = int(b)
            minute_count = max(1, (60 - start) // step)
        else:
            minute_count = 1  # specific minute, doesn't multiply
    runs_per_day *= minute_count

    return max(runs_per_day, 1.0 / 365)  # minimum yearly


def _match_cost(name: str, agent_costs: dict) -> dict | None:
    """Fuzzy-match cron name to a cost-tracker agent key.

    Strategy:
      1. Direct name match
      2. Strip common prefixes (`aiw-`, `ai-`) and try
      3. Strip common suffixes (`-daily`, `-weekly`, `-30min`, `-on-demand`)
    """
    if name in agent_costs:
        return agent_costs[name]

    prefixes_to_strip = ["aiw-", "ai-", "aiw_", "ai_"]
    suffixes_to_strip = ["-daily", "-weekly", "-monthly", "-30min", "-on-demand", "-biwk", "-15min", "-6h"]

    # Strip prefix + suffix combos
    stripped_name = name
    for prefix in prefixes_to_strip:
        if stripped_name.startswith(prefix):
            stripped_name = stripped_name[len(prefix):]
            break

    for suffix in suffixes_to_strip:
        if stripped_name.endswith(suffix):
            stripped_name = stripped_name[:-len(suffix)]
            break

    if stripped_name in agent_costs:
        return agent_costs[stripped_name]

    # Try with stripped prefix only
    for prefix in prefixes_to_strip:
        if name.startswith(prefix):
            test = name[len(prefix):]
            if test in agent_costs:
                return agent_costs[test]

    # Try with stripped suffix only
    for suffix in suffixes_to_strip:
        if name.endswith(suffix):
            test = name[:-len(suffix)]
            if test in agent_costs:
                return agent_costs[test]

    return None


def correlate(jobs: list, costs: dict) -> dict:
    """Build per-cron cost report."""
    # Map cron name -> cost agent data
    agent_costs = costs.get("agents", {})

    cron_costs = []
    uncategorized = []

    for j in jobs:
        name = j.get("name", "")
        schedule = j.get("schedule", {})
        runs_per_day = _runs_per_day_from_schedule(schedule)

        # Try direct name match first, then with ai...\n
        matched_cost = _match_cost(name, agent_costs)

        if matched_cost:
            daily = matched_cost.get("daily_cost_usd", 0.0)
            monthly = matched_cost.get("monthly_cost_usd", 0.0)
            cron_costs.append({
                "cron_name": name,
                "runs_per_day": runs_per_day,
                "daily_usd": daily,
                "monthly_usd": monthly,
                "model": matched_cost.get("model", "primary"),
            })
        else:
            # Estimate from runs_per_day
            estimate = runs_per_day * 0.0375  # mid-tier cost
            cron_costs.append({
                "cron_name": name,
                "runs_per_day": runs_per_day,
                "daily_usd": round(estimate, 4),
                "monthly_usd": round(estimate * 30, 2),
                "model": "estimated",
            })
            uncategorized.append({"cron_name": name, "runs_per_day": runs_per_day})

    # Sort by daily cost
    cron_costs.sort(key=lambda c: c["daily_usd"], reverse=True)
    top_10 = cron_costs[:10]

    total_daily = sum(c["daily_usd"] for c in cron_costs)

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "total_jobs": len(jobs),
        "matched_jobs": len(jobs) - len(uncategorized),
        "total_daily_usd": round(total_daily, 2),
        "top_10_by_daily": top_10,
        "uncategorized": uncategorized,
    }


def main():
    parser = argparse.ArgumentParser(description="Per-cron cost correlation")
    parser.add_argument("--jobs", type=Path, default=JOBS_FILE)
    parser.add_argument("--costs", type=Path, default=COST_FILE)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()

    if not args.jobs.exists():
        print(f"ERROR: jobs file not found: {args.jobs}", file=sys.stderr)
        sys.exit(1)
    if not args.costs.exists():
        print(f"ERROR: cost file not found: {args.costs}", file=sys.stderr)
        sys.exit(1)

    with args.jobs.open() as f:
        jobs_data = json.load(f)
    with args.costs.open() as f:
        costs_data = json.load(f)

    jobs = jobs_data.get("jobs", [])
    report = correlate(jobs, costs_data)

    with args.output.open("w") as f:
        json.dump(report, f, indent=2)

    # Stdout summary
    print(f"=== Cost Per Cron ===")
    print(f"Computed at: {report['computed_at']}")
    print(f"Total jobs: {report['total_jobs']}")
    print(f"Matched with cost data: {report['matched_jobs']}")
    print(f"Total daily cost: ${report['total_daily_usd']}")
    print(f"Written: {args.output}")
    print(f"\nTop 10 by daily cost:")
    for c in report["top_10_by_daily"]:
        marker = "" if c["model"] != "estimated" else " [est]"
        print(f"  {c['cron_name']:50s} ${c['daily_usd']:.4f}/day  ${c['monthly_usd']:.2f}/mo{marker}")

    if report["uncategorized"]:
        print(f"\n{len(report['uncategorized'])} crons without direct cost data (estimated):")
        for c in report["uncategorized"][:5]:
            print(f"  {c['cron_name']:50s} ({c['runs_per_day']:.2f} runs/day)")


if __name__ == "__main__":
    main()
