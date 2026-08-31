#!/usr/bin/env python3
"""migrate_state_to_sqlite.py — One-shot migration from JSON state to SQLite.

For each agent's state JSON, create a SQLite DB with the common schema
and migrate the episodic fields.

Usage:
    python3 migrate_state_to_sqlite.py                  # migrate all
    python3 migrate_state_to_sqlite.py <agent> ...      # migrate specific agents
"""
import gzip
import json
import sqlite3
import sys
from pathlib import Path

STATE_DIR = Path("/opt/data/agents/state")
DB_DIR = Path("/opt/data/db")

COMMON_SCHEMA = """
CREATE TABLE IF NOT EXISTS idempotency (
    job_id TEXT PRIMARY KEY,
    last_run TEXT,
    window TEXT,
    status TEXT,
    override_token TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT,
    override_token TEXT
);

CREATE TABLE IF NOT EXISTS escalations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    reason TEXT NOT NULL,
    context_payload TEXT NOT NULL,
    resolved_by TEXT,
    resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS state_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    data BLOB NOT NULL,
    source TEXT
);

CREATE TABLE IF NOT EXISTS cost_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    model TEXT,
    tokens_in INTEGER,
    tokens_out INTEGER,
    cost_usd REAL NOT NULL,
    task TEXT
);

CREATE INDEX IF NOT EXISTS idx_decisions_ts ON decisions(ts DESC);
CREATE INDEX IF NOT EXISTS idx_escalations_ts ON escalations(ts DESC);
CREATE INDEX IF NOT EXISTS idx_cost_log_ts ON cost_log(ts DESC);
"""

AGENT_SCHEMAS = {
    "business-analyst": """
CREATE TABLE IF NOT EXISTS kpi_snapshot (
    date TEXT PRIMARY KEY,
    pipeline_usd REAL,
    mrr_usd REAL,
    leads_24h INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS open_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT
);
""",
    "management-coordinator": """
CREATE TABLE IF NOT EXISTS stuck_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo TEXT NOT NULL,
    issue_number INTEGER,
    title TEXT,
    owner TEXT,
    since TEXT,
    resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS stale_repos (
    repo TEXT PRIMARY KEY,
    last_push TEXT,
    days_idle INTEGER
);
""",
    "finance-controller": """
CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT NOT NULL,
    value_usd REAL NOT NULL,
    stage TEXT NOT NULL,
    expected_close TEXT,
    signed_at TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_id INTEGER REFERENCES deals(id),
    amount_usd REAL NOT NULL,
    issued_at TEXT NOT NULL,
    paid_at TEXT,
    due_at TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS compliance_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    flag_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    resolved_at TEXT
);
""",
    "sales-pipeline": """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company TEXT,
    icp_match_pct REAL,
    stage TEXT NOT NULL,
    value_usd REAL,
    source TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    next_action TEXT,
    blocker TEXT
);

CREATE TABLE IF NOT EXISTS outreach_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id),
    channel TEXT NOT NULL,
    message TEXT,
    sent_at TEXT NOT NULL,
    response TEXT,
    outcome TEXT
);

CREATE TABLE IF NOT EXISTS funnel_30d (
    date TEXT PRIMARY KEY,
    leads INTEGER DEFAULT 0,
    qualified INTEGER DEFAULT 0,
    proposals INTEGER DEFAULT 0,
    signed INTEGER DEFAULT 0,
    lost INTEGER DEFAULT 0,
    pipeline_value_usd REAL DEFAULT 0
);
""",
    "engineering-roster": """
CREATE TABLE IF NOT EXISTS deploys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,
    deployed_at TEXT NOT NULL,
    deployed_by TEXT,
    status TEXT NOT NULL,
    rollback_at TEXT
);

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    site TEXT,
    severity TEXT,
    description TEXT,
    resolved_at TEXT,
    root_cause TEXT
);

CREATE TABLE IF NOT EXISTS prs_review (
    pr_id INTEGER PRIMARY KEY,
    repo TEXT NOT NULL,
    number INTEGER NOT NULL,
    title TEXT,
    author TEXT,
    created_at TEXT NOT NULL,
    age_days INTEGER
);
""",
    "research-tracker": """
CREATE TABLE IF NOT EXISTS thesis_chapters (
    chapter INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    last_commit TEXT,
    word_count INTEGER,
    target_words INTEGER
);

CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue TEXT NOT NULL,
    title TEXT,
    status TEXT NOT NULL,
    deadline TEXT,
    submitted_at TEXT,
    decision_at TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    modules_total INTEGER,
    modules_done INTEGER DEFAULT 0
);
""",
    "kiki-coach": """
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    topic TEXT NOT NULL,
    file_path TEXT NOT NULL,
    delivered_at TEXT,
    completed_at TEXT,
    feedback TEXT
);

CREATE TABLE IF NOT EXISTS curriculum (
    position INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    status TEXT NOT NULL,
    estimated_week TEXT
);

CREATE TABLE IF NOT EXISTS streak (
    week_start TEXT PRIMARY KEY,
    lessons_delivered INTEGER DEFAULT 0,
    lessons_completed INTEGER DEFAULT 0,
    streak_weeks_completed INTEGER DEFAULT 0
);
""",
}

AGENT_NAME_MAP = {
    "analyst": "business-analyst",
    "coord": "management-coordinator",
    "kiki": "kiki-coach",
    "kiki-prep": "kiki-prep",
    "finance": "finance-controller",
    "sales": "sales-pipeline",
    "engineering": "engineering-roster",
    "research": "research-tracker",
    "people": "people",
}


def migrate_agent(agent_name: str) -> bool:
    """Migrate one agent's state JSON to SQLite. Returns True on success."""
    # agent_name here is the short name (matches JSON filename)
    full_name = AGENT_NAME_MAP.get(agent_name, agent_name)
    json_file = STATE_DIR / f"{agent_name}.json"
    db_file = DB_DIR / f"{agent_name}.db"

    if not json_file.exists():
        print(f"SKIP {agent_name}: no JSON state")
        return False

    # Backup JSON
    backup = json_file.with_suffix(".json.pre-sqlite.bak")
    if not backup.exists():
        import shutil
        shutil.copy(json_file, backup)

    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Read JSON
    try:
        with open(json_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR {full_name}: invalid JSON: {e}")
        return False

    # Create DB
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.executescript(COMMON_SCHEMA)

        agent_schema = AGENT_SCHEMAS.get(full_name)
        if agent_schema:
            cursor.executescript(agent_schema)

        # Idempotency
        last_run = data.get("last_run")
        if last_run:
            cursor.execute(
                "INSERT OR REPLACE INTO idempotency (job_id, last_run, window, status, override_token) VALUES (?, ?, ?, ?, ?)",
                (f"{full_name}_main", last_run, "24h", "migrated", data.get("override_possible") and "yes" or None),
            )

        # Decisions (if list)
        decisions = data.get("decisions", [])
        if isinstance(decisions, list):
            for d in decisions:
                if isinstance(d, str):
                    cursor.execute(
                        "INSERT INTO decisions (ts, decision) VALUES (?, ?)",
                        (last_run or "unknown", d),
                    )

        # Snapshot
        cursor.execute(
            "INSERT INTO state_snapshots (ts, data, source) VALUES (?, ?, ?)",
            (last_run or "unknown", gzip.compress(json.dumps(data).encode()), "migration"),
        )

        # Agent-specific migrations
        if full_name == "business-analyst" and "kpi_snapshot" in data:
            kpi = data["kpi_snapshot"]
            cursor.execute(
                "INSERT INTO kpi_snapshot (date, pipeline_usd, mrr_usd, leads_24h) VALUES (?, ?, ?, ?)",
                (
                    last_run or "unknown",
                    kpi.get("pipeline_usd"),
                    kpi.get("mrr_usd"),
                    kpi.get("leads_24h", 0),
                ),
            )

        if full_name == "business-analyst" and "open_questions" in data:
            for q in data["open_questions"]:
                cursor.execute(
                    "INSERT INTO open_questions (question, created_at) VALUES (?, ?)",
                    (q, last_run or "unknown"),
                )

        if full_name == "management-coordinator" and "open_stuck" in data:
            for item in data["open_stuck"]:
                cursor.execute(
                    "INSERT INTO stuck_items (repo, issue_number, title, owner, since) VALUES (?, ?, ?, ?, ?)",
                    (item.get("repo"), item.get("issue"), item.get("title"), item.get("owner"), item.get("since")),
                )

        if full_name == "management-coordinator" and "stale_repos" in data:
            for repo in data["stale_repos"]:
                cursor.execute(
                    "INSERT INTO stale_repos (repo) VALUES (?)",
                    (repo,),
                )

        if full_name == "sales-pipeline" and "leads_in_flight" in data:
            for lead in data["leads_in_flight"]:
                cursor.execute(
                    "INSERT INTO leads (name, company, icp_match_pct, stage, value_usd, source, created_at, updated_at, next_action, blocker) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        lead.get("name"),
                        lead.get("company"),
                        lead.get("icp_match_pct"),
                        lead.get("stage"),
                        lead.get("value_usd"),
                        lead.get("source"),
                        last_run or "unknown",
                        last_run or "unknown",
                        lead.get("next_action"),
                        lead.get("blocker"),
                    ),
                )

        if full_name == "research-tracker" and "thesis" in data:
            t = data["thesis"]
            cursor.execute(
                "INSERT INTO thesis_chapters (chapter, title, status, last_commit) VALUES (?, ?, ?, ?)",
                (t.get("chapter"), t.get("chapter_title"), "draft", t.get("last_commit")),
            )

        conn.commit()
        conn.close()
        print(f"OK {full_name}: migrated to {db_file}")
        return True
    except Exception as e:
        print(f"ERROR {full_name}: {e}")
        return False


def main():
    if len(sys.argv) > 1:
        agents = sys.argv[1:]
    else:
        agents = list(AGENT_NAME_MAP.keys())

    success = 0
    for a in agents:
        if migrate_agent(a):
            success += 1

    print(f"\n{success}/{len(agents)} agents migrated")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

