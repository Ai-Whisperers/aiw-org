# Department of Research & Education — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Ivan | **Lead agent**: `research-tracker` | **Atomic agents**: `thoth-literature-scanner`, `peitho-language-quality`, `hephaestus-document-miner`, `mnemosyne-document-archivist`
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 8 areas documented. Cadence tiers: 🔴 HOT (1), 🟡 WARM (4), 🔵 COOL (3).

---

## Reading guide

Research & Education is the **knowledge backbone** of the org. Unlike other depts that have external-facing artifacts (sales pitches, code, financials), Research's outputs are internal: thesis chapters, course content, citation databases, source materials.

Areas here focus on **meta-research** — research ABOUT how we do research.

---

# Research & Education Research Areas



## 🔴 HOT areas

### 1. Citation discipline — what's our actual citation coverage? 🔴

| | |
|---|---|
| **Question** | Of all our published research outputs (thesis chapters, course content, blog posts, whitepapers), what % has verified citations and what % has orphan references? |
| **Why** | `citation-checker` agent exists (`05-research-education/citation-checker/PROMPT.md`) but its coverage metric is unknown. If we're at <80%, we have a credibility issue. |
| **Method** | (1) Survey every doc in `wizard-academy/`, `satellite-paraguay/` (thesis), `courses/`, `company/Company/marketing/`. (2) For each doc: extract citations. (3) For each citation: verify it exists (DOI check, URL check). (4) Compute coverage %. (5) Flag orphan references. |
| **Output** | `research/citation-coverage-audit-2026.md` (per-doc table + overall coverage %) |
| **Owner** | citation-checker + research-tracker |
| **Cadence** | Quarterly |
| **Cross-references** | `05-research-education/citation-checker/PROMPT.md`, `~/skills/grounded-citations/`, `state/research.json` |

---

## 🟡 WARM areas

### 2. Course production methodology 🟡

| | |
|---|---|
| **Question** | What's the right methodology for producing a 12-module course (video + slides + transcripts + exercises) end-to-end, with our agent layer? |
| **Why** | `course-producer` agent exists but produces 1 piece/week (per `demiurge/kpi/research-stack.yaml`). For 12-module course, we need methodology to scale without losing quality. |
| **Method** | (1) Read `research/coaching-continuation-plan.md` (existing). (2) Survey 3 AI-coaching courses on quality (BetterUp Academy, CoachHub, Coursera AI courses). (3) Reverse-engineer their production pipeline. (4) Adapt to our agent layer. (5) Document the methodology. |
| **Output** | `research/course-production-methodology.md` (pipeline + agent mappings + quality gates) |
| **Owner** | course-producer + research-tracker + Ivan |
| **Cadence** | Once + per course |
| **Cross-references** | `05-research-education/course-producer/PROMPT.md`, `research/coaching-continuation-plan.md` |

### 3. Thesis to product conversion path 🟡

| | |
|---|---|
| **Question** | How does the GeoData v2 master's thesis convert to a product (course, service, SaaS) without losing academic rigor? |
| **Why** | Thesis has research value; converting to product has $ value. Without explicit methodology, the conversion either dilutes academic rigor OR fails to ship. |
| **Method** | (1) Read `satellite-paraguay/` thesis repo (current state). (2) Identify the 3-5 most valuable findings. (3) For each: potential product format (course, service, SaaS, dataset). (4) Recommend: which path(s) for which finding(s). (5) Roadmap with milestones. |
| **Output** | `research/thesis-to-product-path.md` (per-finding product mapping + roadmap) |
| **Owner** | research-tracker + Ivan |
| **Cadence** | Once + on thesis completion |
| **Cross-references** | `satellite-paraguay/`, `research/30-research-areas.md` #28 |

### 4. Academic liaison processes 🟡

| | |
|---|---|
| **Question** | What academic liaison processes (submissions, peer review, conferences) do we need to have in place by the time GeoData v2 is publication-ready? |
| **Why** | Academic publishing has long lead times (6-12 months). Process design now = no scramble later. |
| **Method** | (1) Read Ivan's existing thesis timelines. (2) Survey 3 academic CS journals (IJGIS, CEUS, TGIS) + 2 conferences (AGU Fall, AAG). (3) For each: submission criteria, review timeline, acceptance rate. (4) Recommend: 2-3 target venues per finding. (5) Document submission timeline. |
| **Output** | `research/academic-liaison-targets.md` (per-venue criteria + submission timeline) |
| **Owner** | research-tracker + Ivan |
| **Cadence** | Once + on each paper |
| **Cross-references** | `research/30-research-areas.md` #25, `research/roles-glossary.md` |

### 5. Source-materials curation methodology 🟡

| | |
|---|---|
| **Question** | What's the curation policy for our `source-materials/` repo (300+ files), and how do we enforce freshness + citation integrity at scale? |
| **Why** | `source-curator` agent exists in Operations dept but its curation policy isn't formalized. With 300+ files, manual curation breaks down. |
| **Method** | (1) Read `01-operations/source-curator/PROMPT.md` (cross-cut). (2) Inventory current `source-materials/` structure. (3) Define: what counts as "fresh" (last 90d?), "valid" (citation verified?), "active" (used in last 6mo?). (4) Build automated scoring. (5) Recommend: archive, refresh, or delete per file. |
| **Output** | `research/source-materials-curation-policy.md` (scoring system + per-file recommendation) |
| **Owner** | source-curator + research-tracker |
| **Cadence** | Quarterly + on new file |
| **Cross-references** | `01-operations/source-curator/PROMPT.md`, `~/skills/arxiv/` |

---

## 🔵 COOL areas

### 6. Hero's journey for curriculum design 🔵

| | |
|---|---|
| **Question** | Can Joseph Campbell's Hero's Journey (17 stages) be operationalized as a curriculum-design framework for AI coaching courses? |
| **Why** | Most AI courses are linear (chapter 1, 2, 3...). Hero's Journey provides a **narrative arc** that increases engagement + retention. |
| **Method** | (1) Read Joseph Campbell's Hero with a Thousand Faces (1949). (2) Map 17 stages to 12 modules (collapse some). (3) For each module: which stage, what content, what exercise. (4) Test with 1 course. (5) Compare engagement vs linear curriculum. |
| **Output** | `research/hero-journey-curriculum-framework.md` (17 stages → 12 modules mapping) |
| **Owner** | course-producer + research-tracker |
| **Cadence** | Once |
| **Cross-references** | `research/coaching-continuation-plan.md`, `research/roles-glossary.md` |

### 7. Peer review and quality gates for academic output 🔵

| | |
|---|---|
| **Question** | What peer-review process do we use internally before submitting thesis chapters or course content for external review? |
| **Why** | Without internal review, we ship embarrassing drafts. With too much review, we never ship. |
| **Method** | (1) Survey Ivan's existing thesis review process. (2) Read `research/PROMPT-ANALYSIS.md` for what works. (3) Design a 3-step process: self-review, peer-review (Kiki or agent), final-review (Ivan). (4) Document acceptance criteria per step. |
| **Output** | `research/peer-review-process.md` (3-step review + acceptance criteria) |
| **Owner** | research-tracker + Kiki |
| **Cadence** | Once |
| **Cross-references** | `05-research-education/`, `constitution/ORG-AGENTS.md` |

### 8. Publication pipeline management 🔵

| | |
|---|---|
| **Question** | How do we manage the publication pipeline (preprints, journal submissions, conference talks) across all research outputs? |
| **Why** | With 12+ potential publications over the next 2 years, manual tracking breaks. Need a system. |
| **Method** | (1) Inventory all current/preplanned publications. (2) Build a simple tracker (Notion table or markdown). (3) Define: status per pub (idea / drafting / submitted / accepted / published). (4) Add cron to remind about stale entries. |
| **Output** | `research/publication-pipeline.md` (tracker schema + first entries) |
| **Owner** | research-tracker + Ivan |
| **Cadence** | Once + quarterly review |
| **Cross-references** | `state/research.json`, `research/academic-liaison-targets.md` |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **Coaching continuation plan**: `research/coaching-continuation-plan.md`
- **Org upgrade coaching context**: `research/org-upgrade-coaching-context.md`
- **Roles glossary**: `research/roles-glossary.md`
- **Org-wide 30-research**: `research/30-research-areas.md` (Areas 25-28 thesis-specific)
- **Citation checker skill**: `05-research-education/citation-checker/PROMPT.md`
- **Source curator**: `01-operations/source-curator/PROMPT.md`
- **Skill sources**: `~/skills/arxiv/`, `~/skills/llm-wiki/`, `~/skills/grounded-citations/`
- **Sibling dept catalogs**: `research/dept-research/{01..04,06,board}-*-research-areas.md`

---

**Total research research areas**: 8
**Cadence breakdown**: 🔴 HOT 1, 🟡 WARM 4, 🔵 COOL 3
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

