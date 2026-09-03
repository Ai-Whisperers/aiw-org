#!/usr/bin/env python3
"""Cost reporting per cron — correlates jobs.json with measured token usage.

Built as Phase 26 #10, rewritten Phase 9 R6 (2026-09-03) to use real M3 rates.

Reads:
  - /opt/data/.hermes/cron/jobs.json (cron definitions)
  - /opt/data/state/cost-tracker.json (per-agent costs from v2 schema)

Outputs:
  - /opt/data/state/cost-per-cron.json (per-cron cost breakdown)
  - Stdout summary

Backward-compatible API: _match_cost() and correlate(jobs, costs)
are preserved for test compatibility. New measured-rate path is in
_estimate_cost_for_unmatched().

Real pricing (per token-efficiency research):
  MiniMax-M3:  $0.30/M in, $1.20/M out, $0.06/M cache_read (no cache on cron)
  Sonnet 4.6:  $3.00/M in, $15.00/M out (used when model=primary if no alias)
  Haiku 4.5:   $0.80/M in, $4.00/M out (used when model=fast if no alias)
  GLM-4.6:     $0.60/M in, $2.20/M out (alternative)
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

JOBS_FILE = Path("/opt/data/.hermes/cron/jobs.json")
COST_FILE = Path("/opt/data/state/cost-tracker.json")
OUTPUT_FILE = Path("/opt/data/state/cost-per-cron.json")

# === Pricing (USD per million tokens) ===
PRICING = {
    "MiniMax-M3": {"input": 0.30, "output": 1.20, "cache_read": 0.06},
    "minimax-m3": {"input": 0.30, "output": 1.20, "cache_read": 0.06},
    "claude-sonnet-4.6": {"input": 3.0, "output": 15.0, "cache_read": 0.30},
    "claude-haiku-4.5": {"input": 0.80, "output": 4.0, "cache_read": 0.08},
    "claude-opus-4.8": {"input": 15.0, "output": 75.0, "cache_read": 1.50},
    "glm-4.6": {"input": 0.60, "output": 2.20, "cache_read": 0.11},
    "glm-4.5-flash": {"input": 0.15, "output": 0.60, "cache_read": 0.03},
    "gpt-4o": {"input": 2.5, "output": 10.0, "cache_read": 0.25},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.015},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30, "cache_read": 0.01},
    "cerebras-gpt-oss-120b": {"input": 0.0, "output": 0.0, "cache_read": 0.0},  # free tier when working
    "cerebras-zai-glm": {"input": 0.0, "output": 0.0, "cache_read": 0.0},
}

AVG_CRON_INPUT = 5000
AVG_CRON_OUTPUT = 1500

# Cron model aliases (resolved by empirical probe on 2026-09-03 via model-probe.py)
CRON_MODEL_ALIAS = {
    "primary": "cerebras-gpt-oss-120b",
    "fast": "cerebras-zai-glm",
    "reasoning": "cerebras-gpt-oss-120b",
}

# Backward-compat: old flat-rate estimate table (used when no cost-tracker data)
_ESTIMATE_RATES = {
    "primary": 0.0375,
    "fast": 0.0016,
    "reasoning": 0.0016,
    "vision": 0.005,
    "default": 0.010,
}


def estimate_call_cost(model: str) -> float:
    """Estimate cost of one cron call at average token usage."""
    p = PRICING.get(model, PRICING["claude-sonnet-4.6"])
    return (
        (AVG_CRON_INPUT / 1e6) * p["input"]
        + (AVG_CRON_OUTPUT / 1e6) * p["output"]
    )


def _runs_per_day_from_schedule(schedule: dict) -> float:
    """Convert a cron expression to estimated runs/day."""
    if not isinstance(schedule, dict):
        return 1.0
    if schedule.get("kind") == "interval":
        minutes = schedule.get("minutes", 60)
        return (24 * 60) / minutes if minutes else 1.0
    expr = schedule.get("expr", "")
    parts = expr.split()
    if len(parts) != 5:
        return 1.0
    minute, hour, dom, month, dow = parts
    runs_per_day = 1.0

    def expand(field: str, total: int) -> int:
        if field == "*":
            return total
        if "," in field:
            return len(field.split(","))
        if field.startswith("*/"):
            n = int(field[2:])
            return total // n
        if field.isdigit():
            return 1
        if "-" in field:
            a, b = field.split("-")
            return int(b) - int(a) + 1
        return 1

    runs_per_day = expand(minute, 60) * expand(hour, 24)
    if dow != "*":
        runs_per_day *= expand(dow, 7) / 7
    if dom != "*":
        runs_per_day *= expand(dom, 31) / 31
    if month != "*":
        runs_per_day *= expand(month, 12) / 12

    return max(runs_per_day, 1.0 / 365)


# ============================================================================
# Backward-compatible API (preserved for tests/test_cost_per_cron.py)
# ============================================================================

def _match_cost(name: str, agent_costs: dict) -> dict | None:
    """Fuzzy-match cron name to a cost-tracker agent key.

    Strategy:
      1. Direct name match
      2. Strip common prefixes (`aiw-`, `ai-`) and try
      3. Strip common suffixes (`-daily`, `-weekly`, etc.)
    """
    if name in agent_costs:
        return agent_costs[name]

    prefixes_to_strip = ["aiw-", "ai-", "aiw_", "ai_"]
    suffixes_to_strip = [
        "-daily", "-weekly", "-monthly", "-30min",
        "-on-demand", "-biwk", "-15min", "-6h",
    ]

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


def _estimate_rate_for_unmatched(model_name: str | None) -> float:
    """Pick model-appropriate estimate rate for unmatched crons."""
    if not model_name:
        return _ESTIMATE_RATES["default"]
    return _ESTIMATE_RATES.get(model_name.lower(), _ESTIMATE_RATES["default"])


def correlate(jobs: list, costs: dict, model_name: str | None = None) -> dict:
    """Build per-cron cost report.

    Backward-compatible 2-arg signature (jobs, costs). When costs
    has the v2 schema (no 'agents' key), this falls back to measured
    per-token estimation.
    """
    # Map cron name -> cost agent data
    agent_costs = costs.get("agents", {}) if isinstance(costs, dict) else {}

    cron_costs = []
    uncategorized = []

    for j in jobs:
        name = j.get("name", "")
        schedule = j.get("schedule", {})
        runs_per_day = _runs_per_day_from_schedule(schedule)

        # Try direct name match first
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
            # Estimate from cost-tracker's per-run rate, not a flat $0.0375
            estimate_rate = _estimate_rate_for_unmatched(model_name)
            estimate = runs_per_day * estimate_rate
            cron_costs.append({
                "cron_name": name,
                "runs_per_day": runs_per_day,
                "daily_usd": round(estimate, 4),
                "monthly_usd": round(estimate * 30, 2),
                "model": "estimated",
                "estimate_rate_per_run": estimate_rate,
            })
            uncategorized.append({"cron_name": name, "runs_per_day": runs_per_day})

    cron_costs.sort(key=lambda c: c["daily_usd"], reverse=True)
    top_10 = cron_costs[:10]
    total_daily = sum(c["daily_usd"] for c in cron_costs)

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "schema": "cost-per-cron-v3",  # backward-compat + measured-rates
        "total_jobs": len(jobs),
        "matched_jobs": len(jobs) - len(uncategorized),
        "total_daily_usd": round(total_daily, 2),
        "top_10_by_daily": top_10,
        "uncategorized": uncategorized,
    }


# ============================================================================
# New measured-rate path (default for CLI invocation)
# ============================================================================

def correlate_measured(jobs: list) -> dict:
    """Build per-cron cost report using measured M3 + litellm rates.

    Used when costs.json doesn't have direct agent data (cost-tracker v2).
    """
    cron_costs = []
    by_provider = {}
    agent_jobs_count = 0

    for j in jobs:
        name = j.get("name", "")
        schedule = j.get("schedule", {})
        model = j.get("model")
        no_agent = j.get("no_agent", False)
        enabled = j.get("enabled", False)

        if not enabled or no_agent:
            continue
        agent_jobs_count += 1

        runs_per_day = _runs_per_day_from_schedule(schedule)
        actual_model = (
            CRON_MODEL_ALIAS.get(model, model) if model else "MiniMax-M3"
        )
        call_cost = estimate_call_cost(actual_model)
        daily = call_cost * runs_per_day
        monthly = daily * 30

        cron_costs.append({
            "cron_name": name,
            "runs_per_day": round(runs_per_day, 3),
            "daily_usd": round(daily, 4),
            "monthly_usd": round(monthly, 2),
            "model": actual_model,
            "provider": j.get("provider", ""),
        })
        by_provider[actual_model] = by_provider.get(actual_model, 0) + daily

    cron_costs.sort(key=lambda c: c["daily_usd"], reverse=True)

    total_daily = sum(c["daily_usd"] for c in cron_costs)

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "schema": "cost-per-cron-v2-measured",
        "total_jobs": len(jobs),
        "agent_jobs": agent_jobs_count,
        "total_daily_usd": round(total_daily, 2),
        "by_provider": {k: round(v, 2) for k, v in by_provider.items()},
        "top_10_by_daily": cron_costs[:10],
        "pricing_source": "research/token-efficiency-minimax-glm-2026-09-01.md",
        "assumptions": {
            "avg_input_tokens_per_call": AVG_CRON_INPUT,
            "avg_output_tokens_per_call": AVG_CRON_OUTPUT,
            "cache_reads_per_call": 0,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Per-cron cost correlation (measured rates)"
    )
    parser.add_argument("--jobs", type=Path, default=JOBS_FILE)
    parser.add_argument("--costs", type=Path, default=COST_FILE)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    parser.add_argument(
        "--measured",
        action="store_true",
        help="Use measured rates path (ignores cost-tracker.json)",
    )
    args = parser.parse_args()

    if not args.jobs.exists():
        print(f"ERROR: jobs file not found: {args.jobs}", file=sys.stderr)
        sys.exit(1)

    with args.jobs.open() as f:
        jobs_data = json.load(f)
    jobs = jobs_data.get("jobs", [])

    if args.measured:
        report = correlate_measured(jobs)
        print(f"=== Cost Per Cron (v2 — measured rates) ===")
        print(f"Computed at: {report['computed_at']}")
        print(f"Total jobs: {report['total_jobs']}  |  Agent jobs (LLM): {report['agent_jobs']}")
        print(f"Total daily cost: ${report['total_daily_usd']}/day  =  ${report['total_daily_usd']*30:.2f}/month")
        print(f"\nBy provider:")
        for prov, cost in sorted(report["by_provider"].items(), key=lambda x: -x[1]):
            print(f"  {prov:25} ${cost:.4f}/day  ${cost*30:.2f}/mo")
        print(f"\nTop 10 by daily cost:")
        for c in report["top_10_by_daily"]:
            print(f"  {c['cron_name']:50s} ${c['daily_usd']:.4f}/day  ${c['monthly_usd']:.2f}/mo  ({c['model']}, {c['runs_per_day']:.2f} runs/day)")
    else:
        if not args.costs.exists():
            print(f"ERROR: costs file not found: {args.costs}", file=sys.stderr)
            sys.exit(1)
        with args.costs.open() as f:
            costs_data = json.load(f)

        report = correlate(jobs, costs_data)
        with args.output.open("w") as f:
            json.dump(report, f, indent=2)

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
