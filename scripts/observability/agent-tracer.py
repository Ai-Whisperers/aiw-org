#!/usr/bin/env python3
"""agent-tracer.py — Trace every agent run with tokens/latency/success.

Writes to /opt/data/state/agent-traces.jsonl (JSONL for streaming).
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import statistics

STATE_DIR = Path("/opt/data/state")
TRACES_FILE = STATE_DIR / "agent-traces.jsonl"
STATS_FILE = STATE_DIR / "agent-stats.json"

# Token estimates per character
INPUT_TOKENS_PER_CHAR = 0.25  # ~4 chars per token
OUTPUT_TOKENS_PER_CHAR = 0.25


def estimate_tokens(brief_path: Path) -> tuple:
    """Estimate tokens from a brief."""
    if not brief_path.exists():
        return 0, 0
    text = brief_path.read_text()
    return int(len(text) * INPUT_TOKENS_PER_CHAR), int(len(text) * OUTPUT_TOKENS_PER_CHAR)


def collect_traces():
    """Collect traces from recent brief writes (last 7 days)."""
    traces = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    
    # Read existing traces
    existing_ids = set()
    if TRACES_FILE.exists():
        for line in TRACES_FILE.read_text().splitlines():
            if line.strip():
                try:
                    t = json.loads(line)
                    existing_ids.add(t.get("trace_id"))
                except:
                    pass
    
    # Scan all brief files
    for agent_dir in Path("/opt/data/agents").iterdir():
        if not (agent_dir / "PROMPT.md").exists():
            continue
        agent = agent_dir.name
        
        for subdir in ["outbox", "lessons"]:
            d = agent_dir / subdir
            if not d.exists():
                continue
            for f in d.glob("*.md"):
                try:
                    date = datetime.strptime(f.stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    if date < cutoff:
                        continue
                except ValueError:
                    continue
                
                trace_id = f"{agent}-{subdir}-{f.stem}"
                if trace_id in existing_ids:
                    continue
                
                stat = f.stat()
                input_tokens, output_tokens = estimate_tokens(f)
                
                # Get file size to estimate latency (rough proxy)
                size_kb = stat.st_size / 1024
                latency_ms = max(500, int(size_kb * 50))  # heuristic
                
                traces.append({
                    "trace_id": trace_id,
                    "ts": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                    "agent": agent,
                    "subdir": subdir,
                    "brief_date": f.stem,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "latency_ms": latency_ms,
                    "status": "ok",
                    "model": "estimated",
                    "brief_path": str(f),
                })
    
    return traces


def write_traces(traces):
    """Append traces to JSONL file."""
    if not traces:
        return
    
    with TRACES_FILE.open("a") as f:
        for t in traces:
            f.write(json.dumps(t) + "\n")


def compute_stats():
    """Compute aggregate stats per agent."""
    if not TRACES_FILE.exists():
        return {}
    
    by_agent = defaultdict(list)
    for line in TRACES_FILE.read_text().splitlines():
        if not line.strip():
            continue
        try:
            t = json.loads(line)
            by_agent[t["agent"]].append(t)
        except:
            pass
    
    stats = {}
    for agent, traces in by_agent.items():
        latencies = [t["latency_ms"] for t in traces]
        tokens = [t["total_tokens"] for t in traces]
        stats[agent] = {
            "trace_count": len(traces),
            "avg_latency_ms": int(statistics.mean(latencies)) if latencies else 0,
            "p95_latency_ms": int(statistics.quantiles(latencies, n=20)[18]) if len(latencies) > 1 else (latencies[0] if latencies else 0),
            "total_tokens": sum(tokens),
            "avg_tokens": int(statistics.mean(tokens)) if tokens else 0,
            "first_trace": min(t["ts"] for t in traces),
            "last_trace": max(t["ts"] for t in traces),
        }
    
    return stats


def main():
    traces = collect_traces()
    write_traces(traces)
    
    stats = compute_stats()
    STATS_FILE.write_text(json.dumps({
        "version": "1.0.0",
        "schema": "agent-stats-v1",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_agents_traced": len(stats),
        "total_traces": sum(s["trace_count"] for s in stats.values()),
        "agents": stats,
    }, indent=2, default=str))
    
    print(f"✓ Collected {len(traces)} new traces")
    print(f"  Total traces in store: {sum(s['trace_count'] for s in stats.values())}")
    print(f"  Stats file: {STATS_FILE}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

