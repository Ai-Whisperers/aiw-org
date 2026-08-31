# Human Review Gate — LATAM + PY Market Research

> **Ticket**: DEMIURGE-068  
> **Owner**: Ivan / John  
> **Status**: **PENDING HUMAN REVIEW**  
> **AI research completed**: 2026-08-26

## Purpose

AI researched public sources and internal state. Only Ivan/Kiki can validate ICP fit, language nuance, and deal-specific facts from live conversations.

---

## Review checklist

### ICP validation

| Item | AI claim | Human verdict | Notes |
|------|----------|---------------|-------|
| Rubicón EAS generalization to legal ICP | Lead gen pipeline + $240/mo + local trust closed deal | ☐ Confirm ☐ Revise | |
| richar-ruiz vertical and pain | Canary at ~$1,500/mo; vertical unknown | ☐ Fill in | |
| Dental as #2 wedge | Pricing constitution exists | ☐ Confirm ☐ Deprioritize | |
| Coaching M-tier $500/mo WTP in PY | Inferred from product strategy | ☐ Confirm | |
| ICP scoring rubric weights | AI-proposed | ☐ Approve ☐ Adjust | |

### Language validation (native ES)

| File | Reviewer | Verdict |
|------|----------|---------|
| `community/revenue-stack/language/es-py-legal.md` | Ivan | ☐ |
| `community/revenue-stack/language/es-py-coaching.md` | Ivan | ☐ |
| `community/revenue-stack/language/es-py-general-smb.md` | Ivan | ☐ |
| `community/cm-marketing/language/es-py-sales-motion.md` | Ivan | ☐ |

Confirm or correct:
- [ ] "acompañamiento" vs "coaching" in PY market
- [ ] "agente" vs "asistente" vs "automatización" cold-outreach default
- [ ] WA cadence (2 follow-ups max) matches local norms

### NL market validation

| Item | Reviewer | Verdict |
|------|----------|---------|
| Mark NL contact exists and fits NL ICP | John | ☐ |
| `nl-direct-sales-motion.md` tone | John | ☐ |
| LinkedIn-primary / anti-WA claims | John | ☐ |

### Regulatory

| Item | Action | Owner |
|------|--------|-------|
| Maquila 7547 applicability to AI consulting export | Accountant consultation | Ivan |
| 1% maquila tax rate accuracy | Accountant sign-off | Ivan |
| SIFEN compliance status of Ai-Whisperers billing | Finance | Ivan/Kiki |
| DPA template needed before EU client | Legal | Ivan |

### Community sources

| Item | Owner | Verdict |
|------|-------|---------|
| Named PY WhatsApp tech groups | Ivan | ☐ Supply names |
| AI en Español Slack invite (current) | Ivan/Kiki | ☐ |
| Cámara de Comercio PY URL | Ivan | ☐ |

### Deck / narrative updates

| File | Change | Approved |
|------|--------|----------|
| `state/deck-template-v0.1.md` | TAM/SAM/SOM cited | ☐ |
| `state/founder-narrative-v0.1.md` | "50M+ SMBs" line | ☐ Optional update |

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| CEO / ES native | Ivan | | |
| Co-founder | Kiki | | |
| Advisor | John | | |

**Gate rule**: Promote `community/*/language/` entries from `proposed` → `active` only after Ivan sign-off on language rows.

---

## Post-review actions

1. Update `confidence` fields in community memory entries
2. Fill richar-ruiz row in `sources/latam/icp-profiles.md`
3. Schedule accountant call for maquila (if export path pursued)
4. Add `sources/latam/catalog.yaml` with rated sources
5. Register Echo cron sources from `community-sources.md`
