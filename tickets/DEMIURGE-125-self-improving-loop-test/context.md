# DEMIURGE-125 Context

**STATUS**: PENDING
**TITLE**: self-improving-loop-test
**OWNER**: AI
**SIZE**: 1h

## Focus

Per the David Ondrej analysis, AIW's self-improving loop is real
production code. The gap: NO test proves the loop runs end-to-end.

This ticket ships `tests/test_self_improving_loop.py` which exercises
the full pipeline:
1. Synthetic instinct YAML → curator-evolver → curation-proposal JSON
2. Curation-proposal → homunculus → approved or rejected
3. Round-trip: a proposal can be validated, approved, and read back

This is the "show your work" pattern from David's corpus applied to
AIW's own self-improving capability. Per AGENTS.md R1: tests must
run, not skip.
