# 05 — Research & Education Playbook

> Department charter + roles + agents + tooling + SOPs for Research & Education.
> **Last updated**: 2026-08-14

---

## Research & Education — Department Charter

**Mission**: Drive the master's thesis (P1 GeoData v2 — Paraguayan cartography) to completion, package research into publications, and turn it into paid products (courses, papers, consulting). Research is a flagship asset, not a side project.

**Head**: Ivan
**Sub-functions**: Knowledge Management (Tier 2 cross-cutting, owned by Research policy)

---

## Roles (12 roles)

| # | Role | Tier | Status |
|---|------|------|--------|
| 5.1 | Research Lead | 🟢 T1 | Ivan |
| 5.2 | Researcher | 🟢 T1 | Ivan + sub-agent |
| 5.3 | Writer / Editor | 🟢 T1 | Ivan + sub-agent |
| 5.4 | Academic Liaison | 🟡 T2 | deferred (post-thesis submission) |
| 5.5 | Citation / Bibliography Specialist | 🟢 T1 | sub-agent: citation-checker |
| 5.6 | Course Designer | 🟢 T1 | Ivan |
| 5.7 | Course Producer | 🟡 T2 | sub-agent |
| 5.8 | Instructional Designer | 🟠 T3 | deferred |
| 5.9 | Subject Matter Expert (SME) | 🟡 T2 | external contractors |
| 5.10 | Research Engineer | 🟡 T2 | sub-agent (eval harnesses) |
| 5.11 | IP / Patent Specialist | 🟠 T3 | deferred (post-patent) |
| 5.12 | Publication Coordinator | 🟡 T2 | sub-agent |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `research-tracker` | Sun 18:00 PYT | Thesis status, publications, courses |
| `citation-checker` | On-demand | Verifies every citation in research output |
| `thesis-tracker` | Daily 06:00 UTC | Fine-grained thesis progress |
| `course-producer` | Weekly | Slides + transcript generation |
| `source-curator` | Weekly | source-materials/ freshness sweep |

---

## Tooling

### Research Lead (Ivan)
- **Writing**: Obsidian + Markdown + Zotero
- **Citations**: Zotero (OSS) + Better BibTeX
- **Statistics**: R / Python
- **Version control**: Git (`/opt/data/thesis-active/`)

### Researcher
- **Literature search**: Connected Papers, Semantic Scholar
- **Data analysis**: Python (pandas, scikit-learn)
- **Visualization**: matplotlib, seaborn

### Writer / Editor
- **Markdown editor**: Obsidian, VS Code
- **Style guide**: Strunk & White + APA 7th
- **Plagiarism check**: (manual for thesis)

### Course Designer
- **Authoring**: Markdown + Pandoc
- **Slides**: reveal.js (OSS) or Marp
- **Video**: OBS Studio (OSS) for recording

### Citation Specialist
- **Tool**: Zotero + Better BibTeX + cite-as-you-write
- **Validation**: Manubot-style citation grounding
- **Format**: BibTeX, APA, MLA, Chicago

---

## SOPs

### Daily
- 06:00 UTC: thesis-tracker (autonomous thesis tick)

### Weekly
- Sun 18:00 PYT: research-tracker (thesis checkpoint)
- Weekly: course-producer, source-curator

### On-demand
- citation-checker (before any external publication)

### Quarterly
- Thesis milestone review (every 90 days)
- Course content audit

---

## Hard stops (Research dept)

| Action | Authority |
|--------|-----------|
| Thesis chapter sign-off | Ivan |
| Submit to arXiv / conference | Ivan (research-tracker drafts cover letter) |
| Publish course module | Ivan + Kiki (technical review) |
| Open-source agentic framework updates | Ivan |
| Accept invited talk / podcast | Ivan |
| License research IP to external party | Ivan + Kiki |

---

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

---

## Monetization paths

| Asset | Path | Status |
|-------|------|--------|
| 20-pattern agentic framework | MIT license → GitHub stars → consulting leads | Live (agentic-schemas repo) |
| Thesis (P1 GeoData v2) | arXiv preprint → journal → academic consulting | In flight |
| ParaguAI Builder | SaaS product | 5+ live tenants |
| Agent org framework (this doc) | Open-source template → 1-person-AI-company course | Drafted |
| Multi-agent BPM research | Position paper at 2026 Workshop on AI for BPM | Drafted |

---

## Skills stack

- `thesis-active-autonomy` — the active autonomy protocol
- `research-integrity-protocol` — methodology rigor + citation grounding
- `grounded-citations` — citation discipline
- `evaluating-llms-harness` — eval methodology (relevant for thesis)
- `academic-thesis-paper-first` — thesis structure methodology

---

## Source-materials policy

- Research dept owns the policy (add/retire decisions)
- `source-curator` agent does mechanical curation (Tier 2)
- Trigger to ship source-curator: source-materials/ > 50 files
- Ivan approves any add/retire decision

---

## Thesis-active directory structure

```
/opt/data/thesis-active/
├── THESIS_STATE.md     (top 50 lines read by research-tracker)
├── TASK_QUEUE.md        (87 tasks with priority tags)
├── PROGRESS.md         (last few entries for context)
├── AUTONOMY.md          (system overview)
├── chapters/           (the actual thesis content)
├── data/               (raw + processed data)
└── .venv/               (Python venv for thesis scripts)
```

---

## Escalation triggers

- Thesis stuck on same chapter > 14d → surface in next brief
- Conference deadline < 7d with submission not started → Ivan page
- Course draft > 90d untouched → flag
- arXiv rejection → Ivan direct, decide next venue

---

## Knowledge Management (sub-function)

**Owner**: Research dept (policy) + source-curator agent (mechanical)
**Cadence**: Weekly freshness sweep
**Promotion trigger to standalone dept**: source-materials/ > 100 files

Current state: ~30 files in `/opt/data/source-materials/`:
- `topics/`: 4 (hostinger-trademark-incident, paraguai-builder-saas, rubicon-eas-deal, trilingual-middle-market, org-design)
- `skills/`: 12
- `prompts/`: 3
- `repos/`: 4

---

## See also

- `/opt/data/agents/departments/05-research-education.md` (canonical charter)
- `/opt/data/agents-v2/agents/research-tracker/PROMPT.md` (agent spec)
- `/opt/data/thesis-active/` (thesis repo)
- `/opt/data/agents-v2/source-materials/triage-2026-08-14.md` (future: triage doc)
