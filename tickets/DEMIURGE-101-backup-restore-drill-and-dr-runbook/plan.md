# DEMIURGE-101: backup-restore-drill-and-dr-runbook

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Backup infrastructure + DR runbook. Test restore.

## Acceptance criteria

- [ ] Nightly backup script (e.g. to BWS-backed storage)
- [ ] Outbox retention policy implemented (>90 days archive)
- [ ] docs/DR-RUNBOOK.md written with measured RTO
- [ ] One restore drill completed and documented

## Deliverables (paths)

- `scripts/backup.sh`
- `docs/DR-RUNBOOK.md`

## Verification

```bash
# See progress.md for verification output (once started)
```
