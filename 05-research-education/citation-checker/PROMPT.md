---

name: citation-checker
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - peitho-language-quality
  - thoth-literature-scanner
transfer_targets:
  - 05-research-education/research-tracker
  - 05-research-education/thesis-tracker
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

