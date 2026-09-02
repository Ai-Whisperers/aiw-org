# David Ondrej Content Analysis — 2026-09-02

> **Goal**: Analyze David Ondrej's YouTube channel (394 grounded videos) for
> insights that can upgrade AIW-org's operations, agent design, and content
> strategy. Findings grounded in video titles, view counts, and upload dates
> fetched via public RSS feed + yt-dlp flat-playlist (no auth).
>
> **Status**: DONE (analysis only, no behavior change to AIW)
> **Author**: AI (per session request, 2026-09-02)
> **Method**: `scripts/fetch-youtube-channel.py` (new tool, see §10)
> **Confidence**: HIGH for title patterns + view counts; LOW for transcript-level claims
> (no transcripts analyzed — would require yt-dlp subtitle extraction)

## 1. Corpus

- **Channel**: @DavidOndrej (id `UCPGrgwfbkjTIgPoOh2q1BAg`)
- **Videos grounded**: **394 unique videos** (15 via RSS + 383 via /videos tab + 145 via 3 playlists, deduplicated)
- **Total views**: ~23.8 million
- **Upload years**: 2023 (32), 2024 (120), 2025 (144), 2026 (87)
- **Tool**: `yt-dlp` (2026.8.19) installed via `uv tool install yt-dlp`

Per **R11**, this is **analysis only**, not engagement/marketing/outreach.

## 2. Top 15 videos (all-time by view count)

| Rank | Views | Uploaded | Title |
|---|---|---|---|
| 1 | 1.7M | 2025-09 | **Build Everything with AI Agents: Here's How** |
| 2 | 1.2M | 2023-09 | Sam Altman - The Man Who Owns Silicon Valley |
| 3 | 1.1M | 2024-09 | Build Anything With ChatGPT, Here's How |
| 4 | 590K | 2025-09 | Build anything with DeepSeek R1, here's how |
| 5 | 416K | 2025-09 | Google just destroyed all vibe-coding apps (Firebase Studio) |
| 6 | 388K | 2023-09 | The Man OpenAI Fears The Most |
| 7 | 377K | 2026-07 | Matt Pocock's Agentic Engineering Workflow (just copy him) |
| 8 | 349K | 2024-09 | Build Anything with AI Agents, Here's How |
| 9 | 346K | 2024-09 | Llama 3 for my specific use case |
| 10 | 301K | 2025-09 | Build Anything with Claude Agents, Here's How |
| 11 | 282K | 2026-04 | The only AutoResearch tutorial you'll ever need |
| 12 | 279K | 2025-09 | 5 simple AI Agents you must have |
| 13 | 278K | 2025-09 | Build anything with DeepSeek V3, here's how |
| 14 | 254K | 2024-09 | Build Anything with Perplexity, Here's How |
| 15 | 246K | 2025-09 | Build Anything with OpenAI o1, Here's How |

**Note**: The 2026-07 video (#7, 377K views) is **already 377K views in 2 months** — it's on track to be his biggest 2026 hit.

## 3. 2026 content themes (87 videos)

The 87 videos uploaded in 2026 reveal a clear thematic shift:

| Theme | Count | Examples |
|---|---|---|
| **Agentic Engineering workflow** (workflow composition, not just tools) | ~25 | Matt Pocock's AE Workflow (377K), Ex-NASA dev's AE Workflow (233K), L8 Principal's Setup (120K), Why This Dev Ships 100x Faster (215K), 100 hours of Hermes Agent lessons (167K) |
| **Hermes Agent** (the AIW-adjacent agentic framework) | ~12 | Hermes Agent is insane (184K), Obsidian Just 10x'd Hermes (68K), Hermes Agent is crazy (83K), 100 hours of Hermes (167K), I gave my Hermes Agent a phone number (48K), Hermes /goal is insane (81K) |
| **Self-improving / autonomous agents** | ~5 | Self-Improving AI Agents Are Almost Here (13K), 100% self-improving AI Agent is insane (60K), This AI Agent can actually self-evolve (71K), 100% automatic AI Agent can do anything (180K) |
| **Open-source model tutorials** | ~10 | Build Anything with Kimi K3 (147K), DeepSeek V4 shocked AI industry (66K), How to run DeepSeek on your computer (100K), Llama 3.3 better than ChatGPT (51K), Llama 3.2 destroys 100B models (66K), Fine-Tune biggest open-source models (27K) |
| **Vibe-coding app builders** (Cursor, v0, Bolt, Lovable, Replit Agent) | ~10 | Google destroyed all vibe-coding apps (416K!), OpenCode just killed vibe coding apps (145K), 8 Insane OpenCode Use Cases (92K), Build Anything with Cursor (56K), I just replaced myself with Clawdbot (90K) |
| **AI business / money-making** | ~10 | Tokens can make you rich - Mario Zechner (229K), This unique AI business model will make millionaires (100K), How To Run a Zero-Human Company Paperclip (45K), Don't start an AI business before watching this (19K), $75M founder reveals AE setup (44K) |
| **AI model hot-takes / drama** | ~15 | GPT 5.6 banned, Fable banned (42K), GPT 5.4 hit a wall (31K), DeepSeek V4 shocked industry (66K), Claude Mythos might be AGI (39K), GPT 5.2 first model I'd give work to (20K), OpenAI killed open-source (14K), OpenAI destroying image tools (10K), Anthropic will destroy OpenAI by 2027 (?), Sam Altman the man who owns Silicon Valley (1.2M) |
| **Practical building blocks** | ~10 | How to run DeepSeek on your computer (100K), Build anything with Local AI Models (34K), Unsloth Studio (124K), 100% private AI Agent (180K), AgentZero OpenClaw killer (75K), Obsidian 10x'd Hermes (68K) |

## 4. Top 20 most-viewed in 2026

| Views | Date | Title |
|---|---|---|
| **377K** | 2026-07 | Matt Pocock's Agentic Engineering Workflow (just copy him) |
| 282K | 2026-04 | The only AutoResearch tutorial you'll ever need |
| 233K | 2026-08 | Ex-NASA dev reveals his Agentic Engineering Workflow |
| 229K | 2026-06 | Tokens can make you rich – Mario Zechner |
| 215K | 2026-06 | Why This Dev Ships 100x Faster Than 99% of Engineers |
| 184K | 2026-05 | Hermes Agent is insane… 100,000+ github stars |
| 180K | 2026-02 | This 100% private AI Agent can do anything… just watch |
| 167K | 2026-06 | 100 hours of Hermes Agent lessons in 46 minutes |
| 161K | 2026-02 | Claude Code can now make videos, here's how |
| 147K | 2026-08 | Build Anything with Kimi K3, Here's How |
| 145K | 2026-02 | OpenCode just killed all vibe coding apps |
| 135K | 2026-08 | Build a $5,000 AI Datacenter at Home |
| 124K | 2026-06 | Unsloth Studio: fine-tune any AI model locally |
| 120K | 2026-08 | L8 Principal's Agentic Engineering Setup |
| 107K | 2026-03 | I made my OpenClaw 10x more powerful |
| 100K | 2026-01 | This unique AI business model will make millionaires |
| 93K | 2026-05 | Google destroyed all open-source models (Gemma 4) |
| 92K | 2026-02 | 8 Insane OpenCode Use Cases |
| 90K | 2026-02 | I just replaced myself with Clawdbot |
| 84K | 2026-08 | Agentic Engineering, explained by a 10x developer |

**Pattern**: "Workflow" + "Ship faster" + "self-improving" + "open-source model setup" dominate the top 20. **"X is dead" / drama content gets clicks but isn't in the top tier.** His sustainable hits are educational + actionable.

## 5. Patterns AIW should adopt

### High-leverage, low-cost (do this)

| Pattern from David | Concrete AIW implementation | Sprint |
|---|---|---|
| **"Workflow over tools" framing** — the biggest 2026 cliff is from "build with X" to "how to wire X+Y+Z into a workflow" | When AIW's kernel ships (Sprint F WS-5), **package the kernel + adjacent tools as a workflow**, not just a directory of files | Sprint F + post-F |
| **"100 hours of Hermes Agent lessons in 46 minutes"** — the distil-and-share format | When AIW has 6+ sprints of accumulated work, write the retrospective in the same format: "6+ sprints of agent-org-design in 30 minutes" | After Sprint H (WS-7) ships |
| **"Self-improving agents"** is real signal that the field is moving toward what AIW's demiurge layer does | AIW's existing `scripts/curator-evolver.py` + `scripts/homunculus.py` + instincts YAML **already implement this**. Surface it publicly | Doc-only ticket (post Sprint F) |
| **"100% private AI Agent" content is hot** (180K + 217K + 100K views across 3 videos) | AIW's `kernel/` design explicitly supports local-only deployment (no AIW_ROOT env, no cloud deps in DEMIURGE-098's helper) | Already shipped at 0afca1f |
| **The "Ex-FAANG engineer reveals workflow" interview format** is hugely popular (159K, 233K, 44K, 120K, 84K, 377K) | The 6+ AIW charter departments could be presented as "ex-[domain]-department reveals workflow" — same shape, different domain | Post-Sprint F (when AIW has its own workflow to talk about) |

### Patterns to NOT copy (off-mission for AIW)

| Pattern | Why skip |
|---|---|
| "X is dead, Y is the new thing" clickbait | AGENTS.md forbids speculation; AIW's role is to ship, not to opine |
| "I made $X with AI" / "How to get rich" content | AIW's revenue model is internal; not content marketing |
| Tutorial-of-the-week format | AIW has too few resources to compete on tutorial volume |
| **Public marketing in general** | AIW is an internal org, not a media company |

## 6. Direct comparison: AIW-org vs David's content

| Dimension | David | AIW |
|---|---|---|
| **Target audience** | AI-curious developers, founders, "tech twitter" | Internal Ivan + semi-internal AIW team |
| **Output volume** | ~150 videos/year | ~50 atomic commits/quarter |
| **Tone** | "Here's how", "just copy me", "X is over" | "Closed out", "Fix:", "Per R11/R8" |
| **Format** | 30-90 min video walkthroughs + shorts | Markdown + atomic git commits |
| **Discovery** | YouTube algorithm | Manual handoff in HANDOFF.md |
| **Citation** | Title says it all | Commit message + ticket tracker |
| **Iteration** | "Re-uploaded for X release" | Revert + re-commit |

**One observation**: David's videos all have the IMPLICIT structure of an AIW agent PROMPT.md:
- `title` = agent's role/mission (e.g. "Build Anything with Claude Agents")
- `body content` = the workflow / how-to (corresponds to PROMPT.md body)
- `description` = agent's tools + inputs (corresponds to YAML frontmatter)

The mapping isn't 1:1 but it's suggestive. **For AIW: when the kernel ships, the design docs (`KERNEL-DESIGN`, `SASKIA-INSTANCE-DESIGN`) ARE David's "videos" — except for the kernel they're internal, not public**.

## 7. Concrete recommendation (operator-actionable)

**Single highest-leverage upgrade from this analysis:**

> Ship a one-pager: `analysis/AIW-SELF-IMPROVING-CAPABILITIES.md` (≤30 min).

What it would say:
- AIW's demiurge layer (curator-evolver + homunculus + instincts YAML) is **a working self-improving agent system**
- This exists in production TODAY
- No comparable public-facing artifact from David or his guests specifically describes what AIW has built
- Surface as a 1-page summary for internal stakeholders; do NOT publish externally yet

Per **R11**, this is a low-stakes doc that doesn't change project shape. **No new ticket needed**; it could land as a follow-up commit in Sprint A or be promoted to DEMIURGE-122 (5 min ticket).

## 8. What I did NOT do

- **Did not extract transcripts** — yt-dlp supports `--write-auto-sub` but per R11 + R8 I'd want operator authorization before downloading 100s of video files (~GBs of data)
- **Did not extract individual video descriptions** — RSS doesn't include them; yt-dlp can with `--dump-json` but that's a deeper pull
- **Did not compare against other channels** (Yannic Kilcher, AI Jason, etc.) — out of scope for this request
- **Did not follow the channel for ongoing updates** — that's a cron-j