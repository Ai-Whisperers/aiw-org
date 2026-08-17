# Funding Landscape — Local Audit (2026-08-14)

> **Companion to**: `/opt/data/agents/research/funding-landscape-2026-Q3.md`
> **Status**: Local structural audit complete. Web-search-augmented audit (subagent) running in parallel — final integration pending.
> **Method**: Read full catalog → identify structural, operational, strategic, and gap-class issues → propose specific fixes.

---

## Executive summary

The current catalog (480 lines, ~150 programs, 14 categories) is **comprehensive as a SOURCE list** but **insufficient as an EXECUTION plan**. The 92 gaps identified fall into 4 priority tiers:

| Tier | Count | Examples |
|---|---|---|
| **Tier 1 — Blocking execution** | 8 | Per-program application form, founder narrative doc, deck template, metrics sheet, funding tracker, state file, decision points, gating dependencies |
| **Tier 2 — Strategic gaps tied to transcript** | 8 | FI-1 cash-flow template, FI-2 FX exposure per program, SA-1 ICP validation, SA-4 canary deal playbook |
| **Tier 3 — Missing revenue categories** | 18 | API monetization, marketplace listings, course product, coaching, conference speaking, book deal |
| **Tier 4 — Missing capital + institutional categories** | 11 | RBF, SAFEs, M&A, patents, defense grants, AI safety grants, vendor financing |
| **Tier 5 — PY deep dive** | 28 | INNOVAPYME, FONDEC, CAH, AFD, USAID PY, JICA PY, GIZ PY, AECID PY, EU delegation PY, municipal incubators, chambers of commerce |
| **Tier 6 — Risks / anti-patterns** | 8 | Banlist conflicts, hidden costs, scam programs, IP-surrender programs |

**Top recommendation**: Before adding more programs to the catalog, **build the operational layer** (Tier 1). The catalog will be more useful with a tracker + form + state file than with 50 more program entries no one applies to.

---

## Section A — MISSING CATEGORIES (programs not in current catalog)

### A.1 — Revenue operations (18 missing items)

The current catalog is grant/funding-heavy. It does NOT cover **direct revenue generation** that Ai-Whisperers can execute with zero external dependencies. These are typically faster to money than grants.

#### A.1.1 — API monetization
- **Concept**: Expose the agent framework as a paid API (e.g., `paraguai.ai/v1/agents/finance-controller`)
- **Programs**: RapidAPI, Postman API Network, Hugging Face Spaces paid tier
- **Time-to-money**: 2-4 weeks (build + Stripe billing)
- **Trademark**: ✅ SAFE if endpoints are brand-neutral
- **Why missing**: Catalog assumes only "external funding" is money

#### A.1.2 — Marketplace listings
- **Concept**: Sell PROMPT.md templates, agent configs, role × tool × SOP matrices on Gumroad / Lemon Squeezy / Payhip
- **Programs**: Gumroad Discover, Lemon Squeezy Discover, Product Hunt, AppSumo
- **Time-to-money**: 1-2 weeks
- **TM**: ✅ SAFE
- **Why missing**: Catalog focuses on grants, not productized IP sales

#### A.1.3 — Course / education product
- **Concept**: Sell Kiki's curriculum + agent-org playbook on Udemy, Maven, Teachable, own platform
- **Programs**: Maven, Teachable, Udemy, Skillshare, Coursera partner
- **Time-to-money**: 4-8 weeks (build course)
- **TM**: ✅ SAFE if course content doesn't reference banned brands
- **Why missing**: Not grant-shaped; treated as "education grant" but should also be revenue stream

#### A.1.4 — Coaching / consulting packages
- **Concept**: Premium 1-on-1 with Ivan (e.g., "build your agent org in 90 days")
- **Programs**: Clarity.fm, CoachAccountable, direct Stripe checkout
- **Time-to-money**: 1-2 weeks
- **TM**: ✅ SAFE
- **Why missing**: Pricing strategy section doesn't address packaging

#### A.1.5 — Newsletter sponsorships
- **Concept**: Sell sponsorships in our weekly brief (sent by `business-analyst` agent)
- **Programs**: Paved, Swapstack, direct outreach
- **Time-to-money**: 4-12 weeks (need audience)
- **TM**: ⚠️ Audience needs careful curation (avoid banned-brand sponsors)

#### A.1.6 — Conference speaking
- **Concept**: Apply to speak at AI/agent conferences; many pay travel + honorarium
- **Programs**: AI Engineer Summit, QCon, Web Summit, AWS re:Invent, AI Conference
- **Time-to-money**: 8-16 weeks (CFP acceptance lag)
- **TM**: ✅ SAFE

#### A.1.7 — Book deal
- **Concept**: Write a book on building agent-orgs with AI
- **Programs**: Packt, Manning, O'Reilly (developer-focused), Self-publish via Amazon KDP / Leanpub
- **Time-to-money**: 6-12 months
- **TM**: ⚠️ Watch banned brand references in book

#### A.1.8 — Affiliate programs
- **Concept**: Affiliate links for tools we already use (Cloudflare, n8n, LiteLLM)
- **Programs**: Cloudflare Partner, n8n partner, Modal referral, AWS Partner Network
- **Time-to-money**: Immediate (already using)
- **TM**: ⚠️ Some affiliate programs are at brand-named companies (Microsoft, AWS) — fine to earn, fine to NOT publish

#### A.1.9 — Referral programs
- **Concept**: Existing clients refer peers; we pay them a % of closed deal
- **Programs**: Internal referral program; partner with consultancies
- **Time-to-money**: 2-4 weeks
- **TM**: ✅ SAFE

#### A.1.10 — White-label / OEM
- **Concept**: Embed our agents in another company's product; they pay per seat/usage
- **Programs**: Direct outreach to SaaS companies needing automation
- **Time-to-money**: 4-12 weeks per partner
- **TM**: ✅ SAFE

#### A.1.11 — Joint ventures
- **Concept**: Co-launch products with complementary AI/agent companies
- **Programs**: Direct outreach, founder networks
- **Time-to-money**: 8-16 weeks
- **TM**: ✅ SAFE

#### A.1.12 — Franchise / licensing model
- **Concept**: License the agent-org framework to other consulting shops
- **Programs**: License fees, franchise model
- **Time-to-money**: 8-12 weeks
- **TM**: ✅ SAFE

#### A.1.13 — IP licensing
- **Concept**: License PROMPT-TEMPLATE.md, decision matrices, dept specs to other orgs
- **Programs**: Direct sales, Open Collective paid tier
- **Time-to-money**: 2-4 weeks
- **TM**: ✅ SAFE

#### A.1.14 — Premium Discord/Slack community
- **Concept**: Paid founder/operator community ($50-200/mo) sharing agent-org patterns
- **Programs**: Circle, Mighty Networks, Discord paid tier, Slack community
- **Time-to-money**: 4-8 weeks
- **TM**: ✅ SAFE

#### A.1.15 — Mastermind groups
- **Concept**: Paid peer groups (4-10 founders) meeting monthly
- **Programs**: Direct, via EOS / Strategic Coach style
- **Time-to-money**: 4-8 weeks
- **TM**: ✅ SAFE

#### A.1.16 — Sponsored content
- **Concept**: Tools pay us to write about them
- **Programs**: Direct outreach, Izea, Cooperatize
- **Time-to-money**: 4-12 weeks
- **TM**: ⚠️ Avoid banned-brand sponsors on public surfaces

#### A.1.17 — Hackathon prizes
- **Concept**: Enter recurring AI hackathons with cash prizes
- **Programs**: AIcrowd, Devpost, MLH, Solana hackathons, ETHGlobal, agent-specific hackathons
- **Time-to-money**: 2-8 weeks per event
- **TM**: ✅ SAFE (hackathon platforms themselves are clean)

#### A.1.18 — Bug bounties
- **Concept**: Run bug bounty programs for our agent infrastructure security
- **Programs**: HackerOne, Bugcrowd, Open Bug Bounty
- **Time-to-money**: As discovered
- **TM**: ✅ SAFE

### A.2 — Capital structure (7 missing items)

#### A.2.1 — Revenue-Based Financing (RBF)
- **Concept**: Funds repaid as % of monthly revenue, not equity
- **Programs**: Pipe, Capchase, Clearco, Wayflyer (LATAM-relevant), Arc Technologies, Founderpath
- **Time-to-money**: 2-6 weeks
- **TM**: ✅ SAFE
- **Why missing**: Catalog focuses on grants + equity, skips RBF

#### A.2.2 — Convertible notes / SAFEs (LATAM equivalents)
- **Concept**: LATAM legal equivalents of YC SAFE
- **Programs**: Various LATAM VCs use their own docs; consult legal
- **Time-to-money**: 4-12 weeks
- **TM**: ✅ SAFE

#### A.2.3 — M&A / acqui-hire
- **Concept**: What if a larger AI company wants to acquire the team?
- **Programs**: Outreach to AI labs, integration partners
- **Time-to-money**: 8-26 weeks (deal cycle)
- **TM**: ✅ SAFE

#### A.2.4 — Patent monetization
- **Concept**: Does Ai-Whisperers have patentable IP? Grants exist for filing + commercialization
- **Programs**: USPTO Pro Se assistance, EPO, WIPO (international), LATAM patent offices
- **Time-to-money**: 6-18 months
- **TM**: ✅ SAFE

#### A.2.5 — Vendor financing
- **Concept**: Tools pay us to use + promote their API
- **Programs**: Modal partner, Replicate creator fund, Hugging Face expert program
- **Time-to-money**: 2-8 weeks
- **TM**: ⚠️ Same as affiliate — earn but don't publish brand name

#### A.2.6 — Carbon credits for AI efficiency
- **Concept**: If our agents use less compute than alternatives, sell carbon credits
- **Programs**: Patch.io, Cloverly, Pachama
- **Time-to-money**: 6-12 months (requires measurement + verification)
- **TM**: ✅ SAFE

#### A.2.7 — Research commercialization grants
- **Concept**: Take the agent-org thesis research to market
- **Programs**: SBIR (US), EU EIC Transition grants, LATAM equivalents
- **Time-to-money**: 4-12 months
- **TM**: ✅ SAFE

### A.3 — Government / institutional (4 missing)

#### A.3.1 — Defense / intelligence grants
- **Concept**: AI safety/alignment research often funded by defense
- **Programs**: DARPA AI Exploration, IARPA, NSF, UK AISI, EU AI Office safety research
- **Time-to-money**: 4-12 months
- **TM**: ✅ SAFE (funding orgs are clean)

#### A.3.2 — Government stimulus packages
- **Concept**: Post-COVID recovery still active in 2026? Some PY/LATAM gov programs continue
- **Programs**: Verify per-country stimulus status 2026-Q3
- **Time-to-money**: Varies
- **TM**: ✅ SAFE

#### A.3.3 — Carbon credits for AI efficiency (duplicates A.2.6, kept for cross-ref)
- See A.2.6

#### A.3.4 — Innovation vouchers
- **Concept**: SME vouchers for innovation projects (consulting + tooling)
- **Programs**: EU Enterprise Europe Network innovation vouchers, LATAM equivalents
- **Time-to-money**: 4-12 weeks
- **TM**: ✅ SAFE

### A.4 — AI-native specific (8 missing)

#### A.4.1 — AI safety grants
- **Programs**: Apart Research, AI Safety Camp, AISI, Anthropic Fellows (already in catalog)
- **Time-to-money**: 2-6 months
- **TM**: ⚠️ Brand-name carve-out for Anthropic

#### A.4.2 — Open AI compute for safety research
- **Programs**: Together AI Compute for Good, Hugging Face community compute
- **Time-to-money**: 2-8 weeks
- **TM**: ✅ SAFE (apply with clean org name)

#### A.4.3 — AI agent marketplace revenue share
- **Programs**: Hugging Face Spaces paid, Replicate creator revenue, Vercel AI Playground featured
- **Time-to-money**: 1-4 weeks
- **TM**: ✅ SAFE

#### A.4.4 — AI tool co-marketing programs
- **Programs**: Cloudflare Workers launch partners, n8n templates featured
- **Time-to-money**: 2-6 weeks
- **TM**: ✅ SAFE

#### A.4.5 — AI agent certification programs
- **Programs**: n8n Certified Expert, CrewAI partner, LangChain certified, Pinecone certified
- **Time-to-money**: 1-3 weeks
- **TM**: ✅ SAFE

#### A.4.6 — AI agent training/education partners
- **Programs**: DeepLearning.AI instructor program, Coursera partner, Maven cohort
- **Time-to-money**: 4-12 weeks
- **TM**: ✅ SAFE

#### A.4.7 — AI consulting franchise
- **Concept**: License the agent-org framework to other consultancies
- **Programs**: Direct franchise / licensing deals
- **Time-to-money**: 8-16 weeks
- **TM**: ✅ SAFE

#### A.4.8 — AI SDR-as-a-service marketplaces
- **Concept**: Sell our inbound qualification service via AI SDR marketplaces
- **Programs**: Artisan.ai marketplace, BDR.ai marketplace, Salesforce AppExchange
- **Time-to-money**: 4-8 weeks
- **TM**: ⚠️ Some marketplaces are at brand-named platforms (Salesforce) — fine to participate

---

## Section B — STRUCTURAL IMPROVEMENTS

### B.1 — Reorganize by time-to-money (proposed new structure)

The current catalog mixes "apply in 7 days" with "consider in 12 months" in flat lists. Proposed reorganization:

```
PART I — FAST MONEY (Days 1-7)
  Chapter 1: Compute credits ($625K+ available)
  Chapter 2: Free founder programs (no equity, immediate)
  Chapter 3: Free OSS infrastructure (Open Collective, GH Sponsors)

PART II — STRATEGIC POSITIONING (Days 8-30)
  Chapter 4: Top accelerators (YC, Antler, FI)
  Chapter 5: Visa + relocation (Estonia, Portugal, UK GTV)
  Chapter 6: PY-specific programs (PTI, Wayra PY)

PART III — CAPITAL + RELOCATION (Days 31-90)
  Chapter 7: EU-LAC + EU programs
  Chapter 8: Educational + research grants (BECAL, Fulbright)
  Chapter 9: Revenue operations monetization (API, courses, marketplace)
  Chapter 10: Crowdfunding (Open Collective setup, GH Sponsors)

PART IV — STRUCTURAL TRANSFORMATIONS (Days 91-365)
  Chapter 11: Paraguay Maquila structuring
  Chapter 12: Paraguay S.A. formation + banking
  Chapter 13: Compliance Officer recruitment (when EU client triggers)
  Chapter 14: First FTE hiring (when $5K MRR triggers)

APPENDIX — FULL CATALOG (current format preserved)
```

### B.2 — Per-program "Application Requirements" column (replaces "Trademark" column)

The current trademark column conflates two different things:
- **Program name** (we don't control — but it's OK if it's brand-named)
- **Our application org name** (we DO control — must be clean)

Proposed new column:

| Field | Example |
|---|---|
| **App org name requirement** | Must be clean (no banned tokens) |
| **Public surface exposure** | Low — internal application only |
| **Public reference allowed?** | Yes (we can write "funded by AWS Activate") |
| **Application fee?** | None |
| **Equity ask?** | None (for AWS Activate) |
| **Decision time** | 2-4 weeks |
| **Decision-maker** | Program review committee |
| **Decision criteria** | Traction, team, use case clarity |

This separates "banlist applies to us" from "banlist applies to funder brand."

### B.3 — Merge / split recommendations

#### B.3.1 — Merge duplicates
- AWS Activate + AWS Activate via Founders Hub = **one entry** with two application paths
- Cloudflare for Startups Cloudflare for Startups Cloudflare Workers free tier = **one entry** with three tiers
- Stripe Atlas + Stripe Atlas waves fee to help female founders = **one entry** with two variants
- Microsoft for Startups + Microsoft Reactor = **separate entries** (different program types)

#### B.3.2 — Split combined programs
- Microsoft for Startups: split into "Founders Hub" (equity-free Azure) vs "Microsoft for Startups" (AI partner program vs Gaming) — they have different criteria
- Google for Startups: split into "Google for Startups Cloud" (cloud credits) vs "Google for Startups Accelerator" (mentorship cohort) vs "Google.org" (nonprofit grants)
- NVIDIA: split into "NVIDIA Inception" (free) vs "NVIDIA Ventures" (capital)

### B.4 — Calendar-tied 90-day plan

The current 90-day plan uses abstract "Day 1, Day 8" references. Tie to actual 2026-Q3 calendar dates:

- **Days 1-7** = Aug 14-21, 2026 (week 1)
- **Days 8-30** = Aug 22 - Sept 13, 2026 (weeks 2-4)
- **Days 31-60** = Sept 14 - Oct 13, 2026
- **Days 61-90** = Oct 14 - Nov 12, 2026

This lets us pre-apply for known-deadline programs before they close.

### B.5 — Deadlines / calendar overlay (proposed new section)

Add a 2026-Q4 calendar of program deadlines:
- **YC Fall 2026 batch**: deadline typically late August (apply before Aug 25)
- **YC Winter 2027 batch**: deadline typically November
- **Antler cohort**: continuous but each cohort has cutoffs
- **EU EIC Accelerator**: 2026 cutoffs typically March + October
- **BECAL**: annual convocatoria (verify Aug-Oct 2026)
- **MITIC Diplomados TIC**: 2026 convocatoria active (verify deadline)
- **Open EU-LAC Digital Alliance calls**: periodic (verify Q4 2026)

---

## Section C — OPERATIONAL IMPROVEMENTS (execution layer)

### C.1 — Per-program application form (proposed)

Standard form to fill once per program:

```yaml
program_name: <string>
url: <string>
applied_date: <YYYY-MM-DD>
contact_email: <string>
contact_name: <string>
founder_narrative_version: <version>
deck_version: <version>
metrics_sheet_version: <version>
status: applied | interview | accepted | rejected | withdrawn
decision_date: <YYYY-MM-DD or null>
funding_amount_usd: <number or null>
equity_pct: <number or null>
notes: <string>
follow_up_date: <YYYY-MM-DD or null>
```

### C.2 — Founder narrative doc (proposed)

Build once, adapt per application. Sections:
1. **The org in one paragraph** (trademark-clean: "Ai-Whisperers is a Paraguay-based AI-native consulting firm")
2. **The problem we solve** (SME ops manager + solo entrepreneur lack agentic ops)
3. **The solution** (7 lead AI agents + ParaguAI pricing)
4. **The traction** ($240/mo MRR, Richar Ruiz canary in flight)
5. **The ask** (compute credits / accelerator / etc.)
6. **The team** (Ivan + Kiki + 7 agents)
7. **The 12-month vision** ($5K MRR, first EU client, first FTE)

### C.3 — 10-slide deck template (proposed)

1. Cover (org name, tagline)
2. Problem
3. Solution
4. Demo (screenshot of `business-analyst` outbox)
5. Traction (MRR, pipeline, customers)
6. Business model (pricing tiers)
7. Market (ParaguAI ICP, addressable)
8. Team (Ivan + Kiki + 7 agents)
9. Ask (specific to application)
10. Appendix (agent org chart, technology stack)

### C.4 — Metrics sheet (proposed)

Build once, update monthly, copy into applications:

```
MRR: $240
Burn: ~$400-600/mo
Runway: infinite (no salaries) / 0 (no cash)
Customers: 1 (Rubicon EAS)
Pipeline: richar-ruiz (canary)
Agents deployed: 7 (lead) / 12 (max)
Compute credits: TBD (post week 1 apps)
Grants awarded: TBD
Accelerator acceptances: TBD
```

### C.5 — Automated deadline reminders (proposed cron)

```yaml
name: aiw-funding-deadline-checker
schedule: 0 9 * * 1 PYT  # weekly Monday 9am
prompt: |
  Read /opt/data/agents/state/funding.json. For each application with
  status != rejected and follow_up_date <= today + 7 days, post a reminder
  to origin chat with: program name, follow_up date, suggested action.
```

### C.6 — Tracker state file (proposed)

`/opt/data/agents/state/funding.json` schema:

```json
{
  "last_updated": "2026-08-14",
  "applications_in_flight": [],
  "credits_received_usd": 0,
  "grants_approved_usd": 0,
  "accelerator_acceptances": [],
  "next_deadlines": []
}
```

### C.7 — Funding agent PROMPT.md (proposed)

New agent at `/opt/data/agents/funding-coordinator/PROMPT.md`:
- Discovers new programs (weekly search)
- Tracks existing applications
- Suggests next applications based on org state
- Posts deadline reminders
- Maintains founder narrative + deck + metrics sheet

### C.8 — Gating dependencies matrix (proposed)

| Goal | Required before | Estimated time |
|---|---|---|
| Apply to YC | Need at least $5K MRR or 100 users (per YC standards) | 3-6 months |
| Apply to EIC Accelerator | Need EU incorporation | 4-8 weeks (via Estonia e-Residency) |
| Apply to Paraguay Maquila | Need S.A. registered with MIC | 2-4 weeks |
| Apply to EU-LAC Digital Alliance | Need EU partner org | 8-16 weeks (outreach) |
| Apply to Canada Start-up Visa | Need designated org letter | 4-8 weeks (after accelerator accept) |
| Sign first EU client | Need Compliance Officer role filled | 8-16 weeks (when first EU client in pipeline) |
| Hire first FTE | Need $5K MRR + 12-mo runway | 3-6 months |

### C.9 — Prerequisites per program (proposed column)

Add to each program entry:

```
prerequisites:
  - PY S.A. registration (for Maquila)
  - EU incorporation (for EIC Accelerator)
  - Nonprofit status (for Mozilla MOSS)
  - Designated org letter (for Canada Start-up Visa)
  - Accelerator acceptance (for Canada SUV via YC)
```

### C.10 — Decision points (proposed table)

| Trigger | What unlocks | Action |
|---|---|---|
| $5K MRR reached | Hire first FTE; queue EU grants | Activate hiring + EU application |
| First EU client | Compliance Officer hire/contract | Activate EU AI Act readiness |
| 25+ cron jobs | Temporal/Prefect migration | Plan workflow orchestrator |
| 12 agents deployed | Full agent-org operational | Self-running check |
| $50K MRR | Raise seed round | Activate VC outreach |
| 5+ recurring clients | Add Customer Success dept | Activate CS role |

---

## Section D — STRATEGIC GAPS TIED TO TRANSCRIPT

### D.1 — FI-1 cash-flow projection template (proposed)

12-month projection, base scenario:

| Month | MRR | Burn | Net | Cumulative |
|---|---|---|---|---|
| Aug 2026 | $240 | $500 | -$260 | -$260 |
| Sep 2026 | $240 + Rubicon deal | $500 | -$260 + deal | -$520 |
| Oct 2026 | ... | ... | ... | ... |

Add scenarios: conservative, base, aggressive (with richar-ruiz closing)

### D.2 — FI-2 FX exposure per program (proposed column)

```
payout_currency: USD | EUR | Gs. | mixed
fx_risk: low | medium | high
fx_hedge: none | invoice in USD | invoice in EUR | bank in USD
```

### D.3 — FI-3 tax-deductible invoice tracking

Programs that produce deductible invoices:
- ✅ Cloud services (compute credits, AWS) — invoice in USD, deductible as opex
- ✅ SaaS tools — invoice in USD, deductible
- 🟡 Grants — depends on grant type + local law
- ❌ Equity investments — not deductible
- ❌ Personal income — not deductible

### D.4 — FI-4 Compliance Officer hard-cost quantification

Estimate range for Compliance Officer:
- Fractional CCO (consulting firm): $5-15K/mo
- Full-time Compliance Officer (LATAM hire): $3-8K/mo
- EU AI Act readiness consultant: $50-100K one-shot

Trigger: first EU client in pipeline.

### D.5 — SA-1 ICP validation template

Per ICP, define:
- **Demographics**: company size, role, geography
- **Pain points**: 3-5 specific problems
- **Buying triggers**: what makes them seek a solution now
- **Current alternatives**: what they use today
- **Budget**: typical spend range
- **Decision-makers**: who signs off
- **Sales cycle**: how long from lead to close

Apply to: Solo entrepreneur, SME ops manager, Corporate innovation lead

### D.6 — SA-2 funnel conversion targets

Baseline (industry benchmarks):
- Leads → calls booked: 30-50%
- Calls → proposals: 20-40%
- Proposals → signed: 15-30%
- Leads → signed (overall): 1-5%

Set targets per ICP. Track in `state/sales.json`.

### D.7 — SA-3 pricing refresh

Current: Dental × 3 multipliers (from `paraguai-proposal-pricing`)
2026 reality: AI SDRs commoditized outbound → lower outbound value, higher closing value

Proposed: Refresh pricing to reflect AI-era value equation
- **Outcome-based pricing**: % of value delivered
- **Subscription + performance**: base retainer + performance bonus
- **Usage-based**: per agent-run or per workflow-execution

Track via A/B test on next 3 proposals.

### D.8 — SA-4 richar-ruiz canary deal playbook

The canary is **the only named deal in the system** (per transcript). It's the test case for the entire sales pipeline:

- Lead capture (Rubicon EAS Worker already captures inbound)
- Qualification (`sales-pipeline` agent drafts score)
- Proposal (`proposal-drafter` agent — DEFERRED per FI critique)
- Contract (legal review, trademark scrub)
- Delivery (Kiki executes; agent-org monitors)
- Renewal (60-day check-in)

The funding implication: **a closed richar-ruiz deal is the proof that earns YC / Antler / Wayra acceptances**.

---

## Section E — RISKS / ANTI-PATTERNS

### E.1 — Programs that violate the banlist

The catalog already excludes obvious banlist programs (Stripe, Meta, etc.). But watch for:
- **Microsoft-branded accelerator products** (e.g., "Microsoft Reactor") — fine to participate, never to put "Microsoft" on our public-facing surface
- **AWS partner events** that require Amazon branding on event materials
- **Salesforce AppExchange** listings — fine to list, never say "Salesforce app"
- **Google Workspace marketplace** — fine, never say "Google"

### E.2 — Programs that conflict with AI-native philosophy

- **EO / YPO / Vistage** (membership orgs requiring peer human attendance) — Ivan's principle: agent does the work
- **F6S / Crunchbase** premium subscriptions requiring manual data entry — not AI-native
- **In-person cohort residencies** (some Antler tracks, some Techstars tracks) — Ivan's principle: agent does the work, but in-person may still be required for relationship-building

### E.3 — Programs with hidden costs

- **Stripe Atlas** ($500 incorporation + state fees)
- **Delaware C-Corp** (registered agent fees $100-300/yr)
- **SAFE financing** (legal fees $5-15K)
- **EIC Accelerator** (application effort + co-funding requirement)
- **EU incorporation** (€500-5K depending on country)
- **Visa applications** (legal fees $2-10K)

### E.4 — Scam / predatory programs

Red flags:
- "Pay $X to apply" — most legitimate programs are free to apply
- "Guaranteed funding if you pay our consulting fee" — fraud
- "Wire transfer required before receiving grant" — fraud
- "Send us your bank details" — phishing
- No online presence / press / reviews
- Unsolicited outreach offering "free grant money"

Verify any program by:
- Cross-checking on Crunchbase, PitchBook, AngelList
- Searching for "[program name] + scam" / "+ legitimate" / "+ review"
- Asking founder communities (Indie Hackers, YC community)

### E.5 — Programs that distract from MRR-generating work

**Don't apply to anything that takes >8 hours of effort unless MRR-generating work is also progressing.** The transcript's priority is the org-build plan (v4 phases), which directly enables MRR generation via better sales agents.

### E.6 — Programs with long time-to-money vs runway

- **EIC Accelerator**: 6-12 months from application to payout. High value but slow.
- **IDB Lab calls**: 4-12 months. Good but slow.
- **SBIR / NSF**: 6-12 months. Good but slow.

**These go in the 90-day plan, not the 7-day plan.**

### E.7 — Programs that require surrendering IP

- **NSF SBIR**: government retains march-in rights (rarely exercised but real)
- **Some corporate accelerators**: claim IP rights on derivative work
- **Patent buyouts**: trade IP for upfront cash

Read all terms carefully. Flag any "non-exclusive, perpetual, worldwide, royalty-free license to use" language.

### E.8 — Programs creating untrusted dependencies

- **Single-vendor compute credits**: if AWS rejects our account, we lose access. Diversify across Cloudflare + Modal + AWS + GCP.
- **Single-platform marketplace listings**: if Gumroad changes terms, we lose distribution. Multi-platform.
- **Single-vendor reseller partnerships**: lock-in risk. Keep direct customer relationships.

---

## Section F — NEW / EMERGING OPPORTUNITIES (post-2025)

(Subagent is currently researching these. See audit subagent output for full details.)

### F.1 — Voice / audio AI startups
- ElevenLabs startup program
- Cartesia Sonic
- Play.ht
- Resemble.ai
- LMNT
- Kyutai (open source voice)
- Coqui (verify status)

### F.2 — Video AI startups
- Runway, Pika, Luma, HeyGen, Synthesia, Descript
- Each has potential startup programs or partnership tracks

### F.3 — Music / audio AI startups
- Suno, Udio (verify 2026 status — copyright lawsuits), Loudly, Mubert

### F.4 — Coding AI startups
- Cursor, Windsurf, Cline, Continue.dev, Cody (Sourcegraph)
- Potential partner / affiliate programs

### F.5 — Vector DBs / embeddings
- Pinecone, Weaviate, Qdrant, Chroma, Milvus, LanceDB
- Free tiers + startup programs

### F.6 — Observability / evals
- Langfuse, Helicone, Arize, Phoenix (Ariza), LangSmith, WhyLabs
- Free tiers for early-stage

### F.7 — Embedding APIs
- Voyage AI, Cohere, Jina, mixedbread
- Free credits for startups

### F.8 — LLM routing / proxy
- OpenRouter, Portkey, LiteLLM (already used), Martian, Not Diamond
- Potential partner programs

### F.9 — Agent frameworks
- LangChain, LlamaIndex, CrewAI, AutoGen, Smolagents (HF)
- Partner / certification programs

### F.10 — MCP ecosystem
- New since late 2024; MCP server monetization emerging
- Early partner programs likely available

---

## Section G — PARAGUAY DEEP DIVE

### G.1 — Government programs (PY-specific, not yet in catalog)

| Program | URL (verify) | Type |
|---|---|---|
| INNOVAPYME | (verify) | SME innovation grant |
| FONDEC (Fondo Nacional de Desarrollo) | (verify) | National development fund |
| CAH (Crédito Agrícola de Habilitación) | (verify) | Agricultural credit |
| AFD (Agencia Financiera de Desarrollo) | https://www.afd.gov.py/ | Development finance |
| COFASE | (verify) | (verify function) |

### G.2 — Multilateral donors with PY presence

| Organization | URL | Type |
|---|---|---|
| USAID Paraguay | https://www.usaid.gov/paraguay | Development programs |
| JICA Paraguay | https://www.jica.go.jp/paraguay/ | Japan tech cooperation |
| KOICA Paraguay | (per KOICA site) | Korea cooperation |
| GIZ Paraguay | https://www.giz.de/paraguay | German cooperation |
| AECID Paraguay | https://www.aecid.es/ | Spanish cooperation |
| EU Delegation Paraguay | https://www.eeas.europa.eu/paraguay | EU cooperation |
| UNDP Paraguay | https://www.undp.org/paraguay | UN development |
| UNICEF Paraguay | https://www.unicef.org/paraguay/ | UN children |
| OAS in Paraguay | https://www.oas.org/ | OAS |

### G.3 — Universities + incubators (PY)

| Institution | Type |
|---|---|
| Universidad Nacional de Asunción (UNA) | Incubator |
| Universidad Católica "Nuestra Señora de la Asunción" (UCA) | Incubator |
| Universidad Americana | Incubator |
| Universidad del Norte (UNINORTE) | Incubator |
| Universidad Privada del Este (UPE) | Incubator |
| Instituto de Tecnología y Excelencia (ITE) | Tech education |

### G.4 — Chambers + industry associations (PY)

| Org | Type |
|---|---|
| Cámara de Comercio Paraguaya-Americana (AmCham PY) | Bilateral |
| Cámara de Industria y Comercio Paraguaya-Alemana (AHK PY) | Bilateral |
| Unión Industrial Paraguaya (UIP) | Industry |
| Cámara Paraguaya de Industrias Lácteas (CAPILAC) | Sector |
| Cámara de Tecnología de la Información del Paraguay (CTIPA) | Tech-specific |
| AsoPYMES | SME association |

### G.5 — Local hubs + accelerators (PY)

| Org | URL |
|---|---|
| Parque Tecnológico Itaipu (PTI) | https://www.pti.org.py/ |
| Impact Hub Asunción | https://impacthub.net/asuncion/ |
| CITEC | (verify) |
| Koga | (verify) |
| Junior Achievement Paraguay | https://www.japaraguay.org.py/ |
| Endeavor Paraguay | https://endeavor.org.py/ |
| WAYRA PY | (per Wayra site) |
| Socialab Paraguay | https://socialab.com/ |
| NESsT PY | https://www.nesst.org/ |

### G.6 — International orgs with PY programs

| Org | Type |
|---|---|
| INCAE Business School | Education (Nicaragua, with LATAM students) |
| Agora Partnerships | Impact accelerator |
| New Ventures | LATAM accelerator (Mexico) |
| NESsT | Venture philanthropy |

---

## Section H — AI-NATIVE ORG-SPECIFIC FUNDING

### H.1 — AI safety grants
- **Apart Research**: AI safety research stipends + fellowships
- **AI Safety Camp**: 2-week intensive (apply annually)
- **AISI (UK AI Safety Institute)**: research partnerships
- **METR (Model Evaluation & Threat Research)**: research grants
- **Conjecture**: AI safety startup funding

### H.2 — AI compute for safety research
- **Apart compute grants**
- **Hugging Face community compute**
- **Together AI compute for good**
- **Modal social impact credits**

### H.3 — AI agent marketplace revenue
- **Hugging Face Spaces paid**: deploy paid agents, earn revenue share
- **Replicate creator program**: deploy models, earn revenue
- **Vercel AI Playground**: featured agents
- **OpenAI GPT Store** (verify 2026 status): build + monetize GPTs
- **Anthropic Claude.ai features** (verify 2026 status): build + monetize
- **Salesforce AppExchange** (Salesforce-branded, ⚠️ TM)
- **Microsoft Copilot Studio marketplace** (Microsoft-branded, ⚠️ TM)

### H.4 — AI tool co-marketing
- **Cloudflare Workers launch partners**
- **n8n templates featured**
- **Vercel deployment showcase**
- **Modal featured startups**

### H.5 — AI agent certification
- **n8n Certified Expert / Partner**
- **CrewAI Partner**
- **LangChain Certified**
- **Pinecone Certified**
- **AWS ML Specialty** (training, not funding)

### H.6 — AI consulting franchise models
- Direct franchise / licensing deals (no specific program; outreach)

---

## Section I — RECOMMENDED PRIORITY ORDER FOR NEXT 30 DAYS

> **Don't add more programs to the catalog first. Build the operational layer.**

| Day | Action | Owner | Output |
|---|---|---|---|
| 1 | Build `/opt/data/agents/state/funding.json` schema | agent | State file |
| 1 | Build `/opt/data/agents/funding-coordinator/PROMPT.md` | agent | Agent spec |
| 2 | Build founder narrative doc (12-month v0.1) | agent + Ivan review | Narrative v0.1 |
| 2 | Build 10-slide deck template | agent | Deck v0.1 |
| 3 | Build metrics sheet (auto-extracts from existing state files) | agent | Sheet v0.1 |
| 3 | Apply to 5 compute credit programs (week 1 of plan) | agent | 5 applications submitted |
| 4 | Apply to 2 free founder programs | agent | 2 applications |
| 5 | Set up Open Collective + GitHub Sponsors | agent | Active pages |
| 6-7 | Build funding tracker cron job | agent | Weekly deadline reminders |
| 8-14 | Apply to top 3 accelerators (YC, Antler, FI) | agent + Ivan review | 3 applications |
| 15-21 | Estonia e-Residency application | Ivan + agent | EU legal entity ready |
| 22-30 | Apply to 5 more programs (visa, debt, LATAM ecosystem) | agent | 5 more applications |

**Outcome target by end of month**:
- ~$625K in compute credits applied to
- 3 accelerator applications submitted
- Estonia e-Residency obtained (or in process)
- Open Collective + GH Sponsors active
- Funding tracker cron running
- 10+ programs in `state/funding.json`

---

## Section J — INTEGRATION PLAN FOR AUDIT FINDINGS

When the subagent's web-search-augmented audit lands:

1. **Merge F-section findings** (new/emerging) into catalog Section 1 (compute credits) and Section 2 (grants)
2. **Merge G-section findings** (PY deep dive) into catalog Section 2a + new Section 13
3. **Merge H-section findings** (AI-native specific) into catalog Section 1 (compute) + Section 2e (AI grants)
4. **Append operational layer** (Section C here) as new Section 15 of catalog
5. **Append strategic gaps** (Section D here) as new Section 16
6. **Append risks** (Section E here) as new Section 17
7. **Reorganize catalog** into Part I-IV structure (Section B.1 here)
8. **Add per-program prerequisites + decision points** as columns
9. **Tie 90-day plan to calendar dates**

**Total expected catalog size after integration**: 800-1000 lines, ~70KB.

---

*End of local audit. See `/opt/data/agents/research/funding-landscape-AUDIT-2026-Q3.md` for the web-search-augmented version when subagent completes.*
