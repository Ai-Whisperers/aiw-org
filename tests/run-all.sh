#!/bin/bash
# tests/run-all.sh — Layer 2.4 update: run pytest + lint-prompts + state validation
cd "$(dirname "$0")/.."

# Smoke gate 1: lint all PROMPT.md files (Doctrine 2 enforcer)
echo "=== Lint PROMPTs ==="
/opt/data/.venv/bin/python3 scripts/lint-prompts.py || exit $?

# Smoke gate 2: validate state files
echo "=== Validate state ==="
/opt/data/.venv/bin/python3 scripts/validate-state.py || exit $?

# Smoke gate 3: run all unit tests
echo "=== Run unit tests ==="
exec /opt/data/.venv/bin/python3 -m pytest tests/ "$@"
