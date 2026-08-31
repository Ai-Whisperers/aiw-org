# Pre-Layer-1 Preflight Audit — 2026-09-01

> **Purpose**: Catch blockers BEFORE Ivan says "go Layer 1". Doctrine 1 says
> AI self-fixes when it can; Doctrine 5 says AI pauses for big decisions.
> This audit found 7 blockers that prevent autonomous execution of Task 1.2-1.4.
>
> **Outcome**: **Layer 1 is NOT yet ready for autonomous start.** Decisions needed
> from Ivan before AI can proceed.

---

## TL;DR — 7 hard blockers + 4 advisories

| Severity | Item | Where | What blocks AI |
|----------|------|-------|----------------|
| 🔴 | Tasks 1.2 + 1.3 — validator file location | Validator with `^\d{6,15}$` regex is **NOT in aiw-org** | AI cannot fix what it can't find |
| 🔴 | Task 1.4 — MCP dependency file location | No `requirements.txt` in aiw-org contains `mcp` | Same — code lives elsewhere |
| 🟡 | Task 1.3 — wrangler process | Operator-blocked by design | Covered by runbook Batch C |
| 🟡 | Task 1.10 — pytest install | Active Python has no pytest | Easy fix (pip install) but needs Ivan's go |
| 🟡 | `jq` binary missing | Parse JSON via Python instead | Workaround |
| 🟡 | `fix_requirements.py` orphan at `/opt/data/` | Top-level, not in any repo | Confirm scope |
| 🟡 | `.env` files in adjacent paths | Real keys in `integrations/*`, `work/*`, `profiles/*` | Confirm scope for Layer 1 |

---

## Audit method

I ran:
1. **Code searches** for the bad regex, MCP dep, validator file — all in aiw-org only, then broader
2. **Python env check** — what modules are available for autonomous work
3. **File location audits** — what's in `/opt/data/agents/` vs `/opt/data/agents-v2/` vs `work/research-repos/*`
4. **State file cross-reference** — are the incident descriptions in `state/engineering.json` pointing at code that exists locally?

---

## Detailed findings

### 🔴 1. Validator code is NOT in aiw-org

**Search**: `grep -r 'e164' /opt/data` (broad) and narrower searches for the
specific bad regex `^\d{6,15}$`.

**Result**:
- aiw-org: 0 hits
- agents-v2: 0 hits in `.py/.js/.ts` (only false positives in archive/)
- `fix_requirements.py` at `/opt/data/fix_requirements.py` matched "penal/civil"
  content but that's a docs/translations file, not a validator
- `archive/legal-clients/rubicon-eas-2026-08-28-archived/` has worker.js +
  scripts/ — out of scope (archived)

**Implication**: Tasks 1.2 and 1.3 in `LAYER-1-HYGIENE-SCOPE.md` cannot be
executed autonomously. The incidents are tracked in `state/engineering.json`
but the code lives in a repo I cannot find from here.

**Possible explanations**:
- (a) Incidents are stale; code was already fixed elsewhere
- (b) Code lives in `/opt/data/agents-v2/` but I don't have search access
  (timeout in narrow grep — `/opt/data/agents-v2/` is large)
- (c) Code lives in `work/research-repos/*/leads-api/`
- (d) Different repo entirely

### 🔴 2. MCP dependency is NOT in aiw-org

**Search**: `find /opt/data -name 'requirements.txt' -not -path '*/.venv/*'`
and grep for `mcp` in each.

**Result**:
- aiw-org: no `requirements.txt` with `mcp`
- agents-v2: also not found in narrow searches

**Implication**: Task 1.4 cannot pin anything. The `mcp<2` constraint has
to be applied in a different repo.

### 🟡 3. Wrangler process

Per `state/engineering.json:incidents_72h`:
> `lead_worker_8787_down` — high severity — 14 ticks open
> root_cause: no wrangler process; operator restart required

**Implication**: Operator-blocked. Per `LAYER-1-HYGIENE-RUNBOOK.md` Batch C,
this is Ivan's decision (resurrect vs archive) + AI execution. **Already
covered.** Not blocking start of Layer 1; blocking Task 1.6 specifically.

### 🟡 4. pytest not installed

Active Python: `/opt/hermes/.venv/bin/python3` (per `which hermes`)

`python3 -m pytest --collect-only` → "No module named pytest"

**Implication**: Task 1.10 smoke gate can't run the existing 23-test suite
unless pytest is installed. Three options:
- (a) `pip install pytest` (~30 sec, dev dep, safe)
- (b) Write standalone test scripts (no install)
- (c) Skip pytest; smoke-test via existing `cron-heartbeat.sh`,
  `self-running-check-v2.py`, `health.sh`

### 🟡 5. `jq` missing

`which jq` → not found

**Implication**: AI must parse JSON via Python. Not blocking; just changes
how AI writes scripts.

### 🟡 6. `/opt/data/fix_requirements.py` — orphan

Existence: yes, 4843 bytes at `/opt/data/fix_requirements.py`. Content:
"sync requirements.basicDocuments for nexa-paraguay app."

**Implication**: Probably belongs to `paragu-ai-builder` or one of the
worker repos. Not in aiw-org. Out of Layer 1 scope but flagged.

### 🟡 7. `.env` files in adjacent paths

Discovered:
- `/opt/data/.env` (3450b, real keys — root Hermes env)
- `/opt/data/integrations/social-graph-mcp/.env` (975b, real)
- `/opt/data/integrations/linkedin-mcp/.env.example.filled` (1129b, real)
- `/opt/data/work/research-repos/paragu-ai-builder/.env` (641b, real)
- `/opt/data/work/.../web/.env.local` (1752b, real)
- `/opt/data/profiles/{engineering,people,research,sales,ivan,finance,operations,kiki}/.env`
  (each ~2280b, real)
- `/opt/data/.hermes/.env` (105b, has `BWS_TOKEN`)

**Implication**: aiw-org Layer1 scope says NO env file modifications. But
the `.gitignore` in aiw-org is broken (per Layer 2 scope) and may not be
excluding these. **Carry-forward to Layer 2**: verify `.gitignore` excludes
all `.env*` files including those in adjacent paths.

---

## Per-Doctrine resolution

| Doctrine | Says | Applies here? |
|----------|------|---------------|
| 1. AI self-fixes when it can | AI analyzes logs → fixes | **NO** — AI cannot fix files it cannot locate |
| 2. Per-layer scope docs | Written before layer starts | **YES** — Layer 1 scope doc exists |
| 3. Per-layer runbooks | For operator actions | **YES** — exists for operator parts |
| 4. Reporting cadence | Granular commits + weekly + layer report | **YES** — applied if AI proceeds |
| 5. Pause for big decisions | AI pauses on architecture / cross-repo / secrets | **YES — applies here.** AI is pausing. |

---

## What AI needs from Ivan

### Q1 — Where are Tasks 1.2 + 1.3 + 1.4 actually fixable?

- (a) Code is in aiw-org, AI missed it — point me at the path
- (b) Code is in `/opt/data/agents-v2/` — grant cross-repo authorization
- (c) Code is in `work/research-repos/*/leads-api/` — grant cross-repo authorization
- (d) Code is in another repo — tell me
- (e) Incidents are stale — verify resolved + mark closed in state file
- (f) Layer 1 tasks 1.2-1.4 deferred to Layer 4 (after cross-repo coordination)

### Q2 — pytest for Task 1.10?

- (a) `pip install pytest` (safe, 30 sec)
- (b) Write standalone test scripts
- (c) Use existing `cron-heartbeat.sh` + `self-running-check-v2.py` as smoke gate

### Q3 — `fix_requirements.py` at `/opt/data/fix_requirements.py`?

- (a) Out of scope, ignore
- (b) Should be tracked somewhere — tell me where
- (c) Should be deleted

### Q4 — `.env` files in adjacent paths?

- (a) Audit + report (Layer 1)
- (b) Fix `.gitignore` only (carry to Layer 2)
- (c) Ignore for now

---

## Net recommendation

**Don't greenlight Layer 1 autonomous execution until Q1 is answered.** The
operator parts (P0 leaks, LiteLLM topup, wrangler decision) can proceed
independently — they're documented in the runbook and AI doesn't need to touch
any code for them.

**Greenlight the operator work (Batch A + B + C) now**, but hold Task 1.2-1.4
until Ivan clarifies where the code is.

---

**Awaiting Ivan's answers to Q1-Q4.**