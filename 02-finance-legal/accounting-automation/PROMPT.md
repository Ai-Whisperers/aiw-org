---

name: accounting-automation
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - themis-document-classifier
  - hephaestus-document-miner
transfer_targets:
  - 02-finance-legal/finance-controller
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

