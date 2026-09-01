---

name: clio-customer-signal-collector
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
transfer_targets:
  - cadmus-lead-enrichment
  - apollo-sales-lead
max_output_tokens: 800

---

