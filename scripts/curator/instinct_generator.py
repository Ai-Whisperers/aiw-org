"""Instinct generator — Phase 4.3 of AIW upgrade plan.

Implements the first phase of ADR-0002 (instinct integration plan).
Pattern source: affaan-m/ECC homunculus/instincts/*.yaml

What it does:
  - Scans state/agent-traces.jsonl for patterns
  - Identifies repeated behaviors, common decision points, recurring failures
  - Generates instinct YAML files in /opt/data/agents/state/instincts/
  - Each instinct has: id, trigger, confidence, domain, source_repo, action, evidence

Usage:
  python3 -m scripts.curator.instinct_generator [--dry-run] [--min-count 5]
"""
import argparse
import json
import re
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_TRACES = Path("/opt/data/state/agent-traces.jsonl")
DEFAULT_OUT = Path("/opt/data/agents/state/instincts")
INSTINCT_VERSION = 1
MIN_EVIDENCE_COUNT = 5  # Need at least 5 occurrences to surface an instinct
LOW_CONFIDENCE = 0.5
MEDIUM_CONFIDENCE = 0.75
HIGH_CONFIDENCE = 0.9


def _read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _confidence_from_count(count: int, min_count: int = MIN_EVIDENCE_COUNT) -> float:
    """Map count to confidence score (0-1)."""
    if count < min_count:
        return 0.0
    if count < 2 * min_count:
        return LOW_CONFIDENCE
    if count < 5 * min_count:
        return MEDIUM_CONFIDENCE
    return HIGH_CONFIDENCE


def _yaml_escape(s: str) -> str:
    """Escape a string for inclusion in a YAML value."""
    if s is None:
        return ""
    s = str(s)
    # If contains special chars or newlines, use double-quoted with escaping
    if any(c in s for c in [":", "#", "\n", '"', "'"]) or s.strip() != s:
        escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    return s


def _make_instinct(id: str, trigger: str, confidence: float, domain: str,
                   evidence_count: int, action: str,
                   evidence_examples: list | None = None) -> dict:
    """Build an instinct dict. Single source of truth for instinct schema."""
    inst = {
        "id": id,
        "trigger": trigger,
        "confidence": confidence,
        "domain": domain,
        "source_repo": "aiw-org",
        "source_evidence_count": evidence_count,
        "action": action,
        "generated_at": _now_iso(),
    }
    if evidence_examples:
        inst["evidence_examples"] = evidence_examples
    return inst


def detect_instincts(traces: list, min_count: int = MIN_EVIDENCE_COUNT) -> list:
    """Detect instincts from trace data. Returns list of dicts."""
    if not traces:
        return []

    instincts = []

    # Pattern 1: Most active agents (frequency instinct)
    agent_counts = Counter(t.get("agent", "unknown") for t in traces)
    for agent, count in agent_counts.most_common(5):
        if count < min_count:
            continue
        evidence = [t.get("trace_id") or t.get("id", "unknown")
                    for t in traces if t.get("agent") == agent][:3]
        instincts.append(_make_instinct(
            id=f"agent-frequency-{agent}",
            trigger=f"When an agent is needed for {agent}-related work",
            confidence=_confidence_from_count(count, min_count),
            domain="agent-selection",
            evidence_count=count,
            action=f"Consider {agent} (active {count} times in recent traces)",
            evidence_examples=evidence,
        ))

    # Pattern 2: Common routing_tags (workflow instinct)
    tag_counts = Counter()
    for t in traces:
        for tag in t.get("routing_tags", []):
            tag_counts[tag] += 1
    for tag, count in tag_counts.most_common(5):
        if count < min_count:
            continue
        instincts.append(_make_instinct(
            id=f"workflow-tag-{tag}",
            trigger=f"When a signal has routing_tag={tag}",
            confidence=_confidence_from_count(count, min_count),
            domain="routing",
            evidence_count=count,
            action=f"Tag '{tag}' appears in {count} traces — likely important workflow signal",
        ))

    # Pattern 3: Failure patterns (errors in traces)
    error_keywords = ["error", "fail", "exception", "timeout", "degraded"]
    error_count = sum(
        1 for t in traces
        if any(kw in (t.get("status", "") + str(t.get("error", ""))).lower()
              for kw in error_keywords)
    )
    if error_count >= min_count:
        instincts.append(_make_instinct(
            id="error-rate-watch",
            trigger="When traces show elevated error rate",
            confidence=_confidence_from_count(error_count, min_count),
            domain="reliability",
            evidence_count=error_count,
            action=f"Investigate {error_count} error traces; check pattern before adding features",
        ))

    # Pattern 4: Signal sources (entry points)
    source_counts = Counter(t.get("source", "unknown") for t in traces)
    for source, count in source_counts.most_common(3):
        if count < min_count:
            continue
        instincts.append(_make_instinct(
            id=f"source-frequency-{source}",
            trigger=f"When tracing requires {source} as the source",
            confidence=_confidence_from_count(count, min_count),
            domain="observability",
            evidence_count=count,
            action=f"Source '{source}' is high-volume ({count} traces); ensure it has proper observability hooks",
        ))

    return instincts


def instincts_to_yaml(instincts: list) -> str:
    """Format a list of instinct dicts as a single YAML document."""
    lines = [f"# Auto-generated instincts (version: {INSTINCT_VERSION})",
             f"# Generated at: {_now_iso()}",
             f"# Source: state/agent-traces.jsonl",
             f"# Count: {len(instincts)}",
             ""]
    for inst in instincts:
        lines.append(f"- id: {_yaml_escape(inst['id'])}")
        lines.append(f"  trigger: {_yaml_escape(inst['trigger'])}")
        lines.append(f"  confidence: {inst['confidence']}")
        lines.append(f"  domain: {_yaml_escape(inst['domain'])}")
        lines.append(f"  source_repo: {_yaml_escape(inst['source_repo'])}")
        lines.append(f"  source_evidence_count: {inst['source_evidence_count']}")
        lines.append(f"  action: {_yaml_escape(inst['action'])}")
        if "evidence_examples" in inst:
            lines.append(f"  evidence_examples:")
            for ex in inst["evidence_examples"]:
                lines.append(f"    - {_yaml_escape(ex)}")
        lines.append(f"  generated_at: {_yaml_escape(inst['generated_at'])}")
        lines.append("")
    return "\n".join(lines)


def generate(traces_path: Path = DEFAULT_TRACES,
              out_path: Path = DEFAULT_OUT,
              min_count: int = MIN_EVIDENCE_COUNT,
              dry_run: bool = False) -> dict:
    """Generate instinct YAML file from trace data. Returns a report."""
    traces = _read_jsonl(traces_path)
    if not traces:
        return {
            "generated": 0,
            "traces_processed": 0,
            "message": "No traces found",
            "dry_run": dry_run,
        }

    instincts = detect_instincts(traces, min_count)
    yaml_text = instincts_to_yaml(instincts)

    if not dry_run and instincts:
        out_path.mkdir(parents=True, exist_ok=True)
        ts_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_file = out_path / f"instincts-{ts_str}.yaml"
        out_file.write_text(yaml_text)
        # Also write a 'latest' symlink for consumers
        latest = out_path / "instincts-latest.yaml"
        if latest.exists() or latest.is_symlink():
            latest.unlink()
        latest.write_text(yaml_text)  # copy, not symlink, for portability

    return {
        "generated": len(instincts),
        "traces_processed": len(traces),
        "out_file": str(out_path / f"instincts-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.yaml") if not dry_run and instincts else None,
        "latest_file": str(out_path / "instincts-latest.yaml") if not dry_run and instincts else None,
        "min_count_threshold": min_count,
        "dry_run": dry_run,
        "instincts_summary": [
            {"id": i["id"], "domain": i["domain"], "confidence": i["confidence"]}
            for i in instincts
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Instinct generator from agent traces")
    parser.add_argument("--traces", type=Path, default=DEFAULT_TRACES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--min-count", type=int, default=MIN_EVIDENCE_COUNT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = generate(args.traces, args.out, args.min_count, args.dry_run)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
