# Department 5 — Research & Education

**Head**: Ivan
**Lead agent**: `research-tracker` (Sun 18:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Drive the master's thesis (P1 GeoData v2 — Paraguayan cartography) to completion, package research into publications, and turn it into paid products (courses, papers, consulting). Research is a flagship asset, not a side project.

## What this department owns

- **Thesis progress** — `/opt/data/thesis-active/` (P1 GeoData v2, 5 chapters)
- **Publications queue** — arXiv preprints, conference submissions, journal articles
- **Course content** — `/opt/data/company/Courses-Content/` + courses-website
- **Agentic framework** — `Ai-Whisperers/agentic-schemas` (the 20-pattern MIT-licensed framework)
- **Research integrity** — citation grounding, methodology rigor (per `research-integrity-protocol` skill)
- **Monetization path** — research IP → paid courses / consulting / licensing
- **NEW v0.2.0**: Knowledge Management (sub-function, owns source-materials/ policy)
- **NEW v0.2.0**: source-curator agent (Tier 2)

## What this department does NOT own

- General LinkedIn content (Sales)
- Client deliverables (Engineering)
- Hiring (People)

## Decision rights (v0.2.0)

| Action | Authority |
|--------|-----------|
| Thesis chapter sign-off | Ivan |
| Submit to arXiv / conference | Ivan (research-tracker drafts cover letter) |
| Publish course module | Ivan + Kiki (technical review) |
| Open-source the agentic framework updates | Ivan |
| Accept invited talk / podcast | Ivan |
| License research IP to external party | Ivan + Kiki |
| **NEW**: Add/retire source-materials | Ivan (per source-curator recommendation) |
| **NEW**: Modify curriculum | require Kiki (charter) |

## Sub-roles (v0.2.0 — 12 roles from ROLES-INVENTORY.md)

| # | Role | Tier |
|---|------|------|
| 5.1 | Research Lead | 🟢 T1 |
| 5.2 | Researcher | 🟢 T1 |
| 5.3 | Writer / Editor | 🟢 T1 |
| 5.4 | Academic Liaison | 🟡 T2 |
| 5.5 | Citation / Bibliography Specialist | 🟢 T1 |
| 5.6 | Course Designer | 🟢 T1 |
| 5.7 | Course Producer | 🟡 T2 |
| 5.8 | Instructional Designer | 🟠 T3 |
| 5.9 | Subject Matter Expert (SME) | 🟡 T2 (external) |
| 5.10 | Research Engineer | 🟡 T2 |
| 5.11 | IP / Patent Specialist | 🟠 T3 |
| 5.12 | Publication Coordinator | 🟡 T2 |

## Sub-agents (v0.2.0)

| Agent | Cadence | Class |
|-------|---------|-------|
| `research-tracker` | Sun 18:00 PYT | CONTENT (reflection) |
| `citation-checker` (NEW) | On-demand | CONTENT (reflection) |
| `thesis-tracker` (NEW, existing thesis-daily-tick) | Daily 06:00 UTC | OPERATIONAL |
| `course-producer` (NEW) | Weekly | CONTENT (reflection) |
| `source-curator` (NEW, cross-cutting Tier 2) | Weekly | OPERATIONAL |

## Inputs the lead agent reads

1. `/opt/data/agents/state/research.json` (SQLite)
2. `/opt/data/thesis-active/THESIS_STATE.md` (top 50 lines)
3. `/opt/data/thesis-active/` git log (last 7 days)
4. `/opt/data/logs/thesis-tick.log` — cron outputs
5. `Ai-Whisperers/agentic-schemas` commit activity (last 30d)
6. arXiv listings for cs.MA, cs.AI, cs.CL (periodic search)
7. `/opt/data/company/Courses-Content/` directory activity

## Cadence (v0.2.0)

| Time | What |
|------|------|
| Sun 18:00 PYT | research-tracker weekly checkpoint |
| Daily 06:00 UTC | thesis-tracker (autonomous tick) |
| Weekly | course-producer, source-curator |
| On-demand | citation-checker (before external publication) |
| Quarterly | thesis milestone review |

## Monetization paths (v0.2.0)

| Asset | Path | Status |
|-------|------|--------|
| 20-pattern agentic framework | MIT license → GitHub stars → consulting leads | Live (agentic-schemas repo) |
| Thesis (P1 GeoData v2) | arXiv preprint → journal → academic consulting | In flight |
| ParaguAI Builder | SaaS product | 5+ live tenants |
| Agent org framework (this plan) | Open-source template → 1-person-AI-company course | Drafted |
| Multi-agent BPM research | Position paper at 2026 Workshop on AI for BPM | Drafted |

## Knowledge Management (v0.2.0 — new sub-function)

- **Owner**: Research dept owns policy
- **Mechanical curator**: `source-curator` agent (Tier 2)
- **Cadence**: Weekly freshness sweep
- **Trigger to ship source-curator**: source-materials/ > 50 files (currently ~30)
- **Trigger to promote KM to standalone dept**: > 100 files OR second knowledge-heavy vertical

Current state: ~30 files in `/opt/data/source-materials/`:
- `topics/`: 4 (hostinger-trademark-incident, paraguai-builder-saas, rubicon-eas-deal, trilingual-middle-market, org-design)
- `skills/`: 12
- `prompts/`: 3
- `repos/`: 4

## State schema (`state/research.json`)

```json
{
  "last_run": null,
  "thesis": {
    "chapter": 3,
    "chapter_title": "Methodology",
    "last_commit": "2026-08-12",
    "target_date": null,
    "blocker": null
  },
  "publications_pipeline": [],
  "courses_ready": [],
  "courses_in_draft": [],
  "monetization_backlog": []
}
```

## Skills stack

- `thesis-active-autonomy` — the active autonomy protocol
- `research-integrity-protocol` — methodology rigor
- `grounded-citations` — citation discipline
- `evaluating-llms-harness` — eval methodology
- `academic-thesis-paper-first` — thesis structure

## Escalation triggers

- Thesis stuck on same chapter > 14d → surface in next brief
- Conference deadline < 7d with submission not started → Ivan page
- Course draft > 90d untouched → flag
- arXiv rejection → Ivan direct, decide next venue

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/05-research-education.md`
- Agent spec: `/opt/data/agents-v2/agents/research-tracker/PROMPT.md`
- Thesis repo: `/opt/data/thesis-active/`
- Source materials: `/opt/data/source-materials/`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added 12 sub-roles, 5 sub-agents (incl. source-curator), Knowledge Management sub-function, Expanded monetization paths, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
