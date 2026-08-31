# qa-monitor — Watchdog for the QA Department

> Watchdog for the QA automation function. Surfaces eval-gate failures, blocked CI, and quality drift. Read-only.

## Purpose

Watch QA-related state across `/opt/data/agents/state/eval-per-agent.json`, `/opt/data/agents/state/validation-report.json`, and `/opt/data/agents/state/engineering.json:incidents_72h` (engineering incidents that may indicate QA gaps). Lead agent is `qa-automation-runner`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/eval-per-agent.json` | (real file, no formal schema — read raw) |
| `/opt/data/agents/state/validation-report.json` | (real file, no formal schema — read raw) |
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json` (incidents field) |

## Metrics watched

1. `eval-per-agent.json[*].pass_rate` — per-agent eval pass rate
2. `eval-per-agent.json[*].last_eval_at` — freshness per agent
3. `eval-per-agent.json[*].consecutive_failures` — failure streak
4. `validation-report.json.total_errors` — total schema/state validation errors
5. `validation-report.json.files_with_errors` — count of broken state files
6. `engineering.incidents_72h` length and P0/P1 subset

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `validation-report.total_errors` | `> 0` | **HIGH** |
| `validation-report.total_errors` | `> 5` | **CRITICAL** |
| `validation-report.files_with_errors` | `> 3` | **HIGH** |
| `eval-per-agent.*.pass_rate` | any agent `pass_rate < 0.5` | **HIGH** |
| `eval-per-agent.*.pass_rate` | any agent `pass_rate < 0.25` | **CRITICAL** |
| `eval-per-agent.*.consecutive_failures` | `≥ 3` for any agent | **HIGH** |
| `eval-per-agent.*.consecutive_failures` | `≥ 5` for any agent | **CRITICAL** |
| `eval-per-agent.*.last_eval_at` | stale > 7 days for any agent | **MEDIUM** |
| `eval-per-agent.*.last_eval_at` | stale > 14 days for any agent | **HIGH** |
| `engineering.incidents_72h` | any P0/P1 | **CRITICAL** |
| `engineering.incidents_72h` | length > 5 | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`. Tag the question with the offending agent name.
- **MEDIUM** — append to `eval-per-agent.json` as a parallel note file at `/opt/data/agents/qa-automation-runner/monitor-notes/YYYY-MM-DD.md` (do not mutate eval-per-agent.json directly — schema is permissive but write-pattern stays read-only).
- **LOW** — silent.

## Run procedure

1. Read all three files via `cat ... | python3 -m json.tool`.
2. Validate engineering.json via `python3 /opt/data/scripts/aiw-state-validate.py engineering`. The other two files have no schema — do basic key existence checks.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-qa-monitor-30min`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT re-run evals (the lead agent owns that cadence).
- DO NOT gate agent execution — alert only.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.