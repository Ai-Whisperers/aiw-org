#!/usr/bin/env bash
# trademark-scrub.sh — Mechanical check for banned terms in any text file.
# Run: trademark-scrub.sh <file> [<file> ...]
# Exit 0 = clean, Exit 1 = violations found

set -euo pipefail

BANNED_REGEX='\b(mensaje|mensajebusiness|mensaje-web|wpp|facebook|instagram|insta|messenger|oculus|paypal|stripe|google|gmail|youtube|tiktok|twitter|x-com|discord|slack|microsoft|office365|apple|icloud|amazon|aws-|openai|chatgpt|anthropic|claude|meta)\b'

VIOLATIONS=0
FILES_CHECKED=0

for file in "$@"; do
    if [[ ! -f "$file" ]]; then
        echo "SKIP: $file (not found)"
        continue
    fi
    FILES_CHECKED=$((FILES_CHECKED + 1))

    matches=$(grep -nEi "$BANNED_REGEX" "$file" || true)

    if [[ -n "$matches" ]]; then
        filtered=$(echo "$matches" | grep -vE '\[CITATION\]|\.caveat|TRADEMARK_AWARE|github\.com/(anthropic|meta|openai|google|microsoft|apple|amazon)|example\.com|amazonaws\.com|gmail\.com|/CR/|/CC/|SOURCE:|Best source path|funding-landscape|for Startups|Founders Hub|Inception|startups program|catalog of programs|program list|Calendar API|Maps API|Drive API|Gmail API|YouTube|YouTube video|GitHub Actions|Traefik|CF Worker|Cloudflare Worker|Worker + R2|GitHub CLI|Cloudflare R2|Cloudflare tunnel|Dropbox API|Notion API|Slack webhook|GitHub API|API endpoint|LinkedIn video|platform specs' || true)

        if [[ -n "$filtered" ]]; then
            echo "VIOLATIONS in $file:"
            echo "$filtered" | head -20
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

echo ""
echo "Files checked: $FILES_CHECKED"
echo "Files with violations: $VIOLATIONS"

if [[ $VIOLATIONS -gt 0 ]]; then
    exit 1
fi

echo "OK: All files clean"
exit 0
