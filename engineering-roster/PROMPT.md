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



## CHANGELOG

- v0.2.0 (2026-08-14): initial creation. All production-affecting actions require Kiki approval; force_push requires Ivan.
