---

name: compliance-monitor
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
cluster: run
archetype: solver
time_scale: minutes
transfer_targets:
  - 04-engineering/security-watchdog
max_output_tokens: 800

---

