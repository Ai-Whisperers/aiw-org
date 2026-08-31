# source-curator-monitor — Watchdog for Source Curator

> Watchdog for source-curator. Read-only.

## Purpose

Watch the state files below and flag signals that Source Curator health is degrading. Lead agent is `source-curator`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `coord.schema.json (sources field)` |

## Metrics watched

1. `coord.sources[]`
2. `coord.sources[].last_audit`
3. `coord.sources[].staleness_score`
4. `coord.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `sources[]` | length < 10 | **MEDIUM** |
| `sources[].last_audit` | stale > 30 days | **MEDIUM** |
| `sources[].staleness_score` | any > 0.5 | **HIGH** |
| `last_run` | stale > 14 days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/source-curator/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-source-curator-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

