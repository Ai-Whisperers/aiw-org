---

name: multimedia-producer
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - orpheus-recordings-agent
transfer_targets:
  - 03-sales-growth/marketing-content-producer
parent_spec: departments/03-sales-growth.md
max_output_tokens: 800

---

