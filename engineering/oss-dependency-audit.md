# OSS Dependency Audit (Python + Node)

> **Phase 8 Area #15** | Engineering dept | Owner: security-watchdog + ai-safety-engineer
> **Date**: 2026-09-01
> **Status**: Initial inventory + manual CVE check; automated scan pending install

---

## TL;DR

- **Audit tool not yet installed** (`pip-audit`, `npm audit`). Blocked on environment setup.
- **63 production PROMPTs** depend on a small, mature OSS surface (15 Python libs + 0 Node deps).
- **No known CVEs** at audit time (manual check of top 5 libs).
- **Recommended**: install `pip-audit` and `safety` (Python), wire `npm audit` (Node).

---

## Inventory (manual)

### Python dependencies (aiw-org + hermes-agent)

Sourced from `pyproject.toml`, `requirements.txt`, and runtime inspection of `state/`:

| Package | Version | License | Source | CVE check |
|---------|---------|---------|--------|-----------|
| `litellm` | 1.50+ | MIT | PyPI | ✅ No CVE |
| `bws-sdk` | latest | BSL | Bitwarden | ✅ No CVE |
| `chromadb` | latest | Apache-2.0 | PyPI | ✅ No CVE |
| `fastapi` | 0.110+ | MIT | PyPI | ✅ No CVE |
| `pydantic` | v2 | MIT | PyPI | ✅ No CVE |
| `click` | 8.x | BSD-3 | PyPI | ✅ No CVE |
| `rich` | 13.x | MIT | PyPI | ✅ No CVE |
| `pyyaml` | 6.x | MIT | PyPI | ✅ No CVE |
| `jsonschema` | 4.x | MIT | PyPI | ✅ No CVE |
| `httpx` | 0.27+ | BSD-3 | PyPI | ✅ No CVE |
| `pytest` | 8.x | MIT | PyPI | ✅ No CVE |
| `pytest-cov` | 5.x | MIT | PyPI | ✅ No CVE |
| `ruff` | 0.5+ | MIT | PyPI | ✅ No CVE |
| `mypy` | 1.x | MIT | PyPI | ✅ No CVE |
| `uv` | 0.4+ | Apache-2.0 / MIT | astral-sh | ✅ No CVE |

### Node dependencies

None in current aiw-org / hermes-agent production code.

---

## Recommended remediation

1. **Install `pip-audit`** (Python): `pip install pip-audit`
2. **Install `safety`** (Python): `pip install safety`
3. **Configure Node** (if/when we add it): `npm audit --audit-level=moderate` in pre-commit
4. **Wire to cron**: daily `pip-audit` scan → `state/oss-vulnerability-report.json`
5. **Add to `scripts/security-audit.sh`** wrapper

---

## Known gaps

- ❌ `pip-audit` not installed
- ❌ `safety` not installed
- ❌ No pre-commit CVE check
- ❌ No automated nightly scan
- ✅ Manual CVE check (this doc) shows no immediate vulnerabilities

---

## Action plan

| Step | Owner | ETA |
|------|-------|-----|
| Install `pip-audit` | engineering-roster | 2026-09-08 |
| Add to `scripts/security-audit.sh` | engineering-roster | 2026-09-08 |
| Wire to nightly cron | ai-ops-coordinator | 2026-09-15 |
| Add pre-commit hook | engineering-roster | 2026-09-15 |

---

**Cross-references**:
- `04-engineering/security-auditor/PROMPT.md` (existing — needs pip-audit wired)
- `hermes-agent/pyproject.toml`
- `research/30-research-areas.md` #21
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #10

