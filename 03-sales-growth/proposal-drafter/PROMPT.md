---

name: proposal-drafter
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - metis-proposal-drafter
  - themis-document-classifier
transfer_targets:
  - 03-sales-growth/sales-pipeline
parent_spec: departments/03-sales-growth.md
max_output_tokens: 800

---

