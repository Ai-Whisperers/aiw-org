# DEMIURGE-098: paths-aiw-root-env-var-threading

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Replace every hardcoded /opt/data reference in scripts/tests/patterns with AIW_ROOT-derived paths. Commit in batches by directory per R8.

## Acceptance criteria

- [ ] scripts/_paths.py created with AIW_ROOT + STATE + AGENTS + HERMES + WORK constants
- [ ] 111 /opt/data refs reduced to 0 (excluding _paths.py)
- [ ] Commits in batches by directory (R8: small commits, one verifiable claim)
- [ ] Behavioral equivalence: scripts still work with AIW_ROOT=/opt/data default

## Deliverables (paths)

- `scripts/_paths.py`
- `111 files threaded (in batches)`

## Verification

```bash
# See progress.md for verification output (once started)
```
