# tax-receipt-tracker-monitor — Watchdog for Tax Receipt Tracker

> Watchdog for tax-receipt-tracker. Read-only.

## Purpose

Watch the state files below and flag signals that Tax Receipt Tracker health is degrading. Lead agent is `tax-receipt-tracker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/finance.json` | `finance.schema.json (receipts field)` |

## Metrics watched

1. `finance.receipts_pending[]`
2. `finance.receipts_uncategorized[]`
3. `finance.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `receipts_pending[]` | length > 20 | **MEDIUM** |
| `receipts_pending[]` | length > 50 | **HIGH** |
| `receipts_uncategorized[]` | length > 10 | **HIGH** |
| `last_run` | stale > 14 days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/tax-receipt-tracker/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-tax-receipt-tracker-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

