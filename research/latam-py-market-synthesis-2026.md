# LATAM + Paraguay Market Research — Synthesis

> **Ticket**: DEMIURGE-067  
> **Status**: synthesized 2026-08-26  
> **Inputs**: DEMIURGE-056 through DEMIURGE-066

## Research deliverables

| Domain | Ticket(s) | Output |
|--------|-----------|--------|
| Market sizing | 056 | `sources/latam/market-sizing.md` |
| PY SMB landscape | 057, 058 | `sources/py/smb-landscape.md` |
| ICP profiles | 059, 060 | `sources/latam/icp-profiles.md` + `community/revenue-stack/language/` |
| Competitive | 061, 062 | `sources/latam/competitive-landscape.md` + `community/revenue-stack/practices/competitive-gaps.md` |
| Culture / sales | 063, 064 | `sources/latam/culture-and-language.md` + `community/cm-marketing/language/` |
| Regulatory | 065 | `sources/latam/regulatory.md` |
| Community sources | 066 | `sources/latam/community-sources.md` + `community/cm-marketing/signals/latam-seed.md` |

---

## Key findings (deck-ready)

### Market

- **99.5%** of formal LAC firms are MIPYMES; **~60%** of formal employment; only **~25%** of GDP (productivity gap) — OECD/SELA 2024
- **Six-country formal base**: BR 10.6M enterprises (IBGE 2024) + MX 5.45M units (INEGI 2024) + PY 450k (MIC 2023) + AR/CO/CL millions → **TAM 50M+ economic units defensible**
- **SAM**: ~2–4M digitally-active formal SMBs (5+ employees, e-invoice/payments)
- **SOM**: 50k–150k founder-led service firms with ops pain + budget
- **AI tailwind**: 54% LATAM SMEs use AI; 70% plan higher spend (LF/Microsoft 2025); BR 52% small businesses used AI in prior 2 weeks (Sebrae 2025)

### Paraguay

- **450,167** formalized MIPYMES (88% micro); Central + Asunción + Alto Paraná = ~72%
- Purchasing: **WhatsApp-native, referral-first, proof-before-pitch**
- Ecosystem early: **Distrito Digital** virtual 2025, campus ~2027; Wayra has no PY hub
- **Maquila de Servicios** (Ley 7547/2025) opens export path for AI consulting — accountant sign-off required

### ICP

- **Primary**: founder-led services, 5–30 employees, PY → AR/BR/MX expansion
- **Wedges**: legal (Rubicón proof), coaching ($500/mo M-tier), dental (pricing constitution)
- **Language**: "acompañamiento" not "coaching"; "automatización" before "IA"; "asistente" before "agente" in cold outreach
- **richar-ruiz**: canary deal at ~$1,500/mo — vertical details pending human review

### Competitive

- Real competition: **freelancers, VAs, manual WA** — not Sintra/11x
- Gap: **departmental swarm + human gates + git memory + production proof**
- Sintra $16–97/mo with 250 credit cap vs our $240–500/mo production retainer

### Regulatory

- PY Ley 1682 **derogated** → Ley 6534/2020 (credit data); general privacy law gap
- SIFEN e-invoice mandatory rollout — forces SMB digitization
- LGPD / AR PDPA / MX LFPDPPP when processing local resident data
- No LATAM AI Act equivalent yet

---

## Updated TAM / SAM / SOM (replaces unverified deck lines)

| Metric | Old (deck v0.1) | New (cited) |
|--------|-----------------|-------------|
| TAM | 50M+ LATAM SMBs (unverified) | **50M+ economic units** in PY+AR+BR+MX+CO+CL; 99.5% MIPYMES (OECD/SELA 2024) |
| SAM | 2M+ digitally-active | **2–4M** formal SMBs with digital ops signals |
| SOM | 50K+ burnout + budget | **50k–150k** founder-led service firms in target verticals |

---

## Positioning delta (slide 10)

**Before**: placeholder competitive slide  
**After**: see `community/revenue-stack/practices/competitive-gaps.md`

1. Not agent soup — named departments with souls and KPIs
2. Not hype SaaS — production deploy with human gates
3. Not offshore VA — Spanish, timezone, systems that compound
4. Proof: Rubicón EAS live at $240/mo

---

## Feeds into DEMIURGE runtime

| Agent | Consumes |
|-------|----------|
| **Thoth** | `sources/latam/*.md` as source catalog extensions |
| **Echo** | `community-sources.md` + `latam-seed.md` scan config |
| **Apollo** | `icp-profiles.md`, culture doc, language entries |
| **Hera** | culture doc, competitive gaps, language entries |
| **Calliope** | language entries per vertical |
| **Argus** | regulatory.md for compliance-monitor skeleton |

---

## Items flagged [NEEDS VERIFY]

1. AR/CO/CL absolute enterprise counts (OECD country chapters)
2. Maquila tax treatment for Ai-Whisperers — accountant
3. richar-ruiz vertical and pain profile — Ivan/John
4. PY community WA group names — Ivan
5. All `community/*/language/` entries — Ivan native ES review

→ Tracked in `research/latam-py-market-REVIEW-GATE.md` (DEMIURGE-068)

---

## Sources index

All primary URLs consolidated in per-domain files under `sources/latam/` and `sources/py/`.
