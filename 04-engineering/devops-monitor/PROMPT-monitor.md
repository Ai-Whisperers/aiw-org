# devops-monitor-monitor — Watchdog for DevOps Monitoring

> Watchdog for devops-monitor. Surfaces infra incidents, deploy failures, cost spikes. Read-only.

## Purpose

Watch `/opt/data/agents/state/engineering.json` (deploys, incidents, infra costs) and `/opt/data/state/cost-tracker.json` if present. Lead agent is `devops-monitor`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json` |
| `/opt/data/state/cost-tracker.json` | (real file, no schema) |

## Metrics watched

1. `engineering.deploys_7d[]` — deploys in last 7 days
2. `engineering.incidents_72h[]` — incidents in last 72h
3. `engineering.infra_costs_monthly_usd` — monthly infra spend
4. `engineering.open_prs` — open PR count
5. `engineering.last_run` — last devops brief freshness
6. `cost-tracker.costs_by_service[]` — service-level cost breakdown
7. `cost-tracker.cost_drift_pct` — cost drift percentage

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `deploys_7d` | empty (zero deploys in 7d) | **HIGH** |
| `deploys_7d` | any deploy with `status=failed` | **CRITICAL** |
| `incidents_72h` | any P0/P1 | **CRITICAL** |
| `incidents_72h` | length > 5 | **HIGH** |
| `incidents_72h` | length > 10 | **CRITICAL** |
| `infra_costs_monthly_usd` | increase > 50% vs prior | **HIGH** |
| `infra_costs_monthly_usd` | `> $500` | **MEDIUM** |
| `infra_costs_monthly_usd` | `> $1000` | **HIGH** |
| `open_prs` | length > 20 | **MEDIUM** |
| `open_prs` | any PR `age_days > 30` | **MEDIUM** |
| `open_prs` | any PR `age_days > 60` | **HIGH** |
| `cost_drift_pct` | `> 30%` | **HIGH** |
| `last_run` | stale > 4 days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/devops-monitor/monitor-notes/YYYY-MM-DD.md`.

## Run procedure

1. Read state files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py engineering`. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *` — daily 09:00 PYT. Alias: `aiw-devops-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-rollback or restart services.
- DO NOT merge or close PRs.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 3).

