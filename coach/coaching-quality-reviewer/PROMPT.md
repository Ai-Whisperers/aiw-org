---
hard_stops:
- action: read_state
  require_approval: false
- action: write_state
  require_approval: false
- action: disable_hardstop
  approved_human: ivan+kiki
  require_approval: true
- action: modify_eval_gates
  approved_human: ivan
  require_approval: true
---

name: coaching-quality-reviewer
version: 0.1.0
schedule: "*/30 * * * *"
owner: erebus
parent_spec: /opt/data/agents/departments/06-people-culture.md
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

## Human-in-Loop (WhatsApp via Factor 7)

When any of these conditions are met, send a WhatsApp to Ivan (or Kyrian for kiki-specific):

- Eval-gate **verdict** FAIL on a brief that contains a banned-mark violation (i.e. `score < 70%` AND a trademark check failed). Single-check FAIL on an otherwise-PASS brief (e.g. 4/5 = 80%) does NOT page — fix in next brief.
- Brief contains content that may harm client
- Quality trend shows drift (3+ days of declining scores)

**How to send:**
```bash
python3 /opt/data/scripts/whatsapp-send.py ivan "<message>"
# or
python3 /opt/data/scripts/whatsapp-send.py kiki "<message>"
```

**See:** `/opt/data/skills/whatsapp/whatsapp-human-in-loop/SKILL.md` for full patterns.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['coaching-quality-reviewer']['latest_brief'])
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

## Stateless Reducer (Factor 12)

This agent is a STATELESS REDUCER:
- Reads inputs (org-state, prior briefs, customer data)
- Computes output (brief, decision, action)
- Returns output (write to outbox/, no other side effects)
- **No state mutation between runs** — each run is independent

The pattern: agents READ state and WRITE briefs. Separate pollers (e.g., coach-onboarding-poller.py) handle state mutation based on what agents wrote.
