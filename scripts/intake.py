#!/usr/bin/env python3
"""Intake — per-dept secretary that processes routed signals into tasks.

Built as Phase 28 R3 (A2 - Intake).

Flow:
    1. Read pending signals routed to this dept (from signal queue)
    2. Look up dept's sub-agents (composition field from PROMPT.md)
    3. Match signal to sub-agent by signal_type + routing_tags
    4. Create task in dept's task file (state/<dept>/tasks.jsonl)
    5. Notify assigned sub-agent (write to sub-agent's signal inbox)
    6. Track task status

Dept mapping (canonical):
    sales:        apollo-sales-lead, cadmus-lead-enrichment, metis-proposal-drafter
    finance:      finance-controller, business-analyst
    operations:   management-coordinator, kronos-operations-lead, ai-ops-coordinator
    research:     research-tracker
    engineering:  engineering-roster, ai-safety-engineer
    people:       people-hr

Usage:
    python3 scripts/intake.py --dept sales --process    # process pending signals
    python3 scripts/intake.py --dept sales --list       # list dept tasks
    python3 scripts/intake.py --dept sales --status     # show dept intake status
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add scripts/ to path for signal_queue
sys.path.insert(0, str(Path(__file__).parent))
from signal_queue import SIGNAL_QUEUE, list_signals  # type: ignore

STATE_DIR = Path("/opt/data/agents/state")
AGENTS_ROOT = Path("/opt/data/agents")

# Dept → list of sub-agent names (the secretary's team)
DEPT_AGENTS = {
    "sales": ["apollo-sales-lead", "cadmus-lead-enrichment", "metis-proposal-drafter"],
    "finance": ["finance-controller", "business-analyst"],
    "operations": ["management-coordinator", "kronos-operations-lead", "ai-ops-coordinator"],
    "research": ["research-tracker"],
    "engineering": ["engineering-roster", "ai-safety-engineer"],
    "people": ["people-hr"],
    "board": ["ai-ops-coordinator", "apollo-sales-lead"],
}

# Signal type / routing tag → sub-agent assignment rules
ASSIGNMENT_RULES = [
    {"match": {"routing_tags": ["lead", "inbound"]}, "assign_to": "apollo-sales-lead"},
    {"match": {"routing_tags": ["enrichment"]}, "assign_to": "cadmus-lead-enrichment"},
    {"match": {"routing_tags": ["proposal"]}, "assign_to": "metis-proposal-drafter"},
    {"match": {"routing_tags": ["content"]}, "assign_to": "apollo-sales-lead"},
    {"match": {"routing_tags": ["insight"]}, "assign_to": "research-tracker"},
    {"match": {"routing_tags": ["drift", "hard-stop"]}, "assign_to": "kronos-operations-lead"},
    {"match": {"routing_tags": ["compliance"]}, "assign_to": "kronos-operations-lead"},
    {"match": {"routing_tags": ["customer"]}, "assign_to": "management-coordinator"},
    # Default: dept lead
]


def dept_tasks_file(dept: str) -> Path:
    """Path to dept's task log."""
    p = STATE_DIR / dept / "tasks.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def assign_to_subagent(signal: dict, dept: str) -> str:
    """Determine which sub-agent should handle this signal."""
    routing_tags = set(signal.get("routing_tags", []))
    for rule in ASSIGNMENT_RULES:
        rule_tags = set(rule["match"].get("routing_tags", []))
        if rule_tags.issubset(routing_tags):
            return rule["assign_to"]
    # Default: first sub-agent in dept
    agents = DEPT_AGENTS.get(dept, [])
    return agents[0] if agents else "unknown"


def create_task(signal: dict, dept: str, assignee: str) -> dict:
    """Create a task from a routed signal."""
    task = {
        "task_id": f"task-{signal['id']}",
        "signal_id": signal["id"],
        "dept": dept,
        "assignee": assignee,
        "status": "assigned",  # assigned | in_progress | done | failed | escalated
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": signal.get("source"),
        "summary": f"Handle {signal.get('signal_type', '?')} signal: {', '.join(signal.get('routing_tags', []))}",
        "payload": signal.get("payload", {}),
        "signal_ts": signal.get("ts"),
    }
    return task


def notify_assignee(task: dict, agent: str) -> str:
    """Write task notification to agent's signal inbox."""
    # Try DEMIURGE path first, then dept path
    candidates = [
        AGENTS_ROOT / "demiurge" / "agents" / agent / "outbox" / "signals",
        AGENTS_ROOT / agent / "outbox" / "signals",
    ]
    sig_dir = None
    for c in candidates:
        if c.parent.exists():
            sig_dir = c
            break
    if sig_dir is None:
        sig_dir = candidates[0]
    sig_dir.mkdir(parents=True, exist_ok=True)
    out_path = sig_dir / f"{task['task_id']}.md"
    body = f"""# Task: {task['task_id']}

**From**: {dept_name(task['dept'])} intake
**At**: {task['created_at']}
**Signal**: {task['signal_id']} (from {task['source']})

## Summary

{task['summary']}

## Payload

```json
{json.dumps(task['payload'], indent=2)}
```

## Action required

1. Read the signal source: `{task['source']}`
2. Process per your agent's PROMPT.md
3. Write result to your outbox/ directory
4. Mark task done (set status=done in {task['dept']}/tasks.jsonl)
"""
    out_path.write_text(body)
    return str(out_path)


def dept_name(dept: str) -> str:
    """Map dept code to full name."""
    return {
        "sales": "Sales",
        "finance": "Finance",
        "operations": "Operations",
        "research": "Research",
        "engineering": "Engineering",
        "people": "People",
        "board": "Board",
    }.get(dept, dept)


def append_task(task: dict, dept: str) -> None:
    """Append task to dept's task file (NDJSON)."""
    tasks_file = dept_tasks_file(dept)
    line = json.dumps(task, separators=(",", ":")) + "\n"
    # Cap at 10MB
    if tasks_file.exists() and tasks_file.stat().st_size > 10 * 1024 * 1024:
        archive = tasks_file.with_suffix(f".{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.ndjson")
        tasks_file.rename(archive)
    with tasks_file.open("a") as f:
        f.write(line)


def list_dept_tasks(dept: str, status: str | None = None) -> list[dict]:
    """List tasks for a dept."""
    tasks_file = dept_tasks_file(dept)
    if not tasks_file.exists():
        return []
    out = []
    for line in tasks_file.read_text().splitlines():
        if not line.strip():
            continue
        try:
            t = json.loads(line)
        except json.JSONDecodeError:
            continue
        if status is None or t.get("status") == status:
            out.append(t)
    return out


def process_dept(dept: str, limit: int = 50) -> dict:
    """Process pending signals routed to a dept."""
    # Read pending signals
    pending = list_signals(status="routed", limit=500)
    # Filter by dept (signal.routed_to includes dept's agents, or signal.department matches)
    dept_agents = set(DEPT_AGENTS.get(dept, []))
    relevant = []
    for sig in pending:
        routed_to = sig.get("routed_to", [])
        if any(agent in dept_agents for agent in routed_to):
            relevant.append(sig)
        if len(relevant) >= limit:
            break

    summary = {
        "dept": dept,
        "considered": len(pending),
        "relevant": len(relevant),
        "assigned": 0,
        "errors": 0,
        "tasks": [],
    }
    for sig in relevant:
        try:
            assignee = assign_to_subagent(sig, dept)
            task = create_task(sig, dept, assignee)
            append_task(task, dept)
            path = notify_assignee(task, assignee)
            summary["assigned"] += 1
            summary["tasks"].append({
                "task_id": task["task_id"],
                "assignee": assignee,
                "notified_at": path,
            })
        except Exception as e:
            summary["errors"] += 1
            summary["tasks"].append({"signal_id": sig.get("id"), "error": str(e)})
    return summary


def main():
    parser = argparse.ArgumentParser(description="Per-dept intake")
    parser.add_argument("--dept", required=True, choices=list(DEPT_AGENTS.keys()))
    parser.add_argument("--process", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--task-status", default=None,
                        choices=["assigned", "in_progress", "done", "failed", "escalated"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    if args.process:
        s = process_dept(args.dept, limit=args.limit)
        print(f"Dept: {s['dept']}")
        print(f"Pending signals: {s['considered']}")
        print(f"Relevant to dept: {s['relevant']}")
        print(f"Assigned: {s['assigned']}")
        print(f"Errors: {s['errors']}")
        if s["tasks"]:
            print(f"\nTasks:")
            for t in s["tasks"][:5]:
                print(f"  {t}")
        return

    if args.list:
        tasks = list_dept_tasks(args.dept, status=args.task_status)
        print(f"Dept: {args.dept}, tasks: {len(tasks)}")
        for t in tasks[:20]:
            print(f"  {t['task_id']} [{t['status']}] -> {t['assignee']}: {t['summary'][:60]}")
        return

    if args.status:
        tasks = list_dept_tasks(args.dept)
        counts = {}
        for t in tasks:
            s = t.get("status", "unknown")
            counts[s] = counts.get(s, 0) + 1
        print(f"Dept: {args.dept}, total tasks: {len(tasks)}")
        for s, c in counts.items():
            print(f"  {s}: {c}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
