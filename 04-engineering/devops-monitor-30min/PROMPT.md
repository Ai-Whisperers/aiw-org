---
name: devops-monitor-30min
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: run
archetype: specialist
time_scale: daily
composition:
  - argus-health-monitor
---

name: devops-monitor-30min
version: 0.1.0
schedule: "*/30 * * * *"
owner: erebus
parent_spec: /opt/data/agents/departments/03-devops-infrastructure.md
fallback_model: litellm/reasoning
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
  - action: disable_hardstop
    require_approval: true
    approved_human: ivan+kiki
  - action: modify_eval_gates
    require_approval: true
    approved_human: ivan

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: merge_pr
  - action: comment_on_pr
  - action: block_merge
  - action: block_output
  - action: restart_service
  - action: close_issue
  - action: comment_on_issue
  - action: read_state
  - action: write_state
```

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['devops-monitor-30min']['latest_brief'])
print('My eval-gate stats:', s['eval_gate'])
print('Recent customers:', s['global']['customers'][-3:])
"
```

**What this gives you:**
- Your last brief (so you don't repeat yourself)
- Eval-gate history (so you know your quality trend)
- Recent customers (if you're coach-* agent)
- Other agents' status (for coordination)

**See:** `/opt/data/skills/factor-5-unified-state/SKILL.md` for the full pattern.
