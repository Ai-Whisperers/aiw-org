# okr-tracker-monitor — Watchdog for OKR Tracker

> Watchdog for okr-tracker. Read-only.

## Purpose

Watch the state files below and flag signals that OKR Tracker health is degrading. Lead agent is `okr-tracker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `coord.schema.json (okrs field)` |

## Metrics watched

1. `coord.okrs[]`
2. `coord.okrs[].progress`
3. `coord.okrs[].due_date`
4. `coord.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `okrs[].progress` | any < 0.3 mid-quarter | **MEDIUM** |
| `okrs[].progress` | any < 0.5 at quarter-end | **HIGH** |
| `okrs[].due_date` | any overdue | **HIGH** |
| `last_run` | stale > 7 days | **MEDIUM** |
| `last_run` | stale > 14 days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/okr-tracker/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-okr-tracker-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

