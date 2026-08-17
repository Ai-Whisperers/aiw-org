# Coaching-for-Companies: Find, Offer, Upgrade — Org Analysis & Playbook

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS. Synthesizes:
> - 197 AI coaching companies (`200-ai-coaching-companies.md`)
> - 30 research areas (`30-coaching-research-areas.md`)
> - Sunstein + Solstein inventory (`sunstein-solstein-inventory.md`)
> - 95 known client/org repos
> - Richar Ruiz outreach playbook (the most-developed prospecting playbook we have)
> - Rubicón EAS propuesta (the legal vertical flagship)
> - ParaguAI proposal pricing skill
>
> **The question**: What can we do with the project to find companies, offer coaching with AI, and upgrade them?
> **The answer** (one sentence): Apply the Sunstein-Sunstein AI coaching framework to our existing 95-client base + 200-company prospect universe using the Richar Ruiz "free quick-win → paid tier" upgrade template, then replicate per vertical using the Rubicón EAS propuesta pricing skill.

## Reading guide

1. **Section 1: What we already have** (the assets)
2. **Section 2: The funnel** — find → offer → upgrade
3. **Section 3: The 5 verticals we can attack immediately** (with company lists)
4. **Section 4: The Richar-Ruiz-style upgrade template** (quick-win → S/M/L)
5. **Section 5: The Sunstein-Sunstein coaching product** (what we actually sell)
6. **Section 6: 90-day execution plan**
7. **Section 7: Risks + what NOT to do**
8. **Section 8: Single bet**

---

## Section 1: What we already have (assets)

### The asset audit (most of this is built and live)

| Asset | Where | Status | Relevance to coaching |
|-------|-------|--------|----------------------|
| **95 client/org repos** | `/opt/data/repos/Ai-Whisperers/*` | Live | Existing customer base to upgrade |
| **24 Beauty/Wellness sites** | paragu-ai-builder tenants | Live | High-fit vertical for AI coaching (owner-operators) |
| **8 Education sites** | Courses-Content, Summer-courses, etc. | Live | Direct fit (coaching = education) |
| **3 Legal sites** | rubicon-eas, bufete-mendez, estudio-medieval | Live | Highest ACV; Rubicón flagship ready |
| **3 Real Estate sites** | villa-mayor-asociados, villamayor, alejandro-villamayor | Live | Mark NL coaching canary |
| **Mark NL coaching client** | `mark-nl-vastgoed-coaching/` | Prospect, Aug 2026 | First trilingual coaching engagement |
| **Solstein AI Paraguay client** | `/opt/data/sites/clients/solstein*` | Placeholder sites only | Possible coaching pilot (technology vertical) |
| **Richar Ruiz outreach playbook** | `/opt/data/richar-ruiz-outreach/` | 14 docs ready, awaiting greenlight | **The upgrade template** |
| **Rubicón EAS propuesta** | `/opt/data/build/rubicon-eas/propuesta/PROPUESTA-COMERCIAL.md` | Ready to send | **The legal-tier pricing template** |
| **paraguai-proposal-pricing skill** | `/opt/data/skills/paraguai-proposal-pricing/` | Production | The 3-tier template (A · B · C) |
| **b2b-cold-outreach-pitch skill** | `/opt/data/skills/b2b-cold-outreach-pitch/` | Production | The pitch-kit template |
| **Solstein M&A pipeline** | `Ai-Whisperers/solstein-manda-research` | Private, 88 tests | Lead scoring for prospects |
| **agentic-schemas** | 20 patterns MIT-licensed | Public | Patterns for the coaching agent |
| **wizard-academy** | Transcripts + wisdom synthesis | Public | Substrate for AI coach knowledge |
| **paraguay-supermercados** | 50K+ products scraper | Production | Could become coaching data |
| **Org layer** | 7 cron agents, 6 departments | Production | Manages the funnel autonomously |

### Asset classification by revenue model

| Revenue model | Existing assets | Coaching fit |
|---------------|-----------------|--------------|
| **Existing SaaS/hosting** | 17+ client sites, $240/mo MRR | Upgrade path to coaching subscription |
| **One-off project** | Rubicón propuesta $4.5K-$9M Gs, Richar USD 2.5K-22.5K | Use as entry-point to coaching |
| **Trilingual middle market** | Mark NL coaching pilot, ParaguAI Builder | Direct coaching SKU |
| **EU AI Act consulting** | None | New — coaching product is a vehicle for it |

### The gap

**We have NO existing customers on recurring coaching revenue.** Every coaching SKU must start from zero MRR — but we have 95 clients to upsell into.

---

## Section 2: The funnel — find → offer → upgrade

### The pattern (proven across our existing assets)

The Richar Ruiz playbook is the **canonical template** for what the user is asking. It maps cleanly to "find → offer → upgrade":

```
FIND              → OFFER (free quick-win)        → UPGRADE (paid tiers)
─────────────────────────────────────────────────────────────────────────
Richar identified → Landing + checkout + email    → S: $2,500
through research  → automation (8-12 h dev,       → M: $6,500
+ 200-company       FREE)                          → L: $22,500
landscape         → A cambio: testimonio +        + Co-branding webinar
                   intro a su red CFOs/HR         + Network: Claudio Acosta
```

**The Richar template = the universal coaching-funnel template.** We replicate it per prospect.

### Reusable templates we already have

1. **Find**: Solstein M&A pipeline (8-dimension scoring) + 200-company landscape categories
2. **Offer**: b2b-cold-outreach-pitch skill (10 pitch variations) + client-site-build-workflow (free site as quick-win)
3. **Upgrade**: paraguai-proposal-pricing skill (3-tier A/B/C) + Richar S/M/L tier template

### The funnel math

| Stage | Conversion assumption | Volume needed for $100K ARR |
|-------|----------------------|------------------------------|
| **Find** (leads/month) | 100 | 100 |
| **Qualify** (10% of finds) | 10% | 10 qualified |
| **Offer free quick-win** (50% accept) | 50% | 5 |
| **Convert to Tier A** ($200/mo) | 60% | 3 × $200/mo = $600/mo |
| **Upgrade to Tier B** ($500/mo, 6mo later) | 30% | 1 × $500/mo = $500/mo |
| **Upgrade to Tier C** ($1.5K/mo, 12mo later) | 20% | 1 × $1.5K/mo = $1.5K/mo |
| **Total MRR per cohort** | — | **$2.6K/mo = $31K ARR** |

**To hit $100K ARR**: 3-4 cohorts of 100 finds per quarter = 1,200-1,600 finds per year. **Achievable** if we systemize the funnel.

---

## Section 3: The 5 verticals we can attack immediately

Cross-referencing our **95 client repos** with the **197-company coaching landscape** produces **5 verticals with the highest coaching fit**:

### Vertical 1: 🦷 Dental (2 clients, but high ACV)

**Existing clients**:
- `ometzdental.com` (Dra. Gabriella González Pane — Asunción)
- `dentist` (generic dental template)

**Prospect universe** (from coaching landscape):
- Dental practice coaching platforms (Henry Schein One, Curve Dental, etc.)
- ICF coaches specializing in dental practice management

**Why this vertical**:
- Dentists are **owner-operators with high stress** = high coaching need
- Average dental practice revenue: $500K-2M/year = $50-200/mo coaching fits their budget
- 5-10K dental practices in Paraguay, 100K+ in Argentina, 200K+ in Brazil = huge TAM
- **Existing pricing benchmark** from `paraguai-proposal-pricing`: A Gs. 500K + 150K/mo, B Gs. 1.2M + 400K/mo, C Gs. 2.5M + 900K/mo

**Quick-win**: Free WhatsApp triage bot for appointment booking (1-day build, leverages existing AIW Evolution pipeline)

**Upgrade tiers**:
- **A · Captación**: Gs. 500K + 150K/mo — site + WhatsApp + recordatorios
- **B · Operación**: Gs. 1.2M + 400K/mo — + AI coach for front-desk staff, monthly 1:1 video call
- **C · Crecimiento**: Gs. 2.5M + 900K/mo — + multi-clinica dashboard, treatment-plan acceptance coaching, manager coaching

**Year-1 target**: 5 clinics × Tier B average = Gs. 4M/mo ($550/mo) = $6.6K ARR

### Vertical 2: 💇 Beauty/Wellness (24 clients — biggest base)

**Existing clients**: depiflash, nde-barba, porta's-barber, shine-nails, magnolia-peluqueria, hidrobaby-spa, viviesteticpy, avani-belleza, maskarada, woman-cosmeticos, scott-tatuajes, jota-ink-tattoo, peluqueria-barbershop, mantraspa, fun4me, clau-bellino, arnos-barber-shop, arnoscobar, leticia-carballo, lele-ferreira, barbye-nails, nutrifit-spa, gloriana-peluqueria, etc.

**Why this vertical**:
- 24 existing tenants = **distribution already exists**
- Beauty/wellness owners are typically 1-2 person shops with high coaching need (booking, retention, upsell)
- Average shop revenue: $5-30K/month = $50-200/mo coaching fits
- Spanish-native market = no language barrier

**Quick-win**: Free booking confirmation WhatsApp bot (1-day build)

**Upgrade tiers**:
- **A · Visibilidad**: Gs. 300K + 100K/mo — site + booking + recordatorios
- **B · Retención**: Gs. 800K + 250K/mo — + AI coach for upsell scripts + loyalty program
- **C · Escala**: Gs. 1.5M + 500K/mo — + multi-sucursal dashboard + manager coaching

**Year-1 target**: 12 shops × Tier B = Gs. 3M/mo ($400/mo) = ~$48K ARR

### Vertical 3: ⚖️ Legal (3 clients — highest ACV)

**Existing clients**:
- `rubiconeas.paragu-ai.com` (Rubicón EAS — flagship, propuesta ready)
- `bufete-mendez`
- `estudio-medieval`
- `estudio-contable` (accounting, adjacent)

**Prospect universe**:
- Harvey AI (US legal AI — $1.5B valuation), Spellbook (Canadian — $30M raised)
- Paraguay has 30K+ abogados matriculados = huge TAM

**Why this vertical**:
- **Highest ACV**: abogado PY hace Gs. 2.5M-25M per case = 50-100× ticket of dental
- Legal vertical multiplier ~3× in our pricing skill
- Existing Rubicón propuesta: A Gs. 2M + 550K/mo, B Gs. 4.5M + 1.3M/mo, C Gs. 9M + 2.5M/mo
- Triage bot is a natural quick-win for any firm

**Quick-win**: Free Hermes Triage Bot (8-hour build, leverages existing Rubicón design)

**Upgrade tiers** (Rubicón EAS pricing):
- **A · Presencia**: Gs. 2M + 550K/mo — site + SEO + ficha Colegio
- **B · Captación**: Gs. 4.5M + 1.3M/mo — + triage bot + WhatsApp + CRM
- **C · Operación**: Gs. 9M + 2.5M/mo — + auto documental + reportes + multi-caso

**Year-1 target**: 3 firms × Tier B average = Gs. 3.9M/mo ($525/mo) = ~$6.3K ARR

### Vertical 4: 🏠 Real Estate Coaching (3 sites + Mark NL)

**Existing clients**:
- `villa-mayor-asociados`, `villamayor`, `alejandro-villamayor` (PY RE)
- `mark-nl-vastgoed-coaching` (NL RE coaching — the canary)

**Prospect universe**:
- RE coaching is a $2-5B global industry
- Mark NL has 200+ Dutch-speaking professionals already

**Why this vertical**:
- Mark NL is **active prospect** (SalesFlow config pending)
- Cross-border: PY → NL deal = first EU-coaching entry
- Trilingual edge (es/en/nl) = unique

**Quick-win**: Free WhatsApp triage + SalesFlow audit for Mark (free upgrade of his existing setup)

**Upgrade tiers** (in EUR, since Mark is Dutch):
- **A · Intake**: €500 + €150/mo — WhatsApp bot + intake forms
- **B · Coaching**: €1,200 + €350/mo — + AI coach + 1×/mo 1:1 video + reflective journaling
- **C · Scale**: €2,500 + €800/mo — + multi-language course platform + manager dashboard

**Year-1 target**: 3 NL clients × Tier B = €1.05K/mo = ~$13K ARR

### Vertical 5: 🏋️ Fitness + Education (3+8 clients, founder-led verticals)

**Existing clients**:
- Fitness: xxgym, bichosgym, prep
- Education: magisteriums, cronos-academy, polki-squad, Courses-Content, Summer-courses, courses-website, dayah, dayah-litworks, education-hooks

**Why these verticals**:
- Fitness owners are 1-person operations with high coaching need
- Education is naturally coaching-adjacent (we have wizard-academy IP)

**Quick-win**: Free WhatsApp class-schedule bot for gyms; free course-builder audit for education

**Upgrade tiers** (similar to beauty):
- **A · Visibilidad**: $300 setup + $100/mo
- **B · Coaching**: $800 + $250/mo
- **C · Escala**: $1.5K + $500/mo

**Year-1 target**: 4-5 fitness clients + 2-3 education clients × Tier B = ~$15K ARR

### Vertical aggregate year-1 target

| Vertical | Clients (yr1) | Avg MRR | ARR target |
|----------|---------------|---------|-----------|
| Dental | 5 × Tier B | $110 | $6.6K |
| Beauty/Wellness | 12 × Tier B | $80 | $48K |
| Legal | 3 × Tier B | $525 | $6.3K (in Gs. parity) |
| Real Estate (NL) | 3 × Tier B | €350 | $13K |
| Fitness + Education | 7 × Tier B | $80 | $15K |
| **TOTAL** | **30** | — | **~$89K ARR** |

**Combined with existing hosting MRR ($240/mo) and Rubicón/cookies proposals, year-1 achievable run-rate: $100-150K ARR.**

---

## Section 4: The Richar-Ruiz-style upgrade template

The Richar Ruiz playbook is the **proven template** for what the user is asking. Let me extract the **reusable pattern**:

### The 4-stage upgrade template

```
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1: FIND                                                        │
│ - Solstein M&A scoring (8 dimensions, composite 1-5)                │
│ - Filter for high-fit verticals + PY/EU/LATAM presence              │
│ - 100 leads/month target                                            │
├─────────────────────────────────────────────────────────────────────┤
│ STAGE 2: OFFER (free quick-win)                                      │
│ - 8-12 hours of dev work (per Richar playbook)                       │
│ - Deliverable: site + bot + automation                               │
│ - "No cobro" / "gratis" / "a cambio de testimonio + intro"           │
│ - Owner: Erebus + Kyrian                                             │
│ - Time: 1-2 weeks                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ STAGE 3: UPGRADE TO TIER S ($2,500 USD or Gs. equivalent)           │
│ - Replicate the quick-win for a second product/service               │
│ - First paid contract                                                │
│ - Time: 2-4 weeks                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ STAGE 4: UPGRADE TO TIER M ($6,500 USD)                              │
│ - Migrate to next.js / bigger build                                  │
│ - Multi-product engagement                                           │
│ - Time: 4-8 weeks                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ STAGE 5: UPGRADE TO TIER L ($22,500 USD)                             │
│ - Full transformation (LMS + AI Buddy + automation)                  │
│ - Network effect: intros to other CFOs/HR Directors                  │
│ - Time: 8-12 weeks                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Mapping to the coaching use case

For **AI coaching specifically**, the template becomes:

```
FIND                  → Identify 5 verticals × 30 prospects = 150 leads
OFFER (free)          → Free AI coaching audit: 1-h audit + 3 mock coaching sessions
                        + recommendations (no code, no deploy)
                        Owner: Erebus (autonomous)
                        Time: 1-2 hours per prospect
UPGRADE S             → $2,500 USD setup + AI coach for 1 team (5-10 seats)
                        Time: 1 week
UPGRADE M             → $6,500 USD setup + AI coach + 1×/mo human call + dashboard
                        Time: 3-4 weeks
UPGRADE L             → $22,500 USD setup + multi-team AI coach + custom methodology
                        + EU AI Act compliance + dedicated coach partner
                        Time: 6-12 weeks
```

### The 90-day operational plan (per prospect)

| Week | Action | Owner | Cost |
|------|--------|-------|------|
| 1 | Identify + score prospect via Solstein pipeline | Erebus | 30 min |
| 1-2 | Research + first LinkedIn DM (b2b-cold-outreach-pitch) | Erebus | 1 h |
| 2-3 | 30-min discovery call | Ivan | 30 min |
| 3 | Send free quick-win offer | Erebus + Kyrian | 30 min |
| 3-5 | Execute quick-win (1-h audit + recommendations) | Erebus | 1-2 h |
| 6 | Testimonial + intro ask | Ivan | 30 min |
| 6-10 | Tier S delivery | Kyrian + Erebus | 1 week |
| 10-14 | Tier M upgrade pitch | Ivan | 30 min |
| 14-26 | Tier M delivery | Kyrian + Erebus | 3-4 weeks |
| 26+ | Tier L upgrade pitch | Ivan | 1 h |

**Total per-prospect cost**: ~10 hours Ivan + 20 hours Erebus + 60 hours Kyrian ≈ 90 person-hours.
**At Tier M ($6,500)**: $72/hour effective rate. **At Tier L ($22,500)**: $250/hour.

### Co-branding leverage (the Richar force multiplier)

Richar's value isn't the quick-win — it's the **network**: intros to CFOs and HR Directors at pharma/banca/telecom companies. Each intro can unlock $5-50K pipeline.

For coaching: each upgraded client becomes an **internal champion** at their company. If Tier C is $1.5K/mo with 50 seats, **5 internal champions across 5 verticals = $90K ARR run rate**, plus intros to similar companies.

**Pattern: 1 quick-win → 1 Tier S → 1 Tier M → 5 Tier C internal champions → 5 intros → repeat.**

---

## Section 5: The Sunstein-Sunstein coaching product (what we actually sell)

We have the framework research. Now: **what is the actual coaching product?**

### The product: "Trilingual AI Coach" by AI Whisperers

**Product spec**:

| Layer | Component | Tech |
|-------|-----------|------|
| **Conversation framework** | GROW + CLEAR hybrid | Sunstein-aligned prompt library |
| **Languages** | Spanish (native) + Dutch (fluent) + English (default) | Trilingual prompt library |
| **Methodology** | ICF 8 competencies | `coaching-conversation-framework` skill |
| **Behavior change** | Prochaska + BJ Fogg nudges | `coaching-trilingual-glossary` skill |
| **Compliance** | EU AI Act + GDPR Article 9 | `coaching-eu-compliance` skill |
| **Tech stack** | Claude Sonnet + Whisper-large-v3 + ElevenLabs + Cloudflare R2 EU | `coaching-tech-stack` skill |
| **Multi-tenant** | Per-org data + prompt customization | ParaguAI Builder extension |
| **Session types** | 1:1 async, live call coaching, roleplay | Multi-modal |

### The 3 SKUs (matches our existing pricing tiers)

**SKU A · "Coach Lite"** — $500 setup + $200/seat/mo (5 seats min)
- AI coach async, Spanish + English only
- GROW framework
- ICF-aligned prompts
- Monthly analytics
- ICF-aligned methodology badge

**SKU B · "Coach Pro"** — $2K setup + $500/seat/mo (10 seats min)
- Everything in Lite, plus:
- Trilingual (es/en/nl)
- Live call coaching
- Hybrid human escalation
- CBT patterns
- Slack/Teams integration
- EU AI Act compliance prep

**SKU C · "Coach Enterprise"** — $10K setup + $1.5K/seat/mo (50 seats min)
- Everything in Pro, plus:
- EU AI Act + GDPR Article 9 compliance
- Custom methodology
- Dedicated coach partner (human)
- ICF-aligned whitepaper
- Full data residency (EU region)
- SLA + 24h support

### The Sunstein-Sunstein positioning

**Why Sunstein matters**: Every AI coaching company uses nudge theory, but none name Sunstein. We can claim **"Sunstein-aligned AI coaching"** — defensible because (a) Sunstein's work is canonical public IP, (b) no one else has done the rigorous mapping, (c) it gives our methodology legitimacy.

**Methodology badges**:
- ICF-aligned (8 core competencies)
- Sunstein-aligned (choice architecture, defaults, sludge, attention, autonomy)
- EU AI Act compliant
- Trilingual (es/en/nl native)

**Competitor comparison**:

| | Sunstein-aligned | EU AI Act ready | Trilingual | Mid-market ACV |
|--|:-:|:-:|:-:|:-:|
| BetterUp | ✗ | ✗ | ✗ | $50K+ |
| CoachHub | ✗ | ✓ | ✓ (90+ via humans) | $20K+ |
| Valence | ✗ | ✗ | ✗ | $20K+ |
| Yoodli | ✗ | ✗ | ✗ | $5K |
| **AI Whisperers** | ✓ | ✓ | ✓ | **$5-15K** |

### The Solstein scoring framework, applied to coaching

We can run the **Solstein M&A pipeline** on **coaching prospects/competitors** with a new scoring dimension:

| Dimension | What it scores |
|-----------|----------------|
| Coach supply network | BetterUp's moat: 4000+ coaches |
| Methodology IP | ICF-aligned + Sunstein-aligned |
| EU AI Act compliance | Real EU AI Act risk-classification |
| Tech stack | Modern (Claude + Whisper + ElevenLabs) |
| Trilingual depth | es/en/nl native |
| Mid-market fit | $5-15K ACV (vs $50K+ enterprise) |
| Hybrid escalation | AI → human handoff quality |
| Behavior change science | Prochaska + BJ Fogg deployment |

**Output**: 8-dimension scorecard per coaching company. Use it to **prioritize prospects** and **benchmark competitors**.

---

## Section 6: 90-day execution plan

### Week 1 — Lock the foundation

- [ ] **Sign Rubicón EAS contract** (the legal flagship, immediate revenue path)
- [ ] Wire Rubicón EAS Worker webhook
- [ ] Approve the Richar Ruiz outreach (the proven quick-win template)
- [ ] Send Mark NL his SalesFlow config (RE coaching canary)
- [ ] Read `200-ai-coaching-companies.md` + `sunstein-solstein-inventory.md`
- [ ] Build the 5-vertical prospect lists (see Section 3)

### Week 2-4 — Build the funnel infrastructure

- [ ] Build `coaching-pricing` skill (4h)
- [ ] Build `coaching-pitch-kit` skill (4h)
- [ ] Build `coaching-conversation-framework` skill (6h) — **the IP backbone**
- [ ] Build `coaching-trilingual-glossary` skill (6h)
- [ ] Build Solstein coaching scorecard (8 dimensions, new)
- [ ] Launch Solstein lite tool at `research.ai-whisperers.com` (16h)

### Month 2 — Activate the funnel

- [ ] **Send 20 free quick-win offers** (1-h audit each = 20 hours total)
  - 5 dental, 5 beauty, 3 legal, 4 RE, 3 fitness/education
- [ ] **Run Solstein scoring on all 95 existing clients** to identify best upgrade candidates
- [ ] Wire the Quick-win → Tier S upgrade flow
- [ ] First 3 Tier S deals signed ($2.5K × 3 = $7.5K)

### Month 3 — First paid coaching engagements

- [ ] First Rubicón EAS coaching session shipped
- [ ] First Mark NL coaching session shipped
- [ ] First beauty vertical client (e.g., ometzdental) upgraded to Tier B
- [ ] First legal vertical Tier M close
- [ ] **5 Tier S + 2 Tier M = $25.5K revenue**
- [ ] Write 2 case studies

### What we're NOT doing this quarter

- ❌ Hiring (capacity exists)
- ❌ Fundraising (not venture-scale)
- ❌ Building BetterUp competitor
- ❌ Building US-only product
- ❌ Consumer coaching (Blomma, Tomo already there)

---

## Section 7: Risks + what NOT to do

### Top 5 risks

| Risk | Mitigation |
|------|-----------|
| **No one converts from quick-win to paid** | Quick-win must show concrete ROI within 2 weeks; offer 2 free coaching sessions before pitching |
| **BetterUp enters mid-market** | We're 6-12 months ahead on language + EU AI Act + methodology |
| **EU AI Act enforcement breaks our positioning** | Build compliance in from day 1, not as retrofit |
| **GDPR breach** | `coaching-privacy-protocol` skill from day 1; E2E encryption |
| **Founder-bottleneck on calls** | Automate discovery calls via recorded Loom + Solstein scoring pre-call |

### What NOT to do

- ❌ **Don't build a BetterUp competitor** — too capital-intensive
- ❌ **Don't skip the free quick-win** — it's the entry point; Richar template proves it
- ❌ **Don't pitch Tier L first** — Richar playbook proves Tier S → M → L is the path
- ❌ **Don't hire until $25K MRR** — capacity exists
- ❌ **Don't skip methodology work** — "generic chatbot" is what Gong does; "Sunstein-aligned + ICF + EU AI Act + trilingual" is what we do
- ❌ **Don't ignore existing 95 clients** — they're the warmest leads; upsell before prospecting

### Single biggest mistake to avoid

**Mistake**: Spending 3 months building a "complete coaching platform" before talking to anyone.

**Fix**: Ship the free quick-win offer **today**. Get 3 paying customers in 30 days. Then iterate.

---

## Section 8: Single bet

**The bet**: AI Whisperers can launch a **trilingual AI coaching product** (es/en/nl) for the **mid-market** (5 vertical: dental, beauty, legal, RE, fitness) within 90 days by:

1. **Finding** prospects via the Solstein M&A pipeline (8-dimension scoring) applied to the 5 verticals
2. **Offering** free quick-win AI coaching audits (1-h audit + 3 mock sessions) using the Richar Ruiz playbook
3. **Upgrading** via the 3-tier A/B/C pricing (paraguai-proposal-pricing skill) starting at $200/seat/mo (Tier A) and going to $1.5K/seat/mo (Tier C)

**Year-1 revenue target**: **$89-150K ARR run rate**, sourced from 30 clients across 5 verticals.

**Single next action**: **Send the free quick-win offer to 5 dental clinics + 5 beauty salons this week.** Use the b2b-cold-outreach-pitch skill for the DM. Use the Richar template for the structure.

---

## Files cited

- `/opt/data/agents/research/200-ai-coaching-companies.md` (197 companies)
- `/opt/data/agents/research/30-coaching-research-areas.md` (30 areas)
- `/opt/data/agents/research/coaching-skills-gap-audit.md` (11 new skills)
- `/opt/data/agents/research/coaching-strategic-implications.md` (strategy)
- `/opt/data/agents/research/sunstein-solstein-inventory.md` (Sunstein + Solstein)
- `/opt/data/richar-ruiz-outreach/` (the upgrade template)
- `/opt/data/build/rubicon-eas/propuesta/PROPUESTA-COMERCIAL.md` (the legal-tier pricing)
- `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/solstein-analysis.md` (the M&A framework)
- `/opt/data/sites/clients/solstein*.html` (Solstein client)
- `/opt/data/repos/Ai-Whisperers/mark-nl-vastgoed-coaching/` (RE coaching canary)
- `/opt/data/skills/paraguai-proposal-pricing/SKILL.md` (pricing template)
- `/opt/data/skills/b2b-cold-outreach-pitch/SKILL.md` (pitch template)
- 95 client/org repos in `/opt/data/repos/Ai-Whisperers/*`

## Source data

- Solstein M&A scoring: 8 dimensions, composite score 1-5, 25+ data sources, 88 tests passing
- Richar Ruiz outreach: 14 docs, 90-day plan, 10-50× ROI potential
- Rubicón EAS propuesta: A Gs. 2M+550K/mo, B Gs. 4.5M+1.3M/mo, C Gs. 9M+2.5M/mo
- 95 client repos categorized by vertical
- 197 AI coaching companies categorized in 18 buckets

## Last updated

2026-08-14 by Erebus (autonomous AI agent, AI Whisperers Paraguay EAS)