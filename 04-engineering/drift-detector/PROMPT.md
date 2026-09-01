---

name: drift-detector
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: run
archetype: specialist
time_scale: daily
composition:
  - argus-health-monitor
transfer_targets:
  - 04-engineering/ai-safety-engineer
  - 04-engineering/eval-gate-runner
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800

---

