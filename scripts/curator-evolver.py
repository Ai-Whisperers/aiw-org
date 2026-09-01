#!/usr/bin/env python3
"""curator-evolver.py — Harvest instincts + propose PROMPT.md improvements.

Phase 9 R3 / Tier C5 (ADR-0002 implementation).

Reads:
  - state/instincts/*.yaml (from instinct_generator)
  - state/agent-traces.jsonl (raw traces)
  - state/eval-per-agent.json (current quality)

Writes:
  - state/curation-proposals/{ISO-week}.json (proposed changes)
  - outbox/signals/curation-proposal-{id}.md (operator review)

Behavior:
  - For each high-confidence instinct (>= 0.75):
    1. Identify target agent
    2. Draft a PROMPT.md patch proposal
    3. Write to curation-proposals/
"""
import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/opt/data/agents")
INSTINCTS_DIR = REPO / "state" / "instincts"
PROPOSALS_DIR = Path("/opt/data/state/curation-proposals")
EVAL_PATH = Path("/opt/data/state/eval-per-agent.json")
OUTBOX = REPO / "outbox" / "signals"


def iso_week():
    return datetime.now(timezone.utc).strftime("%G-W%V")


def load_instincts() -> list:
    """Load all instinct YAML files."""
    import yaml
    if not INSTINCTS_DIR.exists():
        return []
    instincts = []
    for f in INSTINCTS_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text())
            # Instinct files may be a list of instincts OR a dict
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("instincts", [])
            else:
                continue
            for inst in items:
                if inst.get("confidence", 0) >= 0.75:
                    instincts.append({"file": f.name, **inst})
        except Exception as e:
            print(f"[curator] Failed to load {f}: {e}")
    return instincts


def propose_for_instinct(inst: dict, week: str) -> dict:
    """Draft a curation proposal for an instinct."""
    proposal = {
        "id": uuid.uuid4().hex[:12],
        "instinct_id": inst.get("id"),
        "agent_target": inst.get("agent_target", "unknown"),
        "action": inst.get("action", "review"),
        "evidence": inst.get("evidence", []),
        "confidence": inst.get("confidence", 0),
        "proposed_at": datetime.now(timezone.utc).isoformat(),
        "iso_week": week,
        "status": "pending",
        "patch": inst.get("patch", ""),  # raw patch suggestion
    }
    return proposal


def write_proposals(proposals: list) -> Path:
    """Write proposals to curation-proposals/{week}.json."""
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    week = iso_week()
    out = PROPOSALS_DIR / f"{week}.json"
    out.write_text(json.dumps(proposals, indent=2))
    return out


def notify_operator(proposals: list) -> int:
    """Write a notification signal to operator queue."""
    OUTBOX.mkdir(parents=True, exist_ok=True)
    sig_path = OUTBOX / f"curation-proposal-{iso_week()}.md"
    content = f"# Curator-Evolver Proposals — {iso_week()}\n\n"
    content += f"> {len(proposals)} instincts >= 0.75 confidence proposed\n\n"
    for p in proposals:
        content += f"## {p['instinct_id']}\n"
        content += f"- Confidence: {p['confidence']}\n"
        content += f"- Target: {p['agent_target']}\n"
        content += f"- Action: {p['action']}\n"
        content += f"- Evidence count: {len(p.get('evidence', []))}\n\n"
    content += "\n**Review:** /opt/data/state/curation-proposals/" + iso_week() + ".json\n"
    content += "**Apply:** move to state/curation-approved/{week}.json after approval\n"
    sig_path.write_text(content)
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    instincts = load_instincts()
    week = iso_week()
    proposals = [propose_for_instinct(i, week) for i in instincts]

    print(f"[curator] Loaded {len(instincts)} high-confidence instincts ({len(instincts)}/total)")
    print(f"[curator] Drafted {len(proposals)} proposals")

    if args.dry_run:
        for p in proposals[:3]:
            print(f"  - {p['instinct_id']} → {p['agent_target']} (conf={p['confidence']})")
        return 0

    out = write_proposals(proposals)
    print(f"[curator] Wrote {out}")
    notify_operator(proposals)
    return 0


if __name__ == "__main__":
    sys.exit(main())