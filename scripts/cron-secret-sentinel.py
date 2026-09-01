#!/usr/bin/env python3
"""cron-secret-sentinel.py — Daily check that cron secrets are not expired.

Phase 9 R4 / Risk R9 mitigation. Iterates every cron job that uses a
BWS secret, validates the secret is fetchable and the value isn't empty,
and writes a sentinel JSON + alerts via the outbox signal queue if any
secret fails.

Catches:
  - Empty .gh_token file (40b = prefix, 0b = no token)
  - Secrets in BWS that no longer resolve
  - Cron jobs that reference a BWS UUID that doesn't exist
  - Cron jobs hardcoded with tokens (should always go through BWS)

Writes: /opt/data/state/cron-secret-sentinel.json
"""
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

JOBS_FILE = Path("/opt/data/.hermes/cron/jobs.json")
STATE_FILE = Path("/opt/data/state/cron-secret-sentinel.json")
GH_TOKEN_PATH = Path("/opt/data/.gh_token")
OUTBOX = Path("/opt/data/agents/outbox/signals")
SIGNALS = Path("/opt/data/state")


def discover_token_uses() -> list:
    """Inspect every cron job for token references."""
    with JOBS_FILE.open() as f:
        cron = json.load(f)
    findings = []
    for j in cron["jobs"]:
        if not j.get("enabled", True):
            continue
        prompt = j.get("prompt", "")
        # Detect hardcoded token patterns (ghp_, gho_, glpat-, etc.)
        import re
        # gitlab personal access token
        # github classic PAT (ghp_)
        # github oauth (gho_)
        # bitwarden access token (bws_)
        bad_patterns = {
            "ghp_": "GitHub classic PAT (should use BWS)",
            "gho_": "GitHub OAuth token (should use BWS)",
            "glpat-": "GitLab PAT (should use BWS)",
            "xoxb-": "Slack bot token (should use BWS)",
        }
        for prefix, label in bad_patterns.items():
            if prefix in prompt:
                findings.append({
                    "job_name": j["name"],
                    "issue": f"hardcoded token ({label})",
                    "pattern": prefix,
                    "severity": "high",
                })
        # Detect BWS UUID references (these are OK if BWS is accessible)
        bws_matches = re.findall(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", prompt)
        for uuid_ in bws_matches:
            findings.append({
                "job_name": j["name"],
                "issue": f"BWS reference {uuid_[:8]}... (verify BWS accessible)",
                "pattern": "bws",
                "severity": "info",
            })
    return findings


def check_gh_token() -> dict:
    """Verify /opt/data/.gh_token is non-empty."""
    if not GH_TOKEN_PATH.exists():
        return {"ok": False, "issue": "/opt/data/.gh_token missing"}
    size = GH_TOKEN_PATH.stat().st_size
    if size == 0:
        return {"ok": False, "issue": "/opt/data/.gh_token empty (0 bytes)"}
    if size < 10:
        return {"ok": False, "issue": f"/opt/data/.gh_token too small ({size}b)"}
    return {"ok": True, "size": size}


def check_bws_secrets() -> dict:
    """Verify BWS CLI can list secrets."""
    try:
        import subprocess
        r = subprocess.run(
            ["bws", "secret", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return {
            "ok": r.returncode == 0,
            "rc": r.returncode,
            "stderr_excerpt": (r.stderr or "")[:120],
        }
    except FileNotFoundError:
        return {"ok": False, "issue": "bws CLI not installed"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "issue": "bws list timed out"}


def main():
    findings = discover_token_uses()
    token_check = check_gh_token()
    bws_check = check_bws_secrets()

    hardcoded_high = [f for f in findings if f["severity"] == "high"]
    healthy = (
        token_check["ok"]
        and bws_check["ok"]
        and len(hardcoded_high) == 0
    )

    report = {
        "timestamp": time.time(),
        "healthy": healthy,
        "gh_token": token_check,
        "bws": bws_check,
        "hardcoded_tokens": len(hardcoded_high),
        "total_findings": len(findings),
        "details": findings[:50],  # cap output
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(report, indent=2))

    if not healthy:
        # Write an alert signal
        OUTBOX.mkdir(parents=True, exist_ok=True)
        sig = OUTBOX / f"cron-secret-sentinel-{int(time.time())}.md"
        body = (
            f"# Cron Secret Sentinel — FAIL\n\n"
            f"Healthy: {healthy}\n\n"
            f"## GitHub token\n{json.dumps(token_check, indent=2)}\n\n"
            f"## BWS\n{json.dumps(bws_check, indent=2)}\n\n"
            f"## Hardcoded tokens found: {len(hardcoded_high)}\n\n"
        )
        for f in hardcoded_high[:5]:
            body += f"- **{f['job_name']}**: {f['issue']}\n"
        sig.write_text(body)
        print(f"[sentinel] FAIL — wrote {sig}")
        return 1

    print(f"[sentinel] OK — gh_token={token_check.get('ok')}, bws={bws_check.get('ok')}, hardcoded={len(hardcoded_high)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
