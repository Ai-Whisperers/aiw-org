# eval-gate-runner-monitor — Watchdog for the Eval Gate

> Watchdog for eval-gate-runner. Surfaces eval-pass-rate drops, gate-disabled patterns, drift in quality scores. Read-only.

## Purpose

Watch `/opt/data/state/eval-per-agent.json` (per-agent pass rates and consecutive failures), and `(no schema — eval config embedded in /opt/data/state/eval-per-agent.json)` if present (gate enable/disable state). Lead agent is `eval-gate-runner`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/state/eval-per-agent.json` | (real file, no schema — read raw) |

## Metrics watched

1. `eval-per-agent.*.pass_rate` — per-agent eval pass rate
2. `eval-per-agent.*.consecutive_failures` — failure streak per agent
3. `eval-per-agent.*.last_eval_at` — per-agent eval freshness
4. Aggregate pass rate across all agents
5. Aggregate eval count today

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| aggregate pass_rate | `< 0.95` (KPI target) | **MEDIUM** |
| aggregate pass_rate | `< 0.80` | **HIGH** |
| aggregate pass_rate | `< 0.60` | **CRITICAL** |
| `eval-per-agent.*.pass_rate` | any agent `= 0` | **HIGH** |
| `eval-per-agent.*.consecutive_failures` | `≥ 3` for any agent | **MEDIUM** |
| `eval-per-agent.*.consecutive_failures` | `≥ 5` for any agent | **HIGH** |
| `eval-per-agent.*.last_eval_at` | stale > 7 days for any agent | **LOW** |
| `eval-per-agent.*.last_eval_at` | stale > 14 days for any agent | **MEDIUM** |
| aggregate eval count today | `= 0` for 2+ days | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`. Tag the failing agent.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/eval-gate-runner/monitor-notes/YYYY-MM-DD.md`.

## Run procedure

1. Read eval-per-agent.json via `cat /opt/data/state/eval-per-agent.json | python3 -m json.tool`.
2. Compute aggregate pass_rate as `sum(pass_rate * eval_count) / sum(eval_count)`.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *` — daily 09:00 PYT. Alias: `aiw-eval-gate-runner-monitor-daily`.

## Hard stops

- DO NOT modify eval-per-agent.json directly (lead agent owns writes).
- DO NOT disable eval gates (hard-stop).
- DO NOT re-run evals (lead agent owns cadence).

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 3).

