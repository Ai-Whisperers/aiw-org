# thesis-tracker-monitor — Watchdog for Thesis Tracker

> Watchdog for thesis-tracker. Read-only.

## Purpose

Watch the state files below and flag signals that Thesis Tracker health is degrading. Lead agent is `thesis-tracker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/research.json` | `research.schema.json (thesis field)` |

## Metrics watched

1. `research.thesis_progress_pct`
2. `research.thesis_milestones_due_30d[]`
3. `research.thesis_blockers[]`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `thesis_progress_pct` | < 0.3 at month 9 of 12 | **HIGH** |
| `thesis_milestones_due_30d[]` | any overdue | **HIGH** |
| `thesis_blockers[]` | length > 2 | **HIGH** |
| `thesis_blockers[]` | any unresolved > 14 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/thesis-tracker/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-thesis-tracker-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

