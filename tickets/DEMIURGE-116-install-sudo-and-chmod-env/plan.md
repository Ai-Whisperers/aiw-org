# DEMIURGE-116: install-sudo-and-chmod-env

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: Ivan

## Objective

Operator-action: install sudo, chmod 600 on .env.

## Acceptance criteria

- [ ] sudo installed on host
- [ ] /opt/data/.hermes/.env chmod 600 (owner = root or hermes only)
- [ ] scripts/verify-hooks.sh added + run from smoke-test.sh

## Deliverables (paths)

- `(host-level changes)`

## Verification

```bash
# See progress.md for verification output (once started)
```
