# coaching-monitor — Watchdog for the Coaching Department

> Watchdog for the coaching practice. Surfaces lesson-streak breaks, prep freshness, customer-pipeline drift, and renewal pressure. Read-only.

## Purpose

Watch `/opt/data/agents/state/kiki.json` (Kiki coach state), `/opt/data/agents/state/kiki-prep.json` (prep freshness), `/opt/data/state/coaching-customers.json` (customer roster + renewals), and `/opt/data/state/conversion-attempts.json`. Lead agent is `coach-practitioner` (and the broader coaching agent family).

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/kiki.json` | `kiki.schema.json` |
| `/opt/data/agents/state/kiki-prep.json` | `kiki-prep.schema.json` |
| `/opt/data/state/coaching-customers.json` | (real file, no schema) |
| `/opt/data/state/conversion-attempts.json` | (real file, no schema) |

## Metrics watched

1. `kiki.last_run` — last kiki-coach run
2. `kiki.lessons_delivered[]` — array of lessons
3. `kiki.streak_weeks_completed` — consecutive weeks with a lesson
4. `kiki.next_topic` — planned next topic
5. `kiki-prep.as_of` — when prep was last generated
6. `kiki-prep.error` — non-null error string
7. `coaching-customers[*].renewal_due` — per-customer renewal date
8. `coaching-customers[*].status` — per-customer active/at-risk/churned
9. `conversion-attempts[*].result` — lead outcomes

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `kiki.streak_weeks_completed` | `= 0` for 2+ consecutive runs | **HIGH** |
| `kiki.streak_weeks_completed` | decreased between runs (streak reset) | **HIGH** |
| `kiki.lessons_delivered` | no new lesson in last 14d | **HIGH** |
| `kiki.lessons_delivered` | no new lesson in last 7d | **MEDIUM** |
| `kiki.last_run` | stale > 8 days (weekly cadence miss) | **HIGH** |
| `kiki.next_topic` | `null` for 3+ runs | **MEDIUM** |
| `kiki-prep.as_of` | older than 8 days (prep going stale) | **HIGH** |
| `kiki-prep.as_of` | older than 4 days | **MEDIUM** |
| `kiki-prep.error` | non-null | **HIGH** |
| `coaching-customers` | any customer `status = "at_risk"` | **MEDIUM** |
| `coaching-customers` | any customer `status = "churned"` this week | **HIGH** |
| `coaching-customers` | any renewal due within 7d | **HIGH** |
| `coaching-customers` | any renewal overdue | **CRITICAL** |
| `coaching-customers` | active count decreased > 20% vs prior snapshot | **HIGH** |
| `conversion-attempts` | 5+ consecutive `result = "no_show"` | **MEDIUM** |
| `conversion-attempts` | `result = "converted"` rate `< 5%` over rolling 30d | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/coach-practitioner/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate kiki.json or kiki-prep.json — schemas are strict).
- **LOW** — silent.

## Run procedure

1. Read kiki.json, kiki-prep.json, coaching-customers.json, conversion-attempts.json.
2. Validate kiki.json + kiki-prep.json via `python3 /opt/data/scripts/aiw-state-validate.py kiki kiki-prep`.
3. For coaching-customers.json / conversion-attempts.json (no schema), do basic key-existence checks; missing or malformed → HIGH.
4. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-coaching-monitor-30min`.

## Hard stops

- DO NOT modify kiki.json, kiki-prep.json, coaching-customers.json, or conversion-attempts.json.
- DO NOT contact Kiki, Kyrian, or coaching customers.
- DO NOT change lesson topics or curriculum.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.