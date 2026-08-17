#!/usr/bin/env bash
# org-pulse.sh — collects org metrics for business-analyst agent
# Designed to be cron-friendly: silent on success, terse on failure.
# Output: JSON to stdout. Exit 0 on success, partial data allowed.
#
# Used by: business-analyst cron job (daily 06:30 PYT)
# Required: gh CLI (authenticated), curl, python3. jq optional (falls back to python).

set -uo pipefail

ORG="${ORG:-Ai-Whisperers}"
OUTPUT=$(mktemp)
trap 'rm -f "$OUTPUT" "$OUTPUT".*' EXIT

# Helper: find a usable PATH-aware tool. Cron jobs run with minimal PATH.
find_tool() {
  for tool in "$@"; do
    if command -v "$tool" >/dev/null 2>&1; then echo "$tool"; return 0; fi
    for prefix in /usr/bin /usr/local/bin /opt/hermes/bin "$HOME/.hermes/bin" /root/.hermes/bin; do
      if [[ -x "$prefix/$tool" ]]; then echo "$prefix/$tool"; return 0; fi
    done
  done
  return 1
}

GH_BIN=$(find_tool gh)
CURL_BIN=$(find_tool curl)
JQ_BIN=$(find_tool jq)
HERMES_BIN=$(find_tool hermes)

# JSON parser fallback (uses python if jq missing)
j() {
  local expr="$1"
  if [[ -n "$JQ_BIN" ]]; then
    "$JQ_BIN" -c "$expr"
  else
    python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
except: sys.exit(0)
expr = '''$expr'''
# Crude but works for our common cases
if expr.strip() == '.total_count':
    print(data.get('total_count', 0))
elif expr.strip().startswith('[.[]'):
    # basic filter — only handles archived==false
    items = data if isinstance(data, list) else []
    items = [r for r in items if not r.get('archived')]
    if 'pushed_at' in expr:
        items.sort(key=lambda r: r.get('pushed_at',''), reverse=True)
    print(json.dumps(items[:5] if '[:5]' in expr else items))
else:
    print(json.dumps(data))
"
  fi
}

# 1. Active repos + recent push activity
if [[ -n "$GH_BIN" ]]; then
  "$GH_BIN" api "orgs/$ORG/repos?per_page=100&type=all" --paginate 2>/dev/null \
    | j '[.[] | select(.archived == false) | {name, size: .size, pushed_at, open_issues: .open_issues_count, language}]' \
    > "$OUTPUT.repos" || echo '[]' > "$OUTPUT.repos"
  # Issues total
  "$GH_BIN" api "search/issues?q=org:$ORG+is:open+is:issue" 2>/dev/null \
    | j '.total_count' > "$OUTPUT.issues" || echo "0" > "$OUTPUT.issues"
  # PRs total
  "$GH_BIN" api "search/issues?q=org:$ORG+is:open+is:pr" 2>/dev/null \
    | j '.total_count' > "$OUTPUT.prs" || echo "0" > "$OUTPUT.prs"
else
  echo '[]' > "$OUTPUT.repos"
  echo "0" > "$OUTPUT.issues"
  echo "0" > "$OUTPUT.prs"
fi

# 2. Live apex checks (top 2 production sites)
if [[ -n "$CURL_BIN" ]]; then
  for site in nexaparaguay.com.py ometzdental.com; do
    code=$("$CURL_BIN" -sS -o /dev/null -w "%{http_code}" --max-time 5 "https://$site/" 2>/dev/null || echo "000")
    echo "$site $code" >> "$OUTPUT.sites"
  done
else
  echo "curl_unavailable 000" >> "$OUTPUT.sites"
fi

# 3. Cron error count (only if hermes CLI present)
if [[ -n "$HERMES_BIN" ]]; then
  "$HERMES_BIN" cron list 2>/dev/null \
    | j '[.jobs[] | select(.last_status == "error") | {name, last_run_at}]' \
    > "$OUTPUT.cron_errors" || echo '[]' > "$OUTPUT.cron_errors"
else
  echo '[]' > "$OUTPUT.cron_errors"
fi

# 4. Assemble final JSON
python3 - "$OUTPUT" "$ORG" <<'PY'
import json, os, sys
from datetime import datetime, timezone, timedelta

out_path = sys.argv[1]
org = sys.argv[2]

def read(p):
    try: return open(p).read().strip()
    except: return ''

def readj(p):
    try: return json.loads(read(p))
    except: return None

repos = readj(out_path + '.repos') or []
try: issues = int(read(out_path + '.issues') or 0)
except: issues = 0
try: prs = int(read(out_path + '.prs') or 0)
except: prs = 0
cron_err = readj(out_path + '.cron_errors') or []

sites = []
for line in read(out_path + '.sites').splitlines():
    if not line: continue
    parts = line.rsplit(' ', 1)
    if len(parts) == 2:
        try: code = int(parts[1])
        except: code = None
        sites.append({'site': parts[0], 'http': code})

cutoff = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
stale = sorted([r['name'] for r in repos if r.get('pushed_at', '') < cutoff])
recent = sorted(repos, key=lambda r: r.get('pushed_at', ''), reverse=True)[:5]

print(json.dumps({
  'org': org,
  'as_of': datetime.now(timezone.utc).isoformat(),
  'active_repos': len(repos),
  'open_issues': issues,
  'open_prs': prs,
  'stale_repos_14d': stale[:10],
  'recently_pushed': [{'name': r['name'], 'pushed_at': r.get('pushed_at','')[:10]} for r in recent],
  'live_sites': sites,
  'cron_errors': cron_err,
  'tools': {
    'gh': bool(os.environ.get('_GH_PRESENT')),
    'jq': bool(os.environ.get('_JQ_PRESENT')),
    'hermes_cli': bool(os.environ.get('_HERMES_PRESENT')),
  }
}, indent=2))
PY

exit 0