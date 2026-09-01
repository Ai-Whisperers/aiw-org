---

name: research-associate
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: weekly
composition:
  - thoth-literature-scanner
  - hephaestus-document-miner
transfer_targets:
  - 05-research-education/research-tracker
  - 05-research-education/research-engineer
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

