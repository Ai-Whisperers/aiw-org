# Complete Plan v5 — AI-Native Org Buildout

> Updated with full research synthesis. 30 functional areas (vs 6), ~135 roles (vs 98), per-agent git repos + SQLite storage architecture.
> **All prior roasts, decisions, and corrections folded in.**

**Last updated**: 2026-08-14
**Author**: Erebus (for Ivan, AI Whisperers Paraguay EAS)
**Scope**: AI-native org buildout for all canonical + cross-cutting + deferred departments.
**Implementation mode**: AI agent (not human) — series-first between phases, parallel within phases.

---

## How to read this document

1. **Part 1** — Executive summary + what's new in v5
2. **Part 2** — What the org looks like when done (30 functional areas, ~50 agents)
3. **Part 3** — Department build order
4. **Part 4** — Storage architecture (NEW in v5: git repos + SQLite)
5. **Part 5** — The 11-phase structure (added Phase 5.5)
6. **Part 6** — Per-phase atomic tasks
7. **Part 7** — The 5 mandatory patterns every agent conforms to
8. **Part 8** — Per-department work (30 functional areas, ~135 roles)
9. **Part 9** — Verification gates
10. **Part 10** — AI-timeline reality
11. **Part 11** — Decisions made
12. **Part 12** — What this plan cannot do

---

# Part 1 — Executive Summary

### The goal

Take the **30 functional areas** (6 Tier 1 + 8 Tier 2 cross-cutting + 12 Tier 3 deferred + 4 Tier 4 enterprise) and fill them with:
- **Real roles** (~135 from the inventory)
- **Real agents** (~40-50 across all tiers)
- **Per-agent storage** (git repo + SQLite DB per agent)
- **Real cadences** (cron-driven, idempotent, off-hours denser heartbeat)
- **Real guardrails** (hard stops, context-payload escalation, eval gates, reflection)
- **Real verification** (every artifact verified by a different prompt)

### What's new in v5 vs v4

| Change | v4 | v5 |
|--------|----|----|
| Functional areas | 6 departments + 3 cross-cutting | **30 functional areas** (6 Tier 1 + 8 Tier 2 + 12 Tier 3 + 4 Tier 4) |
| Role count | ~110 | **~135** |
| Agent count | ~25 | **~40-50** |
| Storage | JSON state files | **Git repos + SQLite DBs per agent** |
| Build order | Per dept sequentially | **7-phase sequenced build** |
| Phase structure | 9 phases | **11 phases** (added 5.5 storage migration) |
| Architecture | Single `/opt/data/agents-v2/` tree | **Per-agent repos + per-agent DBs** |

### What "done" looks like

A **self-running org** where:
- All 7 Tier-1 lead agents deliver on schedule for 7+ consecutive days
- Each agent has its own git repo (memories, decisions, lessons) + SQLite DB (operational state)
- Cron errors caught within 30 min (on-hours) or 15 min (off-hours)
- No silent corruption (SQLite schema validates every 15 min)
- Ivan's "is X live?" messages drop to 0/week
- All public-facing artifacts pass trademark scrub
- Every agent has hard stops, idempotency, context-payload, and (where applicable) reflection

### How long it takes

- **AI sessions**: 20-26 sessions (was 17-22)
- **Turns**: ~200-280 turns
- **Calendar**: 12-18 days at realistic pace
- **Ivan reviews**: ~30 reviews, ~5-7 hours total
- **Tokens**: ~450K total

### The discipline (unchanged from v4)

> **One version good → replicate.** Each artifact class is built once, verified end-to-end, then replicated with modifications. This prevents template drift, scope creep, and the "7 different styles" failure mode.

> **Series between phases, parallel within phases.** No phase N+1 starts until phase N is GREEN. Within a phase, independent sub-tasks can run in the same session.

> **AI-aware timeline.** Phases sized by turns (8-50), not days. Each phase fits in 1-2 AI sessions. Every phase ends with a handoff doc the next session reads first.

---

# Part 2 — What the org looks like when this plan is done

## Org chart (post-plan)

```
                    ┌──────────────────────────────────────┐
                    │  Board (Ivan + Kiki)                │
                    │  - Strategy                         │
                    │  - Approve >$500 spend              │
                    │  - Receive morning + weekly briefs  │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────┐
                    │  Cross-cutting (always-on)           │
                    │  - business-analyst (daily 06:30)    │
                    │  - management-coordinator (Mon/Thu)  │
                    │  - kiki-coach (Fri 17:00)            │
                    │  - ai-ops-coordinator (NEW)          │
                    │  - bizops-tracker (NEW)              │
                    │  - compliance-monitor (NEW)          │
                    │  - revops-pipeline (NEW)             │
                    │  - source-curator (NEW)              │
                    │  + watchdogs: health.sh, heartbeat,  │
                    │    snapshot, validate, cost-cap      │
                    └──────────────┬───────────────────────┘
                                   │
        ┌──────────┬───────────────┼───────────────┬──────────┬──────────┐
        │          │               │               │          │          │
        ▼          ▼               ▼               ▼          ▼          ▼
   ┌────────┐ ┌────────┐     ┌────────┐     ┌────────┐ ┌────────┐ ┌────────┐
   │  Ops   │ │Finance │     │ Sales  │     │  Eng   │ │Research│ │People  │
   │  Tier1 │ │  Tier1 │     │  Tier1 │     │  Tier1 │ │  Tier1 │ │  Tier1 │
   │ +Tier2 │ │ +Tier2 │     │ +Tier2 │     │ +Tier2 │ │ +Tier2 │ │ +Tier2 │
   └────────┘ └────────┘     └────────┘     └────────┘ └────────┘ └────────┘
```

## Agent inventory (~50 agents)

### Tier 1 (active, 7 lead agents)
| Agent | Dept | Cadence | Class |
|-------|------|---------|-------|
| `business-analyst` | Cross-cutting | Daily 06:30 | OPERATIONAL |
| `management-coordinator` | Cross-cutting | Mon/Thu 17:00 | OPERATIONAL |
| `kiki-coach` | Cross-cutting | Fri 17:00 | CONTENT (reflection) |
| `finance-controller` | Finance & Legal | Fri 18:00 | OPERATIONAL |
| `sales-pipeline` | Sales & Growth | Daily 12:00 | CONTENT (reflection, inbound-first) |
| `engineering-roster` | Engineering & Delivery | Tue/Fri 17:00 | OPERATIONAL |
| `research-tracker` | Research & Education | Sun 18:00 | CONTENT (reflection) |

### Tier 2 (active, ~14 sub-agents)
| Agent | Dept | Cadence |
|-------|------|---------|
| `proposal-drafter` | Sales | On-demand |
| `lead-enrichment` | Sales | Daily |
| `marketing-content-producer` | Sales/Marketing | Mon/Wed/Fri |
| `multimedia-producer` | Sales/Marketing | On-demand |
| `accounting-automation` | Finance | Daily |
| `tax-receipt-tracker` | Finance | Weekly |
| `procurement-tracker` | Finance/Procurement | Weekly |
| `devops-monitor` | Engineering | Every 30 min |
| `qa-automation-runner` | Engineering | On-PR |
| `security-watchdog` | Engineering | Every 30 min |
| `ai-safety-engineer` | Engineering | Every 30 min |
| `citation-checker` | Research | On-demand |
| `thesis-tracker` | Research | Daily 06:00 |
| `course-producer` | Research | Weekly |
| `source-curator` | Research | Weekly |
| `founder-bandwidth-watchdog` | People | Weekly |

### Tier 2 cross-cutting (8 NEW)
| Agent | Function | Cadence |
|-------|----------|---------|
| `ai-ops-coordinator` | AI Ops | Daily |
| `eval-gate-runner` | AI Ops | On-agent-run |
| `chaos-test-runner` | AI Ops | Weekly |
| `bizops-tracker` | BizOps | Weekly |
| `compliance-monitor` | Compliance | Weekly |
| `revops-pipeline-analyzer` | RevOps | Daily |
| `pipeline-analyzer` | RevOps | Daily |
| `okr-tracker` | BizOps | Weekly |

### Tier 3 (deferred, ~15 triggers)
Documented in `DEFERRED-AGENTS.md` with explicit promotion triggers.

## State files + repos (per-agent storage)

### Per-agent git repos (17 repos)
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

### Per-agent SQLite DBs (~11 DBs)
```
/opt/data/db/
├── business-analyst.db
├── management-coordinator.db
├── kiki-coach.db
├── finance-controller.db
├── sales-pipeline.db
├── engineering-roster.db
├── research-tracker.db
├── ai-ops.db
├── compliance.db
├── source-curator.db
└── bandwidth.db
```

### Cron jobs (~30 total)
19 existing + 8-12 new + 7 infra = **~30 cron jobs at buildout**.

---

# Part 3 — Department build order (Ivan's directive)

> Ivan: "start with management dept then sales then marketing and so on"

Build order respects dependencies + revenue-first within non-mgmt:

### Phase A — Management/Operations (build first)
**Why first**: Every other dept reads from cross-cutting agents. Without management spine, the org is blind.
- Operations dept (Tier 1)
- AI Ops (Tier 2 cross-cutting) — own it now before more agents ship
- BizOps (Tier 2 cross-cutting)

### Phase B — Revenue depts (build second)
**Why second**: Only revenue-producing dept. Without sales, the company dies.
- Sales dept (Tier 1) + proposal-drafter + lead-enrichment
- Marketing (sub of Sales initially) + content-producer + multimedia-producer
- RevOps (Tier 2 cross-cutting)

### Phase C — Operations-supporting depts (build third)
**Why third**: Everything else depends on infrastructure.
- Engineering (Tier 1) + devops + qa + security-watchdog
- AI Safety (Tier 2 sub of Engineering)

### Phase D — Finance + compliance (build fourth)
**Why fourth**: Finance depends on sales + engineering outputs.
- Finance (Tier 1) + accounting-automation + tax-receipt-tracker
- Compliance (Tier 2 named role)
- Procurement (Tier 2 cross-cutting)

### Phase E — Research + knowledge (build fifth)
**Why fifth**: Flagship but not daily-driver.
- Research (Tier 1) + citation-checker + thesis-tracker + course-producer
- Knowledge Management (Tier 2 cross-cutting)

### Phase F — People (build sixth)
**Why sixth**: Internal-facing. By here, we've seen real workloads.
- People (Tier 1) + kiki-coach (extended) + founder-bandwidth-watchdog

### Phase G — Tier 3 depts (deferred, trigger-based)
- Customer Success (5+ clients)
- Marketing independent (>$2K/mo budget)
- Compliance standalone (first EU client)
- Knowledge Management standalone (>100 source-materials files)
- AI Governance (>15 agents)
- Investor Relations (first external investor)
- Chief of Staff (>50 hrs coord/week)
- DevRel (ParaguAI Builder public API)
- Workplace (open physical office)
- Fraud/Risk ($500K+ payment volume)
- Compensation & Benefits (first FTE)
- People Operations (5+ FTEs)

---

# Part 4 — Storage architecture (NEW in v5)

## 3-layer model

### Layer 1: Git repos (per agent, per dept)
- **Permanent, version-controlled, auditable**
- Each agent has own repo with: PROMPT.md, outbox/, state/ (gitignored), logs/, memories/, decisions/, lessons/, eval/, README, CHANGELOG
- Push to GitHub `Ai-Whisperers/` org (private)

### Layer 2: SQLite (per-agent operational state)
- **One SQLite DB per agent** at `/opt/data/db/<agent>.db`
- Schema: episodic tables (leads, outreach_log), decisions, idempotency, state_snapshots
- Daily snapshot to `/opt/data/backups/db/{date}/`, retained 90 days
- Weekly offsite to R2

### Layer 3: Qdrant (deferred to Tier 2)
- **Semantic memory for RAG** (cross-agent, cross-source-materials search)
- Ships when source-materials > 50 files OR first eval-gate needs golden trajectories

## Memory taxonomy

| Memory type | Backend | Example |
|------------|---------|---------|
| Episodic (what happened) | Git `outbox/`, `logs/`, `decisions/` | "Yesterday drafted 3 outreach emails" |
| Semantic (what I know) | SQLite + Qdrant | "ICP match for legal vertical is 70%" |
| Procedural (how I do things) | Git `PROMPT.md` + `patterns/` | "Always check idempotency before action" |

## Backup strategy
- **Git repos**: pushed to GitHub `Ai-Whisperers/` (private, per-agent repos)
- **SQLite DBs**: daily snapshot cron + weekly offsite to R2
- **Qdrant** (Tier 2): snapshot weekly

## Migration strategy (Phase 5.5)

Current state: JSON files at `/opt/data/agents/state/*.json`. New: SQLite + git.

**Phase 5.5 sub-tasks**:
1. Build per-agent git repo structure (17+ repos)
2. Write migration script: JSON state → SQLite
3. Set up git push automation (cron for each agent)
4. Set up SQLite backup cron
5. Validate: all agents still deliver correctly
6. Keep JSON files as read-only mirror for 30 days

---

# Part 5 — The 11-phase structure

| Phase | Name | Goal | Turns | Sessions |
|-------|------|------|-------|----------|
| **0** | Decisions + Setup | 8 decisions; backups; dirs | 8-12 | 1 |
| **1** | Fix P0 cron errors + unify storage | 3 jobs green; single path | 8-13 | 1-2 |
| **2** | Infra: snapshot + validate + heartbeat | 3 scripts proven | 26-39 | 2-3 |
| **3** | Lock patterns + template | 4 patterns + template | 15-20 | 1-2 |
| **4** | First reference agent | `business-analyst` complete | 10-15 | 1 |
| **5** | Replicate to 6 lead agents | All 6 conform + soak | 30-50 | 4-6 |
| **5.5** | **Storage migration (NEW)** | Git repos + SQLite per agent | 25-35 | 2-3 |
| **6** | Per-dept playbook catalog | 30 functional areas catalogued | 35-50 | 3-4 |
| **7** | Procurement + grid + cash-flow | Decisions + cost-cap | 15-20 | 1-2 |
| **8** | Constitution v0.2.0 + docs | Bumped + deferred + rituals | 15-20 | 2 |
| **9** | Operational disciplines + self-running | Fallbacks + security + chaos + milestone | 20-30 | 2-3 |

**Total**: 20-26 sessions, ~200-280 turns, ~450K tokens.

### Series-first discipline
- Each phase ends with `PHASE-N-COMPLETE.md` handoff
- Each phase has explicit verification gate
- Next phase doesn't start until current is GREEN

---

# Part 6 — Per-phase atomic tasks

## Phase 0 — Decisions + Setup (8-12 turns, 1 session)

| # | Task | Verification |
|---|------|--------------|
| 0.1 | Read existing `ORG-AGENTS.md`, `ORCHESTRATION.md`, `state/*.json` | 5-6 reads |
| 0.2 | Write `/opt/data/agents/DECISIONS-2026-Q3.md` (D1-D8) | File exists, 8 decisions |
| 0.3 | Backup ORG-AGENTS.md, ORCHESTRATION.md, jobs.json, 8 state files | 12 backups |
| 0.4 | Create `/opt/data/agents-v2/{patterns,specs,playbooks,prompts,backups,repos,db}/` | 7 dirs |
| 0.5 | Write `PHASE-0-COMPLETE.md` | File exists |

## Phase 1 — Fix P0 cron errors (8-13 turns, 1-2 sessions)

### 1A — Atomic cron fixes (5-8 turns)
- Edit jobs.json: delete provider_snapshot + model_snapshot from morning-brief + thesis-daily-tick
- Fix aiw-dashboard-refresh: workdir + absolute script path
- Verify: `hermes cron list` shows 3 green
- Manual run: aiw-dashboard-refresh writes HTML

### 1B — Unify cron storage (3-5 turns)
- Diff /opt/data/cron/jobs.json vs /opt/data/.hermes/cron/jobs.json
- Symlink if different
- Verify: same count from both paths

## Phase 2 — Infra (26-39 turns, 2-3 sessions)

### 2A — State snapshot (8-12 turns)
- Write `/opt/data/agents/scripts/state-snapshot.sh` (atomic: temp + mv)
- Race test: 2 concurrent
- Register `aiw-state-snapshot-6h` `0 */6 * * *` PYT

### 2B — State validate (10-15 turns)
- Write `state/SCHEMAS.md` (≥6 sections)
- Write `validate-state.py` with `/tmp/validate-state.lock`
- Test: corrupt file → exit 1 + violation report
- Register `aiw-state-validate-15m` `*/15 * * * *` PYT

### 2C — Cron heartbeat (8-12 turns)
- Write `cron-heartbeat.sh` with rate-limit
- Register on-hours `*/30 6-22 * * *` + off-hours `*/15 23-5 * * *` PYT
- Test: simulated error → fires; rate-limit suppresses

## Phase 3 — Lock patterns (15-20 turns, 1-2 sessions)

| # | Task | Verification |
|---|------|--------------|
| 3.1-3.3 | Idempotency pattern + example + test | py_compile + run |
| 3.4-3.7 | Hard-stop pattern + wrapper + test | wrapper blocks |
| 3.8 | Context-payload pattern (6-field JSON schema) | schema valid |
| 3.9 | Reflection loop pattern | file exists |
| 3.10 | PROMPT-TEMPLATE.md (12 sections, fallback_model) | 12 sections |
| 3.11-3.12 | Trademark-scrub pattern + test | catches banned |

## Phase 4 — First reference agent (10-15 turns, 1 session)

| # | Task | Verification |
|---|------|--------------|
| 4.1 | Read current business-analyst/PROMPT.md | Read |
| 4.2 | Copy PROMPT-TEMPLATE.md → business-analyst/PROMPT.md | File overwritten |
| 4.3 | Fill dept-specific 10 sections | All placeholders replaced |
| 4.4 | Add Hard Stops (3 stops for business-analyst) | Wrapper validates |
| 4.5-4.7 | Add Idempotency + Context-Packaging + Fallback Model | All sections present |
| 4.8 | Verify 12 sections | `grep -c "^## "` returns 12 |
| 4.9 | Save as PROMPT.md.reference (gold) | Gold exists |
| 4.10-4.13 | Manual run + duplicate trigger + escalation + trademark scrub | All pass |
| 4.14 | Update ORCHESTRATION.md | Row updated |
| 4.15 | Write PHASE-4-COMPLETE.md | File exists |

## Phase 5 — Replicate to 6 lead agents (30-50 turns, 4-6 sessions)

**Order** (Ivan's directive, modified for dependencies):
1. `management-coordinator` (cross-cutting)
2. `kiki-coach` (cross-cutting, content+reflection)
3. `finance-controller` (financial discipline)
4. `sales-pipeline` (revenue, inbound-first, content+reflection)
5. `engineering-roster` (technical delivery)
6. `research-tracker` (knowledge work, content+reflection)

**Per-agent pattern** (~5-8 turns each):
- Copy template → fill dept-specific 10 sections
- Add Hard Stops (3-5 dept-specific)
- Add Idempotency + Context-Packaging + Fallback
- Add Reflection (content agents only)
- Create `state/<dept>.json` with initial schema
- Create `outbox/.gitkeep` + seed example
- Verifier pass: 12 sections + trademark scrub
- Register cron
- grid.sh verify zero collisions
- Manual run + 1-day soak
- Write `<agent>-DAY-1-OBSERVATION.md`

## Phase 5.5 — Storage migration (25-35 turns, 2-3 sessions) **NEW**

**Goal**: Per-agent git repos + SQLite DBs.

### 5.5A — Build git repo structure (8-12 turns)
| # | Task | Verification |
|---|------|--------------|
| 5.5A.1 | Create `/opt/data/git-repos/` dir tree | Exists |
| 5.5A.2 | `git init` per agent (17 repos) | 17 repos |
| 5.5A.3 | Write per-agent README.md (template) | 17 files |
| 5.5A.4 | Write per-agent CHANGELOG.md (initial) | 17 files |
| 5.5A.5 | Add `.gitignore` (excludes state/, db/, logs/) | 17 files |
| 5.5A.6 | Configure git push to GitHub (private org) | All repos remote-set |

### 5.5B — Migrate state JSON to SQLite (10-15 turns)
| # | Task | Verification |
|---|------|--------------|
| 5.5B.1 | Write SQLite schema template | `python3 -m py_compile` passes |
| 5.5B.2 | Write migration script (JSON → SQLite) | Script runs |
| 5.5B.3 | Migrate business-analyst state | SQLite populated |
| 5.5B.4 | Migrate other 6 lead agents | All migrated |
| 5.5B.5 | Verify: JSON contents == SQLite contents | Diff = 0 |

### 5.5C — Backup automation (7-8 turns)
| # | Task | Verification |
|---|------|--------------|
| 5.5C.1 | Write SQLite backup script (sqlite3 .backup) | `bash -n` passes |
| 5.5C.2 | Register `aiw-db-snapshot-daily` cron | Visible |
| 5.5C.3 | Test backup + restore roundtrip | Works |
| 5.5C.4 | Write git-push automation (per-agent) | All agents push |
| 5.5C.5 | Register `aiw-git-push-daily` cron | Visible |

## Phase 6 — Per-dept playbook catalog (35-50 turns, 3-4 sessions)

### 6A — Reference playbook + INDEX (12-18 turns)
- Write PLAYBOOK-TEMPLATE.md
- Write `01-operations.md` (Operations + AI Ops + BizOps)
- Verify URLs + trademark scrub
- Save as reference gold
- Write `00-INDEX.md`

### 6B — Replicate to remaining functional areas (23-32 turns)

**Order** (Ivan's directive: sales → marketing → ...):
1. `02-sales-growth.md` (includes Marketing)
2. `03-engineering-delivery.md` (includes AI Safety)
3. `04-finance-legal.md` (includes Compliance, Procurement)
4. `05-research-education.md` (includes Knowledge Management)
5. `06-people-culture.md`
6. `07-cross-cutting-concerns.md` (AI Ops, BizOps, RevOps)
7. `08-deferred-tier3.md` (12 dept triggers documented)

**Per-playbook**: copy template + fill + verify URLs + trademark scrub + role count check.

## Phase 7 — Procurement + cron grid + cash-flow (15-20 turns)

- Get pre-Phase-7 budget approval
- Write `tool-stack-decisions.md` (Sections A-F)
- Cost roll-up + cash-flow model + FX notes
- Vendor consolidation (3-5 opportunities)
- Pricing refresh (per AI-SDR 2026 reckoning)
- Write cost-cap.sh
- grid.sh verify

## Phase 8 — Constitution v0.2.0 + docs (15-20 turns)

- Read current 6 dept specs
- Add Sub-roles, Sub-agents, Tooling, SOP sections
- Bump version 0.1.0 → 0.2.0
- Update ORG-AGENTS.md: all 8 sections
- Add ON-CALL, Cultural Rituals, Board Governance
- Write DEFERRED-ROLES.md (30 functional areas, ~135 roles)
- Write DEFERRED-AGENTS.md (Tier 3 triggers)
- Write REVIEW-2026-Q4.md (30/60/90-day checklist)
- Write BURNOUT-SIGNAL-SPEC.md
- Write STORAGE-ARCHITECTURE.md (NEW)

## Phase 9 — Operational disciplines + self-running (20-30 turns)

- 9A: Model fallbacks + gitignore spec (5-8 turns)
- 9B: Security + load + chaos tests (10-15 turns)
- 9C: Self-running milestone (5-7 turns)

---

# Part 7 — The 5 mandatory patterns (unchanged)

1. **Hard Stops** — action-level approval gates, enforced via wrapper
2. **Idempotency Contract** — state.last_run + window check
3. **Context-Packaging Escalation** — 6-field JSON payload
4. **Reflection Loop** — content-producing agents only
5. **Fallback Model** — primary + fallback + retry logic

---

# Part 8 — Per-department work (30 functional areas)

## 8.1 — Tier 1 (6 canonical departments)

**Operations** (Ops Lead, Repo Steward, Asset Tracker, Vendor Coordinator, Compliance Watchdog, Watchdog Engineer)
- Lead: `management-coordinator` Mon/Thu 17:00
- Tier 2: source-curator, ai-ops-coordinator, bizops-tracker, compliance-monitor
- Hard stops: write_state, comment_on_issue (require ivan), close_issue (require ivan)

**Finance & Legal** (CFO, Accountant, Bookkeeper, AP/AR, Procurement Officer, Legal Counsel, Tax Specialist, Contract Drafter, Pricing Analyst, FP&A Analyst)
- Lead: `finance-controller` Fri 18:00
- Tier 2: accounting-automation, tax-receipt-tracker, procurement-tracker, compliance-monitor
- Hard stops: send_invoice, apply_refund, sign_contract (require ivan), modify_pricing

**Sales & Growth** (Head of Sales, SDR, BDR, AE, Sales Engineer, CSM, Proposal Writer, Marketing Manager, Content Producer, Multimedia Designer, SEO Specialist, Email Marketing Specialist, Community Manager, Account Manager, Renewals Manager, Channel Sales Manager)
- Lead: `sales-pipeline` Daily 12:00
- Tier 2: proposal-drafter, lead-enrichment, marketing-content-producer, multimedia-producer, customer-health-scorer
- Hard stops: send_outreach, send_proposal, apply_discount (all require ivan)

**Engineering & Delivery** (CTO, Frontend, Backend, Full-stack, Mobile, DevOps/SRE, QA, Security, ML Engineer, Data Engineer, Solutions Architect, Tech Writer, Product Designer, Engineering Manager, Release Manager, Build Engineer, Embedded Engineer, AI Safety Engineer, Database Admin, Network Engineer)
- Lead: `engineering-roster` Tue/Fri 17:00
- Tier 2: devops-monitor, qa-automation-runner, security-watchdog, ai-safety-engineer
- Hard stops: merge_pr, deploy_prod (require kiki), force_push (require ivan)

**Research & Education** (Research Lead, Researcher, Writer/Editor, Citation Specialist, Course Designer, Course Producer, Instructional Designer, SME, Research Engineer, IP/Patent Specialist, Publication Coordinator, Source Curator)
- Lead: `research-tracker` Sun 18:00
- Tier 2: citation-checker, thesis-tracker, course-producer, source-curator
- Hard stops: submit_arxiv, publish_course_module (require ivan + kiki)

**People & Culture** (Head of People, Recruiter, Onboarding Specialist, Performance Coach, Recognition Lead, Compensation Specialist, People Ops, L&D Manager)
- Lead: `kiki-coach` Fri 17:00
- Tier 2: founder-bandwidth-watchdog
- Hard stops: modify_curriculum (require kiki)

## 8.2 — Tier 2 cross-cutting (8 NEW)

**AI Ops** — agent layer health, eval gates, agent observability
- Owner: Kiki
- Agents: ai-ops-coordinator, eval-gate-runner, chaos-test-runner
- Trigger to promote: agent count > 10 OR chaos failures > 1/month

**Compliance** — named role (D3), hard-stop on EU clients
- Owner: Ivan (named)
- Agents: compliance-monitor
- Trigger to promote: first EU client OR $50K MRR

**Knowledge Management** — source-materials curation
- Owner: Ivan (policy) + source-curator agent (mechanical)
- Trigger to promote: > 100 source-materials files

**RevOps** — funnel optimization
- Sub-function of Sales
- Agents: pipeline-analyzer, revops-pipeline-analyzer
- Trigger to promote: pipeline value > $500K

**BizOps** — cross-functional analytics, OKR tracking
- Sub-function of Operations
- Agents: bizops-tracker, okr-tracker
- Trigger to promote: Ivan's coord hours > 30/week

**Customer Success** — post-sale retention
- Sub-function of Sales
- Agents: customer-health-scorer
- Trigger to promote: 5+ recurring clients

**AI Safety** — Kiro-class incident prevention
- Sub-function of Engineering
- Agents: ai-safety-engineer
- Always active (every agent has safety)

**Procurement** — vendor evaluation, renewals
- Sub-function of Finance
- Agents: procurement-tracker
- Trigger to promote: active vendors > 10 OR SaaS spend > $1K/mo

## 8.3 — Tier 3 deferred (12-15)

All documented in `DEFERRED-AGENTS.md` with quantitative triggers (see Part 3 above).

## 8.4 — Tier 4 enterprise (5)

Documented but not in scope at our scale.

---

# Part 9 — Verification gates (one per phase)

| Phase | Gate | Pass criteria |
|-------|------|---------------|
| **0** | Setup complete | 8 decisions + 12 backups + 7 dirs + handoff |
| **1** | P0 cron errors fixed | 3 jobs green + storage unified |
| **2** | Infra proven | snapshot/validate/heartbeat all tested |
| **3** | Patterns locked | 4 patterns + template + verifier verified |
| **4** | First agent reference | business-analyst conforms to template, 3-day soak |
| **5** | 6 agents replicated | All conform + grid clean + 1-day soak each |
| **5.5** | Storage migrated | 17 git repos + 11 SQLite DBs + backup automation |
| **6** | Playbook catalog | 30 functional areas + 135 roles + URLs verified + trademarks clean |
| **7** | Procurement + grid | Ivan budget approved + decisions doc + cost-cap |
| **8** | Constitution bumped | 6 specs v0.2.0 + ORG-AGENTS v0.2.0 + CHANGELOG + deferred docs |
| **9** | Operational disciplines + self-running | All verified + self-running achieved OR gap documented |

---

# Part 10 — AI-timeline reality

### Session shape

- Phase 0-1: 1 session each (~10-15 turns)
- Phase 2: 2-3 sessions (~26-39 turns)
- Phase 3-4: 1-2 sessions each (~15-25 turns)
- Phase 5: 4-6 sessions (~30-50 turns)
- Phase 5.5: 2-3 sessions (~25-35 turns)
- Phase 6: 3-4 sessions (~35-50 turns)
- Phase 7-9: 1-3 sessions each

**Total**: 20-26 sessions, ~450K tokens.

### Calendar estimate

- 20-26 sessions at 1-2 sessions/day = 10-26 calendar days
- Realistic with Ivan reviews + rate limits: 12-18 calendar days
- + 30-day post-rollout loop

### Ivan reviews per phase

| Phase | Reviews | Time |
|-------|---------|------|
| 0 | 1 | 5 min |
| 1-3 | 0 (auto-verified) | — |
| 4 | 1 | 5 min |
| 5 | 6 (per agent) | 30 min |
| 5.5 | 1 | 15 min |
| 6 | 1 | 20 min |
| 7 | 1 (budget) | 20 min |
| 8 | 1 (ratification) | 30 min |
| 9 | 1 (milestone) | 15 min |
| **Total** | **~14 reviews** | **~2.5 hours** |

---

# Part 11 — Decisions made (no re-asking)

Per Ivan: "you decide, you built everything."

### D1-D8 (Phase 0)
- D1: Cost cap $1/agent/day, $10/day total
- D2: Sales inbound-first, outbound deferred
- D3: Compliance Officer named role (Ivan wears hat), hard-stop on EU clients
- D4: /opt/data/agents-v2/ as new sibling dir
- D5: Gitignored state + 6-hour snapshot + manual archive
- D6: Idempotency = state.last_run + window check
- D7: Hard stops = PROMPT.md prose + runtime wrapper
- D8: Template AFTER first agent (locked from reference)

### Q1-Q5 (resolved in v3/v4)
- Q1: New dir not new repo
- Q2: 500-word / 2-week threshold for sub-agent promotion
- Q3: Eval-gate POC on business-analyst only
- Q4: Research owns source-materials policy; source-curator agent Tier 2
- Q5: Eval-gate infra after Phase 8 (post-rollout)

### v5 NEW decisions
- **Storage**: Per-agent git repos (17+) + SQLite DBs (11) — 3-layer model
- **Functional areas**: 30 (6 Tier 1 + 8 Tier 2 + 12 Tier 3 + 4 Tier 4)
- **Role count**: ~135 (was 98 in Session 1)
- **Agent count**: ~40-50 (was ~25)
- **Phase 5.5 added**: Storage migration
- **Phase 6 expanded**: 6 dept playbooks → 8 catalog files covering all 30 functional areas
- **Phase 8 added**: STORAGE-ARCHITECTURE.md

### Operational decisions
- Token budget per phase: 50K cap
- Phase 4 soak: 3 days (not 7)
- Verifier: same model, different prompt + skill
- Self-running milestone: 7 days all-green + 0 "is X live?" messages/week
- EU client hard-stop: until Compliance Officer filled by named person
- Chaos tests: 3 scenarios (LLM down, corrupt state, malformed tool)
- Gitignore policy: state/, db/, logs/ excluded; outbox/, decisions/, lessons/, eval/ committed
- DB backup: daily snapshot cron + weekly R2 offsite
- Qdrant: deferred to Tier 2

---

# Part 12 — What this plan cannot do

- Hire a real human
- Sign a real contract
- Spend real money without Ivan's approval
- Make decisions that affect people's lives (FTE, EU client, etc.)
- Replace Ivan's judgment on values/mission/strategy
- Run without Ivan's "continue" between phases (by design)

The plan CAN:
- Wire agents to do mechanical work
- Maintain agent layer autonomously
- Surface decisions for Ivan to make
- Audit itself (trademark, hard stops, idempotency)
- Self-test (chaos, load, eval gates)
- Detect and report failures within minutes (heartbeat)

---

# Final note

When Ivan says **"go"**, I execute Phase 0.

Phase 0 takes 8-12 turns (~1 session). Output: 1 decisions doc + 12 backups + 7 dirs + 1 handoff doc.

Then I stop. Wait for Ivan's "continue" before Phase 1.

The plan can't run end-to-end without Ivan's "continue" between phases. **By design.**

---

**Document path**: `/opt/data/agents-v2/PLAN-v5.md`
**File size**: comprehensive
**Last updated**: 2026-08-14
**Version**: 5.0
**Status**: Ready for execution
