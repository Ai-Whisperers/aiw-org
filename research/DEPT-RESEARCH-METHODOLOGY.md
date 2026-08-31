# Per-Department Research Methodology

> **The shared template** every per-dept research area follows.
> Built 2026-09-01 as part of Phase 7 (research deepening).
>
> **Source**: This consolidates patterns from `research/30-research-areas.md`, `research/30-coaching-research-areas.md`, `research/org-design-literature.md`, and the existing 30+ research files in this repo.

---

## Why this exists

The repo has **~30 cross-org research areas** documented in `research/30-research-areas.md` and **~30 coaching-specific areas** in `research/30-coaching-research-areas.md`. But there was **no per-department research catalog**. Ivan's Phase 7 directive: build one for each Tier-1 dept + board.

This file defines the **methodology** every per-dept research area follows. The 7 per-dept catalogs (`research/dept-research/{dept}-research-areas.md`) use this template.

---

## The 7-question pattern

Every research area answers these 7 questions. The format is consistent across all per-dept catalogs:

### 1. **Question** (the actual research question)
- One sentence, phrased as a question.
- Should be specific enough that answering it produces a concrete artifact.

### 2. **Why** (the decision it informs)
- 2-4 sentences.
- What business/personal decision depends on this research?
- What does NOT happen if we skip this research?

### 3. **Method** (how to do the research)
- Step-by-step, ideally 3-7 steps.
- Concrete data sources (URLs, files, queries, datasets).
- Tooling required.

### 4. **Output** (what artifact is produced)
- Specific filename + format (markdown, CSV, JSON, dashboard).
- Length target (1 page, 1 spreadsheet tab, etc.).
- Location in repo (`research/`, `company/`, etc.).

### 5. **Owner** (who in the org does it)
- Agent + human owner (per the 6-dept framework).
- If the agent doesn't exist yet, mark as TIER-3-DEFERRED.

### 6. **Cadence** (when to do it)
- Once / Quarterly / Monthly / Weekly / Daily / On-demand.
- Trigger event (if applicable).

### 7. **Cross-references** (related research)
- Other dept research areas this depends on or informs.
- Existing files in `research/` that already cover this.

---

## The depth test

Every research area should pass at least the first 2 levels of depth. Level 4 is for the most strategic areas.

| Level | Definition | Effort | Use case |
|-------|-----------|--------|----------|
| **1 — Enumerate** | List the items, no analysis | 30 min - 2 hr | Inventory research (e.g., "list all our vendors") |
| **2 — Analyze** | Compare + categorize + quantify | 2-8 hr | Benchmark research (e.g., "compare 10 LATAM AI agencies on price + ICP + positioning") |
| **3 — Synthesize** | Cross-reference + pattern-match + recommend | 1-3 days | Strategic research (e.g., "synthesize our positioning vs 200 competitors → recommend 3 ICPs") |
| **4 — Recommend** | Action plan + decision framework + ownership | 3-10 days | High-stakes research (e.g., "design funding strategy → 5-year plan with quarterly milestones") |

---

## Cross-department patterns

The 7 per-dept catalogs share 4 universal research themes:

1. **What we already know** — internal research (existing state files, outbox briefs, agent logs)
2. **What the market is doing** — competitor research (200-ai-companies, 200-ai-coaching-companies)
3. **What the literature says** — methodology research (org-design-literature, ground-citations, llm-wiki)
4. **What we should change** — actionable research (gap-research-findings, prompt-analysis)

A good per-dept research area touches at least 2 of these themes. A great one touches all 4.

---

## Cadence tiers

| Tier | Cadence | Why |
|------|---------|-----|
| 🔴 HOT | Daily / Weekly | Affects revenue or production health TODAY |
| 🟡 WARM | Monthly / Quarterly | Affects quarterly planning / OKRs |
| 🔵 COOL | Annually / On-event | Affects long-term strategy only |

---

## The shared template (copy/paste)

Use this template when adding new research areas:

```markdown
### [N]. [Title] [cadence-tier emoji]

| | |
|---|---|
| **Question** | [One sentence] |
| **Why** | [2-4 sentences on what decision this informs] |
| **Method** | [3-7 numbered steps] |
| **Output** | `[filename]` ([format], [length]) |
| **Owner** | [agent-name + human] |
| **Cadence** | [frequency + trigger if any] |
| **Cross-references** | [links to other dept research areas / existing files] |
```

---

## Index — 7 per-dept catalogs

| Catalog | File | Areas |
|---------|------|-------|
| Operations | `research/dept-research/01-operations-research-areas.md` | 6 |
| Finance & Legal | `research/dept-research/02-finance-legal-research-areas.md` | 8 |
| Sales & Growth | `research/dept-research/03-sales-growth-research-areas.md` | 10 |
| Engineering & Development | `research/dept-research/04-engineering-research-areas.md` | 10 |
| Research & Education | `research/dept-research/05-research-education-research-areas.md` | 8 |
| People & Culture | `research/dept-research/06-people-culture-research-areas.md` | 6 |
| Board of Directors | `research/dept-research/board-of-directors-research-areas.md` | 4 |
| **TOTAL** | | **52 per-dept research areas** |

Plus the existing 60 cross-org research areas (`research/30-research-areas.md` + `research/30-coaching-research-areas.md`), we have **~112 documented research areas** across the AI Whisperers org.

---

## How to USE this methodology

When Ivan (or an agent) needs research for a specific decision:
1. Open the relevant dept research catalog (`research/dept-research/{dept}-research-areas.md`)
2. Find the research area that matches the decision
3. Follow the 7-question pattern — start at the **Method** step
4. Produce the **Output** at the specified location
5. Update the research file with new data (or note why no new data)

When adding NEW research areas:
1. Pick the right dept catalog (or create a new Tier-3 catalog when a Tier-3 dept activates)
2. Use the 7-question template above
3. Cross-reference 2+ existing files where possible
4. Set cadence tier (🔴 HOT / 🟡 WARM / 🔵 COOL)

---

**Status**: Methodology complete. Per-dept catalogs under construction in Phase 7 Round 2.
