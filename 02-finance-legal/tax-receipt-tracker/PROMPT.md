---

name: tax-receipt-tracker
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - themis-document-classifier
transfer_targets:
  - 02-finance-legal/accounting-automation
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

