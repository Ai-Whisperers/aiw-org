---

name: instructional-designer
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: monthly
composition:
  - calliope-content-producer
  - orpheus-recordings-agent
  - peitho-language-quality
transfer_targets:
  - 05-research-education/course-producer
  - 05-research-education/subject-matter-expert
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

