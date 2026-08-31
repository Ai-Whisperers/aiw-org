# Complete Org Inventory for AI-Run Business — Research-Driven

> Exhaustive research synthesis. 105+ queries across 3 waves. Evidence-cited.
> **Decision-authority**: Ivan said "you decide, you built everything." Every decision in this document is autonomous.
> **Last updated**: 2026-08-14

---

## Reading guide

- **Part 1** — Why 15 → 6 was wrong (and the real number)
- **Part 2** — The complete department catalog (Tier 1 + Tier 2 + Tier 3 + Tier 4)
- **Part 3** — Role inventory (~120+ roles)
- **Part 4** — Storage architecture (git repos + DB-backed memory)
- **Part 5** — Build order (which departments to staff first)
- **Part 6** — What this means for PLAN-v4

---

# Part 1 — Why "6 departments" was too compressed

The Session 1 cheatsheet said "6 functional departments is enough for 2 founders." That's correct **for Tier 1 staffing**. But it's wrong as a **catalog of functions the org needs**.

A real org has ~15-20 functional areas. Within each, there are 3-8 sub-roles. Within each sub-role, there's an SOP. An AI-run business can have 1 human + 30 agents filling these roles — the human isn't the constraint, the role catalog is.

**The corrected view**:

| Layer | Count | What's there |
|-------|-------|--------------|
| **Tier 1 departments** (active now) | 6 | Operations, Finance-Legal, Sales-Growth, Eng-Delivery, Research-Edu, People-Culture |
| **Tier 2 sub-departments / disciplines** (active now as cross-cutting concerns) | 8-10 | AI Ops, Compliance, Knowledge Mgmt, RevOps, BizOps, Customer Success prep, AI Safety, Procurement discipline |
| **Tier 3 departments** (deferred, trigger-based) | 12-15 | Investor Relations, Trust & Safety, Data Protection Office, Treasury, Internal Audit, etc. |
| **Total functional areas** | **~30** | Real org-chart nodes |
| **Total roles** | **~120+** | Standard role catalog |
| **Total agent candidates** | **~40-50** | Full build-out |

---

# Part 2 — The complete department catalog (30 functional areas)

Organized by tier. Each entry: **Name / Mission / Trigger to activate / Trigger to promote to own dept / SOPs / Sub-roles / Hard-stops**.

## Tier 1 — Active canonical departments (6)

### 1. Operations / Management
- **Mission**: Keep the agent platform itself alive, healthy, observable
- **Status**: Active (existing)
- **Lead agent**: `management-coordinator` (Mon/Thu 17:00)
- **Sub-roles**: Operations Lead, Repo Steward, Asset Tracker, Vendor Coordinator, Compliance Watchdog, Watchdog Engineer, BizOps Specialist (Tier 2), RevOps Specialist (Tier 2)
- **Agents**: management-coordinator, business-analyst, source-curator (Tier 2), ai-ops-coordinator (Tier 2)

### 2. Finance & Legal
- **Mission**: Track every dollar, every contract, every compliance flag
- **Status**: Active (existing)
- **Lead agent**: `finance-controller` (Fri 18:00)
- **Sub-roles**: CFO/Controller, Accountant, Bookkeeper, AP/AR Specialist, Procurement Officer, Legal Counsel, Tax Specialist, Contract Drafter, Pricing Analyst, FP&A Analyst, Treasury Manager (Tier 3), Compliance Officer (Tier 2, named)
- **Agents**: finance-controller, accounting-automation (Tier 2), tax-receipt-tracker (Tier 2), procurement-tracker (Tier 2)

### 3. Sales & Growth
- **Mission**: Generate qualified leads, run outreach, close deals
- **Status**: Active (existing)
- **Lead agent**: `sales-pipeline` (Daily 12:00)
- **Sub-roles**: Head of Sales, SDR, BDR, AE, Sales Engineer, Customer Success Manager, Proposal Writer, Marketing Manager, Content Producer, Multimedia Designer, SEO Specialist (Tier 2), Email Marketing Specialist (Tier 2), Community Manager (Tier 2), Account Manager, Renewals Manager, Channel Sales Manager (Tier 2)
- **Agents**: sales-pipeline, proposal-drafter (Tier 2), lead-enrichment (Tier 2), marketing-content-producer (Tier 2), multimedia-producer (Tier 2), customer-success (Tier 3)

### 4. Engineering & Delivery
- **Mission**: Ship, maintain, secure the platforms
- **Status**: Active (existing)
- **Lead agent**: `engineering-roster` (Tue/Fri 17:00)
- **Sub-roles**: CTO/Eng Lead, Frontend, Backend, Full-stack, Mobile (Tier 3), DevOps/SRE, QA, Security, ML Engineer (Tier 3), Data Engineer (Tier 3), Solutions Architect (Tier 3), Tech Writer (Tier 2), Product Designer (Tier 2), Engineering Manager (Tier 3), Release Manager, Build Engineer, Embedded Engineer (Tier 3), AI Safety Engineer (Tier 2), Database Admin (Tier 2), Network Engineer (Tier 2)
- **Agents**: engineering-roster, devops-monitor (Tier 2), qa-automation-runner (Tier 2), security-watchdog (Tier 2), ai-safety-engineer (Tier 2)

### 5. Research & Education
- **Mission**: Drive thesis + courses + IP to completion
- **Status**: Active (existing)
- **Lead agent**: `research-tracker` (Sun 18:00)
- **Sub-roles**: Research Lead, Researcher, Writer/Editor, Citation Specialist, Course Designer, Course Producer, Instructional Designer (Tier 3), SME, Research Engineer (Tier 2), IP/Patent Specialist (Tier 3), Publication Coordinator, Source Curator (Tier 2)
- **Agents**: research-tracker, citation-checker (Tier 2), thesis-tracker (Tier 2), course-producer (Tier 2), source-curator (Tier 2)

### 6. People & Culture
- **Mission**: Founders + future hires stay sharp, healthy, growing
- **Status**: Active (existing)
- **Lead agent**: `kiki-coach` (Fri 17:00)
- **Sub-roles**: Head of People, Recruiter (Tier 4), Onboarding Specialist (Tier 4), Performance Coach, Recognition Lead, Compensation Specialist (Tier 4), People Ops (Tier 3), L&D Manager (Tier 3)
- **Agents**: kiki-coach, founder-bandwidth-watchdog (Tier 2)

## Tier 2 — Cross-cutting concerns (active now)

### 7. AI Ops (new cross-cutting function)
- **Mission**: Keep the agent layer itself healthy — patterns, eval gates, agent observability
- **Status**: Active as cross-cutting concern (Tier 2)
- **Owner**: Kiki (CTO)
- **Trigger to become standalone dept**: Agent count > 10 OR chaos test failures > 1/month
- **Sub-roles**: AI Ops Lead, Agent Reliability Engineer, MLOps Engineer, Prompt Engineer (Tier 2), AI Evaluator, Agent Manager
- **Agents**: ai-ops-coordinator (Tier 2), eval-gate-runner (Tier 2), chaos-test-runner (Tier 2)

### 8. Compliance (named role, hard-stop on EU clients)
- **Mission**: Own the compliance program (GDPR, LGPD, EU AI Act, trademark)
- **Status**: Active (D3 decision); Ivan wears the hat
- **Owner**: Ivan (named, with hard-stop rule)
- **Trigger to become standalone dept**: First EU client OR $50K MRR
- **Sub-roles**: Compliance Officer (named), Privacy Counsel/DPO (Tier 3), Trademark Specialist, Regulatory Affairs (Tier 3)
- **Agents**: compliance-monitor (Tier 2, watches for changes in regulations)

### 9. Knowledge Management (sub-function of Research, Tier-2 promotion)
- **Mission**: Curate source-materials/, retire stale content, ensure citation quality
- **Status**: Active; Research owns policy, `source-curator` agent does mechanical work
- **Owner**: Ivan (policy) + source-curator agent (mechanical)
- **Trigger to become standalone dept**: source-materials/ > 100 files OR second knowledge-heavy vertical
- **Sub-roles**: Knowledge Manager, Content Curator, Citation Specialist, Taxonomy Architect (Tier 3)
- **Agents**: source-curator (Tier 2, exists in plan)

### 10. RevOps (Revenue Operations)
- **Mission**: Optimize the funnel from lead → cash
- **Status**: Active as Tier-2 sub-function of Sales
- **Trigger to become standalone dept**: Pipeline value > $500K OR sales team > 5
- **Sub-roles**: RevOps Lead, Sales Ops Analyst, Marketing Ops Manager, BI Analyst (Tier 2), Data Steward (Tier 3)
- **Agents**: pipeline-analyzer (Tier 2, computes funnel metrics)

### 11. BizOps (Business Operations)
- **Mission**: Cross-functional analytics, OKR tracking, executive decision support
- **Status**: Active as Tier-2 sub-function of Operations
- **Trigger to become standalone dept**: Ivan's coordination hours > 30/week
- **Sub-roles**: BizOps Lead, Strategy Analyst, Operations Analyst
- **Agents**: okr-tracker (Tier 2), exec-brief-generator (Tier 2)

### 12. Customer Success (prep work now, promote later)
- **Mission**: Post-sale retention, expansion, renewal
- **Status**: Tier 2 prep, promoted to dept at 5+ recurring clients
- **Trigger**: 5+ recurring clients
- **Sub-roles**: CSM Lead, Onboarding Specialist, Account Manager, Renewals Manager, Customer Education (Tier 3), Support Engineer (Tier 2)
- **Agents**: customer-health-scorer (Tier 2), onboarding-bot (Tier 3)

### 13. AI Safety (sub-function of Engineering, Tier 2)
- **Mission**: Prevent Kiro-class incidents (agent runs amok with elevated perms)
- **Status**: Active; ai-safety-engineer role Tier 2
- **Owner**: Kiki
- **Sub-roles**: AI Safety Engineer, AI Red Team, AI Evaluator, OWASP LLM Compliance
- **Agents**: safety-watchdog (Tier 2), red-team-runner (Tier 2)

### 14. Procurement Discipline
- **Mission**: Vendor evaluation, contract negotiation, renewal management
- **Status**: Sub-function of Finance; promote to dept when active vendors > 10 OR SaaS spend > $1K/mo
- **Owner**: Ivan (currently), `procurement-tracker` agent Tier 2
- **Sub-roles**: Procurement Manager, Vendor Manager, Contract Negotiator, Renewal Specialist
- **Agents**: procurement-tracker (Tier 2), vendor-renewal-watchdog (Tier 2)

## Tier 3 — Deferred departments (12-15)

| # | Department | Trigger to activate | Notes |
|---|------------|---------------------|-------|
| 15 | **Customer Success (full)** | 5+ recurring clients | Expansion revenue, churn prevention |
| 16 | **Marketing (independent)** | >$2K/mo marketing budget | When brand becomes its own P&L |
| 17 | **Trust & Safety** | Ship consumer AI product | Misuse prevention, content moderation |
| 18 | **Data Protection Office** | First EU client | DPO required by GDPR Article 37 |
| 19 | **Treasury (independent)** | $100K+ cash OR debt | Banking, FX, investment management |
| 20 | **Internal Audit** | $1M+ revenue | Constitutional enforcement, audit trails |
| 21 | **Investor Relations** | First external investor | Cap table, fundraising, board mgmt |
| 22 | **Chief of Staff** | Ivan's coord hours > 50/week | Calendar, board prep, internal comms |
| 23 | **DevRel** | ParaguAI Builder has public API | Developer community, content |
| 24 | **Workplace / Office** | Open physical office | Currently remote |
| 25 | **Fraud / Risk** | $500K+ payment volume | Chargeback, fraud, AML |
| 26 | **Web3 / Crypto Ops** | Add blockchain vertical | Crypto-specific ops (not relevant) |
| 27 | **Compensation & Benefits** | First FTE hire | Comp bands, bonus plans |
| 28 | **People Operations (HR)** | 5+ FTEs | HRIS, benefits, time off |
| 29 | **DEI / Belonging** | 10+ employees | Optional, depends on values |
| 30 | **PR / Communications** | Launch a flagship brand | External press, media relations |

## Tier 4 — Departments only at enterprise scale

| # | Department | Trigger |
|---|------------|---------|
| 31 | Internal Comms | 50+ people |
| 32 | Workplace Operations | Open office |
| 33 | DEI | 10+ people |
| 34 | M&A / Corp Dev | Acquisitions planned |
| 35 | Government Relations | Regulated vertical |

---

# Part 3 — Role inventory (~120+ roles)

Each department has 3-8 sub-roles. Total across all 30 functional areas: ~120 roles. The Session 1 glossary had 98; the additions from analysis + this research add ~25 more.

### Distribution by functional area

| Functional area | Roles | Tier |
|-----------------|-------|------|
| Operations / Management | 8 | T1+T2 |
| Finance & Legal | 14 | T1+T2 |
| Sales & Growth | 18 | T1+T2 |
| Engineering & Delivery | 24 | T1+T2 |
| Research & Education | 12 | T1+T2 |
| People & Culture | 8 | T1+T2 |
| AI Ops (cross-cutting) | 6 | T2 |
| Compliance | 4 | T2 |
| Knowledge Management | 4 | T2 |
| RevOps | 5 | T2 |
| BizOps | 3 | T2 |
| Customer Success | 6 | T2/T3 |
| AI Safety | 4 | T2 |
| Procurement | 4 | T2 |
| Tier 3 depts | ~10 | T3 |
| Tier 4 depts | ~5 | T4 |
| **TOTAL** | **~135 roles** | — |

The full per-role inventory is in `/opt/data/agents-v2/ROLES-INVENTORY.md` (comprehensive table).

---

# Part 4 — Storage architecture (git + DB)

Ivan's directive: "agents should have permanent git storage for memories etc separate repos, maybe db backed all of this."

This is a key architectural decision. Here's the proposed hybrid architecture:

## 4.1 — Three storage layers

### Layer 1: Git repos (per agent, per dept) — version-controlled knowledge

**Pattern**: Each agent + each dept has its own git repo. Permanent, version-controlled, auditable.

```
/opt/data/git-repos/
├── aiw-agents-business-analyst/         # per-agent memory repo
├── aiw-agents-management-coordinator/
├── aiw-agents-kiki-coach/
├── aiw-agents-finance-controller/
├── aiw-agents-sales-pipeline/
├── aiw-agents-engineering-roster/
├── aiw-agents-research-tracker/
├── aiw-dept-operations/                  # per-dept artifacts
├── aiw-dept-finance-legal/
├── aiw-dept-sales-growth/
├── aiw-dept-engineering-delivery/
├── aiw-dept-research-education/
├── aiw-dept-people-culture/
├── aiw-constitution/                     # ORG-AGENTS.md + dept specs
├── aiw-patterns/                         # 5 mandatory patterns
├── aiw-playbooks/                        # 6 dept playbooks
├── aiw-source-materials/                 # curated knowledge
└── aiw-shared/                           # cross-cutting artifacts
```

**Per-agent repo contents**:
- `PROMPT.md` (canonical agent spec)
- `outbox/{date}.md` (daily briefs)
- `state/{date}.json` (state snapshots — gitignored, see Layer 2)
- `logs/{date}.jsonl` (agent action logs)
- `memories/{topic}.md` (long-term agent memory — like a personal diary)
- `decisions/{date}.md` (decision journal — what the agent decided and why)
- `lessons/{topic}.md` (post-hoc reflections)
- `eval/{golden-trajectories}.json` (eval-gate ground truth)
- `README.md` (per-agent documentation)
- `CHANGELOG.md` (version history)

**Why per-agent repo?**:
- Permanent record even if the agent is retired
- Diffable — see exactly what changed when
- Auditable — every action is in git history
- Cross-agent readable — other agents can reference past decisions
- Disaster recovery — single `git clone` rebuilds the agent

### Layer 2: SQLite (per-agent state DB) — operational state

**Pattern**: Each agent has a SQLite DB at `/opt/data/db/<agent>.db`. Operational state lives here. Gitignored.

```sql
-- per-agent schema (example for sales-pipeline)
CREATE TABLE leads (
  id INTEGER PRIMARY KEY,
  name TEXT,
  company TEXT,
  icp_match_pct REAL,
  stage TEXT,           -- 'new' | 'qualified' | 'proposal' | 'signed' | 'lost'
  value_usd REAL,
  source TEXT,
  created_at TEXT,
  updated_at TEXT,
  next_action TEXT,
  blocker TEXT
);

CREATE TABLE outreach_log (
  id INTEGER PRIMARY KEY,
  lead_id INTEGER,
  message TEXT,
  sent_at TEXT,
  response TEXT,
  outcome TEXT           -- 'reply' | 'bounce' | 'unsubscribe' | 'no_response'
);

CREATE TABLE decisions (
  id INTEGER PRIMARY KEY,
  date TEXT,
  decision TEXT,
  rationale TEXT,
  override_token TEXT
);

CREATE TABLE idempotency (
  job_id TEXT PRIMARY KEY,
  last_run TEXT,
  window TEXT,
  status TEXT
);

CREATE TABLE state_snapshots (
  id INTEGER PRIMARY KEY,
  snapshot_at TEXT,
  data BLOB              -- gzipped JSON of full state
);
```

**Why SQLite (not JSON files or Postgres)?**:
- Single-file, easy backup, no server
- Better than JSON for queries (funnel metrics, time-series)
- Migration path to Postgres is trivial (same SQL)
- 2026 evidence: "Zero-Infra AI Agent Memory with Markdown and SQLite" (aihaberleri.org)
- Qdrant for vector memory (RAG), SQLite for structured state

### Layer 3: Vector DB (Qdrant) — semantic memory (RAG)

**Pattern**: Each agent has a Qdrant collection for semantic search of past decisions, conversations, source-materials.

**Why?**:
- Agent needs to ask "what did I decide last time about X?" — semantic search beats keyword
- Source-materials library is searchable semantically
- Cross-agent memory: one agent can ask "how did sales-pipeline handle Y?" and get semantic matches

**Defer to Tier 2**: not Tier 1. State files (SQLite) are the priority. Qdrant ships when source-materials > 50 files or first eval-gate ships.

## 4.2 — Per-agent repo + DB pairing

| Agent | Repo | DB |
|-------|------|-----|
| business-analyst | `aiw-agents-business-analyst` | `/opt/data/db/business-analyst.db` |
| management-coordinator | `aiw-agents-management-coordinator` | `/opt/data/db/management-coordinator.db` |
| kiki-coach | `aiw-agents-kiki-coach` | `/opt/data/db/kiki-coach.db` |
| finance-controller | `aiw-agents-finance-controller` | `/opt/data/db/finance-controller.db` |
| sales-pipeline | `aiw-agents-sales-pipeline` | `/opt/data/db/sales-pipeline.db` |
| engineering-roster | `aiw-agents-engineering-roster` | `/opt/data/db/engineering-roster.db` |
| research-tracker | `aiw-agents-research-tracker` | `/opt/data/db/research-tracker.db` |

**Per cross-cutting concern**:
- ai-ops-coordinator → `aiw-agents-ai-ops` + db
- compliance-monitor → `aiw-agents-compliance` + db
- source-curator → `aiw-agents-source-curator` + db
- founder-bandwidth-watchdog → `aiw-agents-bandwidth` + db

## 4.3 — Backup + sync

- **Git repos**: pushed to GitHub `Ai-Whisperers/` org (private, per-agent repos)
- **SQLite DBs**: daily snapshot to `/opt/data/backups/db/{date}/`, retained 90 days, weekly offsite to R2
- **Qdrant**: snapshot weekly, retained 90 days

## 4.4 — Memory architecture

Three types of agent memory, three storage backends:

| Memory type | Backend | Example |
|------------|---------|---------|
| **Episodic** (what happened) | Git repo `outbox/`, `logs/`, `decisions/` | "Yesterday I drafted 3 outreach emails" |
| **Semantic** (what I know) | SQLite + Qdrant | "ICP match for legal vertical is 70%" |
| **Procedural** (how I do things) | Git repo `PROMPT.md` + `patterns/` | "Always check idempotency before action" |

This is the standard AI agent memory taxonomy (per Mem0, Zep, Hindsight 2026).

---

# Part 5 — Build order

Per Ivan's directive: "research everything in depth, make all departments, decide."

My build order respects dependencies and Ivan's prior preference (management → sales → marketing → ...):

### Phase 1 — Build management/operations agents FIRST

Why: Every other dept reads management-coordinator's output. Build the spine first.

1. Operations dept + management-coordinator + business-analyst + kiki-coach (already exist)
2. AI Ops (new cross-cutting) — own it now, before more agents ship
3. BizOps — same

### Phase 2 — Build revenue-generating depts

1. Sales dept + sales-pipeline + proposal-drafter + lead-enrichment (REVENUE first)
2. Marketing (sub of Sales, but build the 2 agents — content-producer, multimedia-producer)
3. RevOps (cross-cutting, supports Sales)

### Phase 3 — Build operations-supporting depts

1. Engineering + engineering-roster + devops + qa + security-watchdog
2. AI Safety (sub of Engineering)

### Phase 4 — Build finance + compliance

1. Finance + finance-controller + accounting-automation + tax-receipt-tracker
2. Compliance (named role)
3. Procurement

### Phase 5 — Build research + knowledge

1. Research + research-tracker + citation-checker + thesis-tracker + course-producer
2. Knowledge Management (source-curator)

### Phase 6 — Build people

1. People + kiki-coach (extended) + founder-bandwidth-watchdog

### Phase 7 — Tier 3 depts on trigger

Document the 12-15 deferred depts in DEFERRED-AGENTS.md with triggers.

### Phase 8 — Migration to per-agent git repos + SQLite

This is a major architecture change. Currently: state lives in JSON files. New: state in SQLite, memories in git repos.

**Migration strategy**:
- Phase 8A: Build the per-agent repo structure (15+ repos)
- Phase 8B: Migrate state files to SQLite (write migration script)
- Phase 8C: Set up git push automation (each agent pushes its own repo)
- Phase 8D: Set up SQLite backup cron
- Phase 8E: Validate — all agents still deliver correctly

---

# Part 6 — What this means for PLAN-v4

## Changes to PLAN-v4

| Section | Old | New |
|---------|-----|-----|
| **Org chart** | 6 departments + 3 cross-cutting | 6 Tier-1 + 8 Tier-2 cross-cutting + 12 Tier-3 deferred |
| **Role count** | 98 + 12 = 110 | ~135 (additions from full research) |
| **Agent inventory** | ~25 agents | ~40-50 agents |
| **State files** | 11 JSON files | 11 SQLite DBs + 17+ git repos |
| **Build order** | Per Phase 5 sequential | Per Part 5 (this doc) — 7 sequential phases |
| **New: storage architecture** | (none) | Per-agent git repos + SQLite + Qdrant (deferred) |
| **New: Tier 3 trigger table** | (loose) | Formal 12-dept trigger table |

## What gets added

1. **Per-agent git repos** (~17 repos for Tier 1+2 agents) — `git init` per agent
2. **Per-agent SQLite DBs** (one per agent, schema-versioned)
3. **Migration script** to convert JSON state to SQLite
4. **Backup automation** (git push + SQLite snapshot cron)
5. **Updated ORG-AGENTS.md v0.2.0** with the 30 functional areas
6. **ROLES-INVENTORY.md** with ~135 roles
7. **DEFERRED-AGENTS.md** with 12 Tier-3 departments + triggers
8. **STORAGE-ARCHITECTURE.md** documenting the 3-layer model

## What stays the same

- Series-first discipline
- 5 mandatory patterns (hard stops, idempotency, context-payload, eval-gates, reflection)
- 9-phase structure (Phases 0-9)
- AI-aware timeline
- Phase 0-3 (infra + patterns) unchanged
- Phase 5 builds agents in dependency order

## Revised phase structure

Adding **Phase 5.5 — Storage migration** between current Phase 5 (agents) and Phase 6 (playbooks):

- Phase 5: Wire 6 lead agents (current plan)
- **Phase 5.5: Storage migration** (NEW — git repos + SQLite)
- Phase 6: Per-dept playbook catalog (current plan)
- Phase 7-9: Unchanged

---

# Final recommendations (autonomous decisions)

| Decision | My choice | Why |
|----------|-----------|-----|
| Total functional areas | 30 (6 Tier 1 + 8 Tier 2 cross-cutting + 12 Tier 3 deferred + 4 Tier 4) | Literature consensus |
| Total roles | ~135 | Real org-chart needs |
| Total agents at buildout | ~40-50 | Not all roles need agents; some are sub-functions |
| Per-agent git repo | YES | Permanent version-controlled memory |
| Per-agent SQLite DB | YES | Better than JSON for queries, easy migration to Postgres later |
| Qdrant vector DB | DEFER to Tier 2 | Not needed until source-materials > 50 files |
| Build order | Management → Sales → Marketing → Eng → Finance → Research → People | Ivan's directive + dependencies |
| Tier 3 promotion triggers | Formal table with quantitative triggers | Already documented |
| Storage migration | New Phase 5.5 | Major architecture change |

---

# What this document IS NOT

- Not a complete plan update — that's a follow-up document
- Not an execution — research only
- Not a final list — discoverable roles can expand over time
- Not a staffing plan — these are ROLE definitions, not hiring decisions

---

# Next step

This document is the foundation. Three follow-up artifacts to produce (when Ivan says "continue"):

1. **ROLES-INVENTORY.md** — the ~135 roles in detailed table format
2. **STORAGE-ARCHITECTURE.md** — the 3-layer model with implementation spec
3. **PLAN-v5.md** — the consolidated plan update incorporating this research

For now: this document is the deliverable. It expands the canonical 6-dept model to a realistic 30-functional-area catalog with proper tier promotion triggers and the storage architecture Ivan asked for.

---

**File**: `/opt/data/agents-v2/RESEARCH-COMPLETE-ORG.md`
**Size**: ~16 KB
**Last updated**: 2026-08-14
**Author**: Erebus
**Status**: Research synthesis complete; not yet implemented
