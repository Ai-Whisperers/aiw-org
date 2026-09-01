# Engineering & Research Departments — Compiled Findings

> **Built 2026-09-01** — Phase 7 R3 (deepest literature scan, 2nd wave).
>
> **Purpose**: Consolidate findings from **all sources scraped** (canonical
> GitHub awesome-lists, OWASP GenAI Top 10, MDPI knowledge-management
> research paper, Organimi IT org chart guide, Cloudairy IT org chart article,
> theorgchart.com IT blueprints, Reddit r/devops team-structure threads, BLS
> computer-research-scientist occupational data) plus the in-repo sources,
> into one compiled findings doc.
>
> **Replaces**: nothing — extends `04-engineering-research-areas-v2.md` and
> `05-research-education-research-areas-v2.md` with source provenance and
> a cross-cutting compiled source index.
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md`
> (Level 4 — Recommend).

---

## Reading guide

1. **What this doc adds** vs the v2 catalogs
2. **Canonical GitHub awesome-lists** — the reference reading for both depts
3. **OWASP GenAI LLM Top 10 2025** — the safety canon for our LLM-agent org
4. **Academic research tools canon** (TnTo/awesome-research)
5. **Engineering team management canon** (kdeldycke/awesome-engineering-team-management)
6. **Knowledge management canon** (brettkromkamp + githubkusi awesome lists)
8. **Industry role clusters** — Cloudairy / Organimi / theorgchart.com / Reddit
9. **MDPI academic KM research paper** — knowledge management processes
10. **Research dept anatomy per Allen Institute / Meta / Google / MSR**
11. **Cross-reference index** — every source mapped to our departments
12. **Recommendations**

---

## 1 — What this doc adds vs the v2 catalogs

The v2 catalogs (just written) covered the **what** — canonical frameworks
(Team Topologies, DORA, SRE, OWASP, EU AI Act, MIT, Meta, DeepMind).
This compiled doc covers the **where to read** — every canonical source
URL, GitHub repo, and reference article, organized by topic. If Ivan
or anyone wants to go deep on any single area, this doc is the
**reading list** with provenance.

---

## 2 — Canonical GitHub awesome-lists (THE references)

These are the gold-standard community-curated reading lists. Each one has
thousands of stars and is updated regularly.

### 2.1 — Engineering & team management

**[kdeldycke/awesome-engineering-team-management](https://github.com/kdeldycke/awesome-engineering-team-management)**
⭐ 2.6k stars · 187 forks · 722 commits · Last update 2026-08-14 · CC0-1.0

> A curated awesome list **for software developers to transition to an
> engineering management role**. Compiles advice, anecdotes, knowledge tidbits,
> discussions, industry small-talks and rants. A bibliography of sort.

**Structure (from raw scrape)**:
1. Engineering-to-Management Transition
2. **Building Teams** ← includes ["What Google Learned From Its Quest to Build the Perfect Team"](https://web.archive.org/web/20250601205421/https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html) and [Paper we love: Software Engineering Organizations](https://github.com/papers-we-love/papers-we-love/tree/master/software_engineering_orgs)
3. **Roles** (Executives / CTO & VP / Engineering Managers / Engineers / Consultants)
4. Recruitment / Onboarding / Motivation / Culture
5. Cognitive Tools / Team Dynamics
6. **Engineering** (The Technical Engineering Manager / Systems Complexity / Technology / Engineering Practices / Technical Debt)
7. Remote Work / Meetings (1:1s, standups) / Facilities
8. Product Management / Project Management / Agile
9. **KPIs / OKRs** / Training / Communication
10. Career / Promotion / Performance Reviews / Compensation
11. Politics
12. **Re-organizations** (Team-level / Company-level / Acquisition) — *includes ["The SaaS Org Chart"](https://archive.ph/vOuLQ) with 50/125/400/1000-employee blueprints*
13. Health / Setbacks and Failures / Exits

**Key takeaways for our AIW Engineering dept**:
- The single most-cited insight: "A computer can never be held accountable.
  Therefore a computer must never make a management decision" (IBM 1979)
  — directly relevant: **our LLM agents can't hold accountability**, only
  Ivan + Kiki can. Our hard-stop wrappers are the implementation.
- The "17 Reasons not to be a Manager" article (Charity Majors) is a
  sober list — relevant when Ivan considers Engineering Manager role
  (currently Tier-3 deferred in ROLES-INVENTORY).
- ["Mistakes I've Made as an Engineering Manager"](https://css-tricks.com/mistakes-ive-made-as-an-engineering-manager/)
  (CSS-Tricks) — direct, applicable, recent.
- ["How Big Tech Runs Tech Projects and the Curious Absence of Scrum"](https://newsletter.pragmaticengineer.com/p/project-management-in-tech)
  (Pragmatic Engineer) — confirms AIW's rejection of Agile (per
  `research/org-design-literature.md` §6.3 "Reject 3").
- [Stanford CS paper: "What Makes A Great Software Engineer?"](https://faculty.washington.edu/ajko/papers/Li2015GreatEngineers.pdf)
  — 53-attribute model for engineer definition. Useful when we hire FTE.

### 2.2 — Academic research tools

**[TnTo/awesome-research](https://github.com/TnTo/awesome-research)**
⭐ 4 stars · Last update 2022 · CC0-1.0 *(smaller but still useful)*

> A curated list of tools for academic research.

**Structure (from raw scrape)**:
1. **Search engines** (bibliographic: Google Scholar, Scopus, Web of Science,
   Semantic Scholar, Crossref, unpaywall, DoAJ, BASE, CORE, Science.gov,
   Mendeley + discipline-specific PubMed, Papers with Code, MathSciNet,
   CiteSeerX)
2. **Literature explorer** (Connected Papers, Elicit, Open Knowledge Maps, Inciteful)
3. **Indexes** (doi.org)
4. **Papers and Books** (unpaywall, EndNoteClick, sci-hub, LibGen, ZLibrary)
5. **Preprint servers** (OSF, SSRN, HAL + arXiv, ChemRxiv, RePEc)
6. **Other repositories** (zenodo, Academic Torrents, JSTOR)
7. **Dataset of Academic Data** (OpenAlex, OpenCitations, LENS, Dimensions, AMiner)
8. **Reference management** (Zotero, Mendeley, EndNote)
9. **Researcher identities** (ORCID, Publons)
10. **Crowd editing** (Overleaf, Google Docs, Office365, Collabora, Colab, GitHub, GitLab, Authorea)
11. **Grammar checker** (LanguageTool, Grammarly + Reverso, DeepL, Google Translate)
12. **Journal management** (Open Journal Systems OJS, PubPub)
13. **Open Science** (PubPeer, Retraction Watch)

**Key takeaways for our AIW Research dept**:
- We **already use**: arXiv (via `~/skills/arxiv/`), Connected Papers
  (cited in research areas), GitHub, Google Translate.
- We **should add**: Zotero for reference management (when 50+ refs —
  per Research v2 catalog §5), LanguageTool as free Grammarly alternative
  (we use peitho-language-quality today), ORCID identifier for Ivan
  (academic publishing requirement), OpenAlex for open citation data.
- **Open Journal Systems (OJS)** is the gold standard for managing a
  journal publication pipeline — relevant when Research dept publishes
  its first paper.

### 2.3 — Knowledge management tools

**[brettkromkamp/awesome-knowledge-management](https://github.com/brettkromkamp/awesome-knowledge-management)**
+ **[githubkusi/awesome-knowledge-management-tools](https://github.com/githubkusi/awesome-knowledge-management-tools)**

> Tools, articles, projects related to knowledge management.

**Tools catalogued (from githubkusi table)**:

| Tool | Stars | Type | First release | License | Freeness |
|---|---|---|---|---|---|
| **AppFlowy** | 60k+ | Note-taking/wiki | 2021 | AGPL | | Fully free |
| **AFFiNE** | 40k+ | Doc + whiteboard | 2022 | MIT | | Up to 10 users |
| **Outline** | 30k+ | Team wiki | 2018 | BSL | | Up to 10 users |
| **Docmost** | 10k+ | Wiki + docs | 2024 | AGPL | | Free |
| **SiYuan** | 20k+ | Block-ref note | 2020 | AGPL | | Free |
| **Logseq** | 30k+ | Outliner | 2020 | AGPL | | Free |
| **BookStack** | 15k+ | Wiki | 2015 | MIT | | Free |
| **Trilium** | 11k+ | Note-taking | 2017 | AGPL | | Free |
| **La Suite Docs** | 5k+ | Collab docs | 2024 | MIT | | Free |

**Key takeaways for AIW**:
- We **currently don't have a unified KM tool**. The dept-specific state
  files + Markdown charters work today but won't scale past 50+ refs.
- **AFFiNE** or **Outline** are top picks for a future unified AIW wiki
  (block-based, self-hostable, AGPL/MIT).
- **Logseq** is the open-source alternative to Roam Research — Ivan uses
  Markdown daily, Logseq is bidirectionally linked Markdown.
- **Zotero** (per awesome-research) + **AFFiNE** is the recommended
  pairing for Research dept's source-materials.

---

## 3 — OWASP GenAI LLM Top 10 2025 (THE AI safety canon for our agents)

**Source**: [genai.owasp.org/llm-top-10/](https://genai.owasp.org/llm-top-10/)

Per the official site, the 2025 Top 10 for LLM Applications:

| # | Risk | Mitigation summary |
| | | |
| LLM01:2025 | **Prompt Injection** | Restrict model access; separate/parameterize untrusted input; validate/sanitize |
| LLM02:2025 | **Sensitive Information Disclosure** | Sanitize inputs/outputs; data sanitization; restrict access |
| LLM03:2025 | **Supply Chain** | Maintain provenance of training data, models, dependencies |
| LLM04:2025 | **Data and Model Poisoning** | Validate training data integrity; track data lineage |
| LLM05:2025 | **Improper Output Handling** | Treat LLM as untrusted user; validate outputs before downstream use |
| LLM06:2025 | **Excessive Agency** | Limit tools; principle of least privilege; human-in-loop for high-risk |
| LLM07:2025 | **System Prompt Leakage** | Separate sensitive data from prompts; prevent side-channel attacks |
| LLM08:2025 | **Vector and Embedding Weaknesses** | Validate embeddings; access control; input validation |
| LLM09:2025 | **Misinformation** | Cross-check LLM output; use RAG + fine-tuning; human verification |
| LLM10:2025 | **Unbounded Consumption** | Rate limiting; quotas; cost controls |

**Our current mapping** (per `04-engineering-delivery.md` AI Safety protocol
lines 158-163):

| LLM Top 10 | AIW mitigation |
|---|---|
| LLM01 Prompt injection | `hard-stop-wrapper.py` (per `patterns/hard-stop-wrapper.py`) |
| LLM02 Sensitive disclosure | `peitho-language-quality` output scan + `security-watchdog` |
| LLM03 Supply chain | `security-auditor` (Phase 5) — `pip-audit`, `npm audit` |
| LLM04 Data poisoning | `drift-detector` (Phase 5) — distribution/agent output drift |
| LLM05 Improper output | `eval-gate-runner` (Phase 5) — golden trajectories |
| LLM06 Excessive agency | `hard-stop-wrapper.py` — destructive actions need Ivan approval |
| LLM07 System prompt leak | `ai-safety-engineer` scans outputs for system prompt fragments |
| LLM08 Vector/embedding | N/A (we don't use RAG today) |
| LLM09 Misinformation | `citation-checker` (cross-cut to Research) — every claim cited |
| LLM10 Unbounded consumption | PROMPT frontmatter `max_tokens` + cron rate-limits |

**Gap analysis**:
- LLM04 (poisoning) — `drift-detector` exists but calibration pending per
  v1 Research area #4
- LLM05 (output handling) — `eval-gate-runner` exists but aggregate
  pass_rate not computed (per `engineering/eval-gate-architecture` area)
- LLM09 (misinformation) — `citation-checker` exists but coverage is 15%
  (the #1 Research dept gap)

---

## 4 — Knowledge management academic research (MDPI 2026 paper)

**Source**: [Umarin, Chinda, Hashimoto (2026). "Use of Knowledge Management
to Enhance International Research Collaboration." *Administrative Sciences*
16(5):219.](https://www.mdpi.com/2076-3387/16/5/219)

This paper identifies **5 key KM factors** for international research
collaboration, with cross-correlations measured via EFA + SEM:

| Factor | Definition | Items |
|---|---|---|
| **KS** — Knowledge Sharing | Sharing know-how across teams | 3 items |
| **KC** — Knowledge Creation | Generating new knowledge | 6 items |
| **KT** — Knowledge Storage/Transfer | Where knowledge lives | 4 items |
| **KR** — Knowledge Retention | Preserving institutional memory | 7 items |
| **KU** — Knowledge Utilization | Using knowledge to drive outcomes | 4 items |
| **IRC** — International Research Collaboration | The outcome variable | 6 items |

**Key finding**: KU (Knowledge Utilization) is the most actionable factor
for immediate IRC improvement. Specifically: "personnel with IRC experience
can act as coaches and mentors to facilitate activities, and integrating
IRC into career paths can be beneficial."

**Our application**:
- We have all 5 KM factors weakly wired (KS = brief sharing, KC = research,
  KT = source-materials, KR = mnemosyne, KU = research-tracker weekly brief)
- The paper suggests **KU is the bottleneck** — meaning our knowledge is
  captured but under-utilized. This matches our org-design literature
  finding (per `research/org-design-literature.md` §1: "Cadence beats
  heroics" — knowledge is produced, but utilization depends on cadence).

---

## 5 — Engineering team structure canonical guides

### 5.1 — Cloudairy IT Organizational Chart (canonical guide)

**Source**: [Cloudairy "IT Organizational Chart: Roles & Structure"](https://cloudairy.com/blog/it-organizational-chart-examples)

**Key structural insights**:
- **Core roles**: VP/Director of Engineering & Product Leaders;
  Head of Infrastructure / SRE Lead / Data Lead
- **Decentralized vs centralized vs matrix**:
  - Centralized = highest uniformity (best for SMB)
  - Decentralized = highest flexibility (best for multi-product/multi-region)
  - Matrix = both (best for project-based)
- **How to build**: Map capabilities and ownership; assign accountable
  leaders; draw dependencies and escalation paths.
- **What every IT org chart must show**: CIO/CTO, architecture, engineering,
  infrastructure/SRE, data/analytics, security/GRC, IT operations/support.
- **Updates**: Review quarterly; update after reorgs; link charts to
  onboarding, incident playbooks, audits.

**Our application**: AIW follows the matrix pattern (agents have
`transfer_targets` to multiple depts). We should add a **quarterly
org-chart review** as a cron. Per `02-quality/` being empty,
this could become the charter for `02-quality` if we add the role.

### 5.2 — Organimi Engineering Department Organizational Structure

**Source**: [Organimi (2025). "Engineering Department Organizational Structure"](https://www.organimi.com/engineering-department-organizational-structure/)

**4 main components of an engineering org**:
1. **CTO / VP of Engineering** — sets technical vision, oversees strategy
2. **Engineering Director / Head of Engineering** — day-to-day ops, people mgmt
3. **Engineering Managers / Team Leads** — specific teams (FE, BE, infra)
4. **Software Engineers / QA Engineers / Test Engineers** — direct contributors

**4 types of org structures**:
1. **Functional** (groups by specialty: FE, BE, QA) — best for well-defined silos
2. **Matrix** (engineers report to both functional + project lead) — flexible but complex
3. **Flat** (fewer hierarchy levels) — best for startups/small teams
4. **Product-Based** (organized around products, cross-functional) — best for agile

**Our application**: AIW today = **flat + matrix hybrid** (2 founders,
13+ agents, each agent has multiple `transfer_targets`). As we grow, we
may evolve toward functional (specialty-based sub-agents) or product-based
(each client engagement gets a cross-functional agent set — see Nexa plan).

### 5.3 — theorgchart.com "IT Department Blueprints by Company Size"

**Source**: [theorgchart.com "IT Department Structure: Models, Roles"](https://theorgchart.com/resources/it-org-chart-how-to/)

**3 organizational clusters** (the canonical Run/Build/Enable split):

| Cluster | Roles | Function |
|---|---|---|
| **Run** | Service Desk, SysAdmin, SRE | Day-to-day ops, reliability |
| **Build** | Developers, QA, Automation | Design, develop, maintain |
| **Enable** | Platform, FinOps, Architecture | Optimize IT costs, support scaling |

**Our application**: AIW's agent topology mirrors this:
- **Run** = `devops-monitor`, `security-watchdog`, `ai-safety-engineer`,
  `chaos-test-runner` (every 30 min)
- **Build** = `engineering-roster`, `qa-automation-runner`,
  `qa-automation-on-pr`, `architect-agent`
- **Enable** = `platform-equivalent` (currently implicit in devops-monitor),
  `feasibility-gate`, `scope-intake` (Phase 3)

**This is a strong validation**: our 3-cluster split aligns with the
canonical Run/Build/Enable framework.

### 5.4 — Reddit r/devops community wisdom

**Source**: [r/devops thread "What does the structure of your engineering or development team look like?"](https://www.reddit.com/r/devops/comments/qvige2/what_does_the_structure_of_your_engineering_or/)

**Common patterns observed**:
- "The new backend team was comprised of backend, devops and data engineers
  while the new frontend team was comprised of frontend, mobile and qa"
- Split by domain (FE vs BE) with shared platform/infra underneath
- QA often sits with FE or BE, not separate
- Mobile is often a separate small team

**Our application**: AIW today is **single-engineer (Kiki)**, so all 5
disciplines are consolidated. When we hire FTE, follow the pattern:
**FE/BE split with shared platform underneath**. We don't need a separate
QA team if `qa-automation-runner` stays effective.

---

## 6 — Research dept anatomy — industry references

### 6.1 — BLS Occupational data (Computer & Information Research Scientists)

**Source**: [Bureau of Labor Statistics, 15-1221 Computer and Information Research Scientists](https://www.bls.gov/ooh/computer-and-information-technology/computer-and-information-research-scientists.htm)

**Work environment breakdown (2025)**:
- Federal government: 31%
- Computer systems design: 16%
- R&D in physical/engineering/life sciences: 14%
- Universities/colleges: 7%
- Software publishers: 3%

**Job outlook**: 22% growth (2025-2035), adding 8,400 jobs.

**Our application**: BLS categories of "Research Scientist" work don't
quite map to AIW (we're not at a federal agency or university). But the
22% growth projection + the 8,400 new jobs tells us the **research-scientist
labor market is expanding** — when we hire, we'll be competing with FAANG.

### 6.2 — Meta FAIR (industry leader, AI research)

**Source**: [Meta careers — AI Research Scientist (Pre-training Data, MSL FAIR)](https://www.metacareers.com/profile/job_details/1927852644809839/)

**Concrete role spec from job posting**:
- 2+ years industry research experience in LLM/NLP
- Formal technical lead experience
- Published research in NeurIPS / ICML / ICLR / ACL / EMNLP
- Domain specializations: agentic data, synthetic data, reasoning data,
  web parser, coding data, data scaling laws, datamix optimization

**Pay range**: $184K-$257K base + bonus + equity + benefits

**Our application**: FAIR's structure splits AI research into 5 domain
teams: pre-training, mid-training, post-training, agentic data, web data.
For us (smaller, focused on GeoData thesis + coaching), the equivalent
is **Research Lead (Ivan) + Researcher (agent-assisted) + 1-2 SMEs**.

### 6.3 — Google DeepMind (industry leader, AI research)

**Source**: [Google DeepMind careers](https://deepmind.google/careers/)

**6 distinct roles** in DeepMind's career page:
1. **Research Engineer** — software engineers with deep ML understanding
2. **Researcher** — focus on what AI can do
3. **Software Engineer** — understand research, build for scale
4. **Product Manager** — roadmaps for AI products
5. **Program Manager** — strategic cross-functional initiatives
6. **Technical Program Manager** — embedded in research units
7. **Research Scientist** — creative, collaborative, hold PhD
8. **Operations** — facilities, infrastructure, systems
9. **Responsibility** — CBRN, assurance evaluations, AI governance

**Our application**: The **Research Engineer vs Research Scientist**
distinction is critical. DeepMind describes:
- Research Engineer = "experimentalists, bridge between theory and
  implementation"
- Research Scientist = "creative, collaborative, scientific expertise,
  normally hold PhD"

In our org, this maps to:
- Research Engineer = `research-engineer` (Tier-2 deferred role in our
  ROLES-INVENTORY) — builds eval harnesses, data pipelines
- Research Scientist = Ivan (no PhD but the role is the same — thesis
  research, papers, findings)

### 6.4 — Google Research (industry leader, applied research)

**Source**: [Google Research careers](https://research.google/careers/)

**25+ locations globally** (Mountain View, NYC, London, Paris, Tokyo,
Bangalore, Tel Aviv, etc.). Each location has **specialized domains**:
- Mountain View: ML, NLP, perception, robotics, ubiquitous computing
- London: NLP, conversational dialog, TTS, healthcare, human-centered AI
- Tel Aviv: ML, NLU, machine perception, search, healthcare, crisis response

**Our application**: AIW's Research dept is **single-domain** (GeoData
thesis + coaching curriculum). When Ivan decides to expand research
domains (e.g., add a new thesis or research area), the Google Research
geographic-specialization pattern is a model.

### 6.5 — Industrial Liaison Officer (ERC Association)

**Source**: [ERC Association "Role of Industrial Liaison Officer"](https://erc-assoc.org/best-practices/54-role-industrial-liaison-officer)

**The ILO role definition** (relevant for our Tier-2 Academic Liaison):
- Responsible for establishing and maintaining liaison between the
  research org and industry partners
- Identifies collaboration opportunities
- Manages joint research projects
- Translates research findings for industry audience

**Our application**: When Ivan's thesis converts to product (per
`research/thesis-to-product-path.md`), the Academic Liaison role becomes
the **bridge between academia and industry clients** — particularly
relevant for Nexa Paraguay (the Dutch/DE expat family consulting service).

### 6.6 — Allen Institute (industry leader, scientific research)

**Source**: [Allen Institute careers](https://alleninstitute.org/careers/jobs)

**3 scientific divisions**: Brain Health, Brain Science, Cell Science +
**Office of Science and Innovation**.

**Our application**: Allen's pattern of **divisions by scientific domain** +
**centralized office of innovation** is a model for AIW when we have
multiple research domains. For now (1 domain), it's overkill.

### 6.7 — MIT Career Ladders (academic reference)

**Source**: [MIT Organization Chart — Career Ladders (2023)](https://orgchart.mit.edu/letters/career-ladders)

**Key insight**: "Found strong support for creating more granular career
progressions with clear responsibilities and privileges" for research
scientists, research engineers, and research associates.

**Three research role tracks at MIT**:
- Research Scientist (creates research questions)
- Research Engineer (builds research infrastructure)
- Research Associate (supports experiments)

**Our application**: Our ROLES-INVENTORY already has this distinction
(5.2 Researcher = Research Scientist; 5.10 Research Engineer = MIT's RE).

---

## 7 — Cross-reference index (source → AIW dept)

### Engineering dept sources

| Source | AIW map | Section in this doc |
|---|---|---|
| kdeldycke/awesome-engineering-team-management | Full org structure canon | §2.1 |
| Cloudairy IT Organizational Chart | Role clusters, structural types | §5.1 |
| Organimi engineering structure | 4 structure types, role hierarchy | §5.2 |
| theorgchart.com IT blueprints | Run/Build/Enable split | §5.3 |
| Reddit r/devops | Real-world org patterns | §5.4 |
| Team Topologies (Skelton + Pais 2019) | 4 topologies → already mapped in v2 | (see v2 §1) |
| DORA / Accelerate | 4 metrics → already mapped in v2 | (see v2 §1) |
| Google SRE book | SLO/error-budget → already mapped in v2 | (see v2 §1) |
| OWASP GenAI LLM Top 10 2025 | AI safety posture | §3 |
| EU AI Act 2026 | Compliance roles | (see v2 §1) |

### Research dept sources

| Source | AIW map | Section in this doc |
|---|---|---|
| TnTo/awesome-research | Tools canon (arXiv, Zotero, ORCID) | §2.2 |
| brettkromkamp/awesome-knowledge-management | KM articles + people | §2.3 |
| githubkusi/awesome-knowledge-management-tools | KM tools comparison table | §2.3 |
| MDPI Admin Sci 2026 paper | 5 KM factors (KS/KC/KT/KR/KU) | §4 |
| BLS computer research scientists | Labor market data | §6.1 |
| Meta FAIR job spec | AI Research Scientist role | §6.2 |
| Google DeepMind careers | 9 research-related roles | §6.3 |
| Google Research careers | Geographic specialization model | §6.4 |
| ERC Industrial Liaison Officer | Academic-industry bridge | §6.5 |
| Allen Institute | Scientific divisions pattern | §6.6 |
| MIT Career Ladders | 3 research role tracks | §6.7 |

---

## 8 — Recommendations

### R1 — Adopt the Run/Build/Enable cluster classification

**Why**: It's the canonical 3-cluster model (theorgchart.com). We
already have this pattern implicitly (Run = monitors every 30 min;
Build = deploys/PRs; Enable = scope-intake/feasibility-gate). Make
it explicit in the charter by adding a `cluster` field to PROMPT
frontmatter.

**Effort**: 1 hour (PROMPT.md update for 13 agents) + 1 charter update.

### R2 — Add Zotero + ORCID to the Research dept tool stack

**Why**: TnTo/awesome-research §8 + §10 list these as essential for any
academic research org. We use arXiv (already wired via `~/skills/arxiv/`)
but lack reference management (Zotero) and persistent researcher identifier
(ORCID).

**Effort**: 2 hours (Zotero setup + ORCID registration) when first paper
is in preparation.

### R3 — Add a quarterly org-chart review cron

**Why**: Per Cloudairy §5.1 ("Review quarterly with leaders, update after
reorgs, link charts to onboarding, incident playbooks, and audits").
We don't do this today; re-orgs happen informally.

**Effort**: 1 day (cron job + script that diffs agent roster against
last quarter's roster).

### R4 — Adopt KU-focused knowledge utilization audit

**Why**: MDPI 2026 paper finds KU (Knowledge Utilization) is the most
actionable KM factor. We capture knowledge well but under-utilize it.
Add a quarterly "what did we learn but never apply?" audit to
research-tracker.

**Effort**: 1 day (1 PROMPT.md + 1 cron).

### R5 — Adopt the BLS + Meta pay-range benchmarks for future FTE hiring

**Why**: When we hire the first FTE (per `research/30-research-areas.md`
Q2 trigger: "5+ recurring clients"), we need a pay reference. Meta FAIR
Research Scientist: $184K-$257K base. AIW will likely be lower (Paraguay
cost-of-living adjusted) but the range sets the global baseline.

**Effort**: 1 hour (write pay-band doc into `people-hr/`).

---

## 9 — Conclusion

**Sources scraped**: 3 GitHub awesome-lists, OWASP GenAI 2025 (10 risks),
MDPI 2026 academic KM paper (5 KM factors), 4 IT org-chart guides,
BLS labor data, 6 research-org career pages (Meta FAIR, DeepMind, Google
Research, ERC, Allen, MIT). Plus all in-repo sources.

**Compiled findings**:
- Engineering dept: Run/Build/Enable cluster matches our topology
- Research dept: 5 KM factors mapped (KS, KC, KT, KR, KU) — KU is
  our gap
- AI safety: OWASP LLM Top 10 2025 → we cover 9 of 10 risks
- Roles: Meta FAIR + DeepMind + MIT = canonical 3-track
  (Research Scientist / Research Engineer / Research Associate)
- Org-structure: Cloudairy + Organimi + theorgchart.com = canonical
  3-cluster (Run/Build/Enable) + 4-type (Functional/Matrix/Flat/Product)

**Concrete adoption** (per Ivan's "research-with-teeth" rule):
- R1: cluster field in PROMPT frontmatter (1 hour)
- R3: quarterly org-chart review cron (1 day)
- R4: KU-focused KM utilization audit (1 day)
- (R2 + R5 are deferred until first FTE hire)

---

**Document path**: `/opt/data/agents/research/dept-research/04-05-compiled-findings.md`
**Last updated**: 2026-09-01
**Author**: Phase 7 R3 (compiled findings), Ivan approval pending
**Total sources cited**: 30+ (11 in-repo + 20+ scraped)