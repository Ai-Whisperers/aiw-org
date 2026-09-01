# Kernel Design — `aiw-org` as Instance Zero

> **Status**: Design (Phase "Kernel")
> **Date**: 2026-09-02
> **Supersedes**: prior WORK-PLAT-* ("Project inside aiw-org") plan
> **Frame**: `aiw-org` is **instance zero** of an instantiable org kernel. Saskia gets her own instance; AIW remains instance zero; the kernel is what both rest on.

---

## 1. What the kernel is and isn't

**IS** the kernel:
- The structural, language-agnostic scaffolding that lets a business stand up its own agent organization on its own Hermes instance: directory layout, schemas, department/agent/conversation definitions, cron conventions, hard-stop primitives, eval-gates, monitoring patterns, dispatch rules, security checks, the research methodology.
- A versioned artifact that lives at `kernel/` in this repo and is **extractable**: a fresh clone + `bootstrap-instance.sh <name>` produces a running skeleton.
- **Bound to Hermes** for runtime (cron executor, prompt assembly, state versioning), but not to AIW-specific content (department names, KPIs, agents).

**Is NOT** the kernel:
- AIW's six charter departments, KPIs, agent roster, research catalogs, board, or constitution.
- The cron jobs at `/opt/data/.hermes/cron/jobs.json` (those are instance data, not kernel).
- Saskia's restaurant departments, suppliers, or menu categories.
- The actual HERMES-FIXED runtime code (the engine is upstream; the kernel is the configuration and templates that run on it).

**The kernel provides STRUCTURE**. The CONTENT (departments, agents, prompts) is generated per business when the kernel is bootstrapped for that instance.

---

## 2. The kernel/ extraction — what's in, what's out

This is the inventory WS-5 step 1 demands. Done from existing repo contents.

### Kernel (generic, versioned)

| Asset | Why kernel | Source |
|---|---|---|
| `patterns/` (10 files) | Generic primitives: hard-stops, idempotency, context-payload, secret-leak, trademark-scrub, sqlite-schema | exists, often underused at instance scope |
| `prompts/PROMPT-TEMPLATE.md` | Canonical 12-section template; parameterizable per instance | exists |
| `schemas/` (17 files) | Generic payload schemas (agent, research, kpi, signals, etc.) — per-instance files override per-domain | exists |
| `demiurge/router/` | Dispatch and timing rules — engine-side, not AIW-specific | exists |
| Eval-gate machinery (`scripts/eval-gate-*`, `tests/test_eval_gate*`) | General scoring framework | exists |
| Cron conventions (`scripts/cron-*.py`, `tests/test_dept_monitor_thresholds.py`) | Cron health checks, overlap detection — generic | exists |
| `templates/` (AGENTS.md, README, .gitignore, pre-commit, install-hooks.sh) | Generic convention files | exists |
| `research/DEPT-RESEARCH-METHODOLOGY.md` | 7-question research template — used by every instance | exists |
| `tests/run-all.sh`, hermetic test infrastructure | Generic CI pattern | exists |
| `scripts/lint-prompts.py`, `scripts/validate-state.py` | Generic validation pass | exists |
| `scripts/_paths.py` (to be created in WS-3) | AIW_ROOT env var abstraction | not yet |
| `scripts/bootstrap-instance.sh <name>` | **NEW** — produces a running skeleton from kernel + instance inputs | not yet |

### Instance (AIW-specific; stays in `aiw-org-clone/`, not in kernel)

| Asset | Why instance |
|---|---|
| `01-operations/`, `02-finance-legal/`, `03-sales-growth/`, `04-engineering/`, `05-research-education/`, `06-people-culture/people-hr/` | The 6 charter departments — AIW-specific content |
| `demiurge/agents/*` (28 dirs) | AIW's agent roster |
| `demiurge/feedback-loops/soul-improvement.yaml` | AIW's adaptive layer (instance-specific) |
| `board/` | AIW's board-of-directors + risk register |
| `OPS-AGENTS.md`, `ORG-AGENTS.md`, `departments/*.md` | AIW's constitution + charters |
| Agent-specific `PROMPT.md` files (76 of them) | AIW agent content |
| `state/coord.json` | AIW's runtime state |
| `/opt/data/.hermes/cron/jobs.json` | AIW's cron registry |
| `analysis/`, `docs/HANDOFF.md`, `docs/REMAINING-WORK-INVENTORY.md`, `analysis/PHASE-*` | AIW-specific operational history |

The **split point**: the kernel holds WHAT an org looks like and HOW to manage it; AIW's repo holds AIW's CONTENT plus its copies of the kernel pieces it uses.

---

## 3. The kernel directory structure

```
kernel/
├── README.md                           # what the kernel is, version, how to bootstrap
├── CHANGELOG.md                        # semantic version
├── CONVENTIONS.md                      # 12-section PROMPT spec, hard-stops schema, etc.
├── patterns/                           # from AIW patterns/, de-AIW'd
│   ├── hard-stop-wrapper.py
│   ├── hardstop_check.py
│   ├── idempotency-check.py
│   ├── context-payload.py
│   ├── secret-leak-check.sh
│   ├── trademark-scrub.sh
│   ├── hard-stops-schema.md
│   ├── idempotency.md
│   └── sqlite-schema.md
├── schemas/                            # generic JSON schemas
│   ├── agent.schema.json
│   ├── coordination.schema.json
│   ├── department.schema.json
│   ├── signal.schema.json
│   ├── eval-gate.schema.json
│   └── … (per-domain schemas as separate files, not per-org)
├── scripts/                            # instance-bootstrap scripts
│   ├── bootstrap-instance.sh
│   ├── lint-prompts.py
│   ├── validate-state.py
│   ├── cron-diagnose.py
│   └── find_overlapping.py
├── research/
│   └── DEPT-RESEARCH-METHODOLOGY.md    # the 7-question template
├── templates/
│   ├── AGENTS.md.template
│   ├── PROMPT-TEMPLATE.md              # the canonical 12-section template
│   ├── README.md.template
│   ├── .gitignore.template
│   ├── pre-commit.template
│   └── install-hooks.sh
├── demiurge/
│   └── router/
│       ├── dispatch-rules.yaml         # generic rules (signal tags → recipients)
│       └── timing-rules.yaml
├── tests/
│   ├── run-all.sh
│   ├── test_lint_prompts.py
│   ├── test_validate_state.py
│   ├── test_idempotency.py
│   └── test_dispatch.py
└── docs/
    ├── HOST-ONLY.md.template
    ├── DR-RUNBOOK.md.template
    └── INSTANCE-LIFECYCLE.md
```

This is **what exists already, plus a directory move + de-AIW'ing**. No kernel code is written from scratch; it's extracted from AIW artifacts and parameterized.

---

## 4. The bootstrap protocol — `bootstrap-instance.sh <instance-name>`

The exit-criterion for WS-5 is that this script produces a running skeleton on a clean machine without `/opt/data/`.

```bash
#!/usr/bin/env bash
# bootstrap-instance.sh <instance-name> [--source <path-to-kernel>]
#
# Required: instance-name, --source (defaults to ./kernel)
# Output: a directory tree at /opt/data/instances/<instance-name>/
#         that runs a smoke test PASS without any AIW-specific paths.
```

### Inputs (the business's parameters)

```bash
# Either via flags or an interactive prompt
INSTANCE_NAME="saskia"
LEGAL_NAME="Saskia Café S.A."                 # for hard-stop disambiguation
OWNER_EMAIL="..."                             # OWNER-bound hard-stops
DEPARTMENTS=( "front-of-house" "kitchen" "supplier-relations" "marketing" "reputation" "bookkeeping" )
PROVIDER_PLAN="flat-rate"                     # hard rule: no pay-as-you-go
DEFAULT_MODEL="<concrete-id>"                 # not an alias; resolve before bootstrap
TIMEZONE="America/Asuncion"
```

### Output tree

```
/opt/data/instances/saskia/
├── README.md                                  # instance-specific overview
├── instance.yaml                              # the parameters above + kernel version
├── Hermes-cron.json                           # placeholder; populated after design
├── agents/<dept>/<agent>/PROMPT.md            # generated from PROMPT-TEMPLATE
├── departments/<dept>.md                      # charters
├── state/coord.json                           # empty {schema_version, events:[]}
├── outbox/<dept>/<agent>/                     # empty
├── logs/                                      # empty
├── docs/HOST-ONLY.md                          # declared host-only list
└── .hermes/                                   # Hermes runtime config (separate from AIW's)
```

### Smoke test (must PASS)

```bash
# 1. Lint passes
python3 <kernel>/scripts/lint-prompts.py --root /opt/data/instances/saskia

# 2. State validates against schema
python3 <kernel>/scripts/validate-state.py /opt/data/instances/saskia

# 3. All paths are inside /opt/data/instances/saskia (or ${AIW_ROOT}/instances/saskia)
grep -rl '/opt/data/agents/' /opt/data/instances/saskia  # returns 0 hits

# 4. Hermes dry-run: schedules generated, no actual calls
hermes cron --validate-only --config <instance>/Hermes-cron.json

# 5. Eval gate: synthetic pass/fail cases
python3 <kernel>/tests/test_eval_gate.py --instance saskia
```

### What it does NOT do

- Does not register crons against a live Hermes instance (operator step)
- Does not ship the kernel (must already exist at `--source`)
- Does not call out to any LLM provider
- Does not assume network
- Does not write to /opt/data/agents/ (AIW's tree)

---

## 5. The AIW-instance / kernel version contract

When the kernel improves, how does AIW (instance zero) get the improvement?

**Answer (v0.1)**: **Manually, via a re-extraction pass**. Real answer requires:

1. Kernel has `kernel/CHANGELOG.md` with semantic version.
2. AIW-instance records its kernel_version in `instance.yaml`.
3. A migration script `kernel/scripts/upgrade-instance.sh <instance-name>` exists that:
   - Diffs kernel files vs instance copies
   - Identifies changes (kernel-only, instance-overridden)
   - Applies kernel-side changes to instance copies
   - Leaves instance-overridden files alone
4. AIW runs `upgrade-instance.sh aiw` whenever it consumes a kernel release.

**For v0.1 (this phase)**: this is documented as a known gap. Real upgrade tooling is **not** in scope. The kernel extraction is the first time this becomes a forcing function.

---

## 6. What this kernel does NOT solve yet

Per the brief's R11 ("changes to this prompt's scope"):

- Hard-stops enforcement (the kernel ships the primitive; whether instances wire it is per-instance policy)
- Multi-instance coordination across instances (Saskia ↔ AIW check-in is application-layer, not kernel)
- Provider routing (kernel requires concrete model IDs, not opaque aliases)
- State-store choice (kernel assumes JSON files; SQLite migration would be per-instance opt-in)
- Kernel version-pinning in deployment (AIW currently consumes from the kernel as-code; no version bump mechanism yet)

These are documented as **kernel gaps** in `kernel/README.md` §Known Limitations so the next session knows.

---

## 7. Open questions for the next operator session

| Q | Why blocking |
|---|---|
| Should the kernel live in this repo (`aiw-org/kernel/`) or in a new repo (`aiw-org-kernel`)? | Affects CI, ownership, version visibility |
| Does `bootstrap-instance.sh` write to `/opt/data/instances/<name>/` by default, or require `--root`? | Affects multiple-machine deployment |
| How is the kernel version pinned in a deployed instance? | Affects upgrade-script correctness |
| Does the kernel include the `secret-leak-check.sh` and `trademark-scrub.sh` patterns, or are those per-instance? | Generic vs AIW-instance concerns |

These are **not blocking the design doc**; they are blocking the v0.2 kernel extraction. They go into the open-questions file for Ivan.

---

## 8. What this design does NOT promise

- That all AIW prompts can be sanitized and placed in the kernel. (AIW-shaped content stays in AIW; only the structural template does.)
- That a Saskia instance will deploy before this design is approved and the kernel v0.1 ships. (Deployment is WS-6 design-only.)
- That auto-upgrade works. (It doesn't yet.)

The kernel extraction **enables** Horizon-2. It does not **complete** it.
