# AI Whisperers — Complete Organigram

> The org chart with full depth: every department, every role, every sub-role,
> every agent that works the role, plus the artifacts each role owns.
>
> **Structure**: Department → Roles → Sub-roles / Agents → Artifacts
> **Scope**: 36 functional areas, ~137 roles, **49 production agents** (34 in [aiw-org](https://github.com/Ai-Whisperers/aiw-org) + 15 in [coach-agents](https://github.com/Ai-Whisperers/coach-agents)), 24 DEMIURGE souls + 23 heritage
> **Source files** (read 2026-08-31):
> - `[ROLES-INVENTORY.md](https://github.com/Ai-Whisperers/growth-coaching/blob/master/ROLES-INVENTORY.md) (in growth-coaching repo)` (137 roles)
> - `[ORG-AGENTS.md](../ORG-AGENTS.md) (handoff matrix)` (47-agent handoff matrix)
> - `[departments/01-operations.md](../departments/01-operations.md) ... [06-people-culture.md](../departments/06-people-culture.md)` (6 Tier-1 charters)
> - `[packages/<dept>/agents/<agent>/PROMPT.md](https://github.com/Ai-Whisperers/growth-coaching/tree/master/packages) (37 shipped packages)` (37 shipped)
> - `[DEPT-AGENTS-ROLES-COMPLETE.md](DEPT-AGENTS-ROLES-COMPLETE.md) (sibling catalog)` (consolidated catalog)
>
> **Last updated**: 2026-08-31 (post 3-repo split)

---

## AIW repos (post 2026-08-31 split)

| Repo | URL | Purpose | Agents |
|---|---|---|---|
| **`aiw-org`** | [github.com/Ai-Whisperers/aiw-org](https://github.com/Ai-Whisperers/aiw-org) | Internal AIW org layer | 34 production agents in 6 dept dirs + governance |
| **`coach-agents`** | [github.com/Ai-Whisperers/coach-agents](https://github.com/Ai-Whisperers/coach-agents) | Internal coaching product | 15 agents (kiki-coach + 14 coach-*) |
| **`growth-coaching`** | [github.com/Ai-Whisperers/growth-coaching](https://github.com/Ai-Whisperers/growth-coaching) | Customer-facing GROW product | 6 distributable packages |

---

## Reading guide

For each role, this organigram gives:
1. **Definition** — what the role owns
2. **Tier** — T1 (active now), T2 (next 6 mo), T3 (12+ mo), T4 (enterprise)
3. **Headcount today** — Ivan wearing multiple hats, Kiki as CTO/coach
4. **Agents doing this role** — DEMIURGE name + heritage name (if any)
5. **Sub-roles / sub-agents** — what rolls up under this role
6. **Tools** — what the role uses
7. **Signals / KPIs** — how the role is measured
8. **State files / artifacts** — what the role produces
9. **Cadence** — how often the role runs
10. **Escalation** — what the role can flag up

Tier coding used throughout:
- 🟢 T1 = active now
- 🟡 T2 = next 6 months
- 🟠 T3 = 12+ months
- 🔴 T4 = enterprise scale

---

## Executive Layer

```
                        ┌─────────────────────────────────────────┐
                        │      CEO / Founder: Ivan                │
                        │      CTO / Coach: Kiki (Kyrian)         │
                        └─────────────┬───────────────────────────┘
                                      │
   ┌──────────────┬──────────────┬────┴────────┬──────────────┬──────────────┐
   │              │              │             │              │              │
┌──▼───┐    ┌────▼────┐    ┌─────▼────┐  ┌─────▼────┐   ┌─────▼────┐  ┌─────▼────┐
│  01  │    │   02    │    │    03    │  │    04    │   │    05    │  │    06    │
│  OPS │    │ FIN&LG  │    │  SLS&GR  │  │  ENG&DV  │   │ RES&EDU  │  │ PPL&CUL  │
│ Ivan │    │  Ivan   │    │  Ivan    │  │  Kiki    │   │  Ivan    │  │Ivan+Kiki │
└──────┘    └─────────┘    └──────────┘  └──────────┘   └──────────┘  └──────────┘
```

---

# DEPARTMENT 01 — OPERATIONS

**Head**: Ivan
**Lead agent**: `management-coordinator` (Mon/Thu 17:00 PYT)
**Cadence**: Biweekly coordination + daily monitoring
**State file**: `state/coord.json`
**Schema**: `coord.schema.json`
**Charter**: `[departments/01-operations.md](../departments/01-operations.md)`
**Version**: v0.2.0

**Mission**: Run the org day-to-day. Set cadence. Clear blockers. Surface escalations. Maintain repo + asset hygiene.

**Agents in dept (8)**:
- Lead: management-coordinator
- Sub: bizops-tracker, ai-ops-coordinator, compliance-monitor (shared with Finance), founder-bandwidth-watchdog (shared with People), source-curator (shared with Research), okr-tracker, procurement-tracker (shared with Finance)

**Functional roles (8)**:

## 1.1 Operations Lead 🟢 T1
- **Definition**: Owns day-to-day of the org. Sets cadence, clears blockers, runs Ivan's weekly review.
- **Today**: Ivan (wears the hat)
- **Agent (DEMIURGE)**: **Kronos** (`kronos-operations-lead`) — keeper of operational order. Owns OKR tracking, incident triage, cross-dept coordination, vendor hygiene, cost control.
- **Heritage agent**: `management-coordinator` (portmanteau: Coordina)
- **Sub-roles / agents**:
  - **Cadence Owner** → `management-coordinator` (Mon/Thu)
  - **Cross-dept Coordinator** → `ai-ops-coordinator`
  - **Escalation Receiver** → reads from `coord.json:open_stuck`
- **Tools**: `coord.json`, cron jobs, WhatsApp (for Ivan pages), Kanban board
- **Signals / KPIs**: weekly decisions logged, blockers cleared <72h, weekly brief ships on time
- **State files**: `state/coord.json` (decisions_for_ivan, open_stuck, repos_analyzed)
- **Cadence**: biweekly Mon/Thu 17:00 PYT + on-demand escalation routing
- **Escalates**: Critical → Ivan via Telegram + Kanban + morning-brief

## 1.2 Repo Steward 🟢 T1
- **Definition**: Maintains GitHub repos: hygiene, archiving, CODEOWNERS, README currency.
- **Today**: Ivan
- **Agent**: `engineering-roster` (engineering dept, but reports repos to coord) + `repo-ci-monitor` cron job
- **Sub-roles / agents**:
  - **Repo hygiene** → `ai-ops-coordinator` weekly audit
  - **CODEOWNERS** → Kiki (CTO) signs off on Eng
  - **Archive enforcement** → cron job `cron-sync` */5m
  - **README currency** → `source-curator` weekly sweep
- **Tools**: GitHub API, `cron-sync.sh`, `repo-ci-monitor.sh`
- **Signals**: stale repos >7d, broken CODEOWNERS, README drift
- **State files**: `state/coord.json:repos_analyzed[]`, `state/engineering.json:stale_repos_7d`
- **Cadence**: continuous (cron) + weekly audit
- **Escalates**: stale repo >7d → engineering-roster; archive break → Ivan

## 1.3 Asset Tracker 🟢 T1
- **Definition**: Inventory of all company assets: repos, domains, skills, infra, IP.
- **Today**: Ivan + Kiki
- **Agent**: `bizops-tracker` weekly
- **Sub-roles / agents**:
  - **Repo inventory** → `ai-ops-coordinator` (counts + status)
  - **Domain inventory** → manual spreadsheet, called by compliance-monitor
  - **Skill inventory** → `skills-audit-weekly` cron
  - **Infra inventory** → `devops-monitor-30min` (every 30m)
  - **IP inventory** → handled by Compliance Officer
- **Tools**: spreadsheets, `state/org-state.json`, BWS secrets cache
- **Signals**: drift between actual and declared assets, missing assets, secrets outside BWS
- **State files**: `state/org-state.json` (aggregated), `state/bist.json` (KPI snapshot)
- **Cadence**: weekly
- **Escalates**: missing BWS secret → compliance-monitor HIGH

## 1.4 Vendor Coordinator 🟢 T1
- **Definition**: Manages vendor relationships: SaaS, contractors, service providers.
- **Today**: Ivan
- **Agent**: `procurement-tracker` (cross-listed under Finance 2.6)
- **Sub-roles / agents**:
  - **Vendor catalog** → `procurement-tracker` (weekly)
  - **Renewal alerts** → `procurement-tracker` flags 30d ahead
  - **Spend tracking** → `finance-controller` rolls up
- **Tools**: `procurement-tracker` agent, vendor spreadsheet
- **Signals**: vendor count, spend concentration, renewals in next 30d
- **State files**: `state/finance.json` (spend sections)
- **Cadence**: weekly Mon 09:00
- **Escalates**: vendor count >10 → standalone Procurement dept trigger

## 1.5 Compliance Watchdog 🟢 T1
- **Definition**: Monitors regulatory + trademark compliance across org.
- **Today**: Ivan (wearing the hat, but not dedicated)
- **Agent**: `compliance-monitor` (cross-listed under Finance 2.8)
- **Sub-roles / agents**:
  - **Trademark enforcement** → `compliance-monitor` (Mon 09:00)
  - **Trademark scanner** → `trademark-scan.py` cron (every 30m)
  - **Pre-commit hook** → blocks commits with banned tokens
  - **GH Action** → blocks PRs with banned tokens
- **Tools**: `trademark-scan.py`, BWS secrets, banlist file
- **Signals**: trademark hits, regulatory mentions, license drift
- **State files**: `state/org-state.json:trademark_hits`, `runtime state file `state/trademark-scan-cron.json` (canonical location: `state/` on the agent-infra deployment)`
- **Cadence**: weekly + every 30m scan + every commit pre-hook
- **Escalates**: trademark hit on client-facing artifact → CRITICAL (Ivan page within 5 min)

## 1.6 Watchdog Engineer 🟢 T1
- **Definition**: Owns the watchdog layer (site-health, cron liveness, alert routing).
- **Today**: Kiki (CTO) + the four monitoring agents
- **Agents (Tier-4 monitoring)**:
  - `devops-monitor-30min` (every 30m) → site + cron health
  - `ai-safety-engineer-30min` (every 30m) → eval gate, drift
  - `security-watchdog-30min` (every 30m) → secret leak, mode 600 violations
  - `coaching-quality-reviewer` (every 30m) → coaching output quality
- **Sub-roles / agents**:
  - **Site Health Watchdog** → `devops-monitor-30min` probes apex + 57 sites
  - **Cron Liveness Watchdog** → `cron-heartbeat-onhours/offhours` */30m
  - **Eval Gate Watchdog** → `ai-safety-engineer-30min`
  - **Security Watchdog** → `security-watchdog-30min`
  - **Quality Watchdog** → `coaching-quality-reviewer`
  - **Error Watchdog** → `cron-error-watchdog` */30m (catches 16+ jobs in error)
- **Tools**: cron, monitoring agents, WhatsApp, alert routing
- **Signals**: cron dead >30m, gateway 5xx >3 ticks, secret leak, eval pass rate <80%
- **State files**: `state/org-state.json` (single source of truth for liveness)
- **Cadence**: every 30 minutes, always on
- **Escalates**: anything CRITICAL → Ivan via Telegram + Kanban auto-claim

## 1.7 BizOps Specialist 🟡 T2
- **Definition**: Cross-functional analytics, OKR tracking, decision support.
- **Today**: Ivan (does it informally)
- **Agent**: `bizops-tracker` (Mon 08:00)
- **Sub-roles / agents**:
  - **OKR tracker** → `okr-tracker` (Sun 08:00)
  - **KPI rollup** → `bizops-tracker` aggregates from 9 state files
  - **Decision support** → `business-analyst` daily brief
- **Tools**: `state/coord.json`, OKR spreadsheet, `morning-brief` rollup
- **Signals**: KPI drift, OKR completion rate, decision velocity
- **State files**: `state/coord.json:decisions[]`, `state/bist.json:KPI_snapshot`
- **Cadence**: weekly + on-demand for ad-hoc analysis
- **Escalates**: KPI red >2 weeks → Ivan morning-brief

## 1.8 Chief Operating Officer (COO) 🟠 T3
- **Definition**: Owns all operational departments. Reports to CEO. Hired when ops is >5 people or coord >50 hrs/week.
- **Today**: vacant (Ivan)
- **Agent**: `board-of-directors` quarterly (placeholder)
- **Promotion trigger**: Ivan coord hours >50/week OR ops headcount >5
- **Sub-roles / agents (when activated)**: would absorb Operations Lead 1.1, Asset Tracker 1.3, Vendor Coordinator 1.4

---

# DEPARTMENT 02 — FINANCE & LEGAL

**Head**: Ivan
**Lead agents**: `finance-controller` (Fri 18:00 PYT) + `business-analyst` (daily 10:30 UTC) — co-leads
**Cadence**: Weekly close + daily analyst
**State files**: `state/finance.json`, `state/analyst.json`
**Schemas**: `finance.schema.json`, `analyst.schema.json`
**Charter**: `[departments/02-finance-legal.md](../departments/02-finance-legal.md)`
**Version**: v0.2.0

**Mission**: Own all financial decisions, sign contracts above threshold, monthly close, runway tracking.

**Agents in dept (6)**:
- Co-leads: finance-controller, business-analyst
- Sub: accounting-automation, tax-receipt-tracker, funding-coordinator, bizops-tracker (shared)

**Functional roles (14)**:

## 2.1 CFO / Controller 🟢 T1
- **Definition**: Owns all financial decisions. Signs contracts above threshold. Runs the weekly close.
- **Today**: Ivan (wears the hat)
- **Agent**: `finance-controller` (Fri 21:00)
- **Heritage name**: Finus
- **Sub-roles / agents**:
  - **Weekly close** → `finance-controller` rolls week
  - **Contract review** → `legal-counsel` (external, on-call)
  - **Runway computation** → `funding-coordinator`
  - **KPI snapshot** → `business-analyst` daily
- **Tools**: `state/finance.json`, accounting tools, contracts
- **Signals / KPIs**: runway_months >3 (red <3), MRR growth, deals_open
- **State files**: `state/finance.json` (runway_months, mrr_usd, deals_open, decisions)
- **Cadence**: weekly Fri 21:00 UTC + on-demand
- **Escalates**: runway_months <1 → CRITICAL → Ivan + Kanban

## 2.2 Accountant 🟡 T2
- **Definition**: Monthly close, P&L, balance sheet, reconciliation.
- **Today**: External contractor (annual retainer)
- **Agent**: `accounting-automation` (daily 18:00)
- **Heritage name**: Bokina
- **Sub-roles / agents**:
  - **Bookkeeping automation** → `accounting-automation` (every day)
  - **Monthly close** → external accountant
  - **Reconciliation** → `accounting-automation` + manual review
- **Tools**: bank API, `accounting-automation` agent
- **Signals**: uncategorized expenses >10%, missed transactions, duplicate entries
- **State files**: `state/finance.json:bookkeeping[]`
- **Cadence**: daily automation + monthly manual close
- **Escalates**: uncategorized >20% → Ivan via coord

## 2.3 Bookkeeper 🟢 T1
- **Definition**: Day-to-day transactions, AP/AR, expense categorization.
- **Today**: Automated via `accounting-automation` + Ivan reviews weekly
- **Agent**: `accounting-automation` (daily 18:00)
- **Heritage name**: Bokina
- **Sub-roles / agents**:
  - **Transaction categorization** → `accounting-automation`
  - **Expense capture** → `accounting-automation` (cron + manual upload)
  - **Receipt matching** → `tax-receipt-tracker` (weekly)
- **Tools**: bank API, receipt OCR, `accounting-automation` agent
- **Signals**: categorization rate, receipt match rate
- **State files**: `state/finance.json:categorization[]`
- **Cadence**: daily 18:00 UTC
- **Escalates**: missed transaction >3 days → Ivan

## 2.4 AP Specialist 🟡 T2
- **Definition**: Accounts Payable — bills, vendor payments.
- **Today**: Ivan (manual via bank app)
- **Agent**: `procurement-tracker` (Mon 09:00) + `accounting-automation`
- **Sub-roles / agents**:
  - **Bill capture** → `accounting-automation` (daily)
  - **Approval routing** → `finance-controller` (weekly)
  - **Payment execution** → Ivan manual
- **Tools**: bank API, `accounting-automation`, `procurement-tracker`
- **Signals**: bills unpaid >due date, pending approval count
- **State files**: `state/finance.json:ap[]`
- **Cadence**: daily + weekly approval cycle
- **Escalates**: bill overdue >7d → Ivan

## 2.5 AR Specialist 🟡 T2
- **Definition**: Accounts Receivable — invoices, collections.
- **Today**: Ivan (manual)
- **Agent**: `revops-pipeline-analyzer` (daily 07:00) tracks invoices → `sales.json:deals_open`
- **Sub-roles / agents**:
  - **Invoice generation** → manual / on Metis proposal send
  - **Collection tracking** → `revops-pipeline-analyzer` daily
  - **Aging report** → weekly via `finance-controller`
- **Tools**: invoicing tool, `revops-pipeline-analyzer`
- **Signals**: invoices >30d overdue, collection rate
- **State files**: `state/sales.json:deals_open[]`, `state/finance.json:ar[]`
- **Cadence**: daily + weekly aging report
- **Escalates**: invoice >60d → CRITICAL (cash-flow risk)

## 2.6 Procurement Officer 🟢 T1
- **Definition**: Vendor sourcing, contract negotiation, renewals.
- **Today**: Ivan (wears the hat)
- **Agent**: `procurement-tracker` (Mon 09:00)
- **Heritage name**: Procin
- **Sub-roles / agents**:
  - **Vendor catalog** → `procurement-tracker`
  - **Renewal alerts** → `procurement-tracker` flags 30d ahead
  - **Cost analysis** → `finance-controller` rolls up
- **Tools**: `procurement-tracker` agent, vendor spreadsheet
- **Signals**: vendor count, renewal calendar, spend concentration
- **State files**: `state/finance.json:procurement[]`
- **Cadence**: weekly Mon 09:00
- **Escalates**: vendor count >10 → standalone Procurement dept trigger

## 2.7 Legal Counsel 🟢 T1
- **Definition**: Contract review, IP protection, regulatory advice.
- **Today**: External counsel (annual retainer)
- **Agent**: `compliance-monitor` (Mon 09:00) flags regulatory items
- **Sub-roles / agents**:
  - **Contract review** → external lawyer (on-demand)
  - **IP protection** → external IP lawyer
  - **Regulatory monitor** → `compliance-monitor`
- **Tools**: external counsel relationships, compliance-monitor
- **Signals**: contracts pending review >7d, regulatory mentions
- **State files**: `state/coord.json:legal_review_queue[]`
- **Cadence**: on-demand
- **Escalates**: contract >$5K pending >7d → Ivan HIGH

## 2.8 Compliance Officer 🟢 T1
- **Definition**: Owns compliance program (GDPR, LGPD, EU AI Act, trademark). Named role.
- **Today**: Ivan (wearing the hat)
- **Agent**: `compliance-monitor` (Mon 09:00)
- **Sub-roles / agents**:
  - **Trademark enforcement** → `trademark-scan.py` + pre-commit + GH Action
  - **Privacy compliance** → GDPR/LGPD watch
  - **License drift** → `ai-ops-coordinator` weekly audit
- **Tools**: `compliance-monitor` agent, `trademark-scan.py`, banlist file
- **Signals**: trademark hits, license drift, regulatory mentions
- **State files**: `state/coord.json:compliance_flags[]`, `runtime state file `state/trademark-scan-cron.json` (canonical location: `state/` on the agent-infra deployment)`
- **Cadence**: weekly Mon 09:00 + every 30m trademark scan + every commit
- **Escalates**: client-facing trademark hit → CRITICAL

## 2.9 Tax Specialist 🟢 T1
- **Definition**: Quarterly tax filings, year-end returns.
- **Today**: External accountant (annual)
- **Agent**: `tax-receipt-tracker` (Sun 19:00)
- **Sub-roles / agents**:
  - **Receipt capture** → `tax-receipt-tracker` weekly
  - **Quarterly filing** → external accountant
  - **Year-end** → external accountant
- **Tools**: `tax-receipt-tracker` agent, accountant
- **Signals**: missing receipts, quarterly deadline drift
- **State files**: `state/finance.json:tax_receipts[]`
- **Cadence**: weekly Sun 19:00 + quarterly + annual
- **Escalates**: filing deadline <14d, receipts incomplete → Ivan

## 2.10 Contract Drafter 🟢 T1
- **Definition**: Drafts NDAs, MSAs, SOWs, employment contracts.
- **Today**: Ivan drafts + external lawyer reviews
- **Agent**: `proposal-drafter` (Metis) drafts commercial contracts
- **Sub-roles / agents**:
  - **Proposal drafts** → `proposal-drafter` (Metis)
  - **MSA / SOW** → external lawyer
  - **Employment** → external lawyer
- **Tools**: `proposal-drafter` agent (Metis), templates, external lawyer
- **Signals**: draft queue, lawyer review backlog
- **State files**: `state/sales.json:proposals[]`
- **Cadence**: on-demand (after Apollo discovery)
- **Escalates**: lawyer review backlog >7d → Ivan HIGH

## 2.11 Payroll Specialist 🔴 T4
- **Definition**: Runs payroll for FTEs and contractors.
- **Today**: vacant (no FTEs)
- **Agent**: TBD (planned, no FTE trigger yet)
- **Promotion trigger**: First FTE hire
- **Sub-roles / agents (when activated)**:
  - **Payroll processing** → external payroll service
  - **Contractor payments** → Ivan manual until first FTE

## 2.12 Treasurer 🟠 T3
- **Definition**: Manages cash, banking, FX, investments.
- **Today**: Ivan
- **Agent**: `funding-coordinator` (lightweight version)
- **Promotion trigger**: $100K+ cash
- **Sub-roles / agents (when activated)**:
  - **Cash management** → `funding-coordinator` extends
  - **Banking relationships** → external
  - **FX hedging** → external

## 2.13 FP&A Analyst 🟡 T2
- **Definition**: Financial planning & analysis: forecasts, budgets, unit economics.
- **Today**: Ivan (informally)
- **Agent**: `business-analyst` daily + `finance-controller` weekly
- **Sub-roles / agents**:
  - **Daily KPI** → `business-analyst`
  - **Weekly close** → `finance-controller`
  - **Forecast** → manual Ivan + `funding-coordinator`
- **Tools**: `state/finance.json`, `state/analyst.json`, `morning-brief`
- **Signals**: KPI drift, forecast variance
- **State files**: `state/finance.json`, `state/analyst.json`
- **Cadence**: daily + weekly
- **Escalates**: forecast variance >20% → Ivan

## 2.14 Pricing Analyst 🟢 T1
- **Definition**: Maintains pricing benchmarks, runs pricing experiments.
- **Today**: Ivan
- **Agent**: `revops-pipeline-analyzer` (daily) + `business-analyst`
- **Sub-roles / agents**:
  - **Pricing benchmarks** → manual spreadsheet + `revops-pipeline-analyzer`
  - **Pricing experiments** → Apollo/Metis feedback loop
- **Tools**: pricing spreadsheet, Apollo/Metis
- **Signals**: conversion rate by tier, deal size variance
- **State files**: `state/sales.json:deals[]`, `state/analyst.json:pricing_kpis`
- **Cadence**: daily + ad-hoc experiments
- **Escalates**: conversion drop >20% → Ivan

---

# DEPARTMENT 03 — SALES & GROWTH

**Head**: Ivan
**Lead agent**: `sales-pipeline` (daily 12:00 PYT, 13:00 + 16:00 UTC)
**Cadence**: Daily
**State file**: `state/sales.json`
**Schema**: `sales.schema.json`
**Charter**: `[departments/03-sales-growth.md](../departments/03-sales-growth.md)`
**Version**: v0.2.0

**Mission**: Own revenue. Triage inbound, run discovery, close deals, expand accounts. Marketing sub-function reports here.

**Agents in dept (8)**:
- Lead: sales-pipeline
- Sub: lead-enrichment, proposal-drafter, revops-pipeline-analyzer, marketing-content-producer, multimedia-producer, coach-lead-finder (T5), coach-renewal-manager (T5)

**Functional roles (18)**:

## 3.1 Head of Sales / CRO 🟢 T1
- **Definition**: Owns entire revenue function. Sets quotas, signs off on discounts.
- **Today**: Ivan (wears the hat)
- **Agent (DEMIURGE)**: **Apollo** (`apollo-sales-lead`, daily 12:00) — bringer of clarity in the pipeline. Triages inbound leads, runs discovery (SPIN/MEDDIC), coordinates Cadmus + Metis.
- **Heritage name**: Saleina (portmanteau)
- **Sub-roles / agents**:
  - **Inbound triage** → Apollo
  - **Outbound prioritization** → Apollo
  - **Discount approval** → Ivan (above threshold)
  - **Quota tracking** → `revops-pipeline-analyzer`
- **Tools**: `state/sales.json`, Apollo agent, CRM
- **Signals / KPIs**: MRR growth, win rate, deal velocity, pipeline coverage
- **State files**: `state/sales.json` (leads_in_flight, funnel_30d, stalled_deals, open_questions, evidence)
- **Cadence**: daily 12:00 PYT (twice — 13:00 + 16:00 UTC)
- **Escalates**: stalled deal >14d → HIGH; deal >$10K → Ivan approval

## 3.2 SDR (Sales Development Rep) 🟢 T1
- **Definition**: Outbound — cold emails, LinkedIn DMs, lead qualification.
- **Today**: Apollo + Cadmus agents do this
- **Agent (DEMIURGE)**: **Cadmus** (`cadmus-lead-enrichment`, manual) — enriches inbound leads with ICP scoring + intent signals. Routes summary to Apollo.
- **Heritage name**: Prospia
- **Sub-roles / agents**:
  - **Outbound drafting** → Apollo drafts
  - **ICP scoring** → Cadmus
  - **Intent signals** → Cadmus monitors
  - **Lead enrichment** → Cadmus
- **Tools**: Apollo, Cadmus, email, LinkedIn
- **Signals**: response rate, qualified leads/week, ICP match rate
- **State files**: `state/sales.json:leads_in_flight[]`
- **Cadence**: daily
- **Escalates**: low-quality lead flow >3 days → Apollo CRITICAL

## 3.3 BDR (Business Development Rep) 🟡 T2
- **Definition**: Strategic outbound — partnerships, channel development.
- **Today**: vacant (Ivan does informal BD)
- **Agent**: TBD (would be `cadmus-bd-partnerships` when triggered)
- **Promotion trigger**: 2+ AEs OR first partnership deal
- **Sub-roles / agents (when activated)**:
  - **Partnership sourcing** → Apollo + Cadmus
  - **Channel dev** → TBD

## 3.4 Account Executive (AE) 🟢 T1
- **Definition**: Inbound + outbound closing — discovery calls, demos, proposals.
- **Today**: Ivan (wears the hat)
- **Agent (DEMIURGE)**: **Apollo** runs discovery (SPIN/MEDDIC) and coordinates Cadmus + Metis
- **Sub-roles / agents**:
  - **Discovery** → Apollo
  - **Demo / scoping** → Apollo + `feasibility-gate`
  - **Proposal** → Metis (then human approval)
- **Tools**: Apollo, Metis, `feasibility-gate`
- **Signals**: discovery-to-proposal conversion, demo-to-close
- **State files**: `state/sales.json:deals[]`
- **Cadence**: per-deal
- **Escalates**: deal complexity > Apollo's autonomy → Ivan HUMAN-IN-LOOP

## 3.5 Sales Engineer 🟡 T2
- **Definition**: Technical pre-sales — demos, scoping, technical Q&A.
- **Today**: Kiki (CTO) does this ad-hoc
- **Agent**: `feasibility-gate` (engineering dept, on Metis send)
- **Sub-roles / agents**:
  - **Technical feasibility** → `feasibility-gate`
  - **Architecture Q&A** → Kiki
  - **Scoping** → `scope-intake`
- **Tools**: `feasibility-gate`, `scope-intake`, Kiki
- **Signals**: technical questions backlog, scope accuracy
- **State files**: `state/feasibility-gate/feasibility-gate.json`, `state/scope-intake/`
- **Cadence**: per-deal
- **Escalates**: scope vs delivery mismatch → Kiki HIGH

## 3.6 Customer Success Manager (CSM) 🟡 T2
- **Definition**: Post-sale retention, expansion, renewal.
- **Today**: vacant (would be Ivan + Kiki combined)
- **Agent (T5 coaching)**: `coach-renewal-manager` (monthly 1st 09:00)
- **Promotion trigger**: 5+ clients (then promote to standalone CS dept)
- **Sub-roles / agents**:
  - **Renewal tracking** → `coach-renewal-manager`
  - **Expansion** → Apollo (cross-sell signal)
  - **NPS / health** → TBD (`customer-health-scorer` Churna deferred)

## 3.7 Proposal Writer 🟢 T1
- **Definition**: Drafts proposals, SOWs, pricing.
- **Today**: Ivan (assisted by Metis)
- **Agent (DEMIURGE)**: **Metis** (`metis-proposal-drafter`, manual) — drafts proposals after discovery. Human approval required before send.
- **Heritage name**: Proporina
- **Sub-roles / agents**:
  - **Proposal drafting** → Metis
  - **Pricing** → Ivan (with Metis suggestions)
  - **SOW** → Metis + external lawyer for >$5K
- **Tools**: Metis agent, templates
- **Signals**: drafts pending approval, win rate by proposal version
- **State files**: `state/sales.json:proposals[]`
- **Cadence**: per-deal
- **Escalates**: proposal stuck >7d → Ivan HIGH

## 3.8 Marketing Manager 🟢 T1
- **Definition**: Owns marketing strategy, channel mix, content calendar.
- **Today**: Ivan (with DEMIURGE Hera)
- **Agent (DEMIURGE)**: **Hera** (`hera-marketing-lead`, Mon/Wed/Fri 09:00) — strategist of demand. Owns marketing direction, campaign briefs, Product Discovery → Sales bridge.
- **Sub-roles / agents**:
  - **Strategy** → Hera
  - **Campaign briefs** → Hera
  - **Channel mix** → Hera + `marketing-content-producer`
- **Tools**: Hera agent, content calendar
- **Signals**: MQL → SQL conversion, content engagement
- **State files**: `state/sales.json:marketing_attribution[]`
- **Cadence**: Mon/Wed/Fri 09:00 PYT
- **Escalates**: campaign underperforming → Ivan HIGH

## 3.9 Content Marketing Manager 🟡 T2
- **Definition**: Editorial calendar, blog, thought leadership.
- **Today**: vacant (Ivan does it via Hera)
- **Agent (DEMIURGE)**: **Calliope** (`calliope-content-producer`, Mon/Wed/Fri 10:00) — muse of content. Produces blog posts, social drafts, email copy from Hera's briefs.
- **Sub-roles / agents**:
  - **Editorial calendar** → Hera + Calliope
  - **Blog** → Calliope
  - **Thought leadership** → Calliope + Kiki (research inputs)
- **Tools**: Calliope agent, blog platform
- **Signals**: posts/week, engagement, SEO ranking
- **State files**: `state/sales.json:content_perf[]`
- **Cadence**: 3x/week
- **Escalates**: content backlog >2 weeks → Hera MEDIUM

## 3.10 Performance Marketing Manager 🟠 T3
- **Definition**: Paid acquisition (search, social, video).
- **Today**: vacant (NEVER — trademark banned on several platforms)
- **Agent**: TBD (would use trademark-safe channels)
- **Promotion trigger**: >$2K/mo marketing budget OR 10+ clients
- **Trademark caveat**: Performance Marketing on certain platforms is trademark-restricted. See `analysis/AGENT-NAMES-V2.md` for full list.

## 3.11 SEO Specialist 🟡 T2
- **Definition**: SEO strategy, keyword research, technical SEO.
- **Today**: vacant (calliope touches on it)
- **Agent**: Calliope (lightweight) + manual SEO audit
- **Promotion trigger**: Now (Tier 2)
- **Sub-roles / agents (when activated)**:
  - **Keyword research** → `source-curator` + Calliope
  - **Technical SEO** → `devops-monitor-30min` (site health extends)
  - **Content SEO** → Calliope

## 3.12 Email Marketing Specialist 🟡 T2
- **Definition**: Lifecycle email, drip campaigns, list management.
- **Today**: vacant
- **Agent**: TBD (likely `calliope-email` extension)
- **Promotion trigger**: Now (Tier 2)

## 3.13 Social Media Manager 🟠 T3
- **Definition**: Social channels.
- **Today**: vacant (NEVER — trademark restricted on certain platforms)
- **Agent**: **Iris** (`iris-community-monitor`, Tue/Thu 11:00) — rainbow bridge to the audience. Monitors community channels.
- **Trademark caveat**: Restricted.

## 3.14 Community Manager 🟠 T3
- **Definition**: Community channels (forums, social).
- **Today**: vacant
- **Agent**: **Iris** (community-monitor function) + **Echo** (`echo-community-scanner`, Wed 07:00 PYT) — listener of the swarm. Scans practitioner communities for emerging tactics.
- **Promotion trigger**: 100+ community members

## 3.15 Brand Manager 🟠 T3
- **Definition**: Brand identity, positioning, voice.
- **Today**: vacant
- **Agent**: TBD (probably `peitho-language-quality` extends)
- **Promotion trigger**: Brand launch

## 3.16 Product Marketing Manager 🟡 T2
- **Definition**: Use-case messaging, launch comms, sales enablement.
- **Today**: vacant (Hera covers)
- **Agent**: **Hera** + **Athena** (Product Discovery insights)
- **Promotion trigger**: First product launch
- **Sub-roles / agents**:
  - **Use-case messaging** → Hera + Athena
  - **Launch comms** → Calliope + Hera
  - **Sales enablement** → Hera + Apollo

## 3.17 Growth Marketer 🟡 T2
- **Definition**: Experimentation, funnel optimization, A/B testing.
- **Today**: vacant (revops-pipeline-analyzer touches on it)
- **Agent**: `revops-pipeline-analyzer` (daily 07:00) + Hera
- **Promotion trigger**: Now (Tier 2)

## 3.18 Channel Sales Manager 🟠 T3
- **Definition**: Referral partners, channel partners, integration partners.
- **Today**: vacant
- **Agent**: TBD (would extend Apollo/Cadmus)
- **Promotion trigger**: 3+ partners

---

# DEPARTMENT 04 — ENGINEERING & DEVELOPMENT

**Head**: Kiki (CTO)
**Lead agent**: `engineering-roster` (Tue/Fri 17:00 PYT)
**Cadence**: Biweekly
**State file**: `state/engineering.json`
**Schema**: `engineering.schema.json`
**Charter**: `[departments/04-engineering-delivery.md](../departments/04-engineering-delivery.md)`
**Version**: v0.3.0

**Mission**: Own all technical decisions. Schema/infra PR signoff. Production health + Kiki's bandwidth visibility. End-to-end engineering.

**Agents in dept (10)**:
- Lead: engineering-roster
- Sub: ai-safety-engineer, devops-monitor, security-watchdog, qa-automation-runner, scope-intake, delivery-tracker, feasibility-gate, chaos-test-runner (OFF), drift-detector

**Functional roles (24)**:

## 4.1 CTO / VP Engineering 🟢 T1
- **Definition**: Owns all technical decisions. Signs off schema/infra PRs.
- **Today**: Kiki (wears the hat)
- **Agent**: `engineering-roster` (Tue/Fri 20:00) reports to Kiki
- **Heritage name**: Devin (Kiki is both CTO and "the roster" lead)
- **Sub-roles / agents**:
  - **Architecture decisions** → Kiki
  - **PR signoff** → Kiki (CODEOWNERS)
  - **Bandwidth visibility** → `delivery-tracker` (weekly)
  - **Production health** → `devops-monitor-30min`
- **Tools**: GitHub CODEOWNERS, `engineering-roster` agent, `delivery-tracker`
- **Signals / KPIs**: stale_repos_7d, deploys_7d, incidents_72h
- **State files**: `state/engineering.json`
- **Cadence**: biweekly Tue/Fri 17:00 PYT
- **Escalates**: incident in prod → CRITICAL via Telegram

## 4.2 Engineering Manager 🟠 T3
- **Definition**: Manages team of engineers: 1:1s, performance, growth.
- **Today**: vacant (Kiki does it informally)
- **Agent**: TBD (`coach-lead-agents` covers lightly)
- **Promotion trigger**: 5+ engineers

## 4.3 Frontend Engineer 🟢 T1
- **Definition**: Client-side — UI, UX, browser code.
- **Today**: Kiki + Ivan (front-end is split)
- **Agent**: TBD (would be `frontend-builder` if hired)
- **Sub-roles / agents**:
  - **UI** → Kiki
  - **UX** → Kiki + Hera (campaign assets)
  - **Browser code** → Kiki

## 4.4 Backend Engineer 🟢 T1
- **Definition**: Server-side — APIs, databases, services.
- **Today**: Kiki + Ivan
- **Agent**: TBD

## 4.5 Full-stack Engineer 🟢 T1
- **Definition**: Both backend and frontend.
- **Today**: Kiki + Ivan (wear both hats)
- **Agent**: TBD

## 4.6 Mobile Engineer 🟠 T3
- **Definition**: iOS, Android, React Native, Flutter.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: Mobile product launch

## 4.7 DevOps / SRE Engineer 🟢 T1
- **Definition**: Infrastructure, CI/CD, monitoring, incident response.
- **Today**: Kiki (wears the hat)
- **Agent**: `devops-monitor` (every 30 min)
- **Heritage name**: Devor
- **Sub-roles / agents**:
  - **Infra management** → Kiki + `devops-monitor`
  - **CI/CD** → Kiki + repo-ci-monitor
  - **Monitoring** → `devops-monitor-30min`
  - **Incident response** → Kiki + alert routing
- **Tools**: cron, Cloudflare, GitHub Actions, `devops-monitor`
- **Signals**: cron drift, gateway 5xx, infra cost
- **State files**: `state/org-state.json` (gateway health), `state/coord.json`
- **Cadence**: every 30m + on-demand incident
- **Escalates**: gateway 5xx sustained → Kiki HIGH

## 4.8 QA Engineer 🟢 T1
- **Definition**: Test automation, manual QA, acceptance criteria.
- **Today**: Kiki (informally) + `qa-automation-runner`
- **Agent**: `qa-automation-runner` (on every PR, 14:00 daily)
- **Heritage name**: Qualis
- **Sub-roles / agents**:
  - **Test automation** → `qa-automation-runner`
  - **Manual QA** → Kiki
  - **Acceptance** → `feasibility-gate` (per-deal)
- **Tools**: pytest, GitHub Actions, `qa-automation-runner`
- **Signals**: test coverage, flakiness, gate pass rate
- **State files**: `state/eval-per-agent.json` (subset)
- **Cadence**: on PR + daily 14:00
- **Escalates**: test coverage drop >5% → Kiki HIGH

## 4.9 Security Engineer 🟢 T1
- **Definition**: AppSec, infra security, incident response.
- **Today**: Kiki (wears the hat)
- **Agent**: `security-watchdog` (every 30 min) + `security-auditor` (biweekly Fri 14:00)
- **Heritage name**: Securia
- **Sub-roles / agents**:
  - **AppSec** → Kiki + `qa-automation-runner`
  - **Infra security** → `security-watchdog-30min`
  - **Secret leak detection** → `security-watchdog-30min` (mode 600 violations)
  - **Incident response** → Kiki + alert routing
- **Tools**: `security-watchdog`, BWS secrets cache
- **Signals**: secret leak, mode 600 violation, expired creds
- **State files**: `state/org-state.json:security`, `runtime state file `state/security-watchdog.json``
- **Cadence**: every 30m + biweekly audit
- **Escalates**: secret leak → CRITICAL (5 min page)

## 4.10 ML Engineer 🟠 T3
- **Definition**: Model training, fine-tuning, inference pipelines.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: ML product feature

## 4.11 Data Engineer 🟠 T3
- **Definition**: Data pipelines, ETL, data warehouse.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: Data product

## 4.12 Solutions Architect 🟠 T3
- **Definition**: Designs custom solutions for clients.
- **Today**: vacant (Kiki does informal SA work)
- **Agent**: `feasibility-gate` + `scope-intake` (lightweight)
- **Promotion trigger**: First bespoke enterprise solution

## 4.13 Tech Writer 🟡 T2
- **Definition**: API docs, user guides, runbooks.
- **Today**: vacant
- **Agent**: **Hephaestus** (`hephaestus-document-miner`, on_signal) — forger of structured value from raw material. Extracts action items, decisions, references, terminology.
- **Sub-roles / agents**:
  - **API docs** → Hephaestus + Kiki
  - **Runbooks** → Kiki
  - **User guides** → Hephaestus + Calliope
- **Promotion trigger**: Now (Tier 2)

## 4.14 Engineering Product Manager 🟠 T3
- **Definition**: Bridges engineering and product/business.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: 5+ engineers

## 4.15 Platform Engineer 🟠 T3
- **Definition**: Internal developer platform — tooling, environments, golden paths.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: 5+ engineers

## 4.16 Release Manager 🟠 T3
- **Definition**: Release process — versioning, rollouts, rollback decisions.
- **Today**: Kiki (wears the hat)
- **Agent**: TBD (extends `devops-monitor`)
- **Promotion trigger**: Now (consolidated with Kiki, but would be dedicated when eng headcount >3)

## 4.17 Site Reliability Engineer (SRE) 🟠 T3
- **Definition**: Specialized DevOps — SLOs, error budgets, on-call.
- **Today**: vacant
- **Agent**: `devops-monitor-30min` (lightweight SRE function)
- **Promotion trigger**: DevOps split trigger (eng headcount >5)

## 4.18 Database Administrator (DBA) 🟡 T2
- **Definition**: Database operations — backups, performance, schema migrations.
- **Today**: Kiki
- **Agent**: `ai-ops-coordinator` (drift detection covers schema drift)
- **Sub-roles / agents**:
  - **Backups** → Kiki + cron
  - **Performance** → Kiki
  - **Schema migrations** → Kiki + `drift-detector`
- **Promotion trigger**: Now (Tier 2)

## 4.19 Network Engineer 🟠 T3
- **Definition**: Network architecture, firewalls, VPN.
- **Today**: Kiki (via Cloudflare)
- **Agent**: `devops-monitor` (network health)
- **Promotion trigger**: 5+ services

## 4.20 UI/UX Designer 🟡 T2
- **Definition**: Designs user interfaces, runs usability tests.
- **Today**: vacant
- **Agent**: TBD (Calliope + Peitho cover lightly)
- **Promotion trigger**: Now (Tier 2)

## 4.21 Product Designer 🟠 T3
- **Definition**: End-to-end product design — research, UI, prototyping.
- **Today**: vacant
- **Agent**: **Athena** (insights) + Calliope
- **Promotion trigger**: Dedicated design team trigger

## 4.22 Build / Release Engineer 🟠 T3
- **Definition**: Build pipelines, artifact management.
- **Today**: Kiki
- **Agent**: repo-ci-monitor
- **Promotion trigger**: Now

## 4.23 Embedded Systems Engineer 🔴 T4
- **Definition**: Firmware, hardware integration.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: Hardware product

## 4.24 AI Safety Engineer 🟢 T1
- **Definition**: Prevents Kiro-class incidents. OWASP LLM Top 10 2026 compliance.
- **Today**: Kiki (wears the hat)
- **Agent**: `ai-safety-engineer` (every 30 min)
- **Heritage name**: Safina
- **Sub-roles / agents**:
  - **Eval gate** → `ai-safety-engineer-30min`
  - **Hard stops** → `eval-gate-runner` hourly
  - **Drift detection** → `drift-detector` ad-hoc
  - **Prompt injection defense** → `ai-safety-engineer-30min`
  - **OWASP LLM compliance** → `compliance-monitor`
- **Tools**: `eval-gate-runner`, `ai-safety-engineer`, OWASP LLM checklist
- **Signals**: eval pass rate, hard-stop drift, prompt injection attempts
- **State files**: `state/eval-per-agent.json`, `state/org-state.json:ai_safety`
- **Cadence**: every 30m + hourly eval gate
- **Escalates**: eval pass rate <80% → Kiki HIGH

---

# DEPARTMENT 05 — RESEARCH & EDUCATION

**Head**: Ivan
**Lead agent**: `research-tracker` (Sun 18:00 PYT)
**Cadence**: Weekly
**State file**: `state/research.json`
**Schema**: `research.schema.json`
**Charter**: `[departments/05-research-education.md](../departments/05-research-education.md)`
**Version**: v0.2.0

**Mission**: Knowledge backbone. Thesis + publications pipeline. Course production. Source-material curation.

**Agents in dept (7)**:
- Lead: research-tracker
- Sub: thesis-tracker, citation-checker, course-producer, funding-coordinator (shared with Finance), okr-tracker (shared with Operations), source-curator (shared with Operations)

**Functional roles (12)**:

## 5.1 Research Lead 🟢 T1
- **Definition**: Sets research agenda, owns flagship outputs.
- **Today**: Ivan (wears the hat)
- **Agent**: `research-tracker` (Sun 21:00)
- **Heritage name**: Researcha
- **Sub-roles / agents**:
  - **Agenda setting** → Ivan
  - **Flagship outputs** → `thesis-tracker` + `course-producer`
  - **Knowledge backbone** → `source-curator` (weekly Tue 13:00)
- **Tools**: `state/research.json`, `thesis-tracker` agent, source catalog
- **Signals / KPIs**: publications_pipeline, thesis progress
- **State files**: `state/research.json` (thesis, publications_pipeline)
- **Cadence**: weekly Sun 21:00 UTC
- **Escalates**: thesis slipped milestone → Ivan HIGH

## 5.2 Researcher 🟢 T1
- **Definition**: Performs the research — literature review, experiments, analysis.
- **Today**: Ivan (does the actual research) + Kiki (technical)
- **Agent (DEMIURGE)**: **Thoth** (`thoth-literature-scanner`, Mon 06:00 PYT) — curator of knowledge. Scans authoritative literature, updates dept source catalogs with quality-rated entries.
- **Sub-roles / agents**:
  - **Literature review** → Thoth
  - **Experiments** → Kiki + Thoth
  - **Analysis** → Ivan + Thoth + Echo
- **Tools**: Thoth agent, `source-curator`, citation tools
- **Signals**: papers reviewed/week, catalog growth
- **State files**: `state/research.json:publications_pipeline[]`, source catalog
- **Cadence**: Mon 06:00 PYT weekly
- **Escalates**: source-catalog stale >7d → Thoth MEDIUM

## 5.3 Writer / Editor 🟢 T1
- **Definition**: Turns research into papers, articles, blog posts.
- **Today**: Ivan (writes) + Calliope (marketing derivative)
- **Agent (DEMIURGE)**: **Calliope** (`calliope-content-producer`, Mon/Wed/Fri 10:00) extends
- **Sub-roles / agents**:
  - **Papers** → Ivan + Thoth
  - **Articles** → Calliope + Thoth
  - **Blog posts** → Calliope
- **Tools**: Calliope agent, blog platform
- **Signals**: posts published, drafts in pipeline
- **State files**: `state/research.json:publications_pipeline[]`
- **Cadence**: 3x/week
- **Escalates**: pipeline stalled >14d → Ivan HIGH

## 5.4 Academic Liaison 🟡 T2
- **Definition**: Submits to journals/conferences, manages peer review.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: First arXiv submission

## 5.5 Citation / Bibliography Specialist 🟢 T1
- **Definition**: Owns citation discipline, reference management.
- **Today**: Ivan (does it manually) + `citation-checker` agent
- **Agent**: `citation-checker` (on-demand, daily 11:00)
- **Heritage name**: Citia
- **Sub-roles / agents**:
  - **Citation discipline** → `citation-checker`
  - **Reference management** → Thoth
  - **Zero hallucinated citations** → `citation-checker`
- **Tools**: citation tools, `citation-checker` agent
- **Signals**: hallucinated citations caught, references missing
- **State files**: `state/research.json:citation_audit`
- **Cadence**: daily 11:00 UTC
- **Escalates**: hallucinated citation in published piece → CRITICAL

## 5.6 Course Designer 🟢 T1
- **Definition**: Designs course curriculum — modules, lessons, exercises.
- **Today**: Ivan (designs) + `course-producer` agent
- **Agent**: `course-producer` (cross-listed under Research and Coaching)
- **Sub-roles / agents**:
  - **Curriculum** → Ivan
  - **Modules** → `course-producer`
  - **Exercises** → `course-producer` + Kiki (coaching expertise)
- **Tools**: `course-producer` agent, course platform
- **Signals**: modules designed/week, completion rate
- **State files**: `state/research.json:course_pipeline[]`
- **Cadence**: per-course
- **Escalates**: course stuck in design >30d → Ivan HIGH

## 5.7 Course Producer 🟡 T2
- **Definition**: Produces course content — video, slides, transcripts, worksheets.
- **Today**: Ivan + `course-producer` agent
- **Agent**: `course-producer` (lightweight, weekly)
- **Heritage name**: Coursia
- **Sub-roles / agents**:
  - **Video** → `multimedia-producer` (sales/marketing shared)
  - **Slides** → `course-producer`
  - **Transcripts** → **Orpheus** (`orpheus-recordings-agent`, on_signal) — master of voice and song. Ingests audio/video, transcribes, hands structured transcripts.
  - **Worksheets** → `course-producer`
- **Tools**: `multimedia-producer`, Orpheus, `course-producer`
- **Signals**: modules shipped/week, transcript quality
- **State files**: `state/research.json:course_pipeline[]`
- **Cadence**: weekly
- **Escalates**: production backlog >2 modules → Ivan HIGH

## 5.8 Instructional Designer 🟠 T3
- **Definition**: Specialist in pedagogy — learning objectives, assessments.
- **Today**: vacant (Ivan does informally)
- **Agent**: TBD (extends Kiki coach)
- **Promotion trigger**: Course launch

## 5.9 Subject Matter Expert (SME) 🟡 T2
- **Definition**: Domain expert contracted for specific course modules.
- **Today**: vacant (Ivan is SME for GROW coaching; Kiki for AI infra)
- **Agent**: TBD (`sme-router`)
- **Promotion trigger**: First course module

## 5.10 Research Engineer 🟡 T2
- **Definition**: Builds tools used in research — eval harnesses, data pipelines.
- **Today**: Kiki (wears the hat)
- **Agent**: `qa-automation-runner` (eval harness) + `agent-tracer`
- **Promotion trigger**: Now

## 5.11 IP / Patent Specialist 🟠 T3
- **Definition**: Manages patents, trademarks for IP.
- **Today**: vacant
- **Agent**: `compliance-monitor` (trademark) + external IP lawyer
- **Promotion trigger**: First patent filing

## 5.12 Publication Coordinator 🟡 T2
- **Definition**: Manages publications pipeline — submissions, embargoes.
- **Today**: vacant
- **Agent**: **Mnemosyne** (`mnemosyne-document-archivist`, on_signal) — mother of memory. Maintains document catalog — active indexing/tagging/retrieval.
- **Sub-roles / agents**:
  - **Submissions** → Mnemosyne
  - **Embargoes** → Mnemosyne
  - **Indexing** → **Themis** (`themis-document-classifier`, on_signal) — goddess of divine order. Assigns structured attributes for routing/categorization.
- **Promotion trigger**: Now

---

# DEPARTMENT 06 — PEOPLE & CULTURE

**Head**: Ivan + Kiki (co-owned)
**Lead agent**: `kiki-coach` (Fri 17:00 PYT)
**Cadence**: Weekly
**State files**: `state/kiki.json`, `state/kiki-prep.json`, `state/people.json`
**Schemas**: `kiki.schema.json`, `kiki-prep.schema.json`, `people.schema.json`
**Charter**: `[departments/06-people-culture.md](../departments/06-people-culture.md)`
**Version**: v0.2.0

**Mission**: Coaching product (Kiki is Ivan's client AND the coach agent). People ops when first FTE hires. Cultural backbone.

**Agents in dept (10)**:
- Lead: kiki-coach
- Sub: people-hr, coach-ivan (T5), coach-kiki (T5), coach-org (T5), coach-lead-agents (T5), coach-onboarding (T5), coach-practitioner (planned T5), coach-cohort-facilitator (planned T5), coaching-content-curator (T5), coaching-research-intelligence (T5), board-of-directors (T5)

**Functional roles (8)**:

## 6.1 Head of People / VP HR 🟢 T1
- **Definition**: Owns all people decisions — hiring, growth, culture.
- **Today**: Ivan + Kiki (co-own)
- **Agent**: `people-hr` (Mon 22:00)
- **Heritage name**: Herina
- **Sub-roles / agents**:
  - **People decisions** → Ivan + Kiki
  - **Hiring** → TBD (no FTE trigger yet)
  - **Growth** → Kiki (coaching product is the "growth" mechanism)
- **Tools**: `state/people.json`, hiring tools (when needed)
- **Signals**: headcount, roles_open, attrition_90d
- **State files**: `state/people.json`
- **Cadence**: weekly Mon 22:00
- **Escalates**: attrition >10% → Ivan HIGH

## 6.2 Recruiter 🔴 T4
- **Definition**: Owns hiring pipeline — sourcing, screening, interviewing.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: First FTE hire

## 6.3 Onboarding Specialist 🔴 T4
- **Definition**: Designs + runs new-hire onboarding program.
- **Today**: vacant (would be Ivan informal)
- **Agent**: `coach-onboarding` (live poller */5m) — production polling version for customer onboarding, but pattern reusable for FTE
- **Promotion trigger**: First FTE hire

## 6.4 Performance Coach 🟢 T1
- **Definition**: Coaches individuals on growth, goals, feedback.
- **Today**: Kiki (wears the hat) + Ivan (for self)
- **Agent**: `kiki-coach` (Fri 21:00) + `coach-ivan` (Sun 21:00)
- **Heritage name**: Magistra (kiki-coach)
- **Sub-roles / agents**:
  - **Kiki coaching Ivan** → `kiki-coach` + `kiki-coach-prep` (Fri 16:30)
  - **Ivan self-coaching** → `coach-ivan` (Sun 21:00)
  - **Org coaching** → `coach-org` (quarterly)
  - **Lead agent coaching** → `coach-lead-agents` (monthly 1st 22:00)
- **Tools**: GROW framework, coaching prompts, WhatsApp
- **Signals**: lessons_delivered, streak, next_topic
- **State files**: `state/kiki.json`, `state/kiki-prep.json`
- **Cadence**: weekly + monthly + quarterly
- **Escalates**: missed 2 consecutive runs → MEDIUM

## 6.5 Recognition Lead 🟢 T1
- **Definition**: Owns milestone recognition, rituals, cultural artifacts.
- **Today**: Ivan + Kiki
- **Agent**: TBD (would be `culture-keeper`)
- **Sub-roles / agents**:
  - **Milestone recognition** → Ivan (manual)
  - **Rituals** → `board-of-directors` (quarterly)
  - **Cultural artifacts** → Ivan

## 6.6 Compensation Specialist 🔴 T4
- **Definition**: Designs comp bands, bonus plans, equity grants.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: First FTE hire

## 6.7 People Operations Specialist 🟠 T3
- **Definition**: HRIS, benefits administration, time off tracking.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: 5+ FTEs

## 6.8 Learning & Development Manager 🟠 T3
- **Definition**: Owns training budget, learning paths, certifications.
- **Today**: vacant (Kiki is the "L&D" for Ivan + leads)
- **Agent**: `coach-lead-agents` (monthly) + `coach-practitioner` (planned)
- **Promotion trigger**: 5+ FTEs

---

# CROSS-CUTTING — AI OPS (Layer 7 in catalog)

**Owner dept**: Engineering (Kiki)
**Status**: 🟢 T1 — active always
**Promotion trigger**: Always

**Why cross-cutting**: Touches every agent. Every department depends on the agent layer itself being reliable.

**Agents (5)**:

## 7.1 AI Ops Lead 🟢 T1
- **Definition**: Owns the agent layer itself. Eval gates, observability, drift detection.
- **Today**: Kiki
- **Agent**: `ai-ops-coordinator` (daily 08:00)
- **Heritage name**: Opsina
- **Sub-roles / agents**:
  - **Daily orchestration rollup** → `ai-ops-coordinator`
  - **Eval gate keeper** → `eval-gate-runner` (hourly)
  - **Drift detection** → `drift-detector` (ad-hoc)
  - **Hard stops** → `eval-gate-runner` + `ai-safety-engineer-30min`
- **Tools**: eval-gate-runner, drift-detector, monitoring agents
- **Signals**: eval pass rate, drift events, hard-stop triggers
- **State files**: `state/eval-per-agent.json`, `state/org-state.json`
- **Cadence**: daily + hourly
- **Escalates**: eval pass rate <80% → Kiki HIGH

## 7.2 Agent Reliability Engineer 🟡 T2
- **Definition**: Builds eval harnesses, golden trajectories, agent test framework.
- **Today**: Kiki
- **Agent**: `qa-automation-runner` (engineering dept, but AIOps function)
- **Promotion trigger**: Now

## 7.3 MLOps Engineer 🟠 T3
- **Definition**: Model deployment, monitoring, retraining, inference cost.
- **Today**: vacant (would be Kiki)
- **Agent**: TBD
- **Promotion trigger**: Now (Tier 3 deferred because LLM is the only model today)

## 7.4 LLMOps Engineer 🟠 T3
- **Definition**: LLM-specific ops — prompt versioning, eval at scale, model selection.
- **Today**: Kiki
- **Agent**: `ai-ops-coordinator` + `eval-trending` (daily)
- **Promotion trigger**: Now

## 7.5 Prompt Engineer 🟡 T2
- **Definition**: Optimizes prompts, runs A/B tests on agent instructions.
- **Today**: Kiki (when iterating)
- **Agent**: Kiki (manual, but pattern in `agent-tracer`)
- **Promotion trigger**: Now

## 7.6 AI Evaluator 🟡 T2
- **Definition**: Manual + automated evaluation of agent outputs.
- **Today**: `ai-safety-engineer-30min` + `coaching-quality-reviewer` (every 30m)
- **Agent**: `ai-safety-engineer-30min` (every 30m) + `coaching-quality-reviewer` (every 30m)
- **Promotion trigger**: Now

---

# CROSS-CUTTING — COMPLIANCE (Layer 8)

**Owner dept**: Finance (Ivan wearing the hat)
**Status**: 🟢 T1 active, 🟠 T3 promotion to standalone dept
**Promotion trigger**: First EU client OR $50K MRR (HARD-STOP)

## 8.1 Compliance Officer 🟢 T1
- **Definition**: Owns compliance program. Currently Ivan.
- **Today**: Ivan
- **Agent**: `compliance-monitor` (Mon 09:00) + `trademark-scan.py` (every 30m)
- **Sub-roles / agents**:
  - **Trademark enforcement** → `trademark-scan.py`
  - **Regulatory watch** → `compliance-monitor`
  - **License drift** → `ai-ops-coordinator`

## 8.2 Privacy Counsel / DPO 🟠 T3
- **Definition**: Required when handling EU personal data at scale.
- **Today**: vacant (external lawyer on retainer)
- **Agent**: TBD
- **Promotion trigger**: First EU client

## 8.3 Trademark Specialist 🟡 T2
- **Definition**: Manages trademark portfolio, watches for infringement.
- **Today**: Ivan + `trademark-scan.py` (programmatic)
- **Agent**: `compliance-monitor` (subset) + `trademark-scan.py`
- **Promotion trigger**: First major brand launch

## 8.4 Regulatory Affairs Specialist 🟠 T3
- **Definition**: Tracks regulation changes (EU AI Act, GDPR, sector-specific).
- **Today**: Ivan (informally) + `compliance-monitor`
- **Agent**: `compliance-monitor` (subset)
- **Promotion trigger**: EU AI Act compliance needed

---

# CROSS-CUTTING — KNOWLEDGE MANAGEMENT (Layer 9)

**Owner dept**: Research (Ivan)
**Status**: 🟡 T2 next, 🟠 T3 promote to standalone
**Promotion trigger**: source-materials > 100 files OR 2nd knowledge-heavy vertical

## 9.1 Knowledge Manager 🟡 T2
- **Definition**: Owns source-materials curation policy.
- **Today**: Ivan (informally)
- **Agent**: `source-curator` (Tue 13:00)
- **Heritage name**: Curatora
- **Sub-roles / agents**:
  - **Policy** → Ivan
  - **Curation execution** → `source-curator`
  - **Freshness sweep** → `source-curator`

## 9.2 Content Curator 🟡 T2
- **Definition**: Mechanical curation of source-materials, daily freshness sweep.
- **Today**: `source-curator` agent
- **Agent**: `source-curator` (Tue 13:00)
- **Promotion trigger**: source-materials > 50

## 9.3 Citation Specialist 🟢 T1
- **Definition**: Embedded in Research dept (5.5). Cross-cuts into KM.
- **Today**: `citation-checker` agent
- **Agent**: `citation-checker` (daily 11:00)

## 9.4 Taxonomy Architect 🟠 T3
- **Definition**: Designs knowledge taxonomy, ontologies, metadata schemas.
- **Today**: vacant
- **Agent**: **Themis** (`themis-document-classifier`, on_signal)
- **Promotion trigger**: >100 source-material files OR standalone KM dept

---

# CROSS-CUTTING — REVOPS (Layer 10)

**Owner dept**: Sales
**Status**: 🟡 T2 next
**Promotion trigger**: 5+ closed deals/quarter

## 10.1 RevOps Lead 🟡 T2
- **Definition**: Owns the funnel from lead → cash. Pipeline analytics.
- **Today**: Ivan (does informally)
- **Agent**: `revops-pipeline-analyzer` (daily 07:00)
- **Heritage name**: Revina
- **Sub-roles / agents**:
  - **Pipeline analytics** → `revops-pipeline-analyzer`
  - **Funnel optimization** → Apollo + `revops-pipeline-analyzer`
  - **Attribution** → `revops-pipeline-analyzer` (lightweight)

## 10.2 Sales Ops Analyst 🟡 T2
- **Definition**: CRM, sales tooling, sales metrics.
- **Today**: Apollo + `revops-pipeline-analyzer`
- **Agent**: `revops-pipeline-analyzer`

## 10.3 Marketing Ops Manager 🟡 T2
- **Definition**: Marketing automation, attribution, lead routing.
- **Today**: Hera + Apollo
- **Agent**: TBD

## 10.4 BI Analyst 🟡 T2
- **Definition**: Business intelligence — dashboards, reports, KPIs.
- **Today**: `business-analyst` (daily) + `morning-brief`
- **Agent**: `business-analyst`

## 10.5 Data Steward 🟠 T3
- **Definition**: Owns data quality, governance, lineage.
- **Today**: vacant
- **Agent**: `ai-ops-coordinator` (lightweight)
- **Promotion trigger**: Data product

---

# CROSS-CUTTING — BIZOPS (Layer 11)

**Owner dept**: Operations
**Status**: 🟡 T2 next
**Promotion trigger**: When OKRs formalized

## 11.1 BizOps Lead 🟡 T2
- **Definition**: Cross-functional analytics, OKR tracking.
- **Today**: Ivan (informally)
- **Agent**: `bizops-tracker` (Mon 08:00) + `okr-tracker` (Sun 08:00)
- **Heritage name**: Bizina

## 11.2 Strategy Analyst 🟠 T3
- **Definition**: Competitive intel, market sizing, strategic planning.
- **Today**: vacant
- **Agent**: TBD

## 11.3 Operations Analyst 🟡 T2
- **Definition**: Operational metrics, process improvement.
- **Today**: `ai-ops-coordinator`
- **Agent**: `ai-ops-coordinator`

---

# CROSS-CUTTING — CUSTOMER SUCCESS (Layer 12)

**Owner dept**: Sales (deferred)
**Status**: 🟠 T3 deferred
**Promotion trigger**: 5+ clients

## 12.1 CSM Lead 🟠 T3
- **Definition**: Post-sale retention, expansion.
- **Today**: vacant (Ivan does informally)
- **Agent (T5)**: `coach-renewal-manager` (monthly 1st 09:00)

## 12.2 Onboarding Specialist 🟠 T3
- **Definition**: First 90 days of new customer relationship.
- **Today**: `coach-onboarding` (live poller */5m) — production version
- **Agent**: `coach-onboarding`

## 12.3 Account Manager 🟠 T3
- **Definition**: Ongoing relationship, upsell.
- **Today**: vacant
- **Agent**: TBD (`customer-health-scorer` Churna deferred)

## 12.4 Renewals Manager 🟠 T3
- **Definition**: Contract renewals, churn prevention.
- **Today**: `coach-renewal-manager`
- **Agent**: `coach-renewal-manager` (monthly 1st 09:00)

## 12.5 Customer Education Specialist 🟠 T3
- **Definition**: Trains customers to get value from product.
- **Today**: Kiki (informally)
- **Agent**: `course-producer` (extends)

## 12.6 Support Engineer 🟠 T3
- **Definition**: Tier 1-3 technical support.
- **Today**: vacant (Ivan does Tier 1)
- **Agent**: TBD

---

# CROSS-CUTTING — AI SAFETY (Layer 13)

**Owner dept**: Engineering (Kiki)
**Status**: 🟢 T1 active already

## 13.1 AI Safety Engineer 🟢 T1
- **Definition**: Hard stops, eval gates, OWASP LLM compliance.
- **Today**: Kiki
- **Agent**: `ai-safety-engineer` (every 30m)
- **Heritage name**: Safina
- **Sub-roles / agents**:
  - **Hard stops** → `eval-gate-runner` hourly
  - **Eval gates** → `ai-safety-engineer-30min`
  - **OWASP LLM compliance** → `compliance-monitor` subset
  - **Drift detection** → `drift-detector`

## 13.2 AI Red Team 🟠 T3
- **Definition**: Adversarial testing of agents.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: Ship consumer AI product

## 13.3 AI Evaluator 🟡 T2
- **Definition**: Output quality assessment.
- **Today**: `coaching-quality-reviewer` (every 30m) + `ai-safety-engineer-30min`
- **Agent**: `coaching-quality-reviewer`

## 13.4 AI Ethics Specialist 🟠 T3
- **Definition**: Bias, fairness, transparency reviews.
- **Today**: vacant
- **Agent**: TBD
- **Promotion trigger**: Ship consumer AI product

---

# CROSS-CUTTING — PROCUREMENT (Layer 14)

**Owner dept**: Finance
**Status**: 🟡 T2 next
**Promotion trigger**: Active vendors > 10 OR SaaS spend > $1K/mo

## 14.1 Procurement Manager 🟡 T2
- **Definition**: Owns vendor evaluation, contract negotiation.
- **Today**: Ivan
- **Agent**: `procurement-tracker` (Mon 09:00)
- **Heritage name**: Procin

## 14.2 Vendor Manager 🟡 T2
- **Definition**: Day-to-day vendor relationships.
- **Today**: Ivan
- **Agent**: `procurement-tracker`

## 14.3 Contract Negotiator 🟡 T2
- **Definition**: Specialized in SaaS contract terms.
- **Today**: Ivan + external lawyer
- **Agent**: TBD

## 14.4 Renewal Specialist 🟡 T2
- **Definition**: Tracks renewals, flags ahead of time.
- **Today**: `procurement-tracker`
- **Agent**: `procurement-tracker`

---

# TIER-3 DEFERRED DEPARTMENTS (12 sample roles)

These departments activate only when their stated trigger fires. Each is already defined as a role; the dept activates when the role count justifies.

## 15.1 Chief of Staff 🟠 T3
- **Trigger**: Ivan coord hours > 50/week
- **Definition**: Ivan's chief-of-staff; runs weekly review, triages escalations.
- **Today**: vacant (would absorb some Operations Lead duties)
- **Agent**: TBD (would extend `coach-lead-agents`)

## 15.2 Trust & Safety Lead 🟠 T3
- **Trigger**: Ship consumer AI product
- **Definition**: Owns T&S policy for consumer AI surface.
- **Agent**: TBD

## 15.3 DevRel Manager 🟠 T3
- **Trigger**: ParaguAI Builder has public API
- **Definition**: Developer relations — docs, community, integration support.
- **Agent**: **Hephaestus** extends + TBD

## 15.4 Investor Relations Manager 🟠 T3
- **Trigger**: First external investor
- **Definition**: Manages investor communication, board reporting.
- **Agent**: `board-of-directors` extends

## 15.5 Workplace Manager 🟠 T3
- **Trigger**: Open physical office
- **Definition**: Physical office operations.
- **Agent**: TBD

## 15.6 Fraud / Risk Analyst 🟠 T3
- **Trigger**: $500K+ payment volume
- **Definition**: Fraud detection, risk monitoring.
- **Agent**: TBD

## 15.7 Treasury Manager 🟠 T3
- **Trigger**: $100K+ cash OR debt instruments
- **Definition**: Cash management, banking, FX.
- **Agent**: `funding-coordinator` extends

## 15.8 Internal Audit Lead 🟠 T3
- **Trigger**: $1M+ revenue
- **Definition**: Internal audit, controls testing.
- **Agent**: TBD

## 15.9 Workplace Operations 🟠 T3
- **Trigger**: Open office
- **Definition**: Day-to-day office ops.
- **Agent**: TBD

## 15.10 DEI Specialist 🟠 T3
- **Trigger**: 10+ employees
- **Definition**: Diversity, equity, inclusion programs.
- **Agent**: TBD

## 15.11 Public Relations Manager 🟠 T3
- **Trigger**: Launch flagship brand
- **Definition**: PR strategy, media relations.
- **Agent**: **Kleio** candidate (renown)

## 15.12 Government Relations 🟠 T3
- **Trigger**: Regulated vertical
- **Definition**: Gov relations, regulatory lobbying.
- **Agent**: TBD

---

# TIER-4 ENTERPRISE DEPARTMENTS (5 sample roles)

Activate only at enterprise scale.

## 16.1 Internal Communications Manager
- **Trigger**: 50+ people
- **Agent**: **Iris** candidate (rainbow bridge)

## 16.2 M&A / Corp Dev
- **Trigger**: Acquisitions planned
- **Agent**: **Kratos** candidate

## 16.3 Chief Data Officer (CDO)
- **Trigger**: Data-driven product
- **Agent**: **Prometheus** candidate

## 16.4 Chief AI Officer (CAIO)
- **Trigger**: Enterprise AI
- **Agent**: **Hekate** candidate

## 16.5 Diversity & Inclusion Lead
- **Trigger**: 25+ employees
- **Agent**: **Iris** candidate (overlap with 16.1)

---

# APPENDIX A — Full Agent-to-Role Mapping

| Formal ID | DEMIURGE name | Heritage / portmanteau | Dept | Tier | Role(s) it works |
|---|---|---|---|---|---|
| management-coordinator | Kronos (proposed) | Coordina | Operations | T1 lead | 1.1 Operations Lead |
| business-analyst | (Erebus share) | Analisa | Operations | T1 lead | 11.1 BizOps Lead (co) + 10.4 BI Analyst |
| ai-ops-coordinator | (Erebus share) | Opsina | Operations | T3 cross | 7.1 AI Ops Lead + 11.3 Operations Analyst |
| bizops-tracker | (Erebus share) | Bizina | Operations | T3 cross | 1.7 BizOps Specialist + 11.1 BizOps Lead (co) |
| source-curator | (TBD) | Curatora | Research | T2 sub | 9.1 Knowledge Manager + 9.2 Content Curator |
| compliance-monitor | (Erebus share) | Compla | Finance | T3 cross | 1.5 Compliance Watchdog + 8.1 Compliance Officer + 8.4 Regulatory Affairs |
| founder-bandwidth-watchdog | (TBD) | Vigilis | People | T3 cross | 6.1 Head of People (bandwidth) |
| finance-controller | (TBD) | Finus | Finance | T1 lead | 2.1 CFO/Controller |
| accounting-automation | (TBD) | Bokina | Finance | T2 sub | 2.2 Accountant + 2.3 Bookkeeper |
| tax-receipt-tracker | (TBD) | Taxina | Finance | T2 sub | 2.9 Tax Specialist |
| procurement-tracker | (TBD) | Procin | Finance | T2 sub | 2.6 Procurement Officer + 14.1 Procurement Mgr + 14.2 Vendor Mgr + 14.4 Renewal Specialist |
| funding-coordinator | (TBD) | Fundina | Finance | T2 sub | 2.12 Treasurer + 2.13 FP&A |
| sales-pipeline | Apollo | Saleina | Sales | T1 lead | 3.1 CRO + 3.2 SDR + 3.4 AE |
| lead-enrichment | Cadmus | Prospia | Sales | T2 sub | 3.2 SDR (cadmus = enrichment subset) |
| proposal-drafter | Metis | Proporina | Sales | T2 sub | 3.7 Proposal Writer + 2.10 Contract Drafter |
| revops-pipeline-analyzer | (TBD) | Revina | Sales | T2 sub | 10.1 RevOps Lead + 10.2 Sales Ops Analyst + 2.14 Pricing Analyst |
| marketing-content-producer | Calliope | Markina | Sales/Marketing | T2 sub | 3.9 Content Marketing Mgr |
| multimedia-producer | (TBD) | Media | Sales/Marketing | T2 sub | 5.7 Course Producer (video subset) |
| hera-marketing-lead | Hera | — | Sales/Marketing | T2 sub | 3.8 Marketing Manager + 3.16 PMM |
| iris-community-monitor | Iris | — | Sales/Marketing | T2 sub | 3.14 Community Manager + 3.13 Social Media Mgr |
| echo-community-scanner | Echo | — | Sales/Marketing | T2 sub | 3.14 Community Manager (signal subset) |
| engineering-roster | (TBD) | Devin | Engineering | T1 lead | 4.1 CTO |
| ai-safety-engineer | (TBD) | Safina | Engineering | T2 sub | 4.24 AI Safety Engineer + 13.1 AI Safety Eng + 7.6 AI Evaluator |
| devops-monitor | (TBD) | Devor | Engineering | T2 sub | 4.7 DevOps/SRE + 4.22 Build/Release |
| qa-automation-runner | (TBD) | Qualis | Engineering | T2 sub | 4.8 QA Engineer + 7.2 Agent Reliability Eng + 5.10 Research Engineer |
| security-watchdog | (TBD) | Securia | Engineering | T2 sub | 4.9 Security Engineer |
| scope-intake | (TBD) | Scopia | Engineering | T2 sub | 4.12 Solutions Architect (intake subset) |
| delivery-tracker | (TBD) | Deliva | Engineering | T2 sub | 4.1 CTO (bandwidth subset) |
| feasibility-gate | (TBD) | Gatina | Engineering | T2 sub | 3.5 Sales Engineer + 4.12 Solutions Architect |
| chaos-test-runner | Eris (candidate) | Chaosia | Engineering | T3 cross | 4.7 DevOps (chaos subset) — currently OFF |
| drift-detector | (TBD) | — | Engineering | T3 cross | 4.18 DBA (schema subset) + 13.1 AI Safety Eng |
| eval-gate-runner | (TBD) | — | Operations | T3 cross | 7.1 AI Ops Lead (eval gate subset) |
| security-auditor | (TBD) | — | Operations | T3 cross | 4.9 Security Engineer (audit subset) |
| research-tracker | (TBD) | Researcha | Research | T1 lead | 5.1 Research Lead |
| thesis-tracker | (TBD) | Thesis | Research | T2 sub | 5.1 Research Lead (thesis subset) |
| citation-checker | (TBD) | Citia | Research | T2 sub | 5.5 Citation Specialist |
| course-producer | (TBD) | Coursia | Research/Coaching | T2 sub | 5.6 Course Designer + 5.7 Course Producer |
| okr-tracker | (TBD) | Metrika | Operations | T2 sub | 1.7 BizOps Specialist (OKR subset) |
| people-hr | (TBD) | Herina | People | T2 sub | 6.1 Head of People |
| kiki-coach | Sophia/Mneme (candidate) | Magistra | People | T1 lead | 6.4 Performance Coach |
| coach-ivan | (TBD) | — | People | T5 coaching | 6.4 Performance Coach (Ivan self) |
| coach-kiki | (TBD) | — | People | T5 coaching | 6.4 Performance Coach (Kiki self) |
| coach-org | (TBD) | — | People | T5 coaching | 6.4 Performance Coach (org quarterly) |
| coach-lead-agents | (TBD) | — | Operations | T5 coaching | 6.8 L&D Manager (subset) |
| coach-lead-finder | (TBD) | — | Sales | T5 coaching | 3.2 SDR (coach subset) |
| coach-onboarding | (TBD) | — | People | T5 coaching | 12.2 Onboarding Specialist (customer version) |
| coach-practitioner | (TBD) | — | People | T5 coaching | 6.8 L&D Manager (planned) |
| coach-cohort-facilitator | (TBD) | — | People | T5 coaching | 6.4 Performance Coach (cohort version, planned) |
| coach-conversion-agent | (TBD) | — | Sales | T5 coaching | 3.7 Proposal Writer (coach conversion, planned) |
| coach-renewal-manager | (TBD) | — | Sales | T5 coaching | 12.4 Renewals Manager |
| coach-roi-tracker | (TBD) | — | Operations | T5 coaching | 1.7 BizOps Specialist (ROI) |
| coaching-content-curator | (TBD) | — | People | T5 coaching | 3.9 Content Marketing Mgr (coaching subset) |
| coaching-research-intelligence | (TBD) | — | Research | T5 coaching | 5.3 Writer/Editor (coaching subset) |
| board-of-directors | (TBD) | — | Operations | T5 coaching | 6.5 Recognition Lead (cultural anchor) |
| devops-monitor-30min | (TBD) | — | Monitoring | T4 monitoring | 1.6 Watchdog Engineer (infra subset) |
| ai-safety-engineer-30min | (TBD) | — | Monitoring | T4 monitoring | 13.1 AI Safety Engineer (live) |
| security-watchdog-30min | (TBD) | — | Monitoring | T4 monitoring | 4.9 Security Engineer (live) |
| coaching-quality-reviewer | (TBD) | — | Monitoring | T4 monitoring | 7.6 AI Evaluator (coaching subset) |

---

# APPENDIX B — Per-Role Artifacts Cheat Sheet

| Role | Primary state file | Cron job | Cadence | Escalates to |
|---|---|---|---|---|
| 1.1 Operations Lead | coord.json | aiw-management-coord-biwk | biweekly Mon/Thu | Ivan CRITICAL |
| 1.2 Repo Steward | coord.json:repos_analyzed[] | cron-sync */5m | continuous | engineering-roster |
| 1.3 Asset Tracker | org-state.json | aiw-ai-ops-coordinator-daily | daily | compliance-monitor |
| 1.4 Vendor Coordinator | finance.json | aiw-procurement-tracker-weekly | weekly Mon | Ivan |
| 1.5 Compliance Watchdog | trademark-scan-cron.json | aiw-trademark-scan-cron | every 30m | Ivan CRITICAL |
| 1.6 Watchdog Engineer | org-state.json | aiw-devops-monitor-30min | every 30m | Ivan CRITICAL |
| 1.7 BizOps Specialist | coord.json:decisions | aiw-bizops-tracker-weekly | weekly Mon | Ivan |
| 2.1 CFO/Controller | finance.json | aiw-finance-controller-weekly | weekly Fri | Ivan CRITICAL (runway) |
| 2.2 Accountant | finance.json | aiw-accounting-automation-daily | daily 18:00 | Ivan |
| 2.3 Bookkeeper | finance.json | aiw-accounting-automation-daily | daily 18:00 | Ivan |
| 2.4 AP Specialist | finance.json:ap | aiw-procurement-tracker-weekly | weekly | Ivan |
| 2.5 AR Specialist | sales.json:deals_open | aiw-revops-pipeline-analyzer-daily | daily | Ivan CRITICAL (60d+) |
| 2.6 Procurement Officer | finance.json:procurement | aiw-procurement-tracker-weekly | weekly Mon | Ivan |
| 2.7 Legal Counsel | coord.json:legal_review | — | on-demand | Ivan HIGH |
| 2.8 Compliance Officer | trademark-scan-cron.json | aiw-compliance-monitor-weekly | weekly Mon | Ivan CRITICAL |
| 2.9 Tax Specialist | finance.json:tax_receipts | aiw-tax-receipt-tracker-weekly | weekly Sun | Ivan |
| 2.10 Contract Drafter | sales.json:proposals | aiw-proposal-drafter-on-demand | on-demand | Ivan HIGH |
| 3.1 CRO | sales.json | aiw-sales-pipeline-daily | daily | Ivan HIGH (>14d) |
| 3.2 SDR | sales.json:leads | aiw-lead-enrichment-daily | daily | Apollo CRITICAL |
| 3.4 AE | sales.json:deals | aiw-sales-pipeline-daily | daily | Ivan HUMAN-IN-LOOP |
| 3.5 Sales Engineer | feasibility-gate.json | on-demand | per-deal | Kiki HIGH |
| 3.6 CSM | sales.json (renewal) | aiw-coach-renewal-manager | monthly | Ivan HIGH (churn) |
| 3.7 Proposal Writer | sales.json:proposals | aiw-proposal-drafter-on-demand | on-demand | Ivan HIGH |
| 3.8 Marketing Manager | sales.json:marketing | aiw-hera-marketing-lead | Mon/Wed/Fri | Ivan HIGH |
| 3.9 Content Marketing | sales.json:content | aiw-calliope-content-producer | 3x/week | Hera MEDIUM |
| 4.1 CTO | engineering.json | aiw-engineering-roster-biwk | biweekly Tue/Fri | Kiki CRITICAL |
| 4.7 DevOps | org-state.json | aiw-devops-monitor-30min | every 30m | Kiki HIGH |
| 4.8 QA | eval-per-agent.json | aiw-qa-automation-on-pr | on-PR | Kiki HIGH |
| 4.9 Security | org-state.json:security | aiw-security-watchdog-30min | every 30m | Kiki CRITICAL |
| 4.18 DBA | ai-ops daily | aiw-ai-ops-coordinator-daily | daily | Kiki MEDIUM |
| 4.24 AI Safety | eval-per-agent.json | aiw-ai-safety-engineer-30min | every 30m | Kiki HIGH |
| 5.1 Research Lead | research.json | aiw-research-tracker-weekly | weekly Sun | Ivan HIGH |
| 5.5 Citation Specialist | research.json:citation_audit | aiw-citation-checker-on-demand | daily 11:00 | Ivan CRITICAL |
| 5.6 Course Designer | research.json:course_pipeline | aiw-course-producer | weekly | Ivan HIGH |
| 5.7 Course Producer | research.json:course_pipeline | aiw-multimedia-producer | weekly | Ivan HIGH |
| 6.1 Head of People | people.json | aiw-people-hr-weekly | weekly Mon | Ivan HIGH |
| 6.4 Performance Coach | kiki.json | aiw-kiki-coach-weekly | weekly Fri | Ivan MEDIUM |
| 7.1 AI Ops Lead | eval-per-agent.json | aiw-ai-ops-coordinator-daily + aiw-eval-gate-runner | daily + hourly | Kiki HIGH |
| 8.1 Compliance Officer | trademark-scan-cron.json | aiw-compliance-monitor-weekly + aiw-trademark-scan-cron | weekly + 30m | Ivan CRITICAL |

---

# APPENDIX C — Today's Org (who's doing what)

This is the ground-truth staffing map right now (2026-08-31):

| Function | Person wearing hat | Agent(s) assisting |
|---|---|---|
| CEO / Strategy / Vision | Ivan | `business-analyst` (daily brief) |
| CTO / Eng / Tech lead | Kiki | `engineering-roster`, `ai-safety-engineer`, `devops-monitor` |
| Sales / Revenue | Ivan | Apollo (sales-pipeline) |
| Marketing | Ivan | Hera + Calliope + Iris |
| Product Discovery | Ivan | Athena + Clio |
| Operations | Ivan | Kronos (proposed) / Coordina + ai-ops-coordinator |
| Finance | Ivan | finance-controller + business-analyst + accounting-automation |
| Legal | Ivan (external lawyer) | compliance-monitor |
| People (head) | Ivan + Kiki | people-hr + kiki-coach |
| Coaching (Ivan's growth) | Kiki (coach) + coach-ivan | kiki-coach + coach-ivan |
| Research | Ivan | research-tracker + Thoth + thesis-tracker |
| AI Safety | Kiki | ai-safety-engineer + eval-gate-runner |
| Compliance | Ivan | compliance-monitor + trademark-scan |

---

*Generated 2026-08-31 by Erebus. Supersedes any prior org listing.*
*Companion docs:*
- `[DEPT-AGENTS-ROLES-COMPLETE.md](DEPT-AGENTS-ROLES-COMPLETE.md) (sibling catalog)` — flat catalog
- `[ORG-AGENTS.md](../ORG-AGENTS.md) (handoff matrix)` — handoff matrix (47 agents, 9 schemas)
- `[ROLES-INVENTORY.md](https://github.com/Ai-Whisperers/growth-coaching/blob/master/ROLES-INVENTORY.md) (in growth-coaching repo)` — role definitions source