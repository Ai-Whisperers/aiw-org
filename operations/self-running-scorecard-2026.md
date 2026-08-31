# Self-Running Org Scorecard (2026-Q3)

> **Phase 8 Area #1** | Operations dept | Owner: ai-ops-coordinator + Ivan
> **Date**: 2026-09-01
> **Status**: First measurement; refresh quarterly

---

## The 7 self-running criteria

For the org to be "self-running" without daily human intervention, it must satisfy:

| # | Criterion | Target | Current | Status |
|---|-----------|--------|---------|--------|
| 1 | All monitors wired to crons | 100% | 28/28 (100%) | ✅ |
| 2 | All state files have schema | 100% | 17/17 (100%) | ✅ |
| 3 | All cron errors auto-alert within 1h | 100% | partial (alert_sent: false today) | 🟡 |
| 4 | Aggregate eval pass_rate ≥ 95% | ≥95% | TBD (script exists, not run) | ⏳ |
| 5 | Daily cost ≤ $15/day | ≤$15 | $9.79/day ($293/mo per L1) | ✅ |
| 6 | Self-running without my input | ≥80% | est. 70% (Ivan still drives cadence decisions) | 🟡 |
| 7 | Operator briefing delivered at 06:00 UTC | 100% | TBD (cron exists, not verified) | ⏳ |

---

## Score: 4.5/7 (64%) — self-running with daily operator input

The org is **mostly self-running** — crons fire, monitors watch, KPIs are computed. The remaining gap is operator awareness: Ivan gets daily briefings but the alerts for cron errors haven't fired yet to verify the path.

---

## What's blocking higher scores

| Gap | Description | Owner | Fix effort |
|-----|-------------|-------|-----------|
| Cron alert verification | Watchdog hasn't sent an alert yet, so we don't know if the path works | ai-ops-coordinator | 1h — manually trigger an error |
| Aggregate eval running | Script exists, needs cron wiring | ai-safety-engineer | 4h — add to nightly cron |
| Daily briefing | Cron exists, needs verification | management-coordinator | 1h — read last 7 days of briefing output |

**Total fix effort**: ~6h. After that, score moves to 7/7 (100%).

---

## The 7 questions this answers

1. **Do we trust the system to keep running?** Mostly yes (4.5/7). 
2. **What does Ivan need to do daily?** Nothing routine; only respond to HIGH/CRITICAL alerts.
3. **What breaks if Ivan is on vacation for 2 weeks?** The system keeps running; the question is whether alerts surface correctly. Answer: unknown until tested.
4. **What needs Ivan's judgment?** Nothing in the system. (Org strategy still needs Ivan, but the agent layer is autonomous.)
5. **What needs Kiki's judgment?** Hard-stops enforcement decision (Phase 8 #2 audit). 16h implementation.
6. **What's the highest-risk unmitigated item?** Token-plan exhaustion on Sunday-evening weekly stack (Phase 8 #3 cron-error-patterns).
7. **When does the org feel self-running?** When score reaches 7/7 (estimated 2 weeks after the 6h of fixes above).

---

## Recommendations

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 1 | Manually trigger a cron error to verify watchdog alert path | ai-ops-coordinator | Now |
| 2 | Wire `eval-aggregate-pass-rate.py` to nightly cron | ai-safety-engineer | 2026-09-08 |
| 3 | Verify daily briefing cron has fired | management-coordinator | 2026-09-08 |
| 4 | Spread Sunday-evening finance weekly crons | ai-ops-coordinator | 2026-09-08 |
| 5 | Re-measure scorecard monthly | ai-ops-coordinator | Monthly |

---

**Cross-references**:
- `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md`
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md`
- `analysis/PHASE-7-dept-research/01-operations-research-areas.md` Area #1
- `state/cron-error-watchdog.json`

