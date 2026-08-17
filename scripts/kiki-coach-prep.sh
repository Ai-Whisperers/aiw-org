#!/usr/bin/env bash
# kiki-coach-prep.sh — pre-gathers Kiki's recent activity for the lesson agent
# Run before the weekly kiki-coach cron job to populate /opt/data/agents/state/kiki-prep.json
# The agent then reads this file instead of running gh API calls itself (faster, more reliable)

set -uo pipefail

ORG="${ORG:-Ai-Whisperers}"
SINCE_DAYS="${SINCE_DAYS:-7}"
OUTPUT="${OUTPUT:-/opt/data/agents/state/kiki-prep.json}"

# Repos Kiki primarily touches (from company/INDEX.md analysis + charter)
KIKI_REPOS=(company marketing-strategy cursor-standards)

# Path discovery
GH_BIN=""
for prefix in /usr/bin /usr/local/bin /opt/hermes/bin "$HOME/.hermes/bin" /root/.hermes/bin; do
  if [[ -x "$prefix/gh" ]]; then GH_BIN="$prefix/gh"; break; fi
done
[[ -z "$GH_BIN" ]] && command -v gh >/dev/null 2>&1 && GH_BIN="gh"

mkdir -p "$(dirname "$OUTPUT")"

# Serialize KIKI_REPOS to JSON safely (use python, not bash interpolation)
REPOS_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.argv[1:]))" "${KIKI_REPOS[@]}")

if [[ -z "$GH_BIN" ]]; then
  # Graceful degradation: write empty prep with diagnostic, no error
  python3 -c "
import json, datetime
out = {
    'as_of': datetime.datetime.utcnow().isoformat() + 'Z',
    'window_days': $SINCE_DAYS,
    'kiki_repos': $REPOS_JSON,
    'recent_commits': [],
    'recent_files_touched': [],
    'error': 'gh CLI not on PATH',
}
with open('$OUTPUT', 'w') as f: json.dump(out, f, indent=2)
print('gh unavailable — wrote empty prep file')
"
  exit 0
fi

# Real run with gh CLI present
export GH_BIN
python3 - "$ORG" "$SINCE_DAYS" "$OUTPUT" "$REPOS_JSON" <<'PY'
import json, subprocess, sys, os
from datetime import datetime, timezone, timedelta

org = sys.argv[1]
days = int(sys.argv[2])
output = sys.argv[3]
repos = json.loads(sys.argv[4])
gh_bin = os.environ.get('GH_BIN', 'gh')

cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

result = {
  'as_of': datetime.now(timezone.utc).isoformat(),
  'window_days': days,
  'kiki_repos': repos,
  'recent_commits': [],
  'recent_files_touched': [],
  'errors': [],
}

for repo in repos:
    try:
        r = subprocess.run([gh_bin, 'api', f'repos/{org}/{repo}/commits?per_page=20'],
                           capture_output=True, text=True, timeout=15)
    except Exception as e:
        result['errors'].append({'repo': repo, 'error': str(e)[:100]})
        continue
    if r.returncode != 0:
        result['errors'].append({'repo': repo, 'error': r.stderr.strip()[:100]})
        continue
    try:
        commits = json.loads(r.stdout)
    except Exception:
        commits = []
    for c in commits:
        cd = c.get('commit', {}).get('author', {}).get('date', '')
        if cd >= cutoff:
            msg = c.get('commit', {}).get('message', '').split('\n')[0][:100]
            author = c.get('commit', {}).get('author', {}).get('name', '?')
            result['recent_commits'].append({
                'repo': repo,
                'sha': c.get('sha', '')[:7],
                'date': cd[:10],
                'author': author,
                'message': msg,
            })

result['recent_commits'].sort(key=lambda c: c.get('date', ''), reverse=True)

with open(output, 'w') as f:
    json.dump(result, f, indent=2, default=list)

print(f"Wrote {output}: {len(result['recent_commits'])} commits in last {days}d")
PY