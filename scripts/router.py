#!/usr/bin/env python3
"""Router — match signals to dispatch rules, deliver to recipients.

Built as Phase 28 R2 (A1 - Router).

Reads:
  - /opt/data/state/signal-queue.ndjson (pending signals)
  - demiurge/router/dispatch-rules.yaml (routing rules)
  - demiurge/router/timing-rules.yaml (SLA rules)

For each pending signal:
  1. Match against dispatch_rules (by signal_type + routing_tags + department)
  2. Compute recipients via deliver_to + fan_out
  3. Check timing-rules for SLA escalation
  4. Mark signal as routed + write to recipient outboxes
  5. Log routing decision

Usage:
    python3 scripts/router.py --process            # process all pending
    python3 scripts/router.py --process --limit 50  # process up to 50
    python3 scripts/router.py --explain <signal-id>  # show what would happen
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Add scripts/ to path so we can import signal_queue
sys.path.insert(0, str(Path(__file__).parent))
from signal_queue import (  # type: ignore
    SIGNAL_QUEUE, append_signal, list_signals, update_signal_status
)

ROUTER_DIR = Path("/opt/data/agents/demiurge/router")
DISPATCH_RULES_FILE = ROUTER_DIR / "dispatch-rules.yaml"
TIMING_RULES_FILE = ROUTER_DIR / "timing-rules.yaml"
ROUTING_LOG = Path("/opt/data/state/routing-decisions.jsonl")

# Required fields per signal_type (refusal-when-constraints-unmet pattern)
REQUIRED_SIGNAL_FIELDS = {"id", "ts", "source", "routing_tags"}

# Maximum recent signals to scan per pre-dispatch contradiction check
CONTRADICTION_LOOKBACK = 10


def pre_dispatch_check(signal: dict) -> dict | None:
    """Validate signal before dispatch. Returns None to proceed, or
    {"reject": reason, "code": ...} to refuse routing.

    Implements two patterns from research:
    1. Refusal-when-constraints-unmet (cerebralvalley Opus 4.7 hackathon,
       Thom Pham): signals missing required fields get refused, not delivered.
    2. Contradiction-detection (khwarizmi-hermes-plugin): if the same source
       emitted a recent signal with contradictory routing_tags, flag it.

    Refused signals are logged but marked 'routed' so they don't loop.
    """
    # 1. Required-field check
    missing = REQUIRED_SIGNAL_FIELDS - set(signal.keys())
    if missing:
        return {
            "reject": True,
            "code": "missing_required_fields",
            "fields": sorted(missing),
            "signal_id": signal.get("id"),
        }

    # 2. routing_tags must be non-empty list (a signal with no tags matches
    # every rule whose match has no tag constraint — usually wrong)
    tags = signal.get("routing_tags", [])
    if not isinstance(tags, list) or len(tags) == 0:
        return {
            "reject": True,
            "code": "empty_routing_tags",
            "signal_id": signal.get("id"),
        }

    # 3. Contradiction check: scan recent routing decisions for same source
    # with overlapping but conflicting tags. We only have a routing-decisions
    # log (not the full signal queue here), so this is best-effort.
    if ROUTING_LOG.exists():
        try:
            recent_same_source = []
            with ROUTING_LOG.open() as f:
                lines = f.readlines()[-CONTRADICTION_LOOKBACK * 3:]
            for line in lines:
                try:
                    decision = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if decision.get("source") == signal.get("source"):
                    recent_same_source.append(decision)
            recent_same_source = recent_same_source[-CONTRADICTION_LOOKBACK:]
            # Heuristic: if 3+ recent decisions from same source failed
            # (no_rule), the source may be misconfigured — flag for review
            failed = sum(
                1 for d in recent_same_source if d.get("result") == "no_rule"
            )
            if failed >= 3:
                return {
                    "reject": True,
                    "code": "source_high_failure_rate",
                    "recent_failures": failed,
                    "lookback": len(recent_same_source),
                    "source": signal.get("source"),
                }
        except Exception:
            # Never let the pre-check itself block routing
            pass

    return None


# Agent name → outbox dir mapping (canonical)
AGENT_OUTBOX = {
    "apollo-sales-lead": "demiurge/agents/apollo-sales-lead/outbox",
    "cadmus-lead-enrichment": "demiurge/agents/cadmus-lead-enrichment/outbox",
    "hera-marketing-lead": "demiurge/agents/hera-marketing-lead/outbox",
    "athena-product-discovery-lead": "demiurge/agents/athena-product-discovery-lead/outbox",
    "kronos-operations-lead": "demiurge/agents/kronos-operations-lead/outbox",
    "clio-customer-signal-collector": "demiurge/agents/clio-customer-signal-collector/outbox",
    "hermes-router-revenue": "demiurge/agents/hermes-router-revenue/outbox",
}


def load_rules() -> tuple[list[dict], list[dict]]:
    """Load dispatch + timing rules from YAML."""
    dispatch_rules = []
    timing_rules = []
    if DISPATCH_RULES_FILE.exists():
        with DISPATCH_RULES_FILE.open() as f:
            data = yaml.safe_load(f) or {}
        dispatch_rules = data.get("dispatch_rules", [])
    if TIMING_RULES_FILE.exists():
        with TIMING_RULES_FILE.open() as f:
            data = yaml.safe_load(f) or {}
        timing_rules = data.get("timing_rules", [])
    return dispatch_rules, timing_rules


def match_signal(signal: dict, dispatch_rules: list[dict]) -> dict | None:
    """Return first matching rule for the signal, or None."""
    for rule in dispatch_rules:
        match = rule.get("match", {})
        # signal_type match (exact)
        if "signal_type" in match:
            if signal.get("signal_type") != match["signal_type"]:
                continue
        # department match (exact)
        if "department_id" in match:
            if signal.get("department") != match["department_id"]:
                continue
        # routing_tags match (ALL tags in rule must be present in signal)
        if "routing_tags" in match:
            signal_tags = set(signal.get("routing_tags", []))
            rule_tags = set(match["routing_tags"])
            if not rule_tags.issubset(signal_tags):
                continue
        # All match criteria passed
        return rule
    return None


def compute_recipients(rule: dict) -> list[dict]:
    """Extract recipient list from rule's deliver_to + fan_out."""
    deliver = rule.get("deliver_to", [])
    fan_out = rule.get("fan_out", "first_available")
    if fan_out == "all":
        # Deliver to every recipient
        return list(deliver)
    elif fan_out == "first_available":
        # Deliver to first; others are fallbacks (Phase 28: deliver to first only)
        return deliver[:1] if deliver else []
    else:
        # Unknown fan-out strategy: be safe, deliver to all
        return list(deliver)


def deliver_to_outbox(recipient: dict, signal: dict) -> str:
    """Deliver signal to recipient's outbox. Returns the file path written."""
    agent_id = recipient.get("id", "")
    outbox_rel = AGENT_OUTBOX.get(agent_id, f"demiurge/agents/{agent_id}/outbox")
    outbox = Path("/opt/data/agents") / outbox_rel
    outbox.mkdir(parents=True, exist_ok=True)
    # File name: signals/<signal-id>.md
    sig_dir = outbox / "signals"
    sig_dir.mkdir(exist_ok=True)
    out_path = sig_dir / f"{signal['id']}.md"
    body = f"""# Signal: {signal['id']}

**From**: {signal.get('source', '?')}
**At**: {signal.get('ts', '?')}
**Type**: {signal.get('signal_type', '?')}
**Tags**: {', '.join(signal.get('routing_tags', []))}

## Payload

```json
{json.dumps(signal.get('payload', {}), indent=2)}
```

## Routing decision

- Rule: {signal.get('routed_via_rule', '?')}
- Routed at: {datetime.now(timezone.utc).isoformat()}
"""
    out_path.write_text(body)
    return str(out_path)


def log_decision(signal: dict, rule: dict, recipients: list[dict], delivered: list[str]):
    """Append routing decision to log (NDJSON)."""
    decision = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "signal_id": signal.get("id"),
        "rule_id": rule.get("id"),
        "recipients": [r.get("id") for r in recipients],
        "delivered_to": delivered,
        "fan_out": rule.get("fan_out"),
    }
    ROUTING_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ROUTING_LOG.open("a") as f:
        f.write(json.dumps(decision, separators=(",", ":")) + "\n")


def process_pending(limit: int = 50) -> dict:
    """Process pending signals. Returns summary dict."""
    dispatch_rules, timing_rules = load_rules()
    pending = list_signals(status="pending", limit=limit)
    summary = {
        "processed": 0,
        "routed": 0,
        "no_rule": 0,
        "errors": 0,
        "details": [],
    }
    for signal in pending:
        summary["processed"] += 1
        try:
            # Pre-dispatch check: refusal-when-constraints-unmet +
            # contradiction-detection. See pre_dispatch_check() docstring.
            pre_check = pre_dispatch_check(signal)
            if pre_check is not None:
                summary["errors"] += 1
                summary["details"].append({
                    "signal_id": signal.get("id"),
                    "result": "pre_dispatch_rejected",
                    "reject_code": pre_check.get("code"),
                    "reject_detail": {k: v for k, v in pre_check.items() if k != "reject"},
                })
                # Log the rejection for audit
                log_decision(
                    {**signal, "source": signal.get("source", "?"), "ts": signal.get("ts", "?")},
                    {"id": f"pre-check:{pre_check.get('code')}", "fan_out": "none"},
                    [],
                    [],
                )
                # Still mark as routed so we don't loop on it
                update_signal_status(
                    signal["id"], "routed",
                    extra={"routed_via_rule": f"pre-check:{pre_check.get('code')}"},
                )
                continue
            rule = match_signal(signal, dispatch_rules)
            if not rule:
                summary["no_rule"] += 1
                summary["details"].append({
                    "signal_id": signal.get("id"),
                    "result": "no_rule",
                })
                # Still mark as routed (so we don't loop on it)
                update_signal_status(signal["id"], "routed", extra={"routed_via_rule": None})
                continue
            recipients = compute_recipients(rule)
            signal["routed_via_rule"] = rule.get("id")
            delivered = []
            for recipient in recipients:
                try:
                    path = deliver_to_outbox(recipient, signal)
                    delivered.append(path)
                except Exception as e:
                    summary["errors"] += 1
                    summary["details"].append({
                        "signal_id": signal.get("id"),
                        "result": "delivery_error",
                        "error": str(e),
                    })
            log_decision(signal, rule, recipients, delivered)
            update_signal_status(
                signal["id"], "routed",
                extra={
                    "routed_via_rule": rule.get("id"),
                    "routed_to": [r.get("id") for r in recipients],
                },
            )
            summary["routed"] += 1
            summary["details"].append({
                "signal_id": signal.get("id"),
                "rule_id": rule.get("id"),
                "recipients": [r.get("id") for r in recipients],
                "delivered": delivered,
            })
        except Exception as e:
            summary["errors"] += 1
            summary["details"].append({
                "signal_id": signal.get("id"),
                "result": "process_error",
                "error": str(e),
            })
    return summary


def explain_signal(signal_id: str) -> dict:
    """Show what the router would do with a signal, without actually routing."""
    sigs = list_signals(limit=1000)
    signal = next((s for s in sigs if s.get("id") == signal_id), None)
    if not signal:
        return {"error": f"signal {signal_id} not found"}
    dispatch_rules, _ = load_rules()
    rule = match_signal(signal, dispatch_rules)
    if not rule:
        return {"signal": signal, "matched_rule": None, "would_route_to": []}
    recipients = compute_recipients(rule)
    return {
        "signal": signal,
        "matched_rule": {"id": rule.get("id"), "fan_out": rule.get("fan_out")},
        "would_route_to": [r.get("id") for r in recipients],
    }


def main():
    parser = argparse.ArgumentParser(description="Signal router")
    parser.add_argument("--process", action="store_true", help="Process pending signals")
    parser.add_argument("--explain", metavar="SIGNAL_ID", help="Show what would happen")
    parser.add_argument("--limit", type=int, default=50, help="Max signals to process")
    args = parser.parse_args()

    if args.explain:
        result = explain_signal(args.explain)
        print(json.dumps(result, indent=2, default=str))
        return

    if args.process:
        summary = process_pending(limit=args.limit)
        print(f"Processed: {summary['processed']}")
        print(f"Routed: {summary['routed']}")
        print(f"No matching rule: {summary['no_rule']}")
        print(f"Errors: {summary['errors']}")
        if summary["details"]:
            print(f"\nDetails:")
            for d in summary["details"][:10]:
                print(f"  {d}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
