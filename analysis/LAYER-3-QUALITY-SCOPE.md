# Layer 3 — Quality Infrastructure — Scope

> **Status**: Active. AI proceeding autonomously per Ivan's directive (2026-09-01).
> **Owner**: AI (6-10h) + Ivan (1-2h review)
> **Total time**: 8-12h
> **Reversibility**: Full per task (each test independently committable)

---

## Goal

Add the testing + eval-gate scaffolding the runtime agents need. Layer 3 makes the system **measurable**: every agent behavior has a test, every KPI formula has a unit test, every dept monitor has a threshold spec. **Layer 3 ships when pytest coverage of `scripts/` and `demiurge/` exceeds 80%, all 7 new test files pass, and the smoke gate runs in <10s.**

---

## Per-task scope

### L3.1 — Update `tests/run-all.sh` to use pytest (already done in L2.4)

**What**: Layer 2.4 already replaced `unittest discover` with `pytest tests/` + 3-stage smoke gate. Verify coverage.

**Acceptance criteria**:
- [x] `tests/run-all.sh` uses pytest
- [x] pytest runs in <10s
- [x] 3 smoke gates: lint-prompts, validate-state, pytest
- [x] 48/48 tests pass (current state)

**Status**: ✅ DONE in L2.4 (commit `a2ef2f4`).

---

### L3.2 — Add `tests/test_agent_composition.py` (composition discipline enforcer)

**What**: Per `THREAT-MODEL.md MAA-1`, composition chains need bounded depth + non-existent-agent detection. New test file:

```python
def test_all_composition_refs_resolve():
    """Each agent's composition: list must reference agents that exist."""
    # Walk all PROMPT.md files, build composition graph
    # Fail if any reference points to non-existent agent
    
def test_no_circular_compositions():
    """No circular dependencies in composition graph."""
    # Build graph, detect cycles, fail if any
    
def test_max_composition_depth():
    """No agent has composition depth > 3 (max atomic→dept→board)."""
    # BFS from leaves, depth-limit to 3
    
def test_no_duplicate_composition():
    """No agent appears in multiple agents' composition as cross-cut."""
    # Cross-cut agents (hermes-router, argus-health-monitor) are allowed
    # but only if explicitly marked
```

**Acceptance criteria**:
- [ ] 4 tests pass
- [ ] All 39 non-empty composition refs resolve
- [ ] No circular dependencies detected
- [ ] Max depth ≤ 3 (current is 2: dept→atomic)
- [ ] ≤500 lines, runs in <2s

**Files affected**: `tests/test_agent_composition.py` (new)

**Rollback**: `git revert <commit>`

**Tokens**: ~800

---

### L3.3 — Add `tests/test_kpi_computation.py` (formula validator)

**What**: Per `demiurge/kpi/*.yaml` files (6 stacks, 33 KPIs total), each KPI formula needs to be syntactically parseable. New test:

```python
def test_all_kpi_files_parse():
    """Each yaml file is valid YAML."""
def test_each_kpi_has_required_fields():
    """id, name, formula, target, feedback_loop required."""
def test_kpi_ids_unique():
    """No duplicate KPI ids across files."""
def test_kpi_formula_references_known_signals():
    """Formula references resolve to known signals."""
def test_kpi_org_health_aggregator_exists():
    """kpi-org-health-score aggregator present in revenue-stack.yaml."""
def test_feedback_loops_resolve():
    """feedback_loop values reference existing agent routes."""
```

**Acceptance criteria**:
- [ ] 6 tests pass
- [ ] 6 yaml files parse
- [ ] 33 KPIs each have required fields
- [ ] No duplicate ids
- [ ] Aggregator exists
- [ ] ≤300 lines, runs in <1s

**Files affected**: `tests/test_kpi_computation.py` (new)

**Rollback**: `git revert <commit>`

**Tokens**: ~600

---

### L3.4 — Add `tests/test_dept_monitor_thresholds.py` (16-monitor spec validator)

**What**: Per `EXECUTION-SCOPE-2026-09 §3` and `GAP-RESEARCH-FINDINGS §S4`, 16 dept monitors exist with thresholds that aren't enforced. New test validates the threshold spec format:

```python
def test_all_monitor_specs_parse():
    """Each monitor spec is valid YAML/JSON."""
def test_each_threshold_has_severity():
    """warn/critical/fatal severity required."""
def test_thresholds_sorted_by_severity():
    """warn < critical < fatal ordering."""
def test_no_orphan_threshold_refs():
    """Each threshold's action references existing script."""
def test_at_least_one_critical_per_monitor():
    """Each monitor has at least one critical threshold."""
def test_16_monitors_in_spec():
    """The spec covers 16 monitors (not fewer, not many more)."""
```

**Acceptance criteria**:
- [ ] 6 tests pass
- [ ] Spec file exists at `demiurge/monitors/spec.yaml` (NEW)
- [ ] 16 monitors each with thresholds
- [ ] Severity ordering correct
- [ ] ≤400 lines, runs in <1s

**Files affected**: `tests/test_dept_monitor_thresholds.py` (new), `demiurge/monitors/spec.yaml` (new)

**Rollback**: `git revert <commit>`

**Tokens**: ~700

---

### L3.5 — Add `scripts/smoke-test.sh` (per-layer gate runner)

**What**: Per `EXECUTION-SCOPE §3`, each phase needs its own smoke gate. New shell script:

```bash
#!/bin/bash
# scripts/smoke-test.sh — run per-layer smoke gate
# Usage: ./scripts/smoke-test.sh [L1|L2|L3|L4|all]
case $1 in
    L1) ./scripts/smoke-test-l1.sh ;;
    L2) pytest tests/test_lint_prompts.py tests/test_kpi_computation.py ;;
    L3) pytest tests/test_agent_composition.py tests/test_dept_monitor_thresholds.py ;;
    L4) pytest tests/test_soul_gates.py ;;  # if exists
    all) ./scripts/smoke-test.sh L1; ./scripts/smoke-test.sh L2; ./scripts/smoke-test.sh L3 ;;
esac
```

**Acceptance criteria**:
- [ ] 4 modes: L1/L2/L3/L4 (L4 stubbed for future)
- [ ] All modes exit 0 if pass
- [ ] Per-mode timing reported
- [ ] Integrates with `tests/run-all.sh`

**Files affected**: `scripts/smoke-test.sh` (new), `tests/run-all.sh` (modified)

**Rollback**: `git revert <commit>`

**Tokens**: ~400

---

### L3.6 — Run pytest + coverage report; baseline numbers

**What**: First real measurement. Run `pytest --cov=scripts --cov=demiurge tests/` and capture results.

**Acceptance criteria**:
- [ ] `pytest-cov` runs successfully
- [ ] Coverage report generated (`htmlcov/` + `.coverage`)
- [ ] Baseline metrics saved to `analysis/BASELINE-COVERAGE-2026-09-01.json`
- [ ] Coverage ≥30% (low bar for first measurement; will grow)
- [ ] Run takes <30s

**Files affected**: `analysis/BASELINE-COVERAGE-2026-09-01.json` (new), `.gitignore` (whitelist `htmlcov/`)

**Rollback**: per-file revert

**Tokens**: ~200

---

### L3.7 — Layer 3 completion report + smoke gate

**What**: 
- Layer 3 completion report at `analysis/LAYER-3-QUALITY-COMPLETION-REPORT.md`
- Run `scripts/smoke-test.sh all`
- All L2 tests + L3 tests pass
- Coverage baseline captured
- Update wishlist + state

**Acceptance criteria** (Layer 3 → Layer 4 gate):
- [ ] All 4 new test files pass (test_agent_composition, test_kpi_computation, test_dept_monitor_thresholds, smoke-test.sh)
- [ ] Coverage ≥30% (baseline)
- [ ] Smoke gate runs in <10s
- [ ] 16-monitor spec exists
- [ ] Completion report committed
- [ ] Wishlist updated
- [ ] AI declares "Layer 3 complete"

**Files affected**: 3 docs + state/coord.json note

**Rollback**: per-commit revert

**Tokens**: ~600

---

## Layer 3 exit criteria

Layer 3 is DONE when:

1. All 7 tasks committed (granular commits per task)
2. Smoke gate passes (lint + state + pytest + smoke-test.sh)
3. Coverage ≥30% (baseline)
4. Completion report committed
5. Wishlist updated
6. AI announces "Layer 3 complete"

Then: **Layer 4 gate check** (customer traction).

---

## Layer 4 Gate Check (per `UPGRADE-PROPOSAL §12`)

Layer 4 is gated by **all three**:

| Gate | Current Status | Required |
|------|---------------|----------|
| Customer traction (MRR ≥ $1000 or N customers ≥ 5) | $240 MRR (0 active), 1 archived | ❌ FAIL |
| Layers 1-3 stable for 30 days | L1 done today, L2 done today, L3 done today | ⏳ Pending |
| Smoke gates ≥95% pass rate | Currently 100% | ✓ PASS |

**Layer 4 is gated by customer traction.** Per `EXECUTION-SCOPE §2 Layer 4 (Adaptive)`: "do deferred indefinitely" per Ivan's directive.

**Decision**: Layer 4 scope doc will be written as **DEFERRED**. AI will document the gate-check result but NOT execute Layer 4.

---

## Dependencies

- Layer 3 depends on Layer 2 (lint-prompts.py + composition fields + per-dept KPIs all from L2)
- Layer 4 conditional on L3 + customer traction

---

## Risks specific to Layer 3

| Risk | Mitigation |
|------|------------|
| test_agent_composition.py fails due to circular refs in current graph | Fix iteratively; check first 39 refs manually |
| Coverage is too low to call baseline | Cap at 30% as initial; iterate up |
| 16-monitor spec is aspirational (no actual monitors) | Define spec but mark as "stage 1 of 3" |
| Smoke-test.sh shell quoting bugs | Test all 4 modes in CI |

---

## Token budget

| Task | Estimate |
|------|----------|
| L3.1 (verify L2.4 done) | 50 |
| L3.2 (composition test) | 800 |
| L3.3 (KPI test) | 600 |
| L3.4 (16-monitor spec + test) | 700 |
| L3.5 (smoke-test.sh) | 400 |
| L3.6 (coverage baseline) | 200 |
| L3.7 (completion report) | 600 |
| **TOTAL** | **~3,350 tokens** |

This is the budget. AI self-monitors and pauses if any single task exceeds 2x estimate.

---

**AI is starting Layer 3 execution now. Per task:**
- Read context
- Apply changes
- Verify with smoke gate
- Commit granularly
- Document in wishlist

**Awaiting nothing** — Ivan said "go for all layers all phases." Proceeding.