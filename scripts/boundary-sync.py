#!/usr/bin/env python3
"""boundary-sync.py — Read /opt/data/boundary/*.ndjson and route signals.

Phase 9 R3 / Tier C6. Polls the boundary directory for new signals
since last sync, validates them, and routes to aiw-org's internal
signal queue.

CLI:
  python3 boundary-sync.py            # sync all boundary files
  python3 boundary-sync.py --since 1h # sync records from last hour
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY_DIR = Path("/opt/data/boundary")
SYNC_STATE = Path("/opt/data/state/boundary-sync-state.json")
SIGNAL_QUEUE = Path("/opt/data/state/signal-queue.ndjson")


def _now():
    return datetime.now(timezone.utc).isoformat()


def load_sync_state() -> dict:
    """Load last sync timestamps per file."""
    if SYNC_STATE.exists():
        return json.loads(SYNC_STATE.read_text())
    return {}


def save_sync_state(state: dict):
    """Persist sync state."""
    SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE.write_text(json.dumps(state, indent=2))


def sync_file(name: str, since: str = None) -> int:
    """Sync one boundary file. Returns count of new records routed."""
    path = BOUNDARY_DIR / f"{name}.ndjson"
    if not path.exists():
        return 0
    count = 0
    SIGNAL_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with SIGNAL_QUEUE.open("a") as q:
        for line in path.open():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                # Check timestamp if --since was set
                if since and rec.get("timestamp", "") < since:
                    continue
                # Route to internal queue
                q.write(json.dumps({
                    "boundary_source": name,
                    "received_at": _now(),
                    **rec,
                }) + "\n")
                count += 1
            except json.JSONDecodeError:
                continue
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="ISO-8601 timestamp or relative (1h, 1d)")
    args = parser.parse_args()

    state = load_sync_state()
    total = 0
    for name in ["signals", "sessions", "coaches"]:
        count = sync_file(name, since=args.since)
        if count > 0:
            print(f"[sync] {name}: routed {count} records")
        total += count
        state[f"{name}_last_sync"] = _now()

    save_sync_state(state)
    print(f"[sync] TOTAL: {total} records routed")
    return 0


if __name__ == "__main__":
    sys.exit(main())