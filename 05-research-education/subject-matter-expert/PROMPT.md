---

name: subject-matter-expert
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: monthly
composition:
  - thoth-literature-scanner
  - calliope-content-producer
transfer_targets:
  - 05-research-education/course-producer
  - 05-research-education/research-tracker
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

