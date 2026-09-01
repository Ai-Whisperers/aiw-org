#!/usr/bin/env python3
"""Generate default hard_stops for unprotected PROMPTs.

Built as Phase 31 R2 (Tier G3).

Reads each PROMPT.md without hard_stops declarations and generates
a default block. The default is based on agent category + action verb
patterns in the PROMPT text.

Does NOT auto-apply — writes drafts to state/dept-hard-stops-defaults.jsonl
for Kiki to review. Apply manually with --apply flag.

Categories (auto-detected from path):
  - sales-*       : outbound + payment actions
  - eng-*         : deploy + git push require approval
  - finance-*     : money actions require approval
  - research-*    : submit/publish actions require approval
  - operations-*  : delete/disable actions require approval
  - people-*      : data access actions require approval
  - board-*       : all require approval (top-level)

Usage:
    python3 scripts/generate-default-hard-stops.py --dry-run    # preview
    python3 scripts/generate-default-hard-stops.py --output     # write drafts (default)
    python3 scripts/generate-default-hard-stops.py --agent 04-engineering/devops-monitor  # one
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/opt/data/agents")
OUTPUT = Path("/opt/data/state/dept-hard-stops-defaults.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# Default rules per category. Each is `action -> require_approval (bool) + approved_human (str)`.
CATEGORY_DEFAULTS = {
    "sales": [
        {"action": "send_outreach", "require_approval": False, "approved_human": ""},
        {"action": "send_proposal", "require_approval": False, "approved_human": ""},
        {"action": "apply_discount", "require_approval": True, "approved_human": "ivan"},
        {"action": "apply_refund", "require_approval": True, "approved_human": "ivan"},
        {"action": "sign_contract", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "modify_pricing", "require_approval": True, "approved_human": "ivan"},
        {"action": "send_external_message", "require_approval": False, "approved_human": ""},
        {"action": "send_invoice", "require_approval": True, "approved_human": "ivan"},
        {"action": "update_deal_stage", "require_approval": False, "approved_human": ""},
        {"action": "close_issue", "require_approval": False, "approved_human": ""},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
    ],
    "eng": [
        {"action": "deploy_prod", "require_approval": True, "approved_human": "ivan"},
        {"action": "rollback", "require_approval": True, "approved_human": "ivan"},
        {"action": "force_push", "require_approval": True, "approved_human": "ivan"},
        {"action": "git_force_push", "require_approval": True, "approved_human": "ivan"},
        {"action": "merge_pr", "require_approval": False, "approved_human": ""},
        {"action": "delete_resource", "require_approval": True, "approved_human": "ivan"},
        {"action": "close_issue", "require_approval": False, "approved_human": ""},
        {"action": "comment_on_pr", "require_approval": False, "approved_human": ""},
        {"action": "block_merge", "require_approval": False, "approved_human": ""},
        {"action": "block_output", "require_approval": False, "approved_human": ""},
        {"action": "modify_eval_gates", "require_approval": True, "approved_human": "ivan"},
        {"action": "disable_hardstop", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "disable_eval_gate", "require_approval": True, "approved_human": "ivan"},
        {"action": "restart_service", "require_approval": True, "approved_human": "ivan"},
        {"action": "rotate_credential", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "block_ip", "require_approval": True, "approved_human": "ivan"},
        {"action": "approve_compliance_officer", "require_approval": True, "approved_human": "ivan"},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
    ],
    "finance": [
        {"action": "file_tax_return", "require_approval": True, "approved_human": "ivan"},
        {"action": "send_invoice", "require_approval": True, "approved_human": "ivan"},
        {"action": "apply_refund", "require_approval": True, "approved_human": "ivan"},
        {"action": "modify_pricing", "require_approval": True, "approved_human": "ivan"},
        {"action": "sign_eu_contract", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
    ],
    "research": [
        {"action": "submit_arxiv", "require_approval": True, "approved_human": "ivan"},
        {"action": "publish_course_module", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "publish_module", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "publish_paper", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "publish_post", "require_approval": True, "approved_human": "ivan"},
        {"action": "update_thesis_metadata", "require_approval": False, "approved_human": ""},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
    ],
    "operations": [
        {"action": "delete_resource", "require_approval": True, "approved_human": "ivan"},
        {"action": "disable_hardstop", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "disable_eval_gate", "require_approval": True, "approved_human": "ivan"},
        {"action": "modify_eval_gates", "require_approval": True, "approved_human": "ivan"},
        {"action": "restart_service", "require_approval": True, "approved_human": "ivan"},
        {"action": "rotate_credential", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "block_ip", "require_approval": True, "approved_human": "ivan"},
        {"action": "modify_curriculum", "require_approval": True, "approved_human": "ivan"},
        {"action": "force_push", "require_approval": True, "approved_human": "ivan"},
        {"action": "git_force_push", "require_approval": True, "approved_human": "ivan"},
        {"action": "publish_post", "require_approval": True, "approved_human": "ivan"},
        {"action": "send_external_message", "require_approval": False, "approved_human": ""},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
    ],
    "people": [
        {"action": "modify_curriculum", "require_approval": True, "approved_human": "ivan+kiki"},
        {"action": "send_external_message", "require_approval": False, "approved_human": ""},
        {"action": "comment_on_issue", "require_approval": False, "approved_human": ""},
        {"action": "read_state", "require_approval": False, "approved_human": ""},
        {"action": "write_state", "require_approval": False, "approved_human": ""},
    ],
    "board": [
        # Board-level: everything requires approval
        {"action": "*", "require_approval": True, "approved_human": "ivan+kiki"},
    ],
}

# Category detection from path
def detect_category(agent_path: str) -> str:
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
    # Check demiurge agent name patterns
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
    return "operations"  # safe default


def generate_drafts(agent_path: str, agent_name: str) -> dict:
    """Generate a hard_stops draft for one agent."""
    category = detect_category(agent_path)
    rules = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["operations"])
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent_path": agent_path,
        "agent_name": agent_name,
        "category": category,
        "hard_stops": rules,
        "draft_yaml": _to_yaml(rules),
        "review_required": True,  # Kiki must approve before apply
    }


def _to_yaml(rules: list) -> str:
    """Render rules as YAML for embedding into PROMPT.md."""
    lines = ["hard_stops:"]
    for r in rules:
        if r.get("action") == "*":
            lines.append(f"  - action: '*'")
            lines.append(f"    require_approval: {str(r['require_approval']).lower()}")
            lines.append(f"    approved_human: '{r['approved_human']}'")
            continue
        lines.append(f"  - action: {r['action']}")
        lines.append(f"    require_approval: {str(r['require_approval']).lower()}")
        if r['require_approval']:
            lines.append(f"    approved_human: '{r['approved_human']}'")
    return "\n".join(lines)


def find_unprotected() -> list[tuple[Path, str]]:
    """Find all PROMPT.md files without hard_stops."""
    out = []
    for p in ROOT.rglob("PROMPT.md"):
        if ".venv" in str(p) or "node_modules" in str(p):
            continue
        try:
            content = p.read_text()
        except Exception:
            continue
        if "hard_stops:" in content and "require_approval" in content:
            continue
        # Skip if it's an instruction/draft file (not an actual PROMPT)
        rel = str(p.relative_to(ROOT))
        if "README" in rel or "template" in rel.lower():
            continue
        out.append((p.parent, rel))
    return out


def main():
    parser = argparse.ArgumentParser(description="Generate default hard_stops drafts")
    parser.add_argument("--dry-run", action="store_true", help="Print summary only, don't write")
    parser.add_argument("--output", action="store_true", help="Write drafts to JSONL (default)")
    parser.add_argument("--agent", help="Only generate for one agent (path or name)")
    parser.add_argument("--apply", action="store_true",
                        help="[DANGEROUS] Apply drafts directly to PROMPT.md files")
    args = parser.parse_args()

    unprotected = find_unprotected()

    # Filter to one agent if requested
    if args.agent:
        unprotected = [(p, r) for p, r in unprotected
                        if args.agent in r or args.agent == p.name]

    if not unprotected:
        print("(no unprotected PROMPTs found)")
        return

    print(f"=== Generate Default hard_stops ===")
    print(f"Unprotected PROMPTs: {len(unprotected)}\n")

    drafts = []
    by_category = {}
    for p, rel in unprotected:
        agent_name = p.name
        draft = generate_drafts(rel, agent_name)
        drafts.append(draft)
        cat = draft["category"]
        by_category.setdefault(cat, []).append(rel)

    print("=== By category ===")
    for cat, paths in sorted(by_category.items()):
        print(f"  {cat}: {len(paths)}")
    print()

    if args.dry_run:
        for d in drafts[:5]:
            print(f"--- {d['agent_path']} ---")
            print(f"  category: {d['category']}")
            print(f"  rules: {len(d['hard_stops'])}")
            print()
        print(f"(showing first 5 of {len(drafts)})")
        return

    if args.output or not args.apply:
        # Write JSONL drafts
        with OUTPUT.open("w") as f:
            for d in drafts:
                f.write(json.dumps(d, separators=(",", ":")) + "\n")
        print(f"Wrote {len(drafts)} drafts to {OUTPUT}")
        print()
        print("Next steps:")
        print(f"  1. Review: cat {OUTPUT}")
        print(f"  2. For each agent, edit PROMPT.md to add the hard_stops block")
        print(f"  3. Or pass --apply to auto-edit (DANGEROUS, Kiki must approve)")

    if args.apply:
        print("\n=== APPLY (modifying PROMPT.md files!) ===")
        applied = 0
        for p, rel in unprotected:
            # p is the parent dir; PROMPT.md is inside
            prompt_file = p / "PROMPT.md"
            if not prompt_file.exists():
                print(f"  SKIP {rel}: PROMPT.md not found in {p}")
                continue
            content = prompt_file.read_text()

            # Skip if already has hard_stops section (idempotency)
            if "## Hard stops" in content:
                print(f"  SKIP {rel}: already has hard_stops")
                continue

            # Find agent draft
            draft = next((d for d in drafts if d["agent_path"] == rel), None)
            if not draft:
                continue

            # Insert hard_stops as a new section AFTER the first H1 or H2 heading
            # (PROMPT.md files here have a title at top, not YAML frontmatter)
            yaml_block = "## Hard stops\n\n```yaml\n" + draft["draft_yaml"] + "\n```\n"

            lines = content.split("\n")
            insert_idx = None
            # Find first H2 (## ...) heading
            for i, line in enumerate(lines):
                if line.startswith("## ") and not line.startswith("## Hard"):
                    insert_idx = i
                    break

            if insert_idx is None:
                # No H2 found — append at end
                new_content = content + "\n\n" + yaml_block
            else:
                # Insert before the first H2
                lines.insert(insert_idx, yaml_block.rstrip())
                lines.insert(insert_idx + 1, "")  # blank line after
                new_content = "\n".join(lines)

            prompt_file.write_text(new_content)
            applied += 1
            print(f"  ✓ {rel}")
        print(f"\nApplied hard_stops to {applied} PROMPTs")
        print("Run: scripts/lint-prompts.py to verify")


if __name__ == "__main__":
    main()
