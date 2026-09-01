#!/usr/bin/env bash
# pre-commit-secret-leak.sh — Stage-only secret pattern check.
#
# Companion wrapper to patterns/secret-leak-check.sh that runs ONLY against
# files staged in the current git index. The underlying pattern script
# scans the whole repo by default; in pre-commit we want to fail on
# *introductions*, not on pre-existing state.
#
# Exits 0 if no secrets found in staged changes, 1 otherwise.
# Bypass with `git commit --no-verify` (not recommended).

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PATTERN_SCRIPT="$REPO_ROOT/patterns/secret-leak-check.sh"

if [[ ! -f "$PATTERN_SCRIPT" ]]; then
    echo "WARN: $PATTERN_SCRIPT missing — secret-leak guard skipped" >&2
    exit 0
fi

# Collect newly-staged file contents to a tmp dir; run pattern script over those
STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
if [[ -z "$STAGED" ]]; then
    exit 0
fi

# Build a tmp dir with copies of only the staged files (preserve paths so
# the pattern script's output is actionable). Limit to files that exist
# and are under a reasonable size cap (binary / huge files skipped).
TMP=$(mktemp -d -t secret-leak-stage.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
COUNT=0
for f in $STAGED; do
    # Skip deletions, mode-only changes, and files outside the repo
    [[ -f "$REPO_ROOT/$f" ]] || continue
    # Skip .git internals
    case "$f" in
        .git/*) continue ;;
    esac
    # Cap at 1 MiB to avoid scanning huge binaries
    sz=$(stat -c%s "$REPO_ROOT/$f" 2>/dev/null || echo 0)
    if (( sz > 1048576 )); then
        continue
    fi
    mkdir -p "$TMP/$(dirname "$f")"
    cp "$REPO_ROOT/$f" "$TMP/$f"
    COUNT=$((COUNT + 1))
done

if (( COUNT == 0 )); then
    exit 0
fi

echo "[secret-leak] scanning $COUNT staged file(s)..."

if ! bash "$PATTERN_SCRIPT" "$TMP" > /tmp/secret-leak-check.out 2>&1; then
    echo ""
    echo "❌ SECRET LEAK DETECTED in staged changes" >&2
    echo "" >&2
    cat /tmp/secret-leak-check.out >&2
    echo "" >&2
    echo "Either:" >&2
    echo "  1. Remove the secret from the file and rotate the credential" >&2
    echo "  2. Move the secret to .env (gitignored) and load via env var" >&2
    echo "  3. If this is a known-safe pattern (test fixture, doc example)," >&2
    echo "     use git commit --no-verify (avoid; document why)" >&2
    rm -f /tmp/secret-leak-check.out
    exit 1
fi

rm -f /tmp/secret-leak-check.out
echo "[secret-leak] OK: no secret patterns in staged changes"
exit 0
