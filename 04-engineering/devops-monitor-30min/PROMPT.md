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
parent_spec: departments/04-engineering-delivery.md
max_output_tokens: 800
fallback_model: litellm/reasoning
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
  - action: disable_hardstop
    require_approval: true
    approved_human: ivan+kiki
  - action: modify_eval_gates
    require_approval: true
    approved_human: ivan

---
## Cron Schedule

- Every 30 minutes
- Owner: Erebus (crosscut)
- Monitors: cron error rate, failed runs, queue depth

## Read Org State (Factor 5)

Before running, read the unified org state:

```bash
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100
```

**What this gives you:**
- Last eval-gate stats
- Recent cron errors (if any)
- Active chaos-runner state
- Token ledger headroom

**See:** `/opt/data/skills/factor-5-unified-state/SKILL.md` for the full pattern.

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: read_state
  - action: write_state
  - action: emit_signal
  - action: comment_on_issue
  - action: restart_cron
```

## Notes

- Composed of: argus-health-monitor (crosscut)
- 30-min interval is the production gate for health signals
- Failures here cascade to founder-bandwidth-watchdog (weekly summary)