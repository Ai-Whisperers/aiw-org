#!/usr/bin/env python3
"""Results collector — verify sub-agent outputs and update task status.

Built as Phase 28 R4 (A3 - Results Collector).

Flow:
    1. Read assigned tasks from each dept's tasks.jsonl
    2. Check if assignee has written a result to outbox/<date>.md
    3. Verify result is non-empty + contains expected sections
    4. Update task status: done | failed | needs_review
    5. Aggregate results for Ivan's daily brief

Per-dept result verification:
    - Read assignee's outbox/<YYYY-MM-DD>.md
    - Check for [DONE] marker or required sections
    - Compute score: passes/fails
    - Update task record

Usage:
    python3 scripts/results-collector.py --check                # check all open tasks
    python3 scripts/results-collector.py --dept sales --check   # check one dept
    python3 scripts/results-collector.py --summary              # show today's summary
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path("/opt/data/agents/state")
AGENTS_ROOT = Path("/opt/data/agents")
RESULTS_LOG = Path("/opt/data/state/results-collector.jsonl")

# Verification rules per assignee (Phase 28 R4: keep simple)
# Format: {agent_name: {"required_sections": [...], "min_words": N, "fail_patterns": [...]}}
VERIFY_RULES = {
    "apollo-sales-lead": {
        "required_sections": ["## Summary", "## Next Steps"],
        "min_words": 50,
        "fail_patterns": [r"^TODO", r"^FIXME"],
    },
    "cadmus-lead-enrichment": {
        "required_sections": ["## Enrichment"],
        "min_words": 30,
        "fail_patterns": [],
    },
    "metis-proposal-drafter": {
        "required_sections": ["## Proposal"],
        "min_words": 100,
        "fail_patterns": [],
    },
    "kronos-operations-lead": {
        "required_sections": ["## Status"],
        "min_words": 30,
        "fail_patterns": [],
    },
    "research-tracker": {
        "required_sections": ["## Summary"],
        "min_words": 30,
        "fail_patterns": [],
    },
    "people-hr": {
        "required_sections": ["## Status"],
        "min_words": 30,
        "fail_patterns": [],
    },
    "finance-controller": {
        "required_sections": ["## Summary"],
        "min_words": 30,
        "fail_patterns": [],
    },
    "engineering-roster": {
        "required_sections": ["## Summary"],
        "min_words": 30,
        "fail_patterns": [],
    },
}

# Default rules if assignee not in VERIFY_RULES
DEFAULT_RULES = {
    "required_sections": [],
    "min_words": 10,
    "fail_patterns": [],
}


def dept_tasks_file(dept: str) -> Path:
    return STATE_DIR / dept / "tasks.jsonl"


def assignee_outbox(agent: str, day: str | None = None) -> Path:
    """Find agent's outbox file for today (or specified day)."""
    if day is None:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Try DEMIURGE path, then dept path
    candidates = [
        AGENTS_ROOT / "demiurge" / "agents" / agent / "outbox" / f"{day}.md",
        AGENTS_ROOT / agent / "outbox" / f"{day}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    # Return first candidate even if missing
    return candidates[0]


def load_tasks(dept: str) -> list[dict]:
    tf = dept_tasks_file(dept)
    if not tf.exists():
        return []
    out = []
    for line in tf.read_text().splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def save_tasks(dept: str, tasks: list[dict]) -> None:
    tf = dept_tasks_file(dept)
    tf.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(t, separators=(",", ":")) for t in tasks]
    tf.write_text("\n".join(lines) + "\n" if lines else "")


def verify_result(assignee: str, content: str) -> dict:
    """Verify an outbox result against rules. Returns verification dict."""
    rules = VERIFY_RULES.get(assignee, DEFAULT_RULES)
    issues = []
    # Check required sections
    for section in rules.get("required_sections", []):
        if section not in content:
            issues.append(f"missing section: {section}")
    # Check word count
    word_count = len(content.split())
    if word_count < rules.get("min_words", 0):
        issues.append(f"too short: {word_count} words < {rules['min_words']}")
    # Check fail patterns
    for pat in rules.get("fail_patterns", []):
        if re.search(pat, content, re.MULTILINE):
            issues.append(f"matched fail pattern: {pat}")
    return {
        "verified": not issues,
        "word_count": word_count,
        "issues": issues,
        "required_sections": rules.get("required_sections", []),
        "min_words": rules.get("min_words", 0),
    }


def check_dept(dept: str, day: str | None = None) -> dict:
    """Check all open tasks for a dept. Update statuses."""
    tasks = load_tasks(dept)
    summary = {
        "dept": dept,
        "total": len(tasks),
        "checked": 0,
        "done": 0,
        "failed": 0,
        "still_open": 0,
        "results": [],
    }
    updated_tasks = []
    for task in tasks:
        if task.get("status") not in ("assigned", "in_progress"):
            updated_tasks.append(task)
            continue
        summary["checked"] += 1
        assignee = task.get("assignee", "unknown")
        outbox = assignee_outbox(assignee, day=day)
        if outbox.exists():
            content = outbox.read_text()
            verification = verify_result(assignee, content)
            if verification["verified"]:
                task["status"] = "done"
                task["verified_at"] = datetime.now(timezone.utc).isoformat()
                task["verification"] = verification
                summary["done"] += 1
            else:
                task["status"] = "needs_review"
                task["verification"] = verification
                summary["failed"] += 1
        else:
            summary["still_open"] += 1
        summary["results"].append({
            "task_id": task.get("task_id"),
            "assignee": assignee,
            "status": task["status"],
            "outbox": str(outbox),
            "outbox_exists": outbox.exists(),
        })
        updated_tasks.append(task)
    save_tasks(dept, updated_tasks)
    log_results(summary)
    return summary


def log_results(summary: dict) -> None:
    """Append results-collector event to log."""
    RESULTS_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **summary,
    }
    with RESULTS_LOG.open("a") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def show_summary(day: str | None = None) -> dict:
    """Show summary across all depts."""
    if day is None:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    depts = [p.name for p in STATE_DIR.iterdir() if p.is_dir()] if STATE_DIR.exists() else []
    out = {"day": day, "depts": []}
    for dept in depts:
        tasks = load_tasks(dept)
        open_t = sum(1 for t in tasks if t.get("status") in ("assigned", "in_progress"))
        done_t = sum(1 for t in tasks if t.get("status") == "done")
        failed_t = sum(1 for t in tasks if t.get("status") == "needs_review")
        out["depts"].append({
            "dept": dept,
            "total": len(tasks),
            "open": open_t,
            "done": done_t,
            "needs_review": failed_t,
        })
    return out


def main():
    parser = argparse.ArgumentParser(description="Results collector")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--dept", help="Specific dept (default: all)")
    parser.add_argument("--day", help="Specific day YYYY-MM-DD")
    args = parser.parse_args()

    if args.check:
        if args.dept:
            s = check_dept(args.dept, day=args.day)
            print(json.dumps(s, indent=2, default=str))
        else:
            depts = [p.name for p in STATE_DIR.iterdir() if p.is_dir()] if STATE_DIR.exists() else []
            for dept in depts:
                s = check_dept(dept, day=args.day)
                print(f"\n=== {dept} ===")
                print(f"  total: {s['total']}, checked: {s['checked']}")
                print(f"  done: {s['done']}, failed: {s['failed']}, open: {s['still_open']}")
        return

    if args.summary:
        out = show_summary(day=args.day)
        print(json.dumps(out, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
