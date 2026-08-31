# DEMIURGE Self-Running Milestone

> DEMIURGE-053

## Definition

Revenue stack (Marketing, Sales, Product Discovery) is **self-running** when all criteria hold for **7 consecutive days**.

## Pass criteria

| # | Criterion | Measurement |
|---|-----------|-------------|
| 1 | All revenue agents deliver on cadence | 0 missed cron runs (excl. HTTP 402 billing) |
| 2 | Router dispatches without manual intervention | 0 unrouted signals in audit log |
| 3 | Quorum SLA | ≥90% met within time_window |
| 4 | KPI health | kpi-org-health-score ≥ 0.85 daily avg |
| 5 | Source catalog current | Thoth scan within 14 days |
| 6 | Feedback loops active | ≥1 loop fired and completed per dept |
| 7 | Human escalations | ≤2/week to Ivan for "is X live?" |

## Observation window

**DEMIURGE-054**: 7 days observe only. No structural changes unless P0 failure.

Start date: _set when Hermes cron + OpenRouter billing active_

## Failure response

Document gaps in `docs/demiurge/SPRINT-6-COMPLETE.md` and open follow-up tickets.

## Relation to agents-v2

Extends existing `SELF-RUNNING-CRITERIA.md` with DEMIURGE revenue-stack specifics.
