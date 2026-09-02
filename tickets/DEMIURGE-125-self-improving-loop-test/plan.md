# DEMIURGE-125: self-improving-loop-test

**Sprint**: Phase Kernel
**Size**: 1h
**Owner**: AI

## Objective

Ship `tests/test_self_improving_loop.py` that proves the demiurge loop
runs end-to-end:
- Load instincts from YAML
- Curator-evolver produces proposals
- Homunculus validates and approves/rejects
- Round-trip integrity

## Acceptance criteria

- [ ] tests/test_self_improving_loop.py
- [ ] Tests run, no @unittest.skip (R1 compliance)
- [ ] Tests use tmpdir for state dirs (no production mutation)
- [ ] Tests verify: load → propose → validate → approve chain
- [ ] Tests verify: validation rejects bad proposals
- [ ] Tests verify: round-trip integrity (proposal JSON survives re-load)

## Verification

- New tests pass
- Full suite still 438+/5/1 (no regression)
- Lint still 77/0
