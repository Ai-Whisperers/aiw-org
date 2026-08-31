# MCP (Model Context Protocol) Maturity Tracking

> **Phase 8 Area #14** | Engineering dept | Owner: engineering-roster
> **Date**: 2026-09-01
> **Status**: First audit

---

## What MCPs does AI Whisperers depend on?

Audit of `hermes-agent/pyproject.toml` and runtime deps.

| MCP / Library | Purpose | Maturity | Lock-in risk | Action |
|---------------|---------|----------|--------------|--------|
| `litellm` | Multi-provider LLM routing | Stable (v1.50+) | Medium | Keep (multi-provider is the value) |
| `bws-sdk` (Bitwarden) | Secret retrieval | Stable | High (vendor lock) | Keep; alternative = HashiCorp Vault (cost >$1K/mo) |
| `chromadb` | Vector storage | Stable | Low | Keep (open-source, self-hostable) |
| `fastapi` | Web framework | Stable | Low | Keep (ubiquitous) |
| `pydantic` | Schema validation | Stable | Low | Keep (de facto standard) |
| `click` | CLI framework | Stable | Low | Keep |
| `rich` | Terminal UI | Stable | Low | Keep |
| `pyyaml` | YAML parsing | Stable | Low | Keep |
| `jsonschema` | Schema validation | Stable | Low | Keep |
| `httpx` | Async HTTP | Stable | Low | Keep |
| `pytest` + `pytest-cov` | Testing | Stable | Low | Keep |
| `ruff` | Linter | Stable | Low | Keep |
| `mypy` | Type checker | Stable | Low | Keep |
| `pre-commit` | Git hooks | Stable | Low | Keep |
| `uv` | Python packaging | Stable (0.4+) | Low | Keep (replacing pip+venv) |

---

## Lock-in analysis

| Risk | Mitigation |
|------|-----------|
| `litellm` | Can swap to direct provider SDKs if needed (high effort) |
| `bws-sdk` | BWS-compatible alternative = Vault (cost prohibitive). Accept risk. |
| `chromadb` | Can swap to Qdrant (open-source, similar API). |

**No critical lock-in identified.** All libraries have open-source alternatives.

---

## Pre-stable / experimental deps

None currently in production. (Note: Phase 4 explored `mem0` for memory; rejected as too unstable.)

---

## Recommendation

- **Annual review** of this list (next: 2027-09-01).
- **Quarterly news scan** for any `litellm` or `bws-sdk` breaking changes.
- **No action needed** for now.

---

**Cross-references**:
- `hermes-agent/pyproject.toml`
- `research/30-research-areas.md` #19 (technology trends)
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #9

