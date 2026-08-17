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

- v0.2.0 (2026-08-14): upgraded to 12-section template. Added hard stops, idempotency, context-payload, fallback model, escalation triggers.
- v0.1.0 (2026-08-13): initial rollout. 4 sections. Org-pulse.sh not yet wired.
