---
hard_stops:
- action: read_state
  require_approval: false
- action: write_state
  require_approval: false
- action: disable_hardstop
  approved_human: ivan+kiki
  require_approval: true
- action: modify_eval_gates
  approved_human: ivan
  require_approval: true
---

name: coach-renewal-manager
version: 0.1.0
schedule: "monthly (1st of month, 09:00 UTC)"
owner: erebus
parent_spec: /opt/data/agents/departments/06-people-culture.md
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
