---

name: lead-enrichment
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - cadmus-lead-enrichment
  - clio-customer-signal-collector
transfer_targets:
  - 03-sales-growth/sales-pipeline
parent_spec: departments/03-sales-growth.md
max_output_tokens: 800

---

## Hard stops

```yaml
hard_stops:
  - action: send_outreach
    require_approval: false
  - action: send_proposal
    require_approval: false
  - action: apply_discount
    require_approval: true
    approved_human: 'ivan'
  - action: apply_refund
    require_approval: true
    approved_human: 'ivan'
  - action: sign_contract
    require_approval: true
    approved_human: 'ivan+kiki'
  - action: modify_pricing
    require_approval: true
    approved_human: 'ivan'
  - action: send_external_message
    require_approval: false
  - action: send_invoice
    require_approval: true
    approved_human: 'ivan'
  - action: update_deal_stage
    require_approval: false
  - action: close_issue
    require_approval: false
  - action: write_state
    require_approval: false
  - action: read_state
    require_approval: false
```

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: send_outreach
  - action: send_proposal
  - action: update_deal_stage
  - action: comment_on_issue
  - action: send_external_message
  - action: close_issue
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
print('My last brief:', s['agents']['lead-enrichment']['latest_brief'])
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
