#!/usr/bin/env python3
"""compact-errors.py — Compact cron errors into structured form (Factor 9).

Instead of dumping raw exception traces, extract:
- error_type (rate_limit, auth, timeout, etc.)
- error_code (HTTP 402, 429, etc.)
- retry_after (if available)
- affected_job
- fix_suggestion

Stores to /opt/data/state/errors.json for eval-gate + self-running-check.
"""
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

STATE_DIR = Path("/opt/data/state")
ERRORS_FILE = STATE_DIR / "errors.json"


def classify_error(error_msg: str) -> dict:
    """Classify an error message into structured form."""
    error_msg = str(error_msg)
    
    # Default
    result = {
        "type": "unknown",
        "code": None,
        "retry_after_seconds": None,
        "suggestion": "Check logs and retry",
    }
    
    # HTTP status codes
    http_match = re.search(r'HTTP\s+(\d{3})', error_msg)
    if http_match:
        code = int(http_match.group(1))
        result["code"] = code
        
        if code == 402:
            result["type"] = "billing"
            result["suggestion"] = "Top up LLM credits (OpenRouter $20) or switch providers"
        elif code == 429:
            result["type"] = "rate_limit"
            result["suggestion"] = "Wait for rate limit reset or use backup provider"
        elif code == 401:
            result["type"] = "auth"
            result["suggestion"] = "Rotate API keys in /opt/data/state/secrets/"
        elif code == 404:
            result["type"] = "not_found"
            result["suggestion"] = "Check resource path or model name"
        elif code == 500:
            result["type"] = "server_error"
            result["suggestion"] = "Retry with backoff or switch provider"
        elif code == 503:
            result["type"] = "unavailable"
            result["suggestion"] = "Service down — use backup or wait"
    
    # Specific patterns
    if "single tool-calls at once" in error_msg:
        result["type"] = "model_limit"
        result["suggestion"] = "Switch to reasoning model (multi-tool capable)"
    elif "No deployments available" in error_msg:
        result["type"] = "cooldown"
        result["suggestion"] = "Wait 30s or switch provider"
    elif "Rate limit exceeded" in error_msg:
        result["type"] = "rate_limit"
        # Extract reset time if available
        reset_match = re.search(r'"X-RateLimit-Reset":"(\d+)"', error_msg)
        if reset_match:
            reset_ts = int(reset_match.group(1)) / 1000
            result["retry_after_seconds"] = max(0, reset_ts - datetime.now(timezone.utc).timestamp())
    elif "Connection" in error_msg or "timeout" in error_msg.lower():
        result["type"] = "network"
        result["suggestion"] = "Check network or use backup endpoint"
    elif "Script not found" in error_msg:
        result["type"] = "config"
        result["suggestion"] = "Copy script to ~/.hermes/scripts/ or fix path"
    elif "Paused/disabled" in error_msg or "paused/disabled" in error_msg.lower():
        result["type"] = "paused"
        result["suggestion"] = "hermes cron resume <job_id>"
    elif "schedule" in error_msg.lower() and "?" in error_msg:
        result["type"] = "schedule"
        result["suggestion"] = "hermes cron edit <id> --schedule '<expr>'"
    elif "invalid" in error_msg.lower() and "json" in error_msg.lower():
        result["type"] = "data"
        result["suggestion"] = "Check JSON syntax in source file"
    elif "hermes: command not found" in error_msg or "command not found" in error_msg.lower():
        result["type"] = "env"
        result["suggestion"] = "Check PATH or install missing dependency"
    
    return result


def get_recent_errors() -> list:
    """Get recent errors from cron runs + heartbeat log."""
    errors = []
    
    # Parse cron heartbeat log
    log_path = Path("/opt/data/agents/state/cron-heartbeat-alerts.log")
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            m = re.match(r'\[([^\]]+)\] \[ERROR\] cron job \'([^\']+)\' is in error state', line)
            if m:
                errors.append({
                    "ts": m.group(1),
                    "job": m.group(2),
                    "source": "heartbeat",
                    "raw": line,
                })
    
    # Get last 50 cron runs from hermes
    try:
        r = subprocess.run(
            ["/opt/hermes/.venv/bin/hermes", "cron", "history"],
            capture_output=True, text=True, timeout=15
        )
        # Parse error lines
        for line in r.stdout.splitlines():
            if "error" in line.lower() and "RuntimeError" in line:
                # Extract job + error
                errors.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "job": "unknown",
                    "raw": line[:300],
                    "source": "cron-history",
                })
    except:
        pass
    
    return errors


def compact_and_store():
    """Compact errors and store to errors.json."""
    raw_errors = get_recent_errors()
    
    # Group by job
    by_job = {}
    for err in raw_errors:
        job = err.get("job", "unknown")
        if job not in by_job:
            by_job[job] = []
        by_job[job].append(err)
    
    # Compact per job
    compacted = []
    for job, errs in by_job.items():
        # Classify the most recent error
        most_recent = max(errs, key=lambda e: e.get("ts", ""))
        classified = classify_error(most_recent.get("raw", ""))
        
        compacted.append({
            "job": job,
            "error_count": len(errs),
            "first_seen": min(e.get("ts", "") for e in errs),
            "last_seen": max(e.get("ts", "") for e in errs),
            "type": classified["type"],
            "code": classified["code"],
            "retry_after_seconds": classified["retry_after_seconds"],
            "suggestion": classified["suggestion"],
            "sample_raw": most_recent.get("raw", "")[:200],
        })
    
    # Stats
    types_count = Counter(c["type"] for c in compacted)
    
    output = {
        "version": "1.0.0",
        "schema": "errors-v1",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_errors": len(raw_errors),
        "unique_jobs_affected": len(by_job),
        "errors_by_type": dict(types_count),
        "errors": compacted,
    }
    
    # Atomic write
    tmp = ERRORS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(output, indent=2, default=str))
    tmp.replace(ERRORS_FILE)
    
    return output


def main():
    result = compact_and_store()
    
    print(f"✓ Compacted {result['total_errors']} errors")
    print(f"  Unique jobs affected: {result['unique_jobs_affected']}")
    print(f"  By type: {result['errors_by_type']}")
    print(f"  Saved to {ERRORS_FILE}")
    
    # Print top suggestions
    if result["errors"]:
        print("\nTop suggestions:")
        seen = set()
        for e in result["errors"][:5]:
            if e["suggestion"] not in seen:
                print(f"  [{e['type']}] {e['job']}: {e['suggestion']}")
                seen.add(e["suggestion"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

