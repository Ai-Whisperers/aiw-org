# DEMIURGE-089: ws-1-prompt-body-restoration

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Restore 65 of 72 PROMPT.md bodies using per-file history search (current frontmatter + historical body splice). Leave 7 unrecoverable as stubs.

## Acceptance criteria

- [ ] scripts/restore-prompt-bodies.py: dry-run default, --apply requires --force
- [ ] tests/test_restore_prompt_bodies.py: 16 pass, safety contract covered
- [ ] analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md: postmortem
- [ ] Repo: 4/76 -> 69/76 prompts with body >= 20 lines
- [ ] Live host: 4/76 -> 69/76 (matches repo)
- [ ] 7 unrecoverable stubs match brief exactly

## Deliverables (paths)

- `scripts/restore-prompt-bodies.py`
- `tests/test_restore_prompt_bodies.py`
- `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md`
- `65 PROMPT.md files restored`

## Verification

```bash
# See progress.md for verification output
```
