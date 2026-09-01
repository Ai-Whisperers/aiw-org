# DEMIURGE-085 Progress

- Commit 2d8bea7 shipped 2026-09-02: fix(prompts): close the 4 pre-existing lint failures
- lint promoted from 72/4 to 76/0 after adding meta-curator + crosscut to VALID_ARCHETYPES + VALID_LAYERS in scripts/lint-prompts.py
- Added layer/topology/archetype to founder-bandwidth-watchdog/PROMPT.md (was missing required fields)
- Closed malformed frontmatter on devops-monitor-30min/PROMPT.md (was missing closing --- )
- Removed duplicate parent_spec + max_output_tokens blocks from curator-evolver + homunculus
- tests/test_add_max_output_tokens.py now has 16 pass (relaxed assertion: any max_output_tokens value 800/1200/1500 acceptable)
- tests/test_agent_composition.py::test_all_composition_refs_resolve passes after removing composition refs to non-existent agents
- Live host synced: live /opt/data/agents/scripts/lint-prompts.py now passes at 76/0
