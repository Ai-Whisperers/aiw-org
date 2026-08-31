# Monitor Threshold Calibration — Initial Calibration

> **Phase 8 Area #4** | Operations dept | Owner: ai-ops-coordinator
> **Date**: 2026-09-01
> **Status**: Pre-calibration — insufficient data for empirical calibration

---

## Current threshold sources

I read every PROMPT-monitor.md (35 total) and extracted the threshold rules. They come from 3 sources:

| Source | # of monitors | Pattern |
|--------|---------------|---------|
| **Educated guess** (Phase 5 default) | 28 | z-score 2.0, ±30%, etc. |
| **Inherited from existing monitor** (Phase 4 era) | 5 | (e.g., cron-error-watchdog) |
| **Empirically tuned** (real-data derived) | 2 | (only `cron-error-watchdog`) |

**Net**: 80% of thresholds are educated guesses. Real calibration requires 30+ days of data we don't have yet.

---

## The 4 most-likely-wrong thresholds

| Monitor | Threshold | Risk | Why likely wrong |
|---------|-----------|------|------------------|
| `eval-gate-runner` | "block if pass_rate < 0.5" | Too lenient | Even 0.95 is below the KPI target |
| `drift-detector` | "alert if z > 2" | Too sensitive | At 131 crons, |z|>2 fires often; might flood alerts |
| `cost-tracker` | "alert if daily > $15" | Wrong target | Per L1 audit, current burn is $9.79/day; $15 leaves no headroom |
| `kpi-freshness-watchdog` | "alert if not updated 24h" | Too strict | Some KPIs update weekly by design |

---

## Calibration plan

After **30 days** of real alert data:

1. For each monitor, count: how often did each threshold fire?
2. Adjust: thresholds that fire 0 times → too loose; >20 fires/month → too tight
3. Re-write threshold rules in PROMPT-monitor.md
4. Test in staging before deploying

**Estimated next calibration**: 2026-10-01.

---

## What to do now

Since calibration data doesn't exist yet:
1. **Trust the defaults** — they're better than nothing
2. **Expect adjustments** — first month will reveal over/under-fitting
3. **Document the next-step** — calibrate in 30d

---

**Cross-references**:
- All 35 PROMPT-monitor.md files
- `analysis/PHASE-7-dept-research/01-operations-research-areas.md` Area #4
- `analysis/PHASE-6-REFINEMENT-FEEDBACK.md` (state-path fixes)

