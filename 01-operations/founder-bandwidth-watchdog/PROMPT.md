---

name: founder-bandwidth-watchdog
version: 0.2.0
schedule: "0 18 * * 0"  # Weekly Sunday 18:00 PYT
owner: ivan
layer: business
topology: stream-aligned
archetype: specialist
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800
fallback_model: litellm/primary
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
## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: comment_on_issue
  - action: block_merge
  - action: block_output
  - action: restart_service
  - action: block_ip
  - action: read_state
  - action: write_state
```

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['founder-bandwidth-watchdog']['latest_brief'])
print('My eval-gate stats:', s['eval_gate'])
print('Recent customers:', s['global']['customers'][-3:])
"
```

**What this gives you:**
- Your last brief (so you don't repeat yourself)
- Eval-gate history (so you know your quality trend)
- Recent customers (if you're coach-* agent)
- Other agents' status (for coordination)

**See:** `/opt/data/skills/factor-5-unified-state/SKILL.md` for the full pattern.

## Cron Schedule

- Weekly Sunday 18:00 PYT (notify-only)
- Owner: Ivan
- Output: weekly founder bandwidth summary to /opt/data/agents/outbox/

## Notes

- This agent is invoked manually or via cron at week boundaries
- Outputs a 1-page summary, no autonomous actions