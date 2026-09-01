---

name: research-engineer
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: build
archetype: specialist
time_scale: weekly
composition:
  - thoth-literature-scanner
  - mnemosyne-document-archivist
  - eval-gate-runner
transfer_targets:
  - 05-research-education/research-tracker
  - 05-research-education/citation-coverage-enforcer
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

