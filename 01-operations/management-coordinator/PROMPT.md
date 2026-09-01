---
name: management-coordinator
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: team-lead
time_scale: daily
composition:
  - hermes-router-revenue
---

## Hard stops

```yaml
hard_stops:
  - action: delete_resource
    require_approval: true
    approved_human: 'ivan'
  - action: disable_hardstop
    require_approval: true
    approved_human: 'ivan+kiki'
  - action: disable_eval_gate
    require_approval: true
    approved_human: 'ivan'
  - action: modify_eval_gates
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
  - action: modify_curriculum
    require_approval: true
    approved_human: 'ivan'
  - action: force_push
    require_approval: true
    approved_human: 'ivan'
  - action: git_force_push
    require_approval: true
    approved_human: 'ivan'
  - action: publish_post
    require_approval: true
    approved_human: 'ivan'
  - action: send_external_message
    require_approval: false
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
```

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: comment_on_issue
  - action: block_merge
  - action: block_output
  - action: restart_service
  - action: block_ip
  - action: read_state
  - action: write_state
```

## CHANGELOG

- v0.2.0 (2026-08-14): upgraded to 12-section template. Added hard stops, idempotency, context-payload, fallback.
- v0.1.0 (2026-08-13): initial rollout. Biweekly cadence.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['management-coordinator']['latest_brief'])
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
