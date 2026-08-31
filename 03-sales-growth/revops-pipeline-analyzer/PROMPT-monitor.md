# revops-pipeline-analyzer-monitor — Watchdog for RevOps Pipeline Analyzer

> Watchdog for revops-pipeline-analyzer. Read-only.

## Purpose

Watch the state files below and flag signals that RevOps Pipeline Analyzer health is degrading. Lead agent is `revops-pipeline-analyzer`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/sales.json` | `sales.schema.json (pipeline field)` |

## Metrics watched

1. `sales.pipeline_value_usd`
2. `sales.deals_open`
3. `sales.avg_deal_size_usd`
4. `sales.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `pipeline_value_usd` | < $10000 (KPI target) | **HIGH** |
| `deals_open` | < 3 | **HIGH** |
| `avg_deal_size_usd` | decrease > 30% vs prior | **MEDIUM** |
| `last_run` | stale > 1 day | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/revops-pipeline-analyzer/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-revops-pipeline-analyzer-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

