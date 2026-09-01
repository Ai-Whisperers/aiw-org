# DEMIURGE-084 Progress

- Commit 3ccc244 shipped 2026-09-01: feat(scripts): add credit-burn-probe.py
- 16 tests pass (lifecycle + pricing + CLI)
- Empirical baseline confirms 100x cost-tracker disagreement documented in fb2b81f audit
- Live: agent-traces.jsonl has 18 events of which 16 are test runs (credits 100 or 999999); only 2 are real cron data
