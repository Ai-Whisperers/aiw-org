# proposal-drafter-monitor — Watchdog for Proposal Drafter

> Watchdog for proposal-drafter. Read-only.

## Purpose

Watch the state files below and flag signals that Proposal Drafter health is degrading. Lead agent is `proposal-drafter`.

## Files watched

| File | Schema |
|------|--------|
| `/opt/data/agents/state/sales.json` | `sales.schema.json (proposals field)` |

## Metrics watched

1. `sales.proposals_pending[]`
2. `sales.proposal_approval_rate`
3. `sales.proposal_avg_value_usd`
4. `sales.last_run`

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| `proposals_pending[]` | length > 5 | **MEDIUM** |
| `proposals_pending[]` | length > 10 | **HIGH** |
| `proposal_approval_rate` | < 0.3 | **HIGH** |
| `last_run` | stale > 2 days | **MEDIUM** |

## Alert routing

- **CRITICAL / HIGH** — append to `/opt/data/agents/state/coord.json:decisions_for_ivan[]`.
- **MEDIUM** — append to parallel notes file at `/opt/data/agents/proposal-drafter/monitor-notes/YYYY-MM-DD.md` (do NOT mutate state files — schemas are `additionalProperties: false`).
- **LOW** — silent.

## Run procedure

1. Read watched files via `cat ... | python3 -m json.tool`.
2. Validate via `python3 /opt/data/scripts/aiw-state-validate.py` for any with schemas. Invalid → HIGH escalation.
3. Evaluate every metric → fire per routing table.

## Suggested cron schedule

`0 9 * * *`. Alias: `aiw-proposal-drafter-monitor-daily`.

## Hard stops

- DO NOT modify any watched file.
- DO NOT auto-fix issues — flag only.

## CHANGELOG

- v0.1.0 (2026-09-01): initial monitor (Phase 5 Round 4).

