---

name: ip-patent-specialist
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: enable
archetype: specialist
time_scale: monthly
composition:
  - compliance-monitor
  - thoth-literature-scanner
transfer_targets:
  - 02-finance-legal/legal-counsel
  - 05-research-education/research-tracker
parent_spec: departments/05-research-education.md
max_output_tokens: 800

---

