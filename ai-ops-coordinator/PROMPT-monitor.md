# operations-monitor — Watchdog for the Operations Department

> Watchdog for the operations layer (the inner workings layer that keeps every other department alive). Surfaces cron failures, gateway down, agent liveness, state-file drift. Read-only.

## Purpose

Watch `/opt/data/agents/state/coord.json` (management-coordinator), `/opt/data/state/agent-stats.json`, `/opt/data/state/errors.json`, and the cron heartbeat at `/opt/data/agents/state/heartbeat-alerts.json`. Lead agent is `management-coordinator` (and `ai-ops-coordinator` for ops-layer health).

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `/opt/data/agents/schemas/coord.schema.json` |
| `/opt/data/state/agent-stats.json` | (real file, no schema) |
| `/opt/data/state/errors.json` | (real file, no schema) |
| `/opt/data/agents/state/heartbeat-alerts.json` | (real file, no schema) |

## Metrics watched

1. `coord.last_run` — coord's last run timestamp (required)
2. `coord.open_stuck[]` — items stuck across agents (required)
3. `coord.stale_repos[]` — repos with no activity (required)
4. `coord.decisions_for_ivan[]` — open decisions (required)
5. `agent-stats.json[*].last_heartbeat` — agent liveness per agent
6. `errors.json[*].count_24h` — error rate last 24h
7. `heartbeat-alerts.json.alerts[]` — outstanding heartbeat alerts

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `coord.last_run` | stale > 4 days (biweekly cadence miss) | **HIGH** |
| `coord.last_run` | stale > 7 days | **CRITICAL** |
| `coord.open_stuck` | length > 5 | **HIGH** |
| `coord.open_stuck` | length > 10 | **CRITICAL** |
| `coord.stale_repos` | length > 3 | **HIGH** |
| `coord.stale_repos` | length > 6 | **CRITICAL** |
| `coord.decisions_for_ivan` | length > 10 (decision debt) | **MEDIUM** |
| `coord.decisions_for_ivan` | length > 20 | **HIGH** |
| `agent-stats.*.last_heartbeat` | any agent stale > 24h | **HIGH** |
| `agent-stats.*.last_heartbeat` | any agent stale > 72h | **CRITICAL** |
| `errors.*.count_24h` | `> 10` for any error class | **HIGH** |
| `errors.*.count_24h` | `> 50` for any error class | **CRITICAL** |
| `heartbeat-alerts.alerts[]` | any alert `severity = "P0"` | **CRITICAL** |
| `heartbeat-alerts.alerts[]` | any alert `severity = "P1"` | **HIGH** |
| `heartbeat-alerts.alerts[]` | length > 5 | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]` (note: writing to coord from this monitor means the operations monitor talks to its own lead agent's state — use a distinct `source` field in the question context if available, otherwise rely on `raised_at`).
- **MEDIUM** — append to `/opt/data/agents/management-coordinator/monitor-notes/YYYY-MM-DD.md` (parallel file, do not mutate coord.json — schema has `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read all four files.
2. Validate coord.json via `python3 /opt/data/scripts/aiw-state-validate.py coord`. Other files: basic key checks.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/15 * * * *` — every 15 minutes (operations signals must be near-real-time). Alias: `aiw-ops-monitor-15min`.

## Hard stops

- DO NOT modify coord.json — escalate via parallel notes instead.
- DO NOT restart cron jobs or kill agents.
- DO NOT mark alerts resolved.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.