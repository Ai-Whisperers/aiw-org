# accounting-monitor — Watchdog for the Accounting Department

> Watchdog for accounting-automation. Surfaces revenue halt, burn drift, payment failures, and MRR anomalies. Read-only.

## Purpose

Watch `/opt/data/agents/state/finance.json` for accounting-relevant signals — MRR, burn, deal pipeline, payment compliance. Lead agent is `accounting-automation`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/finance.json` | `/opt/data/agents/schemas/finance.schema.json` |

## Metrics watched

1. `finance.last_run` — finance-controller last run timestamp
2. `finance.mrr_usd` — monthly recurring revenue (required)
3. `finance.burn_usd_monthly` — monthly cash outflow (required)
4. `finance.runway_months` — operating runway at current burn (required)
5. `finance.deals_signed_this_week[]` — contracts signed in last 7d
6. `finance.compliance_flags[]` — payment / regulatory flags
7. `finance.renewals_due_30d[]` — renewals due for payment reconciliation
8. `finance.open_questions[]` — open accounting questions

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `mrr_usd` | `= 0` | **CRITICAL** |
| `mrr_usd` | decrease > 20% vs prior snapshot | **HIGH** |
| `mrr_usd` | decrease > 40% vs prior snapshot | **CRITICAL** |
| `mrr_usd` | `null` for 2+ runs | **HIGH** |
| `burn_usd_monthly` | absent (`null`) for 2+ runs | **HIGH** |
| `burn_usd_monthly` | increase > 30% vs prior snapshot | **HIGH** |
| `runway_months` | `< 3` | **HIGH** |
| `runway_months` | `< 1.5` | **CRITICAL** |
| `runway_months` | `null` for 2+ runs | **HIGH** |
| `deals_signed_this_week` | `= 0` for 3+ consecutive weeks | **HIGH** |
| `compliance_flags` | any item with `category = "payment"` and `severity = "critical"` | **CRITICAL** |
| `compliance_flags` | any item with `category = "payment"` and `severity = "high"` | **HIGH** |
| `renewals_due_30d` | any item with `category = "subscription"` and unpaid | **HIGH** |
| `open_questions` | length > 3 | **MEDIUM** |
| `open_questions` | length > 6 | **HIGH** |
| `last_run` | stale > 8 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/accounting-automation/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate finance.json — schema is strict).
- **LOW** — silent.

## Run procedure

1. Read finance.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py finance`. Invalid → HIGH.
3. Snapshot prior values from `/opt/data/agents/state/history/snapshots/` if available for trend comparison.
4. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-accounting-monitor-30min`.

## Hard stops

- DO NOT modify finance.json.
- DO NOT issue invoices, refunds, or transfers.
- DO NOT close the books.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.