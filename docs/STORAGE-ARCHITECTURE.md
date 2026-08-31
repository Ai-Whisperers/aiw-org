# Storage Architecture — Implementation Spec

> 3-layer model: per-agent git repos + per-agent SQLite DBs + Qdrant (Tier 2).
> **Last updated**: 2026-08-14

---

## Reading guide

- **Layer 1**: Git repos (permanent, version-controlled memory)
- **Layer 2**: SQLite (operational state, queries, snapshots)
- **Layer 3**: Qdrant (semantic memory, RAG, deferred to Tier 2)

---

# Layer 1: Git repos (per agent, per dept)

## Directory structure

```
/opt/data/git-repos/
├── aiw-agents-business-analyst/
├── aiw-agents-management-coordinator/
├── aiw-agents-kiki-coach/
├── aiw-agents-finance-controller/
├── aiw-agents-sales-pipeline/
├── aiw-agents-engineering-roster/
├── aiw-agents-research-tracker/
├── aiw-agents-ai-ops-coordinator/
├── aiw-agents-compliance-monitor/
├── aiw-agents-source-curator/
├── aiw-agents-founder-bandwidth-watchdog/
├── aiw-agents-marketing-content-producer/
├── aiw-agents-procurement-tracker/
├── aiw-dept-operations/
├── aiw-dept-finance-legal/
├── aiw-dept-sales-growth/
├── aiw-dept-engineering-delivery/
├── aiw-dept-research-education/
├── aiw-dept-people-culture/
├── aiw-constitution/
├── aiw-patterns/
├── aiw-playbooks/
├── aiw-source-materials/
└── aiw-shared/
```

## Per-agent repo layout (template)

```
aiw-agents-<name>/
├── .gitignore              # excludes state/, db/, .env
├── README.md               # agent overview, owner, schedule
├── CHANGELOG.md            # version history
├── PROMPT.md               # canonical agent spec (committed)
├── outbox/
│   └── YYYY-MM-DD.md       # daily briefs (committed)
├── logs/
│   └── YYYY-MM-DD.jsonl    # agent action logs (committed, 90-day retention)
├── memories/
│   └── <topic>.md          # long-term agent memory (committed)
├── decisions/
│   └── YYYY-MM-DD.md       # decision journal (committed)
├── lessons/
│   └── <topic>.md          # post-hoc reflections (committed)
├── eval/
│   └── golden-trajectories.json  # eval-gate ground truth (committed)
└── state/                  # .gitignored
    └── current.json        # active state (ephemeral)
```

## .gitignore (per agent)

```gitignore
# Sensitive state - not committed
state/
*.env
.env
.env.local

# Database files
*.db
*.db-journal
*.db-wal
*.db-shm

# Logs older than 90 days (rotated by cron)
logs/older-than-90d/

# Cache
__pycache__/
*.pyc
*.pyo
.pytest_cache/
```

## Setup script

```bash
#!/usr/bin/env bash
# /opt/data/agents-v2/scripts/setup-agent-repo.sh <agent-name>

set -euo pipefail

AGENT=$1
REPO_DIR="/opt/data/git-repos/aiw-agents-$AGENT"
GITHUB_ORG="Ai-Whisperers"

mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

# Initialize
git init
git checkout -b main 2>/dev/null || git checkout main

# Create directory structure
mkdir -p outbox logs memories decisions lessons eval state

# Copy templates
cp /opt/data/agents-v2/templates/README.md.template README.md
cp /opt/data/agents-v2/templates/CHANGELOG.md.template CHANGELOG.md
cp /opt/data/agents-v2/templates/.gitignore.template .gitignore

# Render README from template (with agent name)
sed -i "s/{{AGENT_NAME}}/$AGENT/g" README.md

# Initial commit
git add .
git commit -m "init: scaffold for $AGENT"

# Add GitHub remote (if not exists)
REMOTE_URL="git@github.com:$GITHUB_ORG/aiw-agents-$AGENT.git"
git remote add origin "$REMOTE_URL" 2>/dev/null || true

# Push to GitHub
git push -u origin main 2>&1 || echo "Push failed - manual setup needed"

echo "✅ Repo created: $REPO_DIR"
echo "   Remote: $REMOTE_URL"
```

## Push automation (per agent, daily)

```bash
#!/usr/bin/env bash
# /opt/data/agents/scripts/git-push-daily.sh
# Cron: 0 3 * * * PYT (3 AM daily)

set -euo pipefail

REPOS_DIR="/opt/data/git-repos"

for repo in "$REPOS_DIR"/aiw-agents-*; do
    cd "$repo"

    # Add any new outbox/logs/decisions files
    git add outbox/ logs/ memories/ decisions/ lessons/ eval/ 2>/dev/null || true

    # Check if there are changes
    if [[ -n "$(git status --porcelain)" ]]; then
        git commit -m "auto: daily snapshot $(date -u +%Y-%m-%d)"
        git push origin main 2>&1 || echo "Push failed for $repo"
    fi
done
```

Register as cron: `aiw-git-push-daily` at `0 3 * * *` PYT.

---

# Layer 2: SQLite (per-agent operational state)

See `/opt/data/agents-v2/patterns/sqlite-schema.md` for full schema spec.

## Summary

- 11 SQLite DBs at `/opt/data/db/<agent>.db`
- Common schema: idempotency, decisions, escalations, state_snapshots, cost_log
- Agent-specific: leads, deals, deploys, thesis_chapters, lessons, etc.

## Backup script

See `/opt/data/agents-v2/scripts/db-snapshot.sh` (Phase 5.5C creates this):

```bash
#!/usr/bin/env bash
# Daily SQLite backup
set -euo pipefail
DB_DIR="/opt/data/db"
BACKUP_DIR="/opt/data/backups/db/$(date -u +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"
for db in "$DB_DIR"/*.db; do
    name=$(basename "$db" .db)
    sqlite3 "$db" ".backup '$BACKUP_DIR/$name.db'"
    gzip "$BACKUP_DIR/$name.db"
done
find /opt/data/backups/db -type d -mtime +90 -exec rm -rf {} + 2>/dev/null || true
```

Cron: `aiw-db-snapshot-daily` at `0 2 * * *` PYT.

## Offsite backup (R2)

Weekly offsite to Cloudflare R2:

```bash
#!/usr/bin/env bash
# /opt/data/agents/scripts/db-offsite-weekly.sh
# Cron: 0 4 * * 0 PYT (Sundays 4 AM)

set -euo pipefail
WEEK=$(date -u +%Y-W%V)
BACKUP_DIR="/opt/data/backups/db"

# Compress all daily backups from past week
TARBALL="/tmp/db-backup-$WEEK.tar.gz"
tar -czf "$TARBALL" -C "$BACKUP_DIR" $(ls -t "$BACKUP_DIR" | head -7)

# Upload to R2 (assumes rclone configured)
rclone copy "$TARBALL" r2:aiw-backups/db/

rm "$TARBALL"
```

---

# Layer 3: Qdrant (Tier 2 deferred)

## When to ship

- source-materials > 50 files, OR
- First eval-gate ships (golden trajectories need semantic search), OR
- Cross-agent memory queries become common (agent X asks "how did agent Y handle Z?")

## Spec

- Qdrant Cloud or self-hosted at `qdrant.paragu-ai.com`
- One collection per agent: `agent_<name>_memory`
- Vectors: 1536-dim (Proveedor de IA ada-002 compatible) or via local embed model
- Distance: cosine

## Collections

| Collection | Source |
|------------|--------|
| `agent_business_analyst_memory` | All outbox + decisions + lessons |
| `agent_sales_pipeline_memory` | All outbox + decisions + lessons |
| ... (per agent) | ... |
| `source_materials` | All `/opt/data/source-materials/**` |
| `playbooks` | All `/opt/data/agents-v2/playbooks/**` |

## Memory write pattern

After every agent run:
1. Take the outbox content
2. Embed via local model
3. Upsert to `agent_<name>_memory` collection
4. Metadata: agent, date, topic, references

## Memory query pattern

Before agent runs:
1. Take today's input context
2. Embed query
3. Search `agent_<name>_memory` for top-5 matches
4. Include in agent prompt as "prior context"

---

# Memory taxonomy

| Memory type | Backend | Example |
|------------|---------|---------|
| **Episodic** (what happened) | Git `outbox/`, `logs/`, `decisions/` | "Yesterday I drafted 3 outreach emails" |
| **Semantic** (what I know) | SQLite + Qdrant | "ICP match for legal vertical is 70%" |
| **Procedural** (how I do things) | Git `PROMPT.md` + `patterns/` | "Always check idempotency before action" |

This is the standard AI agent memory taxonomy (per Mem0, Zep, Hindsight 2026).

---

# Backup strategy summary

| Layer | Backup | Frequency | Retention | Offsite |
|-------|--------|-----------|-----------|---------|
| Git repos | GitHub `Ai-Whisperers/` | Per commit (auto) | Permanent | GitHub |
| SQLite DBs | Local snapshot | Daily | 90 days | Weekly R2 |
| Qdrant (T2) | Local snapshot | Weekly | 90 days | Weekly R2 |
| State JSON (legacy) | Local snapshot | 6 hours | 30 days | None |

---

# Cost estimate

| Component | Cost (USD/mo) |
|-----------|---------------|
| GitHub private repos (~25) | $0 (free tier) or $4/user/mo for team |
| R2 storage (10 GB snapshots) | $0.15 (10 GB × $0.015/GB) |
| R2 egress (weekly restore) | $0 (free tier 10 GB/mo) |
| Qdrant Cloud (T2) | $25 (1 GB vector, when shipped) |
| **Total** | **~$5-30/mo** |

---

# Migration strategy (Phase 5.5)

## From current state (JSON files)

```
/opt/data/agents/state/*.json  →  /opt/data/db/*.db + /opt/data/git-repos/aiw-agents-*/
```

## Migration steps

1. **Phase 5.5A** — Build git repo structure (17 repos)
2. **Phase 5.5B** — Migrate state JSON to SQLite (one-time script)
3. **Phase 5.5C** — Set up backup automation
4. **Phase 5.5D** — Validate (JSON == SQLite, all agents still deliver)
5. **Phase 5.5E** — Decommission JSON (after 30-day shadow period)

## Coexistence period

During Phase 5.5, both systems run. JSON files are read-only mirror. SQLite is source of truth. After 30 days, JSON files archived.

---

**Document path**: `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
