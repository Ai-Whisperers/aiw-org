# multimedia-monitor — Watchdog for the Multimedia Department

> Watchdog for multimedia-producer. Surfaces asset-cadence slippage, delivery misses, and unused inventory. Read-only.

## Purpose

Watch the multimedia outbox at `/opt/data/agents/multimedia-producer/outbox/`, the research state at `/opt/data/agents/state/research.json:courses_ready/courses_in_draft`, and the analyst KPI snapshot at `/opt/data/agents/state/analyst.json:kpi_snapshot` for content-asset production health. Lead agent is `multimedia-producer`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/multimedia-producer/outbox/` | directory freshness |
| `/opt/data/agents/state/research.json` | `research.schema.json` (`courses_ready`, `courses_in_draft`) |
| `/opt/data/agents/state/analyst.json` | `analyst.schema.json` (`kpi_snapshot`) |

## Metrics watched

1. `multimedia-producer/outbox/` — last mtime + file count
2. `research.courses_ready[]` — array of courses ready for multimedia packaging
3. `research.courses_in_draft[]` — array of courses mid-draft
4. `analyst.kpi_snapshot.pipeline_usd` — sales pipeline USD

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `multimedia-producer/outbox/` | no file in last 14 days | **HIGH** |
| `multimedia-producer/outbox/` | no file in last 7 days | **MEDIUM** |
| `multimedia-producer/outbox/` | no file in last 30 days | **CRITICAL** |
| `multimedia-producer/outbox/` | any file flagged `status = "failed"` in metadata | **HIGH** |
| `research.courses_ready` | length > 0 but no outbox activity in 14d (queue not draining) | **HIGH** |
| `research.courses_in_draft` | length > 15 (multimedia bottleneck) | **MEDIUM** |
| `research.courses_in_draft` | length > 25 | **HIGH** |
| `kpi_snapshot.pipeline_usd` | `= 0` | **HIGH** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to `/opt/data/agents/multimedia-producer/monitor-notes/YYYY-MM-DD.md` (parallel file).
- **LOW** — silent.

## Run procedure

1. Stat outbox directory: `find /opt/data/agents/multimedia-producer/outbox -type f`.
2. Read research.json + analyst.json; validate via `python3 /opt/data/scripts/aiw-state-validate.py research analyst`.
3. Evaluate every metric → fire per routing.

## Suggested cron schedule

`*/30 * * * *` — every 30 minutes. Alias: `aiw-multimedia-monitor-30min`.

## Hard stops

- DO NOT modify research.json, analyst.json, or any outbox file.
- DO NOT generate or upload media assets.
- DO NOT contact external platforms.

## CHANGELOG

- v0.1.0 (2026-08-26): initial monitor.