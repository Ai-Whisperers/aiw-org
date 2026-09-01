# AIW Pattern Index

> **AIW-specific curated patterns for building in the agentic age.** Adapted from [`obra/agent-building-playbook`](https://github.com/obra/agent-building-playbook) (22KB INDEX, 50+ patterns, 7 tags).
>
> **Two audiences, one source:**
> - **Agents** read this INDEX — dense, token-efficient, one-line descriptions
> - **Humans** browse `patterns/` — full pattern bodies
>
> **Maintained by:** AIW org, source of truth in this directory.

---

## Patterns (8 total)

| Pattern | Status | One-liner | Source |
|---|---|---|---|
| [reliability-before-features](reliability-before-features.md) | ✓ adopted | Flakiness, not capability, is the enemy — fix reliability before adding features | obra playbook |
| [recipe-not-conversation](recipe-not-conversation.md) | ◐ adopted | A conversation is a trace of what happened once — a recipe is a specification that can be replayed | obra playbook |
| [architect-then-builder](architect-then-builder.md) | ✗ not yet | Separate design from implementation — architect produces spec, builder implements | obra playbook |
| [auditor-agent](auditor-agent.md) | ◐ adopted | The agent that did the work is the worst possible choice to verify the work | obra playbook |
| [clean-slate-delegation](clean-slate-delegation.md) | ◐ adopted | When spawning a subagent, default to empty context — pass distilled briefing | obra playbook |
| [proposer-authority-separation](proposer-authority-separation.md) | ◐ adopted | The entity that proposes an action is the worst authority to approve it | obra playbook |
| [long-horizon-memory](long-horizon-memory.md) | ◐ adopted | Long-running tasks require three memory strategies — compaction, notes, isolation | obra playbook |

**Status legend:** ✓ = fully implemented in AIW | ◐ = partially implemented | ✗ = planned, not yet built

---

## Pattern → AIW file mapping (quick reference)

| AIW file | Patterns it implements |
|---|---|
| `/opt/data/agents/AGENTS.md` | meta-principles > Verify Independently, meta-principles > Start With the Least Agentic Thing, `reliability-before-features` |
| `/opt/data/agents/docs/HANDOFF.md` | `long-horizon-memory` (notes files), context-engineering > Checkpoint to a Handoff File |
| `/opt/data/agents/docs/adr/0003-handoff-boundary-integrity.md` (ADR-0003) | context-engineering > Thin Pointers Zero Poisoning, observability > If It's Important Emit an Event |
| `/opt/data/agents/docs/adr/0002-instinct-integration-plan.md` | `recipe-not-conversation`, instinct integration |
| `/opt/data/agents/scripts/router.py` | `reliability-before-features` (pre_dispatch_check), `clean-slate-delegation` (signal routing) |
| `/opt/data/agents/scripts/circuit_breaker.py` | `proposer-authority-separation`, reliability > Fail-Loud Harnesses |
| `/opt/data/agents/scripts/memory/compactor.py` | `long-horizon-memory` (compaction) |
| `/opt/data/agents/scripts/memory/signal_index.py` | `long-horizon-memory` (L3 inverted index) |
| `/opt/data/agents/scripts/memory/commitments.py` | `recipe-not-conversation` (L1 schema) |
| `/opt/data/agents/scripts/observability/agent-tracer.py` | observability > Build an Awareness Layer |
| `/opt/data/agents/tests/run-all.sh` | `reliability-before-features` (canonical gate) |
| `~/.hermes/skills/verification-before-completion/` | reliability > Evidence Before Assertions |
| `~/.hermes/skills/dispatching-parallel-agents/` | `clean-slate-delegation`, orchestration > Run Independent Agents in Parallel |
| `~/.hermes/skills/subagent-driven-development/` | `clean-slate-delegation`, orchestration > Use Sub-Agents as Context Sinks |

---

## Provenance

- **Source:** [`obra/agent-building-playbook`](https://github.com/obra/agent-building-playbook) (Jesse Vincent, 22.3KB INDEX)
- **Adapted for:** AIW org's specific stack (Hermes + cron + local-first + 63 agents)
- **Cross-referenced against:** Round 1-7 research
- **See also:** `/opt/data/profiles/ivan/plans/2026-09-01-aiw-consolidated-reference.md`

---

## How to add a new pattern to this INDEX

1. Read `obra/agent-building-playbook/INDEX.md` for the canonical format
2. Write the full pattern body to `patterns/<kebab-case-name>.md` with YAML frontmatter (`pattern`, `one_liner`, `source`, `status`, `aiw_implements`, `related_files`, `dimensions`)
3. Add a row to the table above
4. Update any "Pattern → AIW file mapping" entries as needed
