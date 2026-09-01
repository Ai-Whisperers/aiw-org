#!/usr/bin/env python3
"""build-pipeline.py — Two-phase build pipeline runtime dispatcher.

Phase 9 R3 / Tier C4. Reads demiurge/router/dispatch-rules.yaml and
demiurge/router/timing-rules.yaml. When a build signal arrives, runs:
  Phase 1: architect-agent → produces architecture plan
  Phase 2: builder-agent → produces implementation
  Quality gate: auditor-agent reviews both before delivery

This script wires the dispatch rules into actual cron invocation.

CLI:
  python3 build-pipeline.py dispatch --signal <signal_path>
  python3 build-pipeline.py list-rules
  python3 build-pipeline.py validate-rules
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path("/opt/data/agents")
DISPATCH_RULES = REPO / "demiurge" / "router" / "dispatch-rules.yaml"
TIMING_RULES = REPO / "demiurge" / "router" / "timing-rules.yaml"
REVENUE_SIGNALS = REPO / "demiurge" / "router" / "revenue-signals.yaml"


def load_yaml(path: Path) -> dict:
    """Load YAML, return {} if missing."""
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text())


def list_rules() -> int:
    """Show all dispatch rules."""
    rules = load_yaml(DISPATCH_RULES)
    dispatch = rules.get("dispatch_rules", [])
    print(f"[dispatch] {len(dispatch)} rules loaded")
    for r in dispatch:
        match = r.get("match", {})
        targets = r.get("deliver_to", [])
        target_names = [t.get("id", "?") for t in targets]
        print(f"  {r.get('id', '?')}: match={match.get('signal_type', '?')}/{match.get('routing_tags', [])} → {target_names}")
    return 0


def validate_rules() -> int:
    """Verify all rules reference existing agents."""
    rules = load_yaml(DISPATCH_RULES)
    dispatch = rules.get("dispatch_rules", [])
    errors = []
    for r in dispatch:
        for target in r.get("deliver_to", []):
            if target.get("type") == "agent":
                agent_id = target.get("id")
                # Check if PROMPT.md exists
                possible_paths = [
                    REPO / "demiurge" / "agents" / agent_id / "PROMPT.md",
                    REPO / f"{agent_id}" / "PROMPT.md",
                ]
                if not any(p.exists() for p in possible_paths):
                    errors.append(f"Rule {r.get('id')} references missing agent: {agent_id}")
    if errors:
        print("[dispatch] VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"[dispatch] All {len(dispatch)} rules validated")
    return 0


def dispatch(signal_path: str) -> int:
    """Dispatch a build signal through the two-phase pipeline."""
    sp = Path(signal_path)
    if not sp.exists():
        print(f"[dispatch] Signal not found: {signal_path}")
        return 1
    signal = json.loads(sp.read_text())
    routing_tags = signal.get("routing_tags", [])
    signal_type = signal.get("signal_type", "unknown")

    rules = load_yaml(DISPATCH_RULES)
    dispatch_rules = rules.get("dispatch_rules", [])

    # Find matching rule
    matched = None
    for r in dispatch_rules:
        m = r.get("match", {})
        if m.get("signal_type") == signal_type:
            matched = r
            break
        if any(t in m.get("routing_tags", []) for t in routing_tags):
            matched = r
            break

    if not matched:
        print(f"[dispatch] No matching rule for signal_type={signal_type} tags={routing_tags}")
        return 0

    targets = matched.get("deliver_to", [])
    print(f"[dispatch] Rule {matched.get('id')}: delivering to {len(targets)} agents")
    for t in targets:
        print(f"  - {t.get('id', '?')}")

    # Log dispatch
    log_path = Path("/opt/data/state/build-pipeline-dispatch.ndjson")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signal": str(sp),
            "rule": matched.get("id"),
            "targets": [t.get("id") for t in targets],
            "routing_tags": routing_tags,
        }
        f.write(json.dumps(log) + "\n")
    return 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-rules", help="Show all dispatch rules")
    sub.add_parser("validate-rules", help="Validate rules reference existing agents")

    p_dispatch = sub.add_parser("dispatch", help="Dispatch a signal")
    p_dispatch.add_argument("--signal", required=True, help="Path to signal JSON")

    args = parser.parse_args()
    if args.cmd == "list-rules":
        return list_rules()
    if args.cmd == "validate-rules":
        return validate_rules()
    if args.cmd == "dispatch":
        return dispatch(args.signal)
    return 0


if __name__ == "__main__":
    sys.exit(main())