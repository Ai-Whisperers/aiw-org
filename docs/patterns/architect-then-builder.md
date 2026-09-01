---
pattern: architect-then-builder
one_liner: Separate design from implementation — architect agent produces spec, builder agent implements spec.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ✗ (not yet — both roles conflated in current PROMPT.md files)
related_files:
  - /opt/data/agents/01-operations/architect-agent/PROMPT.md
  - /opt/data/agents/02-quality/auditor-agent/PROMPT.md
  - /opt/data/agents/scripts/router.py
dimensions: [orchestration, workflow-discipline]
---

# Two-Phase Build: Architect Then Builder

## What it is

Design and implementation are cognitively distinct activities. A model that is simultaneously figuring out what to build and building it tends to make local decisions that look reasonable in isolation but are globally inconsistent. The two-phase pattern separates these activities into distinct agent roles. The architect agent receives the goal and produces a specification: module boundaries, data models, interface contracts, sequencing. The spec is the output — not code. Only when the spec is complete and reviewed does the builder agent begin.

## When to reach for it

- When building anything with more than two or three modules
- When the work will be executed by multiple agents or multiple team members
- When quality review is required before merging
- When scope is ambiguous enough that the implementer would need to make non-trivial design decisions

## When NOT to

- When the task is a single, self-contained change with no meaningful design surface
- When the user has already provided a complete specification
- When the workflow is exploratory and the design must emerge from implementation

## AIW-specific adoption

Currently, AIW's `01-operations/*` PROMPT.md files often conflate architect + builder roles. The plan (Phase 3) creates:
- **`architect-agent`** — produces spec (no code)
- **`builder-agent`** — implements spec (no design decisions)
- **`auditor-agent`** — verifies implementation against spec

This pattern + auditor-agent pattern together form the "two-phase build with auditor" pipeline.

## Related playbook patterns

- `auditor-agent.md` — verifies the builder's work
- `proposer-authority-separation.md` — architect proposes, auditor authorizes
- `recipe-not-conversation.md` — architect outputs a recipe
- `standing-eval-capability.md` — the auditor role can be implemented as an eval
