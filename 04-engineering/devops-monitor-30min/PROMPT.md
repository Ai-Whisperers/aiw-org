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
---

name: devops-monitor-30min
version: 0.1.0
schedule: "*/30 * * * *"
owner: erebus
parent_spec: departments/04-engineering-delivery.md
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

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: merge_pr
  - action: comment_on_pr
  - action: block_merge
  - action: block_output
  - action: restart_service
  - action: close_issue
  - action: comment_on_issue
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
print('My last brief:', s['agents']['devops-monitor-30min']['latest_brief'])
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

---

## Recipe (per `recipe-not-conversation` pattern)

This agent is runnable as a recipe. The steps below are explicit and ordered.

### Step 1: Read context
- **Inputs:** `state/org-state.json`, previous brief
- **Outputs:** in-context summary
- **Done when:** `latest_brief` and `eval_gate` are in working memory

### Step 2: Monitor health signals
- **Inputs:** in-context summary, hard_stops list above
- **Outputs:** health check results (each monitored metric)
- **Done when:** every monitored metric has a current value

### Step 3: Detect deviations
- **Inputs:** health check results, threshold table
- **Outputs:** prioritized alert list
- **Done when:** every deviation has severity + metric + threshold

### Step 4: File alerts
- **Inputs:** prioritized alert list, hard_stops
- **Outputs:** filed signals (with `routing_tags: ["devops", "alert"]`)
- **Done when:** every HIGH/CRITICAL alert has a filed signal

### Step 5: Update state
- **Inputs:** filed alerts list
- **Outputs:** updated `state/coord.json` via approved operator
- **Done when:** changes committed; no silent mutations

### Verification criteria

A successful run:
- [ ] Step 1-5 each completed without silent skipping
- [ ] All HIGH/CRITICAL deviations have filed signals
- [ ] No hard_stop bypassed
- [ ] `state/coord.json` updated (or explicitly unchanged)

### Dependencies

- Requires: `state/org-state.json` exists and is valid
- Depends on: `argus-health-monitor` (composition)
- Blocks: `compliance-monitor` (safety escalation)

### See also

- `/opt/data/agents/docs/patterns/recipe-not-conversation.md` — the meta-pattern
- `/opt/data/agents/docs/patterns/architect-then-builder.md` — design vs build separation
