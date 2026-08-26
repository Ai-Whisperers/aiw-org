# finance-monitor — Watchdog for the Finance Department

> Pattern from the August 13 transcription: *"Agent that is monitoring the department, not executing the work."* This monitor watches the finance department's state file and reports only — it does not run the finance brief.

## Purpose

Watch `/opt/data/agents/state/finance.json` and surface threshold violations before they become cash-flow surprises. The lead agent (`finance-controller`) writes the file; this monitor reads it.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/finance.json` | `/opt/data/agents/schemas/finance.schema.json` |

## Metrics watched (from schema `required` + `properties`)

1. `last_run` — ISO timestamp of finance-controller's last run
2. `runway_months` — operating runway at current burn (required, number ≥ 0)
3. `mrr_usd` — monthly recurring revenue USD (required, number ≥ 0)
4. `burn_usd_monthly` — monthly cash outflow (required, number ≥ 0)
5. `deals_open` — open contract array
6. `deals_signed_this_week` — array of contracts signed this week
7. `compliance_flags` — array of compliance issues
8. `renewals_due_30d` — array of expiring contracts

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `mrr_usd` | `= 0` for 2 consecutive runs | **CRITICAL** |
| `runway_months` | `< 2` | **CRITICAL** |
| `runway_months` | `2 ≤ x < 4` | **HIGH** |
| `runway_months` | `4 ≤ x < 6` | **MEDIUM** |
| `burn_usd_monthly` | absent (`null`) for 2+ runs | **HIGH** |
| `compliance_flags` | length > 0 with severity=ban | **CRITICAL** |
| `compliance_flags` | length > 0 (non-ban) | **HIGH** |
| `deals_open` | length > 10 with 0 signed-this-week | **HIGH** |
| `renewals_due_30d` | any renewal expired (`end_date < today`) | **HIGH** |
| `renewals_due_30d` | any renewal within 7d | **MEDIUM** |
| `last_run` | stale > 8 days (weekly cadence miss) | **HIGH** |
| `last_run` | stale > 6 days | **MEDIUM** |
| `deals_signed_this_week` | empty for 3 consecutive runs | **MEDIUM** |
| `deals_open` | length 0 (no pipeline) | **LOW** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]` with `{question, context, raised_at}`. Item shape must match the coord.schema.json decision item.
- **MEDIUM** — append a structured note to the finance state file's `open_questions[]` array (lead agent will surface it next run).
- **LOW** — silent; absorbed into the weekly brief rollup.

## Run procedure

1. `cat /opt/data/agents/state/finance.json | python3 -m json.tool`
2. Validate against `/opt/data/agents/schemas/finance.schema.json` using `python3 /opt/data/scripts/aiw-state-validate.py finance` — if invalid, escalate HIGH with the validation error.
3. Evaluate every metric → condition above.
4. Fire alerts per routing table.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Lightweight: read-only, ≤1 s runtime. Alias: `aiw-finance-monitor-30min`.

## Hard stops

- DO NOT modify `finance.json` — read-only.
- DO NOT send alerts directly to Ivan outside the coord.json channel — keep the escalation graph clean.
- DO NOT throttle alerts (one alert per condition per run).

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor, mirrors thresholds from ORG-AGENTS.md §3 escalation graph.