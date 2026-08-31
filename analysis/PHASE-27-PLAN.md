# Phase 27 — Decisions Applied + Execution Plan

> **Date**: 2026-09-01
> **Trigger**: Ivan's decisions on Phase 26 queued items
> **Status**: 3 decisions received; 2 of 3 = "yes execute"; 1 = "skip + defer"

---

## Decisions received

| ID | Owner | Decision | Action |
|---|---|---|---|
| D1 | Ivan | **c** — Skip sales funnel revival, defer to Q1 2027 | Document skip; archive funnel-revival.md as deferred |
| D2 | Kiki | **a** — Invoke hard-stops wrapper globally (8-16h) | Build integration (this turn) |
| D8 | Kiki | **a** — Eval gate enforcement with override (8h) | Build enforcement hook (this turn) |

---

## Execution plan

### R1: Hard-stops wrapper invocation (D2 = a)

The wrapper at `patterns/hard-stop-wrapper.py` exists but has a bug: line 118 hard-codes `allowed = True` (it does nothing). This is the actual fix.

**Sub-steps:**
1. Fix `--check` mode to actually call `check_action()` against the agent's PROMPT.md (not hard-coded allow)
2. Add a thin Python wrapper module `patterns/hardstop_check.py` that agents can `import`
3. Add `--log` flag to record every check (audit trail)
4. Find the 8-12 agents with destructive actions (per `STANDARD_ACTIONS`) and add an invocation snippet to their PROMPT.md
5. Add tests (6-8 tests covering allow/block + audit log)

**Effort estimate**: 6-10h actual work (will be faster; the wrapper logic already exists)

### R2: Eval gate enforcement (D8 = a, with override)

**Sub-steps:**
1. Build `scripts/eval-gate-enforce.py` — reads `eval-trending.json`, returns decision (allow / block / warn)
2. Add override mechanism: `--force` flag with operator note + audit log entry
3. Wire as a pre-cron-hook in cron jobs that have destructive writes (only the 8-12 high-risk agents from R1)
4. Add tests (5-6 tests)
5. Add a daily audit cron that records gate decisions

**Effort estimate**: 4-6h

### R3: JSON schema validation at write-time (from chaos finding)

**Sub-steps:**
1. Build `scripts/schema-validate-write.py` — validates a state file against its JSON schema before write
2. Apply to the 7 dept-lead state files (coord, finance, sales, engineering, research, people, funding)
3. Add tests (4-5 tests)
4. Wire as a wrapper around state writes (in `scripts/state-write.sh` or similar)

**Effort estimate**: 3-4h

### R4: Verify + commit + feedback

---

## What gets DEFERRED (D1 = c)

**Sales funnel revival** (Formspree vs Worker) is explicitly deferred to Q1 2027 per Ivan's decision.

Action: Mark `sales/funnel-revival-2026.md` as deferred, add to `REVIEW-2027-Q1.md` as a top priority.

---

## Sequencing

- R1 first (foundation: hard-stops must work before eval-gate can use them)
- R2 second (depends on R1's audit log + agent list)
- R3 third (independent, but uses same patterns)
- R4 verify + commit

---

## Risks

| Risk | Mitigation |
|---|---|
| Hard-stops wrapper breaks working agents | Use `--allow-fallback` flag for first 7 days; logs all blocked actions but doesn't block |
| Eval-gate enforcement blocks too many agents | Threshold = 30% (not 50%) initially; ramp up after 30d data |
| Schema validation rejects legitimate state | Allowlist fields per schema; schema files reviewed by Kiki before R3 ships |

---

## Total effort

~14-20h actual work. Should fit in this session + 1 follow-up.

## Cross-references

- `analysis/PHASE-26-DECISIONS.md` — source decisions
- `operations/hard-stops-enforcement-audit.md` — the gap we're closing
- `engineering/ai-safety-posture-2026.md` — Gap G1 (hard-stops)
- `scripts/eval-aggregate-pass-rate.py` — R2's input data
- `patterns/hard-stop-wrapper.py` — R1's starting point
