#!/usr/bin/env bash
# pre-commit-citation-coverage.sh
#
# Citation coverage guard — blocks commits to research/ files with 0 citations.
#
# Built Phase 7 R5 (implementation plan §4 Phase 2.2).
# Companion to pre-commit-cron-guard.sh. Both run from .git/hooks/pre-commit.
#
# Behaviour:
#   - If any staged file is under research/ AND ends with .md
#     AND has 0 detectable citations, fail the commit.
#   - If --no-verify is passed (Ivan bypass), skip this guard.
#   - Other commits (non-research/) are unaffected.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT="$REPO_ROOT/scripts/citation-coverage-enforcer.py"
PYTHON="${PYTHON:-/opt/data/.venv/bin/python3}"

# Skip if bypass flag
if [ "${GIT_REFLOG_ACTION:-}" = "_BYPASS_" ]; then
    exit 0
fi

# Find staged research/ markdown files
STAGED=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)
RESEARCH_FILES=""
for f in $STAGED; do
    case "$f" in
        research/*.md)
            RESEARCH_FILES="$RESEARCH_FILES $f"
            ;;
    esac
done

# No research files staged — pass
if [ -z "$RESEARCH_FILES" ]; then
    exit 0
fi

# Check that the script exists
if [ ! -f "$SCRIPT" ]; then
    echo "WARN: $SCRIPT missing — citation guard skipped" >&2
    exit 0
fi

# Run citation check on staged files only
echo "Checking citations for $RESEARCH_FILES..."

# Use --files mode + --strict to fail on 0-citation files
if ! "$PYTHON" "$SCRIPT" --strict --threshold 1 --files $RESEARCH_FILES > /tmp/citation-check.out 2>&1; then
    echo "" >&2
    echo "❌ CITATION COVERAGE FAILED" >&2
    echo "" >&2
    echo "One or more staged research files have 0 citations." >&2
    echo "Either:" >&2
    echo "  1. Add citations (DOI, arXiv, URL, footnote, bibtex, APA inline)" >&2
    echo "  2. Use git commit --no-verify if this is an emergency fix" >&2
    echo "" >&2
    cat /tmp/citation-check.out >&2
    exit 1
fi

# Clean up tmp
rm -f /tmp/citation-check.out

exit 0