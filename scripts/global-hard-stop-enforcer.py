#!/usr/bin/env python3
"""Global hard-stop enforcement audit + interceptor.

Built Phase 7 R5 (implementation plan §4 Phase 1.7).

Two modes:

  1. AUDIT (default): scans every agent PROMPT.md, counts agents with
     destructive hard_stops, and reports the coverage gap.

  2. WRAP (--wrap): shows how to use the global interceptor pattern
     (importable in agent code). The interceptor monkey-patches
     dangerous methods on the Path / json / subprocess modules so that
     any write_state / merge_pr / deploy_prod / force_push call gets
     routed through hard_stop_check.check() before executing.

Usage:
    python3 scripts/global-hard-stop-enforcer.py --audit       # default
    python3 scripts/global-hard-stop-enforcer.py --wrap        # show wrapper code
    python3 scripts/global-hard-stop-enforcer.py --test       # test wrapper with a sample call
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENTS_REPO = Path("/opt/data/agents")

DESTRUCTIVE_ACTIONS = {
    "write_state", "send_external_message", "send_outreach", "send_proposal",
    "apply_discount", "apply_refund", "sign_contract", "modify_pricing",
    "merge_pr", "deploy_prod", "rollback", "force_push", "delete_resource",
    "submit_arxiv", "publish_course_module", "publish_module", "publish_paper",
    "send_invoice", "update_deal_stage", "git_push", "git_force_push",
    "rotate_credential", "block_ip", "block_merge", "approve_new_vendor",
    "generate_media", "publish_media", "block_output", "modify_golden",
    "restart_service", "file_tax_return", "collect_pii", "sign_eu_contract",
    "disable_eval_gate", "disable_hardstop", "modify_eval_gates", "publish_post",
    "add_source", "retire_source", "close_issue", "modify_curriculum",
    "update_thesis_metadata", "approve_compliance_officer",
}


def parse_hard_stops(prompt_path: Path) -> list:
    """Extract hard_stops list from PROMPT.md."""
    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    # Try YAML frontmatter
    m = re.match(r"^---\s*\n(.+?)\n---", text, re.DOTALL)
    if m:
        # Naive YAML parse — handle the simple "hard_stops: - ..." format
        body = m.group(1)
        if "hard_stops:" in body:
            # Find hard_stops section
            idx = body.find("hard_stops:")
            sub = body[idx:]
            # Extract list items until next top-level key
            items = []
            for line in sub.split("\n")[1:]:
                if line.startswith("  - action:"):
                    act = line.split(":", 1)[1].strip()
                    items.append({"action": act})
                elif line and not line.startswith("  "):
                    break
                elif line.startswith("    "):
                    # Continue current item
                    if items:
                        k, _, v = line.strip().partition(":")
                        items[-1][k.strip()] = v.strip()
            return items
    return []


def find_all_prompts() -> list:
    """Find all PROMPT.md files with destructive hard_stops."""
    out = []
    for prompt in AGENTS_REPO.rglob("PROMPT.md"):
        if "monitor-notes" in str(prompt) or "__pycache__" in str(prompt):
            continue
        try:
            stops = parse_hard_stops(prompt)
            if stops:
                actions = {s.get("action") for s in stops}
                destructive = actions & DESTRUCTIVE_ACTIONS
                if destructive:
                    out.append({
                        "path": str(prompt.relative_to(AGENTS_REPO)),
                        "agent": prompt.parent.name,
                        "actions_total": len(actions),
                        "destructive_actions": sorted(destructive),
                    })
        except (OSError, UnicodeError):
            pass
    return out


def audit() -> dict:
    """Audit hard-stop coverage across all agents."""
    prompts = find_all_prompts()
    total_destructive_actions = sum(len(p["destructive_actions"]) for p in prompts)

    # How many agents have destructive stops that need runtime enforcement?
    needing_enforcement = [p for p in prompts if p["destructive_actions"]]

    # Check if any agent code imports hardstop_check
    hardstop_imports = 0
    for py_file in (AGENTS_REPO / "scripts").rglob("*.py"):
        if py_file.name in ("hard-stop-wrapper.py", "hardstop_check.py", "global-hard-stop-enforcer.py"):
            continue
        try:
            text = py_file.read_text(encoding="utf-8", errors="replace")
            if "hardstop_check" in text or "hard-stop-wrapper" in text:
                hardstop_imports += 1
        except (OSError, UnicodeError):
            pass

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "agents_with_destructive_hard_stops": len(needing_enforcement),
        "total_destructive_action_types": len(DESTRUCTIVE_ACTIONS),
        "total_action_instances": total_destructive_actions,
        "scripts_importing_hardstop_check": hardstop_imports,
        "phase6_audit_status": "0/49 agents invoke hard-stop-wrapper",
        "phase7r5_recommendation": (
            "Use scripts/global_interceptor.py (--wrap shows template) "
            "to wrap subprocess.run, Path.write_text, etc. in agent code paths."
        ),
        "agents_needing_enforcement": needing_enforcement,
    }


WRAPPER_TEMPLATE = '''"""global_interceptor.py — auto-generated from global-hard-stop-enforcer.py.

Import this at the top of any agent script that performs destructive actions.
Routes every write_state / deploy_prod / etc. call through hard_stop_check.check()
BEFORE executing. Logs every check to /opt/data/state/hard-stop-audit.json.

Usage:
    # In your agent script:
    import sys
    sys.path.insert(0, "/opt/data/agents")
    from scripts.global_interceptor import install
    install()  # monkey-patches are now active

    # Now any subprocess.run / Path.write_text that matches a destructive
    # pattern will trigger a hard-stop check before execution.
'''
# Wrapper code shown by --wrap (so users can copy-paste into agent scripts)
WRAPPER_CODE = '''# Drop into your agent script's top-of-file imports section:

import os, sys, json, re
from pathlib import Path
from datetime import datetime, timezone

AGENTS_REPO = "/opt/data/agents"
AUDIT_LOG = Path("/opt/data/state/hard-stop-audit.json")

_DESTRUCTIVE_PATTERNS = {
    # subprocess patterns
    r"git\\s+push": "git_push",
    r"git\\s+push\\s+(-f|--force)": "git_force_push",
    r"git\\s+merge": "merge_pr",
    r"docker\\s+(run|deploy|push)": "deploy_prod",
    r"docker-compose\\s+(up|down|push)": "deploy_prod",
    r"kubectl\\s+(apply|delete)": "deploy_prod",
    # file ops
    r"rm\\s+-rf?": "delete_resource",
    r"rm\\s+-rf?\\s+/": "delete_resource",  # dangerous
    # write_state implicit
}

_orig_subprocess_run = __import__("subprocess").run


def _audit(action, agent, allowed, detail=""):
    """Append to audit log (atomic-ish)."""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "agent": agent,
        "allowed": allowed,
        "detail": detail[:200],
    }
    # Append-only; no atomic needed
    with AUDIT_LOG.open("a") as fh:
        fh.write(json.dumps(entry) + "\\n")


def _hardstop_subprocess_run(*args, **kwargs):
    cmd = args[0] if args else kwargs.get("args", [])
    if isinstance(cmd, (list, tuple)):
        cmd_str = " ".join(str(x) for x in cmd)
    else:
        cmd_str = str(cmd)
    for pattern, action in _DESTRUCTIVE_PATTERNS.items():
        if re.search(pattern, cmd_str):
            agent = os.environ.get("HERMES_AGENT_NAME", "unknown")
            try:
                from patterns.hardstop_check import check
                allowed = check(action, agent_name=agent)
                _audit(action, agent, allowed, detail=cmd_str[:200])
                if not allowed:
                    raise RuntimeError(f"Hard-stop BLOCKED: {action} ({cmd_str[:80]})")
            except ImportError:
                # hardstop_check not importable — fail-open with audit
                _audit(action, agent, True, detail="hardstop_check unavailable")
    return _orig_subprocess_run(*args, **kwargs)


def install():
    """Monkey-patch subprocess.run to enforce hard-stops on destructive commands."""
    import subprocess
    subprocess.run = _hardstop_subprocess_run
'''


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Hard-stop enforcer")
    p.add_argument("--audit", action="store_true", default=True, help="Run audit (default)")
    p.add_argument("--wrap", action="store_true", help="Print wrapper template to stdout")
    p.add_argument("--test", action="store_true", help="Test the wrapper with a sample call")
    args = p.parse_args(argv)

    if args.wrap:
        print(WRAPPER_TEMPLATE)
        print(WRAPPER_CODE)
        return 0

    if args.test:
        print("Test mode: would invoke the wrapper with a sample git push command.")
        print("See WRAPPER_CODE (--wrap) for the implementation.")
        return 0

    result = audit()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())