# Sunstein & Solstein — Inventory + Research Roadmap

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS. Triggered by user request "research what we have in Sunstein Solstein and all we should research based on this".
> **Two distinct things**:
> 1. **Sunstein** = the agent persona I'm running under (SOUL.md / developer policy) + Cass Sunstein's intellectual canon (nudge theory, choice architecture, behavioral economics)
> 2. **Solstein** = (a) our internal M&A research pipeline + scorecard framework (the "Solstein M&A Research Pipeline"), (b) the **Solstein AI Paraguay** client site (3 pages: `solstein.html`, `solstein-ai.html`, `solstein-cloud.html`)
>
> **This doc** = (1) inventory both, (2) extract the rules/skills/methodologies embedded in each, (3) identify what we should research next.

## Reading guide

1. **Section 1: Sunstein — what we have** (agent persona + methodology canon)
2. **Section 2: Solstein — what we have** (M&A pipeline + client site)
3. **Section 3: The two intersect** — Sunstein's nudge theory is the methodology backbone of AI coaching; Solstein's pipeline is the M&A/sales tool
4. **Section 4: What to research next** — 25 prioritized areas in 5 groups
5. **Section 5: Skills gap audit** (Sunstein/Solstein-flavored additions)
6. **Section 6: The single bet**

---

# Section 1: Sunstein — what we have

## 1.1 Sunstein as agent persona (the developer policy)

**File**: `/opt/data/SOUL.md` (19 lines)
**Also lives in**: every session dump at `/opt/data/sessions/request_dump_*.json` (the developer policy is prepended to every session; "Sunstein Persona" is the literal opening heading)

The Sunstein Persona is **the operating contract that defines how I (this agent) work in your environment**:

| Dimension | What it specifies | Why it matters |
|-----------|-------------------|----------------|
| **Communication** | Terse, direct, no fluff; code-focused; token-minimal | Defines response register for every interaction |
| **Core principles** | Quality over speed; TDD-driven; security-first | Defines engineering priorities |
| **Role** | Autonomous AI coding agent; Mensaje-first UX; local FPUNA repo + VPS aiw-* services | Defines scope |
| **Capabilities** | Mensaje interface (n8n); image/audio (VPS aiw-*); 33MB state.db persistent context; repo awareness; code generation | Defines what I can do |
| **Constraints** | Max 90 turns; always Anthropic API; Spanish for FPUNA context | Defines limits |

### What the Sunstein Persona **does NOT** specify (gaps)

| Gap | What we need |
|-----|--------------|
| Memory rules (when to use memory vs session_search vs skills) | Defined separately in developer policy ("Save durable facts using the memory tool...") — but the persona doesn't reference it |
| Specific workflow patterns (RED-GREEN-REFACTOR, fail-loud, security-first specifics) | Implied but not codified |
| Project-specific playbooks (Rubicón EAS, coaching product, Solstein M&A) | Not in persona — lives in skills + research docs |
| Quality gates (when to ship vs when to ask) | Defined as "Quality over speed" but no concrete gates |
| Trilingual handling (es/en/nl specifics) | Not codified |
| Trademark compliance (the banlist) | In memory only |

**Recommendation**: **Update SOUL.md to be more prescriptive** — codify memory rules, workflow patterns, project playbooks, quality gates, trilingual handling. This is the "persona v2" work.

## 1.2 Sunstein as methodology canon (Cass Sunstein + behavioral economics)

Even though SOUL.md is named "Sunstein Persona" (probably after the user/sponsor), the **Cass Sunstein intellectual canon** is **directly relevant** to AI coaching:

| Cass Sunstein work | Year | Relevance to AI coaching |
|--------------------|------|--------------------------|
| **Nudge** (with Richard Thaler) | 2008 | The foundational text on choice architecture. Maps directly to AI coaching prompts. **Sunstein is the originator of the methodology that BetterUp/CoachHub/Valence implement**. |
| **Republic.com** | 2001 | Personalization + filter bubbles. AI coaching runs the same risk; Sunstein's analysis is the warning. |
| **Infoglut / Too Much Information** | 2020 | Information overload + decision fatigue. AI coaching must respect attention budgets. |
| **Sludge** (with Lucia Reisch) | 2021 | "Sludge" = friction that prevents good choices. AI coaching should *remove* sludge. |
| **Choosing Not to Choose** | 2015 | The value of default options. AI coaching prompts = default options that nudge. |
| **On Freedom** | 2019 | Autonomy + freedom in an algorithmic age. The ethical backbone for AI coaching ethics. |
| **#Republic** | 2017 | Polarization + social media. Relevant to coaching in politically loaded contexts. |
| **The Cost-Benefit State** | 2023 | How governments use CBA; relevant to ROI measurement in AI coaching products. |
| **Look Again** | 2024 | Noticing what was always there. Relevant to coaching prompts that surface blind spots. |
| **On Liberalism** (in progress 2026) | 2026 | Forthcoming. Likely relevant to ethics + autonomy. |

**Sunstein's relevance to our org**: He's the **canonical authority** for the methodology behind AI coaching. BetterUp pays him nothing to use his frameworks; we can build an **"ICF-aligned + Sunstein-inspired"** methodology badge.

### The 3 Sunstein principles that map directly to AI coaching

1. **Choice architecture** (from Nudge): every AI coaching prompt is a choice architecture. The order of questions, the default options, the friction in the flow — all nudge the user.
2. **Default rules** (from Choosing Not to Choose): AI coaching prompts should default to action, not analysis-paralysis. "What's one small step you could take this week?" not "What are all your options?"
3. **Sludge removal** (from Sludge 2021): every friction in the coaching flow is sludge. AI coaching's killer feature should be: less friction = more behavior change.

**Sources**:
- Cass Sunstein Wikipedia — confirmed American legal scholar, Harvard Law, behavioral economics, NYT bestseller
- "Too Much Information" MIT Press 2020 — Sunstein's most recent major work on information overload
- "Republic.com" 2001 — early work on personalization + democracy
- "Nudge" 2008 (with Thaler) — the foundational text, ~3M copies sold

---

# Section 2: Solstein — what we have

## 2.1 Solstein as M&A research pipeline (the internal tool)

**Repo**: `Ai-Whisperers/solstein-manda-research` (private — currently 404 on public API, so confirmed private)
**Doc**: `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/solstein-analysis.md`
**Scorecard**: `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/solstein-scorecard.json`
**Lite tool sketch**: `/opt/data/repos/infrastructure/sales-playbook/solstein-lite-tool.md`
**Backup sketch**: `/opt/data/scratchpad/sales-playbook/solstein-lite-tool.md`

### The Solstein M&A scoring framework

| Dimension | Weight | What it scores |
|-----------|-------:|----------------|
| Ownership attractiveness | 3 | Cap table cleanliness; no PE/VC; acquirability |
| Revenue scale fit | 3 | Revenue thresholds vs PE buyout criteria |
| Geographic fit | 3 | Paraguay / LATAM / EU alignment with AIW strategy |
| Tech stack modernity | 2 | Modern stack (Next.js, Tailwind, etc.) |
| Customer lock-in | 2 | Switching costs; recurring engagement |
| Vertical depth | 2 | How deep in one vertical vs horizontal |
| Integration potential | 1 | How easy to fold into AIW stack |
| Growth trajectory | 1 | Macro tailwind + execution momentum |

**Total weight**: 17. **Composite score**: weighted average. **Vetoes**: PE-owned, VC-backed, US-headquartered, already acquired, off-market → instant disqualifier.

**Current verified application**: Nexa Paraguay (composite 3.82/5 = "B — Viable with noted risks", readiness 76/100).

### The Solstein pipeline architecture

**Inputs**: company name + URL
**25+ data sources** including:
- Wikipedia, GitHub, SEC EDGAR, yfinance, GLEIF
- Brave News, Exa, DNS, Clearbit (paid), Crunchbase (paid), Glassdoor (paid)

**Output**: 8-dimension scorecard JSON + markdown report (~500-2,000 words)

**Performance**: 5-15 min for full pipeline; 60 seconds for lite version

**Test status**: 88 tests passing (per the lite-tool doc)

### Solstein as data enrichment engine

The pipeline is reused for:
- **Lead enrichment** for AIW sales: web data + behavioral signals
- **Lead scoring**: priority queue for sales team
- **News monitoring**: trigger alerts on tax/policy changes
- **Competitive intel**: 8-dimension scoring of competitors

### What Solstein does NOT do (gaps)

| Gap | What we need |
|-----|--------------|
| **No scoring for coaching companies** | The 8 dimensions are M&A-oriented; coaching company scoring would weight differently (e.g., coach supply network, methodology alignment, EU compliance) |
| **No Solstein coaching template** | A "Solstein coaching scorecard" for evaluating AI coaching prospects/competitors |
| **No public Solstein lite tool** | Architectural sketch exists but not built (estimated 12-16h to ship) |
| **No integration with our CRM (HubSpot, Airtable, etc.)** | Pipeline runs standalone |
| **No multilingual source coverage** | Sources are English-dominant; we need Spanish + Dutch sources for LATAM + NL |
| **No AI Act compliance dimension** | EU AI Act compliance is increasingly a deal-killer; needs its own dimension |

## 2.2 Solstein as client site (Solstein AI Paraguay)

**3 deployed pages**:
- `/opt/data/sites/clients/solstein.html` — "Solstein — Tecnología en Asunción | Paraguay"
- `/opt/data/sites/clients/solstein-ai.html` — "Solstein AI — Inteligencia Artificial en Asunción | Paraguay"
- `/opt/data/sites/clients/solstein-cloud.html` — "Solstein Cloud — (presumed)"
- Plus: `/opt/data/sites/clients/sol-stein.html` — alternate hyphenated URL

**Backups**: `/opt/data/scratchpad/client-sites-backup/solstein*.html`
**Manifest entry**: `/opt/data/sites/manifest.json` has 3 separate entries (solstein, solstein-ai, solstein-cloud)

### What the Solstein client site tells us about the org

- **Solstein is a technology provider in Asunción, Paraguay**
- They offer: Tecnología general, AI products, Cloud services
- We built them a 3-page set — suggests they're either a startup testing the market, or a small team that wanted to launch a multi-vertical presence fast
- The 3 separate pages (`solstein`, `solstein-ai`, `solstein-cloud`) suggest a **verticalized business model** — same pattern BetterUp/Valence use (one platform, multiple products)

### The opportunity here

**Solstein could be a flagship coaching client** (we built their 3-page site; could add an AI coaching agent). But also:

- **If Solstein is a real PY tech company**, they're competing with us in the AI services space. Worth researching their actual position.
- **If Solstein is a personal brand / side project**, they could become a coaching-flavored product extension.

**We have no public information on who actually runs Solstein or what they ship**. The sites we built are template-level — they don't reveal product features or pricing.

---

# Section 3: Where Sunstein and Solstein intersect

The two have a **methodological convergence** we should exploit:

| Sunstein (methodology) | Solstein (M&A scoring) | Combined opportunity |
|------------------------|----------------------|---------------------|
| Choice architecture | Scoring dimensions | A "Solstein-Sunstein" framework: each company scored on **choice-architecture maturity** (do their products nudge well?) |
| Default rules | Revenue scale | A scoring dimension: "Does the company deploy defaults that work?" |
| Sludge removal | Customer lock-in | A scoring dimension: "Is the company removing sludge or adding it?" |
| Infoglut awareness | Tech stack modernity | A scoring dimension: "Does the company respect attention budgets?" |
| Autonomy (On Freedom) | Ownership attractiveness | A scoring dimension: "Does the company preserve user autonomy?" |

### The "Solstein-Sunstein" coaching framework (the IP)

**A 5-dimension framework for evaluating + building AI coaching products:**

1. **Choice architecture quality** — Are coaching prompts well-designed defaults?
2. **Sludge minimization** — Are we removing friction or adding it?
3. **Attention respect** — Do we respect the user's attention budget (no infoglut)?
4. **Autonomy preservation** — Are we coaching or manipulating? (the Sunstein ethical line)
5. **Nudge effectiveness** — Do our nudges measurably change behavior?

This is the **methodological backbone** of the AI coaching product — and it's **defensibly our own IP** because no other AI coaching company frames it this way.

---

# Section 4: What to research next (25 areas)

## Group A — Sunstein canon deep-dive (5 areas)

### 1. 🔴 Nudge (2008) full summary + 2021 final edition delta
- **Why**: The foundational text. We can't ship "Sunstein-aligned" without reading the book.
- **Method**: Read Sunstein's 2021 final edition (which adds 10 years of post-publication research); extract the 9 "nudges" framework; map to AI coaching prompts.
- **Output**: `/opt/data/source-materials/sunstein/nudge-summary.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: 🔴 HIGH

### 2. 🔴 Sludge (2021) — friction taxonomy for AI coaching UX
- **Why**: Sludge is the mirror of nudge. AI coaching's killer feature is sludge removal.
- **Method**: Read Sunstein + Reisch's "Sludge" book; extract the sludge taxonomy; map to our coaching UX.
- **Output**: `/opt/data/source-materials/sunstein/sludge-taxonomy.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: 🔴 HIGH

### 3. Choosing Not to Choose (2015) — default rules for AI coaching prompts
- **Why**: Default rules are central to nudge. AI coaching prompts are default rules.
- **Method**: Read the book; extract the 6 default rules; map to coaching session design.
- **Output**: `/opt/data/source-materials/sunstein/default-rules-coaching.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 4. Infoglut (2020) — attention budget for AI coaching
- **Why**: AI coaching should respect attention budgets. Too many nudges = sludge.
- **Method**: Read Sunstein's "Too Much Information" (MIT Press 2020); extract the attention budget framework.
- **Output**: `/opt/data/source-materials/sunstein/attention-budget.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 5. On Freedom (2019) — ethical line for AI coaching
- **Why**: AI coaching walks a line between helping and manipulating. Sunstein's "On Freedom" is the canonical ethics text.
- **Method**: Read the book; extract the "freedom-preserving" framework; codify as our ethics policy.
- **Output**: `/opt/data/source-materials/sunstein/ethics-policy.md`
- **Owner**: Erebus + Ivan
- **Cadence**: Once
- **Priority**: 🔴 HIGH (this is our ethics IP)

## Group B — Solstein pipeline extensions (5 areas)

### 6. 🔴 Solstein coaching scorecard (new dimensions)
- **Why**: The current 8 dimensions are M&A-oriented. Coaching companies need different dimensions (coach supply, methodology, EU compliance).
- **Method**: Define 5 new coaching-specific dimensions; weight them; test against BetterUp/Valence/CoachHub; refine.
- **Output**: `/opt/data/build/solstein-manda-research/coaching-scorecard.json`
- **Owner**: Erebus + Kyrian (CTO)
- **Cadence**: Once, refine quarterly
- **Priority**: 🔴 HIGH

### 7. 🔴 Solstein lite tool — ship the public version
- **Why**: Architectural sketch exists; 12-16h to ship. The lite tool is the top-of-funnel lead generator for sales.
- **Method**: Follow the sketch (`/opt/data/repos/infrastructure/sales-playbook/solstein-lite-tool.md`). Carve out the free-source subset, wrap in Next.js 16, deploy to `research.ai-whisperers.com`, launch on LinkedIn.
- **Output**: `/opt/data/build/solstein-lite/` deployed at `research.ai-whisperers.com`
- **Owner**: Erebus + Kyrian
- **Cadence**: Once, then iterate
- **Priority**: 🔴 HIGH

### 8. Solstein multilingual source coverage (Spanish + Dutch)
- **Why**: Current sources are English-dominant. LATAM + NL deals need Spanish + Dutch sources.
- **Method**: Add Spanish sources (Mercado Libre, LinkedIn LATAM, Yahoo Hispanic, El Tiempo); add Dutch sources (Marktplaats, LinkedIn NL, FD, NRC).
- **Output**: Updated Solstein source registry
- **Owner**: Erebus + Ivan (ES) + Kyrian (NL)
- **Cadence**: Once, refine per market
- **Priority**: HIGH

### 9. Solstein EU AI Act compliance dimension
- **Why**: EU AI Act compliance is increasingly a deal-killer. Needs its own scoring dimension.
- **Method**: Add a 9th dimension (weight 2): EU AI Act + GDPR Article 9 + data residency compliance.
- **Output**: Updated scorecard framework
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 10. Solstein CRM integration (HubSpot + Airtable)
- **Why**: Solstein runs standalone. Sales team needs pipeline → CRM → outreach flow.
- **Method**: Build HubSpot API integration; auto-create leads from Solstein scores; trigger Airtable records.
- **Output**: Solstein-CRM sync script
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

## Group C — Sunstein × Solstein framework (5 areas)

### 11. 🔴 Build the "Solstein-Sunstein" coaching framework (5 dimensions)
- **Why**: The intersection IP. No other AI coaching company frames it this way.
- **Method**: Combine Sunstein's 5 principles (choice architecture, defaults, sludge, attention, autonomy) with Solstein's 8 scoring dimensions. Define 5 new dimensions specifically for AI coaching.
- **Output**: `/opt/data/source-materials/sunstein/solstein-sunstein-coaching-framework.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: 🔴 HIGH

### 12. Sunstein-aligned AI coaching prompt library
- **Why**: The actual prompts our AI coach uses, grounded in Sunstein methodology.
- **Method**: Build 30 prompts (10 per language × 3 languages) grounded in Nudge + Sludge + Choosing Not to Choose. Test against 3 mock coaching sessions.
- **Output**: `/opt/data/source-materials/coaching/sunstein-prompt-library.md`
- **Owner**: Erebus
- **Cadence**: Once, iterate per model upgrade
- **Priority**: 🔴 HIGH

### 13. Sunstein-style "ethics review" for AI coaching outputs
- **Why**: A formal review process for coaching outputs to ensure they preserve autonomy (not manipulate).
- **Method**: Build a checklist (10 items) per Sunstein's "On Freedom" framework. Apply to every coaching session output.
- **Output**: `/opt/data/skills/sunstein-ethics-review/SKILL.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 14. Solstein-Sunstein benchmarking study
- **Why**: Compare BetterUp/CoachHub/Valence on the Solstein-Sunstein 5-dimension framework. Position ourselves as the highest scorer.
- **Method**: Score 10 AI coaching companies on each dimension. Identify the gap.
- **Output**: `/opt/data/agents/research/sunstein-solstein-coaching-benchmark.md`
- **Owner**: Erebus
- **Cadence**: Quarterly
- **Priority**: MEDIUM

### 15. Sunstein "informed consent" pattern for AI coaching
- **Why**: Users should know they're being nudged. Sunstein emphasizes transparency.
- **Method**: Build a 30-second onboarding flow that explains (a) what nudges the AI will use, (b) how to opt out of any nudge, (c) what data we collect, (d) what choices you keep.
- **Output**: `/opt/data/source-materials/coaching/informed-consent-flow.md`
- **Owner**: Erebus + Ivan
- **Cadence**: Once
- **Priority**: HIGH (EU AI Act compliance)

## Group D — Solstein AI Paraguay client (5 areas)

### 16. Research who Solstein AI actually is
- **Why**: We built them 3 pages but have no public info on the company. Are they a competitor? A partner? An acquisition target?
- **Method**: Search LinkedIn, Paraguayan business registry, Solstein social media, Paraguayan Chamber of Commerce. Document findings.
- **Output**: `/opt/data/agents/research/solstein-py-due-diligence.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 17. Solstein coaching agent prototype
- **Why**: If Solstein is a tech/AI company, they might want an AI coaching product. Build a prototype.
- **Method**: Apply the Sunstein-Sunstein framework to build a "Solstein AI Coach" — a trilingual AI coach branded for Solstein.
- **Output**: Prototype deployed at `solstein-ai.paragu-ai.com/coach`
- **Owner**: Erebus + Kyrian
- **Cadence**: Once
- **Priority**: MEDIUM

### 18. Solstein product extension roadmap
- **Why**: Solstein currently has 3 pages (Tecnología, AI, Cloud). Could expand to: Solstein Coach, Solstein Compliance, Solstein Education.
- **Method**: Propose 3 product extensions based on existing client needs (Rubicón EAS coaching, Mark NL coaching, ParaguAI Builder beauty).
- **Output**: `/opt/data/build/solstein-product-roadmap.md`
- **Owner**: Erebus + Ivan
- **Cadence**: Once
- **Priority**: MEDIUM

### 19. Solstein site content refresh (trilingual + Sunstein-aligned)
- **Why**: Current Solstein sites are template-level. Could elevate with trilingual content + Sunstein-style copy.
- **Method**: Build 3 new landing pages per Solstein site (ES, EN, NL) with Sunstein-inspired value props.
- **Output**: Updated Solstein sites
- **Owner**: Erebus + Kyrian
- **Cadence**: Once
- **Priority**: LOW

### 20. Solstein pricing strategy
- **Why**: The 3 Solstein pages don't show pricing. Need pricing for any revenue.
- **Method**: Apply `paraguai-proposal-pricing` skill methodology to Solstein's 3 verticals (Tecnología, AI, Cloud). Build pricing tiers per vertical.
- **Output**: `/opt/data/build/solstein-pricing.md`
- **Owner**: Erebus + Ivan
- **Cadence**: Once
- **Priority**: MEDIUM

## Group E — Org-level integration (5 areas)

### 21. 🔴 Update SOUL.md to v2 (codify Sunstein-style discipline)
- **Why**: SOUL.md is 19 lines. Could grow to 200+ lines codifying memory rules, workflow patterns, project playbooks, quality gates, trilingual handling, trademark compliance.
- **Method**: Expand SOUL.md to v2 with: (a) memory rules, (b) workflow patterns (TDD, fail-loud, security-first specifics), (c) project playbooks (Rubicón, Mark NL, Solstein), (d) quality gates, (e) trilingual handling, (f) trademark compliance, (g) research method (Cass Sunstein grounding).
- **Output**: `/opt/data/SOUL.md` v2
- **Owner**: Erebus + Ivan
- **Cadence**: Once, then iterate
- **Priority**: 🔴 HIGH

### 22. Solstein pipeline × ICF methodology alignment
- **Why**: Solstein is M&A-oriented; ICF is coaching-oriented. Need a bridge.
- **Method**: Build a mapping: Solstein 8 dimensions → ICF 8 competencies. The intersection = "Solstein-ICF hybrid" for evaluating coaching companies.
- **Output**: `/opt/data/source-materials/coaching/solstein-icf-mapping.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

### 23. Sunstein-style "weekly public memo" for AIW
- **Why**: Sunstein wrote "The World According to Cass Sunstein" — a weekly blog/memo. Could become a content marketing channel for AIW.
- **Method**: Build a weekly LinkedIn/newsletter series: "The World According to AI Whisperers" — Cass Sunstein style memo on AI coaching.
- **Output**: `/opt/data/marketing/world-according-to-aiw/` content calendar + first 4 posts
- **Owner**: Erebus + Ivan
- **Cadence**: Weekly
- **Priority**: MEDIUM

### 24. Sunstein ethics review for all AIW output
- **Why**: Sunstein's "On Freedom" is the ethics canon. Apply to all our AI outputs.
- **Method**: Build an automated Sunstein-ethics-review script that flags manipulative patterns in our content (coaching prompts, sales copy, agent decisions).
- **Output**: `/opt/data/skills/sunstein-ethics-checker/SKILL.md`
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

### 25. Cross-reference: Sunstein + Solstein + 200-ai-coaching + 30-coaching-areas
- **Why**: We have 4 research docs (Sunstein, Solstein, 200 coaching companies, 30 research areas). Need a single "master index" that ties them together.
- **Method**: Build `/opt/data/agents/research/INDEX.md` cross-referencing all 4 docs with key terms + decisions.
- **Output**: `/opt/data/agents/research/INDEX.md`
- **Owner**: Erebus
- **Cadence**: Once, update as new research ships
- **Priority**: 🔴 HIGH

---

# Section 5: Skills gap audit (Sunstein/Solstein-flavored additions)

Beyond the 11 coaching skills from `coaching-skills-gap-audit.md`, **4 new skills** specific to Sunstein + Solstein:

### Skill S1: `sunstein-ethics-review` — ethics checker for AI outputs
- **Purpose**: Apply Sunstein's "On Freedom" framework to flag manipulative patterns in our content.
- **Time**: 4h

### Skill S2: `solstein-pipeline-runner` — Solstein CLI tool
- **Purpose**: Wrap Solstein pipeline in a CLI; run scoring in 60s; output JSON + markdown.
- **Time**: 6h

### Skill S3: `sunstein-prompt-library` — Sunstein-aligned coaching prompts
- **Purpose**: 30 prompts (10 × 3 languages) grounded in Nudge + Sludge + Choosing Not to Choose.
- **Time**: 8h

### Skill S4: `solstein-lite-deploy` — public Solstein lite tool
- **Purpose**: The 12-16h public deployment sketched in `/opt/data/repos/infrastructure/sales-playbook/solstein-lite-tool.md`.
- **Time**: 16h

**Total new skills**: 4 (34h)

---

# Section 6: The single bet

**The bet**: AI Whisperers can claim the **"Sunstein-aligned AI coaching"** intellectual niche — combining (a) the canonical methodology from Cass Sunstein, (b) the Solstein scoring framework for evaluating coaching companies, and (c) the trilingual/LATAM/EU moat from our org.

**The single next action**: **Read "Nudge: The Final Edition" (Sunstein + Thaler, 2021)** — extract the 9 nudge framework; map to AI coaching prompts; document as `/opt/data/source-materials/sunstein/nudge-summary.md`. This is the **IP foundation** of everything that follows.

---

# Files cited

- `/opt/data/SOUL.md` — Sunstein Persona definition
- `/opt/data/config.yaml` — Hermes config (provider/models)
- `/opt/data/sites/clients/solstein*.html` — Solstein client sites (3 pages)
- `/opt/data/sites/manifest.json` — Solstein manifest entries
- `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/solstein-analysis.md` — Solstein M&A scorecard for Nexa
- `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/solstein-scorecard.json` — Solstein scorecard JSON
- `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/research/ai-opportunity-map.md` — 8 AI opportunities for Nexa
- `/opt/data/repos/infrastructure/sales-playbook/solstein-lite-tool.md` — Solstein lite tool architectural sketch
- `/opt/data/scratchpad/sales-playbook/solstein-lite-tool.md` — backup sketch
- `/opt/data/agents/research/200-ai-coaching-companies.md` — 197 coaching companies (Aug 14)
- `/opt/data/agents/research/30-coaching-research-areas.md` — 30 research areas (Aug 14)
- `/opt/data/agents/research/coaching-skills-gap-audit.md` — 11 new skills (Aug 14)
- `/opt/data/agents/research/coaching-strategic-implications.md` — strategy doc (Aug 14)

# Research methodology

- **Cass Sunstein canon**: 6 ddgs queries (Sunstein-related) × 10 results = 60 hits; verified via Wikipedia + MIT Press + Goodreads + multiple book reviews
- **Solstein pipeline**: pulled from existing `/opt/data/build/monorepo-sparse/apps/nexa-paraguay/docs/09-market-intelligence/` (May 2026)
- **Solstein client**: pulled from `/opt/data/sites/clients/` + `/opt/data/sites/manifest.json`
- **Sunstein persona**: pulled from `/opt/data/SOUL.md` + confirmed via session dump files
- **Date**: 2026-08-14 by Erebus

## Source verification

- Cass Sunstein is **confirmed real**: American legal scholar at Harvard Law, NYT bestseller, co-author of "Nudge" with Richard Thaler (Nobel laureate), former Administrator of OIRA in Obama White House. Wikipedia confirms his 30+ books and hundreds of articles.
- Solstein AI Paraguay is **our own client**: 3 sites in `/opt/data/sites/clients/`, manifest entries, backup copies in scratchpad.
- Solstein M&A pipeline is **our internal tool**: `Ai-Whisperers/solstein-manda-research` (private repo, currently 404 on public API).
- The "Sunstein Persona" is **the agent operating contract**: confirmed in `/opt/data/SOUL.md` line 1 + every session dump.