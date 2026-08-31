#!/usr/bin/env python3
"""build-agent-context.py — Build optimal context windows per agent.

Factor 3: Own your context window.

For each agent, gather:
- Prior brief (last 7 days)
- Org-state relevant section
- Today's focus area
- Relevant skill stack snippets
- Recent errors

Output: /opt/data/state/contexts/<agent>/<date>.json
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

STATE_DIR = Path("/opt/data/state")
ORG_STATE = STATE_DIR / "org-state.json"
COST_TRACKER = STATE_DIR / "cost-tracker.json"
ERRORS_FILE = STATE_DIR / "errors.json"
CONTEXTS_DIR = STATE_DIR / "contexts"


def load_json(path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except:
        return default


def build_context_for_agent(agent_name: str) -> dict:
    """Build the optimal context window for one agent."""
    
    # 1. Prior brief (last 7 days)
    agent_dir = Path(f"/opt/data/agents/{agent_name}")
    recent_briefs = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    
    for subdir in ["outbox", "lessons"]:
        d = agent_dir / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md"), reverse=True):
            try:
                date = datetime.strptime(f.stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if date >= cutoff:
                    recent_briefs.append({
                        "date": f.stem,
                        "subdir": subdir,
                        "path": str(f),
                        "preview": f.read_text()[:200],
                    })
            except ValueError:
                continue
        if len(recent_briefs) >= 3:
            break
    
    # 2. Org state
    org = load_json(ORG_STATE)
    agent_state = org.get("agents", {}).get(agent_name, {})
    
    # 3. Cost info (for this agent)
    cost = load_json(COST_TRACKER)
    agent_cost = cost.get("agents", {}).get(agent_name, {})
    
    # 4. Recent errors (for this agent)
    errors = load_json(ERRORS_FILE)
    agent_errors = [e for e in errors.get("errors", []) if e.get("job") == f"aiw-{agent_name}"]
    
    return {
        "agent": agent_name,
        "ts": datetime.now(timezone.utc).isoformat(),
        "prior_briefs": recent_briefs[:3],  # last 3
        "agent_state": {
            "brief_count": agent_state.get("brief_count", 0),
            "latest_brief": agent_state.get("latest_brief"),
        },
        "cost": {
            "runs_per_day": agent_cost.get("runs_per_day", 0),
            "monthly_cost_usd": agent_cost.get("monthly_cost_usd", 0),
        },
        "recent_errors": agent_errors[:5],
        "global_context": {
            "total_agents": org.get("metrics", {}).get("agents_total", 0),
            "eval_gate": org.get("eval_gate", {}),
            "customers": org.get("metrics", {}).get("customers_total", 0),
        },
    }


def main():
    CONTEXTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read org-state to get all agents
    org = load_json(ORG_STATE)
    agent_names = list(org.get("agents", {}).keys())
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    built = 0
    for agent_name in agent_names:
        ctx = build_context_for_agent(agent_name)
        agent_ctx_dir = CONTEXTS_DIR / agent_name
        agent_ctx_dir.mkdir(parents=True, exist_ok=True)
        ctx_path = agent_ctx_dir / f"{today}.json"
        ctx_path.write_text(json.dumps(ctx, indent=2, default=str))
        built += 1
    
    print(f"✓ Built {built} context windows for {today}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

