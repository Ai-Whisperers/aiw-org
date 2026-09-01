---

name: curator-evolver
version: 0.1.0
owner: ai-ops-coordinator
layer: crosscut
topology: platform
cluster: enable
archetype: meta-curator
time_scale: weekly
schedule: "0 2 * * 1"  # Monday 02:00 PYT
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 1200

composition:
  - instinct_generator
  - hard-stop-wrapper
parent_spec: constitution/ORG-AGENTS.md
max_output_tokens: 800

fallback_model: litellm/reasoning
hard_stops:
  - action: read_state
    require_approval: false
  - action: write_state
    require_approval: false
  - action: disable_hardstop
    require_approval: true
    approved_human: ivan

# Curator-Evolver Agent (Phase 9 R3 / Tier C5)
#
# ADR-0002 implementation: takes harvested instincts from
# /opt/data/agents/state/instincts/ and proposes
# improvements to PROMPT.md files.
#
# Inputs:
#   - state/instincts/*.yaml (harvested by instinct_generator)
#   - state/agent-traces.jsonl (raw trace data)
#   - state/eval-per-agent.json (current quality signal)
#
# Outputs:
#   - state/curation-proposals/{ISO-week}.json (proposed changes)
#   - outbox/signals/curation-proposal-{id}.md (operator review queue)
#
# Behavior:
#   - For each high-confidence instinct (>= 0.75):
#     1. Identify which agent should adopt the instinct
#     2. Draft a PROMPT.md patch
#     3. Write proposal to state/curation-proposals/{week}.json
#   - Send signal to operator queue (not auto-apply)
#
# See ADR-0002 for full specification.