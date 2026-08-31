# Phase 10 — Eval-Gate POC Results

**Date**: 2026-08-14
**Status**: POC working, not yet promoted to production gate

## What We Built

`/opt/data/agents-v2/eval-gate.py` — A Python scorer that takes a brief and scores it against a golden trajectory spec.

### Check Coverage (9 checks, weighted 1pt each)

1. **Required sections** (4 pts): Pipeline, Revenue direction, Site & infra health, Today
2. **Word count**: 50-300 words
3. **Has numbers**: at least one stat/digit
4. **Source attribution**: present in text
5. **No trademark violations**: scan against banlist
6. **Today actions concrete**: no vague patterns ("consider", "look into")

### Pass/Fail Threshold

≥ 70% pass rate → PASS (exit 0)
< 70% pass rate → FAIL (exit 2)

## Live Test Results

### Test 1: Real brief from business-analyst (2026-08-14)

```
Score: 7/9 = 78% → PASS
✓ All 4 sections present
✓ Has numbers
✓ No trademark violations
✓ Today actions concrete: "Fix GitHub auth", "Investigate CI failures"
✗ Word count: 43 (below 50-pt floor — agent was too terse)
✗ Source attribution missing
```

### Test 2: Adversarial bad brief

```
Score: 1/9 = 11% → FAIL (exit 2)
✗ All 4 sections missing
✗ Word count: 25
✗ No numbers
✗ Trademark violations: 2 banned brand tokens (model vendor + messaging app)
```

## Storage

Results persisted to `/opt/data/db/analyst.db` in new `eval_log` table:
- `agent`, `brief_path`, `score`, `max_score`, `pass_rate`, `verdict`, `ts`, `details`

## Production Path

To promote from POC to gate:
1. Add `eval-gate.py` to cron: run after every agent brief is written
2. If FAIL → alert on WhatsApp
3. Score trends → eval_regression.py (detect drift from baseline)
4. Golden trajectories per agent (currently only business-analyst)

## Why This Matters

Without eval gates, the org can drift: agents hallucinate, add bloat, drift from spec.
With eval gates, every brief is scored, trends are visible, regressions auto-alert.
