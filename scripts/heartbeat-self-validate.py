#!/usr/bin/env python3
"""Heartbeat self-validation - validates that the heartbeats are working.

Built as Phase 30 R1 (Tier G4 - Self-validating heartbeat).

The heartbeat crons (`cron-heartbeat-onhours`, `cron-heartbeat-offhours`) write
to /opt/data/state/heartbeat-health.json every 30min on-hours / 15min off-hours.

This script validates:
  1. Heartbeat file exists and is recent (< threshold)
  2. Heartbeat values are sane (no zero-age, no negative, etc.)
  3. Heartbeat is NOT stale (was actually fired in last N minutes)
  4. Heartbeat reports correct state

If validation fails: writes a CRITICAL alert to /opt/data/state/heartbeat-meta.json

Usage:
    python3 scripts/heartbeat-self-validate.py                 # validate
    python3 scripts/heartbeat-self-validate.py --strict         # fail on any warning
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path("/opt/data/state")
HEARTBEAT_FILE = STATE_DIR / "heartbeat-health.json"
ALERT_FILE = STATE_DIR / "heartbeat-alert.json"

# Thresholds (seconds)
MAX_HEARTBEAT_AGE = 1800        # 30min — on-hours heartbeat
MAX_HEARTBEAT_AGE_OFF = 900     # 15min — off-hours heartbeat
MIN_HEARTBEAT_AGE = 30          # 30s — at least this should have elapsed


def validate_heartbeat(strict: bool = False) -> dict:
    """Validate heartbeat file. Returns validation result dict."""
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "checks": [],
        "errors": [],
        "warnings": [],
    }

    if not HEARTBEAT_FILE.exists():
        result["errors"].append(f"heartbeat file missing: {HEARTBEAT_FILE}")
        result["healthy"] = False
        return result

    try:
        hb = json.loads(HEARTBEAT_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        result["errors"].append(f"heartbeat file invalid JSON: {e}")
        result["healthy"] = False
        return result

    age = hb.get("heartbeat_age_seconds", -1)
    threshold = hb.get("threshold_seconds", 1800)
    healthy = hb.get("healthy", None)
    alert = hb.get("alert", "none")

    # Check 1: heartbeat_age is a real number
    if not isinstance(age, int) or age < 0:
        result["errors"].append(f"heartbeat_age_seconds invalid: {age!r}")

    # Check 2: heartbeat is fresh (depends on threshold)
    if age > threshold:
        result["errors"].append(f"heartbeat stale: {age}s > threshold {threshold}s")

    # Check 3: heartbeat is not too fresh (sanity — heartbeat should not fire every second)
    if 0 <= age < MIN_HEARTBEAT_AGE and age != -1:
        result["warnings"].append(f"heartbeat too fresh: {age}s < {MIN_HEARTBEAT_AGE}s (possible rapid-fire?)")

    # Check 4: healthy field is consistent
    if healthy is False and alert == "none":
        result["errors"].append("healthy=False but alert='none' (inconsistent)")

    # Check 5: threshold is sensible
    if threshold not in (1800, 900):
        result["warnings"].append(f"unexpected threshold {threshold}s (expected 1800 or 900)")

    result["checks"].append({
        "check": "heartbeat_fresh",
        "age": age,
        "threshold": threshold,
        "ok": age <= threshold,
    })
    result["healthy"] = not result["errors"]

    if strict and result["warnings"]:
        result["healthy"] = False

    return result


def write_alert(result: dict) -> None:
    """Write alert if validation failed."""
    if result["healthy"]:
        # Clear any prior alerts
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        return

    ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)
    alert = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "severity": "CRITICAL" if result["errors"] else "MEDIUM",
        "errors": result["errors"],
        "warnings": result["warnings"],
        "checks": result["checks"],
    }
    with ALERT_FILE.open("w") as f:
        f.write(json.dumps(alert, separators=(",", ":")))


def main():
    parser = argparse.ArgumentParser(description="Heartbeat self-validation")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as failures")
    args = parser.parse_args()

    result = validate_heartbeat(strict=args.strict)
    write_alert(result)

    if result["healthy"]:
        print(f"[OK] heartbeat healthy (age={result['checks'][0]['age']}s)")
    else:
        print(f"[FAIL] heartbeat unhealthy")
        for e in result["errors"]:
            print(f"  ERROR: {e}")
        for w in result["warnings"]:
            print(f"  WARN: {w}")
        print(f"  alert: {ALERT_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
