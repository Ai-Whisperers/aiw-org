---

name: academic-liaison
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: weekly
composition:
  - thoth-literature-scanner
  - peitho-language-quality
  - mnemosyne-document-archivist
transfer_targets:
  - 05-research-education/research-tracker
  - 05-research-education/thesis-tracker
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

