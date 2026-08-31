# Department of Sales & Growth — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Ivan | **Lead agent**: `sales-pipeline` | **Atomic agents**: `apollo-sales-lead`, `cadmus-lead-enrichment`, `metis-proposal-drafter`, `hermes-router-revenue`
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 10 areas documented. Cadence tiers: 🔴 HOT (4), 🟡 WARM (4), 🔵 COOL (2).
>
> **Critical context**: As of 2026-08-31, sales pipeline is **DEAD** (1 client, $240 MRR, 0 open deals). Phase 1 L1 audit finding. The 10 areas here prioritize **revival** over expansion.

---

## Reading guide

Sales & Growth research is the most **time-sensitive** of all departments — every research area ties to revenue in the next 90 days. Unlike Operations (observability) or Finance (compliance), Sales research exists to **find and close deals**.

Areas are grouped by the 4 universal themes (internal / market / literature / actionable).

---

# Sales & Growth Research Areas



## 🔴 HOT areas

### 1. Sales funnel revival — the dead pipeline 🔴

| | |
|---|---|
| **Question** | Why did our lead-generation pipeline go to 0 leads and how do we revive it within 30 days? |
| **Why** | As of 2026-08-31, `state/sales.json` shows `leads_in_flight: []`, `open_deals: 0`, mrr=$240 from 1 client. The Cloudflare Worker (`rubicon-eas-lead`) returns 404. Without pipeline revival, no other sales research matters. |
| **Method** | (1) Diagnose why Worker returns 404 (per Phase 1 L1 audit). (2) Decide: revive webhook OR replace with new form backend. (3) For revival: fix + test webhook. (4) For replacement: pick Formspree / Typeform / custom. (5) Migrate any captured leads. (6) Verify end-to-end flow. (7) Document the playbook. |
| **Output** | `sales/funnel-revival-2026.md` (diagnosis + decision + revival steps + verification) |
| **Owner** | sales-pipeline + engineering-roster + Ivan |
| **Cadence** | Once urgently + on pipeline-health monthly |
| **Cross-references** | `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` surprise #6, `state/sales.json`, `03-sales-growth/sales-pipeline/PROMPT-monitor.md` |

### 2. Customer archaeology — who actually bought vs ghosted 🔴

| | |
|---|---|
| **Question** | Of our 17+ deployed client sites + dozens of prospects, who actually converted, and what was the pattern? |
| **Why** | We have real conversion data hiding in: signed contracts, outreach logs (`marketing-strategy/agent-tasks/`), CF Worker submissions, GitHub commits. Mining this data reveals the **actual ICP** (not the theoretical one). |
| **Method** | (1) Mine signed contracts (if any). (2) Mine `marketing-strategy/agent-tasks/` outreach logs. (3) Mine CF Worker `rubicon-eas-lead` form submissions (if recoverable). (4) Mine GitHub commits by client. (5) Cross-reference with `customers.json` in state dir. (6) Build actual ICP from real conversions vs theoretical. |
| **Output** | `sales/customer-archaeology-2026.md` (real ICP table + segment analysis + lessons) |
| **Owner** | sales-pipeline + Ivan |
| **Cadence** | Every 6 months |
| **Cross-references** | `research/30-research-areas.md` #2, `research/30-coaching-research-areas.md` #8, `state/customers.json` |

### 3. LATAM AI market sizing — Paraguay-specific 🔴

| | |
|---|---|
| **Question** | What is the addressable market size for AI services in Paraguay specifically (not LATAM aggregate)? |
| **Why** | Current data is US/EU-centric ($5.48B AI career coach 2025 globally). For Rubicón EAS pitches + funding applications, we need Paraguay-specific numbers. |
| **Method** | (1) Read `research/STRATEGY.md` Part 3 (LATAM market reality). (2) Sources: Statista LATAM reports, IDB (Inter-American Development Bank) reports, CBP (Centro de Estudios para el Desarrollo) PY, MIC (Ministerio de Industria y Comercio) PY. (3) Compute: total AI services market in PY, growth rate, number of addressable companies, average contract size. (4) Cross-check with at least 3 sources. |
| **Output** | `sales/latam-py-market-sizing.md` (1 page, table with PY figures + CAGR + 5-year forecast) |
| **Owner** | sales-pipeline + Ivan + Erebus (research) |
| **Cadence** | Once, refresh annually |
| **Cross-references** | `research/STRATEGY.md` Part 3, `research/30-coaching-research-areas.md` #1, `marketing-strategy/` |

### 4. WhatsApp outreach at scale — the actual playbook 🔴

| | |
|---|---|
| **Question** | How do we send 100+ personalized WhatsApp outreach messages per week without getting banned, given Paraguay's WhatsApp-heavy culture? |
| **Why** | Paraguay is WhatsApp-first. The `coach-lead-finder` agent + `coach-onboarding-poller` use WhatsApp heavily. But WhatsApp has rate limits + spam detection. Need a documented playbook. |
| **Method** | (1) Read Evolution API docs (rate limits, best practices). (2) Survey 5 LATAM AI agencies' WhatsApp outreach playbooks. (3) Test small (10 messages/day) and ramp up. (4) Track: delivery rate, response rate, ban incidents. (5) Document the playbook. |
| **Output** | `sales/whatsapp-outreach-playbook.md` (rate limits + best practices + banned-incident response) |
| **Owner** | sales-pipeline + coach-lead-finder |
| **Cadence** | Once + quarterly tune |
| **Cross-references** | `coach-agents/coach-lead-finder/`, `research/30-research-areas.md` #12 |

---

## 🟡 WARM areas

### 5. Discovery methodology — SPIN/MED vs BANT vs GPCTBA vs Gap Selling 🟡

| | |
|---|---|
| **Question** | Which sales discovery methodology fits our AI-services offering: SPIN/MED, BANT, GPCTBA, or Gap Selling? |
| **Why** | Our discovery calls use SPIN/MED per `coaching-funnel-playbook.md`. But that's coaching-specific. For Rubicón EAS (AI services), the right methodology may differ. |
| **Method** | (1) Read each methodology (SPIN/MED, BANT, GPCTBA, Gap Selling, MEDDIC). (2) Compare on 5 dimensions: discovery depth, qualification speed, deal closure rate, fit with technical sales, fit with founder-led sales. (3) Pick 1-2 for Rubicón EAS context. (4) Document scripts/templates. |
| **Output** | `sales/discovery-methodology-decision.md` (comparison table + recommendation + scripts) |
| **Owner** | sales-pipeline + Ivan |
| **Cadence** | Once + on methodology question |
| **Cross-references** | `research/coaching-funnel-playbook.md`, `research/1000-company-questions.md` Category 8 |

### 6. Proposal templates — per vertical 🟡

| | |
|---|---|
| **Question** | What are the 5 most common proposal templates we should have ready, by client vertical? |
| **Why** | Speed of proposal-to-send matters. Pre-built templates for the top 5 verticals cut proposal time from 4 hours to 30 minutes. |
| **Method** | (1) Identify top 5 verticals (legal, healthcare, dental, retail, SaaS — based on past outreach). (2) For each: build a proposal template (problem, solution, scope, timeline, pricing). (3) Include case study placeholder. (4) Test with 1 prospect per vertical. (5) Refine. |
| **Output** | `sales/proposal-templates/{vertical}.md` × 5 |
| **Owner** | metis-proposal-drafter agent + sales-pipeline |
| **Cadence** | Once + quarterly review |
| **Cross-references** | `03-sales-growth/proposal-drafter/PROMPT.md`, `research/coaching-funnel-playbook.md` |

### 7. Competitive positioning — per ICP 🟡

| | |
|---|---|
| **Question** | For each of our top 3 ICPs, who are the 5 direct competitors and what's our counter-positioning for each? |
| **Why** | Without per-ICP competitive positioning, our pitch is generic. BetterUp/CoachHub/Valence dominate the US market; we win by addressing their gaps. |
| **Method** | (1) Identify top 3 ICPs (from customer-archaeology #2). (2) For each: list 5 competitors (use `research/200-ai-companies.md` + `research/200-ai-coaching-companies.md`). (3) For each competitor: common complaint pattern (Glassdoor + G2 + Reddit + customer churn signals). (4) Our counter-positioning for each (1 sentence). (5) Compile into competitive matrix. |
| **Output** | `sales/competitive-positioning-matrix.md` (3 ICPs × 5 competitors + counter-positioning) |
| **Owner** | sales-pipeline + Erebus (research) |
| **Cadence** | Once + on competitor product update |
| **Cross-references** | `research/200-ai-coaching-companies.md`, `research/30-coaching-research-areas.md` #3 |

### 8. Lead enrichment patterns — atomic agents + CRM integration 🟡

| | |
|---|---|
| **Question** | How do `cadmus-lead-enrichment` + `clio-customer-signal-collector` atomic agents integrate with our CRM (or do we need one)? |
| **Why** | Lead enrichment is in the atomic layer but no CRM exists yet. We need to know: do we self-host the enrichment logic, use HubSpot free, or build a simple Airtable? |
| **Method** | (1) Read cadmus + clio PROMPT.md specs. (2) Survey free CRM options for <100 leads (HubSpot free, Airtable free, Notion tables). (3) Test 1 prospect end-to-end through enrichment → CRM → outreach. (4) Document the pipeline. |
| **Output** | `sales/lead-enrichment-pipeline.md` (CRM choice + integration pattern + first-end-to-end-test) |
| **Owner** | cadmus-lead-enrichment agent + sales-pipeline |
| **Cadence** | Once + on scale-up |
| **Cross-references** | `demiurge/agents/cadmus-lead-enrichment/PROMPT.md`, `demiurge/agents/clio-customer-signal-collector/PROMPT.md` |

---

## 🔵 COOL areas

### 9. Customer Success playbooks (Tier-3 deferred — research now, build later) 🔵

| | |
|---|---|
| **Question** | What CS playbook patterns from BetterUp/CoachHub should we pre-build now, before activating the Customer Success Tier-3 dept? |
| **Why** | Customer Success is correctly deferred (trigger: 5+ clients). But research now = less scramble later. |
| **Method** | (1) Read `research/30-coaching-research-areas.md` customer-success-related. (2) Survey BetterUp/CoachHub CS playbooks (public + Glassdoor employee reviews). (3) Draft 4 playbooks: onboarding, retention, expansion, renewal. (4) Park in `sales/customer-success-playbooks/`. |
| **Output** | `sales/customer-success-playbooks/{onboarding,retention,expansion,renewal}.md` |
| **Owner** | TIER-3-DEFERRED (no agent yet) — sales-pipeline pre-builds |
| **Cadence** | Once + activate when 5+ clients |
| **Cross-references** | `DEFERRED-ROLES.md` Customer Success, `constitution/DEFERRED-ROLES.md` |

### 10. Brand positioning — ParaguAI as a flagship brand 🔵

| | |
|---|---|
| **Question** | When we launch ParaguAI publicly (per DEFERRED-ROLES.md Public Relations trigger), what should the brand positioning look like? |
| **Why** | The ParaguAI Builder product is the flagship. Public launch is Tier-3 deferred but brand research now saves scramble later. |
| **Method** | (1) Read `marketing-strategy/` repo. (2) Look at 3 adjacent Paraguayan tech brands for cultural reference. (3) Draft 3 positioning statements (each in 1 sentence). (4) Test with 5 LATAM AI practitioners. (5) Recommend. |
| **Output** | `sales/paraguai-positioning-statements.md` (3 candidates + recommendation) |
| **Owner** | hera-marketing-lead agent + Ivan |
| **Cadence** | Once + on flagship launch |
| **Cross-references** | `marketing-strategy/`, `DEFERRED-ROLES.md` Public Relations, `research/STRATEGY.md` Part 4 |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **200 AI companies landscape**: `research/200-ai-companies.md`
- **200 AI coaching companies**: `research/200-ai-coaching-companies.md`
- **Coaching funnel playbook**: `research/coaching-funnel-playbook.md`
- **Org-wide 30-research**: `research/30-research-areas.md` (Areas 2, 7, 8, 12 owner: sales)
- **State**: `state/sales.json` (currently nearly empty)
- **Wrangler issue**: `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (surprise #6 — Worker 404)
- **Marketing strategy**: `marketing-strategy/` repo
- **ICP validation data**: `company/Company/icps/` (if exists)
- **Sibling dept catalogs**: `research/dept-research/{01,02,04..06,board}-*-research-areas.md`

---

**Total sales research areas**: 10
**Cadence breakdown**: 🔴 HOT 4, 🟡 WARM 4, 🔵 COOL 2
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)
**Special note**: Pipeline revival research is 🔴 HOT — without it, no other sales research matters.

