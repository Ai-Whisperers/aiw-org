# Rollback Playbook — Per-Phase

> How to revert each phase if it breaks. Phase 1+ output.
> **Last updated**: 2026-08-14

---

## Reading guide

Each phase has:
- **What can break**: the failure modes for that phase
- **Pre-change snapshot**: what to back up before starting
- **Rollback procedure**: step-by-step revert
- **Verification**: how to confirm rollback succeeded

---

# Phase 0 rollback

**What can break**:
- Backups taken incorrectly
- Decisions doc missing D1-D8

**Pre-change snapshot**: `/opt/data/agents-v2/backups/` (already in plan)

**Rollback**:
1. Delete `/opt/data/agents-v2/` dirs (except backups)
2. Restore any artifact from `/opt/data/agents-v2/backups/` if needed
3. Phase 0 is non-destructive by design (no changes to existing files)

**Verification**: `ls /opt/data/agents/departments/ORG-AGENTS.md` (still v0.1.0)

---

# Phase 1 rollback (cron fixes)

**What can break**:
- jobs.json syntax error after edit
- Cron jobs still in error state after fix
- Storage path split not unified

**Pre-change snapshot**:
- Backup `jobs.json` to `/opt/data/agents-v2/backups/jobs-v0.1.0.json`
- Backup `/opt/data/cron/jobs.json` if exists

**Rollback**:
```bash
# Restore jobs.json
cp /opt/data/agents-v2/backups/jobs-v0.1.0.json /opt/data/.hermes/cron/jobs.json

# If symlink created, restore both files
if [[ -L /opt/data/cron/jobs.json ]]; then
    unlink /opt/data/cron/jobs.json
fi

# Restart gateway if needed
hermes gateway restart  # or equivalent
```

**Verification**: `hermes cron list | grep -E 'morning-brief|thesis-daily-tick|aiw-dashboard-refresh'` returns to original state.

---

# Phase 2 rollback (infra scripts)

**What can break**:
- Snapshot script corrupts state files (atomic write bug)
- Validate script false-positives block all agents
- Heartbeat floods chat with alerts

**Pre-change snapshot**:
- Backup 8 state files (already in plan)
- Save current `jobs.json` (already in Phase 1)

**Rollback**:
```bash
# Stop the cron jobs
hermes cron remove aiw-state-snapshot-6h
hermes cron remove aiw-state-validate-15m
hermes cron remove aiw-cron-heartbeat-onhours
hermes cron remove aiw-cron-heartbeat-offhours

# Restore state files from snapshot (if corrupted)
cp -r /opt/data/agents/state/snapshots/{most-recent-date}/{hour}/* /opt/data/agents/state/

# Restore heartbeat alerts table (if corrupted)
rm /opt/data/agents/state/heartbeat-alerts.json
```

**Verification**: `bash health.sh` returns all green; no alerts in chat.

---

# Phase 3 rollback (patterns)

**What can break**:
- Hard-stop wrapper blocks legitimate actions
- Idempotency check too aggressive (skips real work)
- Trademark scrub has false positives

**Pre-change snapshot**:
- Backup existing PROMPT.md files (already done in Phase 0)

**Rollback**:
- Patterns are additive: deleting the pattern files doesn't break anything
- If hard-stop wrapper is integrated with cron jobs, rollback by removing the wrapper integration

**Verification**: existing agents still deliver normally.

---

# Phase 4 rollback (reference agent)

**What can break**:
- New business-analyst PROMPT.md is broken
- Hard stops block writes
- Context-payload breaks outbox

**Pre-change snapshot**:
- Backup current `business-analyst/PROMPT.md` to `PROMPT.md.v0.1.0`

**Rollback**:
```bash
# Restore reference agent to v0.1.0
cp /opt/data/agents/business-analyst/PROMPT.md.v0.1.0 \
   /opt/data/agents/business-analyst/PROMPT.md

# Restore state if corrupted
cp /opt/data/agents-v2/backups/state/analyst.json \
   /opt/data/agents/state/analyst.json
```

**Verification**: Manual run `hermes cron run aiw-business-analyst-daily` succeeds, outbox delivered.

---

# Phase 5 rollback (6 lead agents)

**What can break**:
- One or more agents don't deliver
- Cron collisions
- Grid.sh shows overlaps

**Pre-change snapshot**:
- Per agent: backup `PROMPT.md` to `PROMPT.md.v0.1.0`
- Backup `jobs.json` (Phase 1)
- Backup `grid.sh` output (text file)

**Rollback** (per agent):
```bash
# Restore one agent's PROMPT.md
cp /opt/data/agents/<agent>/PROMPT.md.v0.1.0 \
   /opt/data/agents/<agent>/PROMPT.md

# Remove the agent's cron job
hermes cron remove <agent-cron-id>

# Restore state
cp /opt/data/agents-v2/backups/state/<dept>.json \
   /opt/data/agents/state/<dept>.json
```

**Verification**: All 6 cron jobs in original state; no new jobs added; existing agents deliver.

---

# Phase 5.5 rollback (storage migration)

**What can break**:
- Git push fails (auth, network)
- SQLite migration corrupts data
- Backup automation fails

**Pre-change snapshot**:
- JSON state files are the source of truth (no migration yet)
- Backup jobs.json (Phase 1)

**Rollback**:
- Phase 5.5 is additive: doesn't touch existing JSON state
- If SQLite DBs are corrupt, delete them; JSON state still works
- If git repos are corrupt, delete `/opt/data/git-repos/`, recreate

**Verification**: All 8 state JSON files still exist and parse; agents still deliver.

---

# Phase 6 rollback (playbook catalog)

**What can break**:
- Tool URL invalid
- Trademark violation missed
- Role count mismatch

**Pre-change snapshot**:
- Backup session 1's roles-glossary.md (already exists)

**Rollback**:
- Playbooks are new files (not modifying existing)
- Delete playbook files, restore to pre-Phase-6 state

**Verification**: `roles-glossary.md` and existing dept specs unchanged.

---

# Phase 7 rollback (procurement)

**What can break**:
- Cost roll-up wrong
- cost-cap.sh too tight (halts agents mid-run)
- Procurement decisions never implemented

**Pre-change snapshot**:
- Backup `state/finance.json`
- Backup current tool list

**Rollback**:
- cost-cap.sh not yet running? Just don't run it
- cost-cap.sh running and blocking? Manually trigger override
- Procurement decisions: don't execute them

**Verification**: No new SaaS subscriptions active; cost-cap not blocking.

---

# Phase 8 rollback (constitution bump)

**What can break**:
- ORG-AGENTS.md v0.2.0 breaks agent prompts
- Dept specs v0.2.0 have wrong cross-references

**Pre-change snapshot**:
- v0.1.0 already backed up to `/opt/data/agents/departments/archive/ORG-AGENTS-v0.1.0-2026-08-13.md`
- Backup each dept spec to `01-operations.md.v0.1.0` etc.

**Rollback**:
```bash
# Restore ORG-AGENTS.md
cp /opt/data/agents/departments/archive/ORG-AGENTS-v0.1.0-2026-08-13.md \
   /opt/data/agents/departments/ORG-AGENTS.md

# Restore each dept spec
for spec in /opt/data/agents/departments/0N-*.md.v0.1.0; do
    base=$(basename "$spec" .v0.1.0)
    cp "$spec" "/opt/data/agents/departments/$base"
done
```

**Verification**: `grep "version: 0.1.0" /opt/data/agents/departments/*.md` returns matches.

---

# Phase 9 rollback (operational disciplines)

**What can break**:
- Model fallbacks cause agent behavior change
- Chaos tests break prod state
- Self-running milestone never achieved

**Pre-change snapshot**:
- Per-agent PROMPT.md (already at v0.2.0)
- jobs.json

**Rollback**:
- Remove fallback model field from PROMPT.md (back to primary only)
- Disable chaos tests (delete cron job)
- Re-run with current state (no rollback needed)

**Verification**: All cron jobs green; agents deliver normally.

---

# General rollback principles

1. **Backups before changes**: every phase takes backups first
2. **Additive changes preferred**: new files over modifying existing
3. **Test before promotion**: dry-run before pushing
4. **Canary cron jobs**: add new jobs in shadow mode first
5. **Document rollback steps**: per phase, in this playbook

---

**Document path**: `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
