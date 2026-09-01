# Department 5 — Research & Education Research Catalog v2

> **Built 2026-09-01** — Phase 7 R2 (literature-grounded deepening of v1 catalog).
>
> **Purpose**: Map canonical research-organization literature (Meta FAIR, Google
> Research, Google DeepMind, MIT career ladders, MSR, Anthropic, AI safety
> frameworks) onto the 12 sub-roles in `ROLES-INVENTORY.md` and the 4 live
> sub-agents. Identify which roles are covered, partially covered, and missing.
>
> **Replaces**: extends `research/dept-research/05-research-education-research-areas.md`
> (v1, 8 areas). v2 adds the **industry-org anatomy** + **role-coverage matrix**
> + **recommended agent additions** + **best-practice reading list**.
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question
> pattern + depth test, this doc targets Level 3 — Synthesize).

---

## Reading guide

This doc is the **canonical synthesis** of what a fully-staffed research department
looks like and what we already have. Sections:

1. **How research departments work in industry** — the 4 invariants + the
   3-layer research org structure (industry anatomy)
2. **Sub-roles inventory** — every role + coverage status + what's missing
3. **Sub-agents inventory** — what we have wired today vs what we need
4. **Areas of responsibility** — the 7 functional areas a Research dept covers
5. **Setup checklist** — what we need to provision (people, tools, processes,
   artifacts) to be "fully staffed"
7. **Best-practice reading list** — books, papers, frameworks, skills
8. **Recommended agent additions** — concrete roles to add next

---

## 1 — How research departments work in industry

Across 6 reference orgs (Meta FAIR, Google Research, Google DeepMind, Microsoft
Research, MIT Office of Research, Allen Institute), the same 4 invariants emerge:

### Invariant 1 — Research is a value-stream with three distinct rhythms

| Rhythm | Cadence | Examples |
|--------|---------|----------|
| **Long-cycle research** | 6-36 months | Thesis chapters, journal papers, patent filings, exploratory prototypes |
| **Medium-cycle research** | 2-8 weeks | Course modules, whitepapers, blog posts, internal technical reports |
| **Short-cycle research** | 1-7 days | Source catalog updates, citation audits, language quality, document mining |

**Our application**: `research-tracker` runs weekly (medium cycle), the 3 atomic
agents (`thoth`, `peitho`, `hephaestus`, `mnemosyne`) run daily (short cycle),
the thesis + course pipeline runs long cycle. **All 3 rhythms are covered.**

### Invariant 2 — Research is the **producer**, every other dept is the **consumer**

```
   ┌─────────────────────────────────────────────┐
   │  5-Research (PRODUCER)                      │
   │  • thesis findings  → 4-Engineering (build) │
   │  • course content   → 6-People (deliver)   │
   │  • market claims    → 3-Sales (cite)        │
   │  • best-practice    → 1-Ops (apply)         │
   │  • macro stats      → 2-Finance (model)     │
   └─────────────────────────────────────────────┘
```

**Our application**: confirmed in the agents' `transfer_targets` — every
research sub-agent declares what it produces and who consumes it.

### Invariant 3 — Research has a **2-tier hiring model**

| Tier | Source | Examples |
|------|--------|----------|
| **Permanent staff** | Full-time researchers with PhD or equivalent | "Research Scientist" at Meta FAIR |
| **Time-bounded collaborators** | Academic partners, SMEs, contractors | MIT visiting researchers, university affiliates |

**Our application**: at 2-person scale, Ivan IS both the permanent staff and
the contractor management. We don't need to hire yet; we need **processes** so
that when we do hire, the playbook is mature.

### Invariant 4 — Research is **peer-reviewed before any external claim**

Every external publication goes through:
1. **Self-review** — author reviews own work
2. **Internal peer review** — independent reader (research engineer or senior
   researcher) provides critique
3. **External peer review** — journal/conference reviewers (when submitting)

**Our application**: `research/peer-review-process.md` already specifies a
3-step process (self → peer → final). Steps 1 + 2 are wired; step 3 deferred
until first paper submission.

### Cross-cutting: the AI-safety dimension (NEW 2026)

Per OWASP GenAI LLM Top 10 2026 and EU AI Act (in force 2026-08-02), research
departments that ship **research outputs from AI agents** (us) need:
- **Citation discipline** — every AI-generated claim must cite its source
  (per `~/skills/grounded-citations/`)
- **AI Red Team** — adversarial testing of any AI-generated output before
  publication (Tier-3 in our inventory)
- **AI Evaluator** — manual + automated quality assessment (cross-cut with
  AI Safety dept)

**Our application**: AI Evaluator and AI Red Team roles are Tier-3 in our
inventory (deferred). When we ship our first AI-generated publication, both
activate.

---

## 2 — Sub-roles inventory (12 from ROLES-INVENTORY.md)

Coverage matrix: ✅ Wired | 🟡 Partial | ❌ Missing | 💤 Deferred

| #    | Role                                | Tier  | Coverage | Agent mapping                       | What's missing                                  |
|------|-------------------------------------|-------|----------|-------------------------------------|-------------------------------------------------|
| 5.1  | Research Lead                       | 🟢 T1 | ✅ Wired | `research-tracker` (lead) + Ivan    | None — this works                                |
| 5.2  | Researcher                          | 🟢 T1 | 🟡 Partial | Ivan + `thoth-literature-scanner`  | Need a 2nd researcher when thesis-to-product starts |
| 5.3  | Writer / Editor                     | 🟢 T1 | 🟡 Partial | Ivan + `peitho-language-quality`    | Need structured editorial calendar               |
| 5.4  | Academic Liaison                    | 🟡 T2 | ❌ Missing | None                                | Activate when first paper submitted              |
| 5.5  | Citation / Bibliography Specialist  | 🟢 T1 | 🟡 Partial | `citation-checker` (15% coverage)   | Coverage % too low — needs process              |
| 5.6  | Course Designer                     | 🟢 T1 | 🟡 Partial | Ivan + 12-module plan               | No Hero's-Journey framework yet                 |
| 5.7  | Course Producer                     | 🟡 T2 | 🟡 Partial | `course-producer` (1 module/week)   | Slow throughput — needs instructional designer  |
| 5.8  | Instructional Designer              | 🟠 T3 | ❌ Missing | None                                | Activate when course scales                      |
| 5.9  | Subject Matter Expert (SME)         | 🟡 T2 | ❌ Missing | None                                | Need SME bench (contract per-module)            |
| 5.10 | Research Engineer                   | 🟡 T2 | ❌ Missing | None                                | Activate when we need eval harnesses/data pipelines |
| 5.11 | IP / Patent Specialist              | 🟠 T3 | ❌ Missing | None                                | Activate on first patent                        |
| 5.12 | Publication Coordinator             | 🟡 T2 | ❌ Missing | None                                | Activate on first submission                    |

**Summary**: 0 fully wired, 6 partial, 6 missing/deferred.

### What's covered today

- 5.1 Research Lead — ✅ fully covered
- 5.2 Researcher — partial (Ivan + Thoth do literature scans; no experimental
  design or hypothesis testing yet)
- 5.3 Writer / Editor — partial (Ivan writes; Peitho scores language quality
  but no structured editorial workflow)
- 5.5 Citation Specialist — partial (agent exists; coverage % is the gap)
- 5.6 Course Designer — partial (curriculum exists; pedagogical framework TBD)
- 5.7 Course Producer — partial (1 module/week; throughput is the constraint)

### What we need to add (priority order)

| Priority | Role                | Trigger to activate                                  | Effort to build |
|---------:|---------------------|------------------------------------------------------|-----------------|
| P1       | 5.5 Citation Spec. (deepen) | This quarter — coverage is at 15%                  | 1 agent, 1 policy |
| P2       | 5.7 Course Producer (scale)  | When 2nd module/week needed                          | 1 sub-agent (instructional designer) |
| P3       | 5.3 Writer / Editor (process) | When 2nd publication cadence starts                  | 1 editorial calendar |
| P4       | 5.10 Research Engineer        | When thesis-to-product eval harness needed           | 1 agent + eval harness |
| P5       | 5.12 Publication Coordinator  | When first paper submitted                          | 1 agent + submission tracker |
| P6       | 5.4 Academic Liaison          | Same as P5                                           | Same as P5       |
| P7       | 5.9 SME bench                 | When 5+ course modules need external expertise      | 1 contract template |
| P8       | 5.8 Instructional Designer    | When course scales past 2 modules/month              | 1 sub-agent |
| P9       | 5.11 IP / Patent              | On first patent trigger                              | External counsel |

---

## 3 — Sub-agents inventory (4 wired + 4 cross-cut)

### Tier-1 sub-agents (4)

| Agent                | Cadence         | Hard-stops                       | Class   | Status  |
|----------------------|-----------------|----------------------------------|---------|---------|
| `research-tracker`   | Weekly Sun 21:00 UTC | publish_paper, submit_arxiv, etc. | FULL_AGENT | WIRED |
| `citation-checker`   | Daily           | same                              | FULL_AGENT | WIRED (15% coverage) |
| `course-producer`    | Daily           | same                              | FULL_AGENT | WIRED (1 module/week) |
| `thesis-tracker`     | Daily           | same                              | FULL_AGENT | WIRED |

### Cross-cutting demiurge agents that feed Research (4)

| Agent                          | Atomic layer | Feeds              | Status  |
|--------------------------------|--------------|--------------------|---------|
| `thoth-literature-scanner`     | atomic       | Research + Sales + Marketing | WIRED |
| `hephaestus-document-miner`    | atomic       | Research + Sales   | WIRED |
| `peitho-language-quality`      | atomic       | Research + Sales   | WIRED |
| `mnemosyne-document-archivist` | atomic       | Research (memory)  | WIRED |

**Total**: 8 agents directly serving the Research dept today.

### What's missing in agent layer

- **Editorial workflow agent** — draft → peer-review → final pipeline
- **Eval harness builder** (Research Engineer role) — automates quality checks
- **Publication tracker** — submission status per paper
- **Academic venue matcher** — recommend journals/conferences per finding
- **Source-materials scorer** — 4-dim scoring (currently informal)

---

## 4 — Areas of responsibility (the 7 functional areas)

A fully-staffed research dept covers **7 functional areas**. Today's coverage:

### 4.1 — Thesis & long-form research

**Owner**: Ivan + thesis-tracker
**Output**: GeoData v2 chapters
**Cadence**: long-cycle (6-12 months per chapter)
**Coverage**: 🟡 70% (chapter production wired; defense prep missing)

### 4.2 — Course & curriculum

**Owner**: Ivan + course-producer
**Output**: 12-module coaching track
**Cadence**: medium-cycle (1 module/week, need 2/week)
**Coverage**: 🟡 50% (curriculum designed; production throughput is gap)

### 4.3 — Citation & reference management

**Owner**: citation-checker
**Output**: coverage % + orphan refs flagged
**Cadence**: daily scan + monthly audit
**Coverage**: 🟡 15% overall, 70% in `research/` — major gap

### 4.4 — Source-materials curation

**Owner**: source-curator (cross-cut from Operations) + research-tracker
**Output**: 4-dim scorecard per file
**Cadence**: monthly sweep + on-new-file
**Coverage**: 🟡 Policy designed; scoring not yet automated

### 4.5 — Peer review & quality gates

**Owner**: Ivan (human reviewer) + peitho-language-quality (auto)
**Output**: per-artifact acceptance log
**Cadence**: on-event (per draft)
**Coverage**: 🟢 Process designed (3 steps); step 2 (peer) needs named reviewers

### 4.6 — Publication pipeline (deferred)

**Owner**: DEFERRED
**Output**: submission tracker, embargo manager, venue matcher
**Cadence**: on-event
**Coverage**: ❌ Activates on first paper

### 4.7 — Knowledge backbone (cross-dept)

**Owner**: mnemosyne-document-archivist + thoth
**Output**: institutional memory + literature catalogs
**Cadence**: continuous
**Coverage**: 🟢 Wired

### Coverage summary

| Area                    | Today | Target (fully staffed) | Gap |
|-------------------------|-------|------------------------|-----|
| Thesis & long-form      | 70%   | 90%                    | Defense prep automation |
| Course & curriculum     | 50%   | 80%                    | Production throughput   |
| Citation & references   | 15%   | 80%                    | Coverage % (priority #1)|
| Source-materials        | 50%   | 85%                    | Automated scoring       |
| Peer review & quality   | 80%   | 95%                    | Named reviewers         |
| Publication pipeline    | 0%    | 80%                    | Whole area              |
| Knowledge backbone      | 85%   | 95%                    | Cross-repo linking      |

---

## 5 — Setup checklist (what "fully staffed" means concretely)

### People (12 roles) — see §2

### Tools (8 tool categories)

| Tool              | Today           | Need                          |
|-------------------|-----------------|-------------------------------|
| Reference manager | None            | Zotero or Paperless (when 50+ refs) |
| Citation checker  | `citation-checker` | Already wired              |
| Literature scanner| `thoth`         | Already wired                 |
| LaTeX / paper writer | Ivan uses VSCode | Overleaf (when collaborating) |
| Course authoring  | Markdown + manual | Authoring tool (TBD)         |
| Source catalog    | Markdown YAML   | Database (when 500+ files)    |
| Peer-review platform | None          | GitHub PRs (current workflow) |
| Submission tracker | None           | Spreadsheet → DB when active  |

### Processes (5 processes)

| Process                 | Status      | Owner            |
|-------------------------|-------------|------------------|
| Citation discipline     | Designed    | citation-checker |
| Peer review (3-step)    | Designed    | Ivan             |
| Source-materials scoring| Designed    | source-curator   |
| Editorial calendar      | Missing     | TBD              |
| Submission workflow     | Missing     | TBD              |

### Artifacts (5 deliverables)

| Artifact                  | Today          | Target              |
|---------------------------|----------------|---------------------|
| Thesis chapters           | In progress    | 6 chapters by Q2 2027 |
| Course modules            | 1/wk           | 2/wk by Q4 2026     |
| Citation coverage %       | 15%            | 80% by Q4 2026      |
| Source-materials scorecard| Missing        | Monthly from Q3 2026 |
| Publication pipeline      | Missing        | 1 paper submitted by Q2 2027 |

### Cadences (we already run 5)

- Sun 21:00 UTC — research-tracker weekly
- Daily — citation-checker, course-producer, thesis-tracker
- Monthly — coverage rollup
- Quarterly — liaison targets
- On-event — chapter/module reviews

---

## 6 — Best-practice reading list

### Books (the canonical org-design canon)

| Book                                  | Author(s)                   | Why it matters for Research            |
|---------------------------------------|------------------------------|---------------------------------------|
| *Team Topologies*                      | Skelton + Pais (2019)        | Org-design vocabulary; we use stream-aligned + enabling |
| *Accelerate*                          | Forsgren, Humble, Kim (2018) | DORA metrics; applies to thesis pipelines too |
| *Site Reliability Engineering*        | Beyer et al. (Google, 2016) | SLO/error-budget thinking applies to research quality |
| *The Phoenix Project*                 | Kim (2013)                  | DevOps culture; relevant for research-ops |
| *Research Methodology* (any methods text) | Creswell, etc.            | For thesis design rigor                |
| *How to Write a Thesis*               | Eco (1977)                  | Thesis chapter structure (long-form)    |
| *The Craft of Research*               | Booth, Colomb, Williams     | Research-question framing              |

### Papers & frameworks

| Source                                | Relevance                                    |
|---------------------------------------|-----------------------------------------------|
| **OWASP GenAI LLM Top 10 2026**       | When AI agents write research outputs         |
| **EU AI Act 2026 (in force 2026-08-02)** | Required governance for AI-generated research  |
| **MIT Career Ladders (2023)**         | Defines Research Scientist / Research Engineer roles precisely |
| **Meta FAIR job specs**               | Concrete role descriptions for AI research orgs |
| **Google DeepMind careers page**      | Defines Research Engineer vs Research Scientist distinction |
| **Accelerate / DORA 2024 report**     | Throughput + stability metrics — applies to research cadence |
| **Team Topologies book (Skelton/Pais)** | Org-design vocabulary                        |
| **12-Factor Agent methodology**       | AI agent deployment practices (we use v0.2.0) |
| **ASTELD (2026)**                     | 6-axis agent classification                  |

### Online resources

| Resource                              | URL                                              |
|---------------------------------------|--------------------------------------------------|
| arXiv (open access preprints)         | https://arxiv.org                                |
| Google Scholar                        | https://scholar.google.com                       |
| Connected Papers (citation graph)     | https://www.connectedpapers.com                   |
| Semantic Scholar                      | https://www.semanticscholar.org                  |
| DORA                                  | https://dora.dev                                 |
| OWASP GenAI                           | https://genai.owasp.org                           |
| SRE book (free online)                | https://sre.google/sre-book/table-of-contents/   |
| Team Topologies                       | https://teamtopologies.com                        |

### In-repo references (already canonical)

| Path                                                                          | Purpose                       |
|-------------------------------------------------------------------------------|-------------------------------|
| `research/org-design-literature.md`                                           | Org-design synthesis (20+ sources) |
| `research/DEPT-RESEARCH-METHODOLOGY.md`                                       | 7-question pattern for research |
| `research/30-research-areas.md`                                               | Org-wide research agenda        |
| `docs/ROLES-INVENTORY.md`                                                     | 135-role canonical roster       |
| `departments/ORG-AGENTS.md`                                                   | Constitution                   |
| `departments/05-research-education.md`                                        | **THIS dept's charter (v0.1.0)** |
| `departments/04-engineering-delivery.md`                                      | Sibling charter for reference   |
| `research/dept-research/05-research-education-research-areas.md`               | v1 catalog (8 areas)            |

### Skills (existing)

| Skill                                  | Used by                                |
|----------------------------------------|----------------------------------------|
| `~/skills/arxiv/`                      | thoth-literature-scanner               |
| `~/skills/grounded-citations/`         | citation-checker + every AI writer     |
| `~/skills/llm-wiki/`                   | research-tracker                       |
| `~/skills/source-curator-freshness/`   | source-curator                         |

---

## 7 — Recommended agent additions (concrete adoption plan)

### Priority 1 — `citation-coverage-enforcer` (Q3 2026)

**Why**: Coverage at 15% is the #1 gap (per dept-research v1 HOT area #1).
**Class**: FULL_AGENT, daily
**Function**: Force every new doc in `wizard-academy/`, `satellite-paraguay/`,
`courses/`, `company/Company/marketing/` to have verified citations before
git-merge. Blocks merge with 0 unverified citations.
**Estimated build**: 1 PROMPT.md + 1 policy + 1 git-hook = 4 hours.

### Priority 2 — `instructional-designer` (Q4 2026)

**Why**: Course throughput is the bottleneck; need pedagogy framework + assets.
**Class**: FULL_AGENT, weekly
**Function**: Apply Hero's-Journey framework to module design; produce
learning objectives + assessments per module.
**Estimated build**: 1 PROMPT.md + 1 framework doc = 6 hours.

### Priority 3 — `editorial-calendar-keeper` (Q4 2026)

**Why**: No structured publishing cadence; everything ad-hoc.
**Class**: CRON_WORKFLOW (no LLM), weekly
**Function**: Tracks what's due, what's in review, what's published.
**Estimated build**: 1 cron job + 1 SQLite schema + 1 dashboard = 3 hours.

### Priority 4 — `publication-pipeline-manager` (Q2 2027)

**Why**: First paper submission triggers the whole pipeline.
**Class**: HITL_AGENT (Ivan approves every submission)
**Function**: Submission status per paper, embargo management, venue matcher.
**Estimated build**: 1 PROMPT.md + 1 tracker DB = 1 day.

### Priority 5 — `eval-harness-builder` (Q2 2027)

**Why**: Research Engineer role activates when thesis-to-product eval needed.
**Class**: FULL_AGENT, on-demand
**Function**: Build automated eval harnesses for any thesis finding that graduates
to product (per thesis-to-product-path.md).
**Estimated build**: 2 days for first harness, then reusable.

---

## 8 — Conclusion & next steps

**Today's state**: 4 wired agents + 4 cross-cut atomics + 5 T1 roles covered
partially + 12 research areas (8 v1 + new ones from this doc).

**Fully-staffed state**: 9 wired agents + 12 T1+T2 roles fully covered + 50+
research areas + 80% citation coverage + 2 modules/week + 1 submitted paper.

**Gap**: 6 of 12 roles missing, 6 partially covered, 5 agent additions needed.

**Recommended next step (Ivan approval)**:
1. Ratify the new charter `departments/05-research-education.md` (just written)
2. Build Priority 1 — `citation-coverage-enforcer` (4 hours, biggest ROI)
3. Re-audit this catalog in 60 days

---

**Document path**: `/opt/data/agents/research/dept-research/05-research-education-research-areas-v2.md`
**Last updated**: 2026-09-01
**Author**: Per Phase 7 plan (research deepening), Ivan approval pending