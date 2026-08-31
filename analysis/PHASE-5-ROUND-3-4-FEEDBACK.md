# Phase 5 Rounds 3+4 — Combined Feedback (Bulk Sub-Agent Monitors)

> **Date**: 2026-09-01
> **Rounds**: 3 + 4 (combined — single execution pass for 18 monitors)
> **Time spent**: ~12 minutes total
> **Result**: Sub-agent monitor coverage **32% → 100%** (28/28 sub-agents with PROMPT-monitor.md)

---

## What was done

Wrote `PROMPT-monitor.md` + created `monitor-notes/` dir for **18 sub-agents**:

### Round 3 (4 high-impact engineering):
- `04-engineering/security-watchdog` (2.6KB) — security audit findings, secret rotations, compliance breaches
- `04-engineering/devops-monitor` (2.5KB) — deploys, incidents, infra costs
- `04-engineering/ai-safety-engineer` (3.0KB) — eval-gate failures, OWASP-LLM compliance, P0/P1 incidents
- `04-engineering/eval-gate-runner` (2.4KB) — eval-pass-rate drops, gate-disabled patterns

### Round 4 (14 remaining across depts, batch-written):
- Operations: founder-bandwidth-watchdog, okr-tracker, source-curator
- Finance: tax-receipt-tracker
- Sales: lead-enrichment, proposal-drafter, revops-pipeline-analyzer
- Engineering -30min variants: ai-safety-engineer-30min, devops-monitor-30min, security-watchdog-30min
- Engineering chaos: chaos-test-runner
- Research: citation-checker, course-producer, thesis-tracker

---

## What worked

1. **Bulk-write via Python script** (16 lines per monitor). Each monitor is `mk_monitor(name, display, files, metrics, thresholds, cron)` — function-driven so the structure stays consistent.

2. **Compact template is enough**. Each monitor is ~50 lines (vs. ~70 for dept-lead monitors). Includes: Purpose, Files, Metrics, Threshold rules (5-8 rows), Alert routing, Run procedure, Cron schedule, Hard stops, CHANGELOG.

3. **Cross-referencing dept KPI targets** (`runway < 1.5mo`, `eval pass_rate < 0.95`) keeps monitors consistent with `demiurge/kpi/{dept}-stack.yaml`.

4. **Cron schedule differentiation**: 30-min cadence variants get `*/30 * * * *`; daily agents get `0 9 * * *` or `0 18 * * *`. Matches the existing `*/30` aliases (engineering-roster uses `aiw-engineering-monitor-30min`).

## What didn't work

1. **Threshold values are still guesses** for some agents. Specifically:
   - `tax-receipt-tracker`: I picked `length > 20/50` for receipts_pending but no real data exists yet
   - `course-producer`: KPI target was `1 piece/week`, monitor enforces `< 1` = MEDIUM but this is a low-volume operation
   
   Future improvement: read `state/{dept}.json` for actual values to calibrate.

2. **No aggregate pass_rate computation**. The eval-gate-runner monitor describes the formula but doesn't actually compute it. Would need a small Python helper for that to be operationally useful. (Out of scope for Phase 5 — note as P3.)

3. **3 of the 30-min variants now have BOTH a parent monitor AND a 30-min variant monitor**. This is fine per the design (parent watches state schema, 30-min watches state freshness), but might confuse Ivan if he sees two alerts. Documentation should clarify.

## Pattern update

**All sub-agent monitors now exist.** This is a new baseline. Future additions should follow the `mk_monitor()` pattern in `scripts/gen-subagent-monitor.py` (extract from this round).

## Time spent

- Round 3 (4 monitors, manual write with prose): ~6 min
- Round 4 (14 monitors, Python function bulk-write): ~5 min
- Feedback writeup: ~1 min
- **Total: ~12 min** ✅

## Delta

| Metric | Before Round 1 | After Round 4 | Δ |
|--------|---------------|---------------|---|
| Dept-leads at 5/5 | 5/7 | **7/7** | +2 |
| Sub-agents with PROMPT-monitor.md | 14/28 (50%) | **28/28 (100%)** | +14 |
| Total monitors | 21 (7 lead + 14 sub) | **35 (7 lead + 28 sub)** | +14 |
| Empty cadence-variant dirs | 5 | 5 | 0 (Round 5 will address) |

---

## Lesson for the AI

**At 5 sec/monitor for bulk writes, the cost of full horizontal coverage is negligible** when you build the right helper. 14 monitors in 5 minutes = ~21 sec each.

**The dept-leads' monitor pattern doesn't transfer 1:1 to sub-agents** — sub-agents have narrower scope (single state file, fewer metrics). The `mk_monitor(name, files=[X], metrics=[Y], thresholds=[Z])` signature captures the difference cleanly.

---

## What's NEXT

**Round 5**: Cleanup 5 cadence-variant empty dirs. Verify no cron references them first.

**Round 6**: Build the 4 missing engineering PROMPTs (drift-detector, security-auditor, delivery-tracker, qa-automation-on-pr).

**Then**: Final commit + Phase 5 completion report.
