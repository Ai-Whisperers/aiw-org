# Paper Structure Template

> **Built 2026-09-01** — Phase 7 R6 (methodology docs).
>
> **Purpose**: Standardize structure for AIW research papers. Used by
> `publication-coordinator`, `academic-liaison`, `research-engineer` agents.
>
> **Standard**: Adapted from IMRaD (Introduction, Methods, Results, Discussion)
> + AI-native additions for agentic / LLM research.

---

## Standard structure (8-12 pages)

### Page budget

| Section | Pages | Notes |
|---|---|---|
| Title + Abstract | 0.5 | 150-250 words abstract |
| 1. Introduction | 1.0 | Motivation + research questions |
| 2. Background | 1.0 | Prior work + gap |
| 3. Methods | 2.0 | Design, data, analysis |
| 4. Results | 2.0 | Key findings (3-5) |
| 5. Discussion | 1.5 | Implications, limitations |
| 6. Conclusions | 0.5 | Summary + future work |
| References | 1.0 | 30-60 refs |
| Appendices | Optional | 1-3 pages |

**Total**: 8-12 pages + refs

---

## Section-by-section template

### Title

**Formula**: `[Topic]: [Method] for [Audience/Use Case] in [Context]`

Examples:
- ✅ "Agentic AI for Coaching: A Mixed-Methods Study in LATAM"
- ✅ "Citation Coverage as a Research-Discipline Metric"
- ❌ "AI Stuff" (too vague)
- ❌ "A Novel Approach to Leveraging Artificial Intelligence..." (over-claims)

### Abstract (150-250 words)

```markdown
**Background**: [Why this matters, 1-2 sentences]
**Objective**: [What we investigated, 1 sentence]
**Methods**: [How, 1-2 sentences with key details]
**Results**: [3-5 key findings with numbers, 2-3 sentences]
**Conclusions**: [What it means, 1-2 sentences]
**Keywords**: [3-5 keywords]
```

### 1. Introduction

- **Paragraph 1**: Why this matters (problem, scale, stakes)
- **Paragraph 2**: What's been tried (prior work, gap)
- **Paragraph 3**: What we did (research questions + contribution)
- **Paragraph 4**: Roadmap (what's in each section)

### 2. Background

- **Paragraph 1**: Field overview
- **Paragraph 2**: Key prior work (3-5 papers, summarized)
- **Paragraph 3**: Gap in literature (what's missing)
- **Paragraph 4**: Our positioning (how we fill the gap)

### 3. Methods

- **3.1 Research design** (overview)
- **3.2 Data sources** (what, where, when)
- **3.3 Participants / sample** (n, demographics, recruitment)
- **3.4 Procedure** (step-by-step)
- **3.5 Analysis** (statistical / qualitative approach)
- **3.6 Ethics** (consent, privacy, IRB)

### 4. Results

- **4.1 Descriptive findings** (demographics, baseline)
- **4.2 Primary finding** (RQ1) — table + figure
- **4.3 Secondary finding** (RQ2) — table + figure
- **4.4 Tertiary findings** (RQ3+) — concise
- **4.5 Unexpected findings** (bonus discoveries)

### 5. Discussion

- **5.1 Summary of findings** (1 paragraph)
- **5.2 Comparison to prior work** (where we confirm / extend / contradict)
- **5.3 Theoretical implications**
- **5.4 Practical implications** (for LATAM specifically)
- **5.5 Limitations** (be honest; 3-5 limits)
- **5.6 Future research** (3-5 directions)

### 6. Conclusions

- **Bullet 1**: Finding 1 (1 sentence)
- **Bullet 2**: Finding 2 (1 sentence)
- **Bullet 3**: Implication (1 sentence)
- **Bullet 4**: Call to action (1 sentence)

### References (30-60)

Use **APA 7th** or **ACM** depending on venue. Tools:
- Zotero with `~/skills/grounded-citations/`
- Pandoc with `--citeproc`

### Appendices (optional)

- A: Survey instrument
- B: Code repository link
- C: Additional figures
- D: Statistical details

---

## Figure & table guidelines

### Figures

- **Number consecutively**: Figure 1, Figure 2...
- **Caption**: Self-contained (reader can understand without text)
- **Resolution**: ≥300 DPI for print
- **Format**: Vector (SVG/PDF) preferred; PNG acceptable
- **Color**: Colorblind-safe palette (viridis, cividis)

### Tables

- **Number consecutively**: Table 1, Table 2...
- **Caption**: Above table, descriptive
- **Format**: Clean borders, no vertical lines (APA style)
- **Numbers**: Report mean + SD, not just mean

---

## Writing style

### Active voice

- ✅ "We collected data from 50 participants"
- ❌ "Data was collected from 50 participants"

### Concrete numbers

- ✅ "Coverage increased from 2.5% to 50% (n=120 files)"
- ❌ "Coverage increased significantly"

### No filler

- ❌ "It is worth noting that..."
- ❌ "It should be mentioned that..."
- ✅ State the fact, cite the source

### Acronyms

- Define on first use: "Large Language Model (LLM)"
- After: just "LLM"

---

## Submission workflow

1. **Draft** → Ivan (lead author)
2. **Internal review** → research-tracker + Kiki (1 week)
3. **External peer review** → academic-liaison finds 2-3 reviewers
4. **Revisions** → Ivan (2 weeks)
5. **Final submission** → publication-coordinator (handles venue upload)
6. **Tracking** → publication-coordinator tracks status

---

## AIW-specific notes

- LATAM-first framing: always include regional context
- Bilingual terms: define Spanish + English on first use
- Paraguay / LATAM data sovereignty noted
- Funding/conflict disclosure: be transparent about AI Whisperers sponsorship

---

## Templates in `template/` (to be added in Phase 8)

- `template/apa-paper.tex` — LaTeX template
- `template/figures.svg` — Figure styles
- `template/refs.bib` — Bibliography starter

---

## Version history

- v0.1.0 (2026-09-01): Initial structure template

**Owner**: publication-coordinator
**Review cadence**: per-paper
**Last reviewed**: 2026-09-01

---

## Sources & Standards

This template conforms to:

- **ICMJE Recommendations** (2024 revision) — uniform manuscript structure for biomedical journals. <https://www.icmje.org/icmje-recommendations.pdf>
- **APA Publication Manual** (7th ed., 2020) — sections 2-3 manuscript structure. ISBN 978-1-4338-3217-8.
- **CONSORT 2010 Statement** (Schulz et al., BMJ 2010;340:c332) — clinical trial reporting. <https://doi.org/10.1136/bmj.c332>
- **STROBE Statement** (von Elm et al., Lancet 2007;370:1453-7) — observational studies. <https://doi.org/10.1016/S0140-6736(07)61602-X>
- **arXiv submission guidelines** — for preprint deposits. <https://arxiv.org/help/submit>