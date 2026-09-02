# AIW Agentic Engineering Workflow

> **What this is**: A READ-FIRST pointer doc. Distills the agentic
> engineering workflow into one place. For deep detail, read
> `AGENTS.md`, `OPERATIONS.md`, `ORCHESTRATION.md`, `docs/HANDOFF.md`.
>
> **Status**: DONE
> **Author**: AI (Tier 1 immediate-action ship)
> **Format**: distilled overview, NOT a replacement for the docs it points at

## 1. The workflow in one sentence

**A human operator specifies the goal; an AI agent executes the work
in atomic commits on a feature branch; a CI gate + a cron fleet
verify + sustain the result.**

## 2. Roles

| Role | Owner | What they do |
|---|---|---|
| **Operator** | Ivan (you) | Sets goals, authorizes shape changes, reviews PRs, makes business decisions. Per AGENTS.md "operator-only" rule (R11), nothing here is automated away. |
| **AI agent** | Claude / Codex / Hermes / any vendor following AGENTS.md | Reads goal, executes work, commits, opens PR. Per AGENTS.md, the same rules apply across vendors. |
| **Demiurge** | `scripts/curator-evolver.py` + `homunculus.py` + `instinct_generator.py` | Reads `agent-traces.jsonl`, generates instincts, proposes PROMPT.md improvements, validates them. The system improves itself. See `analysis/AIW-SELF-IMPROVING-CAPABILITIES.md`. |
| **Cron fleet** | 168 enabled jobs in `/opt/data/.hermes/cron/jobs.json` | Runs the AIW fleet without operator input: every 15min state validation, daily summaries, weekly retrospectives, etc. |
| **Eval gate** | `tests/test_eval_gate*.py` | Blocks regressions. The "no-skips" policy: if a test fails, the agent's claim is rejected. |

## 3. The sprint lifecycle (from ticket → merge)

```
1. Operator creates a ticket (or it gets created during analysis)
   → tickets/DEMIURGE-NNN-<slug>/{context,plan,progress,tracker}.md

2. AI agent (Hermes / Claude) reads the ticket
   → reads AGENTS.md (§"Before starting work")
   → runs the verification command (the canonical baseline)
   → restates the goal before touching code (R8 + R11)

3. AI agent executes the work
   → atomic commits (one commit = one verifiable claim)
   → Conventional Commits format ("fix:", "feat:", "docs:")
   → each commit independently revertable

4. AI agent opens a PR
   → description includes: what changed, why, verification evidence
   → links to ticket tracker
   → per AGENTS.md §"Before declaring work done": FRESH verification
     in the same response as the completion claim

5. Operator reviews + merges (per R11, this is the operator-gated step)

6. Trust-window + state-write audit (when relevant)
   → captures evidence the change didn't break the system
   → DEMIURGE-094 closed out exactly this pattern for the WS-1 incident
```

## 4. The cron layer (the fleet runs while you don't)

From `analysis/CRON-EMPTY-PROMPT-AUDIT-2026-09-02.md`:

- **168 enabled jobs** in `/opt/data/.hermes/cron/jobs.json`
- **6 charter departments** run their daily/weekly crons autonomously
- **The demiurge layer** (curator-evolver, homunculus) generates new
  agent improvements + instincts YAML weekly
- **Heartbeats** every 30 minutes (different cadence for on/off hours)
- **61 jobs have empty prompts** — ~90% are working correctly (the empty
  prompt is the cron-handler convention), 4 are likely dead, 10 are
  partial-orphans worth confirming

The cron layer is what makes AIW "agentic engineering in production."
**Without it, AIW would be a code repo. With it, AIW is a running
org.**

## 5. The self-improving loop (the demiurge layer)

Per `analysis/AIW-SELF-IMPROVING-CAPABILITIES.md` — the full loop:

```
agent-traces.jsonl → instinct_generator → instincts-{ISO}.yaml
                                              ↓ (>=0.75 confidence)
                                        curator-evolver
                                              ↓
                                  curation-proposals/{ISO-week}.json
                                              ↓
                                          homunculus (validates)
                                              ↓ (passes)
                                  curation-approved/{ISO-week}.json
                                              ↓
                                    operator applies patch
                                              ↓
                              next instinct generation observes change
```

**This is the "self-improving" claim grounded in code.** 167K views
worth of David corpus content confirms this is the field's direction.

## 6. The kernel extraction interface

Per `docs/KERNEL-DESIGN-2026-09-02.md` (shipped at commit `b7637cf`):

- AIW-org is **instance zero** of an instantiable org kernel
- Saskia gets her own org on this kernel
- The kernel is the **interface** between operator workflow (above)
  and the runnable instance
- **Sprint F (WS-5)** ships the actual `kernel/` directory + `bootstrap-instance.sh`

**For now (pre-Sprint F):** AIW runs as instance zero. The workflow above
is the production behavior. **Post-Sprint F:** a new instance (Saskia,
or anyone else) can be forked from the kernel and gets the same workflow
out of the box.

## 7. Pointers to the detailed docs

This doc is intentionally short. For detail:

- **`AGENTS.md`** — operator rules, anti-patterns, safety red lines, verification commands (the AI's contract)
- **`OPERATIONS.md`** — the runbook for live host operations
- **`ORCHESTRATION.md`** — how the operator specifies work to AI
- **`docs/HANDOFF.md`** — current state-of-work log (read at session start, update at session end)
- **`ORG-AGENTS.md`** — the canonical 47-agent roster + 9-schema producer→consumer matrix + 4-level escalation graph
- **`playbooks/01-operations.md`** — operations-specific playbook
- **`analysis/AIW-SELF-IMPROVING-CAPABILITIES.md`** — the self-improving loop deep-dive
- **`analysis/DAVID-ONDREJ-CONTENT-ANALYSIS-2026-09-02.md`** — external competitive analysis

## 8. What this doc is NOT

- **Not a replacement for AGENTS.md.** AGENTS.md is the AI's contract
  for behavior. This doc is the READ-FIRST orientation.
- **Not the kernel extraction spec.** That's in
  `docs/KERNEL-DESIGN-2026-09-02.md` and will be implemented in Sprint F.
- **Not an external pitch.** Per R11, this is internal-only.

## 9. Recent empirical evidence

This session (2026-09-02) shipped:

- **12 atomic commits** to `master` (Sprint A + Sprint A-extra + Sprint A-research)
- **6 atomic commits** to `ws-3-portable` (Sprint C, partial)
- **17 atomic commits** total
- **All under:** build-vs-close + R8 ("small commits, one verifiable claim each") + R11 ("operator-gated for client data + shape changes")

This is what "agentic engineering in production" looks like at AIW:
**small, atomic, verifiable, reviewable.** David's 167K-view "100
hours of Hermes Agent lessons in 46 minutes" maps to the same shape:
many small empirical commits, distilled into a pattern.

## 10. References

- `AGENTS.md` — operator rules
- `docs/HANDOFF.md` — current state
- `ORG-AGENTS.md` — roster
- `analysis/AIW-SELF-IMPROVING-CAPABILITIES.md` — self-improving loop
- `analysis/DAVID-ONDREJ-CONTENT-ANALYSIS-2026-09-02.md` — external analysis
- `docs/KERNEL-DESIGN-2026-09-02.md` — kernel extraction spec (Sprint F)
- `analysis/CRON-EMPTY-PROMPT-AUDIT-2026-09-02.md` — cron layer analysis
