---

name: founder-bandwidth-watchdog
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: right-hand
time_scale: daily
composition:
  - clio-customer-signal-collector
max_output_tokens: 800

parent_spec: constitution/ORG-AGENTS.md
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
---

