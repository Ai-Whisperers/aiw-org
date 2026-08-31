# LATAM Community Sources — Echo Scanner Catalog

> **Ticket**: DEMIURGE-066  
> **Status**: researched 2026-08-26  
> **Purpose**: Seed Echo config and community memory with practitioner channels

## Rating key

| Score | Authority | Recency | ICP match |
|-------|-----------|---------|-----------|
| 5 | Official / tier-1 | <6mo | Direct ICP |
| 4 | Established community | <1yr | Adjacent |
| 3 | Useful | 1–2yr | Partial |
| 2 | Noisy | Stale | Low |
| 1 | Unreliable | — | — |

---

## Paraguay

| Source | Type | URL | Auth | Recency | ICP | Notes |
|--------|------|-----|------|---------|-----|-------|
| MITIC | Government | https://mitic.gov.py | 5 | 5 | 3 | Distrito Digital, policy |
| MIC MIPYMES | Government | https://www.mipymes.gov.py | 5 | 5 | 5 | Formalization bulletins |
| CONACYT | Government | https://www.conacyt.gov.py | 4 | 4 | 3 | Science/tech funding |
| INE Paraguay | Statistics | https://www.ine.gov.py | 5 | 5 | 4 | DIRGE, employment |
| Cámara de Comercio Paraguay | Trade | [NEEDS VERIFY URL] | 4 | 4 | 5 | SMB events |
| Paraguay Tech Community (FB/WA) | Community | [NEEDS VERIFY] | 3 | 4 | 4 | Fragmented groups |

---

## LATAM regional

| Source | Type | URL | Auth | Recency | ICP | Notes |
|--------|------|-----|------|---------|-----|-------|
| Wayra | CVC / innovation | https://wayra.com | 5 | 5 | 3 | BR/MX/AR/CL/CO/PE; not PY |
| Endeavor LATAM | Accelerator alumni | https://endeavor.org | 5 | 4 | 4 | Scale-up founders |
| SELA / OECD SME Index | Policy | https://www.sela.org | 5 | 5 | 4 | MIPYME stats |
| IDB Lab | Development finance | https://www.idblab.org | 5 | 4 | 4 | LATAM SME programs |
| LAVCA | VC LATAM | https://www.lavca.org | 4 | 4 | 3 | Funding signals |
| #LatAmStartups | X/Twitter | https://x.com/search?q=%23LatAmStartups | 3 | 5 | 4 | Noisy but current |
| HackerNoon LATAM | Media | https://hackernoon.com | 3 | 4 | 3 | Essays, uneven quality |

---

## Spanish-language AI communities

| Source | Type | URL | Auth | Recency | ICP | Notes |
|--------|------|-----|------|---------|-----|-------|
| r/inteligenciaartificial | Reddit | https://www.reddit.com/r/inteligenciaartificial/ | 3 | 5 | 3 | ES AI discussion |
| r/mexico + AI flairs | Reddit | https://www.reddit.com/r/mexico/ | 3 | 5 | 3 | MX-specific |
| AI en Español (Slack) | Slack | [NEEDS VERIFY invite] | 3 | 4 | 4 | Practitioner chat |
| CrewAI Discord #español | Discord | https://discord.gg/crewai | 4 | 5 | 3 | Technical builders |
| n8n Community (ES posts) | Forum | https://community.n8n.io | 4 | 5 | 4 | Automation practitioners |
| Sebrae ASN | Brazil SMB | https://agenciasebrae.com.br | 5 | 5 | 5 | BR SMB + AI surveys |

---

## Netherlands / EU (NL market)

| Source | Type | URL | Auth | Recency | ICP | Notes |
|--------|------|-----|------|---------|-----|-------|
| TechLeap NL | Government-adjacent | https://www.techleap.nl | 5 | 5 | 4 | NL scale-ups |
| Dutch Tech Association | Industry | https://www.dutchtechassociation.nl | 4 | 4 | 4 | NL tech policy |
| StartupAmsterdam | Ecosystem | https://www.startupamsterdam.com | 4 | 4 | 3 | Amsterdam focus |
| NL AI Coalition | Policy | https://nlaic.com | 4 | 4 | 3 | AI policy, not SMB |

---

## Echo scan priorities (cron config seed)

```yaml
echo_latam_sources:
  high_priority:
    - mic_mipymes_bulletins
    - mitic_news
    - sebrae_asn
    - r/inteligenciaartificial
    - n8n_community_es
  medium_priority:
    - wayra_news
    - endeavor_blog
    - hackernoon_latam
    - techleap_nl
  low_priority:
    - latamstartups_twitter
  scan_cadence: weekly
  promote_threshold: authority >= 4 AND icp_match >= 4
```

---

## Sources metadata for catalog.yaml

Recommend adding to `sources/marketing/catalog.yaml` or new `sources/latam/catalog.yaml`:

| id | title | type | rating |
|----|-------|------|--------|
| latam-oecd-sme-2024 | OECD/SELA SME Policy Index LAC 2024 | policy | 5 |
| py-mic-mipymes | MIC MIPYMES bulletins | government | 5 |
| latam-sebrae-ai | Sebrae AI adoption surveys | research | 5 |
| es-reddit-ia | r/inteligenciaartificial | community | 3 |
| nl-techleap | TechLeap NL | ecosystem | 4 |

---

## Open gaps

- [ ] WA group names (PY tech) — Ivan to supply
- [ ] AI en Español Slack current invite link
- [ ] Create `sources/latam/catalog.yaml` in follow-up ticket
