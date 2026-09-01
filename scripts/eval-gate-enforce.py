#!/usr/bin/env python3
"""Eval gate enforcement — block low-pass agents from running.

Reads /opt/data/state/eval-trending.json (produced by eval-aggregate-pass-rate.py)
and decides whether an agent should be allowed to run.

Built as Phase 27 R2 (D8 = a, with override).

Decisions:
  - PASS_RATE >= 0.50: ALLOW
  - PASS_RATE 0.30-0.50: WARN (allowed, but flagged)
  - PASS_RATE < 0.30: BLOCK (return non-zero; agent must use --force override)

Override mechanism:
  --force "reason text"  : log the override + allow execution anyway
  --threshold 0.40       : override the default 0.30 block threshold

Usage:
  python3 scripts/eval-gate-enforce.py --agent <agent_name>
  python3 scripts/eval-gate-enforce.py --agent <agent_name> --force "operator note"
  python3 scripts/eval-gate-enforce.py --agent <agent_name> --threshold 0.20

Exit codes:
  0 = allowed
  1 = blocked (with reason in stderr)
  2 = error (config issue)

Output JSON: writes /opt/data/state/eval-gate-decisions.json (audit log of decisions)
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EVAL_FILE = Path("/opt/data/state/eval-trending.json")
DECISIONS_LOG = Path("/opt/data/state/eval-gate-decisions.ndjson")
DEFAULT_BLOCK_THRESHOLD = 0.30
DEFAULT_WARN_THRESHOLD = 0.50


def _load_eval_trending() -> dict:
    """Load eval-trending.json. Empty dict if missing."""
    if not EVAL_FILE.exists():
        return {}
    try:
        return json.loads(EVAL_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _agent_pass_rate(agent_name: str, eval_data: dict) -> float | None:
    """Look up pass_rate for the given agent. None if unknown."""
    by_agent = eval_data.get("by_agent", {})
    agent_data = by_agent.get(agent_name)
    if not agent_data:
        return None
    pr = agent_data.get("pass_rate")
    return pr if isinstance(pr, (int, float)) else None


def _log_decision(decision: dict) -> None:
    """Append a decision to the audit log (NDJSON, Phase 28 race-condition fix)."""
    DECISIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(decision, separators=(",", ":")) + "\n"
    # Rotate at 50MB
    if DECISIONS_LOG.exists() and DECISIONS_LOG.stat().st_size > 50 * 1024 * 1024:
        archive = DECISIONS_LOG.with_suffix(f".decisions-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.ndjson")
        DECISIONS_LOG.rename(archive)
    with DECISIONS_LOG.open("a") as f:
        f.write(line)


def decide(agent_name: str, force: str | None, threshold: float) -> dict:
    """Make the allow/warn/block decision for an agent.

    Returns:
        dict with keys: agent, decision (allow/warn/block), pass_rate, reason, force
    """
    eval_data = _load_eval_trending()
    pass_rate = _agent_pass_rate(agent_name, eval_data)

    decision = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name,
        "decision": "allow",  # default; updated below
        "pass_rate": pass_rate,
        "threshold": threshold,
        "force_used": bool(force),
        "force_reason": force,
    }

    if pass_rate is None:
        # Unknown agent = no data = allow but flag
        decision["decision"] = "warn"
        decision["reason"] = "no eval data (agent never ran or no eval recorded)"

    elif pass_rate < threshold:
        # Below block threshold
        if force:
            decision["decision"] = "allow"
            decision["reason"] = f"BLOCKED by threshold {threshold} but operator forced execution"
        else:
            decision["decision"] = "block"
            decision["reason"] = f"pass_rate {pass_rate:.2%} below threshold {threshold:.0%}"

    elif pass_rate < DEFAULT_WARN_THRESHOLD:
        # Between block and warn thresholds
        decision["decision"] = "warn"
        decision["reason"] = f"pass_rate {pass_rate:.2%} below warn threshold {DEFAULT_WARN_THRESHOLD:.0%}"

    else:
        decision["decision"] = "allow"
        decision["reason"] = f"pass_rate {pass_rate:.2%} ≥ warn threshold {DEFAULT_WARN_THRESHOLD:.0%}"

    _log_decision(decision)
    return decision


def main():
    parser = argparse.ArgumentParser(description="Eval gate enforcement")
    parser.add_argument("--agent", required=True, help="Agent name to check")
    parser.add_argument("--force", help="Override block with reason (logged)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_BLOCK_THRESHOLD,
                        help=f"Block threshold (default {DEFAULT_BLOCK_THRESHOLD})")
    args = parser.parse_args()

    decision = decide(args.agent, args.force, args.threshold)

    # Stdout human-readable
    marker = {"allow": "[OK]", "warn": "[WARN]", "block": "[BLOCK]"}.get(decision["decision"], "?")
    print(f"{marker} [{decision['decision'].upper()}] {args.agent}")
    print(f"   pass_rate: {decision['pass_rate']}")
    print(f"   threshold: {decision['threshold']}")
    print(f"   reason:    {decision['reason']}")
    if decision["force_used"]:
        print(f"   force:     {decision['force_reason']}")
    print(f"   logged:    {DECISIONS_LOG}")

    # Exit code
    if decision["decision"] == "block":
        sys.exit(1)
    elif decision["decision"] == "warn":
        sys.exit(0)  # warn still allows
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
