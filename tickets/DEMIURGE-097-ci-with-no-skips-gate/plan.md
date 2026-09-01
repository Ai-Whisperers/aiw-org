# DEMIURGE-097: ci-with-no-skips-gate

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Create .github/workflows/ci.yml with lint + pytest + 'skips fail the build' check + body-presence check.

## Acceptance criteria

- [ ] .github/workflows/ci.yml exists
- [ ] Skipped tests fail the build (a synthetic @skip added in a PR turns red)
- [ ] Lint, pytest, body check wired
- [ ] Runs on a PR: clean = green

## Deliverables (paths)

- `.github/workflows/ci.yml`

## Verification

```bash
# See progress.md for verification output (once started)
```
