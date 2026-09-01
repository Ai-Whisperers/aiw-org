# DEMIURGE-090: disable-broken-token-cap-py

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: AI

## Objective

Ship a wrapper that exits 0 daily with clear advisory banner citing audit. Test it doesn't write fake alerts.

## Acceptance criteria

- [ ] scripts/token-cap.py: minimal banner script, no json/datetime imports
- [ ] tests/test_token_cap_disabled.py: 7 pass
- [ ] Live host: exits 0, no coord.json writes
- [ ] Replacement gated-token-check.py is a separate commit (pending WORK-FLEET-2)

## Deliverables (paths)

- `scripts/token-cap.py`
- `tests/test_token_cap_disabled.py`

## Verification

```bash
# See progress.md for verification output
```
