# ai-safety-engineer-monitor — Watchdog for AI Safety

> Watchdog for ai-safety-engineer. Surfaces eval-gate failures, OWASP-LLM compliance drift, P0 incident patterns. Read-only.

## Purpose

Watch `/opt/data/agents/state/eval-per-agent.json` (per-agent eval pass rates), `/opt/data/agents/state/validation-report.json` (schema validation), and `/opt/data/agents/state/engineering.json:incidents_72h` (P0/P1 patterns). Lead agent is `ai-safety-engineer`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/eval-per-agent.json` | (real file, no schema — read raw) |
| `/opt/data/agents/state/validation-report.json` | (real file, no schema — read raw) |
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json` |

## Metrics watched

1. `eval-per-agent.*.pass_rate` — per-agent eval pass rate
2. `eval-per-agent.*.last_eval_at` — per-agent eval freshness
3. `eval-per-agent.*.consecutive_failures` — failure streak per agent
4. `validation-report.total_errors` — total validation errors
5. `validation-report.files_with_errors` — broken state files count
6. `engineering.incidents_72h` filtered by `severity=P0|P1` — production incidents

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `eval-per-agent.*.pass_rate` | any agent `< 0.5` | **HIGH** |
| `eval-per-agent.*.pass_rate` | any agent `< 0.25` | **CRITICAL** |
| `eval-per-agent.*.consecutive_failures` | `≥ 3` for any agent | **HIGH** |
| `eval-per-agent.*.consecutive_failures` | `≥ 5` for any agent | **CRITICAL** |
| `eval-per-agent.*.last_eval_at` | stale > 7 days for any agent | **MEDIUM** |
| `eval-per-agent.*.last_eval_at` | stale > 14 days for any agent | **HIGH** |
| `validation-report.total_errors` | `> 0` | **HIGH** |
| `validation-report.total_errors` | `> 5` | **CRITICAL** |
| `validation-report.files_with_errors` | `> 3` | **HIGH** |
| `incidents_72h` (P0) | any | **CRITICAL** |
| `incidents_72h` (P1) | any | **HIGH** |
| `incidents_72h` (P0+P1) | length > 3 | **CRITICAL** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`. Tag the offending agent.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/ai-safety-engineer/monitor-notes/YYYY-MM-DD.md`.

## Run procedure

1. Read all three files via `cat ... | python3 -m json.tool`.
2. Validate engineering.json via `python3 /opt/data/scripts/aiw-state-validate.py engineering`.
3. The eval-per-agent and validation-report files have no schema — do basic key existence checks.
4. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *` — daily 09:00 PYT. Alias: `aiw-ai-safety-engineer-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT re-run evals (lead agent owns cadence).
- DO NOT disable eval gates (hard-stop).

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 3).

