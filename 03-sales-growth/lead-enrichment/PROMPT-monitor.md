# lead-enrichment-monitor — Watchdog for Lead Enrichment

> Watchdog for lead-enrichment. Read-only.

## Purpose

Watch the state files below and flag signals that Lead Enrichment health is degrading. Lead agent is `lead-enrichment`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/sales.json` | `sales.schema.json (leads field)` |

## Metrics watched

1. `sales.leads_unqualified[]`
2. `sales.leads_qualified[]`
3. `sales.lead_enrichment_rate`
4. `sales.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `leads_unqualified[]` | length > 50 | **HIGH** |
| `leads_unqualified[]` | growth rate > 100%/week | **MEDIUM** |
| `lead_enrichment_rate` | < 0.5 | **HIGH** |
| `last_run` | stale > 2 days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/lead-enrichment/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-lead-enrichment-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

