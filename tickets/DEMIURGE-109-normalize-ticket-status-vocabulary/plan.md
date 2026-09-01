# DEMIURGE-109: normalize-ticket-status-vocabulary

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

One vocabulary: planned|active|blocked|done|dropped. Single location (tracker.md). Status checker script.

## Acceptance criteria

- [ ] Each ticket has status in tracker.md (planned|active|blocked|done|dropped)
- [ ] scripts/ticket-status.py --check exits 0; --summary shows N/N with status
- [ ] Legacy vocabulary mapped (complete -> done, etc.)

## Deliverables (paths)

- `scripts/ticket-status.py`
- `All 81 tickets normalized`

## Verification

```bash
# See progress.md for verification output (once started)
```
