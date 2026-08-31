#!/usr/bin/env bash
# install-hooks.sh — Install AI Whisperers standard pre-commit hooks into a repo.
# Generated 2026-08-28.
# Usage: cd <repo> && bash /opt/data/agents-v2/templates/install-hooks.sh
#
# What it does:
#   1. Copies pre-commit template to .git/hooks/pre-commit
#   2. chmods it executable
#   3. Optionally copies AGENTS.md template to repo root (if --with-agents)
#   4. Optionally copies gitignore template to repo root (if --with-gitignore)
#
# Idempotent: re-running updates the hook.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
if [[ -z "$REPO_ROOT" ]]; then
    echo "ERROR: not in a git repo. cd into a repo and try again." >&2
    exit 1
fi

TEMPLATES="/opt/data/agents-v2/templates"

WITH_AGENTS=false
WITH_GITIGNORE=false
for arg in "$@"; do
    case "$arg" in
        --with-agents) WITH_AGENTS=true ;;
        --with-gitignore) WITH_GITIGNORE=true ;;
        *) echo "Unknown arg: $arg (ignored)" ;;
    esac
done

echo "Installing pre-commit hook into $REPO_ROOT/.git/hooks/pre-commit..."
cp "$TEMPLATES/pre-commit.template" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
echo "  ✓ Hook installed."

if $WITH_AGENTS; then
    if [[ -f "$REPO_ROOT/AGENTS.md" ]]; then
        echo "  AGENTS.md already exists at repo root — skipping (delete first if you want to overwrite)."
    else
        sed -e "s|{{REPO_NAME}}|$(basename "$REPO_ROOT")|g" \
            -e "s|{{DATE}}|$(date -u +%Y-%m-%d)|g" \
            "$TEMPLATES/AGENTS.md.template" > "$REPO_ROOT/AGENTS.md"
        echo "  ✓ AGENTS.md installed."
    fi
fi

if $WITH_GITIGNORE; then
    if [[ -f "$REPO_ROOT/.gitignore" ]]; then
        echo "  .gitignore already exists at repo root — skipping (review and merge manually if you want)."
    else
        cp "$TEMPLATES/gitignore.template" "$REPO_ROOT/.gitignore"
        echo "  ✓ .gitignore installed."
    fi
fi

echo ""
echo "Done. Try: git commit -m 'test'"
echo "(If the hook fails, fix the violation or use git commit --no-verify with an issue filed.)"
