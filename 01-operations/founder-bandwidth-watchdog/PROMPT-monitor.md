# founder-bandwidth-watchdog-monitor — Watchdog for Founder Bandwidth Watchdog

> Watchdog for founder-bandwidth-watchdog. Read-only.

## Purpose

Watch the state files below and flag signals that Founder Bandwidth Watchdog health is degrading. Lead agent is `founder-bandwidth-watchdog`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `coord.schema.json` |

## Metrics watched

1. `coord.ivan_hours_this_week`
2. `coord.ivan_availability_pct`
3. `coord.escalations_pending[]`
4. `coord.decisions_for_ivan[] length`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `ivan_hours_this_week` | > 50 | **HIGH** |
| `ivan_hours_this_week` | > 60 | **CRITICAL** |
| `ivan_availability_pct` | < 0.4 | **MEDIUM** |
| `ivan_availability_pct` | < 0.2 | **HIGH** |
| `escalations_pending[]` | length > 5 | **HIGH** |
| `decisions_for_ivan[]` | length > 10 | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/founder-bandwidth-watchdog/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-founder-bandwidth-watchdog-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

