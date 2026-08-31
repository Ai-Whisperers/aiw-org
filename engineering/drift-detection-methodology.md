# Drift Detection Methodology — Initial Framework

> **Phase 8 Area #8** | Engineering dept | Owner: drift-detector + ai-safety-engineer
> **Date**: 2026-09-01
> **Status**: Initial methodology (calibration pending 30d of data)

---

## What we detect

5 drift categories, in priority order:

### D1 — Distribution drift (data shifts)

| | |
|---|---|
| **What** | Numerical/categorical distribution of state-file fields changes significantly |
| **Detection** | Z-score test vs 7-day baseline (|z| > 2.0 = drift) |
| **Example** | sales.json `mrr` jumps from $240 to $4000 (z > 5) |
| **Alert** | HIGH if z > 3, MEDIUM if 2 < z ≤ 3 |

### D2 — Agent output drift (text quality)

| | |
|---|---|
| **What** | Agent response length / structure deviates from baseline |
| **Detection** | Rolling 7-day avg response length ± 30% vs 30-day baseline |
| **Example** | kiki-coach agent suddenly returns 1-line responses (avg 200 words → 50 words) |
| **Alert** | HIGH if ±50%, MEDIUM if ±30% |

### D3 — Schema drift (structure changes)

| | |
|---|---|
| **What** | State files get unexpected fields or lose expected fields |
| **Detection** | Schema validation fails (additionalProperties: false) |
| **Example** | coord.json gets a new `"hacker_payload"` field |
| **Alert** | CRITICAL (security signal) |

### D4 — Cron timing drift (schedule variance)

| | |
|---|---|
| **What** | Cron jobs fire later than scheduled by >50% |
| **Detection** | Compare actual-fire-time vs scheduled-time; flag if delay > 50% of interval |
| **Example** | 30min heartbeat fires 47min late (16min late vs 30min interval = 53% drift) |
| **Alert** | HIGH if >100%, MEDIUM if 50-100% |

### D5 — Cross-system correlation drift

| | |
|---|---|
| **What** | Related signals stop correlating (e.g., eval-pass-rate drops but errors don't increase) |
| **Detection** | Pairwise correlation of state files (Pearson, 7d window); flag if |r| < 0.3 when expected > 0.7 |
| **Example** | coordination.json says "all good" but errors.json has 50 errors |
| **Alert** | HIGH (correlated signals should correlate) |

---

## Initial thresholds (educated guesses)

| Category | MEDIUM | HIGH | CRITICAL |
|----------|--------|------|----------|
| D1 distribution | z > 2 | z > 3 | z > 5 |
| D2 output | ±30% length | ±50% | ±100% |
| D3 schema | (not used) | (not used) | any new field |
| D4 cron timing | +50% delay | +100% | +200% |
| D5 correlation | |r| < 0.3 | |r| < 0.1 | NA |

---

## What to do when drift fires

| Alert | Action |
|-------|--------|
| CRITICAL | Page Ivan + Kiki immediately |
| HIGH | Add to next-day briefing (Ivan reads in 24h) |
| MEDIUM | Log to `state/drift-alerts.json`, review weekly |

---

## Calibration plan

After **30 days of real data** (estimated 2026-10-01):
- For each category, count: how often each threshold fires
- Adjust: thresholds that fire 0 times in 30d are too loose; >20 fires in 30d are too tight
- Update this doc with calibrated values

---

**Cross-references**:
- `04-engineering/drift-detector/PROMPT.md`
- `state/drift-alerts.json` (output sink)
- `~/skills/aiw-state-file-write-discipline/`
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #4

