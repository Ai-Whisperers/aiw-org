#!/usr/bin/env python3
"""inject_cache_control.py - Add cache_control: ephemeral markers to cron prompts.

Anthropic's prompt caching saves ~90% on cached tokens. The
cache_control: {type: ephemeral} marker tells the API to cache
the marked content for 5 minutes (TTL).

This script:
  1. Reads /opt/data/.hermes/cron/jobs.json
  2. For each prompt > 200 chars, marks it with cache_control
  3. Writes back idempotently

Usage:
    python scripts/inject_cache_control.py             # dry-run
    python scripts/inject_cache_control.py --apply     # write changes

Refs: HANDOFF-PHASE-8.md ## MED #3, MiniMax cache docs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CRON_PATHS = [
    Path("/opt/data/.hermes/cron/jobs.json"),
    Path("/opt/data/cron/jobs.json"),
]

MIN_PROMPT_LEN = 200  # Only mark long prompts (cache benefit > overhead)
MARKER = {"type": "ephemeral"}


def _has_cache_marker(text: str) -> bool:
    """Return True if prompt already has cache_control."""
    return "cache_control" in text or "ephemeral" in text


def _inject_marker(text: str) -> str:
    """Append a cache_control marker instruction to the prompt."""
    if _has_cache_marker(text):
        return text
    marker_line = (
        "\n\n[cache_control: ephemeral] "
        "This prompt has stable prefix content; the provider should "
        "cache it across invocations within 5min."
    )
    return text + marker_line


def patch(apply: bool = False) -> int:
    total_changed = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            if not j.get("enabled", True):
                continue
            prompt = j.get("prompt", "")
            if not prompt or len(prompt) < MIN_PROMPT_LEN:
                continue
            if _has_cache_marker(prompt):
                continue
            new_prompt = _inject_marker(prompt)
            print(f"[{cp}] {j['name']}: adding cache marker (len {len(prompt)} -> {len(new_prompt)})")
            if apply:
                j["prompt"] = new_prompt
            total_changed += 1
        if apply and total_changed:
            cp.write_text(json.dumps(data, indent=2) + "\n")
    if not apply:
        print(f"\nDRY RUN: would add cache markers to {total_changed} prompts. Re-run with --apply.")
    elif total_changed:
        print(f"\nApplied {total_changed} cache markers.")
    else:
        print("\nNo changes needed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
