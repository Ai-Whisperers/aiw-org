#!/usr/bin/env python3
"""cost-cap.py — Per-agent daily cost cap enforcement.

Reads state/cost-tracker.json. If any agent exceeds $1/day OR total > $10,
halts the agent and posts alert.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/agents/state")
COST_FILE = STATE_DIR / "cost-tracker.json"
PER_AGENT_CAP_USD = 1.0
TOTAL_CAP_USD = 10.0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Per-agent daily cost cap enforcement")
    parser.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not COST_FILE.exists():
        COST_FILE.write_text(json.dumps({"date": today, "per_agent": {}, "total_usd": 0.0}))
        print(f"Initialized cost-tracker.json for {today}")
        return 0

    with open(COST_FILE) as f:
        tracker = json.load(f)

    if tracker.get("date") != today:
        # Reset for new day
        tracker = {"date": today, "per_agent": {}, "total_usd": 0.0}
        with open(COST_FILE, "w") as f:
            json.dump(tracker, f, indent=2)

    halted = []

    for agent, cost in tracker.get("per_agent", {}).items():
        if cost > PER_AGENT_CAP_USD:
            halted.append(f"{agent}: ${cost:.2f} > ${PER_AGENT_CAP_USD:.2f} cap")

    if tracker.get("total_usd", 0) > TOTAL_CAP_USD:
        halted.append(f"TOTAL: ${tracker['total_usd']:.2f} > ${TOTAL_CAP_USD:.2f} cap")

    if halted:
        for h in halted:
            print(f"HALT: {h}")
        return 1

    print(f"OK: total ${tracker.get('total_usd', 0):.2f} within caps (per-agent: ${PER_AGENT_CAP_USD}, total: ${TOTAL_CAP_USD})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
