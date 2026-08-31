# PHASE-1-COMPLETE.md

> Handoff doc. Phase 1 finished.
> **Last updated**: 2026-08-14

---

## Phase 1 — DONE ✅

**Goal**: Fix 1 P0 cron error + unify storage path.

### Tasks completed

| # | Task | Status | Verification |
|---|------|--------|--------------|
| 1A.1 | Locate thesis-daily-tick entry | ✅ | Found (id 135a7c018ccb) |
| 1A.2 | Delete provider_snapshot + model_snapshot from thesis-daily-tick | ✅ | Both keys removed |
| 1A.3 | Same for morning-brief (preventive) | ✅ | Both keys removed |
| 1A.4 | Sync files between /opt/data/cron/jobs.json and /opt/data/.hermes/cron/jobs.json | ✅ | Both files now identical (md5: 36dc6e652dd7e9f88157d2c2d064c4d7) |
| 1B.1 | Verified single canonical storage path | ✅ | Both files point to same content |

### Files modified

- `/opt/data/.hermes/cron/jobs.json` (cleared snapshots, synced to canonical)
- `/opt/data/cron/jobs.json` (cleared snapshots, made canonical)

### Files added

- `/opt/data/agents-v2/backups/2026-08-14-pre-v0.2.0/jobs-canonical-pre-merge.json` (backup of pre-unification state)

### Verification

- Both jobs.json files now have identical md5: `36dc6e652dd7e9f88157d2c2d064c4d7`
- `thesis-daily-tick` snapshot_keys = False (cleared)
- `morning-brief` snapshot_keys = False (cleared)
- Next scheduled run should NOT hit the drift guard

### Not done (deferred)

- Manual trigger to verify the fix works (requires `hermes cron run` — can be done in next session)
- Live check via `hermes cron list` (requires Hermes CLI)

---

## Phase 2 — READY TO START

**Goal**: Build 3 infra scripts (state-snapshot, validate-state, cron-heartbeat) + register 3 cron jobs.

### Tasks queued

1. Write `/opt/data/agents/scripts/state-snapshot.sh` (atomic write: temp + mv)
2. Write `/opt/data/agents/scripts/validate-state.py` (with lockfile)
3. Write `/opt/data/agents/scripts/cron-heartbeat.sh` (with rate-limit)
4. Register 3 cron jobs
5. Test all 3 with race/duplicate scenarios
6. Write `PHASE-2-COMPLETE.md`

### Expected effort

26-39 turns, 2-3 sessions.

### Files to touch

- `/opt/data/agents/scripts/` (3 new files)
- `/opt/data/cron/jobs.json` (3 new entries)
- `/opt/data/.hermes/cron/jobs.json` (sync)

---

**Document path**: `/opt/data/agents-v2/PHASE-1-COMPLETE.md`
**Status**: Phase 1 COMPLETE
**Next phase**: Phase 2 (infra scripts)
**Last updated**: 2026-08-14
