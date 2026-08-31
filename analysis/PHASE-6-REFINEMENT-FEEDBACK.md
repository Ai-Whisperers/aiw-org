# Phase 6 — Refinement (Execution Gap Fixes) — Feedback

> **Date**: 2026-09-01
> **Trigger**: Ivan's question "continue with other tiers or refine?"
> **Decision**: REFINE ONLY.
> **Result**: ✅ All 3 execution gaps fixed.

---

## TL;DR

Phase 5 made the **docs** structurally complete (5/5 + 28 sub-agent monitors + 4 PROMPTs). Phase 6 closed the **execution** loop by:
1. Wiring 18 unwired sub-agent monitor crons
2. Fixing 6 PROMPT-monitor.md files that referenced the wrong state path
3. Fixing 3 references to non-existent files

**Net effect**: All 28 sub-agent monitors are now **executable** (not just documented). Smoke gate is still 100% pass. Lint still 63/63.

---

## What was done

### Gap A — 18 new cron jobs wired (took ~36s with hermes cron create)

The existing 21 monitor crons are **LLM-driven jobs** with a `prompt:` field that says "Read PROMPT-monitor.md for full threshold rules, watch state files X, run validation, alert on CRITICAL/HIGH/MEDIUM."

Before Phase 6: 10 of the 28 sub-agent monitors had wired crons (the ones whose existing PROMPT.md was the dept-lead or a commonly-referenced agent).

After Phase 6: **ALL 28 sub-agent monitors have wired crons.** Total cron count: 113 → 131 (+18).

| Cron name pattern | Example |
|-------------------|---------|
| `aiw-{agent}-monitor-30min` | `aiw-bizops-tracker-monitor-30min` |
| `aiw-{agent}-30min-monitor-30min` | `aiw-devops-monitor-30min-monitor-30min` (the 30-min variant watching itself) |

### Gap B — 6 PROMPT-monitor.md files had wrong state paths

My Phase 5 monitors referenced `/opt/data/agents/state/*.json` for **all** files. That works for dept state files (coord.json, sales.json, engineering.json, etc.) but **6 files actually live at `/opt/data/state/`**:
- `eval-per-agent.json`
- `validation-report.json`
- `cost-tracker.json`
- `agent-stats.json`
- `errors.json`
- (and 1 more)

I patched 6 PROMPT-monitor.md files to use the correct path.

### Gap C — 3 references to non-existent files

After path fixes, 3 references still pointed to files that don't exist:
- `compliance.json` (in 2 files) → use `coord.json:compliance_breaches[]` instead
- `eval-gate-config.json` (in eval-gate-runner) → use embedded eval-per-agent.json
- `heartbeat-alerts.json` (at /opt/data/state/) → actually lives at `/opt/data/agents/state/heartbeat-alerts.json`

After fixes: **all 14 unique state-file references are valid.**

---

## What worked

1. **The `hermes cron create` command is exactly the right tool** for adding monitor crons. Takes ~2 sec per cron (LLM call to register). 18 crons in 36s.

2. **Existing cron prompt template was simple to mimic**:
   ```
   # aiw-{name}-monitor-30min
   Read `/opt/data/agents/{path}/PROMPT-monitor.md` for full threshold rules.
   Watch state files: {state.json}.
   Run `python3 /opt/data/scripts/state-validate.py` first.
   On CRITICAL/HIGH: append to `/opt/data/state/coord.json:decisions_for_ivan[]`.
   On MEDIUM: append to `/opt/data/agents/{path}/monitor-notes/YYYY-MM-DD.md`.
   ```

3. **Path discovery (Gap B) was straightforward**: just check which files actually exist at `/opt/data/state/` vs `/opt/data/agents/state/`. The two directories have meaningfully different contents.

## What didn't work

1. **I almost missed the path discrepancy** until I ran an actual existence check. Phase 5 just wrote paths without verification. Future agents: always verify file references.

2. **The 30-min naming gets awkward**: `aiw-devops-monitor-30min-monitor-30min` (the 30-min variant watching itself). Could be cleaner but matches existing convention.

3. **Smoke gate slowed from 9s → 18s** with 18 new crons. Not a problem, just observation.

## Time spent

- Phase 6 plan: ~3 min
- Gap A (18 crons via hermes): ~5 min
- Gap B (path verification + 6 file patches): ~5 min
- Gap C (file-existence verification + 3 file patches): ~3 min
- Verification (smoke gate + state-file audit): ~2 min
- Feedback writeup: ~2 min
- **Total: ~20 min** ✅

## Delta

| Metric | Before Phase 6 | After Phase 6 |
|--------|---------------|---------------|
| Sub-agent monitors with wired crons | 10/28 (36%) | **28/28 (100%)** |
| Total cron jobs | 113 | **131** |
| PROMPT-monitor.md files with bad state paths | 6 | **0** |
| PROMPT-monitor.md files referencing missing files | 3 | **0** |
| Lint pass | 63/63 | **63/63** |
| Smoke gate | 100% (9s) | **100% (18s)** |

---

## Lessons for next session

1. **Always verify file references before writing PROMPT.md files.** A 30-second `os.path.exists()` check on every state path saves hours of debugging later.

2. **The Hermetic cron wiring pattern (PROMPT.md + cron-job-with-prompt-pointing-at-it) is the unit of execution.** Phase 5 created PROMPT.md without the cron. Phase 6 added the cron. They're inseparable — one without the other is half-built.

3. **Use existing pattern first, customize second.** The 18 new crons use the exact same prompt template as the existing 21. No reinvention needed.

4. **The state path convention is split**:
   - Dept state files (coord, sales, finance, engineering, research, people, etc.) → `/opt/data/agents/state/`
   - Eval/cron state (eval-per-agent, validation-report, cost-tracker, etc.) → `/opt/data/state/`
   - Some files exist at BOTH paths (coord.json, finance.json) — symlinked or duplicated

5. **Refining before expanding was the right call.** Adding Tier-3/4 depts on top of broken execution paths would have multiplied the bug surface.

---

## What's NEXT

**Phase 7 (future)**: After this phase + Phase 5, structure is solid. Optional next moves (Ivan's call):
- **Phase 7a**: Tier-3 dept expansion (Customer Success first per trigger: 5+ clients)
- **Phase 7b**: Threshold calibration against real cron data (needs 30 days of logs)
- **Phase 7c**: Build eval-per-agent.json aggregate pass_rate computation (Phase 5 P3 backlog)
- **Phase 7d**: Consolidate Phase 5+6 lessons into a `scripts/gen-subagent-monitor.py` helper

**Or stop here** — the foundation is solid for current scale. Phase 5+6 = ~30 minutes of AI time, ~2 hours of human-review if any threshold values need tuning.
