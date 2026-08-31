# citation-checker-monitor — Watchdog for Citation Checker

> Watchdog for citation-checker. Read-only.

## Purpose

Watch the state files below and flag signals that Citation Checker health is degrading. Lead agent is `citation-checker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/research.json` | `research.schema.json` |

## Metrics watched

1. `research.citations_pending_review[]`
2. `research.citation_coverage_pct`
3. `research.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `citations_pending_review[]` | length > 30 | **MEDIUM** |
| `citations_pending_review[]` | length > 100 | **HIGH** |
| `citation_coverage_pct` | < 0.95 (KPI target) | **HIGH** |
| `last_run` | stale > 7 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/citation-checker/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-citation-checker-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

