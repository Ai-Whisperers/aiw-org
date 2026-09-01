---

name: echo-community-scanner
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: solver
time_scale: minutes
composition:
  - iris-community-monitor
transfer_targets:
  - athena-product-discovery-lead
max_output_tokens: 800

---

