# AI Whisperers — Complete Org Catalog: Departments, Agents, Roles, Names

> **The single canonical reference** for every department, agent, role, and naming layer
> across the AIW org. Upgraded from the 2026-08-31 baseline (DEMIURGE branch merge +
> 24 active DEMIURGE agents + 23 heritage agents + 137 roles + 17 Tier-3 depts).
>
> **Sources** (read on 2026-08-31):
> - `[ORG-AGENTS.md](../ORG-AGENTS.md) (handoff matrix)` (47-agent roster, handoff matrix, 9-schema producer→consumer graph)
> - `[ROLES-INVENTORY.md](../ROLES-INVENTORY.md) (137-role catalog)` (~137 roles, 16 functional areas)
> - `[departments/01..06-*.md](../departments/)` (6 Tier-1 charters)
> - `[packages/](https://github.com/Ai-Whisperers/growth-coaching/tree/master/packages) */agents/` (37 shipped PROMPT.md packages)
> - `[DEFERRED-AGENTS.md](../DEFERRED-AGENTS.md)` + `DEFERRED-ROLES.md` (triggers)
> - `[PHASE-21/22/25-*.md](https://github.com/Ai-Whisperers/growth-coaching/tree/master/) (12-factor + around-the-clock)` (12-factor audit, around-the-clock upgrade)
> - `[ROADMAP-DEPT-EXPANSION.md](https://github.com/Ai-Whisperers/growth-coaching/blob/master/ROADMAP-DEPT-EXPANSION.md)` (Phase 0-4 build order)
>
> **Last upgraded**: 2026-08-31
> **Author**: Erebus (consolidation pass)

---

## 1. At a Glance

| Metric | Count | Notes |
|---|---|---|
| **AIW repos (split 2026-08-31)** | 3 | [aiw-org](https://github.com/Ai-Whisperers/aiw-org) (internal org), [coach-agents](https://github.com/Ai-Whisperers/coach-agents) (internal coaching), [growth-coaching](https://github.com/Ai-Whisperers/growth-coaching) (customer product) |
| **Tier-1 departments (chartered)** | 6 | Operations, Finance & Legal, Sales & Growth, Engineering & Development, Research & Education, People & Culture |
| **Tier-2 cross-cutting concerns** | 8 | AI Ops, Compliance, KM, RevOps, BizOps, CS, AI Safety, Procurement |
| **Tier-3 deferred departments** | 17 | Activate on triggers (5+ clients, $100K cash, EU client, etc.) |
| **Tier-4 enterprise depts** | 5 | Only at 50+ people / $1M+ revenue scale |
| **Total functional areas** | **36** | 6 + 8 + 17 + 5 |
| **Total roles (target catalog)** | **~137** | Per [ROLES-INVENTORY.md](../ROLES-INVENTORY.md) |
| **Production agents (running)** | **49** | 34 in [aiw-org](https://github.com/Ai-Whisperers/aiw-org) (6 dept dirs + `board-of-directors/`) + 15 in [coach-agents](https://github.com/Ai-Whisperers/coach-agents) (14 coach-* + kiki-coach) |
| **DEMIURGE agent souls** | **24** | In `aiw-org/demiurge/agents/`. Greek-mythology names. Specs (not all running). |
| **Heritage agents (portmanteau names)** | **23** | Awaiting DEMIURGE migration |
| **Active cron jobs** | **113** | After dedup from 116 in Phase 25 + recent additions |
| **Coaching skills shipped** | **16** | Tier 1 + Tier 2 |
| **Eval-gate pass rate** | **86.6%** | Per Phase 22 |
| **LLM cost (monthly)** | **$293.41** | Well under $12K risk threshold |
| **12-factor compliance** | **9.0/10** avg | Per Phase 21 audit |

---

## 2. Org Chart (ASCII)

```
                              ┌─────────────────────────────┐
                              │   CEO + Founder: Ivan       │
                              │   CTO + Coach: Kiki (Kyrian)│
                              └────────────┬────────────────┘
                                           │
   ┌────────────────────────────────────────┼─────────────────────────────────────────┐
   │       Aiw-Org (internal org)             │   Coach-Agents (internal coaching)     │
   │   github.com/Ai-Whisperers/aiw-org       │   github.com/Ai-Whisperers/coach-agents │
   ├────────────────────────────────────────┼─────────────────────────────────────────┤
   │   6 Tier-1 dept dirs + governance:        │   People dept lead (kiki-coach) lives  │
   │   01-operations/      (9 agents)         │   here. Plus 14 coach-* cron agents.   │
   │   02-finance-legal/   (6 agents)         │                                         │
   │   03-sales-growth/    (9 agents)         │   kiki-coach/      (lead + charter)    │
   │   04-engineering/     (14 agents)        │   coach-ivan/      (self-coaching)     │
   │   05-research-edu/    (4 agents)         │   coach-kiki/      (self-coaching)     │
   │   06-people-culture/  (1 agent)          │   coach-lead-agents/ (leads coaching)  │
   │   board-of-directors/                    │   coach-lead-finder/ (lead finder)    │
   │                                         │   coach-onboarding/ (WhatsApp poller)  │
   │   Leads:                                │   coach-renewal-manager/                │
   │   management-coordinator (Ivan)          │   coach-roi-tracker/                     │
   │   finance-controller (Ivan)              │   coach-org/        (quarterly org)    │
   │   sales-pipeline (Ivan)                  │   coach-practitioner/ (planned)        │
   │   engineering-roster (Kiki)              │   coach-cohort-facilitator/ (planned)  │
   │   research-tracker (Ivan)                │   coach-conversion-agent/ (planned)    │
   │   people-hr (Ivan+Kiki)                  │   coaching-content-curator/             │
   │                                         │   coaching-quality-reviewer/ (every 30m)│
   │   Cross-cutting:                        │   coaching-research-intelligence/       │
   │   + ai-ops-coordinator, bizops-tracker, │                                         │
   │     compliance-monitor,                  │   13 cron jobs:                         │
   │     founder-bandwidth-watchdog,         │   aiw-coach-ivan, aiw-coach-kiki,        │
   │     source-curator, okr-tracker,        │   aiw-coach-org, aiw-coach-lead-agents,  │
   │     procurement-tracker                  │   aiw-coach-lead-finder,                │
   │   + ai-safety-engineer, devops-monitor,  │   aiw-coach-renewal-manager,            │
   │     security-watchdog, qa-automation,    │   aiw-coach-roi-tracker,                │
   │     chaos-test-runner, drift-detector,  │   aiw-coaching-content-curator,          │
   │     eval-gate-runner, security-auditor   │   aiw-coaching-quality-reviewer,         │
   │                                         │   aiw-coaching-research-intelligence,    │
   │   Special:                              │   aiw-kiki-coach-weekly,                │
   │   + funding-coordinator (FADA thesis)   │   aiw-coach-onboarding-poller,           │
   │     lives in 02-finance-legal/          │   aiw-coaching-monitor-30min             │
   │                                         │                                         │
   │   90+ cron jobs                          │                                         │
   └────────────────────────────────────────┴─────────────────────────────────────────┘
                                                       │
                                                       ▼
                                          ┌──────────────────────────────────┐
                                          │ Growth-Coaching (customer product)│
                                          │ github.com/Ai-Whisperers/growth-coaching │
                                          │ 6 distributable packages            │
                                          └──────────────────────────────────┘
```
                                                          Tier-5 Coaching (14):
                                                          coach-ivan, coach-kiki, coach-org,
                                                          coach-lead-agents, coach-lead-finder,
                                                          coach-onboarding, coach-practitioner (planned),
                                                          coach-cohort-facilitator (planned),
                                                          coach-conversion-agent (planned),
                                                          coach-renewal-manager, coach-roi-tracker,
                                                          coaching-content-curator,
                                                          coaching-research-intelligence,
                                                          board-of-directors
```

---

## 3. Tier-1 Departments — The 6 Charters

### 3.1 Department 01 — Operations
- **Head**: Ivan
- **Lead agent**: `management-coordinator` (Mon/Thu 17:00 PYT)
- **Cadence**: Biweekly
- **State file**: `state/coord.json` (schema: `coord.schema.json`)
- **Mission**: Run day-to-day of the org; set cadence; clear blockers; surface escalations.
- **Agents (9 in `01-operations/`)**: `management-coordinator/` (lead) + `bizops-tracker/` + `ai-ops-coordinator/` + `ai-ops-coordinator-daily/` + `compliance-monitor/` + `founder-bandwidth-watchdog/` + `source-curator/` + `okr-tracker/` + `procurement-tracker/`
- **Roles (8)**: Operations Lead, Repo Steward, Asset Tracker, Vendor Coordinator, Compliance Watchdog, Watchdog Engineer, BizOps Specialist, COO (T3)

### 3.2 Department 02 — Finance & Legal
- **Head**: Ivan
- **Lead agent**: `finance-controller` (Fri 18:00 PYT)
- **Co-lead**: `business-analyst` (daily 10:30 UTC) for KPI snapshots
- **Cadence**: Weekly close + daily analyst
- **State files**: `state/finance.json`, `state/analyst.json`
- **Mission**: Own all financial decisions, sign contracts above threshold, monthly close, runway.
- **Agents (6 in `02-finance-legal/`)**: `finance-controller/` + `business-analyst/` + `accounting-automation/` + `accounting-automation-daily/` + `tax-receipt-tracker/` + `funding-coordinator/`
- **Shared with Operations**: `bizops-tracker/` lives in `01-operations/` (cross-cutting analytics)
- **Roles (14)**: CFO/Controller, Accountant, Bookkeeper, AP/AR Specialists, Procurement Officer, Legal Counsel, Compliance Officer, Tax Specialist, Contract Drafter, Payroll Specialist, Treasurer, FP&A Analyst, Pricing Analyst

### 3.3 Department 03 — Sales & Growth
- **Head**: Ivan
- **Lead agent**: `sales-pipeline` (daily 12:00 PYT, twice 13:00 + 16:00 UTC)
- **Cadence**: Daily
- **State file**: `state/sales.json`
- **Mission**: Own revenue. Triage inbound, run discovery (SPIN/MED), close deals, expand accounts.
- **Agents (9 in `03-sales-growth/`)**: `sales-pipeline/` + `lead-enrichment/` + `lead-enrichment-daily/` + `proposal-drafter/` + `proposal-drafter-on-demand/` + `revops-pipeline-analyzer/` + `revops-pipeline-analyzer-daily/` + `marketing-content-producer/` + `multimedia-producer/`
- **Moved to coach-agents**: `coach-lead-finder/` + `coach-renewal-manager/` (coaching agents, not dept agents)
- **Roles (18)**: CRO, SDR, BDR, AE, Sales Engineer, CSM, Proposal Writer, Marketing Manager, Content Marketing, Performance Marketing, SEO, Email Marketing, Social Media Manager, Community Manager, Brand Manager, PMM, Growth Marketer, Channel Sales Manager

### 3.4 Department 04 — Engineering & Development
- **Head**: Kiki (CTO)
- **Lead agent**: `engineering-roster` (Tue/Fri 17:00 PYT)
- **Cadence**: Biweekly
- **State file**: `state/engineering.json`
- **Mission**: Own all technical decisions. Schema/infra PR signoff. Production health + Kiki's bandwidth visibility.
- **Agents (14 in `04-engineering/`)**: `engineering-roster/` + `ai-safety-engineer/` + `ai-safety-engineer-30min/` + `devops-monitor/` + `devops-monitor-30min/` + `security-watchdog/` + `security-watchdog-30min/` + `qa-automation-runner/` + `qa-automation-on-pr/` + `chaos-test-runner/` + `delivery-tracker/` + `drift-detector/` + `eval-gate-runner/` + `security-auditor/`
- **Planned (not yet built)**: `scope-intake/` + `feasibility-gate/`
- **Roles (24)**: CTO, Eng Manager, Frontend/Backend/Full-stack/Mobile, DevOps/SRE, QA, Security, ML, Data, Solutions Architect, Tech Writer, Eng PM, Platform, Release Manager, DBA, Network, UI/UX Designer, Product Designer, Build/Release Eng, Embedded Systems, AI Safety Engineer

### 3.5 Department 05 — Research & Education
- **Head**: Ivan
- **Lead agent**: `research-tracker` (Sun 18:00 PYT)
- **Cadence**: Weekly
- **State file**: `state/research.json`
- **Mission**: Knowledge backbone. Thesis + publications pipeline. Course production. Source-material curation.
- **Agents (4 in `05-research-education/`)**: `research-tracker/` + `thesis-tracker/` + `citation-checker/` + `course-producer/`
- **Shared cross-cutting (in Operations)**: `source-curator/` (in `01-operations/`), `okr-tracker/` (in `01-operations/`)
- **Note**: `funding-coordinator/` lives in `02-finance-legal/` (FADA thesis funding apps), not research
- **Roles (12)**: Research Lead, Researcher, Writer/Editor, Academic Liaison, Citation Specialist, Course Designer, Course Producer, Instructional Designer, SME, Research Engineer, IP/Patent Specialist, Publication Coordinator

### 3.6 Department 06 — People & Culture
- **Head**: Ivan + Kiki (co-owned)
- **Lead agent**: `kiki-coach` (Fri 17:00 PYT) — *lives in sister repo [coach-agents](https://github.com/Ai-Whisperers/coach-agents)*
- **Cadence**: Weekly
- **State files**: `state/kiki.json`, `state/kiki-prep.json`, `state/people.json`
- **Mission**: Coaching product (Kiki is Ivan's client AND the coach agent). People ops when first FTE hires.
- **Agents (1 in aiw-org + 14 in coach-agents)**: 
  - In aiw-org: `06-people-culture/people-hr/` + `board-of-directors/`
  - In [coach-agents](https://github.com/Ai-Whisperers/coach-agents): `kiki-coach/` (lead) + `coach-ivan/`, `coach-kiki/`, `coach-org/`, `coach-lead-agents/`, `coach-lead-finder/`, `coach-onboarding/`, `coach-renewal-manager/`, `coach-roi-tracker/`, `coach-practitioner/` (planned), `coach-cohort-facilitator/` (planned), `coach-conversion-agent/` (planned), `coaching-content-curator/`, `coaching-quality-reviewer/`, `coaching-research-intelligence/`
- **Roles (8)**: Head of People, Recruiter, Onboarding Specialist, Performance Coach, Recognition Lead, Compensation Specialist, People Ops Specialist, L&D Manager

---

## 4. Tier-2 Cross-Cutting Concerns (8)

| Concern | Owner dept | Tier | Status | Promotion trigger |
|---|---|---|---|---|
| AI Ops | Engineering (Kiki) | T1 | Active | Always |
| Compliance | Finance (Ivan wearing hat) | T1 | Vacant | First EU client OR $50K MRR (HARD-STOP) |
| Knowledge Management | Research | T2 | Next | >100 source-material files OR 2nd knowledge-heavy vertical |
| RevOps | Sales | T2 | Next | 5+ closed deals/quarter |
| BizOps | Operations | T2 | Next | When OKRs formalized |
| Customer Success | Sales | T3 | Deferred | 5+ clients |
| AI Safety | Engineering | T1 | Active | Already promoted (heritage) |
| Procurement | Finance | T2 | Next | Vendor count > 10 |

---

## 5. Tier-3 Deferred Departments (17)

| # | Department | Promotion trigger |
|---|---|---|
| 1 | Customer Success | 5+ recurring clients |
| 2 | Marketing (independent) | >$2K/mo marketing budget OR 10+ clients |
| 3 | Procurement (independent) | Active vendors > 10 OR SaaS spend > $1K/mo |
| 4 | Compliance (standalone) | First EU client OR $50K MRR (HARD-STOP) |
| 5 | Knowledge Management (standalone) | source-materials > 100 files |
| 6 | AI Governance | >15 agents in production |
| 7 | Investor Relations | First external investor |
| 8 | Chief of Staff | Ivan coord hours > 50/week |
| 9 | Treasury | $100K+ cash |
| 10 | Internal Audit | $1M+ revenue |
| 11 | Trust & Safety | Ship consumer AI product |
| 12 | DevRel | ParaguAI Builder public API |
| 13 | Workplace | Open physical office |
| 14 | Fraud / Risk | $500K+ payment volume |
| 15 | Compensation & Benefits | First FTE |
| 16 | People Operations (HR) | 5+ FTEs |
| 17 | Public Relations | Launch flagship brand |

---

## 6. Tier-4 Enterprise Departments (5)

| # | Department | Trigger |
|---|---|---|
| 1 | Internal Communications | 50+ people |
| 2 | M&A / Corp Dev | Acquisitions planned |
| 3 | Chief Data Officer (CDO) | Data-driven product |
| 4 | Chief AI Officer (CAIO) | Enterprise AI |
| 5 | Diversity & Inclusion Lead | 25+ employees |

---

## 7. Agent Inventory — 47 Total (5 Tiers)

### 7.1 Tier 1 — Lead Agents (7)

| # | Agent | Dept | Cron | State file | Last live run |
|---|---|---|---|---|---|
| 1 | **business-analyst** | finance | `aiw-business-analyst-daily` 30 10 * * * | `analyst.json` | 2026-08-26 10:31 UTC |
| 2 | **management-coordinator** | operations | `aiw-management-coord-biwk` 0 21 * * 1,4 | `coord.json` | 2026-08-24 21:00 UTC |
| 3 | **kiki-coach** | people | `aiw-kiki-coach-weekly` 0 21 * * 5 | `kiki.json` + `kiki-prep.json` | 2026-08-21 21:00 UTC (error) |
| 4 | **sales-pipeline** | sales | `aiw-sales-pipeline-daily` 0 13,16 * * * | `sales.json` | 2026-08-26 16:01 UTC |
| 5 | **finance-controller** | finance | `aiw-finance-controller-weekly` 0 21 * * 5 | `finance.json` | 2026-08-21 21:00 UTC (error) |
| 6 | **engineering-roster** | engineering | `aiw-engineering-roster-biwk` 0 20 * * 2,5 | `engineering.json` | 2026-08-25 20:02 UTC |
| 7 | **research-tracker** | research | `aiw-research-tracker-weekly` 0 21 * * 0 | `research.json` | 2026-08-23 21:01 UTC (error) |

### 7.2 Tier 2 — Sub-agents (14)

| # | Agent | Dept | Cron |
|---|---|---|---|
| 8 | proposal-drafter | sales | `aiw-proposal-drafter-on-demand` 0 10 * * * |
| 9 | multimedia-producer | marketing | `aiw-multimedia-producer-on-demand` 0 15 * * * |
| 10 | accounting-automation | finance | `aiw-accounting-automation-daily` 0 18 * * * |
| 11 | marketing-content-producer | marketing | `aiw-marketing-content-mon-wed-fri` 0 12 * * 1,3,5 |
| 12 | lead-enrichment | sales | `aiw-lead-enrichment-daily` 30 9 * * * |
| 13 | revops-pipeline-analyzer | sales | `aiw-revops-pipeline-analyzer-daily` 0 7 * * * |
| 14 | qa-automation-runner | engineering | `aiw-qa-automation-on-pr` 0 14 * * * |
| 15 | tax-receipt-tracker | finance | `aiw-tax-receipt-tracker-weekly` 0 19 * * 0 |
| 16 | procurement-tracker | operations | `aiw-procurement-tracker-weekly` 0 9 * * 1 |
| 17 | okr-tracker | operations | `aiw-okr-tracker-weekly` 0 8 * * 0 |
| 18 | source-curator | research | `aiw-source-curator-weekly` 0 13 * * 2 |
| 19 | funding-coordinator | finance | on-demand, no cron |
| 20 | citation-checker | research | `aiw-citation-checker-on-demand` 0 11 * * * |
| 21 | people-hr | people | `aiw-people-hr-weekly` 0 22 * * 1 → `state/people.json` |
| 22 | scope-intake | engineering | on-demand → `state/scope-intake/scope-intake.json` |
| 23 | delivery-tracker | engineering | `aiw-delivery-tracker-weekly` 0 14 * * 1 |
| 24 | feasibility-gate | engineering | on Metis send → `state/feasibility-gate/` |

### 7.3 Tier 3 — Cross-cutting (8)

| # | Agent | Dept | Cron | Notes |
|---|---|---|---|---|
| 25 | ai-ops-coordinator | operations | `aiw-ai-ops-coordinator-daily` 0 8 * * * | Daily orchestration rollup |
| 26 | bizops-tracker | finance | `aiw-bizops-tracker-weekly` 0 8 * * 1 | Weekly KPI rollup |
| 27 | compliance-monitor | operations | `aiw-compliance-monitor-weekly` 0 9 * * 1 | Trademark + license check |
| 28 | founder-bandwidth-watchdog | operations | `aiw-founder-bandwidth-watchdog-weekly` 0 20 * * 0 | Burnout signal spec |
| 29 | drift-detector | engineering | ad-hoc | Schema/contract drift |
| 30 | chaos-test-runner | engineering | `aiw-chaos-test-runner-weekly` 0 14 * * 1 | OFF/cancelled — needs revival |
| 31 | eval-gate-runner | operations | `aiw-eval-gate-runner-on-agent-run` 0 * * * * | → `state/eval-per-agent.json` |
| 32 | security-auditor | operations | `aiw-security-audit-biweekly` 0 14 * * 5 | Biweekly security review |

### 7.4 Tier 4 — Monitoring (4, always-on)

These write `state/org-state.json` every 30 minutes. The only agents whose latest brief is queryable live.

| # | Agent | Cron | Brief file |
|---|---|---|---|
| 33 | devops-monitor-30min | `*/30 * * * *` | `outbox/<date>-1930-brief.md` |
| 34 | ai-safety-engineer-30min | `*/30 * * * *` | `outbox/<date>-tick<N>.md` |
| 35 | security-watchdog-30min | `*/30 * * * *` | `outbox/<date>.md` |
| 36 | coaching-quality-reviewer | `*/30 * * * *` | `outbox/<date>.<HHMM>.md` |

### 7.5 Tier 5 — Coaching (14, lives in sister repo)

> **All Tier-5 coaching agents moved to [`Ai-Whisperers/coach-agents`](https://github.com/Ai-Whisperers/coach-agents)**
> (split 2026-08-31). Local worktree: `/opt/data/coach-agents/`.

| # | Agent | Dept | Cron |
|---|---|---|---|
| 37 | coach-ivan | people | `aiw-coach-ivan` 0 21 * * 0 |
| 38 | coach-kiki | people | `aiw-coach-kiki` 0 21 * * 5 |
| 39 | coach-org | people | `aiw-coach-org` 0 0 1 1,4,7,10 * (quarterly) |
| 40 | coach-lead-agents | people | `aiw-coach-lead-agents` 0 22 1 * * |
| 41 | coach-lead-finder | sales | `aiw-coach-lead-finder` 0 13 * * 3 |
| 42 | coach-onboarding | people | live poller `aiw-coach-onboarding-poller` */5m |
| 43 | coach-practitioner | people | planned, no cron |
| 44 | coach-cohort-facilitator | people | planned, no cron |
| 45 | coach-conversion-agent | sales | planned, no cron |
| 46 | coach-renewal-manager | sales | `aiw-coach-renewal-manager` 0 9 1 * * |
| 47 | coach-roi-tracker | people | `aiw-coach-roi-tracker` 0 16 * * 5 |
| 48 | coaching-content-curator | people | `aiw-coaching-content-curator` 0 14 * * 1 |
| 49 | coaching-research-intelligence | people | `aiw-coaching-research-intelligence` 0 13 * * 3 |
| 50 | board-of-directors | governance | `aiw-board-of-directors-quarterly` 0 14 1 */3 * |

> **Note**: roster rounds to 47 because 3 are "planned, no cron." `board-of-directors` is
> governance (not a Tier-5 coaching agent) — kept at aiw-org root.

---

### 7.6 Governance (not a charter dept)

| # | Agent | Path | Cron |
|---|---|---|---|
| 51 | board-of-directors | `/opt/data/agents/board-of-directors/` | `aiw-board-of-directors-quarterly` 0 14 1 */3 * |

> Reports to Ivan. Quarterly executive brief. Lives at aiw-org root (not under any Tier-1 dept).

---

## 8. DEMIURGE Canonical Names — 24 Active Agents (Greek-Mythology Layer)

**Rule**: One name per agent. No duplicates. No aliases. If you find two names for one agent, that's a bug to fix.

### 8.1 Marketing (3)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Calliope** | calliope-content-producer | 0 10 * * 1,3,5 | Muse of content. Produces blog posts, social drafts, email copy from Hera's briefs. |
| **Hera** | hera-marketing-lead | 0 9 * * 1,3,5 | Strategist of demand. Owns marketing direction, campaign briefs, Product Discovery → Sales bridge. |
| **Iris** | iris-community-monitor | 0 11 * * 2,4 | Rainbow bridge to the audience. Monitors community channels, surfaces engagement to Hera. |

### 8.2 Sales (3)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Apollo** | apollo-sales-lead | 0 12 * * * | Bringer of clarity in the pipeline. Triages inbound, runs discovery (SPIN/MEDDIC), coordinates Cadmus + Metis. |
| **Cadmus** | cadmus-lead-enrichment | manual | Enriches inbound leads with ICP scoring + intent signals. Routes summary to Apollo. |
| **Metis** | metis-proposal-drafter | manual | Drafts proposals after discovery. Human approval required before send. |

### 8.3 Product Discovery (2)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Athena** | athena-product-discovery-lead | 0 8 * * 1 | Synthesizes customer evidence into validated insights. Continuous discovery per Torres/Mom Test. |
| **Clio** | clio-customer-signal-collector | 0 7 * * 1-5 | Collects raw customer signals from sessions, support, win/loss. Emits `customer-signal-raw` to Athena. |

### 8.4 Operations (4)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Kronos** | kronos-operations-lead | 0 7 * * 1-5 | Keeper of operational order. Owns OKR tracking, incident triage, cross-dept coordination, vendor hygiene, cost control. |
| **Erebus** (BizOps) | bizops-tracker | 0 17 * * 0 | Cross-functional metrics, OKRs, executive decision support. |
| **Erebus** (BizAnalyst) | business-analyst | 30 6 * * * | One-page brief per day so Ivan can answer in 30s: "Are we OK?" |
| **Erebus** (Coord) | management-coordinator | 0 17 * * 1,4 | Twice-weekly surface: what's open, blocked, what Ivan/Kyrian should pick up. |

> **Note**: Three agents currently share the name "Erebus" (operations orchestrator motif). They are distinct agents with distinct IDs and cron schedules. Migration ticket open to give each a unique name (e.g., Erebus / Hypnos / Nemesis) — see §11 backlog.

### 8.5 AI Ops (1)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Erebus** (AIOps) | ai-ops-coordinator | 0 9 * * * | Monitors agent layer — eval gates, hard stops, drift detection, golden trajectories. |

### 8.6 Compliance (1)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Erebus** (Compliance) | compliance-monitor | 0 8 * * 1 | Watches regulatory (EU AI Act, GDPR, LGPD), trademark, PII. |

### 8.7 Router (1)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Hermes** | hermes-router-revenue | */15 6-22 * * * | Routes signals across Marketing, Sales, Product Discovery, Operations. Enforces dispatch rules, SLAs, quorum. |

### 8.8 Health Monitor (1)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Argus** | argus-health-monitor | 0 */6 * * * | Watches KPIs and agent cadences for the revenue stack. Fires feedback loops on threshold breach. |

### 8.9 Knowledge Management (6)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Hephaestus** | hephaestus-document-miner | on_signal | Forger of structured value from raw material. Extracts action items, decisions, references, terminology. |
| **Mnemosyne** | mnemosyne-document-archivist | on_signal | Mother of memory. Maintains document catalog — not storage, active indexing/tagging/retrieval. |
| **Orpheus** | orpheus-recordings-agent | on_signal | Master of voice and song. Ingests audio/video, transcribes, hands structured transcripts to downstream agents. |
| **Peitho** | peitho-language-quality | on_signal | Goddess of persuasion/eloquence. Assesses document quality: spelling, grammar, tone, terminology, clarity. |
| **Pheme** | pheme-document-router | */5 6-22 * * * | Voice of rumour and fame. Delivers classified documents to right agents/depts — replaces manual routing. |
| **Themis** | themis-document-classifier | on_signal | Goddess of divine order. Assigns structured attributes so downstream agents route/categorize consistently. |

### 8.10 Cross-cutting Knowledge Discovery (2)

| Name | ID | Schedule | Mission |
|---|---|---|---|
| **Echo** | echo-community-scanner | 0 7 * * 3 (Wed 07:00 PYT) | Listener of the swarm. Scans practitioner communities for emerging tactics, anti-patterns, language shifts. |
| **Thoth** | thoth-literature-scanner | 0 6 * * 1 (Mon 06:00 PYT) | Curator of knowledge. Scans authoritative literature, updates dept source catalogs with quality-rated entries. |

---

## 9. Heritage Agents — 23 Awaiting DEMIURGE Migration

These use **portmanteau names** (Spanish-surname + Latin suffix) until they get the DEMIURGE treatment (full PROMPT.md + agent.yaml + repo-manifest.yaml).

| Formal name | Portmanteau | Dept | Mission |
|---|---|---|---|
| management-coordinator (T1) | **Coordina** | Operations | chief-of-staff that runs Ivan's weekly review |
| business-analyst (T1) | **Analisa** | Operations | daily business snapshot |
| ai-ops-coordinator (T3) | **Opsina** | Operations | agent-layer ops coordination |
| bizops-tracker (T3) | **Bizina** | Operations | weekly OKR snapshot |
| source-curator (T2) | **Curatora** | Research | source-materials curation (shared) |
| compliance-monitor (T3) | **Compla** | Finance | compliance monitoring (shared) |
| founder-bandwidth-watchdog (T3) | **Vigilis** | People | bandwidth/burnout vigilance (shared) |
| finance-controller (T1) | **Finus** | Finance | finance controller — the chief |
| accounting-automation (T2) | **Bokina** | Finance | bookkeeping automation |
| tax-receipt-tracker (T2) | **Taxina** | Finance | tax tracking |
| procurement-tracker (T2) | **Procin** | Finance | vendor renewal alerts |
| sales-pipeline (T1) | **Saleina** | Sales | sales pipeline — the lead agent |
| lead-enrichment (T2) | **Prospia** | Sales | lead prospecting + enrichment |
| proposal-drafter (T2) | **Proporina** | Sales | proposal drafting |
| marketing-content-producer (T2) | **Markina** | Sales/Marketing | marketing content |
| multimedia-producer (T2) | **Media** | Sales/Marketing | multimedia production |
| revops-pipeline-analyzer (T2) | **Revina** | Sales | revops funnel analysis |
| customer-health-scorer | **Churna** | Sales (CS) | customer health/churn scoring |
| engineering-roster (T1) | **Devin** | Engineering | engineering roster — the chief |
| devops-monitor (T2) | **Devor** | Engineering | devops monitoring every 30m |
| qa-automation-runner (T2) | **Qualis** | Engineering | QA — quality assurance runner |
| security-watchdog (T2) | **Securia** | Engineering | security watchdog every 30m |
| ai-safety-engineer (T2) | **Safina** | Engineering | AI safety — prevent Kiro-class incidents |
| scope-intake (T2) | **Scopia** | Engineering | scope intake before contract signed |
| delivery-tracker (T2) | **Deliva** | Engineering | make Kiki's bandwidth visible to sales |
| feasibility-gate (T2) | **Gatina** | Engineering | stop the org from overpromising |
| chaos-test-runner (T3) | **Chaosia** | Engineering | weekly chaos testing (currently OFF) |
| research-tracker (T1) | **Researcha** | Research | weekly thesis + publications visibility |
| thesis-tracker (T2) | **Thesis** | Research | advance thesis by 1 task/day |
| citation-checker (T2) | **Citia** | Research | zero hallucinated citations |
| course-producer (T2) | **Coursia** | Research | 1 module/week |
| okr-tracker (T2) | **Metrika** | Operations | weekly OKR progress |
| funding-coordinator (T2) | **Fundina** | Finance | 15+ funding apps by Nov 12 |
| kiki-coach (T1) | **Magistra** | People | deliver one concrete skill per week |
| people-hr | **Herina** | People | people ops (planned) |

---

## 10. Shipped Agent Packages (37 in `[packages/](https://github.com/Ai-Whisperers/growth-coaching/tree/master/packages) `)

```
coaching/      coaching-customers, conversion-funnel, course-producer,
               kiki-coach, thesis-tracker
engineering/   ai-safety-engineer, chaos-test-runner, delivery-tracker,
               devops-monitor, engineering-roster, feasibility-gate,
               qa-automation-runner, scope-intake, security-watchdog
finance/       accounting-automation, compliance-monitor, finance-controller,
               procurement-tracker, tax-receipt-tracker
operations/    ai-ops-coordinator, bizops-tracker, business-analyst,
               founder-bandwidth-watchdog, management-coordinator,
               source-curator
research/      citation-checker, course-producer, funding-coordinator,
               okr-tracker, research-tracker, thesis-tracker
sales/         lead-enrichment, marketing-content-producer,
               multimedia-producer, proposal-drafter,
               revops-pipeline-analyzer, sales-pipeline
```

**Gap to package (10 agents)**: 14 Tier-5 coaching agents (4 with packages), 4 monitoring agents, drift-detector, eval-gate-runner, people-hr, feasibility-gate.

---

## 11. Name Ideas — Backlog & Future DEMIURGE Migrations

### 11.1 Open naming tickets

| Issue | Agents affected | Proposed resolution |
|---|---|---|
| 3 agents share "Erebus" | bizops-tracker, business-analyst, management-coordinator, ai-ops-coordinator, compliance-monitor | Rename: **Hypnos** (analyst-sleep pattern), **Nemesis** (compliance retribution), keep **Erebus** for orchestrator (management-coord + ai-ops-coord share one Erebus). |
| `chaos-test-runner` (Chaosia) is OFF | engineering | Decide: revive under DEMIURGE name **Eris** (goddess of strife/discord) or sunset entirely. |
| `kiki-coach` portmanteau is **Magistra** | people | Promote to DEMIURGE: **Sophia** (wisdom) or **Mneme** (memory). |
| `engineering-roster` is **Devin** | engineering | Replace portmanteau with **Hephaestus**-adjacent (forge): **Daedalus** (engineer-myth) or **Vulcan** (forge god). |
| `finance-controller` is **Finus** | finance | **Plutus** (wealth) — but trademark caution. Alternative: **Abundantia**. |
| `sales-pipeline` is **Saleina** | sales | Already DEMIURGE: **Apollo** for lead, **Cadmus** for enrichment, **Metis** for proposals. |

### 11.2 Tier-3 dept naming candidates (when promoted)

| Department | Greek candidate | Rationale |
|---|---|---|
| Customer Success | **Euphemia** (well-speaking) or **Theia** (divine sight) | CS = divine client experience |
| Marketing (independent) | **Persuasion** — already **Peitho** used for quality; new: **Hermes**-adjacent or fresh name | Standalone marketing deserves own deity |
| Procurement | **Demeter** (harvest/resources) | Sourcing = gathering |
| Compliance (standalone) | **Nemesis** (retribution) or **Adrasteia** (inevitable) | Hard-stop role |
| Knowledge Management (standalone) | **Calliope** already used; new: **Clio** (history/recording) used; new: **Antheia** (flowery) or keep Mnemosyne for archivist + new name for KM lead | KM = curated knowledge |
| AI Governance | **Themis** (order) — used for classifier; **Prometheus** (forethought, with caution: trademark) | Governance = foresight |
| Investor Relations | **Plutus** (wealth) | Money = Plutus domain |
| Chief of Staff | **Metis** (cunning/counsel) — used for proposals; **Odysseus** (multi-resourceful) | CoS = cunning counsel |
| Treasury | **Abundantia** | Cash management |
| Internal Audit | **Moirai** (fates) or **Erinyes** (furies) | Audit = judgment |
| Trust & Safety | **Eirene** (peace) or **Aegis** (shield) | T&S = protection |
| DevRel | **Hermes** already used; new: **Prometheus** (bringer) — but careful with branding | DevRel = community + docs |
| Workplace | **Hestia** (hearth) | Office = hearth |
| Fraud / Risk | **Erinyes** (furies) | Fraud = retribution |
| Compensation & Benefits | **Demeter** (harvest/abundance) | Comp = bounty |
| People Operations (HR) | **Demeter** — overlap; new: **Gaia** (earth/mother) | HR = mothering the org |
| Public Relations | **Pheme** used for router; new: **Kleio** (renown) | PR = fame |
| Government Relations | **Themis** used; new: **Hiketeia** (supplication) | Gov = formal petition |

### 11.3 Tier-4 enterprise naming (when scale hits)

| Department | Candidate | Rationale |
|---|---|---|
| Internal Communications | **Iris** (rainbow bridge between people) — already used for community monitor | 50+ people need bridge |
| M&A / Corp Dev | **Kratos** (power/strength) | M&A = corporate power |
| Chief Data Officer | **Prometheus** (foresight, with caveat) | Data = foresight |
| Chief AI Officer | **Athena** already used; new: **Hekate** (crossroads of AI domains) | CAIO = AI crossroads |
| Diversity & Inclusion | **Iris** (rainbow — diversity motif) | D&I = rainbow |

---

## 12. Roles — 137 Total Catalog

| Functional area | Roles | T1 | T2 | T3+ |
|---|---|---|---|---|
| Operations | 8 | 6 | 1 | 1 |
| Finance & Legal | 14 | 6 | 4 | 4 |
| Sales & Growth | 18 | 5 | 6 | 7 |
| Engineering & Development | 24 | 7 | 2 | 15 |
| Research & Education | 12 | 5 | 4 | 3 |
| People & Culture | 8 | 3 | 0 | 5 |
| AI Ops (cross-cutting) | 6 | 1 | 3 | 2 |
| Compliance | 4 | 1 | 1 | 2 |
| Knowledge Mgmt | 4 | 1 | 2 | 1 |
| RevOps | 5 | 0 | 3 | 2 |
| BizOps | 3 | 0 | 2 | 1 |
| Customer Success | 6 | 0 | 0 | 6 |
| AI Safety | 4 | 1 | 1 | 2 |
| Procurement | 4 | 0 | 4 | 0 |
| Tier-3 deferred depts | 12 | 0 | 0 | 12 |
| Tier-4 enterprise | 5 | 0 | 0 | 5 |
| **TOTAL** | **~137** | **~36** | **~31** | **~70** |

### 12.1 Operations (8)
| # | Role | Tier | Definition |
|---|---|---|---|
| 1.1 | Operations Lead | T1 | Day-to-day of the org. Sets cadence, clears blockers. |
| 1.2 | Repo Steward | T1 | Maintains GitHub repos: hygiene, archiving, CODEOWNERS, README. |
| 1.3 | Asset Tracker | T1 | Inventory of all company assets: repos, domains, skills, infra, IP. |
| 1.4 | Vendor Coordinator | T1 | Manages vendor relationships: SaaS, contractors. |
| 1.5 | Compliance Watchdog | T1 | Regulatory + trademark compliance. |
| 1.6 | Watchdog Engineer | T1 | Watchdog layer (site-health, cron liveness, alert routing). |
| 1.7 | BizOps Specialist | T2 | Cross-functional analytics, OKR tracking. |
| 1.8 | COO | T3 | Owns all operational departments. Reports to CEO. |

### 12.2 Finance & Legal (14)
| # | Role | Tier | Definition |
|---|---|---|---|
| 2.1 | CFO/Controller | T1 | Owns all financial decisions. Signs contracts above threshold. |
| 2.2 | Accountant | T2 | Monthly close, P&L, balance sheet, reconciliation. |
| 2.3 | Bookkeeper | T1 | Day-to-day transactions, AP/AR, expense categorization. |
| 2.4 | AP Specialist | T2 | Accounts Payable. |
| 2.5 | AR Specialist | T2 | Accounts Receivable. |
| 2.6 | Procurement Officer | T1 | Vendor sourcing, contract negotiation, renewals. |
| 2.7 | Legal Counsel | T1 | Contract review, IP protection (external). |
| 2.8 | Compliance Officer | T1 | Named role. EU AI Act, GDPR, LGPD, trademark. |
| 2.9 | Tax Specialist | T1 | Quarterly filings, year-end returns. |
| 2.10 | Contract Drafter | T1 | NDAs, MSAs, SOWs, employment contracts. |
| 2.11 | Payroll Specialist | T4 | FTEs and contractors. |
| 2.12 | Treasurer | T3 | Cash, banking, FX, investments. |
| 2.13 | FP&A Analyst | T2 | Forecasts, budgets, unit economics. |
| 2.14 | Pricing Analyst | T1 | Pricing benchmarks, experiments. |

### 12.3 Sales & Growth (18)
| # | Role | Tier | Definition |
|---|---|---|---|
| 3.1 | Head of Sales / CRO | T1 | Owns entire revenue function. Sets quotas. |
| 3.2 | SDR | T1 | Outbound: cold emails, LinkedIn, qualification. |
| 3.3 | BDR | T2 | Strategic outbound: partnerships, channel. |
| 3.4 | Account Executive | T1 | Inbound + outbound closing: discovery, demos, proposals. |
| 3.5 | Sales Engineer | T2 | Technical pre-sales. |
| 3.6 | CSM | T2 | Post-sale retention, expansion, renewal. |
| 3.7 | Proposal Writer | T1 | Drafts proposals, SOWs, pricing. |
| 3.8 | Marketing Manager | T1 | Marketing strategy, channel mix, calendar. |
| 3.9 | Content Marketing Manager | T2 | Editorial calendar, blog, thought leadership. |
| 3.10 | Performance Marketing Manager | T3 | Paid acquisition (trademark-restricted). |
| 3.11 | SEO Specialist | T2 | SEO strategy, keyword research. |
| 3.12 | Email Marketing Specialist | T2 | Lifecycle email, drip campaigns. |
| 3.13 | Social Media Manager | T3 | Social channels (trademark-restricted). |
| 3.14 | Community Manager | T3 | Community channels. |
| 3.15 | Brand Manager | T3 | Brand identity, positioning, voice. |
| 3.16 | Product Marketing Manager | T2 | Use-case messaging, launch comms. |
| 3.17 | Growth Marketer | T2 | Experimentation, funnel optimization. |
| 3.18 | Channel Sales Manager | T3 | Referral partners, channel, integration. |

### 12.4 Engineering & Development (24)
| # | Role | Tier | Definition |
|---|---|---|---|
| 4.1 | CTO/VP Engineering | T1 | Owns all technical decisions. |
| 4.2 | Engineering Manager | T3 | Manages team: 1:1s, performance, growth. |
| 4.3 | Frontend Engineer | T1 | Client-side: UI, UX, browser code. |
| 4.4 | Backend Engineer | T1 | Server-side: APIs, databases, services. |
| 4.5 | Full-stack Engineer | T1 | Both backend and frontend. |
| 4.6 | Mobile Engineer | T3 | iOS, Android, RN, Flutter. |
| 4.7 | DevOps / SRE Engineer | T1 | Infra, CI/CD, monitoring, incident response. |
| 4.8 | QA Engineer | T1 | Test automation, manual QA, acceptance. |
| 4.9 | Security Engineer | T1 | AppSec, infra security, incident response. |
| 4.10 | ML Engineer | T3 | Model training, fine-tuning, inference. |
| 4.11 | Data Engineer | T3 | Data pipelines, ETL, warehouse. |
| 4.12 | Solutions Architect | T3 | Custom solutions for clients. |
| 4.13 | Tech Writer | T2 | API docs, user guides, runbooks. |
| 4.14 | Engineering Product Manager | T3 | Bridges engineering and product/business. |
| 4.15 | Platform Engineer | T3 | Internal developer platform. |
| 4.16 | Release Manager | T3 | Versioning, rollouts, rollback. |
| 4.17 | SRE | T3 | Specialized DevOps — SLOs, error budgets, on-call. |
| 4.18 | Database Administrator (DBA) | T2 | Backups, performance, schema migrations. |
| 4.19 | Network Engineer | T3 | Architecture, firewalls, VPN. |
| 4.20 | UI/UX Designer | T2 | Interfaces, usability tests. |
| 4.21 | Product Designer | T3 | End-to-end product design. |
| 4.22 | Build / Release Engineer | T3 | Build pipelines, artifact management. |
| 4.23 | Embedded Systems Engineer | T4 | Firmware, hardware integration. |
| 4.24 | AI Safety Engineer | T1 | Prevents Kiro-class incidents (OWASP LLM Top 10 2026). |

### 12.5 Research & Education (12)
| # | Role | Tier | Definition |
|---|---|---|---|
| 5.1 | Research Lead | T1 | Research agenda, flagship outputs. |
| 5.2 | Researcher | T1 | Performs research. |
| 5.3 | Writer / Editor | T1 | Research → papers, articles, blog posts. |
| 5.4 | Academic Liaison | T2 | Submissions to journals/conferences. |
| 5.5 | Citation / Bibliography Specialist | T1 | Citation discipline, reference management. |
| 5.6 | Course Designer | T1 | Curriculum: modules, lessons, exercises. |
| 5.7 | Course Producer | T2 | Produces content: video, slides, transcripts. |
| 5.8 | Instructional Designer | T3 | Pedagogy: learning objectives, assessments. |
| 5.9 | Subject Matter Expert (SME) | T2 | Domain expert for specific modules. |
| 5.10 | Research Engineer | T2 | Tools used in research: eval harnesses, pipelines. |
| 5.11 | IP / Patent Specialist | T3 | Patents, trademarks for IP. |
| 5.12 | Publication Coordinator | T2 | Publications pipeline: submissions, embargoes. |

### 12.6 People & Culture (8)
| # | Role | Tier | Definition |
|---|---|---|---|
| 6.1 | Head of People / VP HR | T1 | All people decisions: hiring, growth, culture. |
| 6.2 | Recruiter | T4 | Hiring pipeline: sourcing, screening, interviewing. |
| 6.3 | Onboarding Specialist | T4 | New-hire onboarding program. |
| 6.4 | Performance Coach | T1 | Coaches individuals on growth, goals, feedback. |
| 6.5 | Recognition Lead | T1 | Milestone recognition, rituals, cultural artifacts. |
| 6.6 | Compensation Specialist | T4 | Comp bands, bonus plans, equity grants. |
| 6.7 | People Operations Specialist | T3 | HRIS, benefits, time off. |
| 6.8 | L&D Manager | T3 | Training budget, learning paths. |

### 12.7 AI Ops (6)
| # | Role | Tier | Definition |
|---|---|---|---|
| 7.1 | AI Ops Lead | T1 | Owns agent layer. Eval gates, observability, drift detection. |
| 7.2 | Agent Reliability Engineer | T2 | Eval harnesses, golden trajectories, agent test framework. |
| 7.3 | MLOps Engineer | T3 | Model deployment, monitoring, retraining, inference cost. |
| 7.4 | LLMOps Engineer | T3 | LLM-specific ops: prompt versioning, eval at scale. |
| 7.5 | Prompt Engineer | T2 | Optimizes prompts, A/B tests on agent instructions. |
| 7.6 | AI Evaluator | T2 | Manual + automated evaluation of agent outputs. |

### 12.8 Compliance (4)
| # | Role | Tier | Definition |
|---|---|---|---|
| 8.1 | Compliance Officer | T1 | Compliance program. Currently Ivan. |
| 8.2 | Privacy Counsel / DPO | T3 | EU personal data at scale. |
| 8.3 | Trademark Specialist | T2 | Trademark portfolio, infringement watch. |
| 8.4 | Regulatory Affairs Specialist | T3 | EU AI Act, GDPR, sector-specific. |

### 12.9 Knowledge Management (4)
| # | Role | Tier | Definition |
|---|---|---|---|
| 9.1 | Knowledge Manager | T2 | Source-materials curation policy. |
| 9.2 | Content Curator | T2 | Mechanical curation, daily freshness sweep. |
| 9.3 | Citation Specialist | T1 | Embedded in Research (5.5). |
| 9.4 | Taxonomy Architect | T3 | Knowledge taxonomy, ontologies, metadata schemas. |

### 12.10 RevOps (5)
| # | Role | Tier | Definition |
|---|---|---|---|
| 10.1 | RevOps Lead | T2 | Lead → cash funnel. Pipeline analytics. |
| 10.2 | Sales Ops Analyst | T2 | CRM, sales tooling, sales metrics. |
| 10.3 | Marketing Ops Manager | T2 | Marketing automation, attribution, lead routing. |
| 10.4 | BI Analyst | T2 | Dashboards, reports, KPIs. |
| 10.5 | Data Steward | T3 | Data quality, governance, lineage. |

### 12.11 BizOps (3)
| # | Role | Tier | Definition |
|---|---|---|---|
| 11.1 | BizOps Lead | T2 | Cross-functional analytics, OKR tracking. |
| 11.2 | Strategy Analyst | T3 | Competitive intel, market sizing. |
| 11.3 | Operations Analyst | T2 | Operational metrics, process improvement. |

### 12.12 Customer Success (6)
| # | Role | Tier | Definition |
|---|---|---|---|
| 12.1 | CSM Lead | T3 | Post-sale retention, expansion. |
| 12.2 | Onboarding Specialist | T3 | First 90 days of new customer. |
| 12.3 | Account Manager | T3 | Ongoing relationship, upsell. |
| 12.4 | Renewals Manager | T3 | Contract renewals, churn prevention. |
| 12.5 | Customer Education Specialist | T3 | Trains customers to get value. |
| 12.6 | Support Engineer | T3 | Tier 1-3 technical support. |

### 12.13 AI Safety (4)
| # | Role | Tier | Definition |
|---|---|---|---|
| 13.1 | AI Safety Engineer | T1 | Hard stops, eval gates, OWASP LLM compliance. |
| 13.2 | AI Red Team | T3 | Adversarial testing of agents. |
| 13.3 | AI Evaluator | T2 | Output quality assessment. |
| 13.4 | AI Ethics Specialist | T3 | Bias, fairness, transparency reviews. |

### 12.14 Procurement (4)
| # | Role | Tier | Definition |
|---|---|---|---|
| 14.1 | Procurement Manager | T2 | Vendor evaluation, contract negotiation. |
| 14.2 | Vendor Manager | T2 | Day-to-day vendor relationships. |
| 14.3 | Contract Negotiator | T2 | SaaS contract terms. |
| 14.4 | Renewal Specialist | T2 | Tracks renewals, flags ahead of time. |

### 12.15 Tier-3 Deferred Roles (12)
| # | Role | Tier | Trigger |
|---|---|---|---|
| 15.1 | Chief of Staff | T3 | Ivan coord hours > 50/week |
| 15.2 | Trust & Safety Lead | T3 | Ship consumer AI product |
| 15.3 | DevRel Manager | T3 | ParaguAI Builder has public API |
| 15.4 | Investor Relations Manager | T3 | First external investor |
| 15.5 | Workplace Manager | T3 | Open physical office |
| 15.6 | Fraud / Risk Analyst | T3 | $500K+ payment volume |
| 15.7 | Treasury Manager | T3 | $100K+ cash |
| 15.8 | Internal Audit Lead | T3 | $1M+ revenue |
| 15.9 | Workplace Operations | T3 | Open office |
| 15.10 | DEI Specialist | T3 | 10+ employees |
| 15.11 | Public Relations Manager | T3 | Launch flagship brand |
| 15.12 | Government Relations | T3 | Regulated vertical |

### 12.16 Tier-4 Enterprise Roles (5)
| # | Role | Trigger |
|---|---|---|
| 16.1 | Internal Communications Manager | 50+ people |
| 16.2 | M&A / Corp Dev | Acquisitions planned |
| 16.3 | Chief Data Officer (CDO) | Data-driven product |
| 16.4 | Chief AI Officer (CAIO) | Enterprise AI |
| 16.5 | Diversity & Inclusion Lead | 25+ employees |

---

## 13. Producer → Consumer Matrix (9 Schemas)

| # | State file | Producer agent + cron | Primary consumers | Failure mode if missing |
|---|---|---|---|---|
| 1 | `analyst.json` | business-analyst via `aiw-business-analyst-daily` | Ivan (daily), management-coordinator, morning-brief | Ivan misses business-health signal; coord's "needs Ivan" list stays empty |
| 2 | `coord.json` | management-coordinator via `aiw-management-coord-biwk` | Ivan (biweekly), business-analyst, devops-monitor-30min | Escalation items invisible to morning-brief |
| 3 | `kiki.json` | kiki-coach via `aiw-kiki-coach-weekly` | Kyrian (weekly), people dept, coach-kiki, coach-onboarding | Kyrian's learning cadence dies |
| 4 | `kiki-prep.json` | (pre-step of kiki-coach) via `scripts/kiki-coach-prep.sh` | kiki-coach prompt | kiki-coach prompt forced to use stale context |
| 5 | `finance.json` | finance-controller via `aiw-finance-controller-weekly` | Ivan (weekly), business-analyst | Runway/MRR signal absent from daily brief |
| 6 | `sales.json` | sales-pipeline via `aiw-sales-pipeline-daily` | Ivan (daily), finance-controller | Finance-controller's deals_open stays stale |
| 7 | `engineering.json` | engineering-roster via `aiw-engineering-roster-biwk` | management-coordinator, Ivan (biweekly), devops-monitor-30min | Coord's blocker list misses infra incidents |
| 8 | `research.json` | research-tracker via `aiw-research-tracker-weekly` | Ivan (weekly), coaching-research-intelligence | Thesis status invisible to brief |
| 9 | `people.json` | people-hr via `aiw-people-hr-weekly` | Ivan (weekly), kiki-coach | Headcount/attrition blind spot |

**Cross-cutting file**: `org-state.json` (4 monitoring writers) — read by every consumer as freshness index. If >5 min stale, every agent has been quiet.

**Eval file**: `eval-per-agent.json` — written by `aiw-eval-gate-runner-on-agent-run` every hour. Read by ai-safety-engineer-30min + devops-monitor-30min.

---

## 14. Escalation Routing (4 Levels)

| Level | Definition | Routing | Latency | Examples |
|---|---|---|---|---|
| **CRITICAL** | Data loss, payment failure, site down, secret leak, model provider down >2h, gateway 5xx sustained | All 3: coord.json `priority:critical` + Kanban `critical` `auto_claim:true` + cron-inject to morning-brief | 5 min detection → 5 min page | `worker_post_probe.http==500` 2 ticks, secret leak, runway < 1.0mo |
| **HIGH** | Revenue-blocking, deadline <72h, blocked lead, SLA imminent, single agent error >24h | Own state `open_questions` `priority:high` + Kanban HIGH | 15 min detection → 15 min Kanban | stalled deal >14d, stale repo >7d, 2 missed kiki-coach runs |
| **MEDIUM** | Process gap, stale repo, missing skill, schema drift, single tick error | Own state `open_questions` `priority:medium` OR Kanban MEDIUM | 4 h → morning-brief | single cron-heartbeat miss, hard-stop drift, Class-35 anchor >5h |
| **LOW** | Cosmetic, nice-to-have, observability polish | Next weekly report | Weekly | doc drift, skill staleness |

---

## 15. Recent Session Upgrades (Phases 17–25)

### Phase 17 — Research analysis
- Analyzed 15+ open-source AI agent repos
- Wrote PHASE-17-RESEARCH-ANALYSIS.md

### Phase 18 — Factor 7: WhatsApp human-in-loop
- `whatsapp-send.py`, whatsapp-human-in-loop skill
- 14 coaching agents have escalation triggers

### Phase 19 — Factor 11: Webhook triggers
- `webhook-receiver.py` on port 8081
- `coach-onboarding-poller.py` every 5 min
- Cron for auto-onboarding (PIX, Mercado Pago, bank, custom)

### Phase 20 — Factor 5: Unified execution state
- `org-state.json` single source of truth
- `build-org-state.py` hourly
- 47 agent PROMPT.md updated with Factor 5

### Phase 21 — 12-factor gaps closed
- Factor 3: `build-agent-context.py` (hourly)
- Factor 9: `compact-errors.py` (every 15 min)
- Factor 12: 14 coaching agents marked stateless
- Cost monitoring: $293/mo (vs $12K risk threshold)
- Agent tracing: latency + tokens
- Eval trending: 30-day pass rate (alerts <80%)
- Org dashboard: 8 FounderOS-style routes
- Skill deprecation: 90-day workflow
- WhatsApp templates: 6 files

### Phase 22 — Loop complete
- Self-running check v2 (uses org-state)
- State auto-commit to git
- Eval per-agent (from criteria)
- Eval auto-trigger on new briefs
- Cost alerts (WhatsApp at $1000/mo)
- Audit fix script (HIGH items → 0)
- Intake form (HTML → webhook)

### Phase 25 — Around-the-clock upgrade (14 items done, 4 in progress, 5 pending)
**Completed**:
1. Trademark banlist enforcement (`trademark-scan.py`, pre-commit hook, GitHub Action, cron every 30m)
2. LLM provider probe (`llm-provider-probe.py`, every 15m)
3. Cron drift-guard fix
4. Cron path unification (115 → 92 jobs after dedup)
5. State-file schema validation (`state-validate.py`, caught 23 drift errors)
6. Real handoff matrix (ORG-AGENTS.md 9.3 KB → 37.8 KB)
7. HTTP hardening re-evaluated
8. Alerting on error state (`cron-error-watchdog.py`, caught 16 jobs in error)
9. Per-dept toolsets (53/53 agents configured)
10. Dept-monitor pattern (16 `PROMPT-monitor.md` + `INDEX.md`)
11. Tier 1 coaching skills (4 SKILL.md files)
12. Chaos tests B + C
13. **24 duplicate cron entries** removed
14. **23 schema drift errors** fixed
15. **57 client sites + apex scrubbed** (trademark)

**Bugs caught & fixed**:
- 24 duplicate cron entries (zombies)
- `aiw-dashboard-refresh` script path wrong
- 16 cron jobs in error state >24h (all LLM billing)
- 9 of 9 LLM providers degraded (only `zai-glm-4-flash` works)
- 113 → 0 dirty files in client sites
- 23 → 0 schema drift errors in state files

**12-Factor final**: 9.0/10 average (up from 7.9/10 in Phase 21 baseline)

---

## 16. Active Cron Jobs (113 active after dedup)

### Tier-1 lead agents (7 cron jobs)
| Agent | Cron job | Schedule |
|---|---|---|
| business-analyst | aiw-business-analyst-daily | 30 10 * * * |
| management-coordinator | aiw-management-coord-biwk | 0 21 * * 1,4 |
| kiki-coach | aiw-kiki-coach-weekly | 0 21 * * 5 |
| sales-pipeline | aiw-sales-pipeline-daily | 0 13,16 * * * |
| finance-controller | aiw-finance-controller-weekly | 0 21 * * 5 |
| engineering-roster | aiw-engineering-roster-biwk | 0 20 * * 2,5 |
| research-tracker | aiw-research-tracker-weekly | 0 21 * * 0 |

### Tier-2 sub-agents (12 cron jobs)
| Agent | Cron job | Schedule |
|---|---|---|
| proposal-drafter | aiw-proposal-drafter-on-demand | 0 10 * * * |
| multimedia-producer | aiw-multimedia-producer-on-demand | 0 15 * * * |
| accounting-automation | aiw-accounting-automation-daily | 0 18 * * * |
| marketing-content-producer | aiw-marketing-content-mon-wed-fri | 0 12 * * 1,3,5 |
| lead-enrichment | aiw-lead-enrichment-daily | 30 9 * * * |
| revops-pipeline-analyzer | aiw-revops-pipeline-analyzer-daily | 0 7 * * * |
| qa-automation-runner | aiw-qa-automation-on-pr | 0 14 * * * |
| tax-receipt-tracker | aiw-tax-receipt-tracker-weekly | 0 19 * * 0 |
| procurement-tracker | aiw-procurement-tracker-weekly | 0 9 * * 1 |
| okr-tracker | aiw-okr-tracker-weekly | 0 8 * * 0 |
| source-curator | aiw-source-curator-weekly | 0 13 * * 2 |
| citation-checker | aiw-citation-checker-on-demand | 0 11 * * * |
| people-hr | aiw-people-hr-weekly | 0 22 * * 1 |
| delivery-tracker | aiw-delivery-tracker-weekly | 0 14 * * 1 |

### Tier-3 cross-cutting (7 cron jobs)
| Agent | Cron job | Schedule |
|---|---|---|
| ai-ops-coordinator | aiw-ai-ops-coordinator-daily | 0 8 * * * |
| bizops-tracker | aiw-bizops-tracker-weekly | 0 8 * * 1 |
| compliance-monitor | aiw-compliance-monitor-weekly | 0 9 * * 1 |
| founder-bandwidth-watchdog | aiw-founder-bandwidth-watchdog-weekly | 0 20 * * 0 |
| chaos-test-runner | aiw-chaos-test-runner-weekly | 0 14 * * 1 (OFF) |
| eval-gate-runner | aiw-eval-gate-runner-on-agent-run | 0 * * * * |
| security-auditor | aiw-security-audit-biweekly | 0 14 * * 5 |

### Tier-4 monitoring (4 cron jobs, every 30 min)
- aiw-devops-monitor-30min
- aiw-ai-safety-engineer-30min
- aiw-security-watchdog-30min
- aiw-coaching-quality-reviewer

### Tier-5 coaching (13 cron jobs, lives in [coach-agents](https://github.com/Ai-Whisperers/coach-agents))

| Agent | Cron job | Schedule |
|---|---|---|
| coach-ivan | aiw-coach-ivan | 0 21 * * 0 |
| coach-kiki | aiw-coach-kiki | 0 21 * * 5 |
| coach-org | aiw-coach-org | 0 0 1 1,4,7,10 * |
| coach-lead-agents | aiw-coach-lead-agents | 0 22 1 * * |
| coach-lead-finder | aiw-coach-lead-finder | 0 13 * * 3 |
| coach-renewal-manager | aiw-coach-renewal-manager | 0 9 1 * * |
| coach-roi-tracker | aiw-coach-roi-tracker | 0 16 * * 5 |
| coach-onboarding-poller | aiw-coach-onboarding-poller | */5 * * * * |
| coaching-content-curator | aiw-coaching-content-curator | 0 14 * * 1 |
| coaching-quality-reviewer | aiw-coaching-quality-reviewer | */30 * * * * |
| coaching-research-intelligence | aiw-coaching-research-intelligence | 0 13 * * 3 |
| kiki-coach-weekly | aiw-kiki-coach-weekly | 0 21 * * 5 |
| coaching-monitor-30min | aiw-coaching-monitor-30min | every 30m |

> Note: `board-of-directors` is governance (not a Tier-5 coaching agent) — see section 7.6.

### Infra & monitoring (16 cron jobs)
| Cron job | Schedule | Purpose |
|---|---|---|
| cron-sync | */5 * * * * | sync jobs.json from `cron/` on the deployment |
| site-health | */15 * * * * | probe apex + 57 sites |
| repo-ci-monitor | 0 11 * * * | GitHub Actions probe |
| rbl-check | 0 12 * * * | trademark scan |
| evo-poll-watchdog | */5 * * * * | Evolution API probe |
| thesis-daily-tick | 0 6 * * * | thesis_active/tick.py |
| thesis-watchdog | */15 * * * * | thesis_active/watchdog.py |
| thesis-weekly-review | 0 18 * * 0 | thesis_active/review.py |
| thesis-git-maintenance | 0 23 * * 0 | git gc + bundle |
| ometzdental-weekly-refresh | 0 6 * * 1 | Cloudflare Worker update |
| morning-brief | 0 10 * * * | legacy brief writer |
| hermes-bridge-watchdog | */5 * * * * | bridge liveness |
| mcp-health-check | 15 */6 * * * | MCP server probe |
| bws-cache-refresh | 0 */6 * * * | Bitwarden secrets cache |
| kv-bws-sync | */5 * * * * | KV↔BWS reconciliation |
| linkedin-token-refresh | 0 9 * * * | OAuth refresh |

### Phase 21/25 additions
| Cron job | Schedule | Purpose |
|---|---|---|
| aiw-compact-errors | */15 * * * * | Factor 9 error compaction |
| aiw-cost-monitor | 0 */6 * * * | cost monitoring |
| aiw-build-agent-context | 0 * * * * | Factor 3 context builder |
| aiw-agent-tracer | */30 * * * * | agent observability |
| aiw-eval-trending | 0 6 * * * | 30-day eval pass rate |
| aiw-org-dashboard | 0 8 * * * | 8-route dashboard |
| aiw-trademark-scan-cron | */30 * * * * | trademark enforcement |
| aiw-llm-provider-probe | */15 * * * * | LLM provider health |
| aiw-cron-error-watchdog | */30 * * * * | cron error alerting |
| aiw-state-validate-15m | */15 * * * * | schema validation |

---

## 17. Coaching Skills (16 shipped)

### Tier 1 (4)
- `coaching skill `coaching-lead-agents` (in skills/ on the deployment)` (11.8 KB)
- `coaching skill `coaching-roi-tracker` (in skills/ on the deployment)` (15.0 KB)
- `coaching skill `coaching-content-curator` (in skills/ on the deployment)` (15.0 KB)
- `coaching skill `coaching-research-intelligence` (in skills/ on the deployment)` (20.5 KB)

### Tier 2/3 (12 planned next)
- Sunstein, Solstein + 10 others

---

## 18. Backlog & Open Work

### Blockers
- **OpenRouter $20 topup** (Ivan action) → unblocks all 47 agents
- First real prospect WhatsApp (Rubicón EAS or Ometz Dental)
- First free GROW quick-win → proves funnel

### Pending from Phase 25
- Item 8: Pre-write snapshots / rollback playbook cron (partial)
- Item 13: Tooling tiers doc + customer template
- Item 14: Split agents-v2 into per-dept repos
- Item 16: Sunstein + Solstein skills
- Item 18: Eval-gate as automatic post-brief hook

### Naming cleanup (Section 11.1)
- 3 agents share "Erebus" — resolve via Hypnos/Nemesis rename
- `chaos-test-runner` (Chaosia) revival decision — **Eris** candidate
- Heritage → DEMIURGE migrations: engineering, finance, kiki-coach

---

## 19. Cross-References

### AIW repos (post 2026-08-31 split)
- **`aiw-org`** ([github.com/Ai-Whisperers/aiw-org](https://github.com/Ai-Whisperers/aiw-org)) — internal AIW org layer: 6 Tier-1 dept dirs + governance, 34 production agents, DEMIURGE framework, 81 tickets, 25 scripts/tests
- **`coach-agents`** ([github.com/Ai-Whisperers/coach-agents](https://github.com/Ai-Whisperers/coach-agents)) — internal coaching product: 15 agents (kiki-coach + 14 coach-* cron agents)
- **`growth-coaching`** ([github.com/Ai-Whisperers/growth-coaching](https://github.com/Ai-Whisperers/growth-coaching)) — customer-facing GROW coaching product: 6 distributable packages
- ~146 repos total across the org

### Sister docs (cross-repo)
- [`ROLES-INVENTORY.md`](../ROLES-INVENTORY.md) — 137-role catalog (in growth-coaching)
- [`ROADMAP-DEPT-EXPANSION.md`](https://github.com/Ai-Whisperers/growth-coaching/blob/master/ROADMAP-DEPT-EXPANSION.md) — Phase 0-4 build order
- [`PHASE-17..25-*.md`](https://github.com/Ai-Whisperers/growth-coaching/tree/master/) — session upgrade logs
- [`MASTER-UPGRADE-CHANGELOG.md`](https://github.com/Ai-Whisperers/growth-coaching/blob/master/MASTER-UPGRADE-CHANGELOG.md) — full changelog
- [`STATE-AUDIT-2026-08-14.md`](https://github.com/Ai-Whisperers/growth-coaching/blob/master/STATE-AUDIT-2026-08-14.md) — state-file audit
- [`12-FACTOR-AUDIT.md`](https://github.com/Ai-Whisperers/growth-coaching/blob/master/12-FACTOR-AUDIT.md) — Factor compliance

### Local files (in this repo)
- [meetings/department-design/README.md](../meetings/department-design/README.md) — **design-meeting source of truth** (Magic Tower, 28 Aug sessions, ratified decisions)
- [ORG-AGENTS.md](../ORG-AGENTS.md) — full handoff matrix
- [ROLLBACK-PLAYBOOK.md](../playbooks/ROLLBACK-PLAYBOOK.md)
- [DEFERRED-AGENTS.md](../DEFERRED-AGENTS.md) — deferred agent triggers
- [DEFERRED-ROLES.md](../DEFERRED-ROLES.md) — deferred role triggers
- [AGENT-NAMES-V2.md](AGENT-NAMES-V2.md) — portmanteau legacy layer
- [NAMING-CONVENTION-ANALYSIS.md](NAMING-CONVENTION-ANALYSIS.md) — naming rationale
- [departments/01..06-*.md](../departments/) — 6 dept charters
- `packages/` (in growth-coaching) — 37 shipped distributable agents
- `runtime cron/jobs.json` (113 jobs; canonical on the deployment)
- `runtime state/` (9 live state files + mirrors)

### Related repos
- [ORGANIGRAM.md](ORGANIGRAM.md) — companion organigram with full dept→role→agent tree

---

## 20. Naming Hierarchy (3 Layers)

```
Layer 1 — DEMIURGE (canonical, 24 agents)
   ↓ migration when dept gets full buildout
Layer 2 — Portmanteau (heritage, 23 agents)
   ↓ until DEMIURGE migration
Layer 3 — Formal name (technical ID, all 47 agents)
```

**One name per agent. No duplicates. No aliases.** If you find two names for one agent, that's a bug.

Open naming tickets (3):
- 3 agents share "Erebus" → resolve via Hypnos/Nemesis/Erebus split
- `chaos-test-runner` OFF → decide revive or sunset
- `kiki-coach` Magistra → promote to DEMIURGE (Sophia or Mneme)

---

*Generated 2026-08-31 by Erebus consolidation pass. **Implementation** source of truth: this file (what exists in git). **Design-meeting** source of truth: `meetings/department-design/`. Supersedes DEPT-AGENTS-ROLES-COMPLETE-v1 (2026-08-14) and the AGENT-NAMES-V2 portmanteau framework (now legacy layer).*