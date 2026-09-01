---

name: business-analyst
version: 0.2.1
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - business-analyst
  - themis-document-classifier
transfer_targets:
  - 02-finance-legal/finance-controller
  - 03-sales-growth/sales-pipeline
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

