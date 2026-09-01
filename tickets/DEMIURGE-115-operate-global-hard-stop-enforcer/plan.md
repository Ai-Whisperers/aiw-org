# DEMIURGE-115: operate-global-hard-stop-enforcer

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: Ivan

## Objective

Decide wire (invoke from cron exec) or delete (with rationale) for global-hard-stop-enforcer.py before any client instance.

## Acceptance criteria

- [ ] Operator-signed decision: WIRE / DELETE / DEFER
- [ ] If WIRE: invoke from cron execution path, scope to DESTRUCTIVE_ACTIONS only
- [ ] If DELETE: rationale documented (something else enforces it)
- [ ] If DEFER: timeline for re-evaluation

## Deliverables (paths)

- `scripts/global-hard-stop-enforcer.py (modified or removed)`

## Verification

```bash
# See progress.md for verification output (once started)
```
