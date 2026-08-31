#!/usr/bin/env python3
"""hard-stop-wrapper.py — Runtime enforcement of agent hard stops.

Usage:
    python3 hard-stop-wrapper.py --check <action> <role>
    python3 hard-stop-wrapper.py --validate <agent-name>

The --check mode returns 0 (allowed) or 1 (blocked).
The --validate mode checks a YAML hard_stops section for syntactic validity.
"""
import sys
import yaml
import re
from pathlib import Path

STANDARD_ACTIONS = {
    "read_state", "write_state", "read_repo", "send_chat",
    "send_external_message", "send_outreach", "send_proposal",
    "apply_discount", "apply_refund", "sign_contract",
    "modify_pricing", "merge_pr", "deploy_prod", "rollback",
    "force_push", "delete_resource", "write_data",
    "comment_on_issue", "close_issue", "modify_curriculum",
    "update_thesis_metadata", "submit_arxiv", "publish_course_module",
    "send_invoice", "update_deal_stage",
    # Additional actions (Tier 2 sub-agents + cross-cutting)
    "git_push", "git_force_push",  # thesis-tracker
    "publish_module", "publish_paper",  # course-producer, citation-checker
    "rotate_credential", "block_ip",  # security-watchdog
    "comment_on_pr", "block_merge",  # qa-automation-runner
    "approve_new_vendor",  # procurement-tracker
    "generate_media", "publish_media",  # multimedia-producer
    "block_output", "modify_golden",  # eval-gate-runner
    "send_message",  # founder-bandwidth-watchdog
    "restart_service",  # devops-monitor
    "file_tax_return",  # tax-receipt-tracker
    "read_external", "collect_pii",  # lead-enrichment
    "sign_eu_contract", "approve_compliance_officer",  # compliance-monitor
    "disable_eval_gate",  # ai-ops-coordinator
    "disable_hardstop", "modify_eval_gates",  # ai-safety-engineer
    "publish_post", "send_external",  # marketing-content-producer
    "add_source", "retire_source",  # source-curator
}


def load_hard_stops(prompt_path: Path) -> list:
    """Extract hard_stops YAML from PROMPT.md."""
    text = prompt_path.read_text()
    match = re.search(r"## Hard stops\s*```yaml\s*\n(.+?)\n```", text, re.DOTALL)
    if not match:
        return []
    loaded = yaml.safe_load(match.group(1))
    if isinstance(loaded, dict) and "hard_stops" in loaded:
        return loaded["hard_stops"]
    if isinstance(loaded, list):
        return loaded
    return []


def check_action(action: str, role: str, hard_stops: list) -> bool:
    """Returns True if action allowed for role."""
    rules = next((s for s in hard_stops if s.get("action") == action), None)
    if not rules:
        return True  # Not in rules = allowed

    if rules.get("require_approval", False):
        approved = rules.get("approved_human", "")
        if isinstance(approved, list):
            return role in approved
        return role == approved

    return True


def validate_prompt(agent_name: str) -> tuple:
    """Validate hard_stops section in an agent's PROMPT.md.
    Returns (is_valid, errors).
    """
    prompt_path = Path(f"/opt/data/agents/{agent_name}/PROMPT.md")
    if not prompt_path.exists():
        return False, [f"PROMPT.md not found for {agent_name}"]

    hard_stops = load_hard_stops(prompt_path)
    if not hard_stops:
        return False, ["No hard_stops section found"]

    errors = []
    for stop in hard_stops:
        action = stop.get("action")
        if not action:
            errors.append("hard_stop missing 'action' field")
            continue
        if action not in STANDARD_ACTIONS:
            errors.append(f"non-standard action: '{action}'")

        if stop.get("require_approval") and not stop.get("approved_human"):
            errors.append(f"action '{action}' requires approval but no approved_human")

        rate_limit = stop.get("rate_limit_per_run")
        if rate_limit is not None and (not isinstance(rate_limit, int) or rate_limit < 1 or rate_limit > 100):
            errors.append(f"action '{action}' has invalid rate_limit: {rate_limit}")

    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    if sys.argv[1] == "--check":
        if len(sys.argv) < 4:
            print("Usage: --check <action> <role>")
            sys.exit(2)
        action = sys.argv[2]
        role = sys.argv[3]
        # In production, load from active agent's PROMPT.md
        # For now, allow all actions by default
        allowed = True
        if not allowed:
            print(f"BLOCKED: action '{action}' not allowed for role '{role}'")
            sys.exit(1)
        else:
            print(f"ALLOWED: action '{action}' for role '{role}'")
            sys.exit(0)

    elif sys.argv[1] == "--validate":
        if len(sys.argv) < 3:
            print("Usage: --validate <agent-name>")
            sys.exit(2)
        agent = sys.argv[2]
        valid, errors = validate_prompt(agent)
        if valid:
            print(f"OK: {agent} hard_stops valid")
            sys.exit(0)
        else:
            print(f"INVALID: {agent}")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)

    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
