# AI Safety Engineering — Current Posture (2026-09-01)

> **Phase 8 Area #7** | Engineering dept | Owner: ai-safety-engineer + engineering-roster + Kiki
> **Date**: 2026-09-01
> **Status**: 🔴 Multiple gaps identified; remediation in progress

---

## TL;DR — 5 safety gaps, 3 critical

| Gap | Severity | Description | Remediation |
|-----|----------|-------------|-------------|
| **G1: Hard-stops never invoked** | 🔴 CRITICAL | `patterns/hard-stop-wrapper.py` exists but 0 of 49 agents call it | Add wrapper to all agent execution paths |
| **G2: No eval-gate enforcement** | 🔴 CRITICAL | Agents run without pass-rate check at execution | Add eval check before agent invocation |
| **G3: Aggregate pass_rate not computed** | 🟠 HIGH | Per-agent eval data exists but no rollup | Implement `scripts/eval-aggregate-pass-rate.py` (this phase) |
| **G4: Compliance.json missing** | 🟡 MEDIUM | `security-watchdog` and `qa-automation-runner` monitor reference it | Use `coord.json:compliance_breaches[]` instead (already exists) |
| **G5: Heartbeat-alerts.json path wrong** | 🟡 MEDIUM | AI-ops-coordinator monitor references wrong path | Patched in Phase 6 |

---

## Gap details

### G1 — Hard-stops wrapper never invoked 🔴 CRITICAL

**The wrapper**: `patterns/hard-stop-wrapper.py` (~80 lines, Python).
**What it does**: Checks each agent action against a hard-stop list (read_state, write_state, disable_hardstop, modify_eval_gates). For each, requires approval based on USD threshold.
**Reality**: **0 of 49 agents invoke it.**

**Why this matters**: The Phase 1 L1 audit found that "hard-stops are 100% advisory." If an LLM call decides to write destructive state or send email without consent, nothing physically stops it.

**Files affected** (where hard-stops are documented but not enforced):
- Every dept-lead PROMPT.md's `hard_stops:` field (advisory only)
- `constitution/ORG-AGENTS.md` (decision rights matrix — advisory)

**Remediation**: Either invoke wrapper in agent execution paths, or remove the wrapper. Decision pending Kiki's review (engineering owner).

### G2 — No eval-gate enforcement 🔴 CRITICAL

**Current state**: `eval-gate-runner` agent monitors eval pass rates, but does NOT block execution when rates drop.
**Risk**: An agent with <50% pass rate continues running, producing low-quality output.
**Remediation**: Add eval check at agent invocation. If pass_rate < 0.5, escalate to Kiki/Ivan.

### G3 — Aggregate pass_rate not computed 🟠 HIGH

**Current state**: `state/eval-per-agent.json` has per-agent data; no aggregate.
**Remediation**: This phase implements `scripts/eval-aggregate-pass-rate.py` (Area #10).

### G4 — Compliance.json missing 🟡 MEDIUM

**Current state**: `security-watchdog` and `qa-automation-runner` reference `compliance.json` (doesn't exist).
**Remediation**: Use `coord.json:compliance_breaches[]` field instead. Patched in Phase 6.

### G5 — Heartbeat-alerts.json path wrong 🟡 MEDIUM

**Current state**: `ai-ops-coordinator/PROMPT-monitor.md` references `/opt/data/state/heartbeat-alerts.json` (doesn't exist).
**Remediation**: Patched in Phase 6 to use `/opt/data/agents/state/heartbeat-alerts.json`.

---

## Threat model coverage (vs `docs/THREAT-MODEL.md`)

| Threat actor | Defense | Status |
|--------------|---------|--------|
| Malicious external (trademark, host takeover) | Trademark-compliance-scrub cron | ✅ Active |
| Compromised internal credential | Bitwarden vault + cron secret rotation | ✅ Active |
| LLM prompt injection | Hard-stops wrapper | 🔴 Advisory only |
| Eval gate compromise | Aggregate pass_rate | 🟠 Partial |
| Internal unauthorized action | Decision rights matrix | 🟡 Advisory |
| Schema mutation attack | additionalProperties: false | ✅ Enforced |

---

## Recommendations

1. **Decide G1 remediation** (Kiki review): invoke wrapper globally, or remove it.
2. **Implement eval-gate enforcement** (G2): add pre-execution eval check.
3. **Run `scripts/eval-aggregate-pass-rate.py`** (this phase — Area #10).
4. **Quarterly safety posture review** (next: 2026-12-01).

---

**Cross-references**:
- `docs/THREAT-MODEL.md`
- `patterns/hard-stop-wrapper.py`
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (surprise #1, #2)
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #2
- `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md`

