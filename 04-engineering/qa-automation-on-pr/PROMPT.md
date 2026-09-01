---

name: qa-automation-on-pr
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: build
archetype: specialist
time_scale: on-demand
composition:
  - eval-gate-runner
  - chaos-test-runner
transfer_targets:
  - 04-engineering/qa-automation-runner
  - 04-engineering/engineering-roster
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800

---

