---
pattern: clean-slate-delegation
one_liner: When spawning a subagent, default to empty context — pass distilled briefing, not full history.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ◐ (subagents get the relevant signal but full briefing is sometimes inherited)
related_files:
  - /opt/data/agents/scripts/router.py
  - /opt/data/agents/scripts/intake.py
  - /opt/data/agents/demiurge/agents/*/PROMPT.md
dimensions: [orchestration, context-engineering]
---

# Default to Clean-Slate Delegation

## What it is

When an orchestrator spawns a subagent, the default assumption is often that more shared context is better. This assumption is usually wrong. Context passed wholesale carries not just the relevant information but also the irrelevant, the contradictory, and the already-superseded. Clean-slate delegation inverts this: the default for any subagent is an empty context. The orchestrator explicitly constructs what the subagent needs.

## When to reach for it

- When spinning up a subagent to perform a focused, self-contained task
- When the orchestrator's conversation is long or contains exploratory content
- When multiple subagents are running in parallel and each needs a consistent, accurate view
- When a subagent will make decisions that need to be right on the first try

## When NOT to

- When the subagent genuinely needs the conversational history (e.g., summarization tasks)
- When the cost of constructing the briefing exceeds the cost of passing the history
- When the subagent is resuming a prior session and continuity is required

## AIW-specific adoption

`scripts/router.py` currently passes the full signal envelope to all recipients. For multi-recipient routing (fan_out: all), this means each subagent gets the entire briefing. **Better:** spawn subagents with empty context + a 1-paragraph distilled briefing from the orchestrator.

Currently implemented (partially) in router.py via pre_dispatch_check but the briefing structure isn't formalized. Should add a `briefing()` function that creates a structured summary from a signal.

## Related playbook patterns

- `thin-pointers.md` — pass paths, not content
- `just-in-time-retrieval.md` — agents pull what they need when they need it
- `subagents-as-context-sinks.md` — subagent absorbs complexity
