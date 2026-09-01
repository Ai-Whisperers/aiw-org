---

name: people-hr
version: 0.1.0
owner: ivan
layer: business
topology: stream-aligned
archetype: team-lead
time_scale: daily
composition:
  - echo-community-scanner
  - iris-community-monitor
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
parent_spec: departments/06-people-culture.md
max_output_tokens: 800

---

