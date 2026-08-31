# Paraguay SMB Landscape — Economic Data & Startup Ecosystem

> **Tickets**: DEMIURGE-057, DEMIURGE-058  
> **Status**: researched 2026-08-26  
> **Confidence**: high on MIC/INE stats; medium on purchasing behavior (practitioner inference)

## Executive summary

Paraguay has **~450k formalized MIPYMES** (MIC 2023), overwhelmingly micro (88%), concentrated in Central + Asunción + Alto Paraná. The **startup ecosystem is early**: Distrito Digital (MITIC) launches virtual hub 2025, physical campus ~2027. **Purchasing is relationship-first, WhatsApp-native, referral-driven.** Real competition is local freelancers and manual processes, not global AI SaaS.

---

## MIPYMES scale and structure

| Metric | Value | Source |
|--------|-------|--------|
| Total MIPYMES (BDMIPYMES) | **450,167** | MIC Boletín Formalización 2023 |
| YoY change | **+23%** vs 366,977 (2022) | ABC Color / MIC 2025 |
| Micro (≤ G. 646M revenue/yr) | **396,407 (88.06%)** | MIC 2023 |
| Pequeña | **43,249 (9.61%)** | MIC 2023 |
| Mediana | **10,511 (2.33%)** | MIC 2023 |
| RENAMIPYMES eligible | **43,140 (9.58%)** | MIC 2023 |
| INE DIRGE MIPYMES (alt.) | **369,718** | INE 2024 (ref 2023) |
| Employment in MIPYMES | **~2.18M (74.9%** of occupied 15+) | INE EPHC 2025 |

### Geographic concentration

| Department | Share of MIPYMES |
|------------|------------------|
| Central | 32.93% |
| Asunción | 19.63% |
| Alto Paraná | 19.91% |
| Itapúa | 7.21% |
| Caaguazú | 5.21% |

**GTM implication**: Asunción + Central + Ciudad del Este (Alto Paraná) = ~72% of formal MIPYMES.

---

## Sector breakdown (ICP-relevant)

MIC bulletin segments by economic activity. Approximate priorities for Ai-Whisperers ICP:

| Sector | Relevance | Notes |
|--------|-----------|-------|
| **Servicios profesionales** (legal, contable, consultoría) | **High** | Rubicón EAS proof point; low tech depth, high referral |
| **Comercio** | Medium | High volume micro; thin margins |
| **Construcción** | Medium | Project-based; WhatsApp coordination |
| **Salud / odontología** | **High** | Pricing benchmarks exist (finance-legal constitution) |
| **Inmobiliaria** | Medium | Relationship sales; lead gen pain |
| **E-commerce / retail** | Medium | Growing; Mercado Libre / Instagram sales |
| **Coaching / capacitación** | **High** | Aligns with M-tier coaching product |

[NEEDS VERIFY] Exact CNAE-style % breakdown per sector — extract from MIC bulletin tables (Fig. sector charts).

### Average revenue / headcount bands (DNIT classification)

| Category | Max annual revenue (approx.) | Typical headcount |
|----------|------------------------------|-------------------|
| Micro | G. 646,045,491 (~US$85k) | 1–10 |
| Pequeña | G. 3,230,227,453 (~US$425k) | 11–30 |
| Mediana | G. 7,752,545,886 (~US$1M+) | 31–50+ |

Average MIPYME age: **~10 years** (MIC 2024 bulletin); Ñeembucú highest at 13 years.

---

## Founder demographics

| Dimension | Finding | Confidence |
|-----------|---------|------------|
| Age | [NEEDS VERIFY] Majority 35–55 in professional services | Low — needs EPHC/ENCUESTA entrepreneur survey |
| Education | University growth in Asunción; interior more informal | Medium |
| Digital literacy | Bimodal: mobile-first WhatsApp fluent; weak on CRM/automation | High (practitioner) |
| Language | Spanish primary; Guaraní in informal comms; English rare outside tech | High |
| Gender | [NEEDS VERIFY] MIC gender disaggregation in bulletin | Low |

---

## Digital payment adoption

| Channel | Status |
|---------|--------|
| **Mercado Pago** | Dominant fintech wallet; QR payments in retail/services |
| **Banking apps** | Banco Continental, Itaú, Regional — transferencias |
| **PGS / POS** | Card present in urban centers |
| **SIFEN e-invoice** | Mandatory rollout 2024+; forces digitization | Decreto 872/2023 |
| **Crypto** | Niche; not ICP default |

[NEEDS VERIFY] Transaction volume share by provider — BCP / DNIT reports.

**Sales implication**: Proposals should include transferencia + Mercado Pago; invoice via SIFEN-compliant factura electrónica.

---

## Startup ecosystem

| Actor | Role | Status 2026 |
|-------|------|-------------|
| **MITIC — Distrito Digital** | National tech hub; virtual launch Oct–Nov 2025; physical campus Ñu Guasu ~mid-2027 | Active development |
| **CONACYT** | Science/tech council; co-designs Distrito Digital | Active |
| **Cámaras de Tecnología** | Private sector coordination | Active |
| **UPTP** (Universidad Politécnica Taiwán Paraguay) | Talent pipeline for hub | Active |
| **Wayra** | Telefónica CVC — **no PY hub**; operates AR, BR, CL, CO, MX, PE | Regional network only |
| **REDIEX / MIC** | Export promotion; Maquila programs | Active |
| **Incubators / accelerators** | [NEEDS VERIFY] List local names — Kuña Katupyry, etc. | Low |

### Ecosystem maturity assessment

| Dimension | Score (1–5) | Notes |
|-----------|-------------|-------|
| Venture capital | 2 | Small rounds; family/revenue-funded |
| Corporate innovation | 2 | Banks, retail slow adopters |
| Talent pool | 3 | Growing dev community; brain drain to remote US/EU |
| Government programs | 3 | MITIC, CONACYT, Maquila 7547/2025 |
| Community density | 2 | Fragmented; WhatsApp groups > formal networks |

---

## Purchasing behavior

| Pattern | Description |
|---------|-------------|
| **Trust-first** | Buy from people they know or who were referred by a trusted peer |
| **WhatsApp-native** | Discovery, negotiation, delivery updates, payment proof — all in WA |
| **Proof over pitch** | Demo > deck; case study > feature list |
| **Price sensitivity** | Micro segment price-shops; pequeña/mediana pays for outcomes |
| **Decision-maker** | Owner/founder decides; no procurement committee under ~30 employees |
| **Anti-patterns** | Cold LinkedIn DM, English-only materials, no local phone, "AI magic" without workflow |

### Rubicón EAS generalization (legal vertical)

What closed the first deal (from internal state):

- **Concrete workflow**: legal lead generation pipeline, not generic "AI transformation"
- **Low monthly entry**: ~US$240/mo MRR — below "consulting project" psychology
- **Production deployment**: not a pilot deck
- **Local presence**: Paraguay-based team, Spanish comms
- **Vertical specificity**: legal-tech framing

Generalize: **named workflow + visible output + affordable recurring + local trust**.

---

## Competitive alternatives (local, non-AI)

| Alternative | Why they win | How we beat them |
|-------------|--------------|------------------|
| Nephew who "knows computers" | Free/cheap | Reliability, SLA, production ops |
| Freelance n8n/Zapier dev | One-time automation | Ongoing dept + memory + personal touch |
| Filipino VA | Low hourly cost | Spanish, timezone, relationship, AI leverage |
| Do nothing | Zero cost | Founder burnout cost is invisible until crisis |

---

## Sources

1. MIC — Boletín Formalización MYPIMES (Mar 2025) — https://www.mipymes.gov.py/wp-content/uploads/2025/03/Boletin-formalizacion-MYPIMES.pdf
2. MIC — Boletín Formalización y Empleo 2024 — https://www.mic.gov.py/wp-content/uploads/2024/04/Boletin_web-1.pdf
3. INE — Día Internacional MIPYMES / DIRGE 2024 — https://www.ine.gov.py/noticias/2442/27-de-junio-dia-internacional-de-las-mipymes
4. ABC Color — MIC database update — https://www.abc.com.py/economia/2025/03/15/cuantas-mipymes-hay-en-paraguay-y-a-que-se-dedican-mic-actualizo-base-de-datos/
5. MITIC — Distrito Digital — https://mitic.gov.py/ministro-villate-compartio-detalles-del-distrito-digital-con-el-senador-kemper-durante-visita-al-predio-del-futuro-parque-tecnologico/
6. Diario HOY — Hub tecnológico — https://www.hoy.com.py/nacionales/2025/04/27/paraguay-busca-posicionarse-como-un-hub-tecnologico

## Open gaps

- [ ] Sector % table from MIC bulletin
- [ ] Named incubator/accelerator list with contact paths
- [ ] Ivan/Kiki validation of purchasing behavior patterns (DEMIURGE-068)
