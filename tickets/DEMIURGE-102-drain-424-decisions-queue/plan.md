# DEMIURGE-102: drain-424-decisions-queue

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Categorize all 424 items: stale / duplicate / auto-resolvable / genuinely needs Ivan. Auto-close with written rules. Add priority, age, batching. Rate-limit agents. Deliver digest.

## Acceptance criteria

- [ ] Categorization complete: 424 items classified
- [ ] Auto-close rule per category documented
- [ ] Priority + age + batching added to schema
- [ ] Rate limit (N per agent per day) enforced
- [ ] Single digest delivered to Ivan
- [ ] Daily decision-generation rate measured

## Deliverables (paths)

- `analysis/DECISIONS-QUEUE-DRAIN-2026-09.md`
- `scripts/decisions-categorize.py`

## Verification

```bash
# See progress.md for verification output (once started)
```
