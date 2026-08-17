# Skills Audit — AI Coaching Practice

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS. Companion to `200-ai-coaching-companies.md` + `30-coaching-research-areas.md`.
> **What we have** (audit of 58 installed skills) → **what we need** (skill recommendations for AI coaching practice) → **prioritized build plan**.

## Reading guide

1. **Section 1: Inventory of installed skills** — what's already in `/opt/data/skills/` that maps to coaching
2. **Section 2: Gap analysis** — what's missing for the coaching practice
3. **Section 3: New skills to build** — 11 prioritized skill specs
4. **Section 4: Methodology IP** — what should live in `/opt/data/source-materials/coaching/`
5. **Section 5: 90-day build plan** — concrete delivery sequence

---

## Section 1: Inventory of installed skills

We have **58 skills installed**. Of these, **8 are directly relevant** to an AI coaching practice, **6 are partially relevant**, and **44 are infrastructure** (not coaching-specific).

### Directly relevant (8 skills)

| Skill | Path | What it covers | Coaching relevance |
|-------|------|----------------|--------------------|
| `b2b-cold-outreach-pitch` | `/opt/data/skills/b2b-cold-outreach-pitch/` | Multi-format B2B pitch kits (10 variations) | **CRITICAL** — pitching coaching product to verticals |
| `paraguai-proposal-pricing` | `/opt/data/skills/paraguai-proposal-pricing/` | 3-tier proposal + Gs. pricing + exclusions | **CRITICAL** — coaching-as-a-service pricing |
| `client-site-kickoff` | `/opt/data/skills/client-site-kickoff/` | 200-question intake + sample site for greenfield clients | **HIGH** — coaching client intake is similar pattern |
| `client-site-build-workflow` | `/opt/data/skills/client-site-build-workflow/` | Site build workflow | **MEDIUM** — coaching platform is a kind of site |
| `client-site-deploy` | `/opt/data/skills/client-site-deploy/` | Deploy to *.paragu-ai.com via Worker | **MEDIUM** — hosting coaching SaaS |
| `client-vps-provisioning` | `/opt/data/skills/client-vps-provisioning/` | VPS provisioning end-to-end | **MEDIUM** — EU data residency |
| `prospect-dossier-pii-sanitization` | `/opt/data/skills/prospect-dossier-pii-sanitization/` | Scrub PII from prospect docs | **HIGH** — coaching conversations are sensitive PII |
| `trademark-compliance-scrub` | `/opt/data/skills/trademark-compliance-scrub/` | Hostinger incident protection | **LOW** — apply to coaching product names |

### Partially relevant (6 skills)

| Skill | What it covers | Coaching relevance |
|-------|----------------|--------------------|
| `org-repo-audit` | Audit org repos via REST + liveness | Adapt for **coaching platform audit** |
| `live-site-triage` | Triage broken live sites end-to-end | Adapt for **coaching agent debugging** |
| `supabase-2026-secret-proxy` | Edge proxy for narrower publishable key | Adapt for **coaching data security** |
| `hermes-sandbox-blocked-payload-workaround` | Sandbox recovery | Apply during prompt-engineering experiments |
| `aiw-git-safety` | Git safety discipline | Apply to coaching platform repo |
| `aiw-ops-discipline` | Completion + validation discipline | Apply to coaching product delivery |

### Indirect (44 skills)

The remaining 44 are infrastructure (Hermes, GitHub, MCP, devops, creative, research, etc.) that **already serve the coaching practice as utilities** — we don't need new skills for them.

---

## Section 2: Gap analysis

### What's missing for an AI coaching practice

Group by capability. I've identified **11 skill gaps** + **8 source-material artifacts**.

#### Gap A — Sales & pricing (currently partial)

- ❌ **Coaching-specific pricing model** — `paraguai-proposal-pricing` covers B2B sites; coaching has per-seat-pricing + hybrid coach-network economics
- ❌ **Coaching pitch deck template** — `b2b-cold-outreach-pitch` is text-first; coaching needs visual decks per vertical
- ❌ **Vertical-specific coaching playbooks** — no template for "how to sell coaching to legal/dental/RE"
- ❌ **Coach-network partner onboarding** — BetterUp's biggest moat is coach supply; we need partner onboarding flow

#### Gap B — Methodology & IP (currently none)

- ❌ **Coaching conversation framework** — the GROW/CLEAR/OSKAR methodology prompt library
- ❌ **ICF competency mapping** — 8 competencies → AI prompt patterns (this is the methodology backbone)
- ❌ **Trilingual coaching glossary** — Spanish + Dutch + English coaching terms with cultural notes
- ❌ **CBT-in-coaching patterns** — for the bridge to mental wellness
- ❌ **Behavioral change nudges** — Prochaska + BJ Fogg patterns

#### Gap C — Privacy & compliance (currently partial)

- ❌ **EU AI Act + GDPR Article 9 protocol for coaching AI** — specific to this market
- ❌ **Coaching conversation data retention** — voice + transcript + emotion data has different retention than text
- ❌ **Cross-border data flow** — PY → EU → US transfers (Schrems II)

#### Gap D — Technical (currently partial)

- ❌ **Tech stack decision** — which LLM (Claude vs GPT vs open-source) + which RAG + which voice
- ❌ **Multilingual ASR benchmark** — Whisper vs ElevenLabs vs Deepgram for ES + NL + EN
- ❌ **Real-time call coaching pipeline** — turn-taking, latency, prompt caching for live sales calls
- ❌ **Multi-tenant coaching platform architecture** — extending ParaguAI Builder to coaching

#### Gap E — Vertical playbooks (currently none)

- ❌ **Legal coaching playbook** (Rubicón EAS-flavored)
- ❌ **Real estate coaching playbook** (Mark NL-flavored)
- ❌ **Dental coaching playbook** (ometzdental-flavored)
- ❌ **Beauty/wellness coaching playbook** (ParaguAI Builder-flavored)
- ❌ **SMB entrepreneur coaching playbook** (wizard-academy-flavored)

#### Gap F — Operations (currently none)

- ❌ **Coach session scheduling + billing** — Calendly + Stripe workflow for coaching products
- ❌ **Coaching agent debugging** — when an AI coaching session goes wrong, how to triage
- ❌ **Coach-to-AI handoff** — when AI hands off to human coach

---

## Section 3: New skills to build (11 prioritized specs)

Each spec follows the AI Whisperers skill format (see `paraguai-proposal-pricing/SKILL.md` for the canonical example). I recommend **Tier 1 = 4 skills this month**, **Tier 2 = 5 skills this quarter**, **Tier 3 = 2 skills Q4**.

### Tier 1 — Ship this month (4 skills)

#### Skill 1: `coaching-pricing` — coaching-specific pricing model
- **Path**: `/opt/data/skills/coaching-pricing/`
- **Purpose**: Per-seat + per-tenant pricing for AI coaching products. Builds on `paraguai-proposal-pricing` but with coaching-specific tiers.
- **Tiers**:
  - **A · Coach Lite**: $500 setup + $200/mo per seat (5 seats min). AI coach, English/Spanish only, async.
  - **B · Coach Pro**: $2K setup + $500/mo per seat (10 seats min). + Trilingual (es/en/nl), live call coaching, hybrid human escalation.
  - **C · Coach Enterprise**: $10K setup + $1.5K/mo per seat (50 seats min). + EU AI Act compliance, custom methodology, dedicated coach partner.
- **References**: `references/betterup-pricing.md`, `references/coachhub-pricing.md`, `references/valence-pricing.md`, `references/gong-pricing.md`
- **Templates**: `templates/coaching-proposal-es.md`, `templates/coaching-proposal-en.md`, `templates/coaching-proposal-nl.md`
- **Owner**: Erebus + Ivan (validation)
- **Time**: 4h to ship

#### Skill 2: `coaching-pitch-kit` — coaching-specific pitch kit
- **Path**: `/opt/data/skills/coaching-pitch-kit/`
- **Purpose**: Multi-format pitch kit specifically for AI coaching products. Builds on `b2b-cold-outreach-pitch` but with coaching-specific framings.
- **10 pitch variations**: cold DM, intro call, 1-pager, deck, vertical case study, demo script, ROI calculator, security/compliance doc, partnership pitch, re-engagement
- **References**: `references/icf-positioning.md`, `references/eu-ai-act-badge.md`, `references/trilingual-value-prop.md`
- **Templates**: `templates/deck-legal.md`, `templates/deck-dental.md`, `templates/deck-real-estate.md`
- **Owner**: Erebus + Ivan
- **Time**: 4h to ship

#### Skill 3: `coaching-conversation-framework` — the GROW + CLEAR hybrid prompt library
- **Path**: `/opt/data/skills/coaching-conversation-framework/`
- **Purpose**: The IP of the coaching product. Every AI coaching session follows this framework.
- **Anatomy**:
  - Opening check-in (5 questions, trilingual)
  - Goal setting (SMART, in user's language)
  - Reality check (GROW's "R" — explore current state)
  - Options exploration ("O" — generate 3+ paths)
  - Will / action ("W" — concrete next steps)
  - Accountability close (CLEAR's "A" — schedule follow-up)
- **References**: `references/grow-model.md`, `references/clear-model.md`, `references/icf-competencies-mapping.md`
- **Templates**: 30 prompt templates per stage in 3 languages = 90 prompts total
- **Owner**: Erebus
- **Time**: 6h to ship

#### Skill 4: `coaching-trilingual-glossary` — Spanish/Dutch/English coaching vocabulary
- **Path**: `/opt/data/skills/coaching-trilingual-glossary/`
- **Purpose**: The trilingual edge in IP form. 300+ terms per language with cultural notes.
- **Categories**: coaching verbs (question, reflect, challenge, support), emotional states, business contexts, regional variations (PY-Spanish vs MX-Spanish, NL-Netherlands vs NL-Belgium vs NL-Suriname)
- **References**: `references/coaching-vocabulary-es.md`, `references/coaching-vocabulary-nl.md`, `references/coaching-vocabulary-en.md`
- **Templates**: `templates/trilingual-prompt-translation.md` — how to translate a coaching prompt without losing meaning
- **Owner**: Erebus + Ivan (ES) + Kyrian (NL)
- **Time**: 6h to ship

### Tier 2 — Ship this quarter (5 skills)

#### Skill 5: `coaching-eu-compliance` — EU AI Act + GDPR Article 9 protocol
- **Path**: `/opt/data/skills/coaching-eu-compliance/`
- **Purpose**: The compliance moat. EU AI Act + GDPR compliance documentation for coaching AI.
- **Includes**: data minimization, opt-in flow, model training opt-out, regional data residency, breach notification, AI Act risk classification, GDPR Art 9 protocol for sensitive categories
- **References**: EU AI Act articles, EDPB guidance, Schrems II decision
- **Owner**: Erebus + external counsel
- **Time**: 8h to ship

#### Skill 6: `coaching-tech-stack` — production stack reference architecture
- **Path**: `/opt/data/skills/coaching-tech-stack/`
- **Purpose**: The architecture decisions. Which LLM, which RAG, which ASR, which voice, which multi-tenant layer.
- **Benchmarks**: Claude Sonnet 4 vs GPT-4o vs open-source for trilingual coaching quality; Whisper-large-v3 vs Deepgram vs ElevenLabs Scribe for ES+NL+EN WER; Pinecone vs Weaviate for RAG; ElevenLabs vs Cartesia vs PlayHT for voice
- **Reference architecture**: Cloudflare Workers + R2 (EU region) + Claude API + Whisper-large-v3 + ElevenLabs + ParaguAI Builder (multi-tenant)
- **Owner**: Erebus + Kyrian (CTO)
- **Time**: 8h to ship

#### Skill 7: `coaching-vertical-playbook` — legal/RE/dental/beauty/SMB playbook
- **Path**: `/opt/data/skills/coaching-vertical-playbook/`
- **Purpose**: Per-vertical playbook for selling coaching. Each vertical: ICP, common objections, proof points, pricing tier, sample conversation.
- **5 vertical playbooks**: legal, real estate, dental, beauty/wellness, SMB entrepreneur
- **Owner**: Erebus + Ivan
- **Time**: 10h to ship

#### Skill 8: `coaching-coach-network` — partner coach onboarding
- **Path**: `/opt/data/skills/coaching-coach-network/`
- **Purpose**: Onboard + manage partner coaches for the hybrid SKU. Recruitment, ICF credential verification, payout model, AI-augmentation training.
- **Includes**: partner coach application form, ICF verification protocol, revenue split (60/40 base + AI multiplier), AI tool training (2h video), performance review (quarterly)
- **Owner**: Erebus + Ivan
- **Time**: 6h to ship

#### Skill 9: `coaching-privacy-protocol` — coaching conversation data protocol
- **Path**: `/opt/data/skills/coaching-privacy-protocol/`
- **Purpose**: Privacy-first protocol for coaching conversation data. End-to-end encryption, retention policy, model training opt-out, breach notification.
- **Owner**: Erebus
- **Time**: 4h to ship

### Tier 3 — Ship Q4 2026 (2 skills)

#### Skill 10: `coaching-agent-debugging` — when AI coaching sessions go wrong
- **Path**: `/opt/data/skills/coaching-agent-debugging/`
- **Purpose**: Triage protocol for AI coaching sessions that fail (ethical issues, off-topic, hallucinated advice, emotional escalation). Adapts `live-site-triage` pattern.
- **Owner**: Erebus + Kyrian
- **Time**: 6h to ship

#### Skill 11: `coaching-roi-measurement` — measure AI coaching impact for clients
- **Path**: `/opt/data/skills/coaching-roi-measurement/`
- **Purpose**: ROI framework for AI coaching — adoption, behavior change, business outcomes. Based on Careertrainer.ai 2026 stats: ROI within 8 months on average, 91% integrate analytics, 64% report productivity gains.
- **Owner**: Erebus + Ivan
- **Time**: 8h to ship

---

## Section 4: Methodology IP — what should live in `/opt/data/source-materials/coaching/`

These are not skills (they're not actionable procedures) — they're **provenance + canonical sources**. Save in `/opt/data/source-materials/coaching/`.

| File | Why | Source |
|------|-----|--------|
| `icf-core-competencies.md` | The 8 ICF competencies for our methodology backbone | ICF public PDF |
| `grow-model.md` | Sir John Whitmore's GROW coaching model | Whitmore's book (public summary) |
| `clear-model.md` | Peter Hawkins' CLEAR model | Hawkins' book (public summary) |
| `oskar-model.md` | Mark McKergow's OSKAR model | McKergow's book (public summary) |
| `prochaska-stages-of-change.md` | Transtheoretical Model | Prochaska & DiClemente |
| `bj-fogg-tiny-habits.md` | Behavior change methodology | Fogg's book |
| `spanish-coaching-vocabulary.md` | Spanish coaching terms + LATAM adaptations | Compiled from 3 sources |
| `dutch-coaching-vocabulary.md` | Dutch coaching terms + business culture | Compiled from 3 sources |
| `paraguay-spanish-coaching.md` | PY-specific coaching patterns | Ivan's interview + cultural research |
| `suriname-antilles-coaching.md` | Surinamese + Antillean Dutch patterns | Kyrian's research |
| `eu-ai-act-coaching-classification.md` | How EU AI Act classifies AI coaching | Artificialintelligenceact.eu + EDPB |
| `gdpr-art-9-coaching.md` | Special-category data protocol | EDPB guidance |
| `betterup-business-model.md` | Why BetterUp works (and doesn't) | Public info + G2 reviews |
| `coachhub-business-model.md` | Why CoachHub works (and doesn't) | Public info + G2 reviews |
| `valence-nadia-methodology.md` | Valence Nadia's agentic coaching architecture | Public docs + Bessemer case study |
| `yoodli-roleplay-architecture.md` | Yoodli's roleplay tech | Yoodli blog + engineering talks |
| `gong-conversation-intelligence.md` | Gong's CI architecture | Gong blog |
| `second-nature-ai-roleplay.md` | Second Nature's roleplay tech | StartupHub.ai |
| `careertrainer-stats-2026.md` | Market sizing + adoption stats | Careertrainer.ai Feb 2026 report |
| `gitnux-ai-coaching-stats-2026.md` | More market stats | Gitnux Feb 2026 report |

---

## Section 5: 90-day build plan

### Week 1 (now)

- [ ] Read `/opt/data/agents/research/200-ai-coaching-companies.md` and `30-coaching-research-areas.md`
- [ ] Sign Rubicón EAS contract (the immediate revenue path)
- [ ] Wire Rubicón EAS Worker webhook (`wrangler secret put WEBHOOK_URL`)
- [ ] Create `/opt/data/source-materials/coaching/` directory
- [ ] Save ICF Core Competencies PDF (free, public)
- [ ] Save GROW + CLEAR + OSKAR public summaries
- [ ] Hire ICF Master Certified Coach for 1h consult ($200)

### Week 2 (Tier 1 starts)

- [ ] Build `coaching-pricing` skill (4h)
- [ ] Build `coaching-pitch-kit` skill (4h)
- [ ] Build 3 vertical-specific pitch decks (legal, dental, RE) using `claude-design` skill
- [ ] Write `careertrainer-stats-2026.md` + `gitnux-ai-coaching-stats-2026.md` in source-materials
- [ ] First NL-targeted outreach using new pitch kit

### Week 3-4 (Tier 1 continues)

- [ ] Build `coaching-conversation-framework` skill (6h) — the IP core
- [ ] Build `coaching-trilingual-glossary` skill (6h) — the trilingual moat
- [ ] Test the conversation framework in Spanish + Dutch with 3 mock coaching sessions
- [ ] Update `company/Company/services/README.md` to add "AI Coaching" service line

### Month 2 (Tier 2 starts)

- [ ] Build `coaching-eu-compliance` skill (8h) — the EU moat
- [ ] Build `coaching-tech-stack` skill (8h) — architecture decisions
- [ ] Wire Rubicón EAS into a coaching agent prototype (using conversation framework + tech stack)
- [ ] Reach out to 5 LATAM ICF coaches for partner network

### Month 3 (Tier 2 continues + first $)

- [ ] Build `coaching-vertical-playbook` skill (10h) — 5 verticals
- [ ] Build `coaching-coach-network` skill (6h) — partner network
- [ ] Build `coaching-privacy-protocol` skill (4h)
- [ ] First Rubicón EAS coaching session shipped
- [ ] First Mark NL coaching session shipped
- [ ] First case study written (Rubicón EAS)

### Q4 2026 (Tier 3)

- [ ] Build `coaching-agent-debugging` skill
- [ ] Build `coaching-roi-measurement` skill
- [ ] Sign 2nd Rubicón-style legal client
- [ ] Sign 1st NL coaching client (Mark NL closes)
- [ ] Sign 1st LATAM SMB coaching client

---

## The single recommendation

**Build `coaching-conversation-framework` first.** It's the IP backbone of every coaching product we ship. Without it, we have a SaaS sales tool. With it, we have a coaching product.

Then build `coaching-pricing` + `coaching-pitch-kit` so we can sell the thing.

Then build `coaching-trilingual-glossary` so the trilingual edge is documented.

Then everything else in 90 days.

---

## Files cited in this audit

- `/opt/data/skills/` (all 58 installed skills inventoried)
- `/opt/data/agents/research/200-ai-coaching-companies.md` — the 197-company landscape
- `/opt/data/agents/research/30-coaching-research-areas.md` — the 30-area research agenda
- `/opt/data/agents/research/STRATEGY.md` — AIW strategy doc
- `/opt/data/repos/Ai-Whisperers/mark-nl-vastgoed-coaching/` — the trigger for this audit
- `/opt/data/skills/paraguai-proposal-pricing/SKILL.md` — the skill format template
- `/opt/data/skills/b2b-cold-outreach-pitch/SKILL.md` — the pitch format template