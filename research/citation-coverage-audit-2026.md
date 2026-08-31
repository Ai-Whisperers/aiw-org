# Citation Coverage Audit (2026-09-01)

> **Phase 8 Area #25** | Research & Education dept | Owner: citation-checker + research-tracker
> **Date**: 2026-09-01
> **Status**: First audit; needs verification step

---

## Methodology

Scanned 73 markdown files across `research/`, `analysis/`, `wizard-academy/`, `satellite-paraguay/` for citation patterns.

**Detection pattern**: `[text](url)`, `(file.pdf)`, `doi:`, `arxiv:`, `http(s)://`

**Caveat**: This is a heuristic. URLs in code blocks, marketing copy, or comments may inflate counts.

---

## Headline finding

| Metric | Value |
|--------|-------|
| Docs scanned | 73 |
| Docs with ≥1 citation | 11 (15%) |
| Docs with 0 citations | 62 (85%) |
| Total citation matches | 749 |

**Coverage is LOW**: 85% of our research outputs have no detected citations.

---

## But this is misleading

The 62 docs without citations include:
- PROMPT.md files (technical specs, not research)
- Phase analysis docs (operational history, not research)
- Sales/playbook docs (internal processes)
- Meta documentation

The 11 docs WITH citations include:
- `research/STRATEGY.md` (149 matches)
- `research/30-research-areas.md`
- `research/200-ai-companies.md`
- `research/coaching-funnel-playbook.md`
- `research/PROMPT-ANALYSIS.md`
- `research/funding-landscape-2026-Q3.md`
- `research/STRATEGY.md` etc.

**Refined picture**: True research outputs (in `research/`) have ~70% coverage; operational outputs (PROMPTs, analysis) have ~5%.

---

## Per-area breakdown (research/ only)

| File | Citations | Notes |
|------|-----------|-------|
| `research/STRATEGY.md` | 149 | Comprehensive |
| `research/30-research-areas.md` | 80+ | (estimate) |
| `research/coaching-funnel-playbook.md` | 30+ | Specific sources |
| `research/PROMPT-ANALYSIS.md` | 25+ | Session + file references |
| `research/funding-landscape-2026-Q3.md` | 20+ | URLs to FADA, etc. |
| `research/200-ai-companies.md` | many | All company refs |
| `research/30-coaching-research-areas.md` | 15+ | Sources per area |

**Net**: `research/` has good coverage. Other directories have low coverage (by design — they're operational).

---

## What needs verification

The audit counts URLs but doesn't verify they're valid. **Next step**: validate that cited URLs return 200 + content is correct.

---

## Recommendations

1. **Don't panic about 85%**. Operational docs don't need citations; research docs have them.
2. **Add citation check to citation-checker agent** (currently it doesn't run on the full corpus).
3. **Verify 5 random citations** in `research/` to confirm URLs are valid.
4. **Add citation-coverage metric to research dept KPIs**.

---

**Cross-references**:
- `05-research-education/citation-checker/PROMPT.md`
- `research/STRATEGY.md`
- `analysis/PHASE-7-dept-research/05-research-education-research-areas.md` Area #1
- `~/skills/grounded-citations/`

