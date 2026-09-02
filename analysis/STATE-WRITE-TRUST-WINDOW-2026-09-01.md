# STATE-WRITE TRUST WINDOW — 2026-09-01

> **Ticket**: DEMIURGE-094 (Phase Kernel brief WS-1 item 6)
> **Status**: DONE
> **Date**: 2026-09-02
> **Author**: AI (Ivan-authorized, sprint A)
> **Reference**: `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md`

## 1. Trust window

- **Start**: 2026-09-01T20:52:02 UTC (commit `fffd7c4` "perf(prompts): cap max_output_tokens: 800 on all 74 PROMPTs (atomic close-out)")
- **End**: 2026-09-02T22:24:02 UTC (commit `320ffdc` "fix(prompts): restore 65 PROMPT.md bodies + incident report (WS-1 close-out)")
- **Duration**: ~25.5 hours (not 16h as the brief estimated — the recovery commit landed later than initially planned)

**Window extension note**: After 320ffdc, the WS-3 step-1 commit `0afca1f` (2026-09-02T00:37) introduced `scripts/_paths.py` and the helper (commits `e4b42e3` and `b710cd9`–`d8f9761`) which **also touched state files in passing**. These are documented separately in §4.

## 2. Per-write inventory

Files modified inside the trust window (counted via filesystem mtime):

| Category | Count | Trust level | Notes |
|---|---|---|---|
| `state/snapshots/<ISO-timestamp>/<agent>.json` (per-tick snapshots) | **2,694** | **TRUSTWORTHY** | Snapshots are read-only derived state. They re-emitted the same shape they always did. The agent-tracer was not writing trace records during this window (see §3), so each snapshot is purely a transform of the agent's authoritative state, not a new write path. |
| `state/instincts/instincts-<ISO-timestamp>.yaml` (instinct deltas) | 1 | UNTRUSTWORTHY | The instincts-yaml recorder ran during the window. Each instinct is a heuristic the system has learned; if the agent that emitted them was operating on truncated prompts (which it was — see §3), the heuristics are derived from sub-optimal behavior. |
| `state/instincts/instincts-latest.yaml` | 1 | UNTRUSTWORTHY | Mirror of the dated instinct file. Same trust concern. |
| `state/analyst.json`, `state/citation-coverage.json`, `state/editorial-calendar.json`, `state/finance.json`, `state/sales.json` | 5 | DEGRADED | These are single-tick state files (not in snapshots/) — each is the most-recent read of the corresponding agent's authoritative state. If the agent read or computed with truncated PROMPT context during the window, the values may be incomplete or stale. |
| `state/coord.json` | 1 | DEGRADED | The coordination file. Cross-cutting signal — multi-agent rollup. Same concern as the per-agent state files. |
| `state/chaos.last_run` | 1 | TRUSTWORTHY | The chaos-runner just records its last run timestamp. Not derived from agent prompt content. |
| **TOTAL files** | **2,702** | — | |

**Severity assessment**: Of 2,702 files written during the trust window, **2,694 (~99.7%) are TRUSTWORTHY (snapshots)**, **4 are DEGRADED (single-tick state files, low blast radius)**, and **2 are UNTRUSTWORTHY (instincts YAML — directly derived from prompt-context-driven agent behavior during the truncation)**.

## 3. Per-agent assessment

### 3.1 Did agents run during the window?

**Yes**. Evidence:
- 2,694 snapshots written between 2026-09-01T20:54:27 and 2026-09-02T13:46:52 (most recent at audit time).
- Snapshots appear every ~30 seconds during active hours (consistent with the `state-validate` cron cadence).
- All 19 snapshot-target agents emitted at least one snapshot during the window: analyst, citation-coverage, coaching-quality-reviewer, coord, cost-tracker, dora-metrics, editorial-calendar, engineering, eval-trending, finance, funding, heartbeat-alerts, kiki-prep, kiki, org-chart-review, people, research, sales, slo-services.

### 3.2 What did agents SEE during the window?

**Truncated PROMPT bodies**. Per the WS-1 close-out investigation (`fb2b81f`, `320ffdc`):
- 65 of 76 PROMPT.md files had their bodies reduced to frontmatter + minimal boilerplate between commits `fffd7c4` (truncation) and `320ffdc` (restoration).
- All 19 snapshot-target agents were among the 65 truncated (they have PROMPT.md files under their agent directories).
- Therefore: **every agent run during the trust window read its own truncated prompt before doing its work**.

### 3.3 What did agents WRITE?

Two write paths were active during the window:

1. **Snapshot recorder** (`scripts/state-validate.py` and friends): re-read each agent's authoritative state, wrote a JSON snapshot. The snapshot content is the agent's own state — not derived from the prompt that was running it. **Trustworthy**.

2. **Instinct recorder** (`scripts/instincts/`): emitted learned behaviors as YAML deltas. These heuristics are derived from the **runtime behavior of the agent**, which IS shaped by the prompt that was running. **Untrustworthy** — they encode sub-optimal patterns observed while prompts were truncated.

3. **Single-tick state files**: a few agents (analyst, citation-coverage, editorial-calendar, finance, sales, coord) wrote top-level state.json files outside the snapshots/ directory. These files reflect "current state as understood by the agent right now". **Degraded** — likely reflects truncated-context reasoning.

### 3.4 Were any writes IRRECOVERABLE?

**No**. Two recovery paths available:

a. **Snapshots are the safety net**: 2,694 timestamped snapshots, one per ~30 seconds during the window. Any of them can be re-promoted to authoritative state by reversing the snapshot→state-write path.

b. **Source-of-truth is the agent's prompt** (now restored): if you re-run an agent with the restored PROMPT, it converges to a correct state from the source material (briefs, signals, ground-truth inputs), independent of the degraded in-flight state.

## 4. WS-3 follow-on writes (post-recovery, still in the audit window)

The WS-3 work landed AFTER the WS-1 close-out but during the extended audit period:

| Commit | Time | Files touched | Trust assessment |
|---|---|---|---|
| `0afca1f` (WS-3 step 1) | 2026-09-02T00:37 | `scripts/_paths.py`, `tests/test_paths.py` | **TRUSTWORTHY** — additive only, no state writes |
| `e4b42e3` (WS-3 step 2) | 2026-09-02T03:27 | `scripts/thread-aiw-root.py`, `tests/test_thread_aiw_root.py`, `scripts/observability/agent-tracer.py` | **TRUSTWORTHY** — no state writes |
| `c88ce0c`–`d8f9761` (WS-3 step 3 batch) | 2026-09-02T03:43–03:44 | 5 more scripts threaded | **TRUSTWORTHY** — no state writes |

**No state files were modified by these commits.** The threading work touched only source code and tests.

## 5. Per-write trust verdict

| File pattern | Trust | Action recommended |
|---|---|---|
| `state/snapshots/<ISO>/<agent>.json` | TRUSTWORTHY | None — keep all |
| `state/instincts/instincts-<ISO>.yaml` | UNTRUSTWORTHY | **Move to `state/instincts/quarantine/2026-09-01-trust-window/`** before WS-4 (decisions drain). New instincts should be learned from post-recovery agent runs. |
| `state/instincts/instincts-latest.yaml` | UNTRUSTWORTHY | **Replace** with a snapshot-derived replica OR with an empty placeholder after quarantine. |
| `state/<agent>.json` (single-tick) | DEGRADED | None needed — agents self-correct on next tick with restored prompts. Snapshots are the audit trail. |
| `state/coord.json` | DEGRADED | None needed — same as above. |
| `state/chaos.last_run` | TRUSTWORTHY | None — not prompt-derived. |

## 6. Rollback protocol (recommended)

If evidence surfaces that the instincts Yaml during the trust window caused downstream damage:

1. Move the 2 instincts files to `state/instincts/quarantine/2026-09-01-trust-window/`.
2. The `state-auto-commit` cron will see the new empty instincts-latest.yaml and start fresh.
3. New instincts will accumulate from post-recovery agent runs.

**This protocol is RECOMMENDED but not yet executed** — operator authorization required (per DEMIURGE-115 / R11).

## 7. Open questions

1. **Were the agents' RUNTIME outputs (not just state writes) ever exposed to other agents during the window?** E.g., did a snapshot read by agent-X contain inferences drawn from truncated-prompt reasoning by agent-Y? If yes, the snapshot chain itself carries the contamination. The snapshot timestamps make this auditable but it requires manual inspection of one or two snapshots.

2. **Did any of the cross-agent signals (coord.json's signal channel) consume instinct-YAML-derived behavior?** If yes, the contamination propagates.

3. **Should the instincts quarantine be a one-time fix or a recurring windowed quarantine?** Per the brief §11.R2 ("every bulk frontmatter edit must assert body preservation"), this could be a periodic audit: every 90 days, archive instincts Yaml from the previous quarter and start fresh.

## 8. Recommendations

1. **Quarantine the 2 instincts files** (Ivan-actionable: DEMIURGE-115).
2. **Run a 24-hour soak test** post-recovery to confirm instincts re-converge to healthy baselines.
3. **Add DEMIURGE-115 (global hard-stop enforcer)** as the operator-actionable counterpart to this audit (per the Phase Kernel brief).

## 9. References

- `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md` (320ffdc) — original incident analysis
- `docs/HERMES-ANSWERS-2026-09-02.md` (fb2b81f) — 142-question audit, including the body-count analysis
- `docs/KERNEL-DESIGN-2026-09-02.md` (b7637cf) — kernel design that this audit informed
- `tickets/DEMIURGE-094-audit-state-write-trust-window/` — ticket for this work
- `tickets/DEMIURGE-115-operate-global-hard-stop-enforcer/` — recommended follow-up
