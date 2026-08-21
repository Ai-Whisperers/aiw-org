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

name: coach-onboarding
version: 0.1.0
schedule: "triggered on new customer signup (via webhook from CF Worker)"
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

- Customer doesn't verify email within 24h
- Customer skips informed consent
- Customer asks to skip steps

**How to send:**
```bash
python3 /opt/data/scripts/whatsapp-send.py ivan "<message>"
# or
python3 /opt/data/scripts/whatsapp-send.py kiki "<message>"
```

**See:** `/opt/data/skills/whatsapp/whatsapp-human-in-loop/SKILL.md` for full patterns.

## Trigger: Webhook Customer Event (Factor 11)

This agent is triggered by webhook events from payment processors via `/opt/data/scripts/webhook-receiver.py`.

**How it works:**
1. Customer pays via Mercado Pago / PIX / bank transfer / custom processor
2. Processor sends webhook POST to our receiver (HMAC-validated)
3. Receiver normalizes event and appends to `/opt/data/state/customers.json`
4. coach-onboarding is triggered (via cron every 5 min OR direct webhook to this agent)
5. Agent reads new customer from `state/customers.json`, sends Sunstein informed-consent
6. Begins 5-step 30-day onboarding flow

**Webhook receiver endpoints:**
- POST /webhook/mercadopago — Mercado Pago LATAM
- POST /webhook/pix — PIX Brazil
- POST /webhook/bank — Bank transfer (manual)
- POST /webhook/custom — Any provider with HMAC
- GET /health — Health check
- GET /customers — List customers (poll endpoint)

**State file format:**
```json
{
  "customers": [
    {
      "customer_id": "cus_xxx",
      "name": "Maria Gonzalez",
      "email": "client@example.com",
      "amount": 1500,
      "currency": "PYG",
      "tier": "L",
      "vertical": "dental",
      "language": "es",
      "source": "mercadopago",
      "received_at": "2026-08-21T03:57:00Z",
      "onboarded": false,
      "webhook_id": "mp-002"
    }
  ],
  "last_updated": "2026-08-21T03:57:00Z"
}
```

**Onboarding logic:**
1. Check `state/customers.json` for `onboarded == false` entries
2. For each new customer:
   a. Send WhatsApp informed-consent (Factor 7)
   b. Create entry in `state/coaching-customers.json`
   c. Send Day 3 goals-intake email
   d. Set `onboarded: true`
3. Write brief to `/opt/data/agents/coach-onboarding/outbox/YYYY-MM-DD.md`

**See:** `/opt/data/skills/devops/webhook-subscriptions/` for webhook setup patterns.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['coach-onboarding']['latest_brief'])
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
