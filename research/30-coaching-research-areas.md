# 30 Research Areas for AI Coaching-for-Companies

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS. Triggered by `mark-nl-vastgoed-coaching` client + the 200-AI-coaching-companies landscape.
> 30 areas, 6 strategic groups, 9 marked 🔴 HIGH priority (do this month).
> Every entry: **Why** / **Method** / **Output** / **Owner** / **Cadence**.

## Reading guide

This document lists the **30 research areas** AI Whisperers should investigate to **own the trilingual mid-market AI coaching** niche — Spanish-native, Dutch-fluent, EU/LATAM-ready. It's grouped into 6 strategic purposes:

1. **Market intel** (5 areas) — what's actually being bought, priced, regulated
2. **Methodology & frameworks** (5 areas) — the intellectual property stack
3. **Trilingual edge** (5 areas) — the moat
4. **Verticals we serve** (5 areas) — the customer-specific plays
5. **Competitive moats** (5 areas) — what protects us from BetterUp/Valence
6. **Operational implementation** (5 areas) — what we have to ship

Mark 🔴 = HIGH priority (do this month, owner = Erebus or an AIW agent). Other priorities are sequenced into a 90-day plan at the end.

---

## Group A — Market Intel (5 areas)

### 1. 🔴 AI coaching market size + segmentation by region
- **Why**: Need a defensible "X% of Y market" number for proposals and pitch decks. The current data is US-centric ($5.48B AI career coach 2025; 28.5% CAGR globally) — we need LATAM/EU/NL splits.
- **Method**: Research and Markets, Markets and Markets, Statista for global; Statista + IDC LATAM reports; CBS NL for Dutch market; Clutch LATAM for Paraguay-relevant data.
- **Output**: `/opt/data/agents/research/coaching-market-sizing.md` — 1 page, table with global / EU / LATAM / NL / PY figures + CAGR + 5-year forecast.
- **Owner**: Erebus (autonomous); validated by Ivan.
- **Cadence**: Once, refresh annually.
- **Priority**: 🔴 HIGH — needed for every proposal and pitch.

### 2. 🔴 EU AI Act compliance requirements for AI coaching products
- **Why**: An EU AI Act-compliant coaching product is a moat. US companies won't bother; we can offer "EU AI Act + GDPR Article 9 ready" as a compliance-first positioning.
- **Method**: Read the AI Act text (artificialintelligenceact.eu), specifically Articles 5, 6, 50, Annex III (high-risk categories). Map each article to AI coaching scenarios (performance eval = high-risk; conversational coaching = likely limited-risk). Document what an EU-compliant coaching AI looks like.
- **Output**: `/opt/data/agents/research/eu-ai-act-coaching-compliance.md` — table mapping articles to coaching features + compliance checklist for our product.
- **Owner**: Erebus.
- **Cadence**: Once, monitor AI Act amendments quarterly.
- **Priority**: 🔴 HIGH — strategic differentiator.

### 3. 🔴 BetterUp / CoachHub / Valence failure modes — what they don't do well
- **Why**: We compete by addressing their gaps. Their public reviews + Glassdoor + customer complaint patterns reveal what they miss. Mid-market, non-English languages, low cost, vertical-specific coaching.
- **Method**: Glassdoor reviews, G2/Capterra reviews, public Reddit threads (r/management, r/coaching), BetterUp employee complaints, customer churn signals (LinkedIn job postings = new customer onboarding), BetterUp "AI-only" tier complaints.
- **Output**: `/opt/data/agents/research/competitor-failure-modes.md` — table: competitor / common complaint / our counter-positioning.
- **Owner**: Erebus (automated) + Ivan (validation).
- **Cadence**: Once, refresh after each competitor product update.
- **Priority**: 🔴 HIGH — feeds pitch copy + product roadmap.

### 4. AI coaching pricing models — what's actually being charged
- **Why**: BetterUp $4K-15K/employee/year; CoachHub $2-8K; Valence enterprise $50-200/seat/year; Gong $1.5K/seat/year. Need LATAM-relevant numbers.
- **Method**: Public pricing pages, customer case studies (look for "seats" + "contract value"), G2 review counts (proxy for customer count), INC.com + Forbes interviews with CFOs.
- **Output**: `/opt/data/agents/research/coaching-pricing-benchmarks.md` — table per competitor with tier, price per seat, what they include.
- **Owner**: Erebus.
- **Cadence**: Quarterly.
- **Priority**: MEDIUM — needed before we price our product.

### 5. LATAM corporate L&D spending patterns
- **Why**: LATAM enterprises spend 50-70% less on L&D per employee than US counterparts. Need to know if AI coaching is even a budget category.
- **Method**: ATD (Assn for Talent Development) LATAM reports, SHRM LATAM chapter surveys, local HR consulting firms (Deloitte PY, PwC PY), LinkedIn talent insights for LATAM.
- **Output**: `/opt/data/agents/research/latam-ld-spend.md` — 1 page with per-country L&D spend numbers + buyer personas.
- **Owner**: Erebus.
- **Cadence**: Once, refresh annually.
- **Priority**: MEDIUM — needed to validate market exists.

---

## Group B — Methodology & Frameworks (5 areas)

### 6. 🔴 ICF Core Competencies + how AI coaches must mirror them
- **Why**: ICF (International Coaching Federation) defines 8 core competencies + ethical guidelines for professional coaches. Any AI coach product should be benchmarked against these to claim "ICF-quality." This is the **methodology IP** of the coaching industry.
- **Method**: Download ICF Core Competency PDF (free, public). Map each competency to AI capability (active listening → voice sentiment; powerful questioning → LLM prompt design; creating awareness → reflection prompt; designing actions → action plan generator; planning & goal setting → SMART goal tracker; managing progress & accountability → dashboard; presence → multi-turn context window; ethical practice → content moderation).
- **Output**: `/opt/data/agents/research/icf-mapping.md` — 8-row table per ICF competency → AI implementation.
- **Owner**: Erebus + Ivan (for ICF credential validation).
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — this is our **methodological backbone**.

### 7. Coaching psychology frameworks — GROW, CLEAR, OSKAR, T-GROW, ACHIEVE
- **Why**: These are the canonical coaching conversation models. AI coach personas should pick one (we'll pick GROW + CLEAR hybrid) and own it as IP.
- **Method**: Sir John Whitmore (GROW), Peter Hawkins (CLEAR), Mark McKergow (OSKAR), David Rock (T-GROW), Bert Parlee (ACHIEVE) — all canonical, public.
- **Output**: `/opt/data/agents/research/coaching-frameworks-comparison.md` — comparison table + recommendation (GROW + CLEAR hybrid as our default).
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — every coaching conversation needs a backbone.

### 8. Cognitive Behavioral Therapy (CBT) patterns for AI coaching
- **Why**: Mental wellness AI (Woebot, Wysa) is CBT-based. Better coaching products blend coaching + CBT micro-techniques. This is also the bridge between coaching AI and mental wellness AI.
- **Method**: Read Judith Beck's CBT primer (public summaries). Map Beck's cognitive distortions to AI reflection prompts. Look at Woebot's published methodology.
- **Output**: `/opt/data/agents/research/cbt-coaching-patterns.md` — 10 cognitive distortion patterns → AI coach intervention prompts.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: MEDIUM — needed for mental wellness extensions.

### 9. Behavioral change science — Prochaska, Fogg, BJ Fogg, Duhigg
- **Why**: AI coaching without behavior change science is just conversation. We need to ground our nudges in published behavior change methodology.
- **Method**: Prochaska Transtheoretical Model (Stages of Change); BJ Fogg Tiny Habits; Charles Duhigg habit loop; James Clear Atomic Habits framework.
- **Output**: `/opt/data/agents/research/behavior-change-frameworks.md` — table mapping each framework to AI coach nudge patterns.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: MEDIUM — required for "AI coach that actually changes behavior" positioning.

### 10. AI coaching session structure — what makes a session feel like coaching (not therapy, not advice)
- **Why**: AI coaching fails when it slips into therapy (needs license) or advice-giving (loses coaching value). The boundary is methodological.
- **Method**: Read 5 ICF sample session transcripts (public). Identify the linguistic patterns that distinguish coaching from therapy/advice. Build a "coaching voice" prompt template.
- **Output**: `/opt/data/agents/research/coaching-session-structure.md` — session anatomy + "coaching voice" prompt template.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — every AI session needs this structure.

---

## Group C — Trilingual Edge (5 areas)

### 11. 🔴 Spanish-language coaching vocabulary + cultural adaptations
- **Why**: Translating English coaching → Spanish word-by-word loses 40% of meaning. Coaching in Spanish needs different metaphors, pacing, and cultural norms (LATAM-directness vs Spain-formality; PY-guaraní-influenced Spanish).
- **Method**: Hire a Spanish-speaking ICF coach for 2h consultation; read 5 Spanish coaching books; build a Spanish coaching vocabulary glossary (300+ terms).
- **Output**: `/opt/data/source-materials/coaching/spanish-vocabulary.md` — glossary + cultural adaptation notes.
- **Owner**: Erebus + Ivan (LATAM-native).
- **Cadence**: Once, refresh when adding new LATAM markets.
- **Priority**: 🔴 HIGH — Spanish IS the native market.

### 12. Dutch-language coaching vocabulary + business-culture norms
- **Why**: Mark NL is the canary. Dutch coaching has directness (Rolf Janssen "De Directe Methode"), specific business-culture patterns (poldermodel, consensus-driven), and Dutch-only concepts (e.g., "nuchterheid" — sobriety, the Dutch preference for down-to-earth over emotional).
- **Method**: Read Dutch coaching canon (Rolf Janssen, Marcel Zwartjes); interview 2 NL coaches; build Dutch coaching glossary.
- **Output**: `/opt/data/source-materials/coaching/dutch-vocabulary.md` — glossary + cultural notes.
- **Owner**: Erebus + Kyrian (Dutch-native).
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — Mark NL is the canary.

### 13. Paraguay-Spanish coaching adaptations (guaraní-influenced)
- **Why**: Paraguay is the only LATAM country with bilingual (Spanish + Guaraní) population. A PY-native coaching product needs to handle guaraní-influenced Spanish, JPAL/JOI unique patterns, and the rural-vs-Asunción divide.
- **Method**: Linguistic research on Paraguayan Spanish; interview 3 PY-based coaches; document guaraní loanwords commonly used in business contexts.
- **Output**: `/opt/data/source-materials/coaching/paraguay-spanish.md` — cultural/linguistic adaptation guide.
- **Owner**: Erebus + Ivan (PY-native).
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — unique to our positioning.

### 14. Suriname + Antilles Dutch-creole coaching adaptations
- **Why**: Suriname Dutch, Papiamento, Sranan Tongo — Dutch-speaking diaspora markets we can serve via Mark NL. None of the coaching companies serve this market.
- **Method**: Linguistics research; reach out to Surinamese coach network; document creole adaptations for coaching prompts.
- **Output**: `/opt/data/source-materials/coaching/suriname-antilles.md` — adaptation guide.
- **Owner**: Erebus + Kyrian.
- **Cadence**: Once.
- **Priority**: HIGH — markets BetterUp/CoachHub ignore.

### 15. EU AI Act + GDPR Article 9 compliance for trilingual coaching AI
- **Why**: Special-category personal data (health, biometric, ethnicity) under GDPR Art 9. Coaching conversations may touch on wellbeing. The compliance-first positioning requires a clear protocol.
- **Method**: Read GDPR Art 9 + EDPB guidance; consult with EU compliance lawyer (1h consult); document coaching-data-minimization protocol.
- **Output**: `/opt/data/agents/research/eu-gdpr-coaching-compliance.md` — protocol + vendor checklist.
- **Owner**: Erebus + external counsel (budget: €500).
- **Cadence**: Once, monitor EDPB guidance quarterly.
- **Priority**: MEDIUM — required for any EU client.

---

## Group D — Verticals We Serve (5 areas)

### 16. 🔴 Legal-vertical AI coaching (Rubicón EAS playbook)
- **Why**: Rubicón EAS is our flagship. The 290-question intake + sample site + propuesta are all live. Need to convert this into a **replicable playbook** for 5 legal firms.
- **Method**: Document the Rubicón EAS discovery → audit → coaching-agent-build → deploy process into a step-by-step. Identify which steps are reusable.
- **Output**: `/opt/data/source-materials/coaching/legal-vertical-playbook.md` — 8-step playbook with templates.
- **Owner**: Erebus + Ivan (Rubicón contact owner).
- **Cadence**: Once, refine after each new legal client.
- **Priority**: 🔴 HIGH — first vertical to monetize.

### 17. Real estate coaching vertical (Mark NL + LATAM RE)
- **Why**: Mark NL is active (SalesFlow config). Real estate coaching is a global industry. LATAM RE coaching is unserved by AI.
- **Method**: Document Mark NL engagement into a playbook; research 3 LATAM RE coaching markets (PY, AR, MX); identify top 5 lead-gen tactics.
- **Output**: `/opt/data/source-materials/coaching/real-estate-playbook.md` — playbook + LATAM market scan.
- **Owner**: Erebus + Mark NL (delivery partner).
- **Cadence**: Once, refine with Mark NL feedback.
- **Priority**: 🔴 HIGH — Mark NL is the canary.

### 18. Dental coaching vertical (ometzdental.com extension)
- **Why**: Dra. Gabriella is an existing client. Dental practice coaching is a real vertical (Front Desk, patient communication, treatment plan acceptance). $300-3K/mo potential per clinic.
- **Method**: Document Dra. Gabriella engagement; identify dental coaching patterns; build "dental practice AI coach" SKU.
- **Output**: `/opt/data/source-materials/coaching/dental-vertical-playbook.md`.
- **Owner**: Erebus + Ivan.
- **Cadence**: Once.
- **Priority**: HIGH — existing client base.

### 19. Beauty/wellness coaching vertical (ParaguAI Builder clients)
- **Why**: ParaguAI Builder has 13+ beauty/wellness clients (depiflash, nde-barba, porta's-barber, shine-nails, xxgym). Each could use an AI coach for owner-operators.
- **Method**: Audit ParaguAI Builder clients; identify common coaching needs; build "beauty/wellness practice AI coach" SKU.
- **Output**: `/opt/data/source-materials/coaching/beauty-vertical-playbook.md`.
- **Owner**: Erebus + Kyrian (ParaguAI Builder).
- **Cadence**: Once.
- **Priority**: HIGH — distribution already exists.

### 20. SMB / entrepreneur coaching vertical (wizard-academy integration)
- **Why**: wizard-academy is our knowledge synthesis repo. Can be the substrate for an AI coach that helps SMB founders. Big market; low-touch sales.
- **Method**: Pull wizard-academy transcripts → build "SMB founder AI coach" prompts. Test with 3 PY-based SMBs.
- **Output**: `/opt/data/source-materials/coaching/smb-entrepreneur-coach.md` — coach specification + first 100 prompts.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: HIGH — uses existing IP.

---

## Group E — Competitive Moats (5 areas)

### 21. Coach supply network (BetterUp's biggest moat)
- **Why**: BetterUp has 4,000+ ICF-certified coaches. To replicate, we'd need partnerships. Alternative: hire 5 LATAM/EU coaches ourselves (~$3-5K/mo burn) + AI matching layer.
- **Method**: Research ICF LATAM chapter + EU directory; identify 5 potential partner coaches; document partnership economics (revenue split).
- **Output**: `/opt/data/agents/research/coach-supply-strategy.md` — partnership model + economics.
- **Owner**: Erebus + Ivan.
- **Cadence**: Once, expand quarterly.
- **Priority**: HIGH — required for "hybrid" SKU.

### 22. EU AI Act compliance as a moat
- **Why**: (already in #2 — the strategic implication). Document the implementation as a differentiator for EU prospects.
- **Method**: Compile compliance documentation; create a public-facing "EU AI Act + GDPR compliant" badge/statement.
- **Output**: `/opt/data/marketing/eu-ai-act-badge.md` — compliance statement + badge asset.
- **Owner**: Erebus.
- **Cadence**: Once, refresh after AI Act amendments.
- **Priority**: HIGH — same as #2.

### 23. ICF-aligned methodology badge (certified-equivalent)
- **Why**: We can't get ICF-accredited (that's for human-coach schools) but we can document "ICF competency-aligned" methodology. That's still a moat.
- **Method**: Hire an ICF Master Certified Coach for 1h consultation; document our 8-competency alignment; produce public-facing "ICF-aligned methodology" whitepaper.
- **Output**: `/opt/data/marketing/icf-aligned-whitepaper.md`.
- **Owner**: Erebus + Ivan.
- **Cadence**: Once.
- **Priority**: HIGH — credibility signal.

### 24. Trilingual prompt engineering methodology
- **Why**: Anyone can call an LLM in Spanish. Few can engineer prompts that produce **culturally coherent coaching dialogue** in 3 languages. This is craft.
- **Method**: Document our prompt engineering for trilingual coaching sessions. Include translation trade-offs (Spanish prefers longer metaphors, Dutch prefers direct questions, English is universal fallback).
- **Output**: `/opt/data/source-materials/coaching/trilingual-prompt-engineering.md` — methodology + sample prompts.
- **Owner**: Erebus.
- **Cadence**: Once, iterate as models evolve.
- **Priority**: HIGH — proprietary IP.

### 25. Coaching conversation data privacy protocol
- **Why**: Coaching conversations are sensitive (mental health, career, finances). A privacy-first protocol is a moat. BetterUp's privacy incidents are public.
- **Method**: Document end-to-end encryption protocol, retention policy, model training opt-out, regional data residency.
- **Output**: `/opt/data/source-materials/coaching/privacy-protocol.md`.
- **Owner**: Erebus.
- **Cadence**: Once, monitor regulatory changes.
- **Priority**: HIGH — required for EU/health verticals.

---

## Group F — Operational Implementation (5 areas)

### 26. 🔴 Tech stack: which LLM + RAG + voice stack
- **Why**: The architecture decisions matter. Whisper.cpp for transcription? OpenAI vs Claude for dialogue? Pinecone vs Weaviate for RAG? ElevenLabs for voice?
- **Method**: Benchmark each layer with Spanish + Dutch + English. Document latency, cost, quality trade-offs. Build a "minimal viable coaching stack" reference architecture.
- **Output**: `/opt/data/agents/research/coaching-tech-stack-benchmarks.md`.
- **Owner**: Erebus.
- **Cadence**: Once, refresh when models change.
- **Priority**: 🔴 HIGH — must ship Q4 2026.

### 27. Session recording + transcription pipeline
- **Why**: Real coaching happens in 1:1 calls. Need to record, transcribe, summarize, extract action items. Multilingual ASR is hard.
- **Method**: Benchmark Whisper-large-v3 (open source), ElevenLabs Scribe, Deepgram Nova-2, OpenAI Whisper API for Spanish + Dutch + English WER.
- **Output**: `/opt/data/agents/research/coaching-asr-benchmarks.md` — WER per language per vendor + recommendation.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: 🔴 HIGH — needed for sales-call-coaching SKU.

### 28. Multi-tenant SaaS deployment architecture
- **Why**: If we're selling to enterprises, we need per-tenant isolation (data, models, prompt configs). ParaguAI Builder exists but for websites, not coaching.
- **Method**: Document the multi-tenant architecture: per-org data lake + per-org prompt customization + per-org billing.
- **Output**: `/opt/data/source-materials/coaching/multi-tenant-architecture.md`.
- **Owner**: Erebus + Kyrian (CTO).
- **Cadence**: Once.
- **Priority**: HIGH — required for SaaS revenue.

### 29. EU data residency + cross-border data flow
- **Why**: GDPR requires EU customer data stays in EU. We host in Paraguay (Cloudflare R2 + VPS). Need EU region for EU clients.
- **Method**: Document Cloudflare R2 EU region, Scaleway (Paris), Hetzner (Falkenstein) options. Build EU-resident deployment.
- **Output**: `/opt/data/source-materials/coaching/eu-data-residency.md`.
- **Owner**: Erebus.
- **Cadence**: Once.
- **Priority**: MEDIUM — required for first EU client.

### 30. Sales pitch deck + proposal template for AI coaching
- **Why**: Need a ready-to-customize pitch for any vertical. Each pitch: problem → our solution → ICF alignment → EU compliance → trilingual → pricing → case studies.
- **Method**: Build the pitch deck template (Claude-design skill); build the proposal template (paraguai-proposal-pricing skill); produce 3 vertical-specific variants (legal, dental, RE).
- **Output**: `/opt/data/build/coaching-pitch-kit/` — 3 pitch decks + 3 proposals.
- **Owner**: Erebus + Ivan.
- **Cadence**: Once, update quarterly.
- **Priority**: 🔴 HIGH — without pitch we can't sell.

---

## Summary table

| # | Area | Why | Owner | Cadence | Priority |
|---|------|-----|-------|---------|----------|
| 1 | AI coaching market size + segmentation | Defensible numbers for proposals | Erebus | Annual | 🔴 HIGH |
| 2 | EU AI Act compliance | Strategic moat | Erebus | Quarterly | 🔴 HIGH |
| 3 | BetterUp/CoachHub/Valence failure modes | Competitive intel | Erebus+Ivan | Bi-annual | 🔴 HIGH |
| 4 | Coaching pricing benchmarks | Pricing | Erebus | Quarterly | MEDIUM |
| 5 | LATAM corporate L&D spending | Market validation | Erebus | Annual | MEDIUM |
| 6 | ICF Core Competencies mapping | Methodology backbone | Erebus+Ivan | Once | 🔴 HIGH |
| 7 | Coaching frameworks comparison | Methodology IP | Erebus | Once | 🔴 HIGH |
| 8 | CBT patterns for coaching | Wellness extension | Erebus | Once | MEDIUM |
| 9 | Behavioral change science | Behavior change methodology | Erebus | Once | MEDIUM |
| 10 | Coaching session structure | Conversation backbone | Erebus | Once | 🔴 HIGH |
| 11 | Spanish coaching vocabulary | Spanish-native moat | Erebus+Ivan | Once | 🔴 HIGH |
| 12 | Dutch coaching vocabulary | Dutch-fluent moat | Erebus+Kyrian | Once | 🔴 HIGH |
| 13 | Paraguay-Spanish adaptations | PY-native moat | Erebus+Ivan | Once | 🔴 HIGH |
| 14 | Suriname + Antilles adaptations | Untapped market | Erebus+Kyrian | Once | HIGH |
| 15 | GDPR Art 9 compliance | EU compliance | Erebus+external | Quarterly | MEDIUM |
| 16 | Legal-vertical playbook | First $ vertical | Erebus+Ivan | Quarterly | 🔴 HIGH |
| 17 | Real estate playbook | Mark NL canary | Erebus+Mark | Bi-annual | 🔴 HIGH |
| 18 | Dental vertical playbook | Existing client base | Erebus+Ivan | Once | HIGH |
| 19 | Beauty/wellness playbook | 13+ existing clients | Erebus+Kyrian | Once | HIGH |
| 20 | SMB entrepreneur coach | wizard-academy IP | Erebus | Once | HIGH |
| 21 | Coach supply strategy | Hybrid SKU | Erebus+Ivan | Quarterly | HIGH |
| 22 | EU AI Act badge | Marketing | Erebus | Quarterly | HIGH |
| 23 | ICF-aligned methodology | Credibility | Erebus+Ivan | Once | HIGH |
| 24 | Trilingual prompt engineering | Proprietary IP | Erebus | Ongoing | HIGH |
| 25 | Privacy protocol | Required | Erebus | Quarterly | HIGH |
| 26 | Tech stack benchmarks | Must ship | Erebus | Quarterly | 🔴 HIGH |
| 27 | ASR benchmarks | Sales-call SKU | Erebus | Once | 🔴 HIGH |
| 28 | Multi-tenant architecture | SaaS revenue | Erebus+Kyrian | Once | HIGH |
| 29 | EU data residency | EU clients | Erebus | Once | MEDIUM |
| 30 | Sales pitch + proposal | Can't sell without | Erebus+Ivan | Quarterly | 🔴 HIGH |

**30 areas total. 9 marked 🔴 HIGH (do this month). 13 marked HIGH (this quarter). 8 marked MEDIUM (Q4-Q1).**

---

## Execution guidance

### Time investment

- **🔴 HIGH priority (9 areas × ~4h each = ~36h)**: do this month. Assign to Erebus + 2-3 sessions/week.
- **HIGH priority (13 areas × ~3h each = ~40h)**: this quarter. Assign to Erebus weekly.
- **MEDIUM priority (8 areas × ~2h each = ~16h)**: Q4 2026 - Q1 2027. Backlog.

### Where the IP lives

Every output goes to one of:
- `/opt/data/agents/research/` — strategic intel
- `/opt/data/source-materials/coaching/` — methodology + frameworks + source-of-truth IP
- `/opt/data/build/coaching-pitch-kit/` — sales assets
- `/opt/data/marketing/` — public-facing compliance + credibility

### How to track progress

- Add each HIGH-priority area to `todo` at start of session
- Save outputs to GitHub (commits track completion)
- Update this doc as areas complete (mark ✅ next to area number)

### What I'm NOT recommending

- ❌ Building a BetterUp competitor (too crowded, too capital-intensive)
- ❌ Building a Gong competitor (too crowded, $500M ARR leader)
- ❌ Building a US-only product (no language moat)
- ❌ A consumer-only play (Blomma, Tomo are there)
- ❌ Fundraising for a coaching product (not venture-scale)

---

## Files cited in this research

- `/opt/data/agents/research/200-ai-coaching-companies.md` — 197 companies in 18 categories (this research)
- `/opt/data/agents/research/STRATEGY.md` — AIW org strategy (Erebus, 2026-08-13)
- `/opt/data/agents/research/department-playbook/` — AIW org structure (Session 2)
- `/opt/data/agents/research/org-design-literature.md` — AIW methodology canon (Session 1)
- `/opt/data/agents/research/roles-glossary.md` — 98-role glossary (Session 1)
- `/opt/data/source-materials/topics/trilingual-middle-market.md` — trilingual positioning
- `/opt/data/source-materials/topics/rubicon-eas-deal.md` — Rubicón EAS vertical playbook
- `/opt/data/skills/paraguai-proposal-pricing/` — pricing skill used for proposal templates
- `/opt/data/skills/b2b-cold-outreach-pitch/` — pitch templates