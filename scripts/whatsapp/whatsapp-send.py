#!/usr/bin/env python3
"""whatsapp-send.py — Send WhatsApp messages via Evolution API.

Used by agents for human-in-loop (Factor 7 of 12-factor-agents).
"""
import sys
import os
import json
import urllib.request
from pathlib import Path

EVOLUTION_URL = "https://evolution.paragu-ai.com"
EVOLUTION_KEY = "a53c00ff3726d2ced6bbfeba8d1a1e90"
INSTANCE = "aiw-alerts-v2"
CONFIG_PATH = Path("/opt/data/.whatsapp-config.json")

# Recipient registry: name -> number
RECIPIENTS = {
    "ivan": "595981324569",
    "kiki": "595981501444",  # Kyrian's number
    "kynian": "595981501444",
    "test": "595981324569",
}

def get_recipient(name_or_number: str) -> str:
    """Resolve recipient name to number, or pass through if already a number."""
    if name_or_number in RECIPIENTS:
        return RECIPIENTS[name_or_number]
    # Try case-insensitive
    for k, v in RECIPIENTS.items():
        if k.lower() == name_or_number.lower():
            return v
    # Pass through (assume it's already a number)
    return name_or_number

def send_text(number: str, text: str, sender: str = "erebus") -> dict:
    """Send a text message. Returns the API response."""
    payload = {
        "number": get_recipient(number),
        "mediatype": "conversation",
        "text": text,
    }
    req = urllib.request.Request(
        f"{EVOLUTION_URL}/message/sendText/{INSTANCE}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "apikey": EVOLUTION_KEY,
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            response = json.loads(r.read())
            return {"status": "sent", "number": payload["number"], "response": response, "sender": sender}
    except Exception as e:
        return {"status": "error", "error": str(e), "sender": sender}

def main():
    if len(sys.argv) < 3:
        print("Usage: whatsapp-send.py <recipient> <message> [--sender NAME]")
        print(f"Known recipients: {', '.join(RECIPIENTS.keys())}")
        sys.exit(1)
    
    recipient = sys.argv[1]
    message = sys.argv[2]
    sender = "erebus"
    
    if "--sender" in sys.argv:
        idx = sys.argv.index("--sender")
        sender = sys.argv[idx + 1]
    
    result = send_text(recipient, message, sender)
    print(json.dumps(result, indent=2, default=str))
    
    sys.exit(0 if result["status"] == "sent" else 2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

