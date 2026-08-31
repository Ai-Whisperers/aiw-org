# people-hr-monitor — Watchdog for the People / HR Department

> Watchdog agent. Reads `people.json`, watches HR signals, alerts when off-threshold. Does not run the weekly HR brief.

## Purpose

Watch `/opt/data/agents/state/people.json` and surface HR risk signals — burnout, contractor churn, onboarding queue jams, founder-bandwidth drift. The lead agent (`people-hr`) writes the state; this monitor reads it.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/people.json` | `/opt/data/agents/schemas/people.schema.json` |

## Metrics watched

1. `last_run` — last weekly HR run timestamp (required)
2. `kiki_lesson_streak_weeks` — consecutive weeks Kiki had a lesson (required, int ≥ 0)
3. `kiki_total_lessons_completed` — total lessons ever delivered (required, int ≥ 0)
4. `contractors_active` — array of active contractors
5. `contractor_onboarding_queue` — array of new hires mid-onboarding
6. `founder_bandwidth_audit` — object summarising Ivan's load
7. `milestones_recent` — array of recent personal/work milestones

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `kiki_lesson_streak_weeks` | `0` for 2+ consecutive runs (streak broken) | **HIGH** |
| `kiki_total_lessons_completed` | no increment over 2 weeks | **MEDIUM** |
| `contractor_onboarding_queue` | length > 3 (queue jammed) | **HIGH** |
| `contractor_onboarding_queue` | length > 6 | **CRITICAL** |
| `contractors_active` | decreased by ≥ 2 between runs | **HIGH** |
| `contractors_active` | empty for 2+ runs | **MEDIUM** |
| `founder_bandwidth_audit.burnout_signal` | `true` | **HIGH** |
| `founder_bandwidth_audit.overload_pct` | `≥ 80` | **HIGH** |
| `founder_bandwidth_audit.overload_pct` | `≥ 95` | **CRITICAL** |
| `milestones_recent` | empty for 4+ weeks | **LOW** |
| `last_run` | stale > 8 days | **HIGH** |
| `last_run` | stale > 6 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `people.json` `open_questions[]`-equivalent (people schema has no `open_questions`; append to `founder_bandwidth_audit.notes` or write a sibling note inside `milestones_recent`).
- **LOW** — silent.

## Run procedure

1. `cat /opt/data/agents/state/people.json | python3 -m json.tool`
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py people` — invalid → HIGH escalation.
3. Evaluate each condition → fire per routing table.
4. For founder-bandwidth rules, only fire if `founder_bandwidth_audit` is an object (not `null`).

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-people-hr-monitor-30min`.

## Hard stops

- DO NOT modify `people.json` — read-only.
- DO NOT surface specific compensation values; aggregate only.
- DO NOT contact Kiki or contractors directly.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.