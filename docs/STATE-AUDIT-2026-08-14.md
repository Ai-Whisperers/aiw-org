# Existing State Audit — 2026-08-14

> Inventory of what's already built. Phase 0 input.
> **Last updated**: 2026-08-14

---

## 3 Lead agents already wired (PROMPT.md exists)

### business-analyst (v0.1.0, 100 lines)

**Schedule**: `0 10:30 * * *` (06:30 PYT daily)
**Status**: cron job `aiw-business-analyst-daily` registered, last_status `ok`
**PROMPT.md sections**: 8 (Role, Hard constraints, What you read, Output structure, State updates, Tone, Failure mode, CHANGELOG)

**What's there**:
- 4-section output structure (Pipeline / Revenue direction / Site & infra health / Today)
- Hard constraints (length, no emojis, source citations)
- Reads: state/analyst.json, logs/site-health.log, GH API, cron list, live apex checks

**What's MISSING (per v5 spec)**:
- Hard Stops table (D7)
- Idempotency Contract (D6)
- Context-Packaging Escalation (6-field payload)
- Fallback Model field
- 12-section structure (currently 8)
- Git repo backing (D5)
- SQLite DB (v5-1)

**Action needed**: Upgrade to v0.2.0 in Phase 4. Add 4 missing sections. Adopt PROMPT-TEMPLATE.md.

---

### management-coordinator (v0.1.0, 91 lines)

**Schedule**: `0 21 * * 1,4` (Mon+Thu 17:00 PYT)
**Status**: cron job `aiw-management-coord-biwk` registered, last_status `pending` (never run)
**PROMPT.md sections**: 7

**What's there**:
- 5-section output (Stuck / Stale repos / PR queue / Thesis / Decisions)
- Reads: GH issues, PRs, push activity, state/coord.json, thesis tick, agent-tasks

**What's MISSING**: Same as business-analyst — 4 missing sections, no git repo, no SQLite.

**Action needed**: Upgrade in Phase 5.

---

### kiki-coach (v0.1.0, 99 lines)

**Schedule**: `0 21 * * 5` (Fri 17:00 PYT)
**Status**: cron job `aiw-kiki-coach-weekly` registered, last_status `pending`
**PROMPT.md sections**: 8 (with KIKI-CHARTER.md reference)

**What's there**:
- 5-section lesson structure (Concept / Worked example / Exercise / Stretch / Sources)
- 8-week curriculum (code topics)
- Bilingual Spanish/English
- Charter for in-scope domains

**What's MISSING**: Same as others + reflection loop should be more explicit.

**Action needed**: Upgrade in Phase 5.

---

## 19 Cron jobs (current state)

| # | Name | Schedule | Status | Notes |
|---|------|----------|--------|-------|
| 1 | site-health | every 15 min | ok | HTTP checks |
| 2 | repo-ci-monitor | `0 11 * * *` | ok | Daily 11:00 UTC |
| 3 | rbl-check | `0 12 * * *` | ok | Daily 12:00 UTC |
| 4 | morning-brief | `0 10 * * *` | **ok** | Was error (model drift), fixed |
| 5 | ometzdental-weekly-refresh | `0 6 * * 1` | ok | Mon 06:00 UTC |
| 6 | thesis-daily-tick | `0 6 * * *` | **ERROR** | Model drift, needs fix |
| 7 | thesis-weekly-review | `0 18 * * 0` | pending | Never run |
| 8 | thesis-git-maintenance | `0 23 * * 0` | pending | Never run |
| 9 | thesis-watchdog | every 15 min | ok | Healthcheck |
| 10 | evo-poll-watchdog | every 5 min | ok | Hermes bridge |
| 11 | aiw-business-analyst-daily | `30 10 * * *` | ok | Daily 06:30 PYT |
| 12 | aiw-management-coord-biwk | `0 21 * * 1,4` | pending | Never run |
| 13 | aiw-kiki-coach-weekly | `0 21 * * 5` | pending | Never run |
| 14 | aiw-sales-pipeline-daily | `0 13,16 * * *` | pending | Never run |
| 15 | aiw-finance-controller-weekly | `0 21 * * 5` | pending | Never run |
| 16 | aiw-engineering-roster-biwk | `0 20 * * 2,5` | pending | Never run |
| 17 | aiw-research-tracker-weekly | `0 21 * * 0` | pending | Never run |
| 18 | aiw-dashboard-refresh | every 15 min | ok | Dashboard HTML regen |
| 19 | cron-sync | every 5 min | pending | Internal |

**Status breakdown**: 12 ok, 1 error (thesis-daily-tick), 6 pending (never run)

**P0 fixes needed (Phase 1)**:
- `thesis-daily-tick` — model drift, delete provider_snapshot + model_snapshot

---

## 6 Dept specs already exist

In `/opt/data/agents/departments/`:
- `ORG-AGENTS.md` (v0.1.0, 231 lines) — constitution
- `01-operations.md` (70 lines)
- `02-finance-legal.md` (106 lines)
- `03-sales-growth.md` (113 lines)
- `04-engineering-delivery.md` (120 lines)
- `05-research-education.md` (112 lines)
- `06-people-culture.md` (111 lines)

**Backup of v0.1.0**: `/opt/data/agents/departments/archive/ORG-AGENTS-v0.1.0-2026-08-13.md` (exists)

**Action needed (Phase 8)**: Upgrade all to v0.2.0 with Sub-roles + Sub-agents + Tooling + SOP sections.

---

## 8 State files (current JSON)

In `/opt/data/agents/state/`:
- `analyst.json` — business-analyst decisions
- `coord.json` — management-coordinator decisions
- `kiki.json` — kiki-coach learning log
- `finance.json` — finance-controller state
- `sales.json` — sales-pipeline state
- `engineering.json` — engineering-roster state
- `research.json` — research-tracker state
- `people.json` — founder-bandwidth-watchdog state (NEW, not yet used)

**Schemas**: Defined in 6 dept specs but NOT in a central `SCHEMAS.md` (Phase 2B creates this).

**Action needed (Phase 2B + 5.5)**: Document schemas + migrate to SQLite.

---

## Source materials (current state)

`/opt/data/source-materials/`:
- `topics/`: 4 topic indexes (hostinger-trademark-incident, paraguai-builder-saas, rubicon-eas-deal, trilingual-middle-market)
- `skills/`: 12 skill indexes
- `prompts/`: 3 prompt templates
- `repos/`: 4 repo indexes
- `topics/org-design/`: NEW (Session 1 deliverables — INDEX, cheatsheet, literature)

**Count**: ~23 files (was), now ~27 with Session 1 additions.

**Action needed (Phase 6)**: Per-dept playbook index, source-materials triage.

---

## Skills installed (current)

51 skills (per `/opt/data/skills/`). Key ones for this plan:

**Already used by existing agents**:
- `aiw-ops-discipline` — operational tone
- `aiw-git-safety` — git safety
- `b2b-cold-outreach-pitch` — sales outreach
- `paraguai-proposal-pricing` — pricing
- `trademark-compliance-scrub` — IP compliance

**Available for v5 agents**:
- `thesis-active-autonomy` — research
- `research-integrity-protocol` — research
- `grounded-citations` — research
- `evaluating-llms-harness` — research/eval
- `github-pr-workflow` — engineering
- `vps-aiw-deploy-pipeline` — engineering
- `client-site-deploy` — engineering
- `live-site-triage` — engineering

**Action needed (Phase 5)**: Each agent's PROMPT.md should reference relevant skills.

---

## What needs to happen in Phase 0

Based on this audit:

1. ✅ Backups (already done in earlier session — confirm)
2. ✅ Decisions doc (just created: `/opt/data/agents/DECISIONS-2026-Q3.md`)
3. ✅ Audit (this file)
4. **TODO**: Create `/opt/data/agents-v2/{patterns,specs,playbooks,prompts,backups,repos,db}/` dirs
5. **TODO**: Backup current ORCHESTRATION.md + jobs.json + 8 state files
6. **TODO**: Write PHASE-0-COMPLETE.md handoff

**Estimated Phase 0 work remaining**: 4-5 tasks, ~6-8 turns.

---

## What this audit reveals

### Strengths
- 3 lead agents already have detailed PROMPT.md (good starting point)
- 12 cron jobs working
- 6 dept specs ratified
- 19 cron jobs inventoried

### Weaknesses
- 6 cron jobs in `pending` state (never run) — risk of unknown bugs
- 1 cron job in error state (thesis-daily-tick) — needs Phase 1 fix
- No git repos backing any agent
- No SQLite (all state is JSON)
- 8 state files lack schema docs
- 23 source materials are unorganized (Phase 6 will triage)

### Opportunities
- Phase 1 only needs to fix 1 cron job (not 3 — most are already green)
- Phase 5 starts with 3 agents to upgrade (not 6 fresh builds)
- Existing dept specs give us 70-120 lines of context per dept
- 51 skills available, 12 already referenced in existing agents

---

**Document path**: `/opt/data/agents-v2/STATE-AUDIT-2026-08-14.md`
**Status**: Audit complete
**Last updated**: 2026-08-14
