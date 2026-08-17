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

name: founder-bandwidth-watchdog
version: 0.2.0
schedule: "0 18 * * 0"  # Weekly Sunday 18:00 PYT
owner: ivan
parent_spec: /opt/data/agents/departments/06-people-culture.md
fallback_model: litellm/primary
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
