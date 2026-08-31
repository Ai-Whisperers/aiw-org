# PHASE-0-COMPLETE.md

> Handoff doc for next session. Phase 0 finished, Phase 1 ready to start.
> **Last updated**: 2026-08-14

---

## Phase 0 — DONE ✅

**Goal**: Decisions ratified, backups taken, directory tree created.

### Tasks completed

| # | Task | Status | Verification |
|---|------|--------|--------------|
| 0.1 | Read existing ORG-AGENTS, ORCHESTRATION, state files | ✅ | 11 files read |
| 0.2 | Write `DECISIONS-2026-Q3.md` with D1-D8 + Q1-Q5 + v5 NEW + OP-1 to OP-10 | ✅ | File exists (10 KB) |
| 0.3 | Backup ORG-AGENTS.md, ORCHESTRATION.md, jobs.json, 8 state files | ✅ | 11 backups at `/opt/data/agents-v2/backups/2026-08-14-pre-v0.2.0/` |
| 0.4 | Create 9 subdirs under `/opt/data/agents-v2/` | ✅ | patterns, specs, playbooks, prompts, backups, repos, db, scripts, outbox |
| 0.5 | Test `trademark-scrub.sh` | ✅ | Returns 0 violations on new artifacts; 8 known false positives on existing dept specs |
| 0.6 | Write `PHASE-0-COMPLETE.md` (this file) | ✅ | File exists |

### Backups taken (with hashes)

```
6a641e1a37d9b7529c18905184ac3627  ORG-AGENTS.md
4ad78c3e1d4449dec40fa1540191487a  ORCHESTRATION.md
fef2883a43f45d9fdd3c1b3c304636b3  jobs.json
5158bd49f33a558446aed9b85d17c607  state/analyst.json
a27536e9d30910affe56e1c91502056f  state/coord.json
56c48e849113f0aa6b652820a33dab4c  state/kiki.json
c8592f2b0fcd35dbc963860d56dadfdc  state/finance.json
f354bee35dab109252ff90c3ac8a0b01  state/sales.json
464430ee3bee7bd0c255d83785112d91  state/engineering.json
e0e022e01e955234a4043a75339cea46  state/research.json
866602e77aaa7bb2d7a2d00dc426a832  state/people.json
228dc0ba3d4b9cffd5c87ccf13333def  state/kiki-prep.json
```

Backup location: `/opt/data/agents-v2/backups/2026-08-14-pre-v0.2.0/`

### Files in `/opt/data/agents-v2/` (15 total)

```
DECISIONS-2026-Q3.md         (10 KB)   decisions
INDEX.md                     ( 6 KB)   master navigation
PLAN-v4.md                   (52 KB)   superseded by v5
PLAN-v5.md                   (32 KB)   CURRENT plan
PHASE-0-COMPLETE.md          (this)    handoff doc
RESEARCH-COMPLETE-ORG.md     (24 KB)   30 functional areas research
ROLES-INVENTORY.md           (16 KB)   ~135 roles
STORAGE-ARCHITECTURE.md      (12 KB)   3-layer model
STATE-AUDIT-2026-08-14.md    ( 8 KB)   existing state inventory
FAILURE-MODES.md             (12 KB)   15 failure modes
THREAT-MODEL.md              ( 8 KB)   7 threats
ROLLBACK-PLAYBOOK.md         ( 8 KB)   per-phase rollback

patterns/
  hard-stops-schema.md       ( 8 KB)
  idempotency.md             ( 8 KB)
  sqlite-schema.md           (12 KB)
  trademark-scrub.sh         ( 6 KB)   executable

prompts/
  PROMPT-TEMPLATE.md         ( 8 KB)   12-section master template
```

### Directories created

```
/opt/data/agents-v2/
├── backups/    (existing 2026-08-14-pre-v0.2.0/)
├── db/         (empty, for Phase 5.5 SQLite)
├── outbox/     (empty, for future agent outboxes)
├── patterns/   (4 files)
├── playbooks/  (empty, for Phase 6)
├── prompts/    (1 file)
├── repos/      (empty, for Phase 5.5 git repos)
├── scripts/    (empty, for Phase 2 infra scripts)
└── specs/      (empty, for new dept specs)
```

### Decisions ratified

**16 decisions** documented in `/opt/data/agents/DECISIONS-2026-Q3.md`:
- D1: Cost cap ($1/agent/day, $10 total)
- D2: Sales inbound-first
- D3: Compliance Officer named role + EU client hard-stop
- D4: /opt/data/agents-v2/ as new sibling dir
- D5: Backup policy (gitignored state + 6h snapshot)
- D6: Idempotency = state.last_run + window
- D7: Hard stops = PROMPT.md prose + runtime wrapper
- D8: Template AFTER first reference agent
- Q1-Q5: location, sub-agent trigger, eval-gate, source ownership, eval timing
- V5 NEW: storage architecture, 30 functional areas, ~135 roles, ~50 agents, build order
- OP-1 to OP-10: token budget, soak length, verifier model, milestone, etc.

### Trademark scrub status

- **21 files checked**
- **0 violations in new artifacts** (PLAN-v5, ROLES-INVENTORY, etc.)
- **8 false positives in existing dept specs** (all are the banlist itself, "objetivo-department" as prefix, "RAG" acronym)

These false positives in existing files are known and expected. They pre-date Phase 0 and don't block.

### What was NOT done in Phase 0

- No changes to existing ORG-AGENTS.md (still v0.1.0)
- No cron jobs fixed (still 1 error, 6 pending) — that's Phase 1
- No infra scripts written (snapshot, validate, heartbeat) — that's Phase 2
- No agent PROMPT.md rewritten — that's Phase 4+
- No SQLite DBs created — that's Phase 5.5
- No git repos created — that's Phase 5.5

---

## Phase 1 — READY TO START

**Goal**: Fix 1 P0 cron error + unify storage path.

### Tasks queued

1. Edit `/opt/data/.hermes/cron/jobs.json`:
   - Delete `provider_snapshot` + `model_snapshot` from `thesis-daily-tick` entry
2. Verify with `hermes cron list | grep thesis-daily-tick` shows `state: scheduled`
3. Manual run `hermes cron run thesis-daily-tick` to confirm
4. Check if `/opt/data/cron/jobs.json` exists; if so, diff vs canonical
5. If different, symlink secondary to canonical
6. Write `PHASE-1-COMPLETE.md`

### Expected effort

8-13 turns, 1-2 sessions.

### Files to touch

- `/opt/data/.hermes/cron/jobs.json` (read, edit, verify)

### Rollback if needed

See `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md` → Phase 1.

---

## What next session should read first

1. This file (`PHASE-0-COMPLETE.md`)
2. `/opt/data/agents/DECISIONS-2026-Q3.md` (what's ratified)
3. `/opt/data/agents-v2/STATE-AUDIT-2026-08-14.md` (what's built)
4. `/opt/data/agents-v2/PLAN-v5.md` Phase 1 (what to do next)

---

**Document path**: `/opt/data/agents-v2/PHASE-0-COMPLETE.md`
**Status**: Phase 0 COMPLETE
**Next phase**: Phase 1 (P0 cron fixes)
**Last updated**: 2026-08-14
