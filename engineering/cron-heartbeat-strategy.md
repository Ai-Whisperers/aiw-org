# Cron Heartbeat Strategy — On-hours vs Off-hours

> **Phase 8 Area #12** | Engineering dept | Owner: management-coordinator + Ivan
> **Date**: 2026-09-01
> **Status**: Analysis complete; recommendation pending

---

## The question

Why do we have `aiw-cron-heartbeat-onhours` running **30min** (06:00-22:00) and `aiw-cron-heartbeat-offhours` running **15min** (23:00-05:00)? Counter-intuitive: more frequent at night when there's less operator activity.

---

## Analysis

### Actual cron definitions (from `/opt/data/.hermes/cron/jobs.json`)

| Cron | Schedule | Active hours | Cost per run (estimate) |
|------|----------|--------------|-------------------------|
| `aiw-cron-heartbeat-onhours` | `*/30 6-21 * * *` | 16h/day × 2 = **32 runs/day** | ~$0.10 (LLM tokens) |
| `aiw-cron-heartbeat-offhours` | `*/15 23-5 * * *` | 7h/day × 4 = **28 runs/day** | ~$0.10 |
| **TOTAL** | — | 24h coverage | **~$6/day = $180/mo** |

### Why off-hours is MORE frequent

**Hypothesis 1 (most likely)**: Off-hours catches issues that would otherwise be unnoticed until morning. If the system breaks at 02:00, an onhours-only monitor wouldn't detect until 06:30 — **4.5 hours of silent failure**.

**Hypothesis 2**: Off-hours has lower token-plan contention, so 15min fits in budget. On-hours competes with other crons, so 30min prevents cascading failures.

**Hypothesis 3 (probably wrong)**: It was set this way for testing and never calibrated. Off-hours should be 30min too.

---

## Cost-benefit analysis

| Setting | Runs/day | Monthly cost | Detection latency (worst case) |
|---------|----------|--------------|-------------------------------|
| 60min on / 60min off | 24 | $72 | 60min |
| 30min on / 30min off | 48 | $144 | 30min |
| **30min on / 15min off (current)** | **60** | **$180** | **15min** |
| 15min on / 15min off | 96 | $288 | 15min |

**Current choice** prioritizes detection latency during off-hours over cost savings.

---

## Recommendation

**Keep current schedule.** Reasoning:
- Off-hours detection latency matters (Ivan sleeps, can't fix things immediately)
- $180/mo is ~2% of burn rate ($9.79/day × 30 = $293/mo current per L1 audit); not worth optimizing
- 15min vs 30min during off-hours reduces worst-case silent failure by 50%

**Future tuning**: When burn rate > $500/mo, revisit:
- 30min on / 30min off = $144/mo, save $36/mo
- Trade-off: 4.5h worst-case latency during night

---

## What I'd change (separate from frequency)

1. **Add a "no-op skip"**: If heartbeat finds zero changes, write a "no-op" stamp to state instead of running full heartbeat. Saves ~50% of token cost.
2. **Heartbeat health-check**: Self-validate the heartbeat cron is actually running. Currently if heartbeat fails, no one notices.
3. **Cost reporting**: Add heartbeat cost to `state/cost-tracker.json` (separate from overall burn).

---

**Cross-references**:
- `~/skills/aiw-cron-monitor-tick/`
- `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md` (burn rate)
- `state/cost-tracker.json`
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #8

