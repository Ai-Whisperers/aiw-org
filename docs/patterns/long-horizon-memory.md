---
pattern: long-horizon-memory
one_liner: Long-running tasks require three memory strategies — compaction, notes files, and isolation.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ◐ (notes files via HANDOFF.md, compaction via Phase 1.2, isolation partial)
related_files:
  - /opt/data/agents/docs/HANDOFF.md
  - /opt/data/agents/scripts/memory/compactor.py
  - /opt/data/agents/scripts/memory/signal_index.py
  - /opt/data/agents/scripts/memory/commitments.py
dimensions: [context-engineering]
---

# Long-Horizon Memory: Compaction, Notes, Isolation

## What it is

A single context window cannot hold the full history of a week-long project. Long-horizon memory is three complementary strategies applied in combination.

**Compaction:** as conversation history ages, summarize aggressively — what was decided, not how; what was built, not every failed attempt. The compact summary replaces the verbose transcript.

**Notes files:** maintain a persistent running document outside the context window that accumulates decisions, open questions, discovered facts, next actions. Every session begins by reading this file and ends by updating it.

**Isolation:** any sub-task with a well-defined output is a candidate for a fresh sub-agent session that inherits only the context it needs.

## When to reach for it

- When a task will span more than a few sessions and cannot be completed in a single context window
- When the working context is mostly history from steps that are now complete
- When facts discovered in one session need to be available in the next
- When agent performance degrades over a long session

## When NOT to

- Short tasks that complete in a single session
- Tasks where the full history is required (legal/compliance/audit)

## AIW-specific adoption

Phase 1 delivery this session covers all three:
- **Compaction:** `/opt/data/agents/scripts/memory/compactor.py` (token-threshold-based + archive)
- **Notes files:** `/opt/data/agents/docs/HANDOFF.md` (read at session start, update at end)
- **Isolation:** `/opt/data/agents/scripts/memory/signal_index.py` (L3 inverted index) + commitment extraction (L1 schema)

**Status:** Compaction and notes are done. Isolation is partial — subagents don't get clean context yet (Phase 3 work).

## Related playbook patterns

- `recipe-not-conversation.md` — recipes ARE the long-horizon memory format
- `clean-slate-delegation.md` — isolation strategy
- `checkpoint-handoff-file.md` — handoff files are notes files
- `subagents-as-context-sinks.md` — subagents as memory mechanism
