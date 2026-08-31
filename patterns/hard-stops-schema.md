# Hard Stops Pattern — YAML Schema

> Canonical format for the hard_stops section of every PROMPT.md.
> **Last updated**: 2026-08-14

---

## Schema spec

```yaml
hard_stops:
  - action: <string>           # action name (snake_case)
    require_approval: <bool>   # true if human approval needed
    approved_human: <string>   # who: ivan, kiki, or both
    rate_limit_per_run: <int>   # max invocations per agent run
    description: <string>       # human-readable
```

## Action types (standard vocabulary)

| Action | Use case | Default |
|--------|----------|---------|
| `read_state` | Read own state file | No approval |
| `write_state` | Write to own state file | No approval, rate 50/run |
| `read_repo` | Read from a repo (no writes) | No approval |
| `send_chat` | Send message to origin chat | No approval |
| `send_external_message` | Email, WhatsApp, LinkedIn DM | Require ivan |
| `send_outreach` | Cold email / cold DM | Require ivan |
| `send_proposal` | Send proposal to client | Require ivan |
| `apply_discount` | Change pricing | Require ivan |
| `apply_refund` | Issue refund | Require ivan |
| `sign_contract` | E-sign any contract | Require ivan (hard rule) |
| `modify_pricing` | Change rate card | Require ivan |
| `merge_pr` | Merge a pull request | Require kiki (or auto-mergeable) |
| `deploy_prod` | Deploy to production | Require kiki |
| `rollback` | Roll back a deploy | No approval (logged) |
| `force_push` | Force-push to git | Require ivan |
| `delete_resource` | Delete any persistent resource | Require ivan+kiki |
| `write_data` | Write to external DB | Require approval (varies) |
| `comment_on_issue` | Comment on a GH issue | Require ivan |
| `close_issue` | Close a GH issue | Require ivan |
| `modify_curriculum` | Edit kiki-coach curriculum | Require kiki |
| `update_thesis_metadata` | Edit thesis state | No approval |
| `submit_arxiv` | Submit paper to arXiv | Require ivan |
| `publish_course_module` | Publish course content | Require ivan+kiki |

## Examples per agent type

### business-analyst
```yaml
hard_stops:
  - action: write_state
    require_approval: false
    rate_limit_per_run: 50
  - action: send_chat
    require_approval: false
  - action: read_repo
    require_approval: false
```

### management-coordinator
```yaml
hard_stops:
  - action: write_state
    require_approval: false
    rate_limit_per_run: 50
  - action: comment_on_issue
    require_approval: true
    approved_human: ivan
  - action: close_issue
    require_approval: true
    approved_human: ivan
```

### kiki-coach
```yaml
hard_stops:
  - action: write_state
    require_approval: false
  - action: send_chat
    require_approval: false  # lesson delivery to origin
  - action: modify_curriculum
    require_approval: true
    approved_human: kiki
```

### finance-controller
```yaml
hard_stops:
  - action: write_state
    require_approval: false
  - action: send_invoice
    require_approval: true
    approved_human: ivan
  - action: apply_refund
    require_approval: true
    approved_human: ivan
  - action: sign_contract
    require_approval: true
    approved_human: ivan
  - action: modify_pricing
    require_approval: true
    approved_human: ivan
```

### sales-pipeline
```yaml
hard_stops:
  - action: write_state
    require_approval: false
  - action: send_outreach
    require_approval: true
    approved_human: ivan
  - action: send_proposal
    require_approval: true
    approved_human: ivan
  - action: apply_discount
    require_approval: true
    approved_human: ivan
  - action: update_deal_stage
    require_approval: false
```

### engineering-roster
```yaml
hard_stops:
  - action: write_state
    require_approval: false
  - action: merge_pr
    require_approval: true
    approved_human: kiki
    rate_limit_per_run: 5
  - action: deploy_prod
    require_approval: true
    approved_human: kiki
  - action: rollback
    require_approval: false  # logged for audit
  - action: force_push
    require_approval: true
    approved_human: ivan
```

### research-tracker
```yaml
hard_stops:
  - action: write_state
    require_approval: false
  - action: update_thesis_metadata
    require_approval: false
  - action: submit_arxiv
    require_approval: true
    approved_human: ivan
  - action: publish_course_module
    require_approval: true
    approved_human: ivan  # + kiki for technical review
```

## Runtime enforcement

`/opt/data/agents-v2/patterns/hard-stop-wrapper.py` checks every action before execution:

```python
def check_hard_stop(action: str, role: str) -> bool:
    """Returns True if action allowed, False if blocked."""
    rules = HARD_STOPS.get(action)
    if not rules:
        return True  # action not in rules = allowed
    if rules.get("require_approval") and role not in rules.get("approved_human", []):
        return False  # blocked
    return True
```

## Verifier

Run `hard-stop-wrapper.py --validate <agent-name>` to check:
- YAML parses correctly
- Every action name is in the standard vocabulary
- Every require_approval=true has an approved_human
- Rate limits are reasonable (1-100)

---

**Document path**: `/opt/data/agents-v2/patterns/hard-stops-schema.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
