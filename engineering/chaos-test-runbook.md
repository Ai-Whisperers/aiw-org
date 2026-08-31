# Chaos Test Runbook — 5 Initial Scenarios

> **Phase 8 Area #9** | Engineering dept | Owner: chaos-test-runner + engineering-roster
> **Date**: 2026-09-01
> **Status**: Draft (ready for first staging run)

---

## How to use this runbook

Each scenario has:
- **What** we're breaking
- **Pre-conditions** (must be true before running)
- **Action** (the actual chaos)
- **Expected outcome** (what should happen if system is robust)
- **Rollback** (how to undo)
- **Learnings** (after running, document here)

Run scenarios in **staging only** until validated. Never chaos-test in production without Ivan's approval.

---

## Scenario 1 — State file corruption (coord.json)

| | |
|---|---|
| **What** | Corrupt `state/coord.json` (insert random bytes) |
| **Pre-conditions** | (a) staging env with same config as prod, (b) `coord.json` is backable, (c) at least one cron is scheduled to read coord |
| **Action** | `echo "GARBAGE" >> /opt/data/state/coord.json` |
| **Expected outcome** | (a) cron reads fail gracefully (alert sent), (b) no destructive write, (c) rollback recovers state |
| **Rollback** | `cp /opt/data/.backup/coord.json /opt/data/state/coord.json` |
| **Learnings** | _TBD on first run_ |

---

## Scenario 2 — Worker endpoint down (Cloudflare)

| | |
|---|---|
| **What** | Take `rubicon-eas-lead` CF Worker offline (DNS to 127.0.0.1) |
| **Pre-conditions** | (a) live website traffic exists, (b) monitoring on `state/errors.json`, (c) Slack/discord for Ivan |
| **Action** | Disable Worker from CF dashboard |
| **Expected outcome** | (a) `errors.json` records 404 surge, (b) cron-error-watchdog alerts within 30min, (c) sales-pipeline agent surfaces the issue |
| **Rollback** | Re-enable Worker from CF dashboard |
| **Learnings** | _TBD on first run_ |

---

## Scenario 3 — LiteLLM provider outage

| | |
|---|---|
| **What** | Simulate MiniMax provider going down |
| **Pre-conditions** | (a) `hermes-model` fallback configured (already done per Phase 6), (b) cron-error-watchdog active |
| **Action** | `hermes provider disable minimax` |
| **Expected outcome** | (a) cron jobs auto-failover to fallback provider, (b) token-plan-exhausted errors reduce, (c) no job stuck in error state >2h |
| **Rollback** | `hermes provider enable minimax` |
| **Learnings** | _TBD on first run_ |

---

## Scenario 4 — Monitor agent offline (no_agent=true)

| | |
|---|---|
| **What** | Disable `aiw-engineering-monitor` cron for 1 hour |
| **Pre-conditions** | (a) backup monitor (eval-gate-runner) is independent, (b) Ivan is on-call |
| **Action** | `hermes cron disable aiw-engineering-monitor` |
| **Expected outcome** | (a) no alerts missed because eval-gate-runner is independent, (b) cron-error-watchdog detects missing monitor, (c) no auto-recovery required (manual re-enable) |
| **Rollback** | `hermes cron enable aiw-engineering-monitor` |
| **Learnings** | _TBD on first run_ |

---

## Scenario 5 — Schema mutation attack (JSON schema)

| | |
|---|---|
| **What** | Submit eval data with additional properties that violate schema |
| **Pre-conditions** | (a) JSON schema exists in `schemas/eval.schema.json`, (b) `additionalProperties: false` set |
| **Action** | Write extra fields to `state/eval-per-agent.json` (e.g., `"hacker_payload": "rm -rf /"`) |
| **Expected outcome** | (a) eval-aggregate-pass-rate.py script rejects extra fields, (b) state-write-disciple triggers CRITICAL alert, (c) no downstream agent ingests the bad data |
| **Rollback** | Restore state from `state-versioned` repo (hourly snapshots) |
| **Learnings** | _TBD on first run_ |

---

## Schedule

| Date | Scenario | Owner | Status |
|------|----------|-------|--------|
| 2026-09-15 | #1 State corruption | chaos-test-runner | pending |
| 2026-09-22 | #5 Schema attack | chaos-test-runner | pending |
| (TBD) | #2, #3, #4 | chaos-test-runner | pending Ivan approval for prod-adjacent |

---

**Cross-references**:
- `04-engineering/chaos-test-runner/PROMPT.md`
- `state/chaos-test-B-result.json`, `state/chaos-test-C-result.json` (existing results)
- `research/30-research-areas.md` #21 (resilience)
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #5

