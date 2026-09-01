---

name: homunculus
version: 0.1.0
owner: ai-ops-coordinator
layer: crosscut
topology: platform
cluster: enable
archetype: meta-curator
time_scale: on-demand
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 1500

fallback_model: litellm/reasoning
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
  - action: disable_hardstop
    require_approval: true
    approved_human: ivan

---
# Homunculus Agent (Phase 9 R3 / Tier C5)
#
# ADR-0002 implementation: the "inner self" that operates between
# curator-evolver proposals and actual changes. Reads proposed
# curation changes and validates they will not violate:
#   - hard_stops policies
#   - parent_spec constraints
#   - eval-gate thresholds
#
# On validation failure: writes rejection to outbox/.
# On validation success: appends to state/curation-approved/ for
# next cron cycle to apply.
#
# Triggered: only after curator-evolver posts new proposals.
#
# Inputs:
#   - state/curation-proposals/{ISO-week}.json (curator-evolver output)
#   - all PROMPT.md files (for hard_stops validation)
#
# Outputs:
#   - state/curation-approved/{ISO-week}.json (validated proposals)
#   - outbox/signals/curation-rejection-{id}.md (on failure)
#
# See ADR-0002 for full specification.