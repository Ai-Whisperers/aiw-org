# DEMIURGE-085: close-four-pre-existing-lint-failures

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Fix 4 PROMPT.md files with malformed frontmatter. Add 'meta-curator' archetype + 'crosscut' layer to lint-prompts.py.

## Acceptance criteria

- [ ] scripts/lint-prompts.py updated (commit 2d8bea7)
- [ ] 4 PROMPT.md files fixed (frontmatter closes, required fields added, duplicates removed)
- [ ] lint 76 pass / 0 fail (was 72/4)
- [ ] tests/test_add_max_output_tokens.py: 16 pass
- [ ] tests/test_agent_composition.py: composition refs resolve

## Deliverables (paths)

- `scripts/lint-prompts.py`
- `01-operations/founder-bandwidth-watchdog/PROMPT.md`
- `04-engineering/devops-monitor-30min/PROMPT.md`
- `demiurge/agents/curator-evolver/PROMPT.md`
- `demiurge/agents/homunculus/PROMPT.md`
- `tests/test_add_max_output_tokens.py`

## Verification

```bash
# See progress.md for verification output
```
