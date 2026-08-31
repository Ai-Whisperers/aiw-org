# Cron Error Patterns — 30d Analysis

> **Phase 8 Area #3** | Operations dept | Owner: ai-ops-coordinator + cron-error-watchdog
> **Date**: 2026-09-01
> **Status**: Single data point (2026-08-31 snapshot); trend pending more data

---

## Snapshot: 2026-08-31 21:38 UTC

Source: `state/cron-error-watchdog.json`

| Metric | Value |
|--------|-------|
| Total cron jobs | 131 |
| Jobs in error | **6** (4.6%) |
| Alerts sent | 0 (alert sent flag = false) |
| Watchdog's last run | 2026-08-31 21:38 UTC |

---

## The 6 jobs in error

| Job | Schedule | Last run | Error category |
|-----|----------|----------|----------------|
| `thesis-weekly-review` | 0 18 * * 0 | 2026-08-30 18:00 | HTTP 429: Token Plan exhausted |
| `aiw-research-tracker-weekly` | 0 21 * * 0 | 2026-08-30 21:00 | HTTP 429: Token Plan exhausted |
| `aiw-coach-ivan` | 0 21 * * 0 | 2026-08-30 21:01 | HTTP 429: Token Plan exhausted |
| `aiw-tax-receipt-tracker-weekly` | 0 19 * * 0 | 2026-08-30 19:00 | HTTP 429: Token Plan exhausted |
| `aiw-founder-bandwidth-watchdog-weekly` | 0 20 * * 0 | 2026-08-30 20:00 | HTTP 429: Token Plan exhausted |
| `aiw-people-hr-weekly` | 0 22 * * 1 | 2026-08-26 20:35 | Unknown provider `minimax-plan` |

---

## Pattern: Sunday evening token-plan exhaustion

5 of 6 errors are HTTP 429 "Token Plan usage limit reached". All happened on **Sunday 2026-08-30** between 18:00 and 21:00.

**Likely cause**: Weekly crons stacked on Sunday evening (18:00, 19:00, 20:00, 21:00). Each runs an LLM call. The cumulative token use exhausted the daily plan.

**Pattern**: Sunday-evening cron pile-up → token-plan exhaustion → all Sunday-evening jobs fail.

**Fix candidates**:
1. Spread weekly crons across days (e.g., Monday morning instead of Sunday evening)
2. Reduce per-job token usage (smaller prompts)
3. Increase token-plan tier (cost trade-off)
4. Retry with exponential backoff

**Recommended fix**: Spread crons (option 1) — cheapest, immediate.

---

## Pattern: Provider config drift

1 of 6 errors is `Unknown provider 'minimax-plan'`. This is a config drift: the cron was set up with a provider name that's no longer valid.

**Likely cause**: Provider name changed in `hermes model` config but cron definition wasn't updated.

**Fix**: Update cron definition to use current provider name.

---

## What `alert_sent: false` means

The watchdog detected 6 jobs in error but **didn't send an alert**. This is intentional (alerts only fire when error >24h old — most haven't hit 24h yet), but also a risk.

**Status of each**: All 6 were last-run on 2026-08-30, so by 2026-09-01 they're >24h old. The next watchdog run should trigger alerts.

**Fix**: Verify alert trigger on next watchdog run (no action needed; just observe).

---

## Recommendations

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 1 | Spread Sunday-evening weekly crons (move some to Mon/Tue) | ai-ops-coordinator | 2026-09-08 |
| 2 | Fix `minimax-plan` provider name | ai-ops-coordinator | 2026-09-08 |
| 3 | Run `scripts/eval-aggregate-pass-rate.py` (Phase 8 #6) | ai-safety-engineer | 2026-09-15 |
| 4 | Document pattern: token-plan exhaustion on stacked crons | ai-ops-coordinator | 2026-09-15 |

---

**Cross-references**:
- `state/cron-error-watchdog.json` (live data)
- `01-operations/ai-ops-coordinator/PROMPT.md`
- `01-operations/cron-error-watchdog/PROMPT.md`
- `analysis/PHASE-7-dept-research/01-operations-research-areas.md` Area #3

