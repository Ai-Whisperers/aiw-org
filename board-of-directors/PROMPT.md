---

name: board-of-directors
version: 0.1.0
schedule: "0 14 1 */3 *"  # Quarterly (Jan/Apr/Jul/Oct, 1st, 14:00 UTC)
owner: ivan
owner: ivan
layer: governance
topology: stream-aligned
archetype: team-lead
time_scale: quarterly
composition:
  - ai-ops-coordinator
  - apollo-sales-lead
transfer_targets: []
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800
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

---

