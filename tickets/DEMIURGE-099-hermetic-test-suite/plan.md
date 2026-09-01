# DEMIURGE-099: hermetic-test-suite

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Make pytest runnable with AIW_ROOT=/nonexistent by populating tmp_path with minimal state fixtures.

## Acceptance criteria

- [ ] conftest.py fixture for AIW_ROOT tmp_path
- [ ] All 16 test files that hardcode /opt/data use the fixture
- [ ] AIW_ROOT=/nonexistent python3 -m pytest tests -q exits 0 with 0 skipped

## Deliverables (paths)

- `conftest.py`
- `16 test files (modified)`

## Verification

```bash
# See progress.md for verification output (once started)
```
