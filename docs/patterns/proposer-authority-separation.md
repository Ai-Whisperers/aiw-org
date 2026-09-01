---
pattern: proposer-authority-separation
one_liner: The entity that proposes an action is the worst authority to approve it — route approval through a role with no stake in the proposal's acceptance.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ◐ (hard-stops exist but proposer→authority flow is implicit)
related_files:
  - /opt/data/agents/patterns/hard-stop-wrapper.py
  - /opt/data/agents/scripts/router.py
  - /opt/data/agents/docs/adr/0003-handoff-boundary-integrity.md
dimensions: [reliability, orchestration]
---

# Separate the Proposer From the Authority

## What it is

In agentic systems, the agent that proposes an action is structurally biased toward approval. Separating the proposer from the authority means the entity with the power to approve and execute does not have a stake in the proposal: it could be a second agent, a deterministic validator, a human, or a gated pipeline stage. The authority's job is to assess whether the proposal is safe, correct, and aligned with intent — and it must be able to say no.

## When to reach for it

- Before any irreversible action (file deletion, deployment, external API call, message send)
- When an agent is designing and implementing in the same turn — split the roles
- When debugging a pipeline that approves its own work
- When human-in-the-loop workflows require explicit structure

## When NOT to

- Trivially reversible, low-stakes actions
- Fully automated pipelines with robust rollback
- Exploratory, draft, or ephemeral work

## AIW-specific adoption

AIW has `patterns/hard-stop-wrapper.py` which encodes whitelist/blacklist enforcement. Currently:
- The same agent that proposes an action also evaluates it against the whitelist
- This conflates proposer + authority

The fix: hard-stop wrapper should be re-architected as a separate "authority" process. The proposing agent signals intent; the authority process validates it. This is what ADR-0003 (handoff boundary integrity) and the `auditor-agent` pattern together imply.

## Related playbook patterns

- `auditor-agent.md` — the auditor is the authority
- `architect-then-builder.md` — architect proposes, builder executes, auditor verifies
- `guardrails-and-escalation.md` — multi-layer defense
