# ai-safety-engineer-30min-monitor — Watchdog for AI Safety Engineer (30-min cadence)

> Watchdog for ai-safety-engineer-30min. Read-only.

## Purpose

Watch the state files below and flag signals that AI Safety Engineer (30-min cadence) health is degrading. Lead agent is `ai-safety-engineer-30min`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/engineering.json` | `engineering.schema.json` |

## Metrics watched

1. `engineering.incidents_72h filtered by tag=ai-safety`
2. `engineering.eval_gate_breaches`
3. `engineering.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `incidents_72h (tag=ai-safety)` | any P0 | **CRITICAL** |
| `incidents_72h (tag=ai-safety)` | length > 1 | **HIGH** |
| `eval_gate_breaches` | > 0 | **CRITICAL** |
| `last_run` | stale > 35 min | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/ai-safety-engineer-30min/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`*/30 * * * *`. Alias: `aiw-ai-safety-engineer-monitor-30min`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

