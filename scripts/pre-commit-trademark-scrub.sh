#!/usr/bin/env bash
# pre-commit-trademark-scrub.sh — Stage-only trademark term check.
#
# Companion wrapper to patterns/trademark-scrub.sh. The underlying pattern
# script accepts a list of files as arguments; this wrapper discovers the
# staged files and passes them through.
#
# Exits 0 if no banned terms in staged changes, 1 otherwise.
# Bypass with `git commit --no-verify` (not recommended).

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PATTERN_SCRIPT="$REPO_ROOT/patterns/trademark-scrub.sh"

if [[ ! -f "$PATTERN_SCRIPT" ]]; then
    echo "WARN: $PATTERN_SCRIPT missing — trademark-scrub guard skipped" >&2
    exit 0
fi

# Only scan newly-staged files (introductions), not pre-existing state.
STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
if [[ -z "$STAGED" ]]; then
    exit 0
fi

# Filter to text-y files we want to scan (.md, .txt, .html, .json, .yaml, .yml, .py).
FILES_TO_CHECK=""
for f in $STAGED; do
    [[ -f "$REPO_ROOT/$f" ]] || continue
    case "$f" in
        # Skip these — either binary, generated, or already-validated
        .git/*) continue ;;
        *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.zip|*.tar|*.gz) continue ;;
        *.lock) continue ;;
        # Existing known-clean files (templates, fixtures)
        templates/*) continue ;;
    esac
    case "$f" in
        *.md|*.txt|*.html|*.json|*.yaml|*.yml|*.py|*.sh)
            FILES_TO_CHECK="$FILES_TO_CHECK $REPO_ROOT/$f"
            ;;
    esac
done

if [[ -z "$FILES_TO_CHECK" ]]; then
    exit 0
fi

COUNT=$(echo "$FILES_TO_CHECK" | wc -w)
echo "[trademark-scrub] scanning $COUNT staged text file(s)..."

if ! bash "$PATTERN_SCRIPT" $FILES_TO_CHECK > /tmp/trademark-scrub.out 2>&1; then
    echo ""
    echo "❌ TRADEMARK VIOLATIONS DETECTED in staged changes" >&2
    echo "" >&2
    cat /tmp/trademark-scrub.out >&2
    echo "" >&2
    echo "Either:" >&2
    echo "  1. Replace the banned term with a generic descriptor" >&2
    echo "  2. Move the content to a private/internal doc (not staged)" >&2
    echo "  3. If this is a citation/comparison context (already allowlisted" >&2
    echo "     in patterns/trademark-scrub.sh), edit the script to allow" >&2
    echo "  4. Use git commit --no-verify (avoid; document why)" >&2
    rm -f /tmp/trademark-scrub.out
    exit 1
fi

rm -f /tmp/trademark-scrub.out
echo "[trademark-scrub] OK: no banned terms in staged changes"
exit 0
