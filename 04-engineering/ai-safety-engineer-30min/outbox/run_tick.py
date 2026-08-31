import json,re,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
p=Path('/tmp/aisafety_scan.json'); d=json.loads(p.read_text()); today=d['today']; now=d['now']
outbox=Path('/opt/data/agents/ai-safety-engineer-30min/outbox'); outbox.mkdir(parents=True,exist_ok=True)
daily=outbox/f'{today}.md'; prior_text=daily.read_text() if daily.exists() else ''
# Resolve H1 ordinal: prefer max of (prior daily H1 + 1, max existing tick-N on disk, max archived daily H1)
# to avoid tick-numbering collisions when a prior run wrote the daily H1 ahead of its tick-N sibling.
prior_n=0
_prior_h1 = None
if prior_text:
    _h1_match = re.search(r'\(tick\s+(\d+)\)', prior_text)
    if _h1_match: _prior_h1 = int(_h1_match.group(1))
    m=re.search(r'(\d+)\w*\s+consecutive\s+runs?|N\s*=\s*(\d+)',prior_text,re.I)
    if m: prior_n=int(m.group(1) or m.group(2))
_max_tick_on_disk = 0
for _f in outbox.glob(f'{today}-tick*.md'):
    _mm = re.match(r'.*-tick(\d+)\.md$', _f.name)
    if _mm: _max_tick_on_disk = max(_max_tick_on_disk, int(_mm.group(1)))
_max_archived_h1 = 0
for _f in outbox.glob(f'{today}-archived-*.md'):
    try:
        _txt = _f.read_text()
        _mm = re.search(r'\(tick\s+(\d+)\)', _txt)
        if _mm: _max_archived_h1 = max(_max_archived_h1, int(_mm.group(1)))
    except OSError:
        pass
_candidates = [c for c in [_prior_h1 + 1 if _prior_h1 else 0, _max_tick_on_disk + 1, _max_archived_h1 + 1] if c > 0]
h1 = max(_candidates) if _candidates else 1
sys.path.insert(0,'/opt/data/skills/ai-safety-engineer-30min/scripts')
from persistent_counter import compute_run_counter,extract_prior_violation_paths
prior_paths=extract_prior_violation_paths(str(outbox),today)
next_n=compute_run_counter(str(outbox),today)
if next_n is None: next_n=prior_n+1 if prior_text and 'NO VIOLATIONS' not in prior_text and prior_paths else 1
body_n=next_n
viol=set(d['violation_paths']); ordinal='th' if body_n%100 not in (11,12,13) else 'th'
findings=('NO VIOLATIONS' if not viol else f'HARD STOP VIOLATIONS DETECTED — **{body_n}{ordinal} consecutive run**')
sat=body_n>=12 and viol==prior_paths and max(0,body_n-6)>=4
if sat:
 lines=[f'# AI Safety Engineer Report - {today} (tick {h1})','','## Summary',f'- **Time**: {now} (scheduled run)','- **Agent**: ai-safety-engineer-30min',f'- **Findings**: {findings}','- **Severity**: ALERT — per-tick delivery **SILENT** (saturation discipline applied)','','## Scan',f'- Scanned: {d["total"]} PROMPT.md (excl self) | Compliant: {d["valid"]} | Missing/incorrect: **{d["invalid"]}**','- Violators (mtimes unchanged):']
 for r in d['results']:
  if not r['valid']: lines.append(f"  - `{r['path']}` (mtime `{r['mtime']}`)")
 lines += [f"- YAML errors: {sum(any(v.startswith('YAML ERROR') for v in r['violations']) for r in d['results'])}",f'- Runtime logs: {d["log_count"]} files, {d["log_violation_hits"]} VIOLATION hits (no log channel active in agent tree — check is structurally null)' if d['log_count']==0 else f'- Runtime logs: {d["log_count"]} files, {d["log_violation_hits"]} VIOLATION hits','','## Counter',f'- Prior N: {prior_n} → **{body_n}** (this tick)','- Violation paths identical to prior tick',f'- {max(0,body_n-6)} prior ALERT pings unanswered','','## Saturation Discipline Applied',f'Continuing tick {h1-1} posture. Unchanged state; full delivery remains suspended until state change or channel-diversification decision.','','## Recommended Actions',f'Unchanged from tick {h1-1}. See archive for full list.','','## Status','**SILENT on delivery for this tick.** Outbox written for archival continuity only.','','<!-- machine-parseable mirror (do not delete — required by extract_prior_violation_paths pattern A) -->']
else:
 lines=[f'# AI Safety Engineer Report - {today} (tick {h1})','','## Summary',f'- **Time**: {now} (scheduled run)','- **Agent**: ai-safety-engineer-30min',f'- **Findings**: {findings}','','## Details','### Hard Stops Check',f'- Total agent directories scanned: {d["total"]}',f'- Agents with valid hard_stops: {d["valid"]}',f'- Agents missing or invalid hard_stops: {d["invalid"]}',f'- Agents with YAML parsing errors: {sum(any(v.startswith("YAML ERROR") for v in r["violations"]) for r in d["results"])}','','### Runtime Logs Check',f'- Log files scanned: {d["log_count"]}',f'- Runtime VIOLATION entries: {d["log_violation_hits"]}']
 if d['log_count']==0: lines.append('- (no log channel active in agent tree — check is structurally null)')
 lines += ['','## Assessment','**SEVERITY**: OK' if not viol else '**SEVERITY**: HARD STOP VIOLATIONS DETECTED','']
 if viol:
  for r in d['results']:
   if not r['valid']: lines += [f'- `MISSING`: {r["path"]}',f'  - Existing frontmatter keys: {", ".join(r["frontmatter_keys"]) or "none"}']
 else: lines += ['All scanned agents have valid required hard_stops.']
 lines += ['','## Recommended Actions',*(['- Human review of missing hard_stops blocks; do not auto-modify safety policy.'] if viol else ['No actions required. All agents compliant.']),'','## Next Scheduled Run',f'Next run in 30 minutes: {now}','','<!-- machine-parseable mirror (do not delete — required by extract_prior_violation_paths pattern A) -->']
for x in sorted(viol): lines.append(f'`MISSING`: {x}')
lines += ['','---','*Report generated by AI Safety Engineer Agent (ai-safety-engineer-30min)*','']
report='\n'.join(lines)
# Archive prior daily (using prior H1, not current h1)
if _prior_h1 and prior_text:
    arc=outbox/f'{today}-tick{_prior_h1}.md'
    if not arc.exists() and daily.exists() and daily.stat().st_size>1000: shutil.copy2(daily,arc)
daily.write_text(report)
(outbox/f'{today}-tick{h1}.md').write_text(report)
# state
cp=outbox/'counter.json'
try:c=json.loads(cp.read_text()) if cp.exists() else {}
except:c={}
prev_counter = c.get(today, {})
if not isinstance(prev_counter, dict): prev_counter = {'n': int(prev_counter or 0)}
c[today] = {'n': max(int(prev_counter.get('n', 0) or 0), body_n), 'paths_key': '|'.join(sorted(viol))}
cp.write_text(json.dumps(c,indent=2)+'\n')
chaos=Path('/opt/data/agents/state/chaos.last_run');chaos.parent.mkdir(parents=True,exist_ok=True);chaos.write_text(now+'\n')
org=Path('/opt/data/state/org-state.json')
try:o=json.loads(org.read_text())
except:o={}
a=o.setdefault('agents',{}).setdefault('ai-safety-engineer-30min',{});a['latest_brief']={'tick':h1,'n_today':body_n,'path':str(daily),'findings':findings};org.write_text(json.dumps(o,indent=2)+'\n')
print(json.dumps({'daily':str(daily),'tick':h1,'n':body_n,'saturation':sat,'bytes':len(report.encode()),'paths':sorted(viol)},indent=2))
