#!/usr/bin/env python3
"""
cron-event-logger.py — Log cron execution events to token-ledger.json.

This script is a wrapper that future cron jobs can call to log their
execution. It writes events to /opt/data/state/token-ledger.json in the
same schema as before (agent, job, credits, timestamp), allowing cost-cap.py
and other monitoring to work with real fleet data.

Usage:
  python3 cron-event-logger.py --agent my-agent --job my-job --credits 100

Why this exists:
  - token-ledger.json currently has 18 test events (no real fleet data)
  - cost-cap.py and token-cap.py need real events to fire correctly
  - This is a forward-compatible hook: cron jobs opt in to logging

Until the Hermes gateway supports built-in ledger writes, this script is
the bridge. Future cron jobs can either call it directly or use the
`log_token_event` Python helper imported from this module.

Created: 2026-09-03 (AIW token audit Tier 2).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOKEN_LEDGER = Path("/opt/data/state/token-ledger.json")


def log_event(agent: str, job: str, credits: int, **extra) -> dict:
    """Append an event to token-ledger.json (atomic)."""
    event = {
        "agent": agent,
        "job": job,
        "credits": int(credits),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **extra,
    }
    if TOKEN_LEDGER.exists():
        try:
            data = json.loads(TOKEN_LEDGER.read_text())
            events = data.get("events", [])
        except Exception:
            events = []
    else:
        events = []
        data = {"events": events, "schema": "token-ledger-v1"}
    events.append(event)
    data["events"] = events
    data["last_updated"] = event["timestamp"]

    tmp = TOKEN_LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(TOKEN_LEDGER)
    return event


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, help="agent name")
    p.add_argument("--job", required=True, help="job/cron name")
    p.add_argument("--credits", type=int, default=0, help="credits used")
    p.add_argument("--extra", type=str, default="{}", help="JSON extra fields")
    args = p.parse_args()

    try:
        extra = json.loads(args.extra)
    except Exception:
        extra = {}

    event = log_event(args.agent, args.job, args.credits, **extra)
    print(f"Logged: {event['agent']}/{event['job']} = {event['credits']} credits @ {event['timestamp']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
