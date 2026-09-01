#!/usr/bin/env python3
"""hard-stop-wrapper.py — Runtime enforcement of agent hard stops.

Usage:
    python3 hard-stop-wrapper.py --check <action> <role> [--agent AGENT] [--log]
    python3 hard-stop-wrapper.py --validate <agent-name>

The --check mode returns 0 (allowed) or 1 (blocked).
The --validate mode checks a YAML hard_stops section for syntactic validity.

Importable as a module:
    from patterns.hard_stop_wrapper import check_action, load_hard_stops

This module is what agents should `import` and call, not the CLI.
"""
import json
import sys
import yaml
import re
from datetime import datetime, timezone
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
    """Extract hard_stops YAML from PROMPT.md.

    Supports multiple formats (in order of preference):
    1. YAML frontmatter (between --- markers at top of file)
    2. A second --- block (legacy format used by some PROMPTs)
    3. A bare `hard_stops:` YAML block anywhere in the file
    4. Markdown section: `## Hard stops` + ```yaml code fence
    """
    text = prompt_path.read_text()

    # Format 1+2: YAML frontmatter (try both --- blocks)
    for fm_match in re.finditer(r"^---\s*\n(.+?)\n---", text, re.DOTALL | re.MULTILINE):
        loaded = yaml.safe_load(fm_match.group(1))
        if isinstance(loaded, dict) and "hard_stops" in loaded:
            stops = loaded["hard_stops"]
            return stops if isinstance(stops, list) else []

    # Format 3: bare hard_stops block anywhere
    bare_match = re.search(r"^hard_stops:\s*\n((?:  [^#\n].*\n?)+)", text, re.MULTILINE)
    if bare_match:
        try:
            loaded = yaml.safe_load(bare_match.group(0))
            if isinstance(loaded, dict) and "hard_stops" in loaded:
                stops = loaded["hard_stops"]
                return stops if isinstance(stops, list) else []
        except yaml.YAMLError:
            pass

    # Format 4: markdown section with code fence
    section_match = re.search(r"## Hard stops\s*```yaml\s*\n(.+?)\n```", text, re.DOTALL)
    if section_match:
        loaded = yaml.safe_load(section_match.group(1))
        if isinstance(loaded, dict) and "hard_stops" in loaded:
            return loaded["hard_stops"]
        if isinstance(loaded, list):
            return loaded

    return []


def check_action(action: str, role: str, hard_stops: list) -> bool:
    """Returns True if action allowed for role.

    Supports TWO modes (Phase 33 R1):
    - blacklist (hard_stops): block specific actions (default)
    - whitelist (default_allow): only allow listed actions, block everything else

    Detection: if hard_stops contains an entry with action='*' OR a
    'mode: whitelist' marker, the list is treated as whitelist.

    IMPORTANT (Phase 34 R4): In whitelist mode, ALL `action:` entries are
    treated as allowed actions regardless of `require_approval` field.
    Do NOT mix whitelist + blacklist entries — if you want allowlist + approval
    for some actions, omit the `mode: whitelist` marker and use blacklist only.

    PHASE 35 R3 (per-action approval in whitelist mode):
    Use `approval_required: true` (distinct from `require_approval`) to mark
    specific whitelisted actions as needing human approval. This works
    orthogonally with the whitelist: action is allowed by the list, but
    still requires the named human (or kiki) to approve at runtime.

    Example:
        hard_stops:
          - mode: whitelist
          - action: read_state
          - action: deploy_prod
            approval_required: true
            approved_human: ivan

    With role=ai-agent: read_state→allowed, deploy_prod→blocked (needs ivan).
    With role=ivan: both allowed.
    """
    # Detect whitelist mode: any entry with action='*' OR 'mode: whitelist' marker
    is_whitelist = any(
        s.get("action") == "*" or s.get("mode") == "whitelist"
        for s in hard_stops
    )

    if is_whitelist:
        # Whitelist mode: only listed actions are allowed (default-deny)
        for s in hard_stops:
            if s.get("action") == "*":
                # Wildcard = allow all (overrides whitelist)
                return True
        # Find specific entry for this action
        entry = next(
            (s for s in hard_stops if s.get("action") == action),
            None
        )
        if entry is None:
            # Action not in whitelist
            return False
        # PHASE 35 R3: per-action approval check
        if entry.get("approval_required", False):
            approved = entry.get("approved_human", "")
            if isinstance(approved, list):
                return role in approved
            if "+" in approved:
                return role in approved.split("+")
            return role == approved
        return True

    # Blacklist mode (default)
    rules = next((s for s in hard_stops if s.get("action") == action), None)
    if not rules:
        return True  # Not in rules = allowed

    if rules.get("require_approval", False):
        approved = rules.get("approved_human", "")
        # Support: "ivan", "ivan+kiki" (any-of), or [list]
        if isinstance(approved, list):
            return role in approved
        if "+" in approved:
            # Any-of: role must match any of the joined names
            return role in approved.split("+")
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


LOG_PATH = Path("/opt/data/state/hard-stop-audit.ndjson")


def _log_check(agent_name: str, action: str, role: str, allowed: bool) -> None:
    """Append a check event to the audit log (NDJSON format).

    Phase 28 fix: switched from read-append-write (race condition) to
    append-only NDJSON. Each line is a complete JSON event. Concurrent
    appends are atomic on POSIX (kernel guarantees writes <PIPE_BUF are atomic).

    NDJSON format (one JSON object per line):
      {"ts": "<ISO>", "agent": "<name>", "action": "<action>", "role": "<role>", "allowed": <bool>}

    Rotation: when file exceeds 50MB, archive current + start fresh.
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name,
        "action": action,
        "role": role,
        "allowed": allowed,
    }
    # Use NDJSON (one event per line) for atomic append
    line = json.dumps(entry, separators=(",", ":")) + "\n"
    # Check size before append
    if LOG_PATH.exists() and LOG_PATH.stat().st_size > 50 * 1024 * 1024:
        # Rotate: archive current, start fresh
        archive = LOG_PATH.with_suffix(f".audit-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.ndjson")
        LOG_PATH.rename(archive)
    with LOG_PATH.open("a") as f:
        f.write(line)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    if sys.argv[1] == "--check":
        if len(sys.argv) < 4:
            print("Usage: --check <action> <role> [--agent AGENT] [--log]")
            sys.exit(2)
        action = sys.argv[2]
        role = sys.argv[3]

        # Parse optional flags
        agent_name = None
        do_log = False
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--agent" and i + 1 < len(sys.argv):
                agent_name = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--log":
                do_log = True
                i += 1
            else:
                i += 1

        # Load hard_stops from agent's PROMPT.md (or default if --agent not given)
        hard_stops = []
        if agent_name:
            prompt_path = Path(f"/opt/data/agents/{agent_name}/PROMPT.md")
            if prompt_path.exists():
                hard_stops = load_hard_stops(prompt_path)
            else:
                print(f"WARN: PROMPT.md not found for {agent_name}; treating as no hard_stops", file=sys.stderr)

        allowed = check_action(action, role, hard_stops)

        # Optional audit log
        if do_log:
            _log_check(agent_name or "<anonymous>", action, role, allowed)

        if not allowed:
            print(f"BLOCKED: action '{action}' not allowed for role '{role}' (agent: {agent_name or '<anonymous>'})")
            sys.exit(1)
        else:
            print(f"ALLOWED: action '{action}' for role '{role}' (agent: {agent_name or '<anonymous>'})")
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
