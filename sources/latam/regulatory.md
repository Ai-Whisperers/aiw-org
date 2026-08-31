# Regulatory & Legal — PY Maquila + LATAM Data Privacy

> **Ticket**: DEMIURGE-065  
> **Status**: researched 2026-08-26  
> **Confidence**: medium — statutory refs verified; tax/maquila application requires accountant [NEEDS VERIFY]

## Executive summary

**Paraguay Maquila de Servicios** (Ley 7547/2025) now explicitly covers software/consulting exports — relevant for EU client billing. **Data privacy**: PY Law 1682 superseded by Ley 6534/2020 (credit data focus); general personal data law still evolving. **LATAM**: LGPD (BR), PDPA (AR), LFPDPPP (MX) apply when processing local residents' data. **Billing**: SIFEN mandatory e-invoice rollout. **No EU AI Act equivalent** in LATAM yet — opportunity window.

---

## Paraguay — Maquila regime

### Legal framework

| Instrument | Summary |
|------------|---------|
| **Ley 7547/2025** | New maquila law; replaces Ley 1064/97 |
| **Decreto 5714/2026** | Regulation [cited by RSM/Pasmor; verify publication] |
| **MIC / CNIME** | Administers programs via SIMEX on VUE platform |

### Maquila de Servicios (relevant to AI consulting export)

| Requirement | Detail |
|-------------|--------|
| Service nature | Provided from PY; consumed abroad; client not present in PY |
| Contract | Contrato de maquila with foreign principal/client |
| Export | Service export = moment of delivery to foreign client |
| Sectors | IT, software dev, BPO, professional consulting, remote services |
| Simplifications | No INTN industrial certification for service maquila |
| Invoicing | Electronic export invoice via DNIT |

### Tax treatment

| Item | Rate / rule | Source |
|------|-------------|--------|
| Maquila tax | **~1%** on added value or export invoice (greater of) | Multiple legal summaries |
| Substitutes | Other national taxes on maquila activity | Ley 7547 |
| Benefit duration | Up to **20 years** renewable | Legal summaries |

**[NEEDS VERIFY]** Confirm exact tax base and applicability to Ai-Whisperers structure with local accountant before relying on 1% rate.

### Application process

1. Constitute PY entity (S.A. / S.R.L.)
2. Prepare programa de maquila (technical memo, employment, export projection)
3. Submit via CNIME / VUE (SIMEX)
4. Obtain maquila program approval
5. Operate with differentiated accounting (NIIF)
6. Issue factura electrónica de exportación

**Timeline**: [NEEDS VERIFY] — allow 3–6 months for setup.

---

## Paraguay — Data privacy

| Law | Status | Scope |
|-----|--------|-------|
| **Ley 1682/2001** | **Derogated** by Art. 30 Ley 6534/2020 | Was general private information |
| **Ley 6534/2020** | In force | **Credit/patrimonial data** — solvency, credit reporting |
| General personal data law | **Gap** — no comprehensive GDPR equivalent identified | [NEEDS VERIFY] MITIC draft bills |

### Ley 6534/2020 key obligations (when handling credit data)

- Informed consent (express, unequivocal, revocable)
- Applies to data processed in PY territory
- Credit bureaus and financial institutions primary targets

### Practical guidance for Ai-Whisperers

| Scenario | Action |
|----------|--------|
| PY client CRM data (names, WA, cases) | Consent in engagement letter; minimize retention |
| EU client data | GDPR applies to EU residents regardless of processor location |
| Lead gen for legal (Rubicón) | Client is controller; we are processor — DPA needed |
| AI training on client data | **Do not** without explicit consent |

---

## Paraguay — Billing & invoicing (SIFEN)

| Item | Detail |
|------|--------|
| System | SIFEN via e-kuatia / Marangatú |
| Legal base | Decreto 872/2023 |
| Effective | Jan 2024+; phased mandatory groups |
| Format | XML + digital signature + DNIT validation |
| Deadline | Transmit within **72 hours** of issuance |
| Requirements | RUC active, qualified electronic signature, Marangatú access |

### Export invoicing

- Maquila service exports: factura electrónica de exportación
- [NEEDS VERIFY] FX declaration and DNIT export procedures

---

## LATAM data privacy by country

| Country | Law | Key points | AI relevance |
|---------|-----|------------|--------------|
| **Brazil** | **LGPD** (Lei 13.709/2018) | Consent, DPO for large processing, ANPD enforcement | High if BR clients |
| **Argentina** | **PDPA Ley 25.326** | Registration of databases; consent; cross-border restrictions | Medium |
| **Mexico** | **LFPDPPP** | ARCO rights; privacy notice (aviso); consent | Medium if MX clients |
| **Chile** | **Ley 19.628** | Basic data protection; reform pending | Lower enforcement |
| **Colombia** | **Ley 1581/2012** | Authorization, SIC enforcement | Medium |
| **Paraguay** | Ley 6534/2020 (credit); general gap | See above | Local clients |

### Cross-border data transfer

- EU → PY: Standard Contractual Clauses (SCCs) if GDPR applies
- PY → EU: Document in DPA; maquila export doesn't exempt GDPR
- LATAM internal: check each country's cross-border rules

---

## AI regulation status (LATAM)

| Jurisdiction | Status 2026 |
|--------------|-------------|
| EU | AI Act in force — affects EU clients, not PY domestic law |
| Brazil | PL 2338/2023 under debate; ANPD monitoring AI [NEEDS VERIFY current status] |
| Mexico | AI strategy documents; no binding AI Act |
| Argentina | Discussion phase |
| Paraguay | No AI-specific law identified |
| Regional | **No LATAM-wide AI Act equivalent** |

**Opportunity**: Deploy structured AI ops now; compliance-monitor agent tracks regulatory changes.

---

## Tax implications — digital service exports

| Flow | Consideration |
|------|---------------|
| PY entity → PY client | IVA, IRP/RGC per DNIT rules; SIFEN invoice |
| PY entity → EU client (B2B) | Maquila export path; VAT reverse charge in EU typically |
| PY entity → EU client (B2C) | [NEEDS VERIFY] VAT OSS rules |
| NL entity (future e-Residency) | Separate structure; not covered here |

**[NEEDS VERIFY]** All tax positions with Paraguayan accountant before scaling.

---

## Compliance checklist (pre-scale)

- [ ] Engagement letter with data processing terms
- [ ] DPA template for EU clients
- [ ] SIFEN e-invoice operational
- [ ] Maquila program evaluation (if export >50% revenue)
- [ ] Consent language for lead-gen pipelines
- [ ] Compliance Officer hire before first EU client (per founder narrative)
- [ ] Accountant sign-off on maquila tax treatment

---

## Sources

1. Ley 7547/2025 — https://www.bacn.gov.py/leyes-paraguayas/12853/ley-n-75472025-del-regimen-de-maquila
2. MIC Maquila — https://www.mic.gov.py/maquila24/
3. Ley 6534/2020 — https://silpy.congreso.gov.py/web/descarga/ley-143275
4. Decreto 872/2023 SIFEN — https://lexparaguaya.com/docs/decreto-n-872-2023
5. RSM Paraguay maquila analysis — https://www.rsm.global/paraguay/es/news/nuevo-regimen-de-maquila-en-paraguay
6. OECD/SELA 2024 — LGPD reference in Brazil chapter

## Open gaps

- [ ] Accountant review: maquila eligibility for AI consulting
- [ ] General PY personal data law status (MITIC)
- [ ] Brazil PL 2338 current legislative status
