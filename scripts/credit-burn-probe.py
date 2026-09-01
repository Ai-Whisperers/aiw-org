#!/usr/bin/env python3
"""credit-burn-probe.py — Empirical 24h token-cost calibration.

Per research/aiw-token-efficiency-v4-2026-09-01.md Q4:
- cost-tracker.json ($9.79/day) uses flat-rate model assumptions
- cost-per-cron.json ($93.61/day) is an estimate based on those assumptions
- agent-traces.jsonl shows actual measured tokens ($1.36/day equivalent)
- The 3 sources disagree 100× because we don't know what `primary` actually
  resolves to (Cerebras/OAuth session per v4 Q1 live probe)

This script resolves the disagreement by:
1. Picking one representative cron (default: devops-monitor-30min)
2. Recording every input/output token for the next 24 hours
3. Reporting per-model empirical cost + 24h projected fleet cost

CLI:
    python3 credit-burn-probe.py --start              # start probing (writes probe.json)
    python3 credit-burn-probe.py --status             # show current state
    python3 credit-burn-probe.py --stop               # stop probing, print report
    python3 credit-burn-probe.py --report             # print last completed probe

Probe state at /opt/data/state/credit-burn-probe.json:
    {
      "started_at": "2026-09-01T...",
      "target_cron": "aiw-devops-monitor-30min",
      "events": [
        {"ts": "...", "input_tokens": N, "output_tokens": N,
         "model": "MiniMax-M3", "provider": "minimax-oauth"}
      ],
      "completed_at": "...",  # populated at --stop
      "totals": {"input_tokens": N, "output_tokens": N, "events": N},
      "per_model": {"MiniMax-M3": {"input": N, "output": N, "events": N}},
    }

NOTE: This script cannot directly observe tokens without instrumentation
in the cron execution path. As a placeholder until token-ledger is wired
into the scheduler (P0.6 follow-up), this script provides:
- A protocol for recording probe state
- A reading from agent-traces.jsonl as the empirical data source
- A report that reconciles claimed vs measured costs

This is the "build the probe infrastructure" piece of P0.6.
The "wire into cron" piece requires scheduler changes (separate commit).
"""
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

LEDGER_PATH = Path("/opt/data/state/token-ledger.json")
PROBE_PATH = Path("/opt/data/state/credit-burn-probe.json")
TRACES_PATH = Path("/opt/data/state/agent-traces.jsonl")

# Pricing per Million tokens (from research/efficient-ai-use-2026-09-01.md)
PRICING = {
    "MiniMax-M3":     {"input": 0.30, "output": 1.20},   # default litellm model
    "MiniMax-M2.7":   {"input": 0.30, "output": 1.20},
    "MiniMax-M2.5":   {"input": 0.30, "output": 1.20},
    "MiniMax-M2":     {"input": 0.30, "output": 1.20},
    "zai-glm-4-flash":{"input": 0.60, "output": 2.20},
    "GLM-4.6":        {"input": 0.60, "output": 2.20},
    "claude-opus-4.8":{"input": 15.0, "output": 75.0},   # pessimistic estimate
    "claude-sonnet-4.6": {"input": 3.0, "output": 15.0},
    "gpt-4o":         {"input": 2.5, "output": 10.0},
    "deepseek-v3":    {"input": 0.27, "output": 1.10},
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _read_traces(since_hours: int = 24) -> list:
    """Read agent-traces.jsonl (the empirical data source)."""
    if not TRACES_PATH.exists():
        return []
    cutoff = (datetime.now(timezone.utc)
              - timedelta(hours=since_hours)).isoformat()
    events = []
    for line in TRACES_PATH.read_text().splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
            ts = d.get("ts", "")
            if ts >= cutoff:
                events.append(d)
        except json.JSONDecodeError:
            pass
    return events


def start_probe(target: str) -> dict:
    """Start a new probe."""
    probe = {
        "started_at": _now().isoformat(),
        "target_cron": target,
        "events": [],
        "completed_at": None,
        "totals": {"input_tokens": 0, "output_tokens": 0, "events": 0},
        "per_model": {},
    }
    PROBE_PATH.write_text(json.dumps(probe, indent=2))
    print(f"[credit-burn-probe] STARTED at {probe['started_at']}")
    print(f"  target_cron: {target}")
    print(f"  state file: {PROBE_PATH}")
    return probe


def status() -> dict:
    """Show current probe state."""
    if not PROBE_PATH.exists():
        print("[credit-burn-probe] No active probe. Run --start first.")
        return {}
    probe = json.loads(PROBE_PATH.read_text())
    started = probe.get("started_at", "?")
    completed = probe.get("completed_at")
    events = len(probe.get("events", []))
    totals = probe.get("totals", {})
    target = probe.get("target_cron", "?")
    print(f"[credit-burn-probe] status:")
    print(f"  target_cron:   {target}")
    print(f"  started_at:    {started}")
    print(f"  completed_at:  {completed or '(in progress)'}")
    print(f"  events:        {events}")
    print(f"  total tokens:  in={totals.get('input_tokens', 0)}, "
          f"out={totals.get('output_tokens', 0)}")
    return probe


def stop_probe() -> dict:
    """Stop the probe and return final report."""
    if not PROBE_PATH.exists():
        print("[credit-burn-probe] No probe to stop.")
        return {}
    probe = json.loads(PROBE_PATH.read_text())
    probe["completed_at"] = _now().isoformat()

    # Generate report from probe state
    per_model = probe.get("per_model", {})
    print(f"\n=== PROBE REPORT ({probe['target_cron']}) ===")
    print(f"  duration: {probe['started_at']} → {probe['completed_at']}")
    print(f"  total events: {probe['totals']['events']}")
    print(f"  total tokens: in={probe['totals']['input_tokens']}, "
          f"out={probe['totals']['output_tokens']}")
    print()
    print("  Per-model breakdown:")
    for model, stats in per_model.items():
        cost_in = stats["input"] * PRICING.get(model, {"input": 0.0})["input"] / 1_000_000
        cost_out = stats["output"] * PRICING.get(model, {"output": 0.0})["output"] / 1_000_000
        print(f"    {model:25s}: in={stats['input']:6d}, out={stats['output']:6d}, "
              f"cost=${cost_in + cost_out:.4f}")

    PROBE_PATH.write_text(json.dumps(probe, indent=2))
    return probe


def report() -> dict:
    """Print a report from agent-traces.jsonl (empirical baseline)."""
    print(f"=== EMPIRICAL BASELINE REPORT ===")
    print(f"  source: {TRACES_PATH}")
    print(f"  window: last 24h")
    print()

    events = _read_traces(since_hours=24)
    if not events:
        print(f"  No events in last 24h ({TRACES_PATH} is empty or stale)")
        return {}

    per_model = defaultdict(lambda: {"input": 0, "output": 0, "events": 0,
                                       "cost_in": 0.0, "cost_out": 0.0})
    total_events = 0
    for e in events:
        model = e.get("model", "unknown")
        in_t = e.get("input_tokens", 0) or 0
        out_t = e.get("output_tokens", 0) or 0
        per_model[model]["input"] += in_t
        per_model[model]["output"] += out_t
        per_model[model]["events"] += 1
        pricing = PRICING.get(model, {"input": 0, "output": 0})
        per_model[model]["cost_in"] += in_t * pricing["input"] / 1_000_000
        per_model[model]["cost_out"] += out_t * pricing["output"] / 1_000_000
        total_events += 1

    total_in = sum(s["input"] for s in per_model.values())
    total_out = sum(s["output"] for s in per_model.values())
    total_cost = sum(s["cost_in"] + s["cost_out"] for s in per_model.values())

    print(f"  total events: {total_events}")
    print(f"  total tokens: in={total_in:,}, out={total_out:,}, "
          f"combined={total_in + total_out:,}")
    print(f"  total cost (24h): ${total_cost:.4f}")
    print(f"  projected monthly: ${total_cost * 30:.2f}")
    print()
    print(f"  Per-model breakdown:")
    for model, s in sorted(per_model.items(), key=lambda x: -(x[1]["cost_in"] + x[1]["cost_out"])):
        cost = s["cost_in"] + s["cost_out"]
        print(f"    {model:30s}: events={s['events']:3d}, "
              f"in={s['input']:6d}, out={s['output']:6d}, cost=${cost:.4f}")

    return {
        "events": total_events,
        "input_tokens": total_in,
        "output_tokens": total_out,
        "cost_24h": total_cost,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Empirical 24h token-cost calibration probe")
    parser.add_argument("--start", action="store_true",
                        help="Start a new probe for the target cron")
    parser.add_argument("--status", action="store_true",
                        help="Show current probe state")
    parser.add_argument("--stop", action="store_true",
                        help="Stop the probe and print final report")
    parser.add_argument("--report", action="store_true",
                        help="Print report from agent-traces.jsonl")
    parser.add_argument("--target", default="aiw-devops-monitor-30min",
                        help="Target cron name (default: devops-monitor-30min)")
    args = parser.parse_args()

    if args.start:
        start_probe(args.target)
    elif args.status:
        status()
    elif args.stop:
        stop_probe()
    elif args.report:
        report()
    else:
        # Default: print empirical baseline report
        report()
    return 0


if __name__ == "__main__":
    sys.exit(main())