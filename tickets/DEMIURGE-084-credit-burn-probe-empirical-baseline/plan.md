# DEMIURGE-084: credit-burn-probe-empirical-baseline

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Build scripts/credit-burn-probe.py that reads agent-traces.jsonl as the empirical source, with --start/--status/--stop lifecycle protocol.

## Acceptance criteria

- [ ] scripts/credit-burn-probe.py shipped at 3ccc244
- [ ] tests/test_credit_burn_probe.py: 16 pass
- [ ] --report shows structured output (header + total events + per-model breakdown)
- [ ] Empirical default: 113 events / 1.8M tokens / $0.00 cost (all model='estimated' = unknown)

## Deliverables (paths)

- `scripts/credit-burn-probe.py`
- `tests/test_credit_burn_probe.py`

## Verification

```bash
# See progress.md for verification output
```
