# DEMIURGE-094: audit-state-write-trust-window

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Identify which agents ran between commit fffd7c4 (~21:00 UTC 2026-09-01) and commit 320ffdc (restore ~mid-day 2026-09-02). For each: what state did it write and is that data still trustworthy.

## Acceptance criteria

- [ ] Time window identified: fffd7c4..320ffdc (~16 hours)
- [ ] Per-agent execution log retrieved (from agent-traces.jsonl or equivalent)
- [ ] Per-write assessment: trustworthy / degraded / untrustworthy
- [ ] Rollback protocol for untrustworthy writes (recommend)

## Deliverables (paths)

- `analysis/STATE-WRITE-TRUST-WINDOW-2026-09-01.md`

## Verification

```bash
# See progress.md for verification output (once started)
```
