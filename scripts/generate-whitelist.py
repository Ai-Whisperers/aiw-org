#!/usr/bin/env python3
"""Generate default-allow whitelists for agents (Tier H3).

Built as Phase 31 R4.

Reads each PROMPT.md and infers which actions the agent SHOULD be allowed
to do (the inverse of hard_stops). Default-allow whitelists are stricter
than blacklists — they block by default instead of allowing by default.

Does NOT auto-apply. Writes drafts to state/dept-whitelists-defaults.jsonl
for Kiki to review.

Categories (mirrored from generate-default-hard-stops.py):
  - sales-*       : sales-actions + read/write_state
  - eng-*         : dev + write_state (deploy/git_push explicit)
  - finance-*     : financial read + write only
  - research-*    : publish + update + read/write_state
  - operations-*  : ops read/write
  - people-*      : people read/write
  - board-*       : minimal (read only)

Usage:
    python3 scripts/generate-whitelist.py --dry-run    # preview
    python3 scripts/generate-whitelist.py --output     # write drafts
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/opt/data/agents")
OUTPUT = Path("/opt/data/state/dept-whitelists-defaults.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# Default-allow whitelists per category
CATEGORY_WHITELISTS = {
    "sales": [
        "send_outreach",
        "send_proposal",
        "update_deal_stage",
        "comment_on_issue",
        "send_external_message",
        "close_issue",
        "read_state",
        "write_state",
    ],
    "eng": [
        "merge_pr",
        "comment_on_pr",
        "block_merge",
        "block_output",
        "restart_service",
        "close_issue",
        "comment_on_issue",
        "read_state",
        "write_state",
        # deploy_prod, force_push, rollback EXCLUDED
    ],
    "finance": [
        "send_invoice",
        "read_state",
        "write_state",
    ],
    "research": [
        "update_thesis_metadata",
        "publish_post",
        "read_state",
        "write_state",
    ],
    "operations": [
        "comment_on_issue",
        "block_merge",
        "block_output",
        "restart_service",
        "block_ip",
        "read_state",
        "write_state",
    ],
    "people": [
        "comment_on_issue",
        "send_external_message",
        "read_state",
        "write_state",
    ],
    "board": [
        "read_state",
    ],
}


def detect_category(agent_path: str) -> str:
    """Mirror of generate-default-hard-stops.py category detection."""
    parts = agent_path.split("/")
    if not parts:
        return "operations"
    first = parts[0]
    if first.startswith("01-operations") or first == "devops-monitor-30min":
        return "operations"
    if first.startswith("02-finance") or first == "tax-receipt-tracker":
        return "finance"
    if first.startswith("03-sales"):
        return "sales"
    if first.startswith("04-engineering") or first.startswith("devops") or first.startswith("ai-safety"):
        return "eng"
    if first.startswith("05-research") or first.startswith("thesis") or first.startswith("course"):
        return "research"
    if first.startswith("06-people") or first.startswith("people"):
        return "people"
    if first.startswith("board") or first.startswith("demiurge"):
        return "board"
    if "apollo" in agent_path or "cadmus" in agent_path or "metis" in agent_path or "hermes-router" in agent_path:
        return "sales"
    if "athena" in agent_path or "hera" in agent_path or "calliope" in agent_path or "orpheus" in agent_path:
        return "research"
    if "kronos" in agent_path or "ai-ops" in agent_path or "compliance" in agent_path:
        return "operations"
    if "hephaestus" in agent_path or "argus" in agent_path:
        return "eng"
    if "themis" in agent_path or "clio" in agent_path or "peitho" in agent_path or "thoth" in agent_path:
        return "research"
    return "operations"


def generate_drafts() -> list[dict]:
    """Generate whitelist drafts for all agents."""
    out = []
    for p in ROOT.rglob("PROMPT.md"):
        if ".venv" in str(p) or "node_modules" in str(p):
            continue
        rel = str(p.relative_to(ROOT))
        if "README" in rel or "template" in rel.lower():
            continue
        try:
            content = p.read_text()
        except Exception:
            continue
        agent_name = p.name
        category = detect_category(rel)
        allowed = CATEGORY_WHITELISTS.get(category, CATEGORY_WHITELISTS["operations"])
        # Extract mentioned actions from PROMPT (heuristic)
        action_mentions = set(re.findall(r'\b[a-z]+_[a-z_]+\b', content.lower()))
        # Filter to known actions only
        from sys import path as syspath
        syspath.insert(0, str(ROOT / 'patterns'))
        try:
            import hard_stop_wrapper
            known_actions = set(hard_stop_wrapper.STANDARD_ACTIONS)
        except Exception:
            known_actions = set()
        mentioned_actions = action_mentions & known_actions
        out.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_path": rel,
            "agent_name": agent_name,
            "category": category,
            "default_allow": allowed,
            "mentioned_actions": sorted(mentioned_actions),
            "review_required": True,
        })
    return out


def main():
    parser = argparse.ArgumentParser(description="Generate default-allow whitelists")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", action="store_true")
    args = parser.parse_args()

    drafts = generate_drafts()
    print(f"=== Generate Default-Allow Whitelists ===")
    print(f"Agents: {len(drafts)}\n")

    from collections import Counter
    cats = Counter(d["category"] for d in drafts)
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
    print()

    if args.dry_run:
        # Show one example per category
        for cat in sorted(cats):
            ex = next(d for d in drafts if d["category"] == cat)
            print(f"--- {cat}: {ex['agent_path']} ---")
            print(f"  default_allow: {ex['default_allow']}")
            print(f"  mentioned: {ex['mentioned_actions'][:5]}...")
            print()
        return

    if args.output:
        with OUTPUT.open("w") as f:
            for d in drafts:
                f.write(json.dumps(d, separators=(",", ":")) + "\n")
        print(f"Wrote {len(drafts)} drafts to {OUTPUT}")


if __name__ == "__main__":
    main()
