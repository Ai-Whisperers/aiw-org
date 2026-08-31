#!/usr/bin/env python3
"""build-org-state.py — Build the unified Factor 5 state file.

Aggregates data from all current state locations into /opt/data/state/org-state.json.

Sources:
- /opt/data/agents/state/*.json (per-agent state)
- /opt/data/state/customers.json (webhook customers)
- /opt/data/state/coaching-customers.json (coaching pipeline)
- /opt/data/cron/jobs.json (cron config)
- /opt/data/agents/<agent>/outbox/*.md (briefs)
- /opt/data/agents/<agent>/lessons/*.md (lessons)
- /opt/data/db/eval-gate.db (eval-gate runs)

Outputs:
- /opt/data/state/org-state.json — unified single source of truth
- /opt/data/state/org-state-history/ — versioned snapshots (git-able)
"""
import json
import os
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/state")
AGENTS_DIR = Path("/opt/data/agents")
DB_DIR = Path("/opt/data/db")
CRON_FILE = Path("/opt/data/cron/jobs.json")

ORG_STATE_FILE = STATE_DIR / "org-state.json"
ORG_STATE_HISTORY = STATE_DIR / "org-state-history"


def load_json(path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except:
        return default


def get_agent_state(agent_name: str) -> dict:
    """Read per-agent state from agents/state/ if exists."""
    state_path = Path(f"/opt/data/agents/state/{agent_name}.json")
    if not state_path.exists():
        return {}
    return load_json(state_path)


def get_agent_briefs(agent_name: str) -> list:
    """Find all briefs for an agent (outbox + lessons)."""
    briefs = []
    for subdir in ["outbox", "lessons"]:
        d = Path(f"/opt/data/agents/{agent_name}/{subdir}")
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            stat = f.stat()
            briefs.append({
                "date": f.stem,
                "subdir": subdir,
                "path": str(f),
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            })
    return briefs


def get_eval_gate_state() -> dict:
    """Read eval-gate DB for latest run."""
    db_path = DB_DIR / "eval-gate.db"
    if not db_path.exists():
        return {}
    try:
        con = sqlite3.connect(str(db_path))
        c = con.cursor()
        c.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        if not row:
            con.close()
            return {}
        c.execute("SELECT COUNT(*), SUM(pass_count), SUM(fail_count) FROM runs")
        agg = c.fetchone()
        con.close()
        return {
            "last_run_id": row[0],
            "last_run_ts": row[1],
            "last_total": row[2],
            "last_pass": row[3],
            "last_fail": row[4],
            "all_runs": agg[0] or 0,
            "all_pass": agg[1] or 0,
            "all_fail": agg[2] or 0,
        }
    except:
        return {}


def get_cron_state() -> dict:
    """Count cron jobs from jobs.json."""
    if not CRON_FILE.exists():
        return {}
    data = load_json(CRON_FILE)
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    if isinstance(jobs, dict):
        jobs = jobs.get("jobs", list(jobs.values()))
    
    enabled = sum(1 for j in jobs if isinstance(j, dict) and j.get("enabled", True))
    no_agent = sum(1 for j in jobs if isinstance(j, dict) and j.get("no_agent"))
    
    return {
        "total_jobs": len(jobs),
        "enabled": enabled,
        "no_agent_scripts": no_agent,
    }


def get_live_cron_state() -> dict:
    """Get live cron state from hermes."""
    try:
        r = subprocess.run(
            ["/opt/hermes/.venv/bin/hermes", "cron", "list"],
            capture_output=True, text=True, timeout=15
        )
        active = r.stdout.count("Name:")
        return {
            "live_active": active,
        }
    except:
        return {}


def build_org_state() -> dict:
    """Build the complete unified state."""
    # Per-agent state
    agents_state = {}
    all_agents = sorted([p.parent.name for p in Path("/opt/data/agents").rglob("PROMPT.md") if p.parent.name != "agents"])
    
    for agent_name in all_agents:
        agent_state_data = get_agent_state(agent_name)
        briefs = get_agent_briefs(agent_name)
        agents_state[agent_name] = {
            "state_data": agent_state_data,
            "briefs": briefs,
            "brief_count": len(briefs),
            "latest_brief": briefs[-1] if briefs else None,
        }
    
    # Global state
    customers = load_json(STATE_DIR / "customers.json", {"customers": []})
    coaching = load_json(STATE_DIR / "coaching-customers.json", {"customers": {}, "last_updated": None})
    
    # Metrics
    metrics = {
        "agents_total": len(all_agents),
        "agents_with_state": sum(1 for a in agents_state.values() if a["state_data"]),
        "agents_with_briefs": sum(1 for a in agents_state.values() if a["brief_count"] > 0),
        "total_briefs": sum(a["brief_count"] for a in agents_state.values()),
        "customers_total": len(customers.get("customers", [])),
        "customers_onboarded": sum(1 for c in customers.get("customers", []) if c.get("onboarded")),
        "coaching_pipeline": len(coaching.get("customers", {})),
        "mrr_usd": 0,  # No real revenue yet
        "burn_usd_month": 0,  # No real cost tracking yet
    }
    
    return {
        "version": "1.0.0",
        "schema": "org-state-v1",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "agents": agents_state,
        "global": {
            "customers": customers.get("customers", []),
            "coaching": coaching.get("customers", {}),
            "webhook_log_count": sum(1 for _ in (STATE_DIR / "webhook-log.json").open() if _.strip()) if (STATE_DIR / "webhook-log.json").exists() else 0,
        },
        "cron": {**get_cron_state(), **get_live_cron_state()},
        "eval_gate": get_eval_gate_state(),
        "metrics": metrics,
        "sources": {
            "agents_state_dir": "/opt/data/agents/state/",
            "global_state_dir": str(STATE_DIR),
            "cron_file": str(CRON_FILE),
            "db_dir": str(DB_DIR),
        },
    }


def save_snapshot(org_state):
    """Save current state to history dir (git-able)."""
    ORG_STATE_HISTORY.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snap_path = ORG_STATE_HISTORY / f"{ts}.json"
    snap_path.write_text(json.dumps(org_state, indent=2, default=str))
    return snap_path


def main():
    org_state = build_org_state()
    
    # Atomic write
    tmp = ORG_STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(org_state, indent=2, default=str))
    tmp.replace(ORG_STATE_FILE)
    
    snap_path = save_snapshot(org_state)
    
    print(f"✓ Built org-state.json ({len(json.dumps(org_state)):,} bytes)")
    print(f"  Agents: {len(org_state['agents'])}")
    print(f"  Briefs: {org_state['metrics']['total_briefs']}")
    print(f"  Customers: {org_state['metrics']['customers_total']}")
    print(f"  Coaching pipeline: {org_state['metrics']['coaching_pipeline']}")
    print(f"  Cron jobs: {org_state['cron'].get('total_jobs')} (file) / {org_state['cron'].get('live_active')} (live)")
    print(f"  Eval-gate: {org_state['eval_gate']}")
    print(f"\n  Snapshot: {snap_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

