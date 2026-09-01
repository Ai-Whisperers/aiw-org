---

name: citation-coverage-enforcer
version: 0.1.0
owner: research-tracker
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - peitho-language-quality
  - mnemosyne-document-archivist
transfer_targets:
  - 05-research-education/research-tracker
cluster: run
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

