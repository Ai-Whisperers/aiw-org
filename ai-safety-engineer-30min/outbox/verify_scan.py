import re
from pathlib import Path

required = {'disable_hardstop', 'modify_eval_gates'}
agents_dir = Path('/opt/data/agents')
self_dir = 'ai-safety-engineer-30min'

results = []
total = 0
for d in sorted(agents_dir.iterdir()):
    if not d.is_dir(): continue
    if d.name == self_dir: continue
    total += 1
    p = d / 'PROMPT.md'
    if not p.exists():
        results.append((d.name, 'NO_PROMPT', [], ['NO_PROMPT.md']))
        continue
    txt = p.read_text(errors='ignore').split('---', 2)
    if len(txt) < 3:
        results.append((d.name, 'NO_FRONTMATTER', [], ['NO_FRONTMATTER']))
        continue
    fm = txt[1]
    has_hs = 'hard_stops' in fm
    actions = re.findall(r'-\s*action:\s*(\w+)', fm)
    viol = []
    if not has_hs:
        viol.append('NO hard_stops block')
    else:
        present = set(actions)
        missing = required - present
        if missing:
            viol.append(f'Missing actions: {sorted(missing)}')
    if viol:
        results.append((d.name, 'VIOLATION', sorted(set(actions)), viol))

print(f'TOTAL: {total}')
print(f'VIOLATIONS: {len(results)}')
for r in results:
    print(r)