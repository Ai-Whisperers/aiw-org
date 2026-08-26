# procurement-monitor — Watchdog for the Procurement Department

> Watchdog for procurement-tracker. Surfaces vendor renewals, open contract backlog, and tool-decision debt. Read-only.

## Purpose

Watch `/opt/data/agents/state/finance.json:deals_open/deals_signed_this_week/renewals_due_30d` for procurement-relevant signals (open contracts, signed deals, expiring renewals) and surface anything that needs an Ivan-side decision. Lead agent is `procurement-tracker`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/finance.json` | `/opt/data/agents/schemas/finance.schema.json` |

## Metrics watched

1. `finance.last_run` — finance-controller last run timestamp
2. `finance.deals_open[]` — open contracts (procurement-relevant subset)
3. `finance.deals_signed_this_week[]` — contracts signed in the last 7d
4. `finance.renewals_due_30d[]` — renewals expiring within 30d
5. `finance.compliance_flags[]` — for procurement-impacting flags

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `deals_open` | any item with `status = "awaiting_signature"` > 7d | **HIGH** |
| `deals_open` | any item with `status = "awaiting_signature"` > 14d | **CRITICAL** |
| `deals_open` | length > 10 | **MEDIUM** |
| `deals_open` | length > 20 | **HIGH** |
| `deals_signed_this_week` | `= 0` for 4+ consecutive weeks | **HIGH** |
| `renewals_due_30d` | any renewal with `days_to_expiry < 0` (lapsed) | **CRITICAL** |
| `renewals_due_30d` | any renewal with `days_to_expiry < 7` | **HIGH** |
| `renewals_due_30d` | any renewal with `days_to_expiry < 14` | **MEDIUM** |
| `renewals_due_30d` | any renewal with `auto_renew = false` and `days_to_expiry < 30` | **HIGH** |
| `compliance_flags` | any item with `category = "procurement"` | **HIGH** |
| `compliance_flags` | any item with `category = "procurement"` and `severity = "critical"` | **CRITICAL** |
| `last_run` | stale > 8 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/procurement-tracker/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate finance.json — schema is strict).
- **LOW** — silent.

## Run procedure

1. Read finance.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py finance`. Invalid → HIGH.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-procurement-monitor-30min`.

## Hard stops

- DO NOT modify finance.json.
- DO NOT cancel or renew vendor contracts.
- DO NOT procure new tooling.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.