#!/usr/bin/env python3
"""idempotency-check.py — Idempotency contract check for agent runs.

Usage: python3 idempotency-check.py <agent-name> <window> [override-token]
Returns 0 (run allowed), 1 (duplicate), 2 (override), 3 (error).
"""
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATE_DIR = Path("/opt/data/agents/state")
DB_DIR = Path("/opt/data/db")

WINDOW_MAP = {
    "24h": timedelta(hours=24),
    "12h": timedelta(hours=12),
    "7d": timedelta(days=7),
    "5min": timedelta(minutes=5),
}


def check_idempotency(agent: str, window: str, override_token: str = None) -> int:
    """Returns 0 (run), 1 (duplicate), 2 (override), 3 (error)."""
    db_file = DB_DIR / f"{agent}.db"

    # Try SQLite first
    if db_file.exists():
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT last_run, override_token FROM idempotency WHERE job_id = ?",
                (f"{agent}_main",),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                last_run, override_db_token = row
                if override_token and override_db_token == override_token:
                    return 2  # Override
        except sqlite3.OperationalError:
            pass

    # Fallback to JSON
    json_file = STATE_DIR / f"{agent}.json"
    if not json_file.exists():
        return 0  # No state = first run

    try:
        with open(json_file) as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError):
        return 3  # Error reading state

    last_run = state.get("last_run")
    if not last_run:
        return 0

    # Parse
    try:
        last_run_dt = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return 0

    # Window check
    window_delta = WINDOW_MAP.get(window)
    if not window_delta:
        return 3  # Unknown window

    now = datetime.now(timezone.utc)
    if now - last_run_dt < window_delta:
        return 1  # Duplicate

    return 0


def main():
    if len(sys.argv) < 3:
        print("Usage: idempotency-check.py <agent> <window> [override-token]")
        sys.exit(2)

    agent = sys.argv[1]
    window = sys.argv[2]
    override = sys.argv[3] if len(sys.argv) > 3 else None

    result = check_idempotency(agent, window, override)

    if result == 0:
        print("RUN_ALLOWED")
    elif result == 1:
        print("DUPLICATE_SKIP")
    elif result == 2:
        print("OVERRIDE_RUN")
    else:
        print("ERROR")
    sys.exit(result)


if __name__ == "__main__":
    main()
