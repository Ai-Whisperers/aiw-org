# research-monitor — Watchdog for the Research Department

> Watchdog for research-tracker state. Surfaces thesis stalls, missed targets, monetization backlog bloat. Read-only.

## Purpose

Watch `/opt/data/agents/state/research.json` and alert on thesis inactivity, missed target dates, and publications/monetization backlog growth. Lead agent is `research-tracker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/research.json` | `/opt/data/agents/schemas/research.schema.json` |

## Metrics watched

1. `last_run` — last research run timestamp (required)
2. `thesis.chapter` — current thesis chapter
3. `thesis.chapter_title` — current chapter title
4. `thesis.last_commit` — last thesis commit timestamp
5. `thesis.target_date` — chapter target date
6. `thesis.blocker` — current blocker string (null when unblocked)
7. `publications_pipeline` — array of upcoming publications
8. `courses_ready` — array of ready courses
9. `courses_in_draft` — array of draft courses
10. `monetization_backlog` — array of monetization candidates

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `thesis.last_commit` | stale > 7 days | **HIGH** |
| `thesis.last_commit` | stale > 14 days | **CRITICAL** |
| `thesis.last_commit` | stale > 4 days | **MEDIUM** |
| `thesis.target_date` | past due (no commit since target) | **HIGH** |
| `thesis.target_date` | within 48h, chapter not `done` | **HIGH** |
| `thesis.blocker` | non-null for > 7 days | **HIGH** |
| `thesis.blocker` | non-null for > 14 days | **CRITICAL** |
| `publications_pipeline` | length > 5 (queue jammed) | **MEDIUM** |
| `publications_pipeline` | any item with `status = "stuck"` for > 14d | **HIGH** |
| `courses_in_draft` | length > 10 | **LOW** |
| `courses_in_draft` | length > 20 | **MEDIUM** |
| `monetization_backlog` | length > 8 | **MEDIUM** |
| `monetization_backlog` | any item with `age_days > 90` | **HIGH** |
| `last_run` | stale > 8 days (weekly cadence miss) | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/research-tracker/monitor-notes/YYYY-MM-DD.md` (parallel file; schema has `additionalProperties: false` so do not mutate research.json).
- **LOW** — silent.

## Run procedure

1. Read research.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py research`. Invalid → HIGH.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-research-monitor-30min`.

## Hard stops

- DO NOT modify research.json.
- DO NOT push thesis commits or alter thesis files.
- DO NOT publish on Ivan's behalf.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.