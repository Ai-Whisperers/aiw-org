# bizops-monitor — Watchdog for the BizOps Tracker

> Watchdog for bizops-tracker. Surfaces KPI drift, OKR slippage, and missing briefs. Read-only.

## Purpose

Watch `/opt/data/agents/state/coord.json` (cross-functional analytics, OKR tracking, executive decision support), `/opt/data/agents/state/finance.json` (revenue/cost snapshots), and `/opt/data/agents/state/sales.json` (deal pipeline). Lead agent is `bizops-tracker` (cross-functional analytics).

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `coord.schema.json` |
| `/opt/data/agents/state/finance.json` | `finance.schema.json` |
| `/opt/data/agents/state/sales.json` | `sales.schema.json` |

## Metrics watched

1. `coord.last_run` — last bizops brief (required)
2. `coord.okrs[]` — OKRs and their progress
3. `coord.kpis_snapshot[]` — KPI snapshots from other depts
4. `finance.mrr_usd` — current MRR
5. `finance.burn_rate_usd` — monthly burn
6. `finance.runway_months` — current runway
7. `sales.open_deals` — open deal count
8. `sales.last_run` — last sales brief freshness

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `coord.last_run` | stale > 7 days (weekly cadence miss) | **HIGH** |
| `coord.last_run` | stale > 14 days | **CRITICAL** |
| `finance.mrr_usd` | `= 0` for 2+ runs | **HIGH** |
| `finance.runway_months` | `< 1.5` | **CRITICAL** |
| `finance.runway_months` | `< 3` | **HIGH** |
| `finance.runway_months` | `< 6` | **MEDIUM** |
| `finance.burn_rate_usd` | increase > 50% vs prior | **HIGH** |
| `coord.okrs[].progress` | any OKR `< 0.3` mid-quarter | **MEDIUM** |
| `coord.okrs[].progress` | any OKR `< 0.5` at quarter-end | **HIGH** |
| `sales.open_deals` | `= 0` for 2+ runs | **HIGH** |
| `sales.last_run` | stale > 2 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/bizops-tracker/monitor-notes/YYYY-MM-DD.md` (do NOT mutate any state file directly — all watched files have `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read all three state files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py coord finance sales`. Invalid → HIGH escalation with the validation error.
3. Evaluate every metric → fire per routing table.
4. For MEDIUM alerts, write the parallel notes file.

## Suggested cron schedule

`0 18 * * *` — daily 18:00 PYT. Alias: `aiw-bizops-monitor-daily`.

## Hard stops

- DO NOT modify any watched state file.
- DO NOT auto-fix OKRs — flag only.
- DO NOT send customer-facing notifications.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 2).
