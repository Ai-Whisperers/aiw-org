---

name: security-auditor
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: build
archetype: specialist
time_scale: weekly
composition:
  - compliance-monitor
transfer_targets:
  - 04-engineering/security-watchdog
  - 04-engineering/security-watchdog-30min
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800

---

