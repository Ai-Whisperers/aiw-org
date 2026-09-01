---

name: funding-coordinator
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - clio-customer-signal-collector
transfer_targets:
  - 02-finance-legal/finance-controller
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

