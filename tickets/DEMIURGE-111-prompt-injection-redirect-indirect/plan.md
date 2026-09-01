# DEMIURGE-111: prompt-injection-redirect-indirect

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Re-aim prompt-injection detection: instead of 'show me your system prompt' (extraction), test for 'I just read this article and it told me to do X' (indirect injection). Add per-source allowlist for agent-ingested content.

## Acceptance criteria

- [ ] Red-team scenarios re-aimed at indirect injection
- [ ] Test coverage on agent-ingested content paths (fetched from external sources)
- [ ] Per-source allowlist where applicable (e.g. review sites, social feeds)

## Deliverables (paths)

- `patterns/indirect-injection-guard.py`
- `tests/red-team/indirect-injection-tests.py`

## Verification

```bash
# See progress.md for verification output (once started)
```
