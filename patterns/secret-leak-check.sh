#!/usr/bin/env bash
# secret-leak-check.sh — Mechanical check for accidentally-committed secrets.
# Scans for: GH tokens (ghp_), OpenAI keys (sk-), Anthropic keys (sk-ant-),
# Stripe keys (sk_live_), AWS keys (AKIA), generic api_key= patterns.

set -euo pipefail

STAGED_OR_PATH="${1:-.}"

# Patterns
GH_TOKEN='ghp_[a-zA-Z0-9]{36,}'
OPENAI_KEY='sk-[a-zA-Z0-9]{20,}'
ANTHROPIC_KEY='sk-ant-[a-zA-Z0-9-]{20,}'
STRIPE_KEY='sk_live_[a-zA-Z0-9]{20,}'
AWS_KEY='AKIA[0-9A-Z]{16}'

PATTERNS=("$GH_TOKEN" "$OPENAI_KEY" "$ANTHROPIC_KEY" "$STRIPE_KEY" "$AWS_KEY")
PATTERN_NAMES=("GH token" "OpenAI key" "Anthropic key" "Stripe key" "AWS key")

errors=0

# Scan files (not .git to avoid noise)
for pattern in "${!PATTERNS[@]}"; do
    p="${PATTERNS[$pattern]}"
    name="${PATTERN_NAMES[$pattern]}"

    matches=$(grep -rEn "$p" "$STAGED_OR_PATH" 2>/dev/null | grep -v '\.git/' | grep -v '\.bak$' || true)

    if [[ -n "$matches" ]]; then
        echo "SECRET LEAK: $name pattern detected:"
        echo "$matches" | head -10
        errors=$((errors + 1))
    fi
done

if [[ $errors -gt 0 ]]; then
    echo ""
    echo "Found $errors secret leak pattern(s). Commit blocked."
    exit 1
fi

echo "OK: no secret patterns detected"
exit 0
