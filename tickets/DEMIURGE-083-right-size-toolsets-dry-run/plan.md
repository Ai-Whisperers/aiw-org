# DEMIURGE-083: right-size-toolsets-dry-run

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Build scripts/right-size-toolsets.py that walks cron jobs, infers needed toolsets per cron prompt, prints diff. Dry-run only by default; --apply requires --force to write.

## Acceptance criteria

- [ ] scripts/right-size-toolsets.py shipped at 4939a1b
- [ ] tests/test_right_size_toolsets.py: 11 pass + 1 skipped (known heuristic limitation)
- [ ] Dry-run does NOT modify jobs.json (proven by hash check)
- [ ] --apply without --force exits non-zero
- [ ] Empirical output: 69 crons identified as 5-toolset, apply deferred until prompt bodies restored

## Deliverables (paths)

- `scripts/right-size-toolsets.py`
- `tests/test_right_size_toolsets.py`

## Verification

```bash
# See progress.md for verification output
```
