#!/usr/bin/env python3
"""cost-monitor.py — Track LLM costs per agent (the $12K/month risk).

Estimates cost per agent per day based on token usage + model pricing.
Reads from:
- /opt/data/cron/jobs.json (model for each agent)
- /opt/data/state/org-state.json (run frequency)

Writes:
- /opt/data/state/cost-tracker.json
- /opt/data/agents/state/cost-tracker.json (legacy)

Run via cron: aiw-cost-monitor (every 6 hours)
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

STATE_DIR = Path("/opt/data/state")
AGENTS_STATE = Path("/opt/data/agents/state")
COST_FILE = STATE_DIR / "cost-tracker.json"

# Model pricing (USD per 1M tokens) — input/output
MODEL_PRICING = {
    "reasoning": {"input": 3.0, "output": 15.0},  # litellm/reasoning (Nvidia NIM)
    "fast": {"input": 0.15, "output": 0.6},  # litellm/fast (Haiku equivalent)
    "modelo de IA-opus-4.8": {"input": 15.0, "output": 75.0},
    "modelo de IA-sonnet-4.6": {"input": 3.0, "output": 15.0},
    "modelo de IA-haiku-4.5": {"input": 0.80, "output": 4.0},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "deepseek-v3": {"input": 0.27, "output": 1.10},
}


def get_model_pricing(model_name: str) -> dict:
    """Get pricing for a model, with fallback."""
    if model_name in MODEL_PRICING:
        return MODEL_PRICING[model_name]
    # Default: assume mid-tier
    return {"input": 3.0, "output": 15.0}


def estimate_tokens(brief_path: Path) -> tuple:
    """Estimate input/output tokens from a brief file."""
    if not brief_path.exists():
        return 0, 0
    
    text = brief_path.read_text()
    # Rough estimate: ~4 chars per token
    total_chars = len(text)
    total_tokens = total_chars / 4
    
    # Estimate: 70% input (prompt + context), 30% output (the brief)
    input_tokens = total_tokens * 0.7
    output_tokens = total_tokens * 0.3
    
    return int(input_tokens), int(output_tokens)


def main():
    # Read jobs.json
    jobs_path = Path("/opt/data/cron/jobs.json")
    if not jobs_path.exists():
        print("ERROR: jobs.json not found")
        return
    
    jobs_data = json.loads(jobs_path.read_text())
    jobs = jobs_data.get("jobs", jobs_data) if isinstance(jobs_data, dict) else jobs_data
    if isinstance(jobs, dict):
        jobs = jobs.get("jobs", list(jobs_data.values()))
    
    # Calculate cost per agent per day
    costs_by_agent = defaultdict(lambda: {
        "runs_per_day": 0,
        "input_tokens_per_run": 0,
        "output_tokens_per_run": 0,
        "daily_cost_usd": 0.0,
        "monthly_cost_usd": 0.0,
        "model": "unknown",
    })
    
    today = datetime.now(timezone.utc).date()
    
    for job in jobs:
        if not isinstance(job, dict):
            continue
        if not job.get("enabled", True):
            continue
        
        name = job.get("name", "")
        model = job.get("model", "fast")
        
        # Extract agent from job name
        if not name.startswith("aiw-"):
            continue
        agent = name[4:]  # strip "aiw-"
        
        # Calculate runs per day from schedule
        schedule = job.get("schedule", {})
        if isinstance(schedule, dict):
            expr = schedule.get("expr", "")
        else:
            expr = str(schedule)
        
        runs_per_day = estimate_runs_per_day(expr)
        
        # Get the latest brief to estimate token usage
        agent_dir = Path(f"/opt/data/agents/{agent}")
        brief_files = list(agent_dir.glob("outbox/*.md")) + list(agent_dir.glob("lessons/*.md"))
        
        if brief_files:
            latest = max(brief_files, key=lambda f: f.stat().st_mtime)
            input_tokens, output_tokens = estimate_tokens(latest)
        else:
            # Default estimate: 5000 input + 1500 output per run
            input_tokens, output_tokens = 5000, 1500
        
        # Calculate cost
        pricing = get_model_pricing(model)
        cost_per_run = (input_tokens / 1_000_000) * pricing["input"] + (output_tokens / 1_000_000) * pricing["output"]
        daily_cost = cost_per_run * runs_per_day
        
        costs_by_agent[agent] = {
            "runs_per_day": runs_per_day,
            "input_tokens_per_run": input_tokens,
            "output_tokens_per_run": output_tokens,
            "cost_per_run_usd": round(cost_per_run, 4),
            "daily_cost_usd": round(daily_cost, 4),
            "monthly_cost_usd": round(daily_cost * 30, 2),
            "model": model,
        }
    
    # Aggregate
    total_daily = sum(c["daily_cost_usd"] for c in costs_by_agent.values())
    total_monthly = sum(c["monthly_cost_usd"] for c in costs_by_agent.values())
    
    # Find top cost agents
    top_cost = sorted(costs_by_agent.items(), key=lambda x: x[1]["monthly_cost_usd"], reverse=True)[:10]
    
    output = {
        "version": "1.0.0",
        "schema": "cost-tracker-v1",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_agents_tracked": len(costs_by_agent),
        "total_daily_usd": round(total_daily, 2),
        "total_monthly_usd": round(total_monthly, 2),
        "model_pricing": MODEL_PRICING,
        "agents": dict(costs_by_agent),
        "top_10_monthly": [{"agent": a, **c} for a, c in top_cost],
    }
    
    # Atomic write
    tmp = COST_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(output, indent=2))
    tmp.replace(COST_FILE)
    
    # Also write to legacy location
    AGENTS_STATE.mkdir(parents=True, exist_ok=True)
    legacy = AGENTS_STATE / "cost-tracker.json"
    legacy.write_text(json.dumps(output, indent=2))
    
    print(f"✓ Tracked {len(costs_by_agent)} agents")
    print(f"  Total daily: ${total_daily:.2f}")
    print(f"  Total monthly: ${total_monthly:.2f}")
    print(f"\n  Top 5 monthly costs:")
    for a, c in top_cost[:5]:
        print(f"    {a}: ${c['monthly_cost_usd']:.2f}/mo ({c['runs_per_day']} runs/day, {c['model']})")


def estimate_runs_per_day(cron_expr: str) -> float:
    """Estimate how many times a cron runs per day."""
    if not cron_expr:
        return 0.0
    
    # Parse common patterns
    if cron_expr.startswith("*/"):
        # */N * * * * = every N minutes
        try:
            n = int(cron_expr[2:].split()[0])
            return 24 * 60 / n
        except:
            pass
    
    parts = cron_expr.split()
    if len(parts) != 5:
        return 0.0
    
    minute, hour, dom, month, dow = parts
    
    # Daily if hour is *
    if hour == "*" and minute == "*/15":
        return 96
    if hour == "*" and minute == "*/30":
        return 48
    if hour == "*" and minute == "*/5":
        return 288
    if hour == "*" and minute == "0":
        return 1
    if hour == "*" and minute.startswith("*/"):
        try:
            n = int(minute[2:])
            return 24 * 60 / n
        except:
            pass
    
    # Hourly
    if minute == "0" and "/" in hour:
        try:
            n = int(hour.split("/")[1])
            return 24 / n
        except:
            pass
    
    # Daily at specific time
    if minute.isdigit() and (hour.isdigit() or hour == "*"):
        if hour == "*":
            return 24  # hourly
        return 1  # daily at that hour
    
    # Weekly
    if "," in dow or dom:
        return 1 / 7  # roughly weekly
    
    return 0.0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

