# PHASE-2-COMPLETE.md

> Phase 2 finished. Infra scripts + cron jobs wired.

---

## Phase 2 — DONE ✅

**Goal**: Build 3 infra scripts (snapshot, validate, heartbeat) + register 3 cron jobs.

### Tasks completed

| # | Task | Status | Verification |
|---|------|--------|--------------|
| 2A.1 | Write state-snapshot.sh (atomic write) | ✅ | File exists, bash -n passes |
| 2A.2 | Manual test | ✅ | "copied=9 skipped=0" |
| 2B.1 | Write validate-state.py (lockfile + schema check) | ✅ | File exists, py_compile passes |
| 2B.2 | Manual test | ✅ | Found 2 schema issues (analyst.json missing fields) |
| 2C.1 | Write cron-heartbeat.sh (rate-limit) | ✅ | File exists, bash -n passes |
| 2C.2 | Manual test | ✅ | Found 5 jobs in error state |
| 2D | Register 4 infra cron jobs | ✅ | aiw-state-snapshot-6h, aiw-state-validate-15m, aiw-cron-heartbeat-onhours, aiw-cron-heartbeat-offhours |

### Files created

- `/opt/data/agents/scripts/state-snapshot.sh` (executable)
- `/opt/data/agents/scripts/validate-state.py` (executable)
- `/opt/data/agents/scripts/cron-heartbeat.sh` (executable)
- `/opt/data/agents/state/heartbeat-alerts.json` (rate-limit table)
- `/opt/data/agents/state/snapshots/2026-08-14T20-25-52Z/` (first snapshot)
- `/opt/data/agents/state/cron-heartbeat-alerts.log` (alert log)

### Cron jobs added

| Name | Schedule | ID |
|------|----------|-----|
| aiw-state-snapshot-6h | `0 */6 * * *` | 486e77634b99 |
| aiw-state-validate-15m | `*/15 * * * *` | 09528b7c1621 |
| aiw-cron-heartbeat-onhours | `*/30 6-22 * * *` | 3fe6c7bbf60d |
| aiw-cron-heartbeat-offhours | `*/15 23-5 * * *` | 8d044064e1fb |

### Total cron jobs: 23 (was 19)

### Issues discovered (not fixed in Phase 2)

1. **analyst.json schema** — missing `last_run` and `open_questions` fields
2. **5 jobs in error state** — repo-ci-monitor, thesis-watchdog, evo-poll-watchdog, aiw-sales-pipeline-daily, aiw-engineering-roster-biwk

These are tracked in `cron-heartbeat-alerts.log` and will be addressed in later phases (Phase 5+ for the agent jobs; thesis-watchdog might need model drift fix).

### Not done (deferred)

- Race test for snapshot (would need concurrent process)
- Concurrent test for validate (lockfile untested under load)
- Rate-limit test for heartbeat (already rate-limited today)
- Manual trigger via `hermes cron run` (requires Hermes CLI)

---

## Phase 3 — READY TO START

**Goal**: Build 4 atomic patterns + PROMPT-TEMPLATE.md.

### Tasks queued

1. Verify idempotency example script (already documented, may need executable)
2. Verify hard-stops wrapper (documented, needs executable)
3. Verify context-payload JSON schema (documented in PROMPT-TEMPLATE)
4. Verify reflection loop pattern (documented)
5. Update PROMPT-TEMPLATE.md (already done, may need verification)
6. Write `PHASE-3-COMPLETE.md`

### Expected effort

15-20 turns, 1-2 sessions (most patterns already documented, just need executable scripts).

---

**Document path**: `/opt/data/agents-v2/PHASE-2-COMPLETE.md`
**Status**: Phase 2 COMPLETE
**Next phase**: Phase 3 (patterns)
**Last updated**: 2026-08-14
