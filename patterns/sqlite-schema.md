# SQLite Schema Spec — Per-Agent State DBs

> Canonical SQLite schema for per-agent operational state. Phase 5.5 input.
> **Last updated**: 2026-08-14

---

## Why SQLite (not JSON files)

- **Queryable**: SQL aggregations beat grep + jq
- **Concurrent-safe**: built-in locking vs JSON read/write races
- **Migration path to Postgres**: identical SQL
- **Single-file backup**: `sqlite3 .backup` produces atomic snapshot
- **Schema validation**: built-in CHECK constraints

---

## Per-agent DB location

```
/opt/data/db/<agent-name>.db
```

Examples:
- `/opt/data/db/business-analyst.db`
- `/opt/data/db/management-coordinator.db`
- `/opt/data/db/sales-pipeline.db`
- `/opt/data/db/finance-controller.db`
- `/opt/data/db/research-tracker.db`
- `/opt/data/db/engineering-roster.db`
- `/opt/data/db/kiki-coach.db`
- `/opt/data/db/ai-ops.db`
- `/opt/data/db/compliance.db`
- `/opt/data/db/source-curator.db`
- `/opt/data/db/bandwidth.db`

---

## Common schema (all agents)

```sql
-- Idempotency tracking
CREATE TABLE idempotency (
  job_id TEXT PRIMARY KEY,
  last_run TEXT NOT NULL,        -- ISO 8601 timestamp
  window TEXT NOT NULL,          -- '24h' | '12h' | '7d' | '5min'
  status TEXT NOT NULL,          -- 'success' | 'duplicate' | 'override' | 'failed'
  override_token TEXT
);

-- Decision journal
CREATE TABLE decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,               -- ISO 8601
  decision TEXT NOT NULL,
  rationale TEXT,
  override_token TEXT
);
CREATE INDEX idx_decisions_ts ON decisions(ts DESC);

-- Escalation log
CREATE TABLE escalations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  reason TEXT NOT NULL,
  context_payload TEXT NOT NULL,  -- JSON: 6-field payload
  resolved_by TEXT,
  resolved_at TEXT
);
CREATE INDEX idx_escalations_ts ON escalations(ts DESC);

-- State snapshots (history)
CREATE TABLE state_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  data BLOB NOT NULL,             -- gzipped JSON
  source TEXT                     -- 'cron_run' | 'manual' | 'migration'
);

-- Reflection scores (content agents)
CREATE TABLE reflection_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  draft_hash TEXT NOT NULL,
  score INTEGER NOT NULL,         -- 1-10
  criteria TEXT NOT NULL,         -- JSON: scores per criterion
  refined INTEGER NOT NULL        -- 0 or 1
);

-- Cost ledger
CREATE TABLE cost_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  model TEXT NOT NULL,
  tokens_in INTEGER,
  tokens_out INTEGER,
  cost_usd REAL NOT NULL,
  task TEXT
);
CREATE INDEX idx_cost_log_ts ON cost_log(ts DESC);
```

---

## Agent-specific schemas

### sales-pipeline

```sql
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  company TEXT,
  icp_match_pct REAL,
  stage TEXT NOT NULL,           -- 'new' | 'qualified' | 'proposal' | 'signed' | 'lost'
  value_usd REAL,
  source TEXT,                   -- 'rubicon_worker' | 'linkedin' | 'referral' | 'manual'
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  next_action TEXT,
  blocker TEXT
);
CREATE INDEX idx_leads_stage ON leads(stage);
CREATE INDEX idx_leads_updated ON leads(updated_at DESC);

CREATE TABLE outreach_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id INTEGER NOT NULL REFERENCES leads(id),
  channel TEXT NOT NULL,         -- 'email' | 'linkedin' | 'whatsapp'
  message TEXT,
  sent_at TEXT NOT NULL,
  response TEXT,
  outcome TEXT                   -- 'reply' | 'bounce' | 'unsubscribe' | 'no_response'
);

CREATE TABLE funnel_30d (
  date TEXT PRIMARY KEY,
  leads INTEGER DEFAULT 0,
  qualified INTEGER DEFAULT 0,
  proposals INTEGER DEFAULT 0,
  signed INTEGER DEFAULT 0,
  lost INTEGER DEFAULT 0,
  pipeline_value_usd REAL DEFAULT 0
);
```

### finance-controller

```sql
CREATE TABLE deals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client TEXT NOT NULL,
  value_usd REAL NOT NULL,
  stage TEXT NOT NULL,           -- 'outreach' | 'proposal' | 'negotiating' | 'signed' | 'closed_lost'
  expected_close TEXT,
  signed_at TEXT,
  notes TEXT
);

CREATE TABLE invoices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  deal_id INTEGER REFERENCES deals(id),
  amount_usd REAL NOT NULL,
  issued_at TEXT NOT NULL,
  paid_at TEXT,
  due_at TEXT NOT NULL,
  status TEXT NOT NULL           -- 'draft' | 'sent' | 'paid' | 'overdue' | 'void'
);

CREATE TABLE compliance_flags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  flag_type TEXT NOT NULL,       -- 'trademark' | 'gdpr' | 'eu_ai_act' | 'tax'
  severity TEXT NOT NULL,        -- 'low' | 'medium' | 'high' | 'critical'
  description TEXT,
  resolved_at TEXT,
  resolution TEXT
);
```

### engineering-roster

```sql
CREATE TABLE deploys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  site TEXT NOT NULL,
  deployed_at TEXT NOT NULL,
  deployed_by TEXT,
  status TEXT NOT NULL,          -- 'success' | 'rolled_back' | 'failed'
  rollback_at TEXT
);

CREATE TABLE incidents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  site TEXT,
  severity TEXT,                 -- 'sev1' | 'sev2' | 'sev3'
  description TEXT,
  resolved_at TEXT,
  root_cause TEXT
);

CREATE TABLE prs_review_queue (
  pr_id INTEGER PRIMARY KEY,
  repo TEXT NOT NULL,
  number INTEGER NOT NULL,
  title TEXT,
  author TEXT,
  created_at TEXT NOT NULL,
  age_days INTEGER
);
```

### research-tracker

```sql
CREATE TABLE thesis_chapters (
  chapter INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,          -- 'draft' | 'review' | 'submitted' | 'published'
  last_commit TEXT,
  word_count INTEGER,
  target_words INTEGER
);

CREATE TABLE publications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  venue TEXT NOT NULL,           -- 'arxiv' | 'journal' | 'conference'
  title TEXT,
  status TEXT NOT NULL,          -- 'planned' | 'drafting' | 'submitted' | 'accepted' | 'rejected'
  deadline TEXT,
  submitted_at TEXT,
  decision_at TEXT
);

CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  status TEXT NOT NULL,          -- 'concept' | 'in_production' | 'live' | 'archived'
  modules_total INTEGER,
  modules_done INTEGER DEFAULT 0
);
```

### kiki-coach

```sql
CREATE TABLE lessons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  topic TEXT NOT NULL,
  file_path TEXT NOT NULL,
  delivered_at TEXT,
  completed_at TEXT,             -- null = not done
  feedback TEXT
);

CREATE TABLE curriculum (
  position INTEGER PRIMARY KEY,
  topic TEXT NOT NULL,
  status TEXT NOT NULL,          -- 'pending' | 'in_progress' | 'done' | 'skipped'
  estimated_week TEXT
);

CREATE TABLE streak (
  week_start TEXT PRIMARY KEY,
  lessons_delivered INTEGER DEFAULT 0,
  lessons_completed INTEGER DEFAULT 0,
  streak_weeks_completed INTEGER DEFAULT 0
);
```

---

## Migration script (JSON → SQLite)

```python
#!/usr/bin/env python3
"""migrate_json_to_sqlite.py — One-time migration from JSON state files to SQLite.

Usage: python3 migrate_json_to_sqlite.py <agent-name>
"""
import json
import sqlite3
import sys
import gzip
from pathlib import Path

STATE_DIR = Path("/opt/data/agents/state")
DB_DIR = Path("/opt/data/db")

def migrate_agent(agent_name: str):
    json_file = STATE_DIR / f"{agent_name}.json"
    db_file = DB_DIR / f"{agent_name}.db"

    if not json_file.exists():
        print(f"No JSON state for {agent_name}, skipping")
        return

    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()

    # Run common schema
    cursor.executescript(COMMON_SCHEMA)

    # Run agent-specific schema
    agent_schema = AGENT_SCHEMAS.get(agent_name)
    if agent_schema:
        cursor.executescript(agent_schema)

    # Read JSON
    with open(json_file) as f:
        data = json.load(f)

    # Migrate idempotency state
    if "last_run" in data:
        cursor.execute(
            "INSERT INTO idempotency (job_id, last_run, window, status) VALUES (?, ?, ?, ?)",
            (f"{agent_name}_main", data["last_run"], "24h", "migrated"),
        )

    # Migrate agent-specific fields
    if agent_name == "sales" and "leads_in_flight" in data:
        for lead in data["leads_in_flight"]:
            cursor.execute(
                "INSERT INTO leads (name, icp_match_pct, stage, value_usd, source, created_at, updated_at, next_action) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    lead.get("name"),
                    lead.get("icp_match_pct"),
                    lead.get("stage"),
                    lead.get("value_usd"),
                    lead.get("source"),
                    lead.get("created_at", data.get("last_run")),
                    data.get("last_run"),
                    lead.get("next_action"),
                ),
            )

    # Save initial state snapshot
    cursor.execute(
        "INSERT INTO state_snapshots (ts, data, source) VALUES (?, ?, ?)",
        (data.get("last_run"), gzip.compress(json.dumps(data).encode()), "migration"),
    )

    conn.commit()
    conn.close()
    print(f"Migrated {agent_name}: {json_file} -> {db_file}")

# Schemas here (truncated for brevity — see full files)
COMMON_SCHEMA = """
... (from above)
"""

AGENT_SCHEMAS = {
    "sales": "... (from above)",
    "finance": "...",
    # etc.
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: migrate_json_to_sqlite.py <agent-name> [<agent-name> ...]")
        sys.exit(1)
    for agent in sys.argv[1:]:
        migrate_agent(agent)
```

---

## Backup automation

```bash
#!/usr/bin/env bash
# /opt/data/agents/scripts/db-snapshot.sh — Daily SQLite backup

set -euo pipefail

DB_DIR="/opt/data/db"
BACKUP_DIR="/opt/data/backups/db/$(date -u +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

for db in "$DB_DIR"/*.db; do
    name=$(basename "$db" .db)
    sqlite3 "$db" ".backup '$BACKUP_DIR/$name.db'"
    gzip "$BACKUP_DIR/$name.db"
done

# Cleanup: retain 90 days
find /opt/data/backups/db -type d -mtime +90 -exec rm -rf {} + 2>/dev/null || true

echo "Backed up $(ls "$DB_DIR"/*.db | wc -l) databases to $BACKUP_DIR"
```

Register as cron: `0 2 * * *` PYT (daily at 2am).

---

## Verifier

`/opt/data/agents/scripts/validate-state.py` runs every 15 min:

```python
#!/usr/bin/env python3
"""Validate all agent SQLite DBs against schema."""
import sqlite3
import sys
from pathlib import Path

DB_DIR = Path("/opt/data/db")
errors = []

for db_file in DB_DIR.glob("*.db"):
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        # Integrity check
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result[0] != "ok":
            errors.append(f"{db_file.name}: integrity_check = {result[0]}")

        # Check common tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        required = {"idempotency", "decisions", "escalations", "state_snapshots", "cost_log"}
        missing = required - tables
        if missing:
            errors.append(f"{db_file.name}: missing tables {missing}")

        conn.close()
    except Exception as e:
        errors.append(f"{db_file.name}: {e}")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"✅ All {len(list(DB_DIR.glob('*.db')))} databases valid")
```

---

**Document path**: `/opt/data/agents-v2/patterns/sqlite-schema.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
