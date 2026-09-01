"""hardstop_check.py — Convenience wrapper for agents to invoke hard-stops.

Agents should import this module and call `check()` before executing destructive
actions. The wrapper logs every check to /opt/data/state/hard-stop-audit.json.

Usage (in agent PROMPT):
    from patterns.hardstop_check import check, log_only

    # Strict mode (raises HardStopViolation if blocked)
    check("force_push", agent_name="04-engineering/devops-monitor-30min")

    # Log-only mode (records but doesn't raise)
    if not log_only("read_state", agent_name="..."):
        continue

    # With role override
    check("disable_hardstop", agent_name="...", role="ivan")
"""
import importlib.util
import sys
from pathlib import Path

_PATTERNS_DIR = Path(__file__).parent
_WRAPPER_PATH = _PATTERNS_DIR / "hard-stop-wrapper.py"

# Load hard-stop-wrapper.py dynamically (Python doesn't auto-normalize hyphens)
_spec = importlib.util.spec_from_file_location("hard_stop_wrapper", _WRAPPER_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load hard-stop-wrapper.py from {_WRAPPER_PATH}")
hard_stop_wrapper = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hard_stop_wrapper)
sys.modules["hard_stop_wrapper"] = hard_stop_wrapper


class HardStopViolation(Exception):
    """Raised when an action is blocked by hard_stops."""

    def __init__(self, agent_name: str, action: str, role: str):
        self.agent_name = agent_name
        self.action = action
        self.role = role
        super().__init__(
            f"HARD-STOP VIOLATION: agent={agent_name}, action={action}, role={role}"
        )


def check(action: str, agent_name: str, role: str = "ai-agent", log: bool = True) -> bool:
    """Check if action is allowed for the given agent+role.

    Args:
        action: One of STANDARD_ACTIONS (or any custom action).
        agent_name: Path-like identifier (e.g. "04-engineering/ai-safety-engineer").
        role: Who is making the request ("ai-agent", "ivan", "kiki").
        log: If True, append to audit log.

    Returns:
        True if allowed; False if blocked.

    Raises:
        HardStopViolation if blocked AND raise_on_block=True.
        ValueError if agent_name contains path traversal (Phase 29 fix BUG-HUNT H1).
    """
    # Phase 29 fix (BUG-HUNT H1): validate agent_name against path traversal
    if not agent_name:
        raise ValueError("agent_name is required")
    if ".." in agent_name.split("/") or agent_name.startswith("/") or "\\" in agent_name:
        raise ValueError(f"invalid agent_name (path traversal): {agent_name!r}")
    prompt_path = (Path("/opt/data/agents") / agent_name).resolve() / "PROMPT.md"
    # Defense in depth: ensure resolved path stays under agents root
    try:
        prompt_path.relative_to(Path("/opt/data/agents").resolve())
    except ValueError:
        raise ValueError(f"invalid agent_name (escapes agents root): {agent_name!r}")
    if not prompt_path.exists():
        if log:
            hard_stop_wrapper._log_check(agent_name, action, role, True)  # default allow
        return True  # No PROMPT = no hard_stops

    hard_stops = hard_stop_wrapper.load_hard_stops(prompt_path)
    allowed = hard_stop_wrapper.check_action(action, role, hard_stops)

    if log:
        hard_stop_wrapper._log_check(agent_name, action, role, allowed)

    return allowed


def check_or_raise(action: str, agent_name: str, role: str = "ai-agent") -> None:
    """Like check(), but raises HardStopViolation if blocked."""
    if not check(action, agent_name, role=role):
        raise HardStopViolation(agent_name, action, role)


def log_only(action: str, agent_name: str, role: str = "ai-agent") -> bool:
    """Record the check but never raise. Returns True/False for observability."""
    return check(action, agent_name, role=role, log=True)


if __name__ == "__main__":
    # CLI convenience
    if len(sys.argv) < 3:
        print("Usage: python3 hardstop_check.py <agent_name> <action> [role]")
        sys.exit(1)
    agent = sys.argv[1]
    action = sys.argv[2]
    role = sys.argv[3] if len(sys.argv) > 3 else "ai-agent"
    allowed = check(action, agent, role=role)
    if allowed:
        print(f"ALLOWED: {action} for {agent} ({role})")
        sys.exit(0)
    else:
        print(f"BLOCKED: {action} for {agent} ({role})")
        sys.exit(1)
