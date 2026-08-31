# Phase 26 — Autonomous Execution + Decision Surfacing

> **Date**: 2026-09-01
> **Trigger**: Ivan's "work on this phase"
> **Scope**: 10 Phase 26 candidates from REVIEW-2026-Q4.md. Split into:
> - **7 autonomous items** (AI can execute now)
> - **3 decision items** (need Ivan or Kiki; surface, don't execute)

---

## Execution plan

### Autonomous (7) — execute in this turn

| # | Action | Effort | Risk |
|---|---|---:|---|
| 3 | Wire `eval-aggregate-pass-rate.py` to nightly cron | 4h | Low |
| 4 | Drift detection calibration (set up scaffolding; 30d passive) | 1h | None |
| 5 | Run chaos-test scenario #1 (state corruption) | 2h | Low (staging) |
| 6 | Spread Sunday-evening weekly crons (reschedule 5) | 1h | Low |
| 7 | Fix `minimax-plan` provider name in `aiw-people-hr-weekly` | 30m | Low |
| 9 | Heartbeat self-validation cron | 4h | Low |
| 10 | Cost reporting per cron (write script + wire) | 4h | Low |

### Decision (3) — surface, do not execute

| # | Action | Owner | Recommendation |
|---|---|---|---|
| 1 | Sales funnel revival (Formspree vs Worker) | Ivan | **Formspree** (1-2h vs 8-16h) |
| 2 | Hard-stops wrapper invocation | Kiki | **YES** (8-16h, closes AI safety hole) |
| 8 | Eval gate enforcement (block low-pass agents) | Kiki | **YES** (8h, but depends on #2) |

---

## Sequencing

**Round 1 (low-risk infrastructure)**: #7 (provider name fix) + #6 (cron spread) + #4 (drift scaffolding)
**Round 2 (eval + monitoring)**: #3 (eval aggregate cron) + #9 (heartbeat self-validation) + #10 (cost reporting)
**Round 3 (chaos test)**: #5 (first chaos scenario run)
**Round 4 (decision surfacing)**: #1 + #2 + #8 with explicit Ivan/Kiki decision prompts
**Round 5 (verify + commit + feedback)**