# Department of Finance & Legal — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Ivan | **Lead agent**: `finance-controller` | **Atomic agents**: `demeter-finance-controller`, `hermes-finance-lead`, `business-analyst`
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 8 areas documented. Cadence tiers: 🔴 HOT (2), 🟡 WARM (4), 🔵 COOL (2).

---

## Reading guide

Finance & Legal research is the most **regulated** of all departments — every area touches either compliance, taxes, contracts, or cash. The 8 areas here prioritize **what's actionable in the next 90 days** over what's academically interesting.

Areas are grouped by the 4 universal themes (internal / market / literature / actionable).

---

# Finance & Legal Research Areas



## 🔴 HOT areas

### 1. Margin reality check — 5 projects × real cost × real price 🔴

| | |
|---|---|
| **Question** | What was the actual margin (revenue minus all costs) on the last 5 client projects we delivered? |
| **Why** | The theoretical pricing in `marketing-strategy/02-PRICING.md` assumes standard margins. Real data may show: (a) some projects are unprofitable, (b) we underprice certain verticals, (c) infra costs eat margin unexpectedly. Without this data, pricing decisions are guesses. |
| **Method** | (1) For each of the last 5 client projects: extract hours (git activity, session DB, calendar entries). (2) Extract tools used (per-project subscription log). (3) Extract infra cost share (cloud bill proportion). (4) Compute total cost. (5) Compare to billed amount. (6) Margin %. (7) Lessons learned. |
| **Output** | `finance/margin-analysis-2026.md` (table per project: cost / price / margin% / lessons) |
| **Owner** | finance-controller + business-analyst + Ivan |
| **Cadence** | Once after 5+ projects, then refresh quarterly |
| **Cross-references** | `state/cost-tracker.json`, `research/30-research-areas.md` #3, `marketing-strategy/02-PRICING.md` |

### 2. EU AI Act compliance read for AI coaching products 🔴

| | |
|---|---|
| **Question** | Which EU AI Act articles apply to our coaching products, and what changes do we need to make to be EU-AI-Act-compliant by August 2026? |
| **Why** | EU AI Act + GDPR Article 9 compliance is a **strategic moat** (per `research/30-coaching-research-areas.md` #2). US competitors won't bother. But this is also a hard regulatory requirement if we ever sell to EU clients. |
| **Method** | (1) Read the AI Act text (artificialintelligenceact.eu), specifically Articles 5, 6, 50, Annex III (high-risk categories). (2) Map each article to our coaching features. (3) Identify which apply (probably: Article 50 for transparency obligations on AI systems, Annex III #4 for biometric/affect-recognition if we ever do that). (4) Build compliance checklist. (5) Estimate implementation cost. |
| **Output** | `finance/eu-ai-act-coaching-compliance.md` (table mapping articles → coaching features → compliance checklist + cost estimate) |
| **Owner** | compliance-monitor agent + Ivan + external legal counsel (1-time review) |
| **Cadence** | Once + quarterly review of AI Act amendments |
| **Cross-references** | `research/30-coaching-research-areas.md` #2, `docs/THREAT-MODEL.md`, `constitution/ORG-AGENTS.md` |

---

## 🟡 WARM areas

### 3. Funding landscape refresh — Q4 2026 🟡

| | |
|---|---|
| **Question** | What new funding opportunities (FADA, NL accelerators, EU grants) appeared since the 2026-Q3 landscape analysis, and which existing leads are still warm? |
| **Why** | The Q3 landscape analysis (`research/funding-landscape-2026-Q3.md`) found 5 active funding leads. 3 months later, those leads may have aged, closed, or evolved. Refresh needed before next funding round decision. |
| **Method** | (1) Read `research/funding-landscape-2026-Q3.md` (the 5 leads). (2) For each: check application status (open? closed? interview stage?). (3) Search for new FADA calls + NL accelerators + EU SME grants. (4) Update the leads table. (5) Recommend: re-apply, abandon, or upgrade tier. |
| **Output** | `research/funding-landscape-2026-Q4.md` (refreshed table) |
| **Owner** | funding-coordinator + Ivan |
| **Cadence** | Quarterly |
| **Cross-references** | `research/funding-landscape-2026-Q3.md`, `state/funding.json`, `02-finance-legal/funding-coordinator/PROMPT.md` |

### 4. Pricing benchmark refresh — LATAM AI agencies 🟡

| | |
|---|---|
| **Question** | What are 10 LATAM AI agencies actually charging for services comparable to ours, by vertical? |
| **Why** | Current pricing is theoretical. Real LATAM AI-agency rates may be 30-50% lower than US rates. If we price at US rates for LATAM clients, we lose deals. |
| **Method** | (1) Identify 10 LATAM AI agencies (public pricing pages + RFP responses + case studies). (2) For each: tier, price per project/month, what they include. (3) Categorize by vertical (legal, healthcare, dental, retail, SaaS). (4) Compute per-vertical rate card. (5) Compare to our current pricing. (6) Recommend price adjustments. |
| **Output** | `finance/latam-ai-pricing-benchmarks.md` (table per competitor + per-vertical rate card) |
| **Owner** | finance-controller + sales-pipeline + Ivan |
| **Cadence** | Annually + on competitor price change |
| **Cross-references** | `research/30-coaching-research-areas.md` #4, `marketing-strategy/02-PRICING.md`, `research/STRATEGY.md` Part 3 |

### 5. LGPD / GDPR / EU AI Act / Trademark — multi-jurisdiction compliance matrix 🟡

| | |
|---|---|
| **Question** | What compliance obligations apply to AI Whisperers in each of: Paraguay (LGPD), Netherlands (GDPR + EU AI Act), US (trademark), and what's our compliance status in each? |
| **Why** | Trademark incident (Hostinger 2026-08-13) showed that compliance is **reactive**, not proactive. We need a clear matrix per jurisdiction. |
| **Method** | (1) Read LGPD text (similar to GDPR, but Paraguayan variant). (2) Read GDPR Articles 5, 6, 9, 22, 32, 33. (3) Read EU AI Act Articles 5, 6, 50. (4) Read the 4 trademark classes we use. (5) For each, list: what triggers compliance, what we have to do, what we're missing. (6) Build a matrix. |
| **Output** | `finance/compliance-jurisdiction-matrix.md` (4-jurisdiction compliance matrix with status) |
| **Owner** | compliance-monitor + Ivan |
| **Cadence** | Annually + on regulation change |
| **Cross-references** | `docs/THREAT-MODEL.md`, `~/skills/trademark-compliance-scrub/`, `constitution/DEFERRED-ROLES.md` |

### 6. Cashflow projection models — runway scenarios 🟡

| | |
|---|---|
| **Question** | What are our runway scenarios under: (a) no new revenue, (b) 1 new client/quarter, (c) 1 new client/month, (d) FADA grant approval? |
| **Why** | Ivan makes capital decisions based on imprecise intuition. A simple model shows the trade-offs explicitly. |
| **Method** | (1) Get current cash + burn rate (from `state/finance.json`). (2) Get current MRR + run-rate projections (from sales-pipeline + business-analyst). (3) Build 4 scenarios in a spreadsheet. (4) Compute months-of-runway for each. (5) Identify trigger thresholds (when to top up LiteLLM, when to defer salaries, when to take FADA). |
| **Output** | `finance/runway-scenarios-2026.md` (4 scenarios + recommended actions) |
| **Owner** | finance-controller + business-analyst + Ivan |
| **Cadence** | Quarterly + on any major revenue/cost change |
| **Cross-references** | `state/finance.json`, `state/coord.json:decisions_for_ivan`, `research/alternative-income-2026-Q3.md` |

---

## 🔵 COOL areas

### 7. Tax optimization across 3 jurisdictions (PY / NL / EU) 🔵

| | |
|---|---|
| **Question** | What's the tax-optimal entity structure for an AI Whisperers operation that has revenue in PY + NL + future EU clients? |
| **Why** | Setting up wrong entity structure = 5-10 years of unnecessary tax. Setting up right = significant savings + clean exit path. |
| **Method** | (1) Read current entity setup (Paraguayan EAS). (2) Compare 3 options: (a) keep PY only + invoice from NL via personal, (b) Dutch BV (besloten vennootschap) + branch in PY, (c) Estonian e-Residency + invoicing platform. (3) For each: tax rate, compliance burden, cost, growth ceiling. (4) Recommend with rationale. |
| **Output** | `finance/tax-structure-comparison.md` (3-option comparison + recommendation) |
| **Owner** | Ivan + external accountant + tax advisor (1-time engagement) |
| **Cadence** | Once + on entity change |
| **Cross-references** | `research/netherlands-2026` repo, `research/STRATEGY.md` Part 5 |

### 8. Spending trends + vendor optimization 🔵

| | |
|---|---|
| **Question** | What did we spend on each vendor in the last 12 months, and which 3 vendors could we eliminate or replace? |
| **Why** | Vendor sprawl is real. The L1 audit found cost is $9.79/day ($293/mo) for 49 agents — that's high for the scale. Periodic vendor review saves money. |
| **Method** | (1) List every active vendor subscription. (2) For each: last 30 days usage, monthly cost, alternative cost. (3) Flag anything: (a) unused, (b) overpriced vs market, (c) duplicate functionality, (d) could be self-hosted. (4) Top 3 savings opportunities. (5) Recommend: cancel, replace, or keep. |
| **Output** | `finance/vendor-spend-review-2026.md` (per-vendor table + top 3 savings) |
| **Owner** | finance-controller + procurement-tracker |
| **Cadence** | Annually + on vendor event (price hike, outage) |
| **Cross-references** | `state/cost-tracker.json`, `01-operations/procurement-tracker/PROMPT.md`, `research/30-research-areas.md` #4 |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **Funding landscape** (most complete existing file): `research/funding-landscape-2026-Q3.md`
- **Alternative income**: `research/alternative-income-2026-Q3.md`
- **Org-wide 30-research**: `research/30-research-areas.md` (Areas 3, 9, 10 owner: finance)
- **Cost tracker**: `state/cost-tracker.json` (live data)
- **Threat model**: `docs/THREAT-MODEL.md`
- **Trademark compliance**: `~/skills/trademark-compliance-scrub/`
- **Sibling dept catalogs**: `research/dept-research/{01,03..06,board}-*-research-areas.md`

---

**Total finance research areas**: 8
**Cadence breakdown**: 🔴 HOT 2, 🟡 WARM 4, 🔵 COOL 2
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

