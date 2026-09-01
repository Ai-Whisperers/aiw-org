# Department 5 — Research & Education

**Head**: Ivan (CEO, sole researcher today)
**Lead agent**: `research-tracker` (weekly Sun review)
**Version**: 0.1.0
**Last updated**: 2026-09-01

---

## Mission

Own the organization's knowledge backbone: thesis work (GeoData v2), course
production (12-module coaching curriculum), source-materials curation, citation
discipline, and academic liaison. Every research output is internal — there is
no external publication today, but the charter is structured so we can publish
without re-orging.

This is the dept that **builds durable IP**. Sales ships, Engineering runs,
Research captures the underlying truth.

---

## What this department owns

- **Thesis pipeline** — `satellite-paraguay/` (GeoData v2), defended-by-date
- **Course curriculum** — 12-module coaching track, Hero's-Journey-aligned
  (per `research/coaching-continuation-plan.md`)
- **Citation discipline** — coverage % across every published output
- **Source-materials curation** — `source-materials/` (300+ files, freshness +
  citation integrity)
- **Peer review** — internal 3-step review before any external submission
- **Publication pipeline** — preprints, journals, conferences (when triggered)
- **Knowledge backbone** for every other dept — Thoth (literature scanner) feeds
  Sales/Marketing/Product Discovery; Hephaestus (document miner) feeds
  Engineering & Sales; Mnemosyne (archivist) preserves institutional memory
- **Academic liaison** — submission + peer-review management (Tier-2, when
  first paper goes out)

## What this department does NOT own

- Sales copywriting / outreach (Sales — `calliope-content-producer`)
- Marketing blog/social posts (Sales — `marketing-content-producer`)
- Coaching delivery (People — `kiki-coach` in `coach-agents/` repo)
- Engineering docs / runbooks (Engineering — Tech Writer role)
- Product discovery / customer interviews (Sales — `athena-product-discovery-lead`)
- Thesis implementation code (Engineering — only when thesis graduates to product)

## Decision rights (v0.1.0)

| Action                                            | Authority                       |
|---------------------------------------------------|---------------------------------|
| Submit preprint to arXiv                          | Ivan (hard-stop)                |
| Publish course module (external)                  | Ivan + Kiki (hard-stop)         |
| Submit paper to peer-reviewed venue               | Ivan + Kiki (hard-stop)         |
| Publish blog post or LinkedIn thought-leadership  | Ivan                            |
| Mark a course module draft as "internally reviewed" | research-tracker (logged)     |
| Promote source-materials from `staging/` → `live/` | research-tracker + source-curator |
| Flag a stale citation for refresh                 | citation-checker (logged)       |
| Approve new thesis chapter for internal review    | Ivan                            |
| Edit the org's academic liaison targets list       | Ivan                            |

## Sub-roles (v0.1.0 — 12 roles from ROLES-INVENTORY.md)

The canonical roster. The 5 currently active are **T1**, the 4 Tier-2 activate
when the thesis-to-product pipeline ships, the 3 Tier-3 defer until first
academic publication.

| #    | Role                                | Tier  | Today's coverage                                |
|------|-------------------------------------|-------|-------------------------------------------------|
| 5.1  | Research Lead                       | 🟢 T1 | `research-tracker` (lead) + Ivan                |
| 5.2  | Researcher                          | 🟢 T1 | Ivan (sole) + `thoth-literature-scanner`        |
| 5.3  | Writer / Editor                     | 🟢 T1 | Ivan + `peitho-language-quality`                |
| 5.4  | Academic Liaison                    | 🟡 T2 | DEFERRED until first paper submitted            |
| 5.5  | Citation / Bibliography Specialist  | 🟢 T1 | `citation-checker` (currently 15% coverage)    |
| 5.6  | Course Designer                     | 🟢 T1 | Ivan (12-module curriculum design)              |
| 5.7  | Course Producer                     | 🟡 T2 | `course-producer` (1 module/week, scale-up)     |
| 5.8  | Instructional Designer              | 🟠 T3 | DEFERRED — pedagogy framework only when scale   |
| 5.9  | Subject Matter Expert (SME)         | 🟡 T2 | DEFERRED — contracted per-module as needed      |
| 5.10 | Research Engineer                   | 🟡 T2 | DEFERRED — eval harnesses + data pipelines      |
| 5.11 | IP / Patent Specialist              | 🟠 T3 | DEFERRED — first patent triggers activation     |
| 5.12 | Publication Coordinator             | 🟡 T2 | DEFERRED — first submission triggers activation |

**Tier breakdown**: 5 T1 active / 4 T2 deferred / 3 T3 deferred.

## Sub-agents (v0.1.0 — 4 wired)

| Agent                  | Cadence         | Class         | Owner                  |
|------------------------|-----------------|---------------|------------------------|
| `research-tracker`     | Weekly Sun 21:00 UTC | OPERATIONAL | Ivan + ai-ops-coordinator |
| `citation-checker`     | Daily           | OPERATIONAL   | ai-ops-coordinator     |
| `course-producer`      | Daily           | OPERATIONAL   | ai-ops-coordinator     |
| `thesis-tracker`       | Daily           | OPERATIONAL   | ai-ops-coordinator     |

Plus 4 cross-cutting demiurge agents that **feed** Research:
- `thoth-literature-scanner` — literature catalog updates (atomic, layer)
- `hephaestus-document-miner` — extracts entities/claims from docs (atomic)
- `peitho-language-quality` — language quality scoring (atomic)
- `mnemosyne-document-archivist` — institutional memory (atomic)

## Inputs the lead agent reads

1. `hermes cron list` filtered to Research + Education jobs
2. `state/research.json` — last brief + 4-week trend
3. `state/citation-coverage.json` — coverage % trend
4. `state/coaching-customers.json` — who consumed what course content
5. `source-materials/` catalog (via `thoth`)
6. `satellite-paraguay/` git log — thesis commits
7. `courses/` git log — course module commits
8. **NEW (2026-09-01)**: arXiv alerts for the 8 thesis-related topic feeds
   (per `~/skills/arxiv/` skill)

## Cadence (v0.1.0)

| Time               | What                                                        |
|--------------------|-------------------------------------------------------------|
| Sun 21:00 UTC      | research-tracker brief (weekly)                             |
| Daily              | citation-checker, course-producer, thesis-tracker           |
| Daily 02:00 UTC    | source-curator freshness sweep (cross-cut from Ops)         |
| Monthly            | coverage % rollup + source-materials scorecard              |
| Quarterly          | academic liaison targets refresh                            |
| On-event           | thesis chapter ready → trigger internal review              |

## Inputs vs Outputs — what flows through Research

```
INPUTS (from demiurge atomics):
  thoth-literature-scanner ──► research-tracker
  hephaestus-document-miner ─► research-tracker
  peitho-language-quality ───► citation-checker (quality score)
  mnemosyne-document-archivist ► research-tracker (memory)

OUTPUTS:
  research-tracker ─► brief (outbox) ─► Ivan + Kiki (weekly review)
  citation-checker ─► coverage % + orphan refs ─► citation-coverage-audit
  course-producer ─► module draft ─► course/* (pending Ivan+Kiki approval)
  thesis-tracker ─► chapter status ─► satellite-paraguay/* (pending approval)
```

## Stack reality

- **Thesis repo**: `/opt/data/work/research-repos/satellite-paraguay/` (private)
- **Course repo**: `/opt/data/work/research-repos/coaching-curriculum/` (private)
- **Source-materials**: `/opt/data/source-materials/` (300+ files)
- **Citation DB**: `/opt/data/state/citation-coverage.json` (live)
- **Academic liaison tracker**: `/opt/data/state/academic-targets.json` (planned)
- **Skills used**: `~/skills/arxiv/`, `~/skills/grounded-citations/`,
  `~/skills/llm-wiki/`, `~/skills/source-curator-freshness/`

## Research department doctrine (the 5 things we always do)

1. **Every claim has a citation.** Internal and external. (Per `citation-checker`
   audit: 15% coverage today, 70% in `research/`, gap is elsewhere.)
2. **Course modules are Hero's-Journey-aligned.** Per the COOL research area
   `research/hero-journey-curriculum-framework.md` (in design).
3. **Thesis chapters go through 3-step peer review** (self → peer → final)
   before they leave the repo. Per `research/peer-review-process.md`.
4. **Source-materials are scored on 4 dimensions**: freshness, validity,
   active-use, citation-integrity. Per `research/source-materials-curation-policy.md`.
5. **Internal-only by default.** Hard-stops gate any external publication.
   No `$1,500` price leaks; no trademark tokens; no premature academic claims.

## Academic liaison protocol (when activated)

Target venues per finding (per `research/academic-liaison-targets.md` plan):
- **IJGIS** (Int'l Journal of Geographical Information Science) — primary
- **CEUS** (Computers, Environment and Urban Systems) — primary
- **TGIS** (Transactions in GIS) — primary
- **AGU Fall Meeting** — conference
- **AAG Annual Meeting** — conference

Submission lead time: 6-12 months. Process design now = no scramble later.

## State schema (`state/research.json`)

```json
{
  "last_run": null,
  "thesis_chapter_status": {},
  "course_modules_completed": 0,
  "course_modules_total": 12,
  "citation_coverage_pct": 15.0,
  "source_materials_count": 312,
  "stale_source_materials": 0,
  "academic_submissions_pipeline": [],
  "next_review_at": null
}
```

## Escalation triggers

- Citation coverage drops below 10% → Ivan same-day
- Thesis chapter blocked > 7 days → Ivan + Kiki
- Course module draft un-reviewed for 14 days → course-producer retires,
  Ivan reviews why
- Source-materials freshness < 60% → source-curator sweeps immediately
- Any external publication request → Ivan+Kiki hard-stop gate

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Methodology: `/opt/data/agents/research/DEPT-RESEARCH-METHODOLOGY.md`
- Roles glossary: `/opt/data/agents/research/roles-glossary.md`
- Per-dept research catalog: `/opt/data/agents/research/dept-research/05-research-education-research-areas.md`
- Org-design synthesis: `/opt/data/agents/research/org-design-literature.md`
- Citation audit: `/opt/data/agents/research/citation-coverage-audit-2026.md`
- Peer-review process: `/opt/data/agents/research/peer-review-process.md`

---

## CHANGELOG

- v0.1.0 (2026-09-01): initial ratification. 12 sub-roles from ROLES-INVENTORY
  adopted. 4 sub-agents wired. Charter shape mirrors `04-engineering-delivery.md`
  v0.3.0 for discoverability.

---

## Agent Naming (Research dept)

The 4 v0.1.0 sub-agents use the org's portmanteau naming framework:
- `research-tracker` → **Athena** (the chief, weekly brief)
- `citation-checker` → **Clio** (citation goddess, daily coverage)
- `course-producer` → **Calliope** (epic poetry / course content)
- `thesis-tracker` → **Thoth** (knowledge, thesis progress)

Plus cross-cutt: `peitho-language-quality` → **Peitho** (persuasion, language quality),
`thoth-literature-scanner` → **Thoth-Scan**, `hephaestus-document-miner` → **Hephaestus**,
`mnemosyne-document-archivist` → **Mnemosyne**.

See `/opt/data/scratchpad/analysis/AGENT-NAMES-V2.md` for the full reference.