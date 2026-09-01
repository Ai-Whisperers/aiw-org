#!/usr/bin/env python3
"""Cron failure diagnosis tool — categorize root causes.

Built as Phase 35 R4 (Q4a).

Reads /opt/data/state/cron-error-watchdog.json and categorizes failures into:
  - token_plan: HTTP 429 token plan exhaustion (auto-recover Sunday)
  - network: Connection/network errors
  - code: Python exceptions (bugs)
  - permission: 401/403 auth errors
  - timeout: 504/timeout errors
  - unknown: other / unrecognized

Outputs:
  /opt/data/state/cron-failure-diagnosis.md

Usage:
    python3 scripts/cron-diagnose.py            # full report
    python3 scripts/cron-diagnose.py --summary # brief summary
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

WATCHDOG = Path("/opt/data/state/cron-error-watchdog.json")
REPORT = Path("/opt/data/state/cron-failure-diagnosis.md")


# Pattern -> category
CATEGORIES = [
    ("token_plan", re.compile(r"429|token.?plan|usage.?limit", re.I)),
    ("network", re.compile(r"connection.?refused|connection.?reset|network.?unreachable|connectionerror", re.I)),
    ("code", re.compile(r"Traceback\s*\(most recent call last\)|AttributeError|TypeError|KeyError|NameError|ImportError|ModuleNotFoundError|SyntaxError", re.I)),
    ("permission", re.compile(r"401|403|unauthorized|forbidden|permission.?denied", re.I)),
    ("timeout", re.compile(r"504|timeout|timed.?out", re.I)),
    ("rate_limit_other", re.compile(r"429|rate.?limit|too.?many.?requests", re.I)),
]


def classify_error(error_text: str) -> str:
    """Classify an error message into a category."""
    for category, regex in CATEGORIES:
        if regex.search(error_text):
            return category
    return "unknown"


def diagnose(jobs: dict | None = None) -> dict:
    """Diagnose all failures in the watchdog.

    Returns dict: category -> list of {cron_name, last_run_at, error_preview}
    """
    if not WATCHDOG.exists():
        return {}

    try:
        data = json.loads(WATCHDOG.read_text())
    except (json.JSONDecodeError, OSError):
        return {}

    details = data.get("details", [])
    findings = defaultdict(list)
    by_name = defaultdict(int)

    for entry in details:
        name = entry.get("name")
        error = entry.get("last_error", "")
        if not name:
            continue
        category = classify_error(error)
        by_name[name] += 1
        findings[category].append({
            "name": name,
            "count": by_name[name],
            "last_run_at": entry.get("last_run_at"),
            "error_preview": error[:200] if error else "(no error)",
        })

    return dict(findings)


def render_report(findings: dict) -> str:
    """Render findings as markdown."""
    lines = [
        "# Cron Failure Diagnosis",
        "",
        f"**Date**: {datetime.now(timezone.utc).isoformat()}",
        f"**Source**: {WATCHDOG}",
        "",
        "## Summary",
        "",
    ]
    total = sum(len(v) for v in findings.values())
    lines.append(f"Total failure entries: {total}")
    lines.append("")

    if not findings:
        lines.append("(no failures)")
        return "\n".join(lines)

    lines.append("## Category Counts")
    lines.append("")
    for category, items in sorted(findings.items(), key=lambda x: -len(x[1])):
        lines.append(f"- **{category}**: {len(items)} entries ({len({i['name'] for i in items})} unique crons)")
    lines.append("")

    for category, items in findings.items():
        lines.append(f"## {category}")
        lines.append("")
        unique = {}
        for item in items:
            unique[item["name"]] = item
        for name, item in sorted(unique.items()):
            lines.append(f"### {name}")
            lines.append(f"- count: {item['count']}")
            lines.append(f"- last_run: {item['last_run_at']}")
            lines.append(f"- error: `{item['error_preview']}`")
            lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    recs = []
    if "token_plan" in findings:
        n = len({i['name'] for i in findings['token_plan']})
        recs.append(f"- **{n} crons failing due to token plan exhaustion**")
        recs.append("  - Wait for weekly Sunday auto-recovery")
        recs.append("  - Or upgrade token plan (decision pending Kiki/finance)")
    if "code" in findings:
        n = len({i['name'] for i in findings['code']})
        recs.append(f"- **{n} crons failing with Python errors** (action needed)")
        recs.append("  - Check traceback in error_preview")
        recs.append("  - Fix code or report to engineering")
    if "permission" in findings:
        n = len({i['name'] for i in findings['permission']})
        recs.append(f"- **{n} crons failing with permission errors**")
        recs.append("  - Check credentials + BWS tokens")
        recs.append("  - Re-authenticate or rotate credentials")
    if "network" in findings:
        n = len({i['name'] for i in findings['network']})
        recs.append(f"- **{n} crons failing with network errors**")
        recs.append("  - Check connectivity + DNS")
        recs.append("  - Retry logic in script if not present")
    if "timeout" in findings:
        n = len({i['name'] for i in findings['timeout']})
        recs.append(f"- **{n} crons timing out**")
        recs.append("  - Increase timeout or optimize script")
    if "unknown" in findings:
        n = len({i['name'] for i in findings['unknown']})
        recs.append(f"- **{n} crons failing with unknown errors**")
        recs.append("  - Manual investigation needed")
    if not recs:
        recs.append("- (none)")
    lines.extend(recs)
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cron failure diagnosis")
    parser.add_argument("--summary", action="store_true", help="Brief summary only")
    args = parser.parse_args()

    findings = diagnose()

    if args.summary:
        print("=== Cron Failure Diagnosis (Summary) ===")
        total = sum(len(v) for v in findings.values())
        print(f"Total entries: {total}")
        for category, items in sorted(findings.items(), key=lambda x: -len(x[1])):
            n_crons = len({i['name'] for i in items})
            print(f"  {category}: {len(items)} entries ({n_crons} unique crons)")
        return 0

    # Full report
    report = render_report(findings)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report)
    print(f"Report: {REPORT}")
    print()
    # Print brief summary
    total = sum(len(v) for v in findings.values())
    print(f"Total failure entries: {total}")
    for category, items in sorted(findings.items(), key=lambda x: -len(x[1])):
        n_crons = len({i['name'] for i in items})
        print(f"  {category}: {len(items)} entries ({n_crons} unique crons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
