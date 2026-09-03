# DEMIURGE-121 Context

**STATUS**: PENDING
**TITLE**: audit-empty-prompt-cron-jobs
**OWNER**: AI
**SIZE**: 45m
**CREATED**: 2026-09-02

## Focus

Per the autonomy analysis (2026-09-02): 61 of 184 cron jobs in
`/opt/data/.hermes/cron/jobs.json` have empty prompts (literal `?` or `""`).
33% of the cron fleet is non-functional in the sense that the cron RUNS
on schedule but does nothing useful — there's no prompt for an LLM to
execute.

This is a diagnosis ticket, not a fix ticket. The investigation will:
1. Categorize the 61 jobs (per-department, per-schedule, per-toolset)
2. Identify which are clearly "stub" (intentional empty) vs "broken"
3. Recommend an action per category
4. Surface any orphan jobs (cron entries that have no agent in PROMPT.md)

## Sprint / Phase

Phase "Kernel" (per docs/HERMES-ANSWERS-2026-09-02.md + design docs).
Adjacent to DEMIURGE-113 (decide provider for 79 dead crons) but narrower
scope: just the empty-prompt subset.

## Why this is a diagnosis ticket (not a fix)

Per Phase Kernel brief §4 + R11:
- Cron decisions are operator-authorized (which jobs to keep / drop / fix)
- The cron drift trap (per AGENTS.md + HANDOFF §pitfalls) means jobs.json
  reverts between turns; auto-fixing is fragile
- The investigation surfaces the data; the operator decides what to do
