# business-analyst-monitor — Watchdog for the Daily Brief

> Watchdog for business-analyst. Surfaces morning-brief staleness, KPI drift, missing data fields. Read-only.

## Purpose

Watch `/opt/data/agents/state/analyst.json` (daily brief snapshot) and cross-reference against `/opt/data/agents/state/finance.json` + `state/sales.json` for accuracy. Lead agent is `business-analyst` (daily 06:30 PYT snapshot).

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/analyst.json` | `analyst.schema.json` |
| `/opt/data/agents/state/finance.json` | `finance.schema.json` |
| `/opt/data/agents/state/sales.json` | `sales.schema.json` |

## Metrics watched

1. `analyst.last_run` — last brief generation time (required, daily 06:30 PYT)
2. `analyst.consumers[]` — who is reading the brief (kronos, hermes-router, etc.)
3. `analyst.sections[]` — which sections were included
4. `finance.mrr_usd` — daily MRR snapshot
5. `finance.burn_rate_usd` — daily burn
6. `sales.open_deals` — open deal count
7. `sales.mrr_in_pipeline` — weighted pipeline MRR

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `analyst.last_run` | stale > 1 day (daily cadence miss) | **HIGH** |
| `analyst.last_run` | stale > 2 days | **CRITICAL** |
| `analyst.consumers[]` | empty for 2+ runs | **MEDIUM** |
| `analyst.sections[]` | missing any required section | **HIGH** |
| `finance.mrr_usd` | change > 50% vs prior brief | **HIGH** |
| `finance.burn_rate_usd` | change > 30% vs prior brief | **MEDIUM** |
| `sales.open_deals` | `= 0` for 2+ briefs | **HIGH** |
| `sales.mrr_in_pipeline` | decrease > 30% vs prior brief | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/business-analyst/monitor-notes/YYYY-MM-DD.md` (do NOT mutate any state file directly — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read all three state files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py analyst finance sales`. Invalid → HIGH escalation with the validation error.
3. Evaluate every metric → fire per routing table.
4. For MEDIUM alerts, write the parallel notes file.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-business-analyst-monitor-30min`.

## Hard stops

- DO NOT modify any watched state file.
- DO NOT auto-generate briefs — flag only.
- DO NOT send Ivan notifications directly — alerts go through coord.json.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 2).
