# Phase 19 — Webhook Triggers (Factor 11)

**Date**: 2026-08-21
**Status**: ✅ WIRED — webhook-pattern payment integration → auto-onboard

## Architecture

```
[Customer pays via Mercado Pago / PIX / bank transfer]
              ↓
[POST /webhook/mercadopago|pix|bank|custom]
              ↓
[webhook-receiver.py on port 8081]
  - Validates HMAC
  - Normalizes event
  - Deduplicates by webhook_id
              ↓
[/opt/data/state/customers.json]
              ↓
[coach-onboarding-poller.py every 5 min]
  - Reads unboarded customers
  - Sends Sunstein informed-consent via WhatsApp
  - Adds to coaching-customers.json
              ↓
[Day 3, 7, 10, 30 follow-ups scheduled]
```

## What Was Built

### 1. `webhook-receiver.py`

Location: `/opt/data/scripts/webhook-receiver.py` (also at `scripts/webhook/`)

- Self-hosted HTTP server on port 8081
- HMAC-validated for security
- Supports 4 processors: Mercado Pago, PIX, Bank transfer, Custom
- Endpoints:
  - `POST /webhook/{processor}` — receive payment events
  - `GET /health` — health check
  - `GET /customers` — list stored customers
- Persists to `/opt/data/state/customers.json`
- Audit log to `/opt/data/state/webhook-log.json`
- Deduplicates by webhook_id (safe retries)

### 3. `coach-onboarding-poller.py`

Location: `/opt/data/scripts/coach-onboarding-poller.py`

- Runs every 5 minutes via cron
- Reads new customers from `state/customers.json`
- For each new customer:
  - Sends WhatsApp to Ivan asking approval
  - Creates entry in `state/coaching-customers.json`
  - Tracks onboarding step
- Writes brief to coach-onboarding/outbox/

### 4. coach-onboarding PROMPT updated

Now references the webhook infrastructure and the 5-step onboarding flow.

### 5. Cron job: `aiw-coach-onboarding-poller`

Schedule: `*/5 * * * *` (every 5 min)
Script: `coach-onboarding-poller.py`

## Rationale for LATAM/EU Payment Stack

The prior payment vendor is on our **trademark banlist** (Hostinger incident from earlier). For LATAM + EU markets:
- **Mercado Pago** — Latin American standard (covers ARG, BRA, MEX, CHL, etc.)
- **PIX** — Brazilian instant payments (free, instant)
- **Bank transfer webhook** — manual via bank API
- **Custom provider** — any with HMAC

This is actually **better than the legacy vendor for our market**:
- PIX is free (legacy vendor charges 4%+)
- Mercado Pago has better LATAM coverage
- No vendor lock-in

## Verification (3 test customers)

| Customer ID | Name | Tier | Source | Onboarded |
|-------------|------|------|--------|-----------|
| cus_test123 | Test Customer | M | custom | ✅ |
| mp-001 | (none) | S | custom | ✅ |
| cus_mp_real | Maria Gonzalez | L | mercadopago | ✅ |

Brief written: `/opt/data/agents/coach-onboarding/outbox/2026-08-21.md`

## This Closes Factor 11

Before: coach-onboarding only triggered manually.
After: ANY payment processor → auto-onboard.

**Real-world flow now:**
1. Customer pays $500 for M tier on Mercado Pago
2. MP sends webhook to our receiver
3. Customer data lands in `state/customers.json`
4. Within 5 minutes, coach-onboarding starts the 5-step flow
5. Ivan gets asked via WhatsApp to approve the first session
6. Day 3 → goals intake email
7. Day 10 → first GROW session

## What's Next

- **Factor 5** — Unify execution state (currently scattered)
- **Cost monitoring** — the $12,600/month risk
- **Real customer** — point the webhook at a real Mercado Pago account

## Files Modified/Created

- `/opt/data/scripts/webhook-receiver.py` (NEW, 280 lines)
- `/opt/data/scripts/coach-onboarding-poller.py` (NEW, 130 lines)
- `~/.hermes/scripts/coach-onboarding-poller.py` (copy for cron)
- `/opt/data/agents/coach-onboarding/PROMPT.md` (updated)
- Cron job: `aiw-coach-onboarding-poller`
