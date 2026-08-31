# management-monitor — Watchdog for the Management Department

> Watchdog for management-coordinator. Surfaces stuck items, stale repos, decision debt, and coord cadence misses. Read-only.

## Purpose

Watch `/opt/data/agents/state/coord.json` and flag operational risks: stuck items accumulating, repos going stale, decision backlog for Ivan, or coord itself falling behind its biweekly cadence. Lead agent is `management-coordinator`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/coord.json` | `/opt/data/agents/schemas/coord.schema.json` |

## Metrics watched

1. `last_run` — last coord run (required)
2. `open_stuck[]` — items stuck across agents (required)
3. `stale_repos[]` — repos with no recent activity (required)
4. `decisions_for_ivan[]` — open decisions requiring Ivan (required)
   - Each item: `question`, `context`, `raised_at` (required `raised_at`-less items fail schema)

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `open_stuck` | length > 3 | **MEDIUM** |
| `open_stuck` | length > 6 | **HIGH** |
| `open_stuck` | length > 12 | **CRITICAL** |
| `open_stuck` | any item with `age_days > 14` | **HIGH** |
| `open_stuck` | any item with `age_days > 30` | **CRITICAL** |
| `stale_repos` | length > 3 | **MEDIUM** |
| `stale_repos` | length > 8 | **HIGH** |
| `stale_repos` | length > 15 | **CRITICAL** |
| `decisions_for_ivan` | length > 5 | **LOW** |
| `decisions_for_ivan` | length > 15 | **MEDIUM** |
| `decisions_for_ivan` | length > 30 | **HIGH** |
| `decisions_for_ivan` | any item with `raised_at` > 7 days ago and no `resolved_at` | **HIGH** |
| `decisions_for_ivan` | any item missing `raised_at` (schema-invalid) | **MEDIUM** |
| `last_run` | stale > 4 days (biweekly cadence miss) | **HIGH** |
| `last_run` | stale > 7 days | **CRITICAL** |
| `last_run` | stale > 3 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]` (a self-loop is acceptable for the management monitor; the question context must clearly mark it as `source: management-monitor`).
- **MEDIUM** — append to `/opt/data/agents/management-coordinator/monitor-notes/YYYY-MM-DD.md` (parallel file; do not mutate coord.json — schema has `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read coord.json.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py coord`. Invalid → HIGH.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-management-monitor-30min`.

## Hard stops

- DO NOT modify coord.json (the self-loop alert write is the only exception and is gated by CRITICAL/HIGH only).
- DO NOT mark alerts resolved or close out items.
- DO NOT message Ivan outside the coord.json channel.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.