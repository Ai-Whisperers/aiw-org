---

name: cadmus-lead-enrichment
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
composition:
  - clio-customer-signal-collector
  - themis-document-classifier
transfer_targets:
  - apollo-sales-lead
max_output_tokens: 800

---

