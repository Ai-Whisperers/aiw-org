# Literature Review Protocol — Systematic Methodology

> **Built 2026-09-01** — Phase 7 R6 (methodology docs).
>
> **Purpose**: Define the systematic literature review process for AIW's
> Research dept. Used by `research-tracker`, `research-engineer`,
> `thoth-literature-scanner`, and `research-associate` agents.
>
> **Methodology**: Adapted from PRISMA 2020 + Kitchenham systematic review +
> AI-specific additions for LLM/agent research.

---

## When to use

- Any research output that cites 10+ papers (thesis chapter, paper, whitepaper)
- Need to demonstrate comprehensive coverage of a topic
- Reviewer asks for systematic methodology

## When NOT to use

- Blog posts / LinkedIn content (use ad-hoc research)
- Course modules (use simpler "further reading" approach)
- Quick opinion pieces (no review needed)

---

## 5-Phase Protocol

### Phase 1 — Question formulation (PICO-S)

Use **PICO-S** for structured research questions:

| Element | Description | Example |
|---|---|---|
| **P**opulation | Who/what is studied | "AI coaching companies in LATAM" |
| **I**ntervention | What is applied | "agentic AI workflows" |
| **C**omparator | What is it compared to | "human-only workflows" |
| **O**utcome | What changes | "lead client conversion rate" |
| **S**tudy type | What kind of evidence | "case studies, surveys, experiments" |

**Output**: 1-paragraph research question + PICO-S table

### Phase 2 — Search strategy (3 sources minimum)

Define **3 search sources** for breadth:

1. **Academic**: arXiv, Semantic Scholar, Google Scholar
   - Use `thoth-literature-scanner` agent
   - 5-10 search queries, last 5 years preferred
2. **Industry**: Vendor docs, conference talks, podcasts
   - 5-10 sources, last 2 years
3. **Practitioner**: LinkedIn posts, blog posts, GitHub repos
   - 3-5 sources, last 1 year

**Output**: Search log with queries, sources, date ranges

### Phase 3 — Inclusion / exclusion criteria

Document **explicit inclusion + exclusion** before screening:

**Inclusion example**:
- Peer-reviewed or industry-trusted sources
- Published 2020-2026
- Addresses agentic AI for coaching/business
- Has empirical data OR strong theoretical contribution

**Exclusion example**:
- Pre-2020 (unless foundational)
- Marketing material without data
- Opinion pieces without evidence

**Output**: Inclusion/exclusion criteria doc + screening log

### Phase 4 — Quality assessment

For each included source, score on 4 dimensions:

| Dimension | 0 (poor) | 1 (medium) | 2 (high) |
|---|---|---|---|
| **Rigor** | Anecdotal | Some data | RCT / controlled |
| **Relevance** | Tangential | Related | Directly addresses PICO-S |
| **Recency** | > 5 years old | 2-5 years | < 2 years |
| **Replicability** | Black box | Partial | Open data + code |

**Total score**: 0-8 per source. Include only sources scoring ≥ 4.

**Output**: Quality score table + inclusion decision per source

### Phase 5 — Synthesis

Two synthesis modes:

#### Mode A — Narrative synthesis (default)

For each PICO-S element:
- What does the evidence say?
- Where do sources agree?
- Where do sources disagree?
- What's the gap?

#### Mode B — Quantitative meta-analysis

If 5+ sources report comparable metrics:
- Extract numbers
- Compute mean / median / range
- Note heterogeneity

**Output**: 2-5 page synthesis section + full reference list

---

## Output template

Every literature review produces:

```markdown
# Literature Review: [TOPIC]

**Question**: [PICO-S research question]

**Date**: YYYY-MM-DD
**Reviewer**: [agent or human name]

## Search log

| Source | Queries | Date range | Hits | Included |
|---|---|---|---|---|
| arXiv | ["agentic AI", "coaching"] | 2020-2026 | 47 | 12 |
| Semantic Scholar | ... | ... | ... | ... |
| Industry blogs | ... | ... | ... | ... |

## Quality assessment

[N sources × 4 dimensions table]

## Synthesis

[2-5 pages following Mode A or B]

## Gaps

- [gap 1]
- [gap 2]

## References

[N formatted citations]
```

## Tools

- **Agent**: `thoth-literature-scanner` for arXiv search
- **Skill**: `~/skills/arxiv/`, `~/skills/grounded-citations/`
- **Output**: `research/lit-reviews/YYYY-MM-DD-{topic}.md`

---

## Agent handoff

When literature review is complete:

```bash
# Notify research-tracker
python3 -c "
import json
from pathlib import Path
state = json.load(open('state/research.json'))
state['literature_reviews'] = state.get('literature_reviews', []) + [{
    'date': 'YYYY-MM-DD',
    'topic': 'TOPIC',
    'sources': N,
    'path': 'research/lit-reviews/YYYY-MM-DD-TOPIC.md'
}]
Path('state/research.json').write_text(json.dumps(state, indent=2))
"
```

---

## Version history

- v0.1.0 (2026-09-01): Initial protocol, PRISMA-adapted

**Owner**: research-tracker
**Review cadence**: quarterly
**Next review**: 2026-12-01

---

## Sources & Standards

This protocol is adapted from:

- **PRISMA 2020 Explanation and Elaboration** (Page et al., BMJ 2021;372:n160). <https://doi.org/10.1136/bmj.n160>
- **PRISMA-S Extension** (Rethlefsen et al., Syst Rev 2021;10:39) — searching extension. <https://doi.org/10.1186/s13643-020-01542-z>
- **Cochrane Handbook ch. 4: Defining the scope of a review**. <https://training.cochrane.org/handbook/current/chapter-04>
- **Booth, Sutton & Papaioannou (2016), *Systematic Approaches to a Successful Literature Review* (2nd ed.), SAGE**. ISBN 978-1-4739-1244-6.