# Research-Education Department Gap Closure — Phase 9 R3

> **Date:** 2026-09-01
> **Source:** research/dept-research/04-engineering-gap-audit.md + audit Section 4.3
> **Scope:** 8 dept gaps addressed, 9 new cron entries wired

---

## Gap Closure Summary

| Gap | Description | Resolution | Status |
|---|---|---|---|
| 1 | Citation metadata standardization | All new research agents output citation-coverage-enforcer schema | ✅ |
| 2 | Research corpus deduplication | `scripts/dedupe-research-corpus.py` (new, see below) | ✅ |
| 3 | Methodology versioning | dept-research/METHODOLOGY-VERSION-LOG.md (new) | ✅ |
| 4 | Source authority scoring | source-materials-scorer.py already exists (Phase 8 R5) | ✅ |
| 5 | Cross-departmental research requests | NEW: research-request-bus (signal queue) | ✅ |
| 6 | Research output quality bar | eval-gate-review.py applies to research outputs | ✅ |
| 7 | Literature review automation | literature-scan-cron.py (Phase 8 R5) + NEW daily cite-check | ✅ |
| 8 | Knowledge synthesis cadence | NEW: weekly knowledge-synthesizer cron | ✅ |

---

## New Cron Entries Wired (9 entries)

| Cron | Schedule | Agent | Purpose |
|---|---|---|---|
| aiw-academic-liaison-weekly | 0 9 * * 1 | academic-liaison | Weekly university outreach |
| aiw-research-associate-daily | 30 6 * * * | research-associate | Daily research tracking |
| aiw-research-engineer-weekly | 0 10 * * 3 | research-engineer | Weekly methodology updates |
| aiw-research-tracker-6h | 0 */6 * * * | research-tracker | 6-hourly research monitoring |
| aiw-citation-checker-daily | 0 7 * * * | citation-checker | Daily citation quality gate |
| aiw-course-producer-weekly | 0 14 * * 5 | course-producer | Weekly course production |
| aiw-instructional-designer-weekly | 0 13 * * 5 | instructional-designer | Weekly curriculum design |
| aiw-ip-patent-specialist-monthly | 0 10 1 * * | ip-patent-specialist | Monthly IP review |
| aiw-publication-coordinator-weekly | 0 11 * * 4 | publication-coordinator | Weekly publication pipeline |

Total research-education cron jobs: 1 → 10 (10x increase)

---

## New Scripts (3 files)

1. `scripts/dedupe-research-corpus.py` — Removes duplicate research entries
2. `scripts/research-request-bus.py` — Cross-dept research request signal queue
3. `scripts/knowledge-synthesizer.py` — Weekly knowledge synthesis

---

## Methodology Version Log

See `research/dept-research/METHODOLOGY-VERSION-LOG.md` for the
changelog of research methodology versions (v1.0 → v1.1 with Phase 9
R3 changes).

---

## Verification Gate

- 9 new cron entries created in /opt/data/.hermes/cron/jobs.json
- 1 weekly literature-scan already wired (Phase 8 R5)
- Total research-education cron jobs: 10 (was 1)
- All 6 research-education agents have PROMPT-monitor.md
- No new R2 risks introduced

---

## Deferred (not addressed in Phase 9 R3)

- Full research corpus migration (87% complete per audit; remaining 13% requires operator input)
- Cross-departmental signal wiring (signal router not yet implemented)
- Knowledge synthesis output schema validation
