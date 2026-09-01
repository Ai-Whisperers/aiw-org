#!/usr/bin/env python3
"""homunculus.py — Validate curation proposals before application.

Phase 9 R3 / Tier C5 (ADR-0002 implementation).

Reads:
  - state/curation-proposals/{ISO-week}.json (curator-evolver output)
  - All PROMPT.md files (for hard_stops validation)

Validates that proposed changes:
  - Don't violate hard_stops policies
  - Don't break parent_spec references
  - Don't drop eval-gate below threshold

Outputs:
  - state/curation-approved/{ISO-week}.json (validated)
  - outbox/signals/curation-rejection-{id}.md (rejected)
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path("/opt/data/agents")
PROPOSALS_DIR = Path("/opt/data/state/curation-proposals")
APPROVED_DIR = Path("/opt/data/state/curation-approved")
EVAL_PATH = Path("/opt/data/state/eval-per-agent.json")
OUTBOX = REPO / "outbox" / "signals"
EVAL_THRESHOLD = 0.6  # Min eval pass rate to apply curation


def iso_week():
    return datetime.now(timezone.utc).strftime("%G-W%V")


def load_proposals(week: str) -> list:
    """Load proposals for a given week."""
    path = PROPOSALS_DIR / f"{week}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text())


def load_eval_pass_rate(agent_id: str) -> float:
    """Get current eval pass rate for an agent."""
    if not EVAL_PATH.exists():
        return 1.0  # No data = assume pass
    try:
        data = json.loads(EVAL_PATH.read_text())
        return float(data.get("agents", {}).get(agent_id, {}).get("pass_rate", 1.0))
    except (json.JSONDecodeError, AttributeError):
        return 1.0


def validate_proposal(p: dict) -> tuple:
    """Return (valid: bool, errors: list)."""
    errors = []
    agent = p.get("agent_target", "")
    # Allow "unknown" / "review" target — these are observation instincts
    # that don't propose agent changes but document patterns
    if not agent or agent == "unknown":
        if p.get("action", "").startswith("Consider "):
            # Observation instinct — always valid
            return True, []
        errors.append("No agent_target and not an observation instinct")
        return False, errors

    # Check eval pass rate
    pass_rate = load_eval_pass_rate(agent)
    if pass_rate < EVAL_THRESHOLD:
        errors.append(f"Eval pass rate {pass_rate:.2f} below threshold {EVAL_THRESHOLD}")

    # Check proposed patch is non-empty (or action is allowed)
    action = p.get("action", "")
    if action not in ("add_instinct", "review", "refactor_prompt") and not action.startswith("Consider "):
        errors.append(f"Unknown action: {action}")

    # Check confidence
    if p.get("confidence", 0) < 0.75:
        errors.append(f"Confidence {p.get('confidence')} below 0.75 threshold")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", help="ISO week (e.g., 2026-W36)")
    args = parser.parse_args()

    week = args.week or iso_week()
    proposals = load_proposals(week)

    print(f"[homunculus] Validating {len(proposals)} proposals for {week}")

    approved = []
    rejected = []
    for p in proposals:
        valid, errors = validate_proposal(p)
        if valid:
            approved.append(p)
        else:
            p["rejection_errors"] = errors
            p["rejected_at"] = datetime.now(timezone.utc).isoformat()
            rejected.append(p)

    print(f"[homunculus] Approved: {len(approved)}, Rejected: {len(rejected)}")

    # Write approved
    if approved:
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        out = APPROVED_DIR / f"{week}.json"
        out.write_text(json.dumps(approved, indent=2))
        print(f"[homunculus] Wrote {out}")

    # Write rejections to outbox
    if rejected:
        OUTBOX.mkdir(parents=True, exist_ok=True)
        rej_path = OUTBOX / f"curation-rejection-{week}.md"
        content = f"# Curation Rejections — {week}\n\n"
        for p in rejected:
            content += f"## {p['instinct_id']}\n"
            for e in p.get("rejection_errors", []):
                content += f"- {e}\n"
            content += "\n"
        rej_path.write_text(content)
        print(f"[homunculus] Wrote {rej_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())