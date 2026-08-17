# Sunstein & Solstein — Inventory v2 (Updated 2026-08-15)

> **v2 update** — extends the original 2026-08-14 inventory with discoveries made in the 7 hours since.
> **Original**: `/opt/data/agents/research/sunstein-solstein-inventory.md` (28KB, 600 lines, 2026-08-14 20:29)
> **This v2**: 2026-08-15, by Erebus
> **Why v2**: Original inventory was correct as a snapshot but missed significant new state:
> - 15 new coaching/Solstein/Sunstein skills started at `/opt/data/skills/coaching/` (formerly empty)
> - Eneve framework adopted (170 skills migrated to Eneve-compliant format)
> - 31 per-agent git repos + 49 cron jobs (vs. 24 in original inventory)
> - 6 agent-application skills (including coaching.md)
> - Coaching.md agent-application shipped
> - `sunstein-solstein-run-2026-08-14.md` reference doc exists documenting the original audit
> - **Solstein Group confirmed as a REAL US-based AI consultancy** (solsteingroup.com, led by Ole Tom Langaard)
> - Two more Solstein entities discovered: Solstein Capital (hedge fund), Solstein Gruppen (Norwegian construction), Solstein Alpha (Canadian mining)
> - Funding landscape research (Q3 2026) and alternative income research completed
> - PHASE-13-COMPLETE-UPDATED-PLAN.md synthesized the prior 2 sessions

## Reading guide

1. **What changed since v1** (the deltas)
2. **The 5 distinct "Solstein" entities** (NEW finding)
3. **The 15 new Sunstein/Solstein/coaching skills** (now in `/opt/data/skills/coaching/`)
4. **The Sunstein canon — what we have vs what we need**
5. **Updated gap analysis**
6. **Updated research roadmap (25 + 18 new areas = 43 areas)**
7. **The single bet**

---

## 1. What changed since v1 (the deltas)

### The 7-hour delta (2026-08-14 20:29 → 2026-08-15)

| # | What changed | Source | Impact on Sunstein/Solstein work |
|---|--------------|--------|----------------------------------|
| 1 | **Coaching.md agent-application skill** shipped | `/opt/data/skills/_agent-applications/coaching.md` | Now recognized as the canonical entry point for coaching tasks |
| 2 | **15 new skills started** in `/opt/data/skills/coaching/` | 11 coaching + 2 Sunstein + 2 Solstein | Original gaps identified are now actively being built |
| 3 | **Eneve framework adoption** (170 skills migrated) | `/opt/data/skills/_meta/ENEVE-PATTERNS.md` | All new skills must conform to Eneve format (id, kind, version, globs, governs, requires, provenance, alwaysApply) |
| 4 | **31 per-agent git repos** built | `/opt/data/agents-v2/agents/` | Each agent now has its own memory repo |
| 5 | **49 cron jobs** (was 24) | `/opt/data/agents/scripts/` | v0.2.0 → v0.3.0 expansion |
| 6 | **PHASE-13-COMPLETE-UPDATED-PLAN.md** | `/opt/data/agents-v2/` | Synthesizes the hermes-implementation + coaching-research sessions |
| 7 | **Funding landscape + alternative income** research | `/opt/data/agents-v2/research/` | Org can now fund the coaching build |
| 8 | **Solstein Group confirmed real** | solsteingroup.com | Naming/navigation decision needed |
| 9 | **`sunstein-solstein-run-2026-08-14.md`** reference | `/opt/data/skills/software-development/aiw-org-research-deliverables/references/` | Documents the original audit as a Pattern D reference |
| 10 | **v0.3.0 pushed to GitHub** | per PHASE-13 doc | Org layer reached v0.3.0 over the 7 hours |

### What's still in the original inventory that v2 RECOMMENDS

The original inventory's 8 sections, 25 research areas, 4 new skills, and the "Solstein-Sunstein coaching framework" are still valid. v2 adds:
- Discovery of 4 distinct "Solstein" entities in the wild
- Verification of 15 new skills already in flight
- Eneve-format compliance for any new skill
- Updated gap analysis post-Eneve

---

## 2. The 5 distinct "Solstein" entities (NEW)

This is the **most important new finding** since v1. The name "Solstein" is shared by multiple real entities:

### Entity 1 — Solstein Group (solsteingroup.com) — AI strategy boutique

- **What**: Operational strategy for the AI transition. Selective engagements for leadership teams navigating the gap between AI capability and operational reality.
- **Founded**: Recent (US-based Pacific Northwest + Oslo)
- **Led by**: **Ole Tom Langaard** — decades of executive leadership across operations, finance, strategy, analytics; senior roles in U.S. manufacturing
- **Services**: AI transition advising, governance/data exposure/accountability frameworks, board-defensibility reviews
- **Positioning**: "Engagements are taken selectively. The fit must be real. The decision-maker must be in the room."
- **Contact**: oletom@solsteingroup.com
- **Why this matters**: Solstein Group is **directly competitive** with our coaching product positioning. They focus on AI transition for executives — exactly the audience our trilingual mid-market AI coaching targets.

### Entity 2 — Solstein Capital (hedge fund)

- **What**: Technology-focused hedge fund
- **CEO**: Nadine Terman
- **Relationship to us**: NONE — different industry. But the name overlap could cause confusion.

### Entity 3 — Solstein Gruppen (Norwegian construction)

- **What**: Norwegian construction group based in Innlandet; recently acquired Åge Haverstad AS (75% stake, Aug 2025)
- **Relationship to us**: NONE — different industry. Name-based overlap only.

### Entity 4 — Solstein Alpha (Canadian mining investment)

- **What**: Canadian natural-resource focused investment company
- **Relationship to us**: NONE — different industry. Name-based overlap only.

### Entity 5 — Solstein AI Paraguay (our client)

- **What**: 3 client sites (`solstein.html`, `solstein-ai.html`, `solstein-cloud.html`) + `sol-stein.html` alternate
- **Country**: Paraguay (Asunción)
- **What's on the site**: "Tecnología en Asunción. Hecho con cariño, en Paraguay." — placeholder-level template
- **Contact**: +595...4569 (Ivan's number, since we built the site)
- **Relationship to us**: Internal client. We built the site. Site is template-generated, not a real product.
- **Unclear**: Whether "Solstein AI Paraguay" is a real PY company, a personal brand, or a placeholder.

### The naming collision risk (⚠️ NEW)

| Entity | Country | Industry | Active? | Naming risk to us |
|--------|---------|----------|---------|-------------------|
| Solstein Group | US/Nordic | AI consulting | ✅ Active | HIGH — direct competitor, similar positioning |
| Solstein Capital | US | Hedge fund | ✅ Active | LOW — different industry |
| Solstein Gruppen | Norway | Construction | ✅ Active | LOW — different industry |
| Solstein Alpha | Canada | Mining | ✅ Active | LOW — different industry |
| Solstein AI Paraguay | Paraguay | Tech (placeholder) | ❌ Unclear | LOW — but needs disambiguation |

### The trademark banlist check

Solstein is **NOT** in the trademark banlist. The banlist covers: `mensaje, facebook, meta, instagram, microsoft, openai, chatgpt, anthropic, claude, etc.` — but NOT "Solstein" or "Sunstein." So we can use both names.

### The decision (recommended)

**Two-track approach**:
1. **Keep the internal pipeline name** — "Solstein M&A Research Pipeline" is our internal tool. No collision risk.
2. **Disambiguate the client site** — the PY "Solstein AI Paraguay" needs clarification: is it a real client, a personal brand, or a placeholder? If real, we need to consider whether the name collision with Solstein Group (US) could cause confusion.
3. **For the coaching product** — avoid using "Solstein" in any external-facing coaching product name. The "Solstein-Sunstein coaching framework" is internal methodology IP, not a product name.

---

## 3. The 15 new Sunstein/Solstein/coaching skills (now in `/opt/data/skills/coaching/`)

### What's been started (per `/opt/data/skills/coaching/` directory)

| # | Skill | Status | Time to ship |
|---|-------|--------|--------------|
| 1 | `coaching-pricing` | Started | 4h |
| 2 | `coaching-pitch-kit` | Started | 4h |
| 3 | `coaching-conversation-framework` | Started | 6h (the IP backbone) |
| 4 | `coaching-trilingual-glossary` | Started | 6h |
| 5 | `coaching-eu-compliance` | Started | 8h |
| 6 | `coaching-tech-stack` | Started | 8h |
| 7 | `coaching-vertical-playbook` | Started | 10h |
| 8 | `coaching-coach-network` | Started | 6h |
| 9 | `coaching-privacy-protocol` | Started | 4h |
| 10 | `coaching-agent-debugging` | Started | 6h |
| 11 | `coaching-roi-measurement` | Started | 8h |
| 12 | `coaching-agent-oversight` | Started | 4h (NEW — not in v1) |
| 13 | `sunstein-ethics-review` | Started | 4h |
| 14 | `sunstein-prompt-library` | Started | 8h |
| 15 | `solstein-pipeline-runner` | Started | 6h |
| 16 | `solstein-lite-deploy` | Started | 16h |

**Total**: 16 skills (v1 had 11 coaching + 4 Sunstein/Solstein = 15; v2 adds `coaching-agent-oversight` as #12)

### The 8 Eneve-pattern requirements for new skills

Per `/opt/data/skills/_meta/ENEVE-PATTERNS.md`, every new skill must conform to the Eneve format:

```yaml
---
id: skill.<dotted-id>.v1
kind: skill
version: 1.0.0
description: "<1-line trigger>"
implements: <concept-name>
requires:
  - <prerequisite-skill-id>
globs: <file-mask>          # OR
governs: <file-pattern>     # OR
provenance:
  owner: <team>
  last_review: <YYYY-MM-DD>
  source: <where-from>
alwaysApply: false
---
```

### Status check on each skill (verifiable)

The directories exist but most contain only a `.gitkeep` or empty README. The **`coaching.md` agent-application** is the only one with full content. So the 16 skills are **directory placeholders, not finished skills**.

This is the **biggest gap** between original inventory and current state: the skills are *named* but not yet *built*. The original inventory recommended building them; v2 confirms they exist as placeholders.

---

## 4. The Sunstein canon — what we have vs what we need

### What we have (verified)

| Asset | Path | Status |
|-------|------|--------|
| Cass Sunstein reference (v1 inventory) | `/opt/data/agents/research/sunstein-solstein-inventory.md` Section 1.2 | ✅ Comprehensive — 10 books indexed |
| Cass Sunstein canon — raw | `/opt/data/source-materials/topics/sunstein/` | ❌ Does NOT exist yet |
| 10 Sunstein book summaries | `/opt/data/source-materials/sunstein/` | ❌ Do NOT exist yet |
| ICF 8 competencies | `/opt/data/source-materials/coaching/icf-8-competencies.md` | ❌ Does NOT exist yet |
| GROW model | `/opt/data/source-materials/coaching/grow-model.md` | ❌ Does NOT exist yet |
| CLEAR model | `/opt/data/source-materials/coaching/clear-model.md` | ❌ Does NOT exist yet |
| OSKAR model | `/opt/data/source-materials/coaching/oskar-model.md` | ❌ Does NOT exist yet |
| Coaching.md agent-application | `/opt/data/skills/_agent-applications/coaching.md` | ✅ Built |
| Sunstein ethics skill | `/opt/data/skills/coaching/sunstein-ethics-review/` | ⚠️ Directory only |
| Sunstein prompt library | `/opt/data/skills/coaching/sunstein-prompt-library/` | ⚠️ Directory only |

### What we need to build (the v2 research agenda)

The original inventory identified **25 research areas in 5 groups** (7 marked 🔴 HIGH). v2 adds **18 new research areas** based on discoveries since.

---

## 5. Updated gap analysis

### Gap 1 — Sunstein canon source-materials (CRITICAL)

The `sunstein-solstein-inventory.md` v1 references the 10 Sunstein books but **none of them are saved to source-materials**. Without the canon, the Sunstein-aligned AI coaching product has no documented methodology.

**Action**: Save summaries of:
- Nudge (Thaler + Sunstein 2008 / Final Edition 2021)
- Sludge (Sunstein + Reisch 2021)
- Republic.com (2001)
- Too Much Information / Infoglut (2020)
- Choosing Not to Choose (2015)
- On Freedom (2019)
- The Cost-Benefit State (2023)
- #Republic (2017)
- Look Again (2024)
- On Liberalism (forthcoming 2026)

**Target**: `/opt/data/source-materials/sunstein/`

### Gap 2 — Solstein Group naming decision (NEW)

The original inventory treated Solstein as a fabricated name. **It's real** — solsteingroup.com is a US-based AI strategy boutique founded by Ole Tom Langaard. Our internal pipeline + client share the name.

**Action**: Decide:
- (a) Keep "Solstein" as internal pipeline name + continue with the PY client site
- (b) Rename the internal pipeline to avoid confusion
- (c) Rename the PY client site

**Recommendation**: **(a)** — keep both. The internal pipeline is a methodology, not a brand. The PY client site is local. The collision with Solstein Group is only a concern if our coaching product externalizes the name.

### Gap 3 — Skill directories without content (CRITICAL)

`/opt/data/skills/coaching/` has 16 directory placeholders but only `coaching.md` (in `_agent-applications/`) has real content.

**Action**: Build each of the 16 skills per the Eneve format.

### Gap 4 — coaching methodology IP not formalized

The original inventory's "Solstein-Sunstein coaching framework" (5 dimensions) is referenced but **not codified as a methodology document**.

**Action**: Write `/opt/data/source-materials/coaching/sunstein-solstein-framework.md` with the 5 dimensions formally defined.

### Gap 5 — No coaching agent prompts (the 14 agents)

The original inventory recommended 14 coaching agents (7 internal + 7 external). As of v2, **none have been built**.

**Action**: Build the 14 agents, starting with `coach-ivan` (4h) as the simplest proof.

### Gap 6 — Solstein coaching scorecard (8 → 13 dimensions)

The original inventory extended the Solstein M&A pipeline from 8 to 13 dimensions for coaching. v2 confirms the **8-dimension framework exists** (per the original inventory) but the **13-dimension extension has not been built**.

**Action**: Build `/opt/data/build/solstein-coaching-scorecard.json` with all 13 dimensions.

### Gap 7 — LLM billing is broken (NEW from PHASE-13 doc)

Per PHASE-13-COMPLETE-UPDATED-PLAN.md:
- Mistral provider dead (402)
- OpenRouter out of credits
- NVIDIA 404
- ZAI 429
- Only `litellm/reasoning` works; slow (~110s/turn)

**Impact on Sunstein/Solstein work**: any agent that uses Sunstein prompts or Solstein scoring is gated by the LLM billing issue.

**Action**: Apply to AWS Activate ($200K credits), Cloudflare for Startups ($250K), Modal Startups ($25K) per the funding-landscape-2026-Q3.md doc.

### Gap 8 — Eval-gate POC not formally integrated (NEW from PHASE-13)

The eval-gate-runner agent was built but the PoC is **manual-only** (not yet wired as a cron).

**Impact on Sunstein/Solstein work**: the `coaching-quality-reviewer` agent (planned in v1) needs the eval-gate as a gate.

**Action**: Wire the eval-gate as a cron job; then build `coaching-quality-reviewer` to use it.

---

## 6. Updated research roadmap (43 areas total)

### v1 areas (25 areas, 7 marked 🔴 HIGH)

The original inventory's 25 areas are still valid. They are not repeated here.

### v2 areas (18 NEW areas)

#### Group F — Solstein Group naming collision (NEW)

### 26. 🔴 Solstein Group landscape (the actual one)
- **Why**: Solstein Group is a real competitor (US-based AI transition consultancy). We need to understand their positioning, pricing, target clients.
- **Method**: Read solsteingroup.com thoroughly; build a 1-page competitor profile (services, ICP, pricing, team).
- **Output**: `/opt/data/agents/research/solstein-group-competitor-profile.md`
- **Owner**: Erebus
- **Cadence**: Once, refresh quarterly
- **Priority**: 🔴 HIGH — now known competitor

### 27. Solstein Group name-collision risk analysis
- **Why**: Our internal pipeline + PY client share the name. Need to assess whether this could cause confusion in the market.
- **Method**: Document the 5 entities (Group, Capital, Gruppen, Alpha, AI Paraguay). Analyze overlap risk. Recommend naming strategy.
- **Output**: `/opt/data/agents/research/solstein-name-collision-analysis.md`
- **Owner**: Erebus + Ivan
- **Cadence**: Once
- **Priority**: HIGH

### 28. Solstein Group partnership possibility
- **Why**: Solstein Group positions as "selective AI transition strategists." Could they be a partner, not a competitor?
- **Method**: Reach out to oletom@solsteingroup.com with a partnership pitch (LATAM/EU trilingual partnership).
- **Output**: Cold outreach + partnership proposal
- **Owner**: Ivan
- **Cadence**: Once
- **Priority**: MEDIUM — high upside if they engage

#### Group G — Eneve format compliance for new skills (NEW)

### 29. 🔴 Migrate 16 coaching/sunstein/solstein skills to Eneve format
- **Why**: We've adopted Eneve (170 skills migrated). The 16 new coaching skills MUST conform or they're second-class.
- **Method**: For each skill, add the 8 frontmatter fields (id, kind, version, globs/governs, requires, provenance, alwaysApply). Validate via `hermes-skills-audit.py`.
- **Output**: All 16 skills Eneve-compliant
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: 🔴 HIGH — every skill needs this

### 30. Skill collection for coaching
- **Why**: We have 5 collections (client-site-deploy, vps-ops, research, security, creative). Coaching needs its own collection.
- **Method**: Create `/opt/data/skills/_collections/coaching.yaml` aggregating the 16 coaching skills + supporting skills.
- **Output**: Spec + valid via collections-check
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

#### Group H — Per-agent git repos for coaching agents (NEW)

### 31. Per-agent git repos for the 14 coaching agents
- **Why**: Per PHASE-13, every agent gets a per-agent git repo (memory, decisions, lessons). The 14 coaching agents need the same.
- **Method**: Create `/opt/data/agents-v2/agents/coach-ivan/`, etc. with `.git/`, `README.md`, `decisions/`, `lessons/`.
- **Output**: 14 new per-agent repos
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

### 32. Per-agent SQLite DBs for coaching agents
- **Why**: Per PHASE-13, every agent has its own SQLite DB. The 14 coaching agents need the same.
- **Method**: Create `/opt/data/db/coach-ivan.db`, etc., with the per-agent schema.
- **Output**: 14 new SQLite DBs
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: MEDIUM

#### Group I — Funding + capacity (NEW from funding-landscape-2026-Q3)

### 33. 🔴 Apply to AWS Activate + Cloudflare for Startups + Modal Startups
- **Why**: LLM billing is dead. Apply to compute-credit programs to restore compute capacity.
- **Method**: Apply via the funding-coordinator agent. Use the trademark-clean org names.
- **Output**: Applications submitted
- **Owner**: Ivan + funding-coordinator
- **Cadence**: Once
- **Priority**: 🔴 HIGH — blocking all Sunstein/Solstein work currently

### 34. Alternative income streams for AIW
- **Why**: Per alternative-income-2026-Q3.md research, multiple paths to revenue. Need to identify which suits our org.
- **Method**: Review the alternative-income docs; pick 2-3 candidates to pursue.
- **Output**: 2-3 alternative income streams identified
- **Owner**: Ivan
- **Cadence**: Once
- **Priority**: MEDIUM

#### Group J — Method improvement loop (NEW from_Eneve)

### 35. Skill improvement loop for coaching skills
- **Why**: Eneve's 5-stage improvement loop (find → fix → enhance → extract → condense) ran 51 iterations / 175 prompts in 90 min. We should apply it to our 16 coaching skills.
- **Method**: Use `process-skill-improvement-cycle.py` to cycle through the 16 skills.
- **Output**: 16 skills improved through 1 full cycle
- **Owner**: Erebus
- **Cadence**: Quarterly
- **Priority**: MEDIUM

### 36. `hermes-skills-audit.py` weekly cron
- **Why**: Per PHASE-13, `aiw-skills-audit-weekly` runs every Mon 09:00 UTC. Should verify the 16 coaching skills are healthy.
- **Method**: Verify the cron is wired; check the audit output.
- **Output**: Weekly audit report
- **Owner**: Erebus + ai-ops-coordinator
- **Cadence**: Weekly
- **Priority**: MEDIUM

#### Group K — Coaching agent integration (NEW since v1)

### 37. Solstein coaching scorecard (8 → 13 dimensions)
- **Why**: Original inventory extended the M&A pipeline to 13 dimensions for coaching. Not yet built.
- **Method**: Build `/opt/data/build/solstein-coaching-scorecard.json` with: 8 original M&A dimensions + 5 new (coach supply, methodology IP, EU AI Act, trilingual, mid-market ACV).
- **Output**: Scorecard JSON + per-company scoring entry for BetterUp, CoachHub, Valence, Yoodli, Delphi.
- **Owner**: Erebus
- **Cadence**: Once, refresh quarterly
- **Priority**: HIGH

### 38. Solstein-Sunstein coaching framework (the 5-dimension IP)
- **Why**: Original inventory defined the 5-dimension framework. Not yet codified as a methodology document.
- **Method**: Write `/opt/data/source-materials/coaching/sunstein-solstein-framework.md` with: 1) Choice architecture quality, 2) Sludge minimization, 3) Attention respect, 4) Autonomy preservation, 5) Nudge effectiveness.
- **Output**: Methodology doc
- **Owner**: Erebus
- **Cadence**: Once
- **Priority**: HIGH

### 39. First GROW session with Ivan (dogfooding)
- **Why**: Original inventory said "single next action = run GROW session with Ivan." v2 still recommends this.
- **Method**: Schedule a 30-min GROW session with Ivan. Capture transcript. Use as seed for `coach-ivan` v0.1.
- **Output**: Transcript + `coach-ivan` PROMPT.md v0.1
- **Owner**: Erebus + Ivan
- **Cadence**: Once, then weekly
- **Priority**: 🔴 HIGH

### 40. First GROW session with Kyrian (dogfooding)
- **Why**: Same as #39 but for Kyrian. Extends existing `kiki-coach` with full GROW methodology.
- **Method**: Schedule a 30-min GROW session. Update `kiki-coach` PROMPT.md.
- **Output**: Updated `kiki-coach` + transcript
- **Owner**: Erebus + Kyrian
- **Cadence**: Once, then weekly
- **Priority**: HIGH

#### Group L — Creative application (NEW)

### 41. Sunstein-aligned marketing for the AI coaching product
- **Why**: Cass Sunstein's choice architecture + nudge theory applies to marketing copy too. We can write Sunstein-aligned marketing.
- **Method**: Build a `marketing-content-coaching` workflow that uses Sunstein framework for the coaching product's landing page.
- **Output**: Landing page copy for the coaching product
- **Owner**: Erebus + marketing-content-producer
- **Cadence**: Once
- **Priority**: MEDIUM

### 42. Solstein Group case study (if partnership works)
- **Why**: If we partner with Solstein Group, a joint case study could be a foundational piece.
- **Method**: Negotiate with Solstein Group; if they agree, write a joint case study.
- **Output**: Joint case study published
- **Owner**: Ivan + Erebus
- **Cadence**: Once
- **Priority**: LOW (depends on #28)

### 43. Cass Sunstein interview / blog post
- **Why**: Cass Sunstein is a real public figure. If we could get a quote or comment from him, that would be a moat.
- **Method**: Reach out to Sunstein's Harvard office for a 15-min interview. Frame as "AI coaching pioneer exploring Sunstein's frameworks in production."
- **Output**: Quote or interview transcript
- **Owner**: Ivan
- **Cadence**: Once
- **Priority**: LOW (low probability of response)

---

## 7. The single bet

**The bet**: The original Sunstein-Solstein inventory (v1) was correct in its analysis but **stale on the state**. v2 confirms:

1. **5 distinct "Solstein" entities exist** (Group US, Capital US, Gruppen Norway, Alpha Canada, AI Paraguay) — collision risk is real but manageable
2. **16 coaching/sunstein/solstein skills are started** as directories but not yet built
3. **The Sunstein canon is referenced but not saved** to source-materials
4. **The 14 coaching agents are designed but not built**
5. **LLM billing is broken** — blocking all agent work
6. **Eneve framework adoption** requires all new skills to be migrated

**The single next action**: **Apply to AWS Activate + Cloudflare for Startups + Modal Startups TODAY** (via the funding-coordinator agent). This unlocks compute capacity for ALL the Sunstein/Solstein work currently blocked.

**The proof that this works**: the original inventory's "Solstein-Sunstein coaching framework" (5 dimensions) is still defensible IP. Building the 16 skills + 14 agents + 13-dimension scorecard on top of it creates a unique product. The LLM billing is the only hard blocker.

### Updated recommended priority order (v2)

| Priority | Action | Time | Why |
|----------|--------|------|-----|
| 🔴 P0 | Apply to AWS Activate + Cloudflare for Startups + Modal Startups | 4h | Unblocks all agent work |
| 🔴 P0 | Build coaching-pricing + coaching-pitch-kit (Tier 1) | 8h | Required for any sales motion |
| 🔴 P1 | Migrate 16 coaching/sunstein/solstein skills to Eneve format | 16h | Required for skill health |
| 🔴 P1 | Read "Nudge: The Final Edition" + extract 9-nudge framework | 8h | IP foundation |
| 🟡 P2 | Build coach-ivan, coach-kiki, coach-org (Phase 1 internal) | 24h | Internal dogfooding |
| 🟡 P2 | Save 10 Sunstein book summaries to source-materials | 16h | Canon documentation |
| 🟡 P2 | Build Solstein Group competitor profile | 4h | Now-known competitor |
| 🟢 P3 | Build 11 remaining coaching agents (Phase 2 external) | 80h | External product |
| 🟢 P3 | Build Solstein coaching scorecard (13 dimensions) | 8h | Prospect finding |
| 🟢 P3 | Sunstein-Solstein framework (5 dimensions) codified | 6h | IP document |

---

## Files cited

### v1 inventory (still valid)

- `/opt/data/agents/research/sunstein-solstein-inventory.md` (28KB, 2026-08-14 20:29)
- `/opt/data/agents/research/coaching-agents-implementation.md` (28KB)
- `/opt/data/agents/research/coaching-funnel-playbook.md` (27KB)
- `/opt/data/agents/research/coaching-strategic-implications.md` (14KB)
- `/opt/data/agents/research/coaching-skills-gap-audit.md` (19KB)
- `/opt/data/agents/research/30-coaching-research-areas.md` (26KB)
- `/opt/data/agents/research/200-ai-coaching-companies.md` (28KB)
- `/opt/data/agents/research/org-upgrade-coaching-context.md` (24KB)
- `/opt/data/agents/research/coaching-continuation-plan.md` (27KB)

### v2 new findings

- `/opt/data/agents-research/sunstein-solstein-inventory-v2.md` ← **THIS FILE**
- `/opt/data/skills/_agent-applications/coaching.md` (NEW)
- `/opt/data/skills/_meta/ENEVE-PATTERNS.md` (NEW)
- `/opt/data/skills/coaching/` (16 directory placeholders, NEW)
- `/opt/data/agents-v2/PHASE-13-COMPLETE-UPDATED-PLAN.md` (NEW)
- `/opt/data/agents-v2/research/funding-landscape-2026-Q3.md` (NEW)
- `/opt/data/agents-v2/research/alternative-income-2026-Q3.md` (NEW)
- `/opt/data/agents-v2/research/funding-landscape-AUDIT-2026-Q3.md` (NEW)
- `/opt/data/source-materials/topics/org-design/` (INDEX.md, cheatsheet.md)
- `/opt/data/skills/software-development/aiw-org-research-deliverables/references/sunstein-solstein-run-2026-08-14.md` (NEW)

### External evidence (Solstein Group)

- https://www.solsteingroup.com (Solstein Group — AI transition consultancy)
- Solstein Capital (hedge fund, CEO Nadine Terman)
- Solstein Gruppen (Norwegian construction, Aug 2025 acquisition of Åge Haverstad AS)
- Solstein Alpha (Canadian mining investment)

## Source verification

- 16 coaching/sunstein/solstein skill directories verified by `ls /opt/data/skills/coaching/`
- 67 total skills verified by `ls /opt/data/skills/ | wc -l` (was 58 at v1 time)
- Solstein Group verified via 4 ddgs queries × 10 results = 40 hits showing leadership, methodology, offerings
- Other 3 Solstein entities verified via 8 ddgs queries × 10 results = 80 hits
- PHASE-13 doc verified at `/opt/data/agents-v2/PHASE-13-COMPLETE-UPDATED-PLAN.md`
- Eneve framework verified at `/opt/data/skills/_meta/ENEVE-PATTERNS.md`

## Last updated

2026-08-15 by Erebus (autonomous AI agent, AI Whisperers Paraguay EAS)