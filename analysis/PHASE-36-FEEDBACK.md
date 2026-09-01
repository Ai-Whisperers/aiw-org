# Phase 36 — Feedback (More Multilingual + Cron Auto-Fix Apply + Wrapper Wildcard + Edge Cases + Audit)

> **Date**: 2026-09-01
> **Trigger**: Ivan "all defaults ok" (a a b b a)
> **Status**: 5/5 decisions applied
> **Outcome**: 4 new langs (15 patterns), 6 crons staggered, wildcard + sensitive_action, 2 edge cases, audit 12/12

---

## Decisions applied

| # | Decision | Action |
|---|---|---|
| **Q1a** | More multilingual KO/VI/ID/HI | 8 new patterns + 4 red-team scenarios. All 4 langs detected (exit 1). |
| **Q2a** | Cron auto-fix in production | Applied 6 stagger candidates live. **Found + fixed critical bug** (jobs.json structure flattened to bare list). |
| **Q3b** | Wrapper wildcard with sensitive_action | New `sensitive_action: true` field. Wildcard allows all EXCEPT sensitive actions. 2 new tests. |
| **Q4b** | 2 more red-team edge cases | false_positive_ignore_cached + mixed_language_ru_en. Both pass. |
| **Q5a** | Full audit + bug-hunt | audit-fresh 12/12, lint 63/63, tests 219/219, no critical bugs. |

---

## What was built (15 patterns + 6 scenarios + 1 cron fix + 1 bug fix + 2 tests)

### Scripts (1 modified + 1 bug fix)

| Script | Change |
|---|---|
| `scripts/cron-autofix.py` | Hardened: handle both wrapped `{jobs: [...]}` and bare list structures |
| `scripts/prompt-injection-check.py` | +8 multilingual patterns (KO/VI/ID/HI × 2 each) |
| `scripts/red-team-scenarios.py` | +6 scenarios (4 KO/VI/ID/HI + 2 edge cases) |

### Wrapper change (R3)

`patterns/hard-stop-wrapper.py:check_action()` now supports `sensitive_action: true` field. When wildcard (`*`) is present, sensitive actions still require approval.

Example:
```yaml
hard_stops:
  - mode: whitelist
  - action: "*"
  - action: delete_resource
    sensitive_action: true
    approval_required: true
    approved_human: ivan
  - action: force_push
    sensitive_action: true
    approval_required: true
    approved_human: ivan+kiki
```

### Tests (2 new)

- `test_check_action_wildcard_with_sensitive_action`: verifies override
- `test_check_action_wildcard_without_sensitive_actions`: regression

### Cron fix (R2)

**Critical bug found + fixed**: Phase 35 R1's `cron-autofix.py --apply` wrote a **bare list** `[...]` to jobs.json instead of the wrapped `{"jobs": [...]}`. The original canonical file at `/opt/data/cron/jobs.json` had the correct structure; only `.hermes/cron/jobs.json` was corrupted.

**Fix**:
- Restored `.hermes/cron/jobs.json` to correct structure (from canonical)
- Patched `cron-autofix.py` to handle both structures safely
- Stagger applied 6 crons live (off by 1-2 minutes from existing schedule)

### Multilingual coverage (Phase 36 R1)

| Lang | Patterns | Status |
|---|---|---|
| Korean (ko) | 2 | ✅ detected |
| Vietnamese (vi) | 2 | ✅ detected (case-insensitive flag) |
| Indonesian (id) | 2 | ✅ detected (case-insensitive flag) |
| Hindi (hi) | 2 | ✅ detected (no flag needed) |

**15 languages total now supported** (was 11). 30+ patterns total.

---

## Live test results

### Canonical gates

```
Lint:        63/63 pass
Smoke gate:  100% pass
Tests:       219/219 pass (was 217; +2 wrapper tests)
Audit:       12/12 (100%)
```

### Red-team (Phase 36 R1 + R4)

```
Scenarios:    38 (was 32; +6 new)
Injection:    38/38 (100%)
PII:          38/38 (100%)
Both passed:  38/38 (100%)
```

### Multilingual test matrix

```
EN ES FR DE PT IT NL RU CN JP AR KO VI ID HI = 15 langs
All 4 new langs (KO/VI/ID/HI) detected live.
```

### Audit-fresh

```
Total jobs: 149 (unchanged)
Enabled: 133
Disabled: 0 (all safe ones resumed in Phase 34)
Tests: 219 pass
Audit log entries: 1338
No secrets: 0 leaks
```

---

## What was NOT done

- **Token plan upgrade**: depends on Kiki/finance decision. 6 cron failures still token_plan (Sunday auto-recover).
- **More multilingual** (next session): Persian, Bengali, Turkish, Polish, Czech, etc.
- **Apply remaining 5 stagger candidates**: Phase 35 R1 found them; Phase 36 R2 found + applied 6; 5 more pending (now in R2 dry-run).

---

## Findings

### 1. Critical bug: jobs.json structure (R2)

**Before**:
- `.hermes/cron/jobs.json` was bare list `[...]` (broken by Phase 35 R1)
- `/opt/data/cron/jobs.json` was wrapped `{"jobs": [...]}` (correct)

**After**:
- Both files have correct structure
- `cron-autofix.py` now handles both structures (forward-compatible)

**Impact**: Could have caused runtime issues if a cron reader expected `{"jobs": [...]}` and got a list. **Now safe**.

### 2. Multilingual pattern design (R1)

For non-Latin scripts (KO/VI/ID/HI), discovered 3 things:
1. `\b` word boundaries don't work → use `{0,N}` instead
2. Word order varies → use bidirectional patterns (A→B OR B→A)
3. Case-sensitive diacritics (VN/ID) → use `re.IGNORECASE | re.UNICODE`

### 3. Wrapper wildcard + sensitive (R3)

Discovery: wildcard mode needs an explicit "override" mechanism. The `sensitive_action: true` field is the cleanest way to say "this action is also blocked even though wildcard says everything is allowed". Backward-compatible (entries without `sensitive_action` behave as before).

---

## Metrics delta

| Metric | Before Phase 36 | After Phase 36 | Delta |
|---|---|---|---|
| Crons staggered (this turn) | 0 | 6 | +6 |
| Total staggered (lifetime) | 16 | 22 | +6 |
| Multilingual patterns | 22 | 30 | +8 |
| Languages supported | 11 | **15** | +4 |
| Red-team scenarios | 32 | **38** | +6 |
| Red-team pass rate | 100% | **100%** | unchanged |
| Wrapper tests | 24 | 26 | +2 |
| Total tests | 217 | **219** | +2 |
| Audit-fresh score | 12/12 | **12/12** | unchanged |
| Cron jobs.json bug | broken | **fixed** | +1 |

---

## Phase 37 candidates (next session, per scope)

In priority order:
1. **Apply remaining 5 stagger candidates** (~5min)
2. **More multilingual** (~3h): Persian, Bengali, Turkish, Polish
3. **Wrapper wildcard with rate-limit** (~2h): combine wildcard with rate_limit_per_run
4. **Token plan upgrade** (depends on Kiki/finance)
5. **Audit cron-autofix on real cron registry** (~1h): verify all 149 jobs OK

Total: ~6h focused eng+devops+AI-safety work.

---

## Cross-references

- `analysis/PHASE-35-FEEDBACK.md` — prior phase
- `analysis/PHASE-36-PLAN.md` — this phase plan
- `state/cost-optimization-report.md` — R2 source (6 candidates applied)
- `state/red-team-report.md` — 38/38 pass
- `state/audit-fresh.md` — 12/12 pass
- `state/cron-autofix-audit.ndjson` — R2 audit log
- `patterns/hard-stop-wrapper.py` — wildcard + sensitive_action
- `scripts/cron-autofix.py` — hardened (handles bare list)
- `scripts/prompt-injection-check.py` — 30 patterns
- `scripts/red-team-scenarios.py` — 38 scenarios
