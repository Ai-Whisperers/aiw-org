# Compliance Jurisdiction Matrix — PY / NL / EU / US

> **Phase 8 Area #17** | Finance & Legal dept | Owner: compliance-monitor + Ivan
> **Date**: 2026-09-01
> **Status**: Initial matrix; refresh on regulation change

---

## The 4 jurisdictions

AI Whisperers has presence (or plans) in:
1. **Paraguay** (EAS, primary ops)
2. **Netherlands** (Ivan's residence, AI Whisperers Europe)
3. **EU** (potential clients + AI Act scope)
4. **US** (trademark scope + Hostinger precedent)

---

## The matrix

| Regulation | Jurisdiction | Trigger | What we need to do | Status |
|------------|--------------|---------|---------------------|--------|
| **LGPD (Ley 1682/2001 + Decreto 10135)** | Paraguay | Any data processing | Data inventory, consent management, breach reporting | 🟡 Initial review |
| **AI Whisperers EAS registration** | Paraguay | Active business entity | Keep registration current, file annual reports | ✅ Active |
| **GDPR (Articles 5, 6, 9, 22, 32, 33)** | Netherlands / EU | Any EU personal data | Lawful basis, data subject rights, breach reporting (72h) | 🟡 Initial review |
| **EU AI Act (Articles 5, 6, 50, Annex III)** | EU | AI system provider | Conformity assessment, transparency, risk classification | 🔴 Researching |
| **Trademark (4 classes: 9, 35, 41, 42)** | US (USPTO) + PY + NL | Brand use in commerce | File, monitor, defend | 🟡 Hostinger issue ongoing |
| **NL KvK registration** | Netherlands | Active business | Keep registration current | ✅ Active |
| **NL WBTR (incoming)** | Netherlands | Active entity (2026) | Comply with new transparency rules | 🟡 Pending |

---

## Per-jurisdiction compliance status

### Paraguay

- ✅ EAS registered with MIC
- ✅ Annual filings current (need verification)
- 🟡 LGPD compliance: data inventory incomplete
- 🟡 Trademark filing status unknown (need to verify)

### Netherlands

- ✅ KvK registered
- ✅ BWS Vault used for credentials (compliance-friendly)
- 🟡 GDPR: data subject rights process not formalized
- 🟡 WBTR (2026): pending implementation

### EU (cross-cutting)

- 🔴 EU AI Act: scoping work needed (per `finance/eu-ai-act-coaching-compliance.md`)
- 🟡 GDPR: see above
- 🟡 Schrems-II: cross-border data transfer needs review

### US (trademark-only)

- 🟡 Trademark monitor: `trademark-scan-cron.json` (active but watch for false positives)
- 🟡 Hostinger trademark case: monitor ongoing

---

## Top 5 action items

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 1 | Verify LGPD data inventory complete | compliance-monitor | 2026-09-15 |
| 2 | Formalize GDPR data-subject-rights process | compliance-monitor | 2026-09-30 |
| 3 | EU AI Act scoping (Area #2 of finance catalog) | external legal counsel | 2026-10-15 |
| 4 | Verify NL WBTR 2026 compliance | compliance-monitor | 2026-12-31 |
| 5 | Trademark filing status (verify registered) | compliance-monitor | 2026-09-15 |

---

## What "compliant" means for us at $240 MRR

At our scale, full legal review is overkill. But we MUST:
1. Document data processing (even informally)
2. Have breach-response plan (even informal)
3. File trademarks in core classes
4. Comply with EU AI Act for any EU-deployed AI

---

**Cross-references**:
- `docs/THREAT-MODEL.md`
- `~/skills/trademark-compliance-scrub/`
- `research/STRATEGY.md` Part 5 (org setup)
- `state/trademark-scan-cron.json`
- `analysis/PHASE-7-dept-research/02-finance-legal-research-areas.md` Area #5

