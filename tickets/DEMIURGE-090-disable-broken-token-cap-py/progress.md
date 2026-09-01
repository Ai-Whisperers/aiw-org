# DEMIURGE-090 Progress

- Commit e03a52a shipped 2026-09-02: fix(scripts): disable broken token-cap.py + safety tests (WS-2 item 3)
- Per brief WS-2 item 3: 'fix token-cap.py unit mismatch (9,000,891 vs 50,000) or disable it. A gate comparing incompatible units is worse than no gate'
- Per the brief's 'or disable it': shipped wrapper that exits 0 daily with clear advisory banner
- tests/test_token_cap_disabled.py: 7 pass (safety contract)
- Live host synced: live token-cap.py now exits 0 with advisory banner, no coord.json writes
- Replacement gated-token-check.py is a separate commit, pending WORK-FLEET-2 (token-ledger scheduler instrumentation)
