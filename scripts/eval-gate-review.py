#!/usr/bin/env python3
"""Eval-gate enforcement review — weekly summary of blocks.

Built as Phase 30 R3 (Tier G2).

Reads eval-gate-decisions.jsonl from the past 7 days and produces:
  - Markdown report: /opt/data/state/eval-gate-weekly-report.md
  - JSON summary: /opt/data/state/eval-gate-summary.jsonl

Reports:
  - Total decisions
  - By decision (allow/warn/block)
  - Force overrides (operator bypasses)
  - Top blocked agents
  - Top agents with force overrides (suspicious patterns)
  - Recommendations (e.g., "tighten threshold if block rate > 50%")

Usage:
    python3 scripts/eval-gate-review.py           # last 7 days
    python3 scripts/eval-gate-review.py --days 30
"""
import argparse
import json
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
DECISIONS_LOG = STATE_DIR / "eval-gate-decisions.ndjson"
REPORT_PATH = STATE_DIR / "eval-gate-weekly-report.md"
SUMMARY_PATH = STATE_DIR / "eval-gate-summary.jsonl"


def load_window(path: Path, days: int) -> list[dict]:
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


def review(days: int) -> dict:
    entries = load_window(DECISIONS_LOG, days)
    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "total": len(entries),
        "by_decision": dict(Counter(e.get("decision") for e in entries)),
        "force_overrides": sum(1 for e in entries if e.get("force_used")),
        "top_blocked_agents": dict(Counter(e.get("agent") for e in entries if e.get("decision") == "block").most_common(5)),
        "top_force_override_agents": dict(Counter(e.get("agent") for e in entries if e.get("force_used")).most_common(5)),
    }
    return summary


def render_markdown(days: int, summary: dict) -> str:
    lines = [
        f"# Eval-Gate Weekly Report",
        f"",
        f"**Period**: last {days} days",
        f"**Generated**: {summary['ts']}",
        f"",
        f"## Summary",
        f"",
        f"- Total decisions: {summary['total']}",
        f"- By decision: {summary['by_decision']}",
        f"- Force overrides: {summary['force_overrides']}",
        f"",
    ]
    if summary["top_blocked_agents"]:
        lines.append("## Top Blocked Agents")
        lines.append("")
        for agent, count in summary["top_blocked_agents"].items():
            lines.append(f"- {agent}: {count} blocks")
        lines.append("")
    if summary["top_force_override_agents"]:
        lines.append("## Top Force-Override Agents")
        lines.append("")
        lines.append("(Force overrides = operator bypassed block with --force)")
        lines.append("")
        for agent, count in summary["top_force_override_agents"].items():
            lines.append(f"- {agent}: {count} overrides")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Eval-gate enforcement review")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    summary = review(args.days)

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("a") as f:
        f.write(json.dumps(summary, separators=(",", ":")) + "\n")

    report = render_markdown(args.days, summary)
    REPORT_PATH.write_text(report)
    print(f"Report: {REPORT_PATH}")
    print(json.dumps({
        "days": args.days,
        "total": summary["total"],
        "by_decision": summary["by_decision"],
        "force_overrides": summary["force_overrides"],
    }, indent=2))


if __name__ == "__main__":
    main()
