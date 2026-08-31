#!/usr/bin/env python3
"""webhook-receiver.py — Self-hosted webhook listener for Factor 11.

Accepts POST requests from any payment processor, validates HMAC,
writes customer events to /opt/data/state/customers.json.

Supports processors:
- Mercado Pago (LATAM standard)
- PIX/Banco Central (Brazil)
- Bank transfer (manual webhook via our script)
- Any custom provider (via HMAC secret)

Usage:
    python3 webhook-receiver.py --port 8081
    python3 webhook-receiver.py --test    #  self-test

Endpoints:
    POST /webhook/mercadopago  -> MP payment events
    POST /webhook/pix          -> PIX transfer events
    POST /webhook/bank          -> Bank webhook events
    POST /webhook/custom        -> Custom provider
    POST /webhook/test          -> Test endpoint (no HMAC)
    GET  /health                -> Health check
    GET  /customers             -> List customers (for coach-onboarding to poll)
"""
import argparse
import json
import hmac
import hashlib
import sys
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

# State paths
STATE_DIR = Path("/opt/data/state")
STATE_DIR.mkdir(parents=True, exist_ok=True)
CUSTOMERS_FILE = STATE_DIR / "customers.json"
WEBHOOK_LOG = STATE_DIR / "webhook-log.json"
HMAC_SECRETS_FILE = STATE_DIR / "webhook-secrets.json"

# Default secrets (override via webhook-secrets.json)
DEFAULT_SECRETS = {
    "mercadopago": "mercadopago-webhook-secret-CHANGE-ME",
    "pix": "pix-webhook-secret-CHANGE-ME",
    "bank": "bank-webhook-secret-CHANGE-ME",
    "custom": "custom-webhook-secret-CHANGE-ME",
}


def load_secrets():
    """Load HMAC secrets from file or use defaults."""
    if HMAC_SECRETS_FILE.exists():
        return json.loads(HMAC_SECRETS_FILE.read_text())
    return DEFAULT_SECRETS


def load_customers():
    """Load existing customers."""
    if CUSTOMERS_FILE.exists():
        return json.loads(CUSTOMERS_FILE.read_text())
    return {"customers": [], "last_updated": None}


def save_customers(customers_data):
    """Save customers atomically."""
    tmp = CUSTOMERS_FILE.with_suffix(".tmp")
    customers_data["last_updated"] = datetime.now(timezone.utc).isoformat()
    tmp.write_text(json.dumps(customers_data, indent=2))
    tmp.replace(CUSTOMERS_FILE)


def log_webhook(event_type, processor, payload, status, message=""):
    """Append to webhook audit log."""
    log = []
    if WEBHOOK_LOG.exists():
        log = json.loads(WEBHOOK_LOG.read_text())
    
    log.append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "processor": processor,
        "status": status,
        "message": message,
        "payload_keys": list(payload.keys()) if isinstance(payload, dict) else [],
    })
    
    # Keep last 1000 events
    log = log[-1000:]
    WEBHOOK_LOG.write_text(json.dumps(log, indent=2))


def verify_hmac(processor, body_bytes, signature):
    """Verify HMAC signature. Returns True if valid or no secret set."""
    secrets = load_secrets()
    secret = secrets.get(processor)
    if not secret or secret.startswith("CHANGE-ME"):
        # No real secret set — log warning but allow (dev mode)
        return True, "no-secret-set"
    
    if not signature:
        return False, "missing-signature"
    
    expected = hmac.new(secret.encode(), body_bytes, hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected, signature):
        return True, "valid"
    return False, "invalid-signature"


def normalize_payment_event(processor, payload):
    """Convert processor-specific payload to canonical customer event."""
    if processor == "mercadopago":
        return {
            "customer_id": payload.get("payer", {}).get("id") or payload.get("external_reference"),
            "name": payload.get("payer", {}).get("first_name", "") + " " + payload.get("payer", {}).get("last_name", ""),
            "email": payload.get("payer", {}).get("email"),
            "amount": payload.get("transaction_amount"),
            "currency": payload.get("currency_id", "PYG"),
            "tier": payload.get("metadata", {}).get("tier", "S"),
            "vertical": payload.get("metadata", {}).get("vertical", "unknown"),
            "language": payload.get("metadata", {}).get("language", "es"),
            "source": "mercadopago",
            "raw": payload,
        }
    elif processor == "pix":
        return {
            "customer_id": payload.get("cpf") or payload.get("cnpj") or payload.get("endToEndId"),
            "name": payload.get("nome") or payload.get("payer_name"),
            "amount": payload.get("valor"),
            "currency": "BRL",
            "tier": payload.get("info", {}).get("tier", "S"),
            "vertical": payload.get("info", {}).get("vertical", "unknown"),
            "language": "pt",
            "source": "pix",
            "raw": payload,
        }
    elif processor == "bank":
        return {
            "customer_id": payload.get("account") or payload.get("reference"),
            "name": payload.get("payer_name"),
            "amount": payload.get("amount"),
            "currency": payload.get("currency", "PYG"),
            "tier": payload.get("tier", "S"),
            "vertical": payload.get("vertical", "unknown"),
            "language": payload.get("language", "es"),
            "source": "bank",
            "raw": payload,
        }
    else:  # custom
        return {
            "customer_id": payload.get("customer_id") or payload.get("id"),
            "name": payload.get("name") or payload.get("customer_name"),
            "email": payload.get("email"),
            "amount": payload.get("amount"),
            "currency": payload.get("currency", "PYG"),
            "tier": payload.get("tier", "S"),
            "vertical": payload.get("vertical", "unknown"),
            "language": payload.get("language", "es"),
            "source": "custom",
            "raw": payload,
        }


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Suppress default access logging."""
        pass

    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        if self.path == "/health":
            return self._send_json(200, {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()})
        if self.path == "/customers":
            return self._send_json(200, load_customers())
        self._send_json(404, {"error": "not found"})

    def do_POST(self):
        # Parse path
        parts = self.path.strip("/").split("/")
        if len(parts) < 2 or parts[0] != "webhook":
            return self._send_json(404, {"error": "not found"})
        processor = parts[1]

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)

        # Parse JSON
        try:
            payload = json.loads(body_bytes)
        except json.JSONDecodeError:
            log_webhook("payment", processor, {"raw": body_bytes[:200].decode(errors="replace")}, "rejected", "invalid-json")
            return self._send_json(400, {"error": "invalid json"})

        # Verify HMAC (except /webhook/test)
        signature = self.headers.get("X-Signature") or self.headers.get("X-MercadoPago-Signature") or self.headers.get("Signature")
        if processor != "test":
            valid, reason = verify_hmac(processor, body_bytes, signature)
            if not valid:
                log_webhook("payment", processor, payload, "rejected", reason)
                return self._send_json(401, {"error": "unauthorized", "reason": reason})

        # Normalize and save
        customer_event = normalize_payment_event(processor, payload)
        if not customer_event.get("customer_id"):
            log_webhook("payment", processor, payload, "rejected", "no-customer-id")
            return self._send_json(400, {"error": "no customer id in payload"})

        # Add timestamp + write to customers.json
        customer_event["received_at"] = datetime.now(timezone.utc).isoformat()
        customer_event["onboarded"] = False
        customer_event["webhook_id"] = payload.get("id") or hashlib.md5(body_bytes).hexdigest()[:12]

        customers_data = load_customers()
        # Dedupe by webhook_id
        existing_ids = {c.get("webhook_id") for c in customers_data["customers"]}
        if customer_event["webhook_id"] not in existing_ids:
            customers_data["customers"].append(customer_event)
            save_customers(customers_data)
            log_webhook("payment", processor, payload, "stored", f"new customer {customer_event['customer_id']}")
            return self._send_json(200, {"status": "stored", "customer": customer_event})
        else:
            log_webhook("payment", processor, payload, "duplicate", f"webhook_id {customer_event['webhook_id']} already seen")
            return self._send_json(200, {"status": "duplicate", "customer_id": customer_event["customer_id"]})


def run_server(port):
    server = HTTPServer(("127.0.0.1", port), WebhookHandler)
    print(f"Webhook receiver listening on http://127.0.0.1:{port}")
    print("Endpoints:")
    print(f"  POST /webhook/mercadopago")
    print(f"  POST /webhook/pix")
    print(f"  POST /webhook/bank")
    print(f"  POST /webhook/custom")
    print(f"  POST /webhook/test  (no HMAC required)")
    print(f"  GET  /health")
    print(f"  GET  /customers")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def self_test():
    """Run a self-test without binding to port."""
    import urllib.request, urllib.error
    
    # Test via direct call (can't easily test HTTP from within process)
    # Instead, test the normalize function
    test_payload = {"payer": {"id": "test123", "email": "test@example.com", "first_name": "Test", "last_name": "User"}, "transaction_amount": 500, "currency_id": "PYG", "metadata": {"tier": "M"}}
    result = normalize_payment_event("mercadopago", test_payload)
    print(f"Normalized MP event: {result}")
    assert result["tier"] == "M", f"Expected M, got {result['tier']}"
    
    # Test HMAC verify
    body = json.dumps(test_payload).encode()
    secret = "test-secret"
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    valid, _ = verify_hmac("custom", body, sig)
    assert valid, "HMAC should be valid"
    
    print("\n✓ Self-test passed")
    print("✓ Normalize works")
    print("✓ HMAC verify works")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8081, help="Port to listen on")
    parser.add_argument("--test", action="store_true", help="Run self-test")
    args = parser.parse_args()
    
    if args.test:
        self_test()
    else:
        run_server(args.port)
