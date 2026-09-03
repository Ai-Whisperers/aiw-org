#!/usr/bin/env python3
"""token-cap.py — DEPRECATED; replaced by gated-token-check.py.

Phase 9 R3 / Tier B1 originally replaced cost-cap.py (which measured dollars
on a flat-rate plan → could never fire).

The replacement is itself broken. Per WS-2 item 3 of the Phase Kernel brief
(commit fb2b81f audit): "Fix token-cap.py's unit mismatch (9,000,891 vs a
50,000 limit) or disable it. A gate comparing incompatible units is worse
than no gate -- check whether it has caused failures blamed on something
else."

The bug: token-ledger.json accumulates test events from validator runs with
unrealistically large credit values (e.g. 999999 per event). token-cap.py
sums these with no unit normalization, producing numbers like 9,000,891
that always exceed its 50000 budget. The cron aiw-token-cap-daily therefore
'fires' every day, but the fire is meaningless -- it claims a budget overrun
based on test data, not real usage.

This file is retained as a one-line wrapper that exits 0 with a clear
log message. The replacement (gated-token-check.py, separate commit) uses
a different gating model once token-ledger is wired into the scheduler.

Why we ship this fix as one commit:
- A daily cron entry that 'fires' with a fake alert is worse than no
  alert at all, because operators stop trusting the channel.
- The current state (8888888 > 50000 every day) makes a token-budget
  appear broken when it isn't.
- Disabling it does NOT remove the cron; the cron will call the disabled
  script and exit 0, which is a valid cron success.

Tests in tests/test_token_cap_disabled.py verify exit 0 + advisory message.
"""
import sys

BANNER = (
    "[token-cap] DISABLED: unit-mismatch with token-ledger (per docs audit "
    "fb2b81f). Replacement logic is gated-token-check.py. This cron slot "
    "will exit 0 daily until replacement ships."
)


def main() -> int:
    print(BANNER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
