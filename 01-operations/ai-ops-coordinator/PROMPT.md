---

name: ai-ops-coordinator
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: team-lead
time_scale: daily
composition:
  - hermes-router-revenue
  - kronos-operations-lead
transfer_targets:
  - 04-engineering/security-watchdog-30min
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

