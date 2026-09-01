---

name: chaos-test-runner
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: run
archetype: specialist
time_scale: daily
composition:
  - argus-health-monitor
transfer_targets:
  - 04-engineering/devops-monitor-30min
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800

---

