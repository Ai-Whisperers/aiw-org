# Idempotency Contract Pattern

> Canonical idempotency check pattern. Phase 3 input.
> **Last updated**: 2026-08-14

---

## Pattern spec

Every agent's PROMPT.md must include:

```yaml
idempotency:
  key: state.last_run
  window:
    daily: 24h
    biweekly: 12h
    weekly: 7d
    on-demand: 5min
  duplicate_action: skip + log "duplicate_run"
  override: state.override_possible = true
```

## Runtime check

`/opt/data/agents-v2/patterns/idempotency-example.py`:

```python
#!/usr/bin/env python3
"""Idempotency check for agent runs.

Usage: python3 idempotency-example.py <agent-name> <window>
Returns:
  0 = run allowed
  1 = duplicate (skip)
  2 = override_token matched (run allowed)
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
    """Returns 0 (run), 1 (duplicate), 2 (override)."""
    db_file = DB_DIR / f"{agent}.db"

    if not db_file.exists():
        # Fallback to JSON
        json_file = STATE_DIR / f"{agent}.json"
        if not json_file.exists():
            print(f"NO STATE for {agent}", file=sys.stderr)
            return 0  # No state = first run

        with open(json_file) as f:
            state = json.load(f)
        last_run = state.get("last_run")
        override_possible = state.get("override_possible", True)
    else:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_run, override_token FROM idempotency WHERE job_id = ?",
            (f"{agent}_main",),
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return 0  # No record = first run
        last_run, override_db_token = row
        override_possible = override_db_token is not None

    if not last_run:
        return 0

    # Parse last_run
    try:
        last_run_dt = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
    except ValueError:
        return 0  # Unparseable = allow

    # Check override token
    if override_possible and override_token:
        return 2

    # Check window
    window_delta = WINDOW_MAP.get(window)
    if not window_delta:
        print(f"Unknown window: {window}", file=sys.stderr)
        return 0  # Allow on unknown window

    now = datetime.now(timezone.utc)
    if now - last_run_dt < window_delta:
        return 1  # Duplicate

    return 0  # Run allowed


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: idempotency-example.py <agent> <window> [override_token]")
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
    sys.exit(result)
```

## Usage in agent runtime

Before agent executes its main task, runtime calls:

```bash
result=$(python3 idempotency-example.py business-analyst 24h)
case "$result" in
  RUN_ALLOWED) ;;  # proceed
  DUPLICATE_SKIP) log "duplicate_run"; exit 0 ;;
  OVERRIDE_RUN) log "override_run"; ;;  # proceed
esac
```

## Override mechanism

Override tokens are UUIDs stored in state when Ivan manually triggers:

```bash
# In Hermes CLI
hermes cron run aiw-business-analyst-daily --override-token $(uuidgen)
```

The token is stored in `state.override_possible` and consumed once.

---

## Testing

Test scenarios:

1. **First run** (no last_run): returns 0 (RUN_ALLOWED)
2. **Within window** (e.g., 1h after last 24h run): returns 1 (DUPLICATE_SKIP)
3. **Outside window** (e.g., 25h after last 24h run): returns 0 (RUN_ALLOWED)
4. **Override token valid**: returns 2 (OVERRIDE_RUN)
5. **Window unknown**: returns 0 (RUN_ALLOWED, fail open)

---

**Document path**: `/opt/data/agents-v2/patterns/idempotency.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
