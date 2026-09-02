---

name: athena-product-discovery-lead
version: 0.2.0
owner: ai-ops-coordinator
layer: atomic
topology: platform
archetype: team-lead
time_scale: minutes
composition:
  - thoth-literature-scanner
  - echo-community-scanner
max_output_tokens: 800

---

## Intentional stub

**Status**: This PROMPT.md has frontmatter only and a minimal body. The agent
is declared as a routing placeholder in the org topology, with full metadata
in the YAML (name, owner, archetype, time_scale, transfer_targets /
composition). The minimal body is intentional, not corruption.

**Rationale**: Per the 2026-09-01 incident analysis
(`analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md`), the restore-prompt-bodies
script `scripts/restore-prompt-bodies.py` (commit 320ffdc) successfully
recovered 65 of 72 truncated PROMPT.md files. The remaining 7 — including this
agent — were never longer than 9-18 lines in any commit on any branch. They
were always stubs.

**Design intent**: This agent is a placeholder name in the org topology
(Lead agent for the Product Discovery department. Aggregates customer signals, runs gap analysis, and routes briefs to other departments (marketing, sales, engineering).). When the agent's role becomes operational, the body should be
authored per `prompts/PROMPT-TEMPLATE.md` Section 6 (Body). A proper body
needs:

- Mission: lead product discovery; coordinate customer-signal-collector
- Inputs: customer-signal-raw signal channel; brief repository
- Hard-stops: never commit to engineering without sales alignment
- Composition: clio-customer-signal-collector (subordinate)

**Tracking**: DEMIURGE-095 closed-out the marker requirement. Follow-up work
to author the proper body for all 7 stubs is filed as `tickets/DEMIURGE-095b-author-stub-bodies/`
(operator-gated; ~2h per stub, 14h total).
