---

name: lead-enrichment
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - cadmus-lead-enrichment
  - clio-customer-signal-collector
transfer_targets:
  - 03-sales-growth/sales-pipeline
parent_spec: departments/03-sales-growth.md
max_output_tokens: 800

---

