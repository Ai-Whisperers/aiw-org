# Webhook directory

This directory previously held standalone webhook receivers for individual
processors. As of 2026-08-28, all processors are integrated into the main
receiver at `/opt/data/home/.hermes/scripts/webhook-receiver.py` — a single
process listening on one port.

## Supported processors

| Processor | Endpoint | HMAC header |
|---|---|---|
| Mercado Pago | `POST /webhook/mercadopago` | `X-MercadoPago-Signature` (hex) |
| PIX | `POST /webhook/pix` | `X-Signature` (hex) |
| Bank | `POST /webhook/bank` | `X-Signature` (hex) |
| **Lemon Squeezy** | `POST /webhook/lemonsqueezy` | `X-Signature: sha256=<hex>` |
| Custom | `POST /webhook/custom` | `X-Signature` (hex) |

Plus `POST /webhook/test` (no HMAC), `GET /health`, `GET /customers`.

## HMAC secrets

Stored in `/opt/data/state/webhook-secrets.json`:

```json
{
  "mercadopago": "...",
  "pix": "...",
  "bank": "...",
  "lemonsqueezy": "...",
  "custom": "..."
}
```

Or via env vars (`LEMONSQUEEZY_WEBHOOK_SECRET`, etc.). Placeholder values
matching `*-CHANGE-ME*` allow the receiver to run unsigned (dev mode only).

## Archived standalone handler

The pre-merge standalone Lemon Squeezy handler was archived at:
- `/opt/data/archive/legal-clients/lemonsqueezy-webhook-receiver.py.archived-2026-08-28`

Do not run that script in parallel with the main receiver — it would
double-write to `customers.json`.

## Self-test

```bash
python3 /opt/data/home/.hermes/scripts/webhook-receiver.py --test
```

Exercises: MP normalize, custom HMAC verify, LS normalize, LS HMAC verify
with `sha256=` prefix, LS HMAC rejection of bad sig / missing prefix /
empty / placeholder bypass.

## Production run

```bash
python3 /opt/data/home/.hermes/scripts/webhook-receiver.py --port 8081
```

Behind a TLS-terminating reverse proxy (Caddy / Traefik). Use the existing
Tunnel config to expose the webhook URL to upstream providers.