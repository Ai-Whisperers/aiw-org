---

name: ai-ops-coordinator
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: architect
time_scale: minutes
composition:
  - kronos-operations-lead
  - argus-health-monitor
max_output_tokens: 800

---

