# board-monitor — Watchdog for the Board of Directors Department

> Watchdog for board-of-directors. Surfaces governance drift, funding-application pressure, and unanswered board decisions. Read-only.

## Purpose

Watch `/opt/data/agents/state/funding.json` (board-level funding + accelerator context), `/opt/data/agents/state/coord.json:decisions_for_ivan` (board-grade open decisions), and the funding outbox at `/opt/data/agents/funding-coordinator/outbox/`. Lead agent is `board-of-directors`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/funding.json` | (real file, no schema) |
| `/opt/data/agents/state/coord.json` | `coord.schema.json` (`decisions_for_ivan`) |
| `/opt/data/agents/funding-coordinator/outbox/` | directory freshness |

## Metrics watched

1. `funding.applications_in_flight[]` — pending funding applications
2. `funding.next_deadlines[]` — upcoming grant/accelerator deadlines
3. `funding.accelerator_acceptances[]` — acceptances received
4. `funding.credits_in_flight_usd` — committed but not received credits
5. `funding.grants_approved_usd` — grants approved total
6. `funding.funding_coordinator_agent_active` — agent liveness flag
7. `coord.decisions_for_ivan[]` — board-grade open decisions
8. `funding-coordinator/outbox/` — last mtime

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `next_deadlines` | any deadline within 24h | **CRITICAL** |
| `next_deadlines` | any deadline within 72h not `submitted` | **HIGH** |
| `next_deadlines` | any deadline within 7d | **MEDIUM** |
| `applications_in_flight` | length > 10 (board saturation) | **HIGH** |
| `applications_in_flight` | length > 15 | **CRITICAL** |
| `applications_in_flight` | length `= 0` for 30d (no motion) | **HIGH** |
| `credits_in_flight_usd` | `> 50000` with no movement 30d | **MEDIUM** |
| `credits_in_flight_usd` | `> 100000` | **HIGH** |
| `accelerator_acceptances` | empty for 90d+ | **MEDIUM** |
| `funding_coordinator_agent_active` | `false` for 14d+ | **HIGH** |
| `coord.decisions_for_ivan` | any board-graded decision (`priority = "board"` or `category = "board"`) > 14d | **HIGH** |
| `coord.decisions_for_ivan` | length > 25 | **HIGH** |
| `funding-coordinator/outbox/` | no file in last 14 days | **HIGH** |
| `funding-coordinator/outbox/` | no file in last 7 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/board-of-directors/monitor-notes/YYYY-MM-DD.md` (parallel file).
- **LOW** — silent.

## Run procedure

1. Read funding.json + coord.json.
2. Validate coord.json via `python3 /opt/data/scripts/aiw-state-validate.py coord`. funding.json has no schema — do basic key existence checks; missing key → HIGH with context.
3. Stat the funding-coordinator outbox directory.
4. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-board-monitor-30min`.

## Hard stops

- DO NOT modify funding.json or coord.json.
- DO NOT submit applications, draft decks, or sign acceptance letters.
- DO NOT contact board members directly.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.