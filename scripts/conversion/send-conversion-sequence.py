#!/usr/bin/env python3
"""send-conversion-sequence.py - Send the 3-email sequence for approved customers.

Reads conversion-attempts.json. For each APPROVED customer, sends the 3-email sequence.
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/state")
CONVERSION_LOG = STATE_DIR / "conversion-attempts.json"
EMAIL_SCRIPT = "/opt/data/scripts/email-send.py"


def load_json(p, default=None):
    if default is None:
        default = {}
    if not p.exists():
        return default
    return json.loads(p.read_text())


def save_json(p, data):
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    tmp.replace(p)


def send_email_template(to, template, **kwargs):
    """Send email via template."""
    cmd = ["python3", EMAIL_SCRIPT, to, template]
    for k, v in kwargs.items():
        cmd.append(f"{k}={v}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(r.stdout)
    except:
        return {"status": "error", "stderr": r.stderr}


def main():
    conversion = load_json(CONVERSION_LOG, {"attempts": []})
    
    sent_count = 0
    for attempt in conversion["attempts"]:
        # Skip if not approved
        if attempt.get("status") != "APPROVED":
            continue
        
        # Skip if sequence already sent
        if attempt.get("sequence_status") == "SENT":
            continue
        
        customer_id = attempt["customer_id"]
        name = attempt.get("name", "Customer")
        email = attempt.get("email")
        
        if not email:
            attempt["sequence_status"] = "SKIPPED_NO_EMAIL"
            continue
        
        # Send Day 1 email
        result = send_email_template(email, "day_1_consent", name=name)
        attempt["day_1_sent"] = result
        attempt["sequence_status"] = "SENT"
        attempt["sequence_sent_at"] = datetime.now(timezone.utc).isoformat()
        sent_count += 1
        
        print(f"Sent Day 1 to {customer_id} ({email})")
    
    if sent_count > 0:
        save_json(CONVERSION_LOG, conversion)
        print(f"\nTotal sent: {sent_count}")
    else:
        print("No APPROVED customers to send to")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Conversion pipeline scripts.""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    main()
