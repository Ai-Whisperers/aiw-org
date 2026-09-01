---

name: devops-monitor-30min
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: run
archetype: specialist
time_scale: daily
composition:
  - argus-health-monitor
max_output_tokens: 800

parent_spec: departments/04-engineering-delivery.md
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
---

