# DEMIURGE-123: document-self-improving-capabilities

**Sprint**: Phase Kernel
**Size**: 30m
**Owner**: AI

## Objective

Ship `analysis/AIW-SELF-IMPROVING-CAPABILITIES.md` (1-page summary):
- What "self-improving" means in AIW
- Evidence from production runs (instincts count, evolution events)
- What's available vs what's planned
- 5 patterns AIW should adopt (from David corpus)
- 3 patterns AIW should NOT copy

## Acceptance criteria

- [ ] analysis/AIW-SELF-IMPROVING-CAPABILITIES.md (~1 page, 1-3KB)
- [ ] References curator-evolver.py, homunculus.py, instincts/
- [ ] Cites actual evidence (instinct count, evolution events)
- [ ] Operator-actionable recommendations (1h, doc-only)

## Verification

- File exists, content reflects actual AIW state (not generic)
- pytest + lint still pass (no code changes, only doc)
