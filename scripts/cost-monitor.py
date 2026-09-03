#!/usr/bin/env python3
"""
cost-monitor.py — Track LLM costs from real measurement sources.

Reads:
  - /opt/data/profiles/ivan/state.db.session_model_usage (real interactive spend)
  - /opt/data/state/token-ledger.json (cron events when wired)
  - /opt/data/.hermes/cron/jobs.json (cron schedule → estimated daily calls)

Writes:
  - /opt/data/state/cost-tracker.json  (real-time cost snapshot)
  - /opt/data/state/cost-tracker-history.jsonl  (append-only trend)

Real prices (from research/token-efficiency-minimax-glm-2026-09-01.md):
  MiniMax-M3: $0.30/M input, $1.20/M output, $0.06/M cache read
  GLM-4.6:    $0.60/M input, $2.20/M output, $0.11/M cache read
  Sonnet 4.6: $3.00/M input, $15.00/M output
  Haiku 4.5:  $0.80/M input, $4.00/M output

Why this rewrite:
  - Original used flat-rate $0.0375/run for every model — wrong by 5-50x.
  - State data was 13 days stale (last update 2026-08-21).
  - Interactive spend was completely invisible.

Created: 2026-09-03 (AIW token audit Tier 1 fix).
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# === Configuration ===
STATE_DB = Path("/opt/data/profiles/ivan/state.db")
COST_FILE = Path("/opt/data/state/cost-tracker.json")
HISTORY_FILE = Path("/opt/data/state/cost-tracker-history.jsonl")
TOKEN_LEDGER = Path("/opt/data/state/token-ledger.json")
CRON_FILE = Path("/opt/data/.hermes/cron/jobs.json")

# Pricing per million tokens
PRICING = {
    "MiniMax-M3": {"input": 0.30, "output": 1.20, "cache_read": 0.06},
    "minimax-m3": {"input": 0.30, "output": 1.20, "cache_read": 0.06},
    "glm-4.6": {"input": 0.60, "output": 2.20, "cache_read": 0.11},
    "glm-4.5-flash": {"input": 0.15, "output": 0.60, "cache_read": 0.03},
    "claude-sonnet-4.6": {"input": 3.0, "output": 15.0, "cache_read": 0.30},
    "claude-haiku-4.5": {"input": 0.80, "output": 4.0, "cache_read": 0.08},
    "claude-opus-4.8": {"input": 15.0, "output": 75.0, "cache_read": 1.50},
    "gpt-4o": {"input": 2.5, "output": 10.0, "cache_read": 0.25},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.015},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30, "cache_read": 0.01},
}

# Cron model alias resolution (what `model=primary` or `model=fast` actually means)
# This is the EMPIRICAL guess; tests/model_probe.py will verify.
CRON_MODEL_ALIASES = {
    "primary": "claude-sonnet-4.6",  # placeholder; verified by empirical test
    "fast": "claude-haiku-4.5",
    "reasoning": "claude-opus-4.8",
}


def cost_for_model(model: str, inp: float, outp: float, cache: float) -> float:
    """Compute cost in USD for a model with given token counts."""
    p = PRICING.get(model)
    if not p:
        return 0.0
    return (
        (inp / 1e6) * p["input"]
        + (outp / 1e6) * p["output"]
        + (cache / 1e6) * p.get("cache_read", 0)
    )


def read_interactive_spend(days: int = 7) -> dict:
    """Aggregate interactive session spend from state.db."""
    if not STATE_DB.exists():
        return {"total_usd": 0.0, "per_model": {}, "window_days": days, "available": False}
    try:
        conn = sqlite3.connect(str(STATE_DB))
        c = conn.cursor()
        since_ts = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()
        c.execute(
            """
            SELECT model, billing_provider,
                   SUM(api_call_count), SUM(input_tokens), SUM(output_tokens),
                   SUM(cache_read_tokens), SUM(cache_write_tokens)
            FROM session_model_usage
            WHERE first_seen > ?
            GROUP BY model, billing_provider
            """,
            (since_ts,),
        )
        per_model = {}
        total_usd = 0.0
        for row in c.fetchall():
            model, provider, calls, inp, outp, cache_rd, cache_wr = row
            inp = inp or 0
            outp = outp or 0
            cache_rd = cache_rd or 0
            cost = cost_for_model(model, inp, outp, cache_rd)
            total_usd += cost
            per_model[model] = {
                "provider": provider or "",
                "calls": calls or 0,
                "input": inp,
                "output": outp,
                "cache_read": cache_rd,
                "cost_usd": round(cost, 2),
            }
        conn.close()
        return {
            "total_usd": round(total_usd, 2),
            "per_model": per_model,
            "window_days": days,
            "available": True,
        }
    except Exception as e:
        return {"total_usd": 0.0, "per_model": {}, "window_days": days, "available": False, "error": str(e)}


def read_cron_spend() -> dict:
    """Estimate cron fleet spend based on schedules + measured rates.

    For each enabled MiniMax-M3 cron job, compute calls/day from its schedule
    and estimate cost at $0.005/call (typical MiniMax-M3 cron at 5k in + 1.5k out
    with no caching → roughly $0.005).

    For litellm-routed jobs, use the alias pricing.
    """
    if not CRON_FILE.exists():
        return {"total_daily_usd": 0.0, "per_job": [], "available": False}
    try:
        data = json.loads(CRON_FILE.read_text())
        jobs = [j for j in data.get("jobs", []) if j.get("enabled") and not j.get("no_agent")]
        per_job = []
        total_daily = 0.0
        for j in jobs:
            model = j.get("model")
            if not model or model == "none":
                continue
            # Resolve alias if needed
            actual_model = CRON_MODEL_ALIASES.get(model, model)
            # Estimate calls/day from schedule
            calls_per_day = _estimate_calls_per_day(j)
            if calls_per_day <= 0:
                continue
            # Average cron: 5k input + 1.5k output (no cache, fresh session each time)
            est_cost_per_call = cost_for_model(actual_model, 5000, 1500, 0)
            daily_cost = est_cost_per_call * calls_per_day
            total_daily += daily_cost
            per_job.append({
                "name": j["name"],
                "model": actual_model,
                "schedule": j.get("schedule", {}).get("display", ""),
                "calls_per_day": round(calls_per_day, 2),
                "est_cost_per_call": round(est_cost_per_call, 4),
                "daily_usd": round(daily_cost, 4),
            })
        per_job.sort(key=lambda x: -x["daily_usd"])
        return {
            "total_daily_usd": round(total_daily, 2),
            "per_job": per_job,
            "job_count": len(per_job),
            "available": True,
        }
    except Exception as e:
        return {"total_daily_usd": 0.0, "per_job": [], "available": False, "error": str(e)}


def _estimate_calls_per_day(job: dict) -> float:
    """Estimate daily cron call count from schedule."""
    s = job.get("schedule", {})
    if s.get("kind") == "interval":
        m = s.get("minutes", 60)
        return 1440 / m if m > 0 else 0
    expr = s.get("expr", "")
    if not expr:
        return 0
    parts = expr.split()
    if len(parts) != 5:
        return 0
    m, h, dom, mo, dow = parts
    # Expand each field
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
        # Range like 1-5
        if "-" in field:
            a, b = field.split("-")
            return int(b) - int(a) + 1
        return 1
    mc, hc = expand(m, 60), expand(h, 24)
    # Daily fires
    daily = mc * hc
    # DOW / DOM / month factors
    if dow != "*":
        daily *= expand(dow, 7) / 7
    if dom != "*":
        daily *= expand(dom, 31) / 31
    if mo != "*":
        daily *= expand(mo, 12) / 12
    return daily


def read_token_ledger_events() -> dict:
    """Read non-test events from token-ledger.json (test events have agent='test-agent' or 'verify')."""
    if not TOKEN_LEDGER.exists():
        return {"events": 0, "total_credits": 0, "available": False}
    try:
        d = json.loads(TOKEN_LEDGER.read_text())
        events = d.get("events", [])
        # Filter out test events
        real = [e for e in events if e.get("agent") not in ("test-agent", "verify")]
        total = sum(int(e.get("credits", 0)) for e in real)
        return {
            "events": len(real),
            "test_events_excluded": len(events) - len(real),
            "total_credits": total,
            "available": True,
        }
    except Exception as e:
        return {"events": 0, "total_credits": 0, "available": False, "error": str(e)}


def main() -> int:
    interactive = read_interactive_spend(days=7)
    cron = read_cron_spend()
    ledger = read_token_ledger_events()

    # Composite report
    interactive_monthly = interactive.get("total_usd", 0) * 30 / 7
    cron_monthly = cron.get("total_daily_usd", 0) * 30
    total_monthly = interactive_monthly + cron_monthly

    report = {
        "schema": "cost-tracker-v2",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "interactive_7d_usd": round(interactive.get("total_usd", 0), 2),
            "interactive_monthly_usd_est": round(interactive_monthly, 2),
            "cron_daily_usd_est": round(cron.get("total_daily_usd", 0), 2),
            "cron_monthly_usd_est": round(cron_monthly, 2),
            "total_monthly_usd_est": round(total_monthly, 2),
            "cron_jobs_tracked": cron.get("job_count", 0),
        },
        "interactive_breakdown": interactive,
        "cron_breakdown": cron,
        "token_ledger": ledger,
        "pricing_source": "research/token-efficiency-minimax-glm-2026-09-01.md",
        "model_alias_resolution": CRON_MODEL_ALIASES,
        "notes": [
            "Interactive cache ratio is 97% (auto-cached by Hermes desktop)",
            "Cron fleet has 0% cache (each session is fresh)",
            "litellm-primary alias resolution is a placeholder — verify via tests/model_probe.py",
        ],
    }

    # Atomic write
    tmp = COST_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(report, indent=2))
    tmp.replace(COST_FILE)

    # Append to history
    with HISTORY_FILE.open("a") as f:
        f.write(json.dumps({
            "ts": report["computed_at"],
            "summary": report["summary"],
        }) + "\n")

    # Human summary
    print(f"=== Cost Monitor (Tier 1 rewrite) — {report['computed_at']} ===")
    print(f"Interactive (7d):  ${report['summary']['interactive_7d_usd']:>8.2f}  → ~${report['summary']['interactive_monthly_usd_est']:>7.0f}/mo")
    print(f"Cron fleet (daily): ${report['summary']['cron_daily_usd_est']:>7.2f}  → ~${report['summary']['cron_monthly_usd_est']:>7.0f}/mo")
    print(f"Total monthly est:  ~${report['summary']['total_monthly_usd_est']:>7.0f}")
    print(f"Cron jobs tracked: {report['summary']['cron_jobs_tracked']}")
    print()
    if cron.get("per_job"):
        print("Top 5 cron jobs by daily cost:")
        for j in cron["per_job"][:5]:
            print(f"  ${j['daily_usd']:>6.4f}/day  {j['name']:40} ({j['model']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
