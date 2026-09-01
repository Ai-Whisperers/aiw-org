---

name: sales-pipeline
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: team-lead
time_scale: daily
composition:
  - hermes-router-revenue
  - apollo-sales-lead
  - cadmus-lead-enrichment
parent_spec: departments/03-sales-growth.md
max_output_tokens: 800

---

