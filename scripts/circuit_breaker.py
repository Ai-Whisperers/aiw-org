"""Circuit breaker for signal routing recipients (cc-switch pattern).

Tracks per-recipient failure rate over a sliding window. When failures exceed
a threshold, the circuit opens and that recipient is skipped until the cooldown
elapses. After cooldown, one probe is allowed (half-open state) — if it succeeds,
the circuit closes; if it fails, the circuit re-opens.

State per recipient:
  - closed:     normal operation, deliveries proceed
  - open:       circuit tripped, deliveries skipped (with reason logged)
  - half-open:  cooldown elapsed, one probe allowed

Persisted to /opt/data/state/circuit-breakers.json so state survives restarts.

Pattern source: farion1231/cc-switch (Local proxy with hot-switching,
auto-failover, circuit breaker, provider health monitoring) — 130,532 stars.
"""
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

CircuitState = Literal["closed", "open", "half-open"]

STATE_FILE = Path("/opt/data/state/circuit-breakers.json")

# Defaults — tunable via module-level overrides if needed.
FAILURE_THRESHOLD = 3         # open after N failures in window
WINDOW_SIZE = 10              # ... within last N attempts
COOLDOWN_SECONDS = 300        # 5 minutes before half-open probe


def _load_state() -> dict:
    """Load circuit-breaker state from disk. Returns dict keyed by recipient id."""
    if not STATE_FILE.exists():
        return {}
    try:
        with STATE_FILE.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict) -> None:
    """Persist circuit-breaker state to disk. Atomic via tmp+rename."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    tmp.replace(STATE_FILE)


def _new_state() -> dict:
    """Fresh state for a recipient."""
    return {
        "state": "closed",
        "failures": [],          # list of ISO timestamps of recent failures
        "successes": [],         # list of ISO timestamps of recent successes
        "opened_at": None,       # ISO timestamp when circuit opened
        "last_probe_at": None,   # ISO timestamp of last half-open probe
    }


def _trim_window(state: dict) -> None:
    """Keep only the last WINDOW_SIZE entries in failures/successes."""
    # Deques for efficient trim; convert on load
    state["failures"] = state.get("failures", [])[-WINDOW_SIZE:]
    state["successes"] = state.get("successes", [])[-WINDOW_SIZE:]


def get_state(recipient_id: str) -> dict:
    """Get current circuit-breaker state for a recipient, initializing if needed."""
    state = _load_state()
    if recipient_id not in state:
        state[recipient_id] = _new_state()
        _save_state(state)
    return state[recipient_id]


def can_deliver(recipient_id: str) -> tuple[bool, str]:
    """Check if a delivery is allowed for the recipient.

    Returns (allowed, reason):
      (True, "closed")          — circuit closed, deliver normally
      (True, "half-open-probe") — cooldown elapsed, this delivery is a probe
      (False, "circuit-open")   — circuit open, skip

    Updates state on cooldown-elapsed (closed → half-open).
    """
    state = _load_state()
    if recipient_id not in state:
        return True, "closed"  # never seen, default allow

    rstate = state[recipient_id]
    if rstate["state"] == "closed":
        return True, "closed"

    if rstate["state"] == "open":
        # Check if cooldown has elapsed → half-open
        if rstate.get("opened_at"):
            opened_at = datetime.fromisoformat(rstate["opened_at"])
            now = datetime.now(timezone.utc)
            if (now - opened_at).total_seconds() >= COOLDOWN_SECONDS:
                rstate["state"] = "half-open"
                rstate["last_probe_at"] = now.isoformat()
                state[recipient_id] = rstate
                _save_state(state)
                return True, "half-open-probe"
        return False, "circuit-open"

    # Already half-open → don't allow more probes, wait for result
    return False, "circuit-half-open-pending"


def record_success(recipient_id: str) -> None:
    """Record a successful delivery. Closes circuit if half-open."""
    state = _load_state()
    if recipient_id not in state:
        return  # nothing to record
    rstate = state[recipient_id]
    now = datetime.now(timezone.utc).isoformat()
    rstate["successes"].append(now)
    _trim_window(rstate)
    if rstate["state"] in ("half-open", "open"):
        # Probe succeeded — close circuit
        rstate["state"] = "closed"
        rstate["opened_at"] = None
        rstate["failures"] = []
    state[recipient_id] = rstate
    _save_state(state)


def record_failure(recipient_id: str, error: str = "") -> dict:
    """Record a failed delivery. Opens circuit if threshold reached.

    Returns updated state dict for the recipient (useful for logging).
    """
    state = _load_state()
    if recipient_id not in state:
        state[recipient_id] = _new_state()
    rstate = state[recipient_id]
    now = datetime.now(timezone.utc).isoformat()
    rstate["failures"].append(now)
    if error:
        rstate["last_error"] = error
    _trim_window(rstate)

    # Trip the breaker if threshold reached
    if (len(rstate["failures"]) >= FAILURE_THRESHOLD
            and rstate["state"] != "open"):
        rstate["state"] = "open"
        rstate["opened_at"] = now

    state[recipient_id] = rstate
    _save_state(state)
    return rstate


def reset_all() -> int:
    """Reset all circuit-breaker state. Returns number of recipients cleared."""
    state = _load_state()
    count = len(state)
    _save_state({})
    return count


def summary() -> dict:
    """Return summary stats: {recipient_id: {state, failure_count, opened_at}}."""
    state = _load_state()
    return {
        rid: {
            "state": rstate.get("state", "unknown"),
            "failure_count": len(rstate.get("failures", [])),
            "opened_at": rstate.get("opened_at"),
            "last_error": rstate.get("last_error"),
        }
        for rid, rstate in state.items()
    }


if __name__ == "__main__":
    # Self-test / CLI
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "summary":
        import pprint
        pprint.pprint(summary())
    elif cmd == "reset":
        n = reset_all()
        print(f"Reset {n} circuit breakers")
    elif cmd == "test":
        # Quick smoke: trip a breaker
        for i in range(FAILURE_THRESHOLD + 1):
            record_failure("test-recipient", f"err-{i}")
        print(f"After {FAILURE_THRESHOLD + 1} failures:")
        print(summary())
        allowed, reason = can_deliver("test-recipient")
        print(f"can_deliver: allowed={allowed}, reason={reason}")
        reset_all()
        print("Reset.")
    else:
        print(f"Unknown command: {cmd}. Try: summary | reset | test")
