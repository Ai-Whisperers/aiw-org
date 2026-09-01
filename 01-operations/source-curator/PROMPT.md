---

name: source-curator
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - thoth-literature-scanner
  - peitho-language-quality
transfer_targets:
  - 05-research-education/research-tracker
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

---

