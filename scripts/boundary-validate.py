#!/usr/bin/env python3
"""boundary-validate.py — Validate records in /opt/data/boundary/*.ndjson.

Phase 9 R3 / Tier C6. The boundary between aiw-org and growth-coaching
repos lives at /opt/data/boundary/. Records written here must pass
schema validation before being committed.

CLI:
  python3 boundary-validate.py --file /opt/data/boundary/signals.ndjson
  python3 boundary-validate.py --all  # validate all *.ndjson in boundary/
"""
import argparse
import json
import re
import sys
from pathlib import Path

BOUNDARY_DIR = Path("/opt/data/boundary")

REQUIRED_FIELDS = {
    "signals": ["signal_type", "source", "target", "payload", "timestamp"],
    "sessions": ["session_id", "coach_id", "customer_id", "started_at"],
    "coaches": ["coach_id", "name", "status"],
}

VALID_SIGNAL_TYPES = {
    "coach_engagement", "coach_performance_alert", "customer_lifecycle_event",
    "session_scheduled", "session_completed", "alert", "escalation",
}

VALID_COACH_STATUSES = {"active", "paused", "offboarding", "offboarded"}

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def validate_signal(record: dict) -> list:
    errors = []
    for field in REQUIRED_FIELDS["signals"]:
        if field not in record:
            errors.append(f"missing required field: {field}")
    if record.get("signal_type") not in VALID_SIGNAL_TYPES:
        errors.append(f"invalid signal_type: {record.get('signal_type')}")
    if not record.get("timestamp", "").startswith("20"):
        errors.append(f"timestamp must be ISO-8601 UTC, got: {record.get('timestamp')}")
    return errors


def validate_session(record: dict) -> list:
    errors = []
    for field in REQUIRED_FIELDS["sessions"]:
        if field not in record:
            errors.append(f"missing required field: {field}")
    if not UUID_RE.match(record.get("session_id", "")):
        errors.append(f"session_id must be UUIDv4: {record.get('session_id')}")
    return errors


def validate_coach(record: dict) -> list:
    errors = []
    for field in REQUIRED_FIELDS["coaches"]:
        if field not in record:
            errors.append(f"missing required field: {field}")
    if record.get("status") not in VALID_COACH_STATUSES:
        errors.append(f"invalid status: {record.get('status')}")
    return errors


def validate_file(path: Path) -> tuple:
    """Return (valid_count, invalid_count, errors)."""
    valid = 0
    invalid = 0
    errors = []

    name = path.stem  # e.g., "signals", "sessions", "coaches"
    validator = {
        "signals": validate_signal,
        "sessions": validate_session,
        "coaches": validate_coach,
    }.get(name)

    if not validator:
        return 0, 0, [f"Unknown boundary file type: {name}"]

    if not path.exists():
        return 0, 0, []

    for i, line in enumerate(path.open(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {i}: JSON decode error: {e}")
            invalid += 1
            continue
        rec_errors = validator(record)
        if rec_errors:
            errors.append(f"line {i}: {rec_errors}")
            invalid += 1
        else:
            valid += 1
    return valid, invalid, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Specific boundary file to validate")
    parser.add_argument("--all", action="store_true", help="Validate all *.ndjson")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    elif args.all:
        files = list(BOUNDARY_DIR.glob("*.ndjson"))
    else:
        print("Specify --file or --all")
        return 1

    total_valid = 0
    total_invalid = 0
    all_errors = []

    for f in files:
        v, inv, errs = validate_file(f)
        total_valid += v
        total_invalid += inv
        all_errors.extend([(f.name, e) for e in errs])
        if v > 0 or inv > 0:
            print(f"[validate] {f.name}: {v} valid, {inv} invalid")

    print(f"[validate] TOTAL: {total_valid} valid, {total_invalid} invalid")

    if all_errors:
        print("[validate] Errors:")
        for fname, e in all_errors[:20]:
            print(f"  - {fname}: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())