#!/usr/bin/env python3
"""context-payload.py — Validate context-packaging escalation JSON.

Usage: python3 context-payload.py <payload.json>
Returns 0 (valid), 1 (invalid).
"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "reasoning_trace",
    "tool_calls_made",
    "state_changes_intended",
    "why_escalated",
    "what_tried_first",
    "override_token",
]


def validate(payload: dict) -> list:
    """Returns list of validation errors (empty if valid)."""
    errors = []

    if "escalation_context" not in payload:
        errors.append("missing 'escalation_context' wrapper")
        return errors

    ctx = payload["escalation_context"]
    for field in REQUIRED_FIELDS:
        if field not in ctx:
            errors.append(f"missing field: {field}")

    # Type checks
    if "tool_calls_made" in ctx:
        if not isinstance(ctx["tool_calls_made"], list):
            errors.append("tool_calls_made must be a list")
        else:
            for i, call in enumerate(ctx["tool_calls_made"]):
                if not isinstance(call, dict):
                    errors.append(f"tool_calls_made[{i}] must be a dict")
                elif "tool" not in call:
                    errors.append(f"tool_calls_made[{i}] missing 'tool' field")

    if "state_changes_intended" in ctx and not isinstance(ctx["state_changes_intended"], dict):
        errors.append("state_changes_intended must be a dict")

    if "reasoning_trace" in ctx and not isinstance(ctx["reasoning_trace"], str):
        errors.append("reasoning_trace must be a string")

    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0  # No-op exit when no args (for cron testing)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(2)

    try:
        with open(path) as f:
            payload = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    errors = validate(payload)
    if errors:
        print("INVALID context payload:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("OK: context payload valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
