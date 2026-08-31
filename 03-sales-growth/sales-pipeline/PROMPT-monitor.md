# sales-monitor — Watchdog for the Sales Department

> Watchdog for sales-pipeline. Surfaces funnel collapse, stalled deals, outreach queue jams, cadence misses. Read-only.

## Purpose

Watch `/opt/data/agents/state/sales.json` and flag any signal that revenue motion is slowing — empty funnel, no outreach, long-stalled deals, missed daily cadence. Lead agent is `sales-pipeline`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/sales.json` | `/opt/data/agents/schemas/sales.schema.json` |

## Metrics watched

1. `last_run` — last sales-pipeline run (required)
2. `leads_in_flight[]` — active leads (required)
3. `funnel_30d.leads` — leads in last 30d (required)
4. `funnel_30d.calls_booked` — calls booked in 30d (required)
5. `funnel_30d.proposals_sent` — proposals sent in 30d (required)
6. `funnel_30d.contracts_signed` — contracts signed in 30d (required)
7. `outreach_queue_today[]` — today's outreach queue
8. `stalled_deals[]` — deals stalled > 7d
9. `open_questions[]` — open sales questions

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `funnel_30d.contracts_signed` | `= 0` over rolling 30d | **CRITICAL** |
| `funnel_30d.leads` | `= 0` | **HIGH** |
| `funnel_30d.proposals_sent` | `= 0` for 7d rolling | **HIGH** |
| `funnel_30d.calls_booked` | `< 3` for 30d rolling | **MEDIUM** |
| `leads_in_flight` | length > 25 (capacity risk) | **MEDIUM** |
| `leads_in_flight` | length > 50 | **HIGH** |
| `leads_in_flight` | empty for 3+ runs | **HIGH** |
| `outreach_queue_today` | length > 100 (queue jammed) | **HIGH** |
| `stalled_deals` | any deal stalled > 14d | **HIGH** |
| `stalled_deals` | any deal stalled > 30d | **CRITICAL** |
| `stalled_deals` | length > 5 | **HIGH** |
| `open_questions` | length > 5 | **MEDIUM** |
| `last_run` | stale > 26h (daily cadence miss) | **HIGH** |
| `last_run` | stale > 18h | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/sales-pipeline/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate sales.json — schema is strict).
- **LOW** — silent.

## Run procedure

1. Read sales.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py sales`. Invalid → HIGH.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-sales-monitor-30min`.

## Hard stops

- DO NOT modify sales.json.
- DO NOT send outreach emails or place calls.
- DO NOT advance deals through the funnel.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.