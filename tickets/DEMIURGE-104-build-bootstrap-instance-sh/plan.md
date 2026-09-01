# DEMIURGE-104: build-bootstrap-instance-sh

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Implement bootstrap-instance.sh from kernel/ design §4. Smoke-test 5 steps must all exit 0 on a clean machine.

## Acceptance criteria

- [ ] scripts/bootstrap-instance.sh shipped
- [ ] Smoke test 1: lint passes on /opt/data/instances/saskia
- [ ] Smoke test 2: state validates against schema
- [ ] Smoke test 3: no /opt/data/agents/ references in instance
- [ ] Smoke test 4: Hermes dry-run schedules generated
- [ ] Smoke test 5: eval gate synthetic cases pass

## Deliverables (paths)

- `kernel/scripts/bootstrap-instance.sh`

## Verification

```bash
# See progress.md for verification output (once started)
```
