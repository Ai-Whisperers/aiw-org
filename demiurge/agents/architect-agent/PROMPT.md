---

name: architect-agent
version: 0.1.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
cluster: enable
archetype: architect
time_scale: on-demand
transfer_targets:
  - 02-quality/auditor-agent
max_output_tokens: 800

---


