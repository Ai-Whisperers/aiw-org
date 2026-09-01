---
pattern: auditor-agent
one_liner: The agent that did the work is the worst possible choice to verify the work — put a second agent in the audit seat with no stake in the original claim.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ◐ (eval-gate-enforce.py exists but is not a formal auditor-agent)
related_files:
  - /opt/data/agents/scripts/eval/eval-gate-enforce.py
  - /opt/data/agents/scripts/eval/eval-gate-review.py
  - /opt/data/agents/02-quality/auditor-agent/PROMPT.md
dimensions: [reliability, orchestration]
---

# Use a Second Agent as Auditor

## What it is

When a task is completed by an agent, that agent's verification of its own output is structurally compromised: it is reasoning from the same assumptions, biases, and context that produced the original work. A second agent placed in the auditor role has none of those anchors. It reads the artifact cold — without the history of decisions that led to it — and applies independent judgment about whether the output matches the specification, whether required steps were actually taken, and whether claims of success are backed by evidence.

## When to reach for it

- Any high-stakes pipeline step whose failure has significant downstream costs
- Before any irreversible action (deploying, sending, deleting, publishing)
- When implementing a multi-agent workflow: design the auditor role explicitly

## When NOT to

- Simple deterministic steps where the output is machine-checkable without reasoning
- Tight interactive loops where the latency of a second agent call exceeds the acceptable feedback cycle

## AIW-specific adoption

`scripts/eval/eval-gate-enforce.py` exists and does part of this work but:
- It's a deterministic validator, not an LLM agent
- It's not adversarial (doesn't try to find what's wrong)
- It's not context-isolated (reads the same state as the builder)

The plan (Phase 3) creates a real `auditor-agent` that addresses all three gaps.

## Related playbook patterns

- `architect-then-builder.md` — auditor verifies the builder's work
- `verify-independently.md` — the meta-principle
- `demand-independent-proof.md` — the evidence standard
