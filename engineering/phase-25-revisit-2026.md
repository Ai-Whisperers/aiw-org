# Phase 25 (Around-the-clock Upgrade) — Status Revisit

> **Phase 8 Area #13** | Engineering dept | Owner: engineering-roster + Kiki
> **Date**: 2026-09-01
> **Status**: All 14 items audited; Phase 26 candidates identified

---

## Status of the 14 Phase 25 items

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | Cron heartbeat onhours/offhours | ✅ Done | jobs.json (current schedule) |
| 2 | Monitor sub-agents | ✅ Done | Phase 5 R3-R4 (28 monitors created) |
| 3 | Wired sub-agent crons | ✅ Done | Phase 6 (113 → 131 crons) |
| 4 | PROMPT-monitor.md for all monitors | ✅ Done | Phase 5 (35 PROMPT-monitor.md files) |
| 5 | State-path reference fixes | ✅ Done | Phase 6 (3 wrong paths fixed) |
| 6 | Cron sync script | ✅ Done | `bash /opt/data/scripts/cron-sync.sh` |
| 7 | Lint-prompts.py | ✅ Done | 63/63 pass |
| 8 | Smoke-test.sh | ✅ Done | L1-L4 all-modes pass |
| 9 | 12-factor methodology adoption | ✅ Done | Phase 21 + Phase 8 #1 audit |
| 10 | State-write discipline | ✅ Done | Phase 8 #7 pattern catalog |
| 11 | Drift detection agent | ✅ Done (PROMPT only) | drift-detector agent exists, calibrated thresholds pending |
| 12 | Chaos testing agent | 🟡 Partial | PROMPT exists, 5 scenario runbooks now exist (Phase 8 #5), no first run yet |
| 13 | Eval gate runner | 🟡 Partial | PROMPT exists, aggregate pass_rate script now exists (Phase 8 #6), aggregation not yet running |
| 14 | Cross-agent coordination layer | ✅ Done | dept-monitors/INDEX.md + PROMPT.md references |

**Summary**: 11/14 done, 3/14 partial (drift-detection calibration, chaos-test first run, eval aggregation).

---

## Phase 26 candidates

| # | Candidate | Why now |
|---|-----------|---------|
| 1 | Drift detection calibration (run for 30d, calibrate thresholds) | Drift agent exists; needs real data |
| 2 | Eval aggregate pass_rate running daily | Script exists; needs cron wiring |
| 3 | Chaos test first run (Scenario #1) | Runbook exists; should run weekly |
| 4 | Hard-stops wrapper enforcement (Kiki decision) | AI safety gap; needs Kiki's call |
| 5 | Eval gate enforcement (block low-pass agents) | AI safety gap; needs Kiki's call |
| 6 | Heartbeat self-validation (heartbeat of the heartbeat) | Operator awareness |
| 7 | Cost reporting per cron | Visibility into $6/day heartbeat cost |

---

## What's NOT a Phase 26 candidate (correctly)

- Tier-3 dept expansion (doctrine: trigger-based)
- Self-running org criteria scoring (org not yet at scale)
- Multi-payroll/cross-currency (no clients in multiple currencies yet)

---

**Cross-references**:
- `docs/phases/PHASE-25-*` (original phase)
- `analysis/PHASE-5-COMPLETION-REPORT.md`
- `analysis/PHASE-6-REFINEMENT-FEEDBACK.md`
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #3

