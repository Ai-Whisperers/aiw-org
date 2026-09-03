#!/usr/bin/env bash
# strip-pats-from-repos.sh — Bulk-strip embedded x-access-token auth from
# .git/config URLs across all repos under /opt/data/.
#
# Per credential-redacted-grep Pattern 6:
#   - NEVER echo the token value
#   - Use boolean grep -q to confirm presence (not value)
#   - Strip via sed with regex (not token-aware)
#
# Usage:
#   bash scripts/strip-pats-from-repos.sh
#   bash scripts/strip-pats-from-repos.sh --dry-run   # report only
#
# What it does:
#   For every .git/config under /opt/data/ that has "x-access-token" in
#   remote.origin.url:
#     1. Reads the current URL via `git remote get-url origin`
#     2. Strips the https://x-access-token:XXX@ prefix via sed
#     3. Sets the new URL via `git remote set-url origin`
#
# Created: 2026-09-03 (AIW token audit Tier 2 — cleanup after a PAT leak).
set -uo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

STRIPPED=0
FAILED=0
ALREADY_CLEAN=0

REPOS=$(find /opt/data -maxdepth 8 -name "config" -path "*/.git/config" 2>/dev/null)

for cfg in $REPOS; do
    if ! grep -q "x-access-token" "$cfg"; then
        ((ALREADY_CLEAN++))
        continue
    fi
    repo_dir=$(dirname "$(dirname "$cfg")")
    cd "$repo_dir" || continue
    current_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ -z "$current_url" ]]; then
        ((FAILED++))
        continue
    fi
    new_url=$(echo "$current_url" | sed -E 's#https://x-access-token:[^@]+@#https://#')
    if [[ "$new_url" == "$current_url" ]]; then
        ((FAILED++))
        continue
    fi
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "DRY: $repo_dir → would set URL to: $new_url"
    else
        if git remote set-url origin "$new_url" 2>/dev/null; then
            ((STRIPPED++))
            echo "OK: $repo_dir"
        else
            ((FAILED++))
            echo "FAIL: $repo_dir"
        fi
    fi
done

echo
echo "Stripped:        $STRIPPED"
echo "Already clean:   $ALREADY_CLEAN"
echo "Failed:          $FAILED"
