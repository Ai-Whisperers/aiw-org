# DEMIURGE-096: readme-counts-script-and-ci-check

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Build scripts/readme-counts.py that regenerates README counts from live state. Wire as a CI check.

## Acceptance criteria

- [ ] scripts/readme-counts.py: --check exits 0 if counts match, 1 otherwise
- [ ] README.md table counts match the actual measured values
- [ ] CI workflow runs readme-counts.py --check

## Deliverables (paths)

- `scripts/readme-counts.py`
- `README.md (corrected counts)`
- `.github/workflows/ci.yml (calls --check)`

## Verification

```bash
# See progress.md for verification output (once started)
```
