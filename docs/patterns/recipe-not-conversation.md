---
pattern: recipe-not-conversation
one_liner: A conversation is a trace of what happened once — a recipe is a specification that can be replayed, inspected, versioned, and recovered from.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ◐ (some PROMPT.md are recipes, most are conversations)
related_files:
  - /opt/data/agents/docs/AGENTS.md
  - /opt/data/agents/01-operations/*/PROMPT.md
  - /opt/data/agents/docs/patterns/reliability-before-features.md
dimensions: [reliability, workflow-discipline]
---

# Encode Multi-Step Work as a Recipe

## What it is

Multi-step work expressed as ad-hoc conversation — "now do X, now do Y, now do Z" — is inherently fragile: it cannot be replayed from a checkpoint, it has no schema to validate, it accumulates context silently until something breaks, and its state is invisible to anyone who wasn't present for the conversation. A recipe encodes the same work as a declarative specification: each step is named, its inputs and outputs are defined, its dependencies are explicit, and its execution can be resumed after interruption. Recipes are checkpointed, auditable, and version-controlled.

## When to reach for it

- Any multi-step workflow that will run more than once
- When a workflow involves more than two sequential steps with handoffs between agents
- When you need recoverability: a recipe that checkpoints between steps can resume after interruption
- When a workflow must be auditable

## When NOT to

- Truly one-off, exploratory interactions
- Work that is inherently interactive, where the next step cannot be known until the previous result is seen

## AIW-specific adoption

AIW has ~63 PROMPT.md files. Audit categories:

**Recipe-style (good candidates):**
- Cron-driven agents with deterministic steps (`management-coordinator`, `board-monitor-30min`)
- Coordinators with explicit routing tables (`apollo-sales-lead`, `cadmus-lead-enrichment`)
- Eval/review agents with checklists (`qa-monitor`, `eval-agent-aware`)

**Conversation-style (over-conversationed):**
- Free-form advisory PROMPT.md (many 01-operations/* agents)
- Ad-hoc cron jobs with narrative descriptions

**Concrete next step:** Pick 3 high-frequency PROMPT.md and convert to recipe format (yaml frontmatter with named steps, inputs, outputs).

## Related playbook patterns

- `standing-eval-capability.md` — recipes need evals to verify replayability
- `auditable-artifacts.md` — recipes produce auditable artifacts naturally
- `reliability-before-features.md` — recipes are how reliability becomes encoded
