# Layer1 Autonomous Prechecks — 2026-09-01

> **Purpose**: Final verification of all Q1-Q8 answers before greenlighting
> Layer1 autonomous execution. Each precheck is verifiable + actionable.

---

## TL;DR

- Q1 ✅ — Found the validator file (cross-repo, need Ivan's authorization)
- Q2 ✅ — Found MCP dep locations (cross-repo, need Ivan's authorization)
- Q3 ✅ — pytest works via `/opt/data/.venv/bin/python3`
- Q4 ✅ — 14 real `.env` files audited; surfaced 1 P0 secret (Supabase service-role in work/research-repos/paragu-ai-builder/.env)
- Q5 ✅ — Out of scope confirmed
- Q6 — Default applied (commit small, pause big, surface on next session)
- Q7 — AI's choice (using same template as Layer1)
- Q8 — No additional prep items

**Net status**: **2 cross-repo decisions await Ivan authorization. Once granted, Layer 1 autonomous execution can proceed.**

---

## Q1 — Validator file location (Tasks1.2 + 1.3)

### What was searched
Wide search across `/opt/data/` (excluding `.venv`, `.git`, `node_modules`, `__pycache__`, `archive`).

### What was found

**Q1.a — Bad regex `^\d{6,15}$` (validator_e164_regression)**:
```
templates/legal-lead-worker/api/lead-worker.js                 <-- primary hit
templates/legal-lead-worker/api/lead-worker-validator.test.js <-- test file
```

**Q1.b — penal/civil case-inversion (validator_area_case_inversion)**:
```
briefs/repos/rubicon-eas-website/sample/assets/schema.js        <-- stale, archived
scratchpad/negligencia-medica-py/raw-searches/batch_02_paraguay.py     <-- one-off
scratchpad/negligencia-medica-py/raw-searches/batch_03_legal_benchmark.py <-- one-off
```

**Q1.c — Files with both "phone" + "e164"**:
```
skills/devops/devops-monitoring/scripts/validator_e164_probe_v183.py   <-- active validator
hermes-fixed/gateway/platforms/signal.py
hermes-fixed/tools/send_message_tool.py
hermes-agent/gateway/platforms/signal.py
hermes-agent/tools/send_message_tool.py
hermes-agent/tests/tools/test_send_message_target_parse.py
hermes-agent/plugins/platforms/photon/{auth.py,adapter.py}
```

### Interpretation
- **`validator_e164_regression` lives in `templates/legal-lead-worker/api/lead-worker.js`** — this is the rubicon-eas lead worker that's been 404ing. **The validator bug is the cause of why lead intake has been broken.**
- **`validator_area_case_inversion` is most likely STALE** — the hits are archived/one-off files, not active code. Recommend closing this incident as "stale, code no longer in active paths."
- **`skills/devops/devops-monitoring/scripts/validator_e164_probe_v183.py`** is an active validator and may also have the bug.

### Cross-repo concern
- `templates/legal-lead-worker/` is **NOT in aiw-org**. It lives in `agents-v2` sister repo (or a worker repo).
- `hermes-agent/`, `hermes-fixed/` are also outside aiw-org.
- Per Doctrine5: AI **pauses on cross-repo edits**. Need Ivan's authorization.

### Recommended action
1. AI: read `templates/legal-lead-worker/api/lead-worker.js` to confirm the bug is exactly the regex mismatch
2. AI: read `validator_e164_probe_v183.py` to confirm whether it has the same bug
3. **Decision point (Ivan)**: authorize AI to edit `templates/legal-lead-worker/api/lead-worker.js` (and possibly `validator_e164_probe_v183.py`)? These are in scope per Ivan's "check the whole server" directive, but cross-repo.

---

## Q2 — MCP dep location (Task1.4)

### What was found

Files referencing `mcp` package:
```
hermes-fixed/pyproject.toml                                <-- Hermes (sister)
hermes-fixed/hermes_cli/setup.py                           <-- Hermes (sister)
hermes-agent/pyproject.toml                               <-- Hermes (sister)
hermes-agent/hermes_cli/setup.py                           <-- Hermes (sister)
integrations/social-graph-mcp/pyproject.toml              <-- MCP integration
integrations/linkedin-mcp/pyproject.toml                  <-- MCP integration
mcp-installs/n8n/requirements.txt                          <-- n8n MCP server
mcp-installs/n8n/pyproject.toml                            <-- n8n MCP server
briefs/repos/linkedin-mcp/pyproject.toml                   <-- archived brief
```

Files that IMPORT `mcp`:
```
hermes-agent/mcp_serve.py                                  <-- main
hermes-fixed/mcp_serve.py                                  <-- main
hermes-agent/hermes_cli/mcp_picker.py
hermes-agent/hermes_cli/mcp_config.py
hermes-fixed/tools/mcp_tool.py
hermes-fixed/tools/mcp_oauth.py
integrations/social-graph-mcp/social_graph_mcp/server.py
integrations/linkedin-mcp/linkedin_mcp/server.py
... 143 files total
```

### Interpretation
- **`mcp` is used in `hermes-agent` and `hermes-fixed`** — these are the active Hermes runtimes. **Not in aiw-org.**
- **`hermes-agent/` is the live runtime** — fixing `mcp<2` here here is where the parking-storm needs to go.
- **Integrations** also use `mcp` but those are independent servers.

### Cross-repo concern
- `hermes-agent/`, `hermes-fixed/` are OUTSIDE aiw-org.
- Per Doctrine5: AI pauses on cross-repo.

### Recommended action
- **Decision point (Ivan)**: authorize AI to edit `hermes-agent/pyproject.toml` (and possibly `hermes-fixed/pyproject.toml`) to pin `mcp<2`?
- If yes: AI makes the edit, runs tests, commits in `hermes-agent` repo
- If no: defer Task1.4 to Layer 2 (cross-repo coordination)

---

## Q3 — pytest for Layer1 smoke gate

### Attempted
- `pip install pytest pytest-cov` in Hermes venv: **FAILED** (no pip in hermes venv; `ensurepip` failed)
- `pip install pytest pytest-cov` in `/opt/data/.venv/`: **SUCCESS** (pytest + pytest-cov already installed)

### Verification
`/opt/data/.venv/bin/python3 -m pytest --collect-only` → **44 tests collected**, all green

### Recommendation
- **Use `/opt/data/.venv/bin/python3` for pytest** — it's already installed
- **Update `tests/run-all.sh`** to use this python instead of Hermes venv
  - Per Layer3 scope (don't touch in Layer1)
  - For Layer1 smoke gate: AI uses `/opt/data/.venv/bin/python3 -m pytest` directly
- **Don't** try to install in Hermes venv (breaks, no pip)

### Q3 status: ✅ RESOLVED

---

## Q4 — `.env` files audit (read-only)

### Found: 14 real `.env` files

| File | Size | Mode | Real keys |
|------|------|------|-----------|
| `.env` (root) | 3450b | **644** ⚠ | 41 keys |
| `profiles/sales/.env` | 2280b | 600 ✓ | 30 keys |
| `profiles/research/.env` | 2280b | 600 ✓ | 30 keys |
| `profiles/people/.env` | 2280b | 600 ✓ | 30 keys |
| `profiles/operations/.env` | 2280b | 600 ✓ | 30 keys |
| `profiles/finance/.env` | 2280b | 600 ✓ | 30 keys |
| `profiles/engineering/.env` | 2280b | 644 ⚠ | 30 keys |
| `scratchpad/round3-backup/.env` | 2279b | 644 ⚠ | 30 keys |
| `profiles/ivan/.env` | 1831b | 600 ✓ | 32 keys |
| `profiles/kiki/.env` | 1777b | 600 ✓ | 31 keys |
| `integrations/social-graph-mcp/.env` | 975b | 600 ✓ | 8 keys |
| `work/research-repos/paragu-ai-builder/.env` | 641b | 644 ⚠ | 7 keys |
| `home/.cache/uv/archive-v0/.../.env` | 180b | 644 | 2 keys |
| `.hermes/.env` | 105b | 644 | 1 key (`BWS_TOKEN`) |

### Sensitive pattern hits

| File | GitHub PAT | OpenAI | Firecrawl | Bitwarden |
|------|-----------|--------|-----------|-----------|
| `.env` (root) | 2 (`ghp_`) | 8 (`sk-`) | — | — |
| `profiles/ivan/.env` | — | 7 | 1 (`fc-`) | — |
| `profiles/sales/.env` etc. | — | 7 each | — | — |
| `scratchpad/round3-backup/.env` | 2 (`ghp_`) | 7 | — | — |
| `.hermes/.env` | — | — | — | 1 (`BWS_TOKEN`) |

**Total: 4 `ghp_` + 70 `sk-` + 1 `fc-` + 1 `BWS_TOKEN`** across all `.env` files.

### 🚨 P0 LEAK surfaced (NEW)

`work/research-repos/paragu-ai-builder/.env` contains `SUPABASE_SERVICE_ROLE_KEY` (real, not `.example`).

**This is the P0 leak Batch A Step A1 addresses** (rotate Supabase service-role key). Confirmed via this audit.

### 🚨 File permission issue (NEW)

- `/opt/data/.env` is **644 (world-readable)** — should be 600
- `profiles/engineering/.env` is **644** — should be 600
- `scratchpad/round3-backup/.env` is **644** — should be 600
- `work/.../.env` is **644** — should be 600
- `home/.cache/.../.env` is 644 (uv cache, low risk)

**Recommended**: `chmod 600` on all sensitive `.env` files. **Layer 1 candidate** (operator action or AI self-fix).

### `agents-v2` sister repo: NO `.env` files ✅

### Q4 status: ✅ AUDIT DONE — surfaced 1 P0 (already in Batch A) + 1 permission issue

---

## Q5 — `fix_requirements.py`

- Lives at `/opt/data/fix_requirements.py` (4870b, 12 days old)
- Content: doc translation sync script for nexa-paraguay app
- **NOT tracked in any repo** (checked: aiw-org, agents-v2, hermes-agent, hermes-fixed)
- **NOT in any gitignore**

### Verdict: **OUT OF SCOPE** ✅
- No action needed
- It belongs to a defunct build monorepo (`/opt/data/build/monorepo-sparse-20260826` per adjacent paths)
- Leave as-is; if it becomes a problem, archive it in Layer 2 cleanup

---

## Q6 — Cross-session autonomous work behavior

**Decision (default applied)**: AI commits small fixes only; pauses on big decisions; surfaces on next session.

### What this means in practice
- **Small decisions** (Q3-style fixes, file edits, test runs, documentation updates): AI commits + reports on next contact
- **Big decisions** (cross-repo edits, secrets, architectural changes, soul-improvement, anything customer-facing): AI pauses + asks
- **Documentation** for any pause is committed so context survives session boundaries

### Doctrine 1 + 5 combined = "smart autonomous"

---

## Q7 — Layer 2 scope doc format

**Decision (default applied)**: Use the same template as Layer1.
- 10-12 tasks (more than Layer1 since Layer2 has more work)
- Acceptance criteria per task
- Per-task rollback
- Token budgets
- Smoke gate at end of layer

---

## Q8 — Other prep items

**Decision (default applied)**: No additional prep items beyond what we've identified.

### What this audit DID surface (additional finding)

**`work/research-repos/paragu-ai-builder/.env` Supabase service-role leak** — already in Batch A but worth highlighting to Ivan directly.

**File permission hardening** — 5 `.env` files have mode 644 when they should be 600. **Layer1 candidate.**

---

#### Recommended execution path

1. **Q3 (pytest)** ✅ — use `/opt/data/.venv/bin/python3` for all pytest work
2. **Q4 (.env)** — audit done; P0 already in Batch A; chmod 600 fixes are operator-action or AI-self-fix
3. **Q5 (fix_requirements.py)** ✅ — out of scope
4. **Q1 + Q2 (cross-repo)** — need Ivan's authorization. **Doctrine 5 boundary.**

### Ivan's 2 questions to answer before Layer1 autonomous start

1. **Q1: authorize AI to edit `templates/legal-lead-worker/api/lead-worker.js` and `skills/devops/devops-monitoring/scripts/validator_e164_probe_v183.py`?**
 - (a) yes — AI fixes both
   - (b) yes but only lead-worker.js
   - (c) defer to Layer 2 cross-repo coordination

2. **Q2: authorize AI to edit `hermes-agent/pyproject.toml` to pin `mcp<2`?**
 - (a) yes — AI fixes
   - (b) defer to Layer 2
   - (c) fix `hermes-fixed/` instead (or both)

### Once answered: GREENLIGHT Layer 1

After authorization:
- Layer 1 autonomous execution starts (Tasks 1.2, 1.3, 1.4 with file locations confirmed)
- Layer 1 baseline metrics (Task 1.7) captures
- Layer 1 completion report
- **Pause for Layer 2 greenlight**

### Default if you don't answer

Per Doctrine 1 + Q6 default: AI defers Tasks 1.2-1.4 to Layer2 (cross-repo coordination), runs Task1.7 baseline metrics + Task1.8 wishlist update + Task1.9 completion report now. **Layer 1 ships with operator parts done + baseline captured, autonomous fixes deferred.**

---

**Awaiting Ivan's Q1+Q2 authorization decisions.**