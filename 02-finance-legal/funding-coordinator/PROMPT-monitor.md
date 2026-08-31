# funding-monitor — Watchdog for the Funding Department

> Watchdog for funding-coordinator. Surfaces application deadlines, credit stalls, and narrative-version drift. Read-only.

## Purpose

Watch `/opt/data/agents/state/funding.json` and flag any signal that funding motion is slipping — deadlines approaching, applications stuck, narrative artefacts going stale, agent itself inactive. Lead agent is `funding-coordinator`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/funding.json` | (real file, no schema) |
| `/opt/data/agents/funding-coordinator/outbox/` | directory freshness |

## Metrics watched

1. `funding.last_updated` — funding.json mtime / `last_updated` field
2. `funding.applications_in_flight[]` — pending applications
3. `funding.credits_received_usd` — received credits total
4. `funding.credits_in_flight_usd` — committed but not received credits
5. `funding.grants_approved_usd` — grants approved total
6. `funding.grants_in_flight_usd` — grants pending
7. `funding.accelerator_acceptances[]` — acceptances received
8. `funding.next_deadlines[]` — upcoming deadlines
9. `funding.key_metrics.*` — embedded MRR, burn, runway, customers
10. `funding.founder_narrative_version` — narrative doc version
11. `funding.deck_version` — pitch deck version
12. `funding.metrics_sheet_version` — metrics sheet version
13. `funding.funding_coordinator_agent_active` — agent liveness flag

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `next_deadlines` | any deadline within 24h | **CRITICAL** |
| `next_deadlines` | any deadline within 72h not `submitted` | **HIGH** |
| `next_deadlines` | any deadline within 7d | **MEDIUM** |
| `next_deadlines` | any deadline lapsed | **CRITICAL** |
| `applications_in_flight` | length > 10 (oversubscribed) | **HIGH** |
| `applications_in_flight` | length `= 0` for 30d (no motion) | **HIGH** |
| `credits_in_flight_usd` | `> 50000` no movement 30d | **MEDIUM** |
| `credits_in_flight_usd` | `> 100000` | **HIGH** |
| `grants_in_flight_usd` | any grant pending > 60d | **MEDIUM** |
| `accelerator_acceptances` | empty for 90d+ | **MEDIUM** |
| `key_metrics.mrr_usd` | `= 0` (no revenue signal for funding) | **HIGH** |
| `key_metrics.runway_months` | `null` (funding can’t quote runway) | **HIGH** |
| `founder_narrative_version` | `null` (no narrative on file) | **HIGH** |
| `deck_version` | `null` (no deck on file) | **HIGH** |
| `metrics_sheet_version` | `null` | **HIGH** |
| `funding_coordinator_agent_active` | `false` | **MEDIUM** |
| `funding_coordinator_agent_active` | `false` for 14d+ | **HIGH** |
| `funding-coordinator/outbox/` | no file in last 14 days | **HIGH** |
| `funding-coordinator/outbox/` | no file in last 7 days | **MEDIUM** |
| `last_updated` | older than 30 days | **HIGH** |
| `last_updated` | older than 14 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/funding-coordinator/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate funding.json — it has no formal schema but the lead agent owns it).
- **LOW** — silent.

## Run procedure

1. Read funding.json.
2. funding.json has no schema — do basic key-existence checks; missing keys → HIGH with context.
3. Stat the funding-coordinator outbox directory.
4. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-funding-monitor-30min`.

## Hard stops

- DO NOT modify funding.json.
- DO NOT submit applications, draft decks, or update narrative docs.
- DO NOT contact funders, accelerators, or grant offices.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.