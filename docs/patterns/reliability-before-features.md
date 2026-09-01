---
pattern: reliability-before-features
one_liner: Flakiness, not capability, is the enemy — a system that sometimes works is harder to improve than one that reliably fails.
source: obra/agent-building-playbook
status: adopted
adopted: 2026-09-01
aiw_implements: ✓
related_files:
  - /opt/data/agents/tests/run-all.sh
  - /opt/data/agents/docs/adr/0001-adopt-agents-md-methodology-layer.md
dimensions: [meta-principles, reliability]
---

# Fix Reliability Before Features

> Source: [`obra/agent-building-playbook/reliability-before-features.md`](https://github.com/obra/agent-building-playbook/blob/main/patterns/reliability-before-features.md)
> Adapted for AIW org's specific stack.

## What it is

The instinct to add capabilities before fixing reliability is almost always wrong. A system that succeeds 70 percent of the time is not a 70-percent solution — it is an unreliable system that produces unreliable data, unreliable user trust, and unreliable signal for further improvement. Flakiness masks every other problem: you cannot tell whether a prompt change helped or hurt if the baseline is already noisy. A system that reliably fails is infinitely more useful than one that intermittently succeeds, because reliable failure is measurable, diagnosable, and improvable.

## When to reach for it

- Before adding any new capability, confirm the existing capabilities run cleanly and repeatably.
- When an eval or workflow shows high variance across runs with no change in inputs — fix that before moving on.
- When stakeholders are asking for more features and the current system is already flaky — the conversation about reliability must come first.
- After any infrastructure change: verify reliability has not regressed before building on top.

## When NOT to

- Early prototyping where the goal is to discover what is even possible — some flakiness is acceptable when you are still exploring the problem space.
- When reliability requires infrastructure that doesn't exist yet and the prototype is strictly time-boxed — but document the debt and plan to pay it.

## AIW-specific adoption

AIW's `tests/run-all.sh` is the canonical reliability gate. The standing rule:

> **Before adding a new feature (plugin, skill, agent PROMPT.md, or change to `scripts/*.py`), `tests/run-all.sh` must be green.**

This rule is enforced by:
- **AGENTS.md §"Before declaring work done"** — "Run the FULL verification command, confirm all green."
- **ADR-0001** — the methodology layer that established the rule
- **`scripts/eval-gate-enforce.py`** — automated enforcement for changes

If the gate is flaky (a test that fails ~5-10% of runs), fixing that flakiness is **higher priority** than adding any new feature.

## AIW's current reliability state

| Component | Reliability status |
|---|---|
| `tests/test_router.py` (23 tests) | ✓ Green (sometimes 1 flaky on order) |
| `tests/test_circuit_breaker.py` (10 tests) | ✓ Green |
| `tests/test_hard_stop_wrapper.py` | ⚠️ 1 known-flaky test (`test_check_action_mixed_blacklist_and_whitelist`) — should be fixed |
| `tests/test_signal_queue.py` | ✓ Green |
| `tests/test_eval_gate_enforce.py` | ✓ Green |
| `tests/run-all.sh` aggregate | 217/217 passing on first try this session |

## Next concrete steps

1. **Fix the flaky `test_check_action_mixed_blacklist_and_whitelist`** — this is a real bug (whitelist mode ignores `require_approval` per the test's expectation). Should be fixed in `patterns/hard-stop-wrapper.py` to make whitelist mode truly default-deny.
2. **Add a `tests/test_chronos.py`** — chronos time-awareness functions added in this session don't have unit tests yet. They're tested manually via `pre_dispatch_check` but not in isolation.
3. **Add a `tests/test_agent_tracer_fixes.py`** — verify the 3 bug fixes from Round 1 are still working (main() is called, rglob finds nested agents, suffixed date stems parse).
4. **Stand up an eval-driven-development workflow** — before any new PROMPT.md, write 3-5 pressure scenarios that test it.

## Related AIW files

- `/opt/data/agents/tests/run-all.sh` — the canonical reliability gate
- `/opt/data/agents/docs/adr/0001-adopt-agents-md-methodology-layer.md` — the methodology layer that established the rule
- `/opt/data/agents/docs/HANDOFF.md` — current state, includes "How to verify" section
- `/opt/data/agents/AGENTS.md` §"Before declaring work done" — the rule itself

## Related playbook patterns

- `fail-loud-harnesses.md` — how the harness behaves when things fail
- `demand-independent-proof.md` — how to verify beyond self-reports
- `verify-independently.md` — independent verification pattern
- `standing-eval-capability.md` — making evals a standing capability (not one-time)
- `eval-driven-development.md` — using evals to drive development
- `prove-on-small-sample.md` — run on 2 before 20
