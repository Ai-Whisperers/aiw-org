---
name: business-analyst
version: 0.2.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
archetype: specialist
time_scale: daily
composition:
  - business-analyst
  - themis-document-classifier
transfer_targets:
  - 02-finance-legal/finance-controller
  - 03-sales-growth/sales-pipeline
---

## CHANGELOG

- v0.2.0 (2026-08-14): upgraded to 12-section template. Added hard stops, idempotency, context-payload, fallback model, escalation triggers.
- v0.1.0 (2026-08-13): initial rollout. 4 sections. Org-pulse.sh not yet wired.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['business-analyst']['latest_brief'])
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
