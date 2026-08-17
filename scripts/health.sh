#!/usr/bin/env bash
# health.sh — verifies the 3 management agents delivered in the last 7 days
# Silent on all-healthy. Loud on missing/failed.
# Used by: morning-brief agent (optional add-on) and ad-hoc by Ivan.

set -uo pipefail

AGENTS=(business-analyst management-coordinator kiki-coach sales-pipeline finance-controller engineering-roster research-tracker)
DAYS=7
ERRORS=()

# Path discovery (cron has minimal PATH)
HERMES_BIN=""
for prefix in /usr/bin /usr/local/bin /opt/hermes/bin "$HOME/.hermes/bin" /root/.hermes/bin; do
  if [[ -x "$prefix/hermes" ]]; then HERMES_BIN="$prefix/hermes"; break; fi
done
[[ -z "$HERMES_BIN" ]] && command -v hermes >/dev/null 2>&1 && HERMES_BIN="hermes"

for a in "${AGENTS[@]}"; do
  # kiki-coach writes to lessons/ instead of outbox/
  if [[ "$a" == "kiki-coach" ]]; then
    target_dir="/opt/data/agents/$a/lessons"
  else
    target_dir="/opt/data/agents/$a/outbox"
  fi
  if [[ ! -d "$target_dir" ]]; then
    ERRORS+=("$a: directory missing ($target_dir)")
    continue
  fi
  # Find newest .md in target dir
  newest=$(find "$target_dir" -maxdepth 1 -name '*.md' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
  if [[ -z "$newest" ]]; then
    ERRORS+=("$a: no output files yet ($target_dir)")
    continue
  fi
  # Check freshness
  file_age_days=$(( ( $(date +%s) - $(stat -c %Y "$newest") ) / 86400 ))
  if (( file_age_days > DAYS )); then
    ERRORS+=("$a: newest file is $(basename "$newest"), $file_age_days days old")
  fi
done

# Cron health (only if hermes CLI present)
if [[ -n "$HERMES_BIN" ]]; then
  CRON_DATA=$("$HERMES_BIN" cron list 2>/dev/null || echo '{"jobs":[]}')
  CRON_ERR=$(python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
except: d = {'jobs': []}
errs = [j['name'] for j in d.get('jobs', []) if j.get('last_status') == 'error' and j.get('name', '').startswith('aiw-')]
print('\n'.join(errs))
" "$CRON_DATA")
  if [[ -n "$CRON_ERR" ]]; then
    while IFS= read -r name; do
      ERRORS+=("cron: $name in error state")
    done <<< "$CRON_ERR"
  fi
else
  ERRORS+=("hermes CLI not on PATH — cron status unknown")
fi

if (( ${#ERRORS[@]} == 0 )); then
  echo "✅ All agents healthy (last ${DAYS}d)"
  exit 0
fi

echo "⚠️ ${#ERRORS[@]} issue(s):"
for e in "${ERRORS[@]}"; do
  echo "  - $e"
done
exit 1