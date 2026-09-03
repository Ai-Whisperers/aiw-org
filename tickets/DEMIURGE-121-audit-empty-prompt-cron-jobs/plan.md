# DEMIURGE-121: audit-empty-prompt-cron-jobs

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Investigate the 61 cron jobs with empty prompts in
`/opt/data/.hermes/cron/jobs.json` and produce a categorization document
that the operator can use to decide what to do with each.

## Acceptance criteria

- [ ] All 61 jobs identified and categorized by:
  - Per-department (based on prompt/path references)
  - Per-schedule (interval vs cron, frequency)
  - Per-toolset (if available)
  - Per-status (enabled vs disabled, but flagged if previously was enabled)
- [ ] Categorization taxonomy: stub-vs-broken-vs-orphan-vs-system
- [ ] Action recommendation per category
- [ ] Surface: any jobs that reference PROMPT.md files that don't exist
- [ ] Surface: any jobs that are duplicates of other jobs

## Deliverables (paths)

- `analysis/CRON-EMPTY-PROMPT-AUDIT-2026-09-02.md`

## Verification

- [ ] All 61 jobs appear in the analysis doc with their categorization
- [ ] Recommendations are actionable (operator can decide without re-investigating)
- [ ] Cross-references to related tickets (DEMIURGE-113) where relevant
