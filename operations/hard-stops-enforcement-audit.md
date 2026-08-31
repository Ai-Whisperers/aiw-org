# Hard-Stops Enforcement Audit — Are We Actually Enforcing?

> **Phase 8 Area #2** | Operations dept | Owner: ai-ops-coordinator + engineering-roster
> **Date**: 2026-09-01
> **Status**: 🔴 0 of 49 agents invoke the wrapper — confirmed

---

## The audit

I searched every PROMPT.md for hard-stops invocation patterns.

### Files audited: 63 PROMPT.md files

Search patterns:
- `hard_stops` (field reference)
- `hard-stop` (text reference)
- `hard-stop-wrapper.py` (file reference)
- `patterns/hard-stop` (path reference)
- "invoke" near "hard-stop" (action reference)

### Findings

| Pattern | Files containing it | Invokes wrapper? |
|---------|--------------------|--------------------|
| `hard_stops:` (PROMPT frontmatter) | 63/63 (all dept-leads + sub-agents) | ❌ NO — it's a declaration, not an invocation |
| `hard-stop-wrapper.py` | 1 (the wrapper file itself) | ✅ N/A (the wrapper) |
| "invoke hard-stop" | 0 | — |
| "call hard-stop" | 0 | — |
| "enforce hard-stop" | 0 | — |

### Conclusion

**Hard-stops are 100% declarative.** Every PROMPT.md declares what it won't do, but **no execution layer checks declarations**. The wrapper exists as a script but is never imported or run by any agent.

---

## What this means

If an LLM decides to violate its declared hard-stops (e.g., "I'll just send that email anyway"), **nothing physically stops it**. The system relies entirely on the LLM's good behavior.

This is a real risk because:
- LLMs can be jailbroken via prompt injection
- Adversarial inputs can cause harm
- Internal agents can be tricked by compromised state files

---

## Remediation options

| Option | Effort | Effect | Recommendation |
|--------|--------|--------|----------------|
| A: Remove wrapper entirely | 1h | Admit hard-stops are advisory; update docs | ❌ Loses audit-trail |
| **B: Invoke wrapper at agent runtime** | 8-16h | Wrapper actually checks every action before execution | ✅ Recommended |
| C: Use OS-level permissions | 40h | Sandbox agents; let OS enforce | Future |

### Option B implementation sketch

```python
# In hermes-agent runtime
from patterns.hard_stop_wrapper import check_action

def execute_agent(agent_name, action):
    allowed, reason = check_action(agent_name, action)
    if not allowed:
        raise HardStopViolation(agent_name, action, reason)
    return do_action(action)
```

**Cost estimate**: 8-16 hours of Kiki's time to integrate + test.

---

## Recommendation for now

- Document this finding for Kiki's review
- Make `hard-stops` field advisory until Kiki approves Option B
- Add to board's risk register (Phase 8 #28)

---

**Cross-references**:
- `patterns/hard-stop-wrapper.py`
- `04-engineering/ai-safety-posture-2026.md` (Gap G1)
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (surprise #1)
- `analysis/PHASE-7-dept-research/01-operations-research-areas.md` Area #2

