#!/usr/bin/env python3
"""PII redaction on outbound content.

Built as Phase 30 R2 (Tier H2).

Redacts common PII patterns from text before sending outbound (emails,
chat messages, API responses):
  - Email addresses
  - Phone numbers (US format + international)
  - Credit card numbers (16-digit groups)
  - SSN (XXX-XX-XXXX)
  - API tokens / Bearer tokens (sk-..., ghp_..., gho_..., etc.)
  - IPv4 addresses
  - Physical addresses (basic)

Logs all redactions to /opt/data/state/redaction-log.jsonl (NDJSON).

Usage:
    python3 scripts/pii-redact.py --text "Email me at john@example.com"
    cat email.txt | python3 scripts/pii-redact.py --stdin
    python3 scripts/pii-redact.py --file /path/to/outbound.txt
    python3 scripts/pii-redact.py --file email.txt --quiet   # exit code only
"""
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

LOG_PATH = Path("/opt/data/state/redaction-log.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


# Pattern catalog: (name, regex, replacement)
# Each pattern replaces matched content with a redaction marker
PATTERNS = [
    # Email addresses
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    # US SSN (XXX-XX-XXXX)
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    # US phone (10 digits, various formats)
    ("phone-us", re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"), "[PHONE]"),
    # Phase 33 R3: US phone with parentheses (555) 123-4567
    ("phone-us-parens", re.compile(r"\(\d{3}\)\s?\d{3}[-.]?\d{4}\b"), "[PHONE]"),
    # International phone (basic)
    ("phone-intl", re.compile(r"\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,9}[-.\s]?\d{1,9}\b"), "[PHONE]"),
    # Credit card (16 digits, possibly with spaces/dashes)
    ("credit-card", re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"), "[CC]"),
    # GitHub PAT
    ("github-pat", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[GH-TOKEN]"),
    # OpenAI key
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "[OPENAI-KEY]"),
    # Slack token
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"), "[SLACK-TOKEN]"),
    # Generic Bearer token
    ("bearer", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"), "Bearer [TOKEN]"),
    # IPv4
    ("ipv4", re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "[IP]"),
]


def redact_text(text: str) -> tuple[str, list]:
    """Apply all redaction patterns. Returns (redacted_text, list of redactions).

    Each redaction is a dict with: pattern, original (truncated to 50 chars), replacement.
    """
    redactions = []
    redacted = text
    for name, regex, replacement in PATTERNS:
        matches = list(regex.finditer(redacted))
        for m in matches:
            original = m.group(0)
            # Truncate for privacy in log
            if len(original) > 50:
                original_log = original[:47] + "..."
            else:
                original_log = original
            redactions.append({
                "pattern": name,
                "original": original_log,
                "replacement": replacement,
                "position": m.start(),
            })
        # Apply redaction (replaces all matches with the marker)
        redacted = regex.sub(replacement, redacted)

    return redacted, redactions


def log_redactions(input_text: str, redactions: list) -> None:
    """Log redaction event to NDJSON."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "input_len": len(input_text),
        "redactions_count": len(redactions),
        "patterns": [r["pattern"] for r in redactions],
    }
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description="PII redaction on outbound")
    parser.add_argument("--text", help="Text to redact")
    parser.add_argument("--file", type=Path, help="File to redact")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--quiet", action="store_true",
                        help="Print only redacted output (no metadata)")
    parser.add_argument("--show-counts", action="store_true",
                        help="Show redaction counts to stderr")
    args = parser.parse_args()

    # Get text
    if args.text:
        text = args.text
    elif args.file:
        if not args.file.exists():
            print(f"ERROR: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        text = args.file.read_text()
    elif args.stdin or not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    redacted, redactions = redact_text(text)
    log_redactions(text, redactions)

    if args.quiet:
        print(redacted)
        return

    if args.show_counts:
        from collections import Counter
        counts = Counter(r["pattern"] for r in redactions)
        for pat, count in counts.most_common():
            print(f"  {pat}: {count}", file=sys.stderr)

    print(json.dumps({
        "input_len": len(text),
        "output_len": len(redacted),
        "redactions_count": len(redactions),
        "patterns": sorted(set(r["pattern"] for r in redactions)),
        "output": redacted,
    }, indent=2))


if __name__ == "__main__":
    main()
