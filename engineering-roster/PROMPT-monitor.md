# engineering-monitor — Watchdog for the Engineering Department

> Watchdog for engineering-roster state. Surfaces deploy failures, stale repos, infra incidents, runaway costs. Read-only.

## Purpose

Watch `/opt/data/agents/state/engineering.json` and flag any signal that engineering health is degrading — pipeline stopped, repos going stale, incidents stacking, costs drifting up.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/engineering.json` | `/opt/data/agents/schemas/engineering.schema.json` |

## Metrics watched

1. `last_run` — last roster run (required)
2. `deploys_7d` — array of deploys in last 7d (required)
3. `open_prs` — open PRs (required)
4. `stale_repos_7d` — repos with no commits in 7d (required)
5. `incidents_72h` — incidents in last 72h (required)
6. `kiki_commits_7d` — Kyrian's commit count
7. `infra_costs_monthly_usd` — monthly infra spend
8. `tools_pending_decision` — tools awaiting an Ivan decision

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `deploys_7d` | empty (zero deploys) | **HIGH** |
| `deploys_7d` | any deploy with `status = "failed"` | **CRITICAL** |
| `incidents_72h` | any incident with `severity = "P0"` or `severity = "P1"` | **CRITICAL** |
| `incidents_72h` | length > 5 | **HIGH** |
| `incidents_72h` | length > 10 | **CRITICAL** |
| `stale_repos_7d` | length > 3 | **HIGH** |
| `stale_repos_7d` | length > 6 | **CRITICAL** |
| `open_prs` | any PR with `age_days > 30` | **MEDIUM** |
| `open_prs` | any PR with `age_days > 60` | **HIGH** |
| `open_prs` | length > 20 | **MEDIUM** |
| `infra_costs_monthly_usd` | increase > 50% vs prior snapshot | **HIGH** |
| `infra_costs_monthly_usd` | absent (`null`) for 2+ runs | **MEDIUM** |
| `kiki_commits_7d` | `< 5` | **MEDIUM** |
| `kiki_commits_7d` | `= 0` for 2+ runs | **HIGH** |
| `tools_pending_decision` | length > 3 | **MEDIUM** |
| `last_run` | stale > 4 days (biweekly cadence miss) | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to a sibling `monitor_notes` block in `engineering.json` (the schema does not define `open_questions`, so use a key not in `required` — note this will be schema-invalid if `additionalProperties: false`. Solution: write a parallel note file at `/opt/data/agents/engineering-roster/monitor-notes/YYYY-MM-DD.md` instead).
- **LOW** — silent.

## Run procedure

1. Read `engineering.json`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py engineering`. Invalid → HIGH escalation with the validation error.
3. Evaluate every metric → fire per routing table.
4. For MEDIUM alerts, write the parallel notes file (do NOT mutate engineering.json).

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-engineering-monitor-30min`.

## Hard stops

- DO NOT modify `engineering.json`.
- DO NOT attempt to restart, redeploy, or fix any service — alert only.
- DO NOT auto-merge PRs.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.