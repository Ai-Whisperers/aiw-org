# Complete Department & Role History — All Three Catalog Generations

> Answer to Ivan's question: "**how many departments had demiurge**? wasn't there a more complete list?"
>
> YES — there have been **three different inventory generations**. DEMIURGE is the most recent (24 agents) but the catalog spans 30 functional areas + 135 roles. Here's the unredacted history.

---

## TL;DR

| Generation | Date | What | Total | DEMIURGE? |
|------------|------|------|-------|-----------|
| **0 — Conversation original** | 2026-07 (pre-repo) | Hand-drawn long-list | **20 departments** | No |
| **1 — Long-list after conversation** | 2026-08-14 | Built from session transcription | **16 departments, 51 agents** | No |
| **2 — Expanded catalog (current)** | 2026-08-31 | Adds Tier 2/3/4 + 135 roles | **6 Tier-1 + 30 functional areas** | Partial (only DEMIURGE bracketed names) |
| **3 — DEMIURGE canonical** | 2026-08-31 | Greek-mythology naming for atomic agents | **24 DEMIURGE + 23 heritage + 7 dept-leads** | YES — this is "DEMIURGE" |

So the answer to **"how many departments had DEMIURGE?"**:

- **6 Tier-1 dept dirs** structurally (the ones you see today: 01-operations through 06-people-culture + board-of-directors)
- All 6 dept-leads get **composition fields** in their frontmatter (per Layer 2.5/2.6 work) — that's how DEMIURGE extends **across** all depts
- **24 DEMIURGE atomic agents** are arranged under functional areas (sections 8.1–8.10 of `DEPT-AGENTS-ROLES-COMPLETE.md`), including 2 reserved for the **now-retired "long list"** depts (Security, Product, Course/Education, etc.)

The catalog you saw in my previous answer was the **summary view** — it had 6 Tier-1 dept dir counts (43 / 5 / 9 / 14 / 4 / 1) but didn't include the **30 functional-area / 135-role section**. That's the more complete view.

---

## The Three Generations

### Generation 0 — Original 20-Department long list

From `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md` (reconstructed from the conversation where it was condensed):

| # | Department | Maps to (Final Agent) |
|---|------------|-----------------------|
| 1 | **Finance** | finance-controller |
| 2 | **Human Resources** | people-hr |
| 3 | **Legal** | compliance-monitor |
| 4 | **Development** | engineering-roster, devops-monitor |
| 5 | **QA** | qa-automation-runner, eval-gate-runner |
| 6 | **Operations** | ai-ops-coordinator |
| 7 | **Research** | research-tracker, citation-checker |
| 8 | **Marketing** | marketing-content-producer |
| 9 | **Multimedia** | multimedia-producer |
| 10 | **Sales** | sales-pipeline, lead-enrichment |
| 11 | **Procurement** | procurement-tracker |
| 12 | **Content Management** | (folded into Marketing) |
| 13 | **Board of Directors** | board-of-directors |
| 14 | **Cross-Cutting** | (multiple: ai-safety, security) |
| 15 | **Customer Success** | coach-renewal-manager |
| 16 | **Data & Analytics** | bizops-tracker (partial) |
| 17 | **Security** | security-watchdog |
| 18 | **Compliance** | (folded into Legal) |
| 19 | **Product** | (covered by management-coordinator) |
| 20 | **Course / Education** | coach-practitioner (the coaching product) |

This is the **pre-constitution drawing-board list**, before any code or agents were built.

---

### Generation 1 — 16 Departments × 51 Agents

After removing duplicates and folding sub-concerns (per `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md`):

| # | Department | Final Count |
|---|------------|-------------|
| 1 | Finance | 3 agents |
| 2 | HR | 2 agents |
| 3 | Legal | 1 agent |
| 4 | Development | 5 agents |
| 5 | QA | 3 agents |
| 6 | Operations | 2 agents |
| 7 | Research | 4 agents |
| 8 | Marketing | 2 agents |
| 9 | Multimedia | 1 agent |
| 10 | Sales | 6 agents |
| 11 | Procurement | 1 agent |
| 12 | Accounting | 1 agent |
| 13 | Management | 6 agents |
| 14 | Board | 1 agent |
| 15 | Coaching (the product) | 8 agents |
| 16 | Cross-Cutting | 4 agents |

This was the **first "real" catalog** in 2026-08-14 (`constitution/ORG-AGENTS.md` v0.2.0). It also introduced the **6 Tier-1 + Tier-2 cross-cutting** structure we use today.

---

### Generation 2 — Expanded Catalog (current, before DEMIURGE rebrand)

From `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` Section 7 (49 agents, current as of 2026-08-31 13:00):

```
Tier 1 — Lead Agents (7)
  operations, finance-legal, sales-growth, engineering-delivery,
  research-education, people-culture, board-of-directors

Tier 2 — Sub-agents (14)
  bizops-tracker, business-analyst, ai-ops-coordinator, devops-monitor,
  qa-automation-runner, security-watchdog, ai-safety-engineer,
  marketing-content-producer, proposal-drafter, lead-enrichment,
  thesis-tracker, citation-checker, course-producer, founder-bandwidth-watchdog

Tier 3 — Cross-cutting (8)
  ai-ops-coordinator (lead+coord), bizops-tracker, accounting-automation,
  procurement-tracker, source-curator, okr-tracker, compliance-monitor,
  revops-pipeline-analyzer, tax-receipt-tracker (some overlap)

Tier 4 — Monitoring (4 always-on)
  chaos-test-runner, drift-detector, eval-gate-runner, security-auditor
  (+ ai-safety-engineer-30min, devops-monitor-30min, security-watchdog-30min
   as 30-min variants)

Tier 5 — Coaching (14 — in sister repo coach-agents)
  coach-ivan, coach-kiki, coach-org, coach-lead-agents, coach-lead-finder,
  coach-onboarding-poller, coach-renewal-manager, coach-roi-tracker,
  coach-practitioner, coach-cohort-facilitator, coach-conversion-agent,
  coaching-content-curator, coaching-quality-reviewer, coaching-research-intelligence
```

---

### Generation 3 — DEMIURGE canonical (current, post-2026-08-31)

The **DEMIURGE promotion** (`afb7abd`, 2026-08-31 14:07) reorganized the **atomic-agent layer** under Greek-mythology names. This doesn't change the count, but it's how the catalog is now structured:

```
DEMIURGE Atomic Layer (24 agents) - mythology names
├── 8.1 Marketing (3):       calliope-content-producer, hera-marketing-lead, iris-community-monitor
├── 8.2 Sales (3):           apollo-sales-lead, cadmus-lead-enrichment, metis-proposal-drafter
├── 8.3 Product Discovery (2): athena-product-discovery-lead, clio-customer-signal-collector
├── 8.4 Operations (4):      kronos-operations-lead, bizops-tracker, business-analyst, management-coordinator
├── 8.5 AI Ops (1):          ai-ops-coordinator
├── 8.6 Compliance (1):      compliance-monitor
├── 8.7 Router (1):          hermes-router-revenue
├── 8.8 Health Monitor (1):  argus-health-monitor
├── 8.9 Knowledge Mgmt (6):  hephaestus-document-miner, mnemosyne-document-archivist,
│                            orpheus-recordings-agent, peitho-language-quality,
│                            pheme-document-router, themis-document-classifier
└── 8.10 Cross-cut Knowledge (2): echo-community-scanner, thoth-literature-scanner

Total: 24 DEMIURGE agents
```

So when the catalog says **"DEMIURGE touches all 6 Tier-1 depts"**, it means:
- **Operations** uses kronos-operations-lead, bizops-tracker, business-analyst, management-coordinator (4)
- **Finance** uses hermes-router-revenue, business-analyst (2)
- **Sales** uses apollo-sales-lead, cadmus-lead-enrichment, hermes-router-revenue (3)
- **Research** uses thoth-literature-scanner, hephaestus-document-miner (2)
- **People** uses echo-community-scanner, iris-community-monitor (2)
- **Engineering** uses thoth-literature-scanner, echo-community-scanner, themis-document-classifier (cross-cutting via transfer_targets)
- **Board** uses ai-ops-coordinator, apollo-sales-lead (2)

**12 of 24 DEMIURGE agents are in dept `composition:[]` graphs**. The other 12 are connected via `transfer_targets` (cross-cut injection).

---

## The "More Complete List" — 135 Roles × 30 Functional Areas

From `docs/ROLES-INVENTORY.md` (written 2026-08-14, 292 lines):

| Functional Area | Roles | Tier 1 | Tier 2 | Tier 3+ |
|-----------------|-------|--------|--------|---------|
| Operations / Management | 8 | 6 | 1 | 1 |
| Finance & Legal | 14 | 6 | 4 | 4 |
| Sales & Growth | 18 | 5 | 6 | 7 |
| Engineering & Delivery | 24 | 7 | 2 | 15 |
| Research & Education | 12 | 5 | 4 | 3 |
| People & Culture | 8 | 3 | 0 | 5 |
| AI Ops (cross-cutting) | 6 | 1 | 3 | 2 |
| Compliance (named role) | 4 | 1 | 1 | 2 |
| Knowledge Management | 4 | 1 | 2 | 1 |
| RevOps | 5 | 0 | 3 | 2 |
| BizOps | 3 | 0 | 2 | 1 |
| Customer Success | 6 | 0 | 0 | 6 |
| AI Safety | 4 | 1 | 1 | 2 |
| Procurement | 4 | 0 | 4 | 0 |
| Tier-3 deferred departments | 12 | 0 | 0 | 12 |
| Tier-4 enterprise | 5 | 0 | 0 | 5 |
| **TOTAL** | **~135** | **~36** | **~31** | **~68** |

### Functional areas covered (full list, 30 total = 16 Tier-1+2 + 12 Tier-3 + 4 Tier-4)

```
TIER-1 (active, 6):
  Operations / Management
  Finance & Legal
  Sales & Growth
  Engineering & Delivery
  Research & Education
  People & Culture

TIER-2 (cross-cutting, 8):
  AI Ops
  Compliance
  Knowledge Management
  RevOps
  BizOps
  Customer Success       ← deferred dept
  AI Safety
  Procurement

TIER-3 (12 deferred):
  Chief of Staff
  Trust & Safety
  DevRel
  Investor Relations
  Workplace Manager
  Fraud / Risk Analyst
  Treasury Manager
  Internal Audit
  Workplace Operations
  DEI Specialist
  Public Relations
  Government Relations

TIER-4 (5 enterprise):
  Internal Communications Manager
  M&A / Corp Dev
  Chief Data Officer (CDO)
  Chief AI Officer (CAIO)
  Diversity & Inclusion Lead
```

---

## What's DEMIURGE vs what's not (today's reality)

| Layer | Naming | Count | Purpose |
|-------|--------|-------|---------|
| **Tier-1 dept dirs** (6 + 1 governance) | Role-names (e.g., `management-coordinator`) | 7 lead agents, 28 specialists = **35 dept agents** | Day-to-day production work |
| **DEMIURGE atomic** | Greek-mythology | **24** | Reusable solver + router sub-agents |
| **Heritage portmanteau** | Original portmanteau (e.g., `ai-ops-coordinator`) | **23** | Older agents, intentionally not renamed (catalog §9) |
| **Cross-cuts (Tier 2)** | Mix of DEMIURGE + heritage | 8 functional areas, ~12 agents | AI Ops, Compliance, AI Safety, Procurement |
| **Monitors (Tier 4)** | Descriptive + `-30min` suffixes | 16 dept-monitors + variations | Watchdog layer |
| **Coaches (sister repo)** | `coach-*` naming | 14 coach agents | Lives in `coach-agents` repo |
| **Tier-3 + Tier-4 depts** | (varied) | 17 dept placeholders | Triggered by scale milestones |

---

## Should we / could we build out the full 135-role list?

| Question | Answer |
|----------|--------|
| Is 135 roles needed today? | **No**. Org is 1 person (Ivan) + Kiki coaching. Real hiring FTE pipeline is years away. |
| Is the catalog useful for planning? | **YES**. Triggers in `DEFERRED-ROLES.md` tell us when to activate each. |
| Could we use DEMIURGE for all 24 to map to roles? | **YES** — `hera-marketing-lead` already covers Marketing Manager role. The DEMIURGE Prometheus pattern is reusable for unbuilt roles. |
| Will we run out of DEMIURGE names? | **No** — dozens of unused mythology characters (Ares, Artemis, Demeter, Dionysus, Nemesis, Pan, Persephone, Prometheus, Selene, Triton, Tyche...) |
| What's the recommended next build? | The 4 unbuilt dept-agents in `04-engineering/` (drift-detector, security-auditor, delivery-tracker, qa-automation-on-pr). THEN once those exist, plan Tier-3 promotions (Customer Success at first, per catalog trigger). |

---

## Bottom line

**Answer to "how many departments had DEMIURGE?"**:
- **6 Tier-1 dept dirs** are where DEMIURGE is structurally connected today
- **30 functional areas** (6 + 8 + 12 + 4) exist in the full role catalog — of those, DEMIURGE atomic agents cover maybe 10–12 today
- **Tier-3 departments (12)** like Customer Success, Trust & Safety, IR, Chief of Staff — none have DEMIURGE agents yet (correctly deferred)
- **Tier-4 departments (5)** like CDO, CAIO, M&A — even more deferred

**Answer to "more complete list?"**:
YES. Here's what's available:
1. `docs/ROLES-INVENTORY.md` — 135 roles, 30 functional areas, 292 lines, **the most complete**
2. `analysis/DEPT-AGENTS-ROLES-COMPLETE.md` — 49 agents + DEMIURGE section, 1,038 lines, **the current catalog**
3. `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md` — original 20-dept + 16-dept generations, 212 lines
4. `analysis/ORGANIGRAM.md` — 75KB tree, **the visual org chart**
5. `analysis/NAMING-CONVENTION-ANALYSIS.md` — naming layer history
6. `DEFERRED-ROLES.md` + `constitution/DEFERRED-ROLES.md` — what to build when

The "summary" I gave in the previous answer only touched **Section 7** (49 agents) — but the **Section 12 (135 roles × 30 areas)** is the more complete inventory you asked about.

---

**Working tree**: clean
**This audit committed**: (about to)