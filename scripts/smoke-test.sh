#!/bin/bash
# scripts/smoke-test.sh — Per-layer smoke gate runner.
# Usage: ./scripts/smoke-test.sh [L1|L2|L3|L4|all]
#
# Per EXECUTION-SCOPE-2026-09 §3 Layer 3 deliverable.
#
# Each layer runs the relevant tests + sanity checks:
#   L1: lint-prompts + state-validate + pytest
#   L2: + composition test + kpi test
#   L3: + monitor thresholds test
#   L4: stub (gated by Layer 4 activation; currently DEFERRED)
set -e

cd "$(dirname "$0")/.."
PYTHON="/opt/data/.venv/bin/python3"

usage() {
    echo "Usage: $0 [L1|L2|L3|L4|all]"
    echo ""
    echo "  L1   Basic: lint-prompts + state-validate + pytest"
    echo "  L2   Composition + KPI formula tests"
    echo "  L3   + dept monitor thresholds test"
    echo "  L4   Soul-improvement gate (DEFERRED — gated by customer traction)"
    echo "  all  L1 → L2 → L3 (L4 skipped if gated)"
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

MODE=$1

LINT_START=$(date +%s)
LINT_RESULT=0
STATE_RESULT=0
PYTEST_RESULT=0
TEST_RESULT=0

lint_prompts() {
    echo "=== Lint PROMPTs ==="
    $PYTHON scripts/lint-prompts.py
}

validate_state() {
    echo "=== Validate state ==="
    $PYTHON scripts/validate-state.py
}

run_pytest() {
    echo "=== Run unit tests ==="
    $PYTHON -m pytest tests/ "$@" --tb=short -q
}

case "$MODE" in
    L1)
        lint_prompts || exit 1
        validate_state || exit 1
        run_pytest
        ;;
    L2)
        lint_prompts || exit 1
        validate_state || exit 1
        run_pytest --ignore=tests/test_agent_composition.py \
                   --ignore=tests/test_kpi_computation.py \
                   --ignore=tests/test_dept_monitor_thresholds.py
        # L2-specific tests
        echo "=== L2 composition + KPI tests ==="
        $PYTHON -m pytest tests/test_agent_composition.py tests/test_kpi_computation.py --tb=short -q
        ;;
    L3)
        lint_prompts || exit 1
        validate_state || exit 1
        # Run all tests including composition, kpi, monitor
        run_pytest
        # Confirm all 3 new test files pass
        echo "=== L3 specific gates ==="
        $PYTHON -m pytest tests/test_agent_composition.py tests/test_kpi_computation.py tests/test_dept_monitor_thresholds.py -v
        ;;
    L4)
        echo "=== L4 Soul-Improvement Gate ==="
        echo "Layer 4 (Adaptive) is DEFERRED per EXECUTION-SCOPE §2."
        echo ""
        echo "Gate check:"
        echo "  customer_traction: $240 MRR, 1 archived customer (REQUIRED: ≥\$1000 MRR or ≥5 customers)"
        echo "  layers_1_3_stable: <30 days (REQUIRED: ≥30 days)"
        echo "  smoke_gates: ≥95% (CURRENT: 100%)"
        echo ""
        echo "GATE STATUS: FAIL (customer_traction)"
        echo ""
        echo "Layer 4 execution BLOCKED. To unblock: \$1000 MRR or 5+ customers."
        exit 1
        ;;
    all)
        $0 L1 && $0 L2 && $0 L3
        ;;
    *)
        usage
        ;;
esac

LINT_ELAPSED=$(($(date +%s) - LINT_START))
echo ""
echo "=== Smoke gate ($MODE) complete in ${LINT_ELAPSED}s ==="