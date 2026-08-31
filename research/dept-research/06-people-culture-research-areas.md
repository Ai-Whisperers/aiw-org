# Department of People & Culture — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Ivan + Kiki (co-owned) | **Lead agent**: `people-hr` | **Coaching product agent**: `kiki-coach` (in sister repo `coach-agents`)
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 6 areas documented. Cadence tiers: 🔴 HOT (2), 🟡 WARM (3), 🔵 COOL (1).
>
> **Special context**: 2-person org (Ivan + Kiki). People research is mostly **founder effectiveness**, not traditional HR (HR is Tier-3 deferred per doctrine).

---

## Reading guide

People & Culture research here is mostly **founder effectiveness + Kiki's growth + first-FTE preparation**. Traditional HR topics (compensation, benefits, HRIS) are Tier-3 deferred.

---

# People & Culture Research Areas



## 🔴 HOT areas

### 1. Ivan bandwidth audit — 2-week time tracking 🔴

| | |
|---|---|
| **Question** | How does Ivan actually spend his time across billable / internal / thesis / family / sleep categories, and what does the breakdown reveal about bandwidth optimization? |
| **Why** | Ivan's bandwidth is the **single constraint** on the org. Without data, his decisions about what to work on are guesses. |
| **Method** | (1) Track 2 weeks: every hour tagged (billable / internal / thesis / family / sleep / admin). (2) Use a simple spreadsheet or Notion. (3) At end of 2 weeks: aggregate, identify top 3 categories, find the 3 lowest-value time sinks. (4) Recommend: stop / delegate / automate. |
| **Output** | `people/ivan-bandwidth-2wk-2026.md` (per-category breakdown + 3 recommendations) |
| **Owner** | Ivan + people-hr |
| **Cadence** | Twice yearly |
| **Cross-references** | `research/30-research-areas.md` #14, `01-operations/founder-bandwidth-watchdog/PROMPT.md`, `state/coord.json` |

### 2. Kiki engineering growth path 🔴

| | |
|---|---|
| **Question** | What are Kiki's next 2 engineering milestones (technical + leadership), and what's the path to reach them? |
| **Why** | Kiki is CTO + technical director. Her growth directly determines the org's engineering ceiling. |
| **Method** | (1) Self-assessment (Kiki). (2) Peer review (Ivan reviews Kiki's last 30d of PRs). (3) Skill graph: compare to industry standard for CTO at org of similar size/stage. (4) Identify 2-3 next milestones (e.g., "ship a major refactor", "lead architecture review", "publish a technical blog post"). (5) Per milestone: 90-day plan. |
| **Output** | `people/kiki-growth-path-2026.md` (self-assessment + 2-3 milestones + 90-day plans) |
| **Owner** | kiki-coach agent + Kiki + Ivan |
| **Cadence** | Quarterly review |
| **Cross-references** | `research/30-research-areas.md` #13, `coach-agents/kiki-coach/`, `state/kiki.json`, `state/kiki-prep.json` |

---

## 🟡 WARM areas

### 3. AI engineer hiring rubric (for first FTE) 🟡

| | |
|---|---|
| **Question** | When we hire the first AI engineer FTE (Tier-3 trigger: $5K+ MRR or 6+ months runway), what's the rubric for resume screen + technical interview + system design? |
| **Why** | First FTE is high-stakes. Wrong hire = 6 months lost. Need rubric ready BEFORE the trigger fires. |
| **Method** | (1) Read `research/30-research-areas.md` #24 (hiring market). (2) Define role: AI engineer (Python + LLMs + MCPs + eval-gates). (3) Build rubric: 5 dimensions × 4 levels. (4) Draft interview questions (10 coding + 3 system design + 3 behavioral). (5) Pilot rubric with Kiki applying it to 5 real resumes. |
| **Output** | `people/ai-engineer-rubric-2026.md` (5-dim rubric + 16 interview questions) |
| **Owner** | people-hr + Kiki |
| **Cadence** | Once + per FTE hire |
| **Cross-references** | `DEFERRED-ROLES.md` Compensation (Tier-3 deferred), `research/30-research-areas.md` #24 |

### 4. Coaching methodology for engineering leaders 🟡

| | |
|---|---|
| **Question** | What's Kiki's coaching methodology for engineering leaders (specifically: 1:1 structure, goal-setting, feedback patterns, escalation handling)? |
| **Why** | Kiki coaches Ivan on engineering decisions. The methodology is implicit; making it explicit enables 2 things: (a) better coaching sessions, (b) trainable by other agents (kiki-coach agent). |
| **Method** | (1) Read `research/coaching-continuation-plan.md` + `coach-agents/kiki-coach/`. (2) Reverse-engineer Kiki's approach from her last 10 sessions with Ivan. (3) Identify: 1:1 structure (5-15-30 pattern), goal-setting (OKR + weekly), feedback (SBI model), escalation handling. (4) Document the methodology. (5) Pilot with 1 new coaching pair. |
| **Output** | `people/kiki-coaching-methodology.md` (4-component methodology + scripts) |
| **Owner** | kiki-coach agent + Kiki |
| **Cadence** | Once + quarterly tune |
| **Cross-references** | `coach-agents/kiki-coach/`, `research/coaching-continuation-plan.md`, `state/kiki-prep.json` |

### 5. Performance review cadence — founder + Kiki 🟡

| | |
|---|---|
| **Question** | What's the right cadence for Ivan ↔ Kiki performance reviews (formal + informal), and what triggers a structured conversation? |
| **Why** | 2-person co-founder teams often skip performance reviews because "we talk all the time". This leads to misalignment that compounds. |
| **Method** | (1) Read `research/org-design-literature.md` (the cadence-beats-heroics invariant). (2) Design: weekly informal (15min) + monthly structured (60min) + quarterly deep (2hr). (3) Per cadence: agenda template. (4) For each: what triggers escalation to deeper review. |
| **Output** | `people/perf-review-cadence.md` (3-tier cadence + agenda templates + escalation triggers) |
| **Owner** | people-hr + Ivan + Kiki |
| **Cadence** | Once + per quarter |
| **Cross-references** | `constitution/ORG-AGENTS.md`, `state/kiki.json` |

---

## 🔵 COOL areas

### 6. Founder bandwidth optimization — long-term 🔵

| | |
|---|---|
| **Question** | Over the next 3 years, what changes (hiring, automation, delegation) would most reduce Ivan's bandwidth constraint? |
| **Why** | Strategic — informs the 3-year roadmap. The bottleneck is Ivan, not money. |
| **Method** | (1) Read `research/STRATEGY.md` Part 5 (org setup). (2) Map: every Ivan hour → either (a) automatable, (b) delegatable to Kiki, (c) delegatable to a future FTE, (d) requires founder judgment. (3) For each: cost to automate/delegate, time saved, quality risk. (4) Build 3-year roadmap with milestones. |
| **Output** | `people/founder-bandwidth-roadmap.md` (3-year bandwidth optimization plan) |
| **Owner** | Ivan + Erebus (research) |
| **Cadence** | Once + annual review |
| **Cross-references** | `research/STRATEGY.md`, `research/30-research-areas.md` #14, `state/coord.json` |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **Coaching strategic implications**: `research/coaching-strategic-implications.md`
- **Coaching continuation plan**: `research/coaching-continuation-plan.md`
- **Coaching skills gap audit**: `research/coaching-skills-gap-audit.md`
- **Coaching continuation plan**: `research/coaching-continuation-plan.md`
- **Org-wide 30-research**: `research/30-research-areas.md` (Areas 13-16 owner: people)
- **Kiki coach agent**: `coach-agents/kiki-coach/`
- **Coaching implementation**: `research/coaching-agents-implementation.md`
- **People state**: `state/people.json`
- **Sibling dept catalogs**: `research/dept-research/{01..05,board}-*-research-areas.md`

---

**Total people research areas**: 6
**Cadence breakdown**: 🔴 HOT 2, 🟡 WARM 3, 🔵 COOL 1
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

