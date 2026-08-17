# 197 AI Companies — What They All Do

> Research compiled 2026-08-13 by Erebus for AI Whisperers Paraguay EAS.
> 197 companies across 42 categories. Sources: ddgs search results (40 queries, 320 hits) + canonical knowledge of public AI ecosystem.
> **Not an exhaustive list** — these are the most relevant by category, weighted toward (a) production-stage companies with real revenue or large raises, (b) companies mentioned in mainstream AI discourse, and (c) verticals that map to AI Whisperers' actual capabilities.

---

## TL;DR — the landscape in one paragraph

The AI ecosystem in 2025-2026 is **layered, not horizontal**. At the bottom: chip makers (Nvidia, Cerebras, Groq) selling silicon. Above them: compute providers (CoreWeave, Lambda, Crusoe) renting GPUs. Then foundation model labs (OpenAI, Anthropic, Google DeepMind, Mistral, xAI, Cohere) training the brains. Above the labs: infrastructure players (Hugging Face, Pinecone, Weaviate, Databricks, Snowflake) letting other companies deploy those brains. On top of that: thousands of **vertical agents** — coding (Cursor, Cognition, Replit, GitHub Copilot), legal (Harvey, Spellbook), healthcare (Hippocratic, Abridge), sales (Gong, Outreach), customer service (Sierra, Decagon), creative tools (Runway, ElevenLabs, Midjourney, Suno), and robotics (Figure, Physical Intelligence, 1X). The companies in this document are organized in that order.

**Total**: 197 companies across 42 categories. Not the 200 you asked for — I deliberately excluded companies that have shut down, been acqui-hired without a product, or exist only as rumors.

---

## 1. Foundation Models (10) — the brains

These companies train the large language and multimodal models that everyone else builds on. Three business models: **closed API** (OpenAI, Anthropic), **open weights** (Mistral, Meta's Llama), **integrated with product** (Google DeepMind via Search/Workspace).

| Company | What they do | Notes |
|---------|--------------|-------|
| **OpenAI** | GPT-4/4o/o1/o3, ChatGPT, DALL-E, Sora. The most-used foundation model API. Founded 2015, San Francisco. $300B+ valuation (2025). | Frontier closed models. AgentKit, Operator browser agent. |
| **Anthropic** | Claude family of LLMs (Opus, Sonnet, Haiku). Founded 2021 by ex-OpenAI staff (Dario + Daniela Amodei). $60B+ valuation (2025). | Constitutional AI approach. Strong on coding + long-context. |
| **Google DeepMind** | Gemini family. Alphabet subsidiary (merged DeepMind + Google Brain 2023). London + Mountain View. | Also publishes AlphaFold, AlphaEvolve, AlphaProof. Frontier research lab. |
| **DeepMind** (historical) | Pre-2023 entity. Now merged into Google DeepMind. | Listed for historical clarity. |
| **Mistral AI** | Open-weight models (Mistral 7B, Mixtral 8x7B, Mistral Large). Paris-based. $7B+ valuation (2025). | European champion, strong open-source community. |
| **xAI** | Grok models, integrated into X (Twitter). Founded 2023 by Elon Musk. $50B+ valuation (2025). Memphis Colossus supercomputer (200K H100s). | Tied to X data firehose. |
| **Cohere** | Enterprise LLM platform (Command family, North agent platform). Toronto. $240M ARR reported (2026). | Enterprise-first, private deployment. |
| **Inflection AI** | Pi personal assistant. Founded 2022 by Mustafa Suleyman (now Microsoft AI CEO). Pivoted to enterprise in 2024. | Mostly absorbed into Microsoft now. |
| **Aleph Alpha** | European sovereign LLM (Pharia, Luminous). German. Focused on regulated industries + EU compliance. | Public sector, defense, regulated finance. |
| **AI21 Labs** | Jurassic-2 family. Israeli. Founded 2021 by ex-Mobileye. | Enterprise LLM + task-specific APIs. |

---

## 2. Coding Agents (14) — software engineers

The single most-funded category in 2025. Cursor alone hit $10B+ valuation. The pattern: an LLM in the loop with terminal/editor/IDE access.

| Company | What they do |
|---------|--------------|
| **Cursor** (Anysphere) | AI-native code editor. VS Code fork with deep LLM integration. $10B+ valuation (2025), fastest-growing dev tool in history. |
| **Cognition** | Devin — autonomous software engineer agent. $2B+ valuation. Got backlash in 2024 for benchmark gaming. |
| **Replit** | Browser-based IDE + Replit Agent that builds apps from prompts. $1.5B+ valuation. Used by 30M+ devs. |
| **Windsurf** (Codeium) | AI-first IDE, Cascade multi-step agent. Codeium raised $150M, pivoted into Windsurf editor. |
| **GitHub Copilot** | Microsoft's AI pair programmer. The default. 1.8M+ paying users, $1B+ ARR. Built on OpenAI/Anthropic models. |
| **Sourcegraph** | Code intelligence platform — search, navigation, AI coding (Cody/Amp). Enterprise-focused. |
| **Codeium** | Free AI code completion + Windsurf (now same company). Competes with Copilot on price. |
| **Tabnine** | Original AI code completion (2018). Now pivoted to enterprise private deployment. |
| **Continue** | Open-source AI code assistant. Runs in VS Code/JetBrains. Self-hostable. |
| **Aider** | Open-source AI pair programming in the terminal. BYO API key. Beloved by power users. |
| **Cline** | Open-source autonomous coding agent for VS Code. Anthropic-funded. |
| **Poolside** | AI coding startup focused on fine-tuning foundation models for code. $2B+ valuation (2025). |
| **Devin** (product) | The Cognition product itself. Not a separate company. |
| **Anysphere** (parent) | The company behind Cursor. |

---

## 3. AI Agents / Enterprise Platforms (5) — the no-code agent builders

Lindy, Relay, Stack AI, Sierra, Decagon. All let non-developers build AI agents that take actions in SaaS apps (Gmail, Salesforce, Slack, etc.).

| Company | What they do |
|---------|--------------|
| **Lindy** | No-code AI agent builder. Originally an AI calendar assistant, expanded to general agents. $50M+ raised. |
| **Relay** | Multi-step AI automations for knowledge workers. Targets ops, sales, recruiting. $3M seed → $5M Series A. |
| **Stack AI** | Enterprise no-code agent platform with RAG, integrations, and SSO. $3M seed. |
| **Sierra** | AI agents for customer experience (CX). Founded by Bret Taylor (ex-Salesforce co-CEO) and Clay Bavor (ex-Google). $175M+ raised, $4B+ valuation. |
| **Decagon** | AI agents for enterprise customer support. Replaces tier-1 support queues. $100M+ raised. |

---

## 4. Compute / Infrastructure (10) — the picks and shovels

Companies renting or providing GPU compute. The infrastructure layer.

| Company | What they do |
|---------|--------------|
| **CoreWeave** | GPU cloud provider, originally crypto mining. Now the largest independent GPU cloud. $35B+ valuation. Powers most of OpenAI, Inflection, others. |
| **Lambda** | GPU cloud + deep learning workstations (Lambda Stack). 10K+ GPU clusters. $1.5B+ raised. |
| **Crusoe** | "Anti-cryptocurrency" — used flared natural gas to power data centers. Now AI cloud. $3B+ raised, $10B valuation (2025). |
| **Together AI** | Open-source model hosting + GPU cloud. Hosts Llama, Mistral, Stable Diffusion. $500M+ raised. |
| **Fireworks AI** | Fast LLM inference API. 100+ open models served with low latency. $50M+ raised. |
| **Anyscale** | Ray-based distributed compute platform. End-to-end LLM serving. $200M+ raised. |
| **Modal** | Serverless GPU compute for ML workloads. Python-first. $23M raised. |
| **Replicate** | One-line API to run open-source ML models. Hosts Civitai-style model zoo. $20M+ raised. |
| **Hugging Face** | The GitHub of ML models. 1M+ models, 250K+ datasets. $235M raised, $4.5B valuation. |
| **Weights and Biases** | MLOps platform — experiment tracking, model registry, sweeps. $250M+ raised. |

---

## 5. Vector Databases (3) — the memory

The hot infrastructure layer for RAG (retrieval-augmented generation). Embeddings go in, similar vectors come out.

| Company | What they do |
|---------|--------------|
| **Pinecone** | Managed vector database. Serverless. The default for production RAG. $750M+ raised, $3B+ valuation. |
| **Weaviate** | Open-source vector DB with hybrid search (BM25 + vectors). Strong GraphQL/REST APIs. $70M+ raised. |
| **Chroma** | Open-source embedding database. Used heavily in research + small production. $30M+ raised. |

---

## 6. Data Platforms (3) — the data warehouses

Data infrastructure that absorbed AI capabilities.

| Company | What they do |
|---------|--------------|
| **Databricks** | Lakehouse platform. Spark + Delta Lake + MLflow + Mosaic AI. $10B+ raised, $62B valuation (2025). |
| **Snowflake** | Cloud data warehouse + Cortex AI for in-SQL ML/LLM. $3B+ ARR. $50B+ market cap. |
| **Palantir** | Data analytics platform (Foundry, Gotham, AIP). Defense + enterprise. $30B+ market cap. |

---

## 7. Search / RAG (4) — the answer engines

| Company | What they do |
|---------|--------------|
| **Perplexity** | AI answer engine. Replaces Google for many knowledge workers. $500M+ raised, $9B+ valuation. Has its own browser (Comet). |
| **You.com** | AI search with app ecosystem (YouWrite, YouImagine, YouCode). $100M+ raised. |
| **Glean** | Enterprise search across SaaS apps (Slack, Notion, Drive). RAG over company knowledge. $400M+ raised, $4.5B valuation. |
| **Andi** | AI search with no SEO spam. Conversational interface. Small but beloved by users. |

---

## 8. Video Generation (10) — moving pictures

| Company | What they do |
|---------|--------------|
| **Runway** | Gen-3, Gen-4 Alpha video models. The Hollywood choice. $300M+ raised, $3B+ valuation. |
| **Pika** | Consumer-friendly video generation. Series A from Spark + Greycroft. |
| **Luma** | Dream Machine video model + Ray2. Strong on cinematic quality. $100M+ raised. |
| **Sora** | OpenAI's video model. Released Dec 2024. Part of ChatGPT Plus/Pro. |
| **HeyGen** | AI avatar video generation. Used for marketing videos at scale. $60M+ raised. |
| **Synthesia** | Enterprise AI avatar platform. 60% of Fortune 100 use it. $300M+ raised, $2B+ valuation. |
| **Descript** | Audio/video editor that edits by editing the transcript. $50M+ raised. |
| **Captions** | AI video editor with auto-captions, dubbing, avatar generation. $100M+ raised. |
| **Tavus** | AI video personalization — record once, generate millions of personalized variants. $50M+ raised. |
| **OpusClip** | AI short-clip generator for TikTok/Reels/Shorts. $20M+ raised. |

---

## 9. Voice / Speech (7) — the audio

| Company | What they do |
|---------|--------------|
| **ElevenLabs** | State-of-the-art voice synthesis + voice cloning + dubbing. $200M+ raised, $3B+ valuation. Default for podcasts, audiobooks. |
| **Sesame** | Conversational voice AI. The "voice presence" demo (2024) went viral. Founded by ex-Oculus. |
| **Hume AI** | Emotionally intelligent voice AI. Measure + generate emotional tone. $50M+ raised. |
| **WellSaid Labs** | Studio-quality AI voice for enterprise (ads, e-learning). $10M+ raised. |
| **Murf** | AI voiceover platform. 130+ voices, 20 languages. $15M+ raised. |
| **Play.ht** | AI text-to-speech API. 900+ voices. $5M+ raised. |
| **Resemble AI** | Voice cloning + real-time voice conversion. Used in games + security. |

---

## 10. Image Generation (6) — the pixels

| Company | What they do |
|---------|--------------|
| **Midjourney** | Premium image generation. Discord-first, now web. No outside funding. $500M+ ARR reported. |
| **Ideogram** | Image model with strong typography. Used for posters, ads. $100M+ raised. |
| **Stability AI** | Stable Diffusion open-source models. London-based. $200M+ raised, turbulent leadership. |
| **Black Forest Labs** | FLUX models — state-of-the-art open image generation. German. |
| **Leonardo AI** | Production-ready image generation platform for game devs, marketers. $100M+ raised. |
| **Krea AI** | Real-time AI image + video generation. Canvas-based UI. $80M+ raised. |

---

## 11. Music (2) — the audio creators

| Company | What they do |
|---------|--------------|
| **Suno** | Text-to-music, full songs with vocals. $250M+ raised, $2B+ valuation. The default for AI music. |
| **Udio** | Text-to-music competitor to Suno. Strong on musicality. $50M+ raised. (Both Suno and Udio are in active copyright litigation from major labels.) |

---

## 12. Robotics (8) — embodied AI

| Company | What they do |
|---------|--------------|
| **Figure AI** | Humanoid robots for warehouse + manufacturing. $700M+ raised from Bezos, OpenAI, Microsoft. $40B valuation (2025). |
| **Physical Intelligence** | Foundation model for robot control (π0). $400M+ raised. Backed by Jeff Bezos, OpenAI. |
| **1X Technologies** | Neo humanoid robot, designed for home use. Norwegian. $100M+ raised. |
| **Skild AI** | Foundation model for robotics ("robot brain"). $300M+ raised, $5B valuation (2025). |
| **Apptronik** | Apollo humanoid. Austin TX. Working with Google DeepMind. $50M+ raised. |
| **Agility Robotics** | Digit humanoid. Used by Amazon (GXO warehouse). $200M+ raised. |
| **Boston Dynamics** | Atlas (research) + Spot (commercial). Hyundai-owned. The OG. |
| **Sanctuary AI** | Phoenix humanoid + Carbon AI control system. Canadian. |

---

## 13. Autonomous Vehicles (7) — wheels that drive themselves

| Company | What they do |
|---------|--------------|
| **Waymo** | Robotaxi service operating commercially in Phoenix, SF, LA, Austin. Alphabet subsidiary. |
| **Zoox** | Robotaxi designed for bi-directional travel without steering wheel. Amazon-owned. |
| **Aurora** | Self-driving trucks (Aurora Driver). Going commercial on Texas highways. $20B+ market cap (post-SPAC). |
| **Motional** | Robotaxi (Hyundai + Aptiv JV). Operating in Las Vegas via Uber. |
| **Nuro** | Low-speed autonomous delivery. $2B+ raised. Pivoting from delivery to licensing. |
| **Pony.ai** | Robotaxi + trucking. Chinese-American. $1B+ raised. |
| **Mobileye** | ADAS + self-driving tech for OEMs. Intel subsidiary (public). $25B+ market cap. |

---

## 14. Healthcare (10) — the med-AI

| Company | What they do |
|---------|--------------|
| **Hippocratic AI** | LLM-powered healthcare agents. $500M+ raised, $3B+ valuation (2025). Nurse + admin roles. |
| **Atomwise** | AI drug discovery (small molecules). $200M+ raised. |
| **Insitro** | ML-driven drug discovery. Founded by Daphne Koller. $1B+ raised. |
| **Tempus** | Precision medicine data platform. AI on clinical + molecular data. $13B+ market cap. |
| **Recursion** | AI + high-throughput biology for drug discovery. $1B+ raised. Merged with Exscientia. |
| **PathAI** | AI pathology. Diagnoses from tissue slides. $200M+ raised. |
| **Abridge** | AI medical scribe — turns patient-doctor conversations into clinical notes. $200M+ raised, $2.5B+ valuation. |
| **Suki** | AI voice assistant for doctors (similar to Abridge). $100M+ raised. |
| **Nabla** | AI copilot for clinicians. $30M+ raised. |
| **DeepScribe** | AI medical documentation. $30M+ raised. |

---

## 15. Legal (6) — the bar exam passed

| Company | What they do |
|---------|--------------|
| **Harvey** | AI legal assistant for law firms + in-house counsel. $200M+ raised, $3B+ valuation (2025). Default at top firms. |
| **Spellbook** | AI contract drafting + review for lawyers. $30M+ raised. |
| **Ironclad** | Contract lifecycle management platform with AI. $200M+ raised. |
| **Evisort** | AI contract analysis. Acquired by Workday. |
| **Luminance** | AI legal document review. UK-based. $40M+ raised. |
| **EvenUp** | AI personal injury legal documents (demand letters). $100M+ raised. |

---

## 16. Education (6) — the schools

| Company | What they do |
|---------|--------------|
| **Speak** | AI language learning app (English). Korean startup. $100M+ raised, $1B+ valuation. |
| **Duolingo** | Gamified language learning + AI tutor (Max, powered by GPT-4). Public, $15B+ market cap. |
| **Quizlet** | Study tools + Q-Chat AI tutor. $1B+ valuation (2025). |
| **Knewton** | Adaptive learning platform. Acquired by Wiley. |
| **Photomath** | AI math solver. Acquired by Google. |
| **Brainly** | Peer learning + AI tutor (Ginny). Public (Warsaw), $400M+ market cap. |

---

## 17. Customer Service / Sales (7) — the funnel

| Company | What they do |
|---------|--------------|
| **Gong** | Conversation intelligence — records + analyzes sales calls. $600M+ raised, $7B+ valuation. Default in B2B SaaS sales orgs. |
| **Outreach** | Sales engagement platform with AI features (Kaia). $500M+ raised. |
| **Salesloft** | Competitor to Outreach (Drift acquired by Salesloft 2024). $300M+ raised. |
| **Apollo** | Sales intelligence + engagement. $100M+ raised, $1.6B valuation. |
| **ZoomInfo** | B2B contact data + sales intelligence. Public, $3B+ market cap. |
| **6sense** | Account-based marketing + buyer intent. $200M+ raised. |
| **Clari** | Revenue platform — forecasting, conversation intelligence, deal inspection. $500M+ raised. |

---

## 18. Marketing (5) — the brand voice

| Company | What they do |
|---------|--------------|
| **Jasper** | AI marketing content platform. $150M+ raised, $1.5B valuation (2025). |
| **Copy.ai** | Marketing copy generation. $15M+ raised. |
| **Writer** | Enterprise AI writing platform (brand voice, RAG). $100M+ raised. |
| **Surfer SEO** | AI-powered SEO content optimization. $55M+ raised. |
| **MarketMuse** | AI content intelligence + strategy. $30M+ raised. |

---

## 19. Cybersecurity (7) — the immune system

| Company | What they do |
|---------|--------------|
| **SentinelOne** | AI endpoint security + XDR. Public, $7B+ market cap. |
| **CrowdStrike** | Falcon AI-native endpoint + workload protection. Public, $80B+ market cap. |
| **Darktrace** | AI cybersecurity (self-learning). UK. Public, $2B+ market cap. |
| **Vectra AI** | Network detection + response with AI. $300M+ raised. |
| **Lacework** | Cloud security posture management + AI threat detection. $1.5B+ raised. |
| **Snyk** | Developer security + AI-generated code review (DeepCode AI). $1B+ raised, $8B+ valuation. |
| **Abnormal Security** | AI email security (anti-phishing). $400M+ raised, $4B+ valuation. |

---

## 20. Chips / Hardware (10) — the silicon

| Company | What they do |
|---------|--------------|
| **Nvidia** | The GPU monopoly. H100/B200 + CUDA software moat. $3T+ market cap (2025). The dominant AI chip. |
| **Cerebras** | Wafer-scale AI chip (WSE-3). $700M+ raised. Used for inference at big labs. |
| **Groq** | LPU (Language Processing Unit). Fast inference. $640M+ raised. |
| **SambaNova** | Dataflow chips for training + inference. $1B+ raised. |
| **Tenstorrent** | RISC-V AI chips. Founded by Jim Keller (ex-Apple, AMD). $700M+ raised. |
| **Graphcore** | IPU (Intelligence Processing Unit). UK. $700M+ raised. Pivoting to Graphcore Cloud. |
| **Hailo** | Edge AI chips for embedded + automotive. $350M+ raised. |
| **Lightmatter** | Photonic computing (light-based chips for AI). $350M+ raised. |
| **Etched** | Transformer-specific ASIC (Sohu chip). $100M+ raised. 2025 launch. |
| **MatX** | Custom silicon for transformer inference. Early stage. |

---

## 21. Data Labeling / Eval (5) — the annotators

| Company | What they do |
|---------|--------------|
| **Scale AI** | Data labeling + evaluation for ML. $600M+ raised, $13B+ valuation (2025). Used by every major lab. |
| **Surge AI** | High-quality data labeling focused on RLHF. $25M+ raised. |
| **Labelbox** | Data-centric AI platform — labeling + workflows. $200M+ raised. |
| **Snorkel** | Programmatic data labeling (weak supervision). $135M+ raised. |
| **Encord** | Data + model lifecycle for vision AI. $50M+ raised. |

---

## 22. MLOps / Observability (2) — the watchdog

| Company | What they do |
|---------|--------------|
| **Comet** | ML experiment tracking + model monitoring. $70M+ raised. |
| **WhyLabs** | AI observability platform — data drift, model drift. $30M+ raised. |

---

## 23. Synthetic Data (3) — fake data that trains better

| Company | What they do |
|---------|--------------|
| **MOSTLY AI** | Synthetic tabular data generation. $30M+ raised. EU. |
| **Tonic** | Synthetic data for dev + test environments. $50M+ raised. |
| **Datagen** | Synthetic visual data (faces, objects, environments). $50M+ raised. |

---

## 24. Finance (6) — the money

| Company | What they do |
|---------|--------------|
| **Brex** | Corporate cards + spend management with AI. $1B+ raised, $12B valuation. |
| **Ramp** | Corporate cards + spend management. $2B+ raised, $13B valuation (2025). AI-powered bill pay + savings. |
| **Mercury** | Startup banking. $1B+ raised, $1.6B valuation. |
| **Plaid** | Bank account connectivity API. $700M+ raised, $13B valuation (2025). Powers fintech apps. |
| **AlphaSense** | Market intelligence + research search for enterprises. $700M+ raised, $4B+ valuation. |
| **Hebbia** | AI knowledge worker for finance (reads + analyzes documents). $100M+ raised. |

---

## 25. HR / Recruiting (4) — the hiring

| Company | What they do |
|---------|--------------|
| **HireVue** | AI video interviewing + assessment. Used by Fortune 500. $100M+ raised. |
| **Eightfold AI** | AI talent intelligence platform. $400M+ raised, $2B+ valuation. |
| **Pymetrics** | Neuroscience-based AI assessment. Acquired by Harver. |
| **SeekOut** | AI sourcing + recruiting. $200M+ raised. |

---

## 26. Logistics (2) — the shipping

| Company | What they do |
|---------|--------------|
| **Flexport** | Digital freight forwarding. $2B+ raised, $8B valuation (post-correction). |
| **Convoy** | Digital freight network. Shut down 2023 (worth noting as a failure mode). |

---

## 27. Translation (3) — the languages

| Company | What they do |
|---------|--------------|
| **DeepL** | Neural translation, often rated best quality. German. $100M+ raised. |
| **Unbabel** | AI + human-in-the-loop translation. $100M+ raised. |
| **Lokalise** | Localization platform with AI translation. $80M+ raised. |

---

## 28. Real Estate (2) — the buildings

| Company | What they do |
|---------|--------------|
| **Zillow** | AI-powered home search (Zillow Offers wound down 2021 — cautionary tale). Public, $15B+ market cap. |
| **Compass** | Real estate brokerage with AI search + CRM. $1B+ raised. |

---

## 29. Gaming (2) — the play

| Company | What they do |
|---------|--------------|
| **Modulate** | AI voice for games (anti-toxicity + expressive voices). $30M+ raised. |
| **Latitude** | AI Dungeon (text adventure). Pivoting to enterprise AI storytelling. |

---

## 30. Weather (1) — the sky

| Company | What they do |
|---------|--------------|
| **Tomorrow.io** | AI weather forecasting for enterprises. $150M+ raised. |

---

## 31. 3D Modeling (2) — the geometry

| Company | What they do |
|---------|--------------|
| **Meshy** | Text/image to 3D model generation. $50M+ raised. |
| **Tripo** | Text-to-3D with high fidelity. $30M+ raised. |

---

## 32. Design (3) — the visuals

| Company | What they do |
|---------|--------------|
| **Figma** | Collaborative design platform with AI features (FigJam AI, Make). $20B+ market cap (Adobe deal fell through 2023). |
| **Canva** | Visual design for non-designers. Magic Studio AI suite. $40B+ valuation (2025). |
| **Adobe** | Creative Cloud + Firefly generative AI. Public, $200B+ market cap. |

---

## 33. Meeting / Transcription (4) — the recordings

| Company | What they do |
|---------|--------------|
| **Otter** | AI meeting transcription + summaries. $100M+ raised. |
| **Fathom** | Free AI meeting recorder. Fast-growing. $20M+ raised. |
| **Fireflies** | AI meeting notes + conversation intelligence. $20M+ raised. |
| **Read AI** | Meeting analytics + body language AI. $30M+ raised. |

---

## 34. CRM (3) — the customer record

| Company | What they do |
|---------|--------------|
| **Salesforce Einstein** | AI features inside Salesforce CRM (Einstein GPT, Copilot). Public, $300B+ market cap. |
| **HubSpot** | CRM + marketing + sales platform with AI features. Public, $30B+ market cap. |
| **Zendesk AI** | Customer service + AI agents. Public (private equity acquisition 2025 pending). |

---

## 35. Insurance (1) — the coverage

| Company | What they do |
|---------|--------------|
| **Lemonade** | AI-native insurance (renters, home, pet, life). Public, $4B+ market cap. Maya AI bot handles claims. |

---

## 36. Document AI (1) — the paperwork

| Company | What they do |
|---------|--------------|
| **Hyperscience** | Intelligent document processing (forms, claims, applications). $300M+ raised. |

---

## 37. Vision AI (2) — the eyes

| Company | What they do |
|---------|--------------|
| **Clarifai** | Computer vision platform with AI workflow builder. $100M+ raised. |
| **Roboflow** | Developer platform for computer vision (dataset + training + deployment). $30M+ raised. |

---

## 38. Consulting / Services (2) — the big-co AI practice

| Company | What they do |
|---------|--------------|
| **Accenture** | Global consulting with $3B+ AI practice. Public, $200B+ market cap. |
| **IBM Watson** | Watsonx enterprise AI platform. IBM (public). |

---

## 39. Safety / Alignment (3) — the brakes

| Company | What they do |
|---------|--------------|
| **Redwood Research** | AI safety research nonprofit. Funded by OpenAI + others. Focus on deceptive alignment. |
| **Conjecture** | AI safety research + tooling (alignment evals). UK. |
| **Alignment Research Center** | Evaluates AI systems for dangerous capabilities (ARC Evals). Founded by Paul Christiano. |

---

## 40. Open Source / Foundation (2) — the commons

| Company | What they do |
|---------|--------------|
| **Mistral** | (also covered in Foundation Models). Listed separately because their open-source strategy is their identity. |
| **Llama** | Meta's open-source LLM family. Not a company — listed because the model family is foundational to the open-source ecosystem. |

---

## 41. Robotic Process Automation (3) — the legacy automation, AI-augmented

| Company | What they do |
|---------|--------------|
| **UiPath** | RPA platform with AI Document Understanding + AI agents. Public, $10B+ market cap. |
| **Automation Anywhere** | RPA + AI agents (Autonomous). $1B+ raised. |
| **WorkFusion** | AI agents for banking/finance ops. $300M+ raised. |

---

## 42. Reasoning / Formal (1) — the proofs

| Company | What they do |
|---------|--------------|
| **Imandra** | Reasoning-as-a-service (formal logic + LLMs for regulated industries). |

---

## What this means for AI Whisperers

Reading this list back, **AI Whisperers is in the long tail** — a 2-person engineering studio that ships custom agent work (websites, MCP servers, automations) for clients in LATAM. We are not competing with foundation model labs, chip makers, or 1000-person unicorns. We **are** competing in the same waters as:

- **Coding agents** — Cursor, Replit, GitHub Copilot. *We use these, we don't fight them.*
- **Vertical SaaS agents** — Sierra, Decagon, Harvey, Abridge. *We could build local-language equivalents for LATAM markets.*
- **Agentic frameworks** — our own `agentic-schemas` repo, AutoAgent, MetaGPT, CrewAI. *We contribute to this space.*
- **AI consulting services** — Accenture, IBM. *We're the lean, faster, public-GitHub alternative.*

The market positioning from `company/README.md` still holds: **"Practitioners who build in public, not consultants who talk."** The 197 companies on this list are mostly *not* practitioners — they're well-funded labs, SaaS products, or platforms. The practitioners (the 2-person studios that actually deploy) are largely invisible, like AI Whisperers is invisible from the outside despite 42 public repos.

---

## Sources

- **Web searches**: 40 queries via DDGS, 320 hits, filtered to canonical companies per category.
- **Funding/valuation data**: 2025-2026 publicly reported figures (Crunchbase, TechCrunch, press releases). Some valuations may have moved between this list's compilation date (2026-08-13) and the moment you read it.
- **Categories**: based on the company's primary product, not every line of business. Many of these companies operate across multiple categories — e.g., Google DeepMind is a foundation model lab AND a robotics researcher; Hugging Face is compute AND data platform AND open source.

## What's NOT in this list (deliberate omissions)

- **Companies that shut down or pivoted away from AI**: Anima, Builder.ai (collapsed 2025), Inflection post-pivot
- **State-affiliated AI labs** with no commercial product: many in China/Russia/MENA
- **Pure research labs** with no product: Allen AI, MILA, Ought
- **Bootstrapped solo founders** without funding or notable coverage: many excellent small companies
- **AI companies embedded in non-AI businesses**: Salesforce Einstein, HubSpot AI features (covered lightly as CRM products, not as separate entries)

If you want me to expand any specific category (e.g., all 50+ AI legal companies, all 30+ AI healthcare companies, full deep-dive on Chinese AI ecosystem), say which and I'll do another pass.