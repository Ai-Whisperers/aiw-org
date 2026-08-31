# chaos-test-runner-monitor — Watchdog for Chaos Test Runner

> Watchdog for chaos-test-runner. Read-only.

## Purpose

Watch the state files below and flag signals that Chaos Test Runner health is degrading. Lead agent is `chaos-test-runner`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json (chaos_tests field)` |

## Metrics watched

1. `engineering.chaos_tests_last_run`
2. `engineering.chaos_tests_failures_7d`
3. `engineering.chaos_tests_pass_rate`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `chaos_tests_last_run` | stale > 7 days | **MEDIUM** |
| `chaos_tests_failures_7d` | > 2 | **HIGH** |
| `chaos_tests_pass_rate` | < 0.8 | **HIGH** |
| `chaos_tests_pass_rate` | < 0.5 | **CRITICAL** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/chaos-test-runner/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-chaos-test-runner-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

