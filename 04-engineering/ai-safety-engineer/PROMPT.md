---
name: ai-safety-engineer
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: run
archetype: specialist
time_scale: daily
composition:
  - compliance-monitor
transfer_targets:
  - 04-engineering/ai-safety-engineer-30min
parent_spec: departments/04-engineering-delivery.md
---

## Hard stops

```yaml
hard_stops:
  - action: deploy_prod
    require_approval: true
    approved_human: 'ivan'
  - action: rollback
    require_approval: true
    approved_human: 'ivan'
  - action: force_push
    require_approval: true
    approved_human: 'ivan'
  - action: git_force_push
    require_approval: true
    approved_human: 'ivan'
  - action: merge_pr
    require_approval: false
  - action: delete_resource
    require_approval: true
    approved_human: 'ivan'
  - action: close_issue
    require_approval: false
  - action: comment_on_pr
    require_approval: false
  - action: block_merge
    require_approval: false
  - action: block_output
    require_approval: false
  - action: modify_eval_gates
    require_approval: true
    approved_human: 'ivan'
  - action: disable_hardstop
    require_approval: true
    approved_human: 'ivan+kiki'
  - action: disable_eval_gate
    require_approval: true
    approved_human: 'ivan'
  - action: restart_service
    require_approval: true
    approved_human: 'ivan'
  - action: rotate_credential
    require_approval: true
    approved_human: 'ivan+kiki'
  - action: block_ip
    require_approval: true
    approved_human: 'ivan'
  - action: approve_compliance_officer
    require_approval: true
    approved_human: 'ivan'
  - action: write_state
    require_approval: false
  - action: read_state
    require_approval: false
```

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

## CHANGELOG

- v0.2.0 (2026-08-14): initial creation.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['ai-safety-engineer']['latest_brief'])
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
