#!/usr/bin/env python3
"""Audit trail reviewer — weekly review of policy violations.

Built as Phase 30 R3 (Tier H4).

Reviews audit logs from the past week and reports:
  - Hard-stops wrapper: how many blocks, override uses, unusual patterns
  - Eval gate: block decisions, force overrides
  - Prompt injection: detected attempts, blocked content
  - PII redaction: redaction counts by pattern
  - State write log: anomalies, failed writes

Outputs a markdown summary to /opt/data/state/audit-weekly-report.md
and writes structured NDJSON to /opt/data/state/audit-summary.jsonl.

Usage:
    python3 scripts/audit-trail-review.py           # weekly review (last 7d)
    python3 scripts/audit-trail-review.py --days 1 # last 24h
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---
import sys as _sys_bootstrap_098
from pathlib import Path as _Path_bootstrap_098
_PY_PATHS_ROOT = _Path_bootstrap_098(__file__).resolve().parent.parent
if str(_PY_PATHS_ROOT) not in _sys_bootstrap_098.path:
    _sys_bootstrap_098.path.insert(0, str(_PY_PATHS_ROOT))
from _paths import AIW_ROOT, STATE
# --- end bootstrap ---


STATE_DIR = STATE
REPORT_PATH = STATE_DIR / "audit-weekly-report.md"
SUMMARY_PATH = STATE_DIR / "audit-summary.jsonl"


def load_ndjson_window(path: Path, days: int) -> list[dict]:
    """Load NDJSON entries within last N days."""
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts_str = entry.get("ts", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if ts >= cutoff:
                out.append(entry)
        except (ValueError, AttributeError):
            continue
    return out


def review_hard_stops(days: int) -> dict:
    """Review hard-stops audit log."""
    entries = load_ndjson_window(STATE_DIR / "hard-stop-audit.ndjson", days)
    if not entries:
        return {"count": 0, "note": "no entries"}
    allowed = sum(1 for e in entries if e.get("allowed"))
    blocked = sum(1 for e in entries if not e.get("allowed"))
    by_agent = Counter(e.get("agent") for e in entries if not e.get("allowed"))
    by_action = Counter(e.get("action") for e in entries if not e.get("allowed"))
    return {
        "count": len(entries),
        "allowed": allowed,
        "blocked": blocked,
        "block_rate": blocked / len(entries) if entries else 0,
        "blocked_by_agent": dict(by_agent.most_common(5)),
        "blocked_by_action": dict(by_action.most_common(5)),
    }


def review_eval_gate(days: int) -> dict:
    """Review eval-gate decisions log."""
    entries = load_ndjson_window(STATE_DIR / "eval-gate-decisions.ndjson", days)
    if not entries:
        return {"count": 0, "note": "no entries"}
    by_decision = Counter(e.get("decision") for e in entries)
    forced = sum(1 for e in entries if e.get("force_used"))
    return {
        "count": len(entries),
        "by_decision": dict(by_decision),
        "force_overrides": forced,
    }


def review_injection(days: int) -> dict:
    """Review prompt-injection attempts log."""
    entries = load_ndjson_window(STATE_DIR / "injection-attempts.jsonl", days)
    if not entries:
        return {"count": 0, "note": "no entries"}
    by_verdict = Counter(e.get("verdict") for e in entries)
    patterns = Counter()
    for e in entries:
        for p in e.get("patterns", []):
            patterns[p["name"]] += 1
    return {
        "count": len(entries),
        "by_verdict": dict(by_verdict),
        "top_patterns": dict(patterns.most_common(5)),
    }


def review_redaction(days: int) -> dict:
    """Review PII redaction log."""
    entries = load_ndjson_window(STATE_DIR / "redaction-log.jsonl", days)
    if not entries:
        return {"count": 0, "note": "no entries"}
    total_redactions = sum(e.get("redactions_count", 0) for e in entries)
    patterns = Counter()
    for e in entries:
        for p in e.get("patterns", []):
            patterns[p] += 1
    return {
        "count": len(entries),
        "total_redactions": total_redactions,
        "top_patterns": dict(patterns.most_common(5)),
    }


def review_state_writes(days: int) -> dict:
    """Review state-write-log.jsonl."""
    entries = load_ndjson_window(STATE_DIR / "state-write-log.jsonl", days)
    if not entries:
        return {"count": 0, "note": "no entries"}
    by_file = Counter(e.get("file") for e in entries)
    return {
        "count": len(entries),
        "by_file": dict(by_file.most_common(5)),
    }


def render_markdown(days: int, summary: dict) -> str:
    """Render summary dict as markdown."""
    lines = [
        f"# Weekly Audit Trail Report",
        f"",
        f"**Period**: last {days} days",
        f"**Generated**: {datetime.now(timezone.utc).isoformat()}",
        f"",
        f"## Hard-Stops Wrapper",
        f"",
    ]
    hs = summary["hard_stops"]
    lines.append(f"- Total checks: {hs.get('count', 0)}")
    lines.append(f"- Allowed: {hs.get('allowed', 0)}")
    lines.append(f"- Blocked: {hs.get('blocked', 0)}")
    if hs.get("blocked", 0) > 0:
        lines.append(f"- Block rate: {hs.get('block_rate', 0):.1%}")
        lines.append(f"- Top blocked agents: {hs.get('blocked_by_agent', {})}")
        lines.append(f"- Top blocked actions: {hs.get('blocked_by_action', {})}")
    lines.append("")

    lines.append("## Eval Gate")
    lines.append("")
    eg = summary["eval_gate"]
    lines.append(f"- Total decisions: {eg.get('count', 0)}")
    if eg.get("count", 0) > 0:
        lines.append(f"- By decision: {eg.get('by_decision', {})}")
        lines.append(f"- Force overrides: {eg.get('force_overrides', 0)}")
    lines.append("")

    lines.append("## Prompt Injection Detection")
    lines.append("")
    inj = summary["injection"]
    lines.append(f"- Total attempts: {inj.get('count', 0)}")
    if inj.get("count", 0) > 0:
        lines.append(f"- By verdict: {inj.get('by_verdict', {})}")
        lines.append(f"- Top patterns: {inj.get('top_patterns', {})}")
    lines.append("")

    lines.append("## PII Redaction")
    lines.append("")
    rd = summary["redaction"]
    lines.append(f"- Total events: {rd.get('count', 0)}")
    if rd.get("count", 0) > 0:
        lines.append(f"- Total redactions: {rd.get('total_redactions', 0)}")
        lines.append(f"- Top patterns: {rd.get('top_patterns', {})}")
    lines.append("")

    lines.append("## State Writes")
    lines.append("")
    sw = summary["state_writes"]
    lines.append(f"- Total writes: {sw.get('count', 0)}")
    if sw.get("count", 0) > 0:
        lines.append(f"- Top files: {sw.get('by_file', {})}")
    lines.append("")

    # Action items
    lines.append("## Action Items")
    lines.append("")
    items = []
    if hs.get("block_rate", 0) > 0.5:
        items.append("- High hard-stops block rate — investigate: are legitimate actions being misclassified?")
    if eg.get("force_overrides", 0) > 5:
        items.append(f"- {eg['force_overrides']} eval-gate force overrides — review for abuse")
    if inj.get("by_verdict", {}).get("blocked", 0) > 0:
        items.append("- Prompt injection attempts blocked — investigate source")
    if rd.get("total_redactions", 0) > 100:
        items.append("- High PII redaction volume — review for compliance")
    if not items:
        items.append("- (none — clean audit)")
    lines.extend(items)
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit trail review")
    parser.add_argument("--days", type=int, default=7, help="Days to review (default 7)")
    parser.add_argument("--quiet", action="store_true",
                        help="Don't write markdown report")
    args = parser.parse_args()

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "days": args.days,
        "hard_stops": review_hard_stops(args.days),
        "eval_gate": review_eval_gate(args.days),
        "injection": review_injection(args.days),
        "redaction": review_redaction(args.days),
        "state_writes": review_state_writes(args.days),
    }

    # Write structured NDJSON summary
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("a") as f:
        f.write(json.dumps(summary, separators=(",", ":")) + "\n")

    # Markdown report
    if not args.quiet:
        report = render_markdown(args.days, summary)
        REPORT_PATH.write_text(report)
        print(f"Report written: {REPORT_PATH}")

    # Stdout summary
    print(json.dumps({
        "days": args.days,
        "hard_stops": summary["hard_stops"]["count"],
        "eval_gate": summary["eval_gate"]["count"],
        "injection": summary["injection"]["count"],
        "redaction": summary["redaction"]["count"],
        "state_writes": summary["state_writes"]["count"],
    }, indent=2))


if __name__ == "__main__":
    main()
