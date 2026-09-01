# ADR-0001: Adopt AGENTS.md Methodology Layer for AIW Org

- **Date:** 2026-09-01
- **Status:** Accepted
- **Deciders:** AIW org (Ivan Weiss Van Der Pol), with research synthesis from Hermes session `20260901_134405_00cab4`
- **Affects:** All AIW org repos; agent invocation discipline; documentation workflow; future session continuity

## Context

AIW org has a working multi-agent orchestration stack: 24 DEMIURGE agents + 39 sub-agents + 63 PROMPT.md files, with cron-driven pipeline (`signal_queue.py → router.py → intake.py → results-collector.py`), YAML dispatch rules, and Hermes-router-revenue as the meta-router. The architecture is sound and competitive with community projects (crewAI, oh-my-claudecode, mission-control).

**The gap:** No cross-vendor agent discipline doc. `OPERATIONS.md` and `ORCHESTRATION.md` exist but describe what the system does, not how agents (Claude Code, Codex, Cursor, Gemini, Windsurf, OpenClaw, Hermes) should behave when working in this org. Recurring failure mode observed across multiple sessions in 2026-08 / 2026-09: agents say "writing now" / "shipping X" and end the turn without `write_file`/`patch`/`terminal` — the **preamble-stall** failure mode.

Research across the community (`obra/superpowers`, `affaan-m/ECC`, `mattpocock/skills`, `iPythoning/b2b-sdr-agent-template`, `cloud-custodian`) found that mature multi-agent orgs all ship an `AGENTS.md` file that codifies: starting-work ritual, ending-work ritual, verification commands, git discipline, anti-patterns, engineering principles, and safety red lines.

## Decision

Adopt **`AGENTS.md` as the single authoritative collaboration rulebook for AIW org**, modeled on `iPythoning/b2b-sdr-agent-template/AGENTS.md` and merged with AIW-specific safety red lines and verification commands.

**Concrete artifacts shipped in this decision:**
- `/opt/data/agents/AGENTS.md` — the rulebook itself (6 KB, 10 required sections)
- `/opt/data/agents/docs/HANDOFF.md` — current-state-of-work log (required by AGENTS.md)
- `/opt/data/agents/docs/adr/0000-template.md` + this ADR — architecture-decision-record infrastructure

**Plus** install 7 community skills from `obra/superpowers`:
- `verification-before-completion` (literal cure for preamble-stall)
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `executing-plans`
- `receiving-code-review`
- `finishing-a-development-branch`
- `anti-laziness` (clawhub alternative)

## Alternatives Considered

### Alternative 1: Continue without AGENTS.md, rely on existing OPERATIONS.md
- **Pros:** No new file to maintain.
- **Cons:** Recurring preamble-stall failures (4× in 36h per session evidence). No cross-vendor discipline. New sessions re-discover org conventions from scratch.
- **Why not:** Doesn't fix the failure mode that motivated this research.

### Alternative 2: Use only obra/superpowers's writing-skills convention for individual PROMPT.md files
- **Pros:** Skill-level discipline, smaller scope.
- **Cons:** Doesn't address cross-agent coordination. Each skill stands alone; no shared ritual.
- **Why not:** Doesn't capture the org-wide coordination pattern that `AGENTS.md` provides.

### Alternative 3: Vendor-specific AGENTS.md files per tool (.claude/, .cursor/, .codex/)
- **Pros:** Tool-native.
- **Cons:** Splits truth across multiple files. Conflicts hard to detect. iPythoning's exact anti-pattern is "❌ 把关键上下文写进 `.claude/`、`.cursor/` 等厂商私有目录".
- **Why not:** Explicitly forbidden by ECC and iPythoning.

### Alternative 4: Wait for a "more mature" framework to emerge before standardizing
- **Pros:** Avoid premature standardization.
- **Cons:** The 4-session preamble-stall pattern is happening now. Waiting costs visible work.
- **Why not:** Action beats waiting.

## Consequences

### Positive
- **Preamble-stall cure** via `verification-before-completion` skill (installed)
- **Cross-vendor agent discipline** for all 63 PROMPT.md agents
- **Session continuity** via HANDOFF.md (no more "what was I doing")
- **Decision traceability** via ADR infrastructure (no more "why did we do this?")
- **Safety** via explicit red lines (token-leak, PII, BWS wrapper usage)
- **Composition with existing infra** — `OPERATIONS.md` and `ORCHESTRATION.md` unchanged, AGENTS.md complements

### Negative / Costs
- One new file to maintain (`AGENTS.md` + `HANDOFF.md` + `docs/adr/`)
- Discipline required: agents must read AGENTS.md first (lazy agents will skip)
- Skill scanner blocked 2 obra skills with DANGEROUS verdict (`writing-skills`, `using-superpowers`) — must manually audit before installing

### Risks + Mitigations
- **Risk:** Agents ignore AGENTS.md (recency bias + lazy behavior)
  **Mitigation:** Build the discipline into `commit-before-preamble` and `pre-tool-call-discipline` local skills (already installed). Verification-before-completion forces fresh-verification claims.
- **Risk:** AGENTS.md becomes stale (vendor tools change, AIW adds new patterns)
  **Mitigation:** HANDOFF.md update rule + ADR review every quarter
- **Risk:** HANDOFF.md becomes a wall of text, agents skip
  **Mitigation:** AGENTS.md mandates "restate current task in your own words" before starting work

## Provenance

- Research synthesis: `/opt/data/profiles/ivan/plans/2026-09-01-aiw-research-round-4-upgrades-templates.md`
- Community source: `iPythoning/b2b-sdr-agent-template/AGENTS.md` (the closest peer-project AGENTS.md)
- Methodology reference: `obra/superpowers` skill framework (280k stars)

## Related

- `/opt/data/agents/AGENTS.md` (the rulebook)
- `/opt/data/agents/docs/HANDOFF.md` (current state)
- `/opt/data/profiles/ivan/plans/2026-09-01-aiw-research-round-3-communities.md` (predecessor)
- `/opt/data/profiles/ivan/plans/2026-09-01-harness-failure-modes-and-community-patterns.md` (the failure mode that motivated this ADR)
