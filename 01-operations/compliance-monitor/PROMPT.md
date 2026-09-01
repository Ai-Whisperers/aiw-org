---

name: compliance-monitor
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - compliance-monitor
transfer_targets:
  - 02-finance-legal/legal-counsel
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

