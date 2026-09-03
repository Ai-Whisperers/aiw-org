#!/usr/bin/env python3
"""
model-probe.py — Empirical test to identify which model litellm-primary resolves to.

Sends the same 1k-token prompt to the litellm proxy with model="primary"
and measures the response characteristics + token counts. The result
tells us if primary is Sonnet, Haiku, Opus, GLM, or something else.

This is the missing data point that cost-per-cron.py needs to give accurate
estimates. Without it, we default to Sonnet 4.6 rates, which may over- or
under-estimate by 5-10x.

Output:
  /opt/data/state/model-probe-result.json

Usage:
  python3 model-probe.py                # full probe
  python3 model-probe.py --quick        # 1-call probe
"""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.error

# litellm proxy endpoint
PROXY_URL = os.environ.get("LITELLM_PROXY_URL", "http://localhost:4000/v1/messages")
PROXY_KEY = os.environ.get("HERMES_LITELLM_API_KEY", "")

PROBE_PROMPT = "In one sentence, what is the capital of Paraguay?"
PROBE_MAX_TOKENS = 50

OUTPUT_FILE = Path("/opt/data/state/model-probe-result.json")


def probe(model_alias: str, max_tokens: int = PROBE_MAX_TOKENS) -> dict:
    """Send probe to litellm and capture response metadata."""
    if not PROXY_KEY:
        return {"error": "HERMES_LITELLM_API_KEY not set", "model": model_alias}

    payload = {
        "model": model_alias,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": PROBE_PROMPT}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PROXY_KEY,
        "anthropic-version": "2023-06-01",
    }
    req = urllib.request.Request(
        PROXY_URL,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        latency = time.time() - start
        return {
            "model": model_alias,
            "latency_seconds": round(latency, 3),
            "response_model": body.get("model", "unknown"),
            "input_tokens": body.get("usage", {}).get("input_tokens", 0),
            "output_tokens": body.get("usage", {}).get("output_tokens", 0),
            "stop_reason": body.get("stop_reason", "unknown"),
            "content_preview": (body.get("content", [{}])[0].get("text", "") if body.get("content") else "")[:200],
        }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:300]}", "model": model_alias}
    except Exception as e:
        return {"error": str(e), "model": model_alias}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="only probe 'primary' alias")
    args = p.parse_args()

    results = {"computed_at": datetime.now(timezone.utc).isoformat(), "probes": []}

    aliases = ["primary"] if args.quick else ["primary", "fast", "reasoning"]
    print(f"Probing model aliases: {aliases}")
    for alias in aliases:
        print(f"\nProbing {alias}...")
        result = probe(alias)
        results["probes"].append(result)
        if "error" in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Resolved model: {result.get('response_model','?')}")
            print(f"  Latency: {result.get('latency_seconds','?')}s")
            print(f"  Tokens: in={result.get('input_tokens','?')} out={result.get('output_tokens','?')}")
            print(f"  Content: {result.get('content_preview','')[:100]}")

    # Determine mapping
    mapping = {}
    for r in results["probes"]:
        if "error" not in r:
            mapping[r["model"]] = r["response_model"]
    results["alias_to_model_mapping"] = mapping
    print(f"\n=== Alias mapping ===")
    for alias, resolved in mapping.items():
        print(f"  {alias} → {resolved}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2))
    tmp.replace(OUTPUT_FILE)
    print(f"\nWritten: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
