# LATAM Market Sizing — SMB Counts, Digital Adoption, AI Spend

> **Ticket**: DEMIURGE-056  
> **Status**: researched 2026-08-26  
> **Confidence**: medium-high on structural stats; medium on AI spend (vendor surveys)

## Executive summary

The deck claim "50M+ LATAM SMBs" is **directionally correct but underspecified**. Formal MIPYMES in six target countries alone exceed **15M registered economic units**; including micro-informal and MEI-style sole proprietors pushes the addressable universe well above 50M. **AI spend is accelerating** (54% of LATAM SMEs using some AI per LF research; 70% plan to increase spend), but **willingness to pay for structured ops consulting** remains concentrated in digitally active small firms with 5–50 employees.

---

## Regional baseline (LAC)

| Metric | Value | Source |
|--------|-------|--------|
| Share of formal firms that are MIPYMES | **99.5%** (88.4% micro) | OECD/CAF/SELA SME Policy Index LAC 2024 |
| Share of formal employment from MIPYMES | **~60%** | OECD/CAF/SELA 2024; IEE/CEPAL characterization 2025 |
| Share of regional GDP from MIPYMES | **~25%** (vs ~56% EU) | IEE Punto de Vista Nov 2025 |
| Informal economy (regional avg 2010–2015) | **~33.4% of GDP** | IEE/CEPAL |

**Implication**: TAM is huge in unit count; SAM must filter for formalization, digital readiness, and budget.

---

## SMB counts by country (primary 6)

Definitions differ by country (establishments vs enterprises vs RUC). Do not sum across rows without deduplication.

| Country | Metric | Count | Year | Source |
|---------|--------|-------|------|--------|
| **Brazil** | Enterprises & organizations (CEMPRE) | **10.6M** | 2024 | IBGE CEMPRE 2024 |
| | Share with 0–9 employees | **93.4%** | 2024 | IBGE CEMPRE 2024 |
| | New small-business openings (MEI+ME+EPP) | **4.16M** (annual) | 2024 | Sebrae / RFB CNPJ |
| **Mexico** | Total establishments | **7.06M** | 2024 | INEGI Censos Económicos 2024 |
| | Private-sector economic units | **5.45M** | 2024 | INEGI CE 2024 |
| **Paraguay** | MIPYMES (MIC BDMIPYMES, RUC+IPS) | **450,167** | 2023 | MIC Boletín Formalización MYPIMES 2025 |
| | MIPYMES (INE DIRGE, secondary+tertiary) | **369,718** | 2023 | INE DIRGE 2024 |
| **Argentina** | MIPYMES share of firms | **95–99%** (regional pattern) | 2024 | OECD/SELA country chapter |
| **Colombia** | MIPYMES share of firms | **95–99%** (regional pattern) | 2024 | OECD/SELA country chapter |
| **Chile** | MIPYMES share of firms | **95–99%** (regional pattern) | 2024 | OECD/SELA country chapter |

### Paraguay note

MIC and INE counts diverge (~80k) because DIRGE excludes primary sector and uses different inclusion rules. Use **450k** for formalization/policy narrative; **370k** for cross-country industry comparisons.

### Argentina / Colombia / Chile absolute counts

[NEEDS VERIFY] Country-specific enterprise totals not extracted in this pass. OECD/SELA 2024 country chapters (pp. 126–230) contain national tables. **Conservative deck range**: 2–4M formal MIPYMES each for AR + CO + CL combined with BR+MX+PY → **15M+ formal units** in six countries.

### Revised TAM framing (replaces unverified "50M+")

| Layer | Definition | Estimate | Basis |
|-------|------------|----------|-------|
| **TAM (units)** | All MIPYMES + MEI/micro in 6 countries | **50M–70M** | BR ~19M+ active small entities (gov cite via Sebrae); MX ~5.5M units; PY ~450k; AR/CO/CL millions each; informal layer adds tens of millions |
| **SAM** | Formal, secondary/tertiary, 5+ employees OR digital payment active | **2–4M** | Filter 93% micro in BR; PY 88% micro; digital adoption filters below |
| **SOM (3yr)** | Founder-led services firms, consulting budget, ES/NL reachable | **50k–150k** | Vertical ICP filters in `icp-profiles.md` |

---

## Digital adoption

| Signal | Finding | Source |
|--------|---------|--------|
| Regional SME policy focus | Digital transformation is explicit SME Policy Index dimension (2024 vs 2019) | OECD/CAF/SELA 2024 |
| Brazil small-business AI use | **52%** used AI in prior 2 weeks (marketing, CS, inventory) | Sebrae survey 2025 (Valor International) |
| Brazil AI expansion intent | **60%** plan to start or expand AI use in next 6 months | Sebrae survey 2025 |
| Adoption barrier | **38%** of non-adopters cite lack of knowledge of AI capabilities | Sebrae survey 2025 |
| Paraguay payments | Mercado Pago, banking apps widespread; SIFEN e-invoice rollout 2024+ | DNIT Decreto 872/2023; [NEEDS VERIFY] penetration % |
| WhatsApp as business channel | De facto CRM for PY/LATAM SMBs | Practitioner consensus; validate per vertical |

**SAM filter**: digitally active = uses WhatsApp Business + electronic invoicing OR cloud accounting + accepts digital payments.

---

## AI / tech services spending

| Signal | Finding | Source |
|--------|---------|--------|
| LATAM orgs increasing AI budget | **97%** plan increase; avg **+14%** YoY | IDC via Mexico Business News 2025 |
| Systematic AI adoption (orgs) | **62%** in systematic/pilot phase (up from 39% in 2024) | IDC 2025 |
| SME AI usage | **54%** of LATAM SMEs using some AI; **49%** gen AI | Linux Foundation LATAM AI report 2025 |
| SME AI spend intent | **70%** plan to increase AI investments in 2025 | Microsoft study cited in LF report |
| Brazil IT market | **US$67.8B** (2025); **38.4%** of LATAM IT | 4MATT/ABES study 2026 |
| Brazil AI software/services | **US$1.9B** projected 2026 (**+36%** YoY) | 4MATT/ABES 2026 |
| SAP regional survey | **55%** plan higher AI spend vs 2024; small firms more likely to hold flat budget | SAP LATAM corporate AI report 2025 |
| Large vs small gap | Large cos **77%** increasing spend; small more likely to maintain | SAP 2025 |

### Spend per SMB segment (inferred bands)

| Segment | Employees | Typical monthly tech budget | AI/consulting WTP |
|---------|-----------|----------------------------|-------------------|
| Micro | 1–5 | US$0–50 | Low; DIY ChatGPT, freelancers |
| Small | 6–30 | US$50–500 | **Core ICP** — coaching M-tier ($500/mo) viable |
| Medium | 31–100 | US$500–5k | Standard/Premium tiers; dept modules |
| Large SMB | 100+ | US$5k+ | Enterprise tier; competes with agencies |

[NEEDS VERIFY] Per-country FX and local pricing bands in `icp-profiles.md`.

---

## Growth rate — SMB digital ops spending

| Driver | Trend |
|--------|-------|
| Cloud/SaaS normalization | Post-COVID baseline; AI layer on top 2024–2027 |
| E-invoicing mandates | PY SIFEN, MX CFDI, BR NF-e — forces digitization |
| AI agent hype cycle | YouTube "AI employee" products pull demand; skepticism also rising |
| IT spend CAGR (Brazil AI slice) | **~36%** (2025–2026 AI software/services) | 4MATT |

---

## Deck-ready citations

Replace slide 2 / market slide bullets with:

```
▸ TAM: 50M+ economic units in PY+AR+BR+MX+CO+CL (99.5% MIPYMES — OECD/SELA 2024)
▸ SAM: ~2–4M digitally-active formal SMBs (5+ employees, e-invoice/payments)
▸ SOM: 50k–150k founder-led service firms with ops pain + budget
▸ AI tailwind: 54% LATAM SMEs already use AI; 70% plan higher spend (LF/Microsoft 2025)
```

---

## Sources

1. OECD/CAF/SELA — *SME Policy Index: Latin America and the Caribbean 2024* — https://www.sela.org/wp-content/uploads/2025/02/Final-Report-IPPALC-SME-Policy-Index-Latin-America-and-the-Caribbean-2024.pdf
2. IEE — *Caracterización de las mipymes en América Latina y el Caribe* (Nov 2025) — https://www.ieemadrid.es/sites/ceoe-iee/files/content/file/2025/12/03/25/iee.-punto-de-vista-noviembre-2025.-caracterizacion-de-las-mipymes-en-america-latina-y-el-caribe.pdf
3. IBGE — CEMPRE 2024 — https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47285-cresce-o-numero-de-empresas-no-pais-em-2024-mas-salario-medio-fica-estavel
4. Sebrae — Painel Abertura Pequenos Negócios 2024 — https://agenciasebrae.com.br/
5. INEGI — Censos Económicos 2024 resultados oportunos — https://www.inegi.org.mx/contenidos/programas/ce/2024/doc/ro_pcp_ce2024.pdf
6. MIC Paraguay — Boletín Formalización MYPIMES 2025 — https://www.mipymes.gov.py/wp-content/uploads/2025/03/Boletin-formalizacion-MYPIMES.pdf
7. IDC LATAM AI spend — https://mexicobusiness.news/cloudanddata/news/most-latin-american-firms-boost-ai-spend-over-year-idc
8. Linux Foundation — *Economic and Workforce Impacts of AI in Latin America* — https://www.linuxfoundation.org/hubfs/Research%20Reports/Economic_Workforce_Impacts_AI_LatAm_Report.pdf
9. SAP — *Artificial Intelligence in the Corporate World* (LATAM) — https://news.sap.com/latinamerica/files/2025/06/05/Regional-IA-in-the-corporate-world-External.pdf

## Open gaps

- [ ] Extract AR/CO/CL absolute enterprise counts from OECD country chapters
- [ ] Mercado Pago / PGS adoption rates by PY department
- [ ] Segment IT spend survey for PY specifically (MIC/MITIC)
