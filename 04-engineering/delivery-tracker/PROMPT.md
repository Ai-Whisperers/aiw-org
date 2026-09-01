---

name: delivery-tracker
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: daily
composition:
  - kronos-operations-lead
transfer_targets:
  - 04-engineering/engineering-roster
  - 01-operations/management-coordinator
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800

---

