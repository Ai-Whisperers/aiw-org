# marketing-monitor — Watchdog for the Marketing Department

> Watchdog for marketing-content-producer. Surfaces content cadence slippage, lead-pipeline stalls, and KPI drift. Read-only.

## Purpose

Watch `/opt/data/agents/state/sales.json` (lead funnel), `/opt/data/agents/state/analyst.json:kpi_snapshot` (leads_24h, pipeline_usd), and the marketing outbox freshness at `/opt/data/agents/marketing-content-producer/outbox/`. Lead agent is `marketing-content-producer`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/sales.json` | `sales.schema.json` (funnel + stalled_deals) |
| `/opt/data/agents/state/analyst.json` | `analyst.schema.json` (`kpi_snapshot`) |
| `/opt/data/agents/marketing-content-producer/outbox/` | directory freshness |

## Metrics watched

1. `sales.funnel_30d.leads` — leads in last 30d
2. `sales.funnel_30d.calls_booked` — calls booked in 30d
3. `sales.funnel_30d.proposals_sent` — proposals sent in 30d
4. `sales.funnel_30d.contracts_signed` — contracts signed in 30d
5. `sales.stalled_deals[]` — deals stalled > 7d
6. `analyst.kpi_snapshot.leads_24h` — leads last 24h
7. `analyst.kpi_snapshot.pipeline_usd` — pipeline USD value
8. `marketing-content-producer/outbox/` — last mtime

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `funnel_30d.leads` | `= 0` | **HIGH** |
| `funnel_30d.leads` | `< 10` | **MEDIUM** |
| `funnel_30d.proposals_sent` | `= 0` for 7d window | **HIGH** |
| `funnel_30d.contracts_signed` | `= 0` for 30d window | **CRITICAL** |
| `stalled_deals` | length > 5 | **HIGH** |
| `stalled_deals` | any deal stalled > 21d | **HIGH** |
| `stalled_deals` | any deal stalled > 30d | **CRITICAL** |
| `kpi_snapshot.leads_24h` | `= 0` for 3 consecutive days | **HIGH** |
| `kpi_snapshot.pipeline_usd` | decrease > 50% vs prior snapshot | **HIGH** |
| `kpi_snapshot.pipeline_usd` | `= 0` | **CRITICAL** |
| `marketing-content-producer/outbox/` | no file in last 7 days | **HIGH** |
| `marketing-content-producer/outbox/` | no file in last 4 days | **MEDIUM** |
| `funnel_30d.calls_booked / funnel_30d.leads` | conversion `< 0.05` | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/marketing-content-producer/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate sales.json or analyst.json — schemas are strict).
- **LOW** — silent.

## Run procedure

1. Read sales.json + analyst.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py sales analyst`.
3. Stat outbox directory: `find /opt/data/agents/marketing-content-producer/outbox -type f -newermt "8 days ago" | head -1`.
4. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-marketing-monitor-30min`.

## Hard stops

- DO NOT modify sales.json, analyst.json, or any outbox file.
- DO NOT draft or queue content.
- DO NOT contact leads.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.