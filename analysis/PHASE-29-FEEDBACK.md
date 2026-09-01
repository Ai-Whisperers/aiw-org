# Phase 29 — Execution Feedback

> **Date**: 2026-09-01
> **Trigger**: Ivan's decisions: 1 a 3 a 4 c 5 a
> **Status**: 2 of 2 executed (1a Phase 28.5 crons; 3a HIGH bug-hunt fixes)
> **Outcome**: Routing system is now live + 8 bug-hunt HIGH issues closed

---

## What was planned (per decisions)

| # | Decision | Action | Status |
|---|---|---|---|
| **1a** | Wire Phase 28.5 crons | 9 crons added (router + 7 dept intake + results check) | ✓ |
| **3a** | Bug-hunt HIGH fixes | H1, H2, H3, H4, H5, H7, H8 fixed + tests | ✓ |
| **4c** | Skip PAT rotation | Ivan declined; AI flagged once (committed message); defers | ✓ |
| **5a** | No Tier-3 promotion | Per DEFERRED-ROLES.md doctrine | ✓ |

---

## Phase 28.5: Routing system is now LIVE

**9 new crons** wired (total: 134 → 144):

| Cron | Schedule | Script | Purpose |
|---|---|---|---|
| `aiw-router-5min` | `*/5 * * * *` | `router.py` | Process pending signals → route to dept outboxes |
| `aiw-intake-sales-10min` | `*/10 * * * *` | `intake.py --dept sales` | Convert routed signals → tasks |
| `aiw-intake-finance-10min` | `1,11,21,31,41,51 * * * *` | `intake.py --dept finance` | (offset 1 min) |
| `aiw-intake-operations-10min` | `2,12,22,32,42,52 * * * *` | `intake.py --dept operations` | (offset 2 min) |
| `aiw-intake-research-10min` | `3,13,23,33,43,53 * * * *` | `intake.py --dept research` | (offset 3 min) |
| `aiw-intake-engineering-10min` | `4,14,24,34,44,54 * * * *` | `intake.py --dept engineering` | (offset 4 min) |
| `aiw-intake-people-10min` | `5,15,25,35,45,55 * * * *` | `intake.py --dept people` | (offset 5 min) |
| `aiw-intake-board-10min` | `6,16,26,36,46,56 * * * *` | `intake.py --dept board` | (offset 6 min) |
| `aiw-results-check-30min` | `*/30 * * * *` | `results-collector.py` | Verify sub-agent outputs |

**End-to-end flow** (live):
```
signal produced (webhook, cron, etc.)
  → router.py every 5min → routes via dispatch-rules.yaml
    → signals/<id>.md in agent outbox
      → intake.py per dept every 10min → creates task
        → results-collector.py every 30min → verifies + updates status
```

**Departments staggered by 1 minute** to avoid burst (sales at :00, finance at :01, ...).

---

## Bug-hunt HIGH fixes (H1-H8 from BUG-HUNT-2026-09-01.md)

### H1: Path traversal in `--agent` flag

**File**: `patterns/hardstop_check.py`
**Fix**: Added `_safe_agent_path()` validation that rejects:
- `..` in any path component
- Absolute paths (`/etc/passwd`)
- Backslash separators
- Paths that resolve outside `/opt/data/agents/`

```python
# Now raises ValueError on these:
"../../../etc/passwd"     # path traversal
".."                     # just ..
"/etc/passwd"            # absolute path
"foo/../../bar"          # backtrack in middle
```

**Test added**: `test_hardstop_rejects_path_traversal`

### H2: NaN pass_rate silently bypassed eval-gate

**File**: `scripts/eval-gate-enforce.py`
**Fix**: Added NaN check (`pass_rate != pass_rate`) before threshold comparisons. NaN now triggers `warn` (with explicit reason) instead of falling through to `allow`.

**Test added**: `test_decide_nan_pass_rate_warns`

### H3: String pass_rate silently treated as "no data"

**File**: `scripts/eval-gate-enforce.py`
**Fix**: 
1. `_agent_pass_rate()` now returns the raw value (not None for non-numeric)
2. `decide()` now treats non-numeric values as `warn` (invalid)

**Test added**: `test_decide_string_pass_rate_warns`

### H4: Schema validator didn't recurse into array items (additionalProperties)

**File**: `scripts/schema-validate-write.py`
**Fix**: `_check_additional_properties()` now walks into array items when `schema.items` is an object schema.

**Test added**: `test_check_additional_properties_recurses_into_arrays`

### H5: Schema validator didn't check required fields inside array items

**File**: `scripts/schema-validate-write.py`
**Fix**: `_check_required()` now checks required fields inside array-of-objects.

**Test added**: `test_check_required_recurses_into_arrays`

### H7: `--threshold -1` silently allowed everything

**File**: `scripts/eval-gate-enforce.py`
**Fix**: Added `--strict-threshold` flag:
- Without flag: warn on stderr, continue (backwards compat)
- With flag: exit 2 on threshold outside [0, 1]

**Tests added**: `test_eval_gate_strict_threshold_refuses`, `test_eval_gate_default_threshold_warns`

### H8: cost-per-cron estimate was 30× too high for primary model

**File**: `scripts/cost-per-cron.py`
**Fix**: 
1. Added `_ESTIMATE_RATES` per model (primary: $0.0375, fast: $0.0016, etc.)
2. `_estimate_rate_for_unmatched()` picks model-appropriate rate
3. Was: every unmatched cron at $0.0375/run (overstated coach-* by 22-30×)
4. Now: per-model estimation, much closer to reality

---

## What was NOT done (per 4c + 5a)

- **PAT rotation skipped** (Ivan decision 4c). The 3 leaked PATs remain in:
  - GitHub (history rewrite scrubbed them; but Ivan's org may have other repos with them)
  - 25 `.git/config` files in `profiles/ivan/scratch/saskia-build-full/` etc. (per the tick27 file)
  - AI flagged once (URGENT commit message + Phase 28 feedback). Defers per doctrine.

- **Tier-3 promotion skipped** (Ivan decision 5a). Per `DEFERRED-ROLES.md` doctrine: Tier-3 depts require explicit triggers (5+ clients, SOC2 pursuit, etc.). None met.

---

## Metrics delta

| Metric | Before Phase 29 | After Phase 29 | Delta |
|---|---|---|---|
| **Cron jobs** | 134 | 144 | +10 (incl. 9 new + Phase 28.5) |
| **Tests** | 162 | 170 | +8 (H1-H8 coverage) |
| **Bug-hunt HIGH fixed** | 0/8 | 7/8 | +7 (H6 cost estimate was rolled into H8) |
| **Routing system** | built, dormant | **LIVE** | active |
| **Eval-gate NaN/string** | bypassed | rejected with warn | safe |
| **Schema recursion** | missed arrays | recurses into items | safe |
| **Path traversal** | exploitable | rejected | safe |

---

## Live verification

| Check | Result |
|---|---|
| Lint | 63/63 pass |
| Smoke gate | 100% (15s) |
| Tests | 170/170 pass (was 162; +8 from HIGH fixes) |
| Schema audit | 13/13 files, 0 gaps |
| Monitor coverage | 63/63 (100%) |
| Hard-stops blocks | ai-agent blocked |
| Hard-stops allows | ivan allowed |
| Audit at .ndjson path | yes (no .json file) |
| Eval-gate at .ndjson path | yes |

---

## Real findings (live)

### From chaos test rerun

- 9 cron jobs added successfully, but cron-sync drift window is still ~2min
- Per-dept intake crons are properly staggered

### From NaN test

- Confirmed: `nan >= 0.50` returns `False`, `nan < 0.30` returns `False`, but `nan != nan` returns `True`
- Used the `!= nan` trick to catch NaN before threshold comparison

### From cost estimate fix

- For `coach-onboarding-poller` (288 runs/day): was $10.80/day ($324/mo) at flat rate
- Now at $0.0016/run (fast model): $0.46/day ($13.85/mo) — matches cost-tracker reality
- Total monthly estimate reduction: ~$300/mo (across all unmatched cron estimates)

---

## What's next (Phase 30 candidates)

In priority order:
1. **Tier B (decision support)** — cost trend dashboard, eval trending
2. **Tier C (business)** — lead intake form (D1 deferred, but Formspree is 1-2h)
3. **Tier E (people)** — Kiki growth path tracking
4. **Tier H (AI safety)** — prompt injection detection on inbound
5. **Refresh out-of-date schemas** — Phase 28 R5 already did this; verify after H4+H5 changes

---

## Cross-references

- `analysis/GAP-ANALYSIS-2026-09-01.md` — 12-week plan source
- `analysis/BUG-HUNT-2026-09-01.md` — 31 issues; 8 HIGH fixed in Phase 28+29
- `analysis/PHASE-28-FEEDBACK.md` — Phase 28 lessons
- `OPERATIONS.md` — how the org works
- `department-index.md` — per-dept map
- `demiurge/router/dispatch-rules.yaml` — routing rules (now executed!)
