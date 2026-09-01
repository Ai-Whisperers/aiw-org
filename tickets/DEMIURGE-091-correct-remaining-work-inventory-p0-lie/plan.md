# DEMIURGE-091: correct-remaining-work-inventory-p0-lie

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Replace false 'zero P0 items open' claim with honest listing of: 4 credential leaks + 79 broken crons (47%) + 1 signal-indexer never ran + 424 decisions overflow.

## Acceptance criteria

- [ ] docs/REMAINING-WORK-INVENTORY-2026-09-01.md: 'How to use this inventory' section rewritten
- [ ] tests/test_inventory_p0_claim.py: 8 pass
- [ ] Literal phrase 'zero P0 items open' is gone
- [ ] All 4 credential leaks named
- [ ] Numbers 79/168 cited
- [ ] Audit fb2b81f + token-cap fix e03a52a cited

## Deliverables (paths)

- `docs/REMAINING-WORK-INVENTORY-2026-09-01.md`
- `tests/test_inventory_p0_claim.py`

## Verification

```bash
# See progress.md for verification output
```
