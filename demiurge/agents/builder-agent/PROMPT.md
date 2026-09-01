---

name: builder-agent
version: 0.1.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: on-demand
transfer_targets:
  - 02-quality/auditor-agent
max_output_tokens: 800

---

