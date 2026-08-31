# course-producer-monitor — Watchdog for Course Producer

> Watchdog for course-producer. Read-only.

## Purpose

Watch the state files below and flag signals that Course Producer health is degrading. Lead agent is `course-producer`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/research.json` | `research.schema.json (course_pieces field)` |

## Metrics watched

1. `research.course_pieces_per_week`
2. `research.course_quality_pass_rate`
3. `research.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `course_pieces_per_week` | < 1 (KPI target) | **MEDIUM** |
| `course_quality_pass_rate` | < 0.7 | **HIGH** |
| `course_quality_pass_rate` | < 0.5 | **CRITICAL** |
| `last_run` | stale > 7 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/course-producer/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-course-producer-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

