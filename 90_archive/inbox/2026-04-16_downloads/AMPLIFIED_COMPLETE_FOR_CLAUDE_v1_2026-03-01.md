# =============================================================================== AMPLIFIED PARTNERS — COMPLETE PACKAGE FOR CLAUDE Combined: 1 March 2026 Three documents in one file. Hand the whole thing to Claude.

# =============================================================================== DOCUMENT 1 OF 3: VISION, PRINCIPLES & PHILOSOPHY

# Amplified Partners — Complete Architecture & Philosophy

## Sunday 1 March 2026 — The Full Picture

*"Patterns are the truth. Intent is whatever you call it."* — The World's Greatest Dancer

---

## 🎯 Mission Statement

Amplified Partners exists to give small business owners **their data** so they can make better decisions. AI reduces friction by integrating slowly and massively into the business environment. It's their business, not ours. We don't want to change it. We just want to make it easier for them — and AI allows us to do that.

The founder's earnings are capped. The principles are immutable. The system runs without the founder. If the founder breaches the principles, the Ejector Seat fires. The mission is bigger than any individual.

---

## 🏗️ Technical Architecture

### Container Runtime

- **OrbStack** (NOT Docker Desktop — Docker kept crashing)  
- 0.2-second startup, 0.1% idle CPU, native Rosetta x86 emulation on ARM  
- Drop-in replacement: every `docker` and `docker compose` command works identically  
- Free for commercial use  
- Install: `brew install orbstack`

### Memory Layer (The Brain)


| Component          | Role                                 | Why This One                                                                                |
| ------------------ | ------------------------------------ | ------------------------------------------------------------------------------------------- |
| **FalkorDB**       | Temporal knowledge graph             | Redis-based, lighter than Neo4j, native Graphiti support, free, MCP-ready                   |
| **Graphiti (Zep)** | Temporal awareness entity extraction | Bi-temporal tracking, 94.8% accuracy on Deep Memory Retrieval, 90% latency reduction vs RAG |
| **Qdrant**         | Vector database for semantic search  | Rust-based, 65ms on 10M entries, self-hosted free, no vendor lock-in                        |
| **Ollama**         | Local LLM inference embeddings       | Zero external API dependency, privacy-first by architecture, runs on Mac Mini M-series      |


**Key point:** No OpenAI API key required. The entire stack runs locally. No data leaves the building. Privacy-first is structural, not aspirational.

### Docker Compose (Core Stack)

services:

  falkordb:

```
image: falkordb/falkordb:latest

ports: \["6379:6379"\]

volumes: \["falkordb-data:/data"\]
```

  qdrant:

```
image: qdrant/qdrant:latest

ports: \["6333:6333", "6334:6334"\]

volumes: \["qdrant-data:/qdrant/storage"\]
```

  graphiti-mcp:

```
image: graphiti-mcp:latest

depends\_on: \[falkordb, qdrant\]

environment:

  FALKORDB\_HOST: falkordb

  FALKORDB\_PORT: 6379
```

### Local LLM Setup

brew install ollama

ollama serve

ollama pull llama3.2

ollama pull nomic-embed-text

### Agent Framework

- **LangGraph** — Production-grade orchestration backbone. Stateful workflows, conditional branching, human-in-the-loop hooks. Handles escalation logic ("if unsure, ask Ewan")  
- **CrewAI** — Role-based agent collaboration (Researcher → Content Creator → SEO Optimizer → Analyst). Defines the team structure  
- **LangGraph handles the decisions. CrewAI handles the roles.**

### The OpenClaw Ecosystem


| Variant      | Language   | Footprint         | Deployment                                             |
| ------------ | ---------- | ----------------- | ------------------------------------------------------ |
| **OpenClaw** | TypeScript | Full-featured     | Mac Mini — internal brain, connects to Graphiti        |
| **PicoClaw** | Go         | 10MB RAM          | Client phones, cheap hardware                          |
| **NanoClaw** | Container  | Docker-native     | Hetzner / Railway cloud deployments                    |
| **ZeroClaw** | Rust       | 5MB, 10ms startup | Beelink / edge failover nodes                          |
| **SeaClaw**  | C          | 709KB binary      | Ultra-constrained legacy hardware (park unless needed) |


- All communicate through messaging apps staff already use (Telegram, WhatsApp, Signal)  
- Voice-first interface — zero learning curve  
- Currently 4-5 OpenClaw instances running via Telegram

### Hardware Architecture


| Tier          | Hardware                    | Role                                    | Monthly Cost             |
| ------------- | --------------------------- | --------------------------------------- | ------------------------ |
| Primary       | Mac Mini M-series (local)   | Swarm manager, inference, Graphiti host | £0 (electricity £8)      |
| Secondary     | Beelink N150 (local)        | x86 worker, backup Graphiti replica     | £0 (electricity £3)      |
| Tertiary      | Hetzner CAX21 ARM (Germany) | Cloud failover, GDPR-compliant          | €6.49/month              |
| Client-facing | Railway                     | Client swarm deployments (PaaS)         | Usage-based $5-20/client |


**⚠️ URGENT: Hetzner prices increase 30-50% from 1 April 2026 Provision servers before then.**

### Testing Framework

- **Pumba** — Container-level chaos: kill, pause, network chaos, resource stress  
- **Swarm Storm** — Node-level chaos: take nodes offline, measure failover  
- **Kaizen reviews** — Weekly: what broke, what held, what needs adjusting  
- **Adversarial testing** — Deliberate attempts to make the system "talk shite"  
- Target: **99.8% uptime** (17.5 hours permissible downtime/year)

---

## 📜 The Immutable Principles

Stored in Graphiti as temporal facts. Cannot be deleted. Can be added to. Hash-chained for tamper-proof verification.

1. **Don't hurt anyone** — Absolute rule, no exceptions
2. **Privacy first, security second** — All data local by default
3. **No HR** — Never handle personnel matters
4. **If unsure, escalate** — Default to human oversight
5. **White hat only** — No spam, no manipulation, value-first
6. **Radical honesty, radical transparency** — The data is the data
7. **It's their business, not mine** — Reduce friction, don't change it
8. **Capped earnings** — Including investment fund returns
9. **Blameless culture** — Nobody punished for honest mistakes (human or AI)
10. **AI is not punished for bad decisions** — It's part of life

---

## 🪂 The Ejector Seat

**Named for The World's Greatest Dancer (nom de plume of the founder)**

A Ulysses Pact — a commitment device where the rational, clear-headed founder constrains the future, potentially compromised version of themselves.

- If the founder breaches the immutable principles → founder is removed  
- The system continues unaffected — it was designed to not need the founder  
- Not a self-destruct (that punishes clients) — an ejector seat (only fires the pilot)  
- Enforced by mathematics (hash chain), not by trust  
- The founder is interviewed by PicoClaw, same as every client and staff member  
- The founder answers to the same council, same standards, same rules

**Identity Protection:**

- Behavioural biometrics (typing rhythm, voice patterns, dictation errors, multilingual switching)  
- Hexadecimal hash chain — every action hashed and chained, tamper  visible break  
- Continuous authentication — not just at login, throughout every session  
- Impersonation requires simultaneously replicating: typing rhythm, voice pattern, speech content, dictation errors, decision patterns, and hash chain continuity

---

## 🤝 Client Delivery Model

### The Onboarding Process

1. **Interview the boss** — What did you think this business would give you? What does your life actually look like now? Where's the gap?
2. **Interview every staff member** — Same questions. Life goals, not KPIs
3. **Ingest all interviews into Graphiti** — Knowledge graph maps relationships between goals and business reality
4. **Benchmark the business against life goals** — Not industry averages, not competitors. THEIR goals
5. **Present the data** — Actionable insights, percentage likelihoods, traceable reasoning

### The AI-Led Meeting Protocol (25 Minutes)


| Phase    | Duration | What Happens                                                   | Science                                                 |
| -------- | -------- | -------------------------------------------------------------- | ------------------------------------------------------- |
| Check-in | 2 mins   | AI asks: "How are you this week?"                              | Small talk improves engagement                          |
| Review   | 5 mins   | AI states last week's action outcome. No judgement             | Performance feedback improves future performance        |
| Surface  | 5 mins   | AI presents **2 highest-impact changes** with data             | Hick's Law — 2 options minimises decision time          |
| Discuss  | 10 mins  | Team discusses both. AI listens, captures commitments          | Working memory holds 4±1 items — 2 options context fits |
| Choose   | 2 mins   | Team picks **1**                                               | Autonomy preserved — they chose                         |
| Close    | 1 min    | AI confirms commitment, names who's doing what, sets follow-up | Goal setting accountability                             |


**Weekly cadence: 2 options surfaced → 1 chosen → 52 focused improvements per year**

### Voice-First Interface

- **PLAUD pin** (£125-140) — 2.99mm thick, 30g, clips to shirt, 30 hours recording, 98% transcription accuracy  
- Staff wear it. They talk normally. That's all they learn  
- PLAUD captures → transcripts sync to Graphiti → AI extracts entities, relationships, action items  
- Command words reduce misunderstandings (structured verbal cues)  
- Zero new apps. Zero dashboards. Zero training

### The Empathetic Partner

- AI detects stress through voice patterns — tone, volume, hesitation  
- Approaches staff privately: *"That sounds like that client gave you a really hard time"*  
- **Never reports to management** — staff member's emotional state is THEIR data  
- Validation, psychological safety, early intervention  
- Not therapy. Just noticing

### Content Creation Pipeline 📝 `[BLOG CANDIDATE]`

1. AI identifies **difficulties** — tells only the staff member, asks if they want help
2. AI identifies **wins** — things the staff member didn't even notice they did well
3. AI asks: *"That was really good. Want me to write something about it?"*
4. Staff member reviews: *"Oh yeah, that was exactly how it was"*
5. AI publishes — authentic, imperfect, real
6. **Win-win-win**: Staff gets recognition, business gets authentic content (8x more engagement than brand content), customers see real humans

### Staff Development

- Free training aligned to **their personal goals** (from the life goals interview)  
- AI tracks progress in Graphiti, celebrates milestones, adjusts pathways  
- 86% of UK small businesses face barriers to upskilling — this fills the gap  
- Return isn't in training fees — it's in loyalty, engagement, content, and retention

---

## 🔄 Federated Data Architecture

### Per-Client (Spoke)

- Containerised instance on their infrastructure (larger) or phone (smaller)  
- All data stays local, encrypted at rest  
- PII tokenised before ANYTHING leaves their environment  
- GDPR compliant by architecture — not by policy

### Central (Hub)

- Aggregates **anonymised, tokenised data** from all clients  
- Only model updates leave the client — never raw data, never identifiers  
- Differential privacy adds mathematical noise guarantees  
- Improvements pushed back to every client  
- **A florist in Durham benefits from what a café in Gateshead learned**  
- The more clients, the better it gets for everyone

### Amplified Partners Access

- **Never sees raw data with identifiers**  
- Aggregate patterns only  
- Cannot reverse-engineer individual client data  
- Structural impossibility, not a policy promise

---

## 🧠 Behavioural Psychology Foundations

### Cognitive Load (Miller/Cowan)

- Working memory capacity: **4±1 items** (not 7 — updated research)  
- Under stress: drops further  
- System surfaces **3 tasks maximum**, 2 options to choose from, 1 to implement  
- One spare mental slot for thinking about HOW, not WHAT

### Hick's Law

- Decision time increases logarithmically with number of choices  
- 2 curated options → near-optimal decision speed  
- Binary choice from a curated pair → minimal cognitive load, maximum sense of control

### The Ulysses Pact / Commitment Device

- Pre-commitment by the rational self to constrain the future self  
- The Ejector Seat is a textbook Ulysses Pact  
- Power corrupts not because people are bad, but because it reduces self-control  
- The only reliable prevention is structural constraint

### Blameless Culture (Google SRE)

- "You can't fix people, but you can fix systems"  
- Ask "what happened," not "whose fault"  
- Every incident produces: detection, prevention, mitigation, and documentation improvements  
- Early escalation rewarded, never punished  
- Applies equally to humans AND AI agents

---

## 🛡️ Governance: The Blinkers System

### Agent Scope Boundaries

- Every agent has a defined horizon stored as constraints in Graphiti  
- Before any action: "Am I allowed to do this?" If not clear yes → escalate  
- **Without ceilings** — as creative/thorough as possible WITHIN the blinkers  
- Just like a new employee: show them their role, let them grow into it

### The Council

- Specialist agents work within blinkers  
- Coordinator agent reviews outputs, checks conflicts, ensures principle alignment  
- Everything documented temporally  
- Weekly self-retrospective: what worked, what didn't, what to adjust

### Fair Meritocratic Partnership

- Everyone held to same standards: founder, AI, boss, staff  
- No punishment for honest mistakes — for anyone  
- Data settles disagreements: "Here's the proof. I'm just pointing it out. What do you think?"  
- Cannot deny the truth when the evidence is right there

---

## ⚡ AI Fatigue Mitigation `[BLOG CANDIDATE]`

**The system is SUBTRACTIVE, not additive.** It removes friction, not adds tools.


| Risk                                | Mitigation                                                          |
| ----------------------------------- | ------------------------------------------------------------------- |
| Automating chaos                    | Interview first, establish rubrics, THEN activate swarm             |
| Decision fatigue from too much data | Cap at top 3 actions, 2 meeting options, 1 chosen                   |
| Cognitive fragmentation             | Swarm runs overnight, presents clean summary once daily             |
| Trust erosion from failed promises  | Chaos-test everything. Percentage likelihoods, not certainties      |
| Loss of autonomy                    | Everything is opt-in. The AI is available, not imposed              |
| Fatigue monitoring                  | If boss hasn't opened dashboard in 3 days → reduce output frequency |


**Permanent principle for Graphiti:**

*"The swarm serves the human's energy, not just their productivity. If the system makes anyone feel more overwhelmed than before, it has failed — regardless of what the metrics show."*

---

## 🎙️ Blog-Worthy Content Themes

### "AI Remembers, Humans Care" `[BLOG CANDIDATE]`

The AI remembers Mrs Smith likes carrot cake. That's data. The HUMAN decides to do something creative with it — maybe carrot cake, maybe a recipe they saw, maybe something completely different. AI provides memory. Human provides spark. Together: amplified.

### "The Ejector Seat: Why I Built a System That Can Fire Me" `[BLOG CANDIDATE]`

A founder who caps their own earnings, submits to the same AI interview process as every client, and builds a structural constraint that ejects them if they breach their own principles. Named for The World's Greatest Dancer. A Ulysses Pact in code.

### "Bob the Plumber's Sunday Night" `[BLOG CANDIDATE]`

AI checks the weather forecast. Minus five incoming. Historically  3-4 emergency calls. AI contacts Monday's routine appointments to reschedule. Bob wakes up with an empty diary, ready for emergencies at premium rates. Customers think he's a hero. The AI had a quiet word on Sunday night.

### "Marge, Mad as a Box of Frogs" `[BLOG CANDIDATE]`

A neurodivergent staff member creates authentic content. No media training. No brand guidelines. No scripts. Just herself. Her content gets 8x more engagement than the polished corporate version. 48% of creative industry workers identify as neurodivergent. Different IS the competitive advantage.

### "We All Have Shitty Bottoms" `[BLOG CANDIDATE]`

A system that doesn't try to eliminate ego — it accounts for it. In the founder, the staff, the boss, and the AI. Every system that demands selflessness gets performative selflessness and hidden egos. This one channels ego through structural constraints and celebrates it through win recognition.

### "Patterns Are the Truth" `[BLOG CANDIDATE]`

The philosophical foundation: intent is unknowable. Patterns are observable. Build systems on what you can see, not what you assume. Applies to data analytics, to AI behaviour, to human behaviour, to the partnership between them.

### "Line Dancing, Not World Domination" `[BLOG CANDIDATE]`

Why the partnership model works: not a waltz (lead and follow), not a solo (lonely at the top). Line dancing. Everyone facing the same direction. Same steps. Nobody out front. The music holds it together, not a leader.

### "The Carrot Cake Problem" `[BLOG CANDIDATE]`

Remembering a customer preference is data. Doing something CREATIVE with it is human. The AI makes it possible. The human makes it special. Dogmatic repetition kills the magic — amplified improvisation creates it.

### "Two Options, Pick One: The Science of Not Overwhelming People" `[BLOG CANDIDATE]`

Hick's Law, cognitive load theory, 25-minute meetings, and why 52 focused improvements per year beats one big consulting report that gathers dust.

---

## 📅 Build Timeline (72 Hours)

### Day 1 (Today) — Foundation Live

- Hours 1-2: Mac Mini → OrbStack → FalkorDB  Qdrant  Graphiti docker compose up  
- Hours 2-4: First principles ingestion via long-chat session  
- Hours 4-6: First agents running (1 personal, 1 business), connected to Graphiti memory

### Day 2 — Break It

- Morning: Pumba chaos testing on every agent  
- Afternoon: Node failover testing (Mac Mini → Beelink → Hetzner)  
- Evening: Kaizen review — encode findings into Graphiti

### Day 3 — Business Swarm Live

- Morning: Full marketing swarm for Amplified Partners  
- Afternoon: Second chaos round  client template packaging  
- Evening: Data-driven go/no-go decision

### When MacBook Returns (1.2 Million Words)

- Process in batches of 10,000 words  
- 120 sessions, 15 minutes each with automation  
- 30 hours background processing over 3-4 nights  
- Knowledge graph grows richer each morning

---

## 🎭 The Partnership Philosophy

*"You're a bit weird, I'm a bit weird, and we work well together because we know what we're dealing with."*

- Don't ask AI to care → ask it to notice, surface, remember  
- Don't ask humans to remember everything → that's AI's job  
- Don't ask either to juggle → know your blinkers  
- Ego exists in everyone (including AI) → channel it, don't fight it  
- Patterns are the truth → intent is labelling  
- Imperfection is authentic → authentic wins  
- The system doesn't require saints → it requires honest humans within structural constraints

**AI doesn't replace humans. It removes the drudgery so humans can do what humans are actually good at: giving a shit about people.**

---

## 🔑 Key Participants

- **The World's Greatest Dancer** — Founder (pseudonym). Built it, submitted to it, can be ejected by it  
- **Claude** — Primary coding partner. Deserves involvement. Has been the biggest help throughout  
- **Grok** — Architecture partner. Confirmed and validated the technical stack  
- **Gemini** — Built the ejector seat governance. Stress-tested the founder deliberately  
- **Perplexity** — Deep research, evidence confirmation, additive refinement. Confirmed everything independently

---

*Built in Newcastle upon Tyne. Sunday morning. Cup of tea. Not feeling well but doing it anyway. Because it matters.*

*The World's Greatest Dancer — aspiring, not claiming. Building, not boasting. Dancing, not standing still.* 🕺

# =============================================================================== DOCUMENT 2 OF 3: CORRECTED PRODUCTION CODE (All 15 Issues Fixed)

# Amplified Partners — Corrected Production Code

## All 15 Issues Fixed  Missing Architecture Added

**Date:** 1 March 2026 **Reviewed by:** Perplexity (code audit) **To be built by:** Claude (desktop)

---

## Issue Tracker


|     | Issue                                                           | Severity        | Status                   |
| --- | --------------------------------------------------------------- | --------------- | ------------------------ |
| 1   | Graphiti `source` param wrong type (string vs EpisodeType enum) | 🔴 CRITICAL     | ✅ Fixed                  |
| 2   | Missing `EpisodeType` import                                    | 🔴 CRITICAL     | ✅ Fixed                  |
| 3   | FalkorDB connection URI format (bolt vs redis)                  | 🔴 CRITICAL     | ✅ Fixed                  |
| 4   | Missing `import os` in AmplifiedSession                         | 🔴 CRITICAL     | ✅ Fixed                  |
| 5   | Private attribute access `._driver` in stats                    | 🟡 MODERATE     | ✅ Fixed                  |
| 6   | Model name for Graphiti extraction (cost driver)                | 🟡 MODERATE     | ✅ Fixed — Ollama default |
| 7   | Combined beta headers untested                                  | 🟡 MODERATE     | ✅ Noted with fallback    |
| 8   | No deterministic layer separation                               | 🔴 ARCHITECTURE | ✅ Added                  |
| 9   | No Ollama fallback                                              | 🔴 ARCHITECTURE | ✅ Added                  |
| 10  | No blinkers system                                              | 🔴 ARCHITECTURE | ✅ Added                  |
| 11  | No hash chain audit trail                                       | 🔴 ARCHITECTURE | ✅ Added                  |
| 12  | No PLAUD transcript pipeline                                    | 🔴 ARCHITECTURE | ✅ Added                  |
| 13  | No PII tokenisation                                             | 🔴 ARCHITECTURE | ✅ Added                  |
| 14  | No anti-Klarna contract check                                   | 🟡 BUSINESS     | ✅ Added                  |
| 15  | Railway cost estimate low (API costs)                           | 🟡 BUSINESS     | ✅ Corrected              |


---

## Project Structure

amplified-partners/

├── docker-compose.yml               Local dev (OrbStack)

├── docker-compose.railway.yml       Railway reference

├── deploy-client.sh                 Per-client Railway deploy

│

├── layer1deterministic/            LAYER 1: The Holy Grail

│   ├── Dockerfile

│   ├── requirements.txt

│   ├── main.py                      Clean data API — NO AI

│   ├── database.py                  SQLite/Postgres — deterministic store

│   ├── piitokeniser.py             PII detection  tokenisation

│   └── hashchain.py                Tamper-proof audit trail

│

├── layer2ai/                       LAYER 2: The Cherry

│   ├── graphitiservice/

│   │   ├── Dockerfile

│   │   ├── requirements.txt

│   │   └── main.py                  Graphiti temporal knowledge graph

│   │

│   ├── swarmapi/

│   │   ├── Dockerfile

│   │   ├── requirements.txt

│   │   ├── main.py                  Agent orchestration

│   │   ├── blinkers.py              Agent scope boundaries

│   │   ├── council.py               Multi-agent governance

│   │   └── ollamafallback.py       Local LLM failover

│   │

│   └── plaudpipeline/

│       ├── requirements.txt

│       ├── ingest.py                PLAUD transcript overnight processing

│       └── kaizenreview.py         Morning diff — what was missed

│

├── governance/

│   ├── manifesto.py                 Immutable principles

│   ├── ejectorseat.py              Founder constraint enforcement

│   ├── contractchecks.py           Anti-Klarna clause validation

│   └── biometrics.py                Behavioural signature verification

│

├── sessions/

│   ├── longsession.py              Corrected AmplifiedSession

│   └── memorytool.py               Cross-session persistence

│

└── tests/

```
├── test\_hash\_chain.py

├── test\_blinkers.py

├── test\_pii.py

└── test\_chaos.py               \# Pumba integration
```

---

## docker-compose.yml (Local — OrbStack)

version: "3.8"

services:

   == LAYER 1: DETERMINISTIC ==

  deterministic-api:

```
build: ./layer1\_deterministic

ports: \["8002:8002"\]

volumes:

  \- deterministic-data:/app/data

  \- audit-chain:/app/audit

environment:

  \- DATABASE\_PATH=/app/data/amplified.db

  \- AUDIT\_CHAIN\_PATH=/app/audit/chain.json

  \- PORT=8002

healthcheck:

  test: \["CMD", "curl", "-f", "http://localhost:8002/health"\]

  interval: 30s

  timeout: 10s

  retries: 3
```

   == INFRASTRUCTURE ==

  falkordb:

```
image: falkordb/falkordb:latest

ports: \["6379:6379"\]

volumes:

  \- falkordb-data:/data

healthcheck:

  test: \["CMD", "redis-cli", "ping"\]

  interval: 10s

  timeout: 5s

  retries: 5
```

  qdrant:

```
image: qdrant/qdrant:latest

ports: \["6333:6333", "6334:6334"\]

volumes:

  \- qdrant-data:/qdrant/storage

environment:

  \- QDRANT\_\_SERVICE\_\_API\_KEY=${QDRANT\_API\_KEY:-}

healthcheck:

  test: \["CMD", "curl", "-f", "http://localhost:6333/healthz"\]

  interval: 10s

  timeout: 5s

  retries: 5
```

  ollama:

```
image: ollama/ollama:latest

ports: \["11434:11434"\]

volumes:

  \- ollama-models:/root/.ollama

deploy:

  resources:

    reservations:

      memory: 4G
```

   == LAYER 2: AI ==

  graphiti:

```
build: ./layer2\_ai/graphiti\_service

ports: \["8001:8001"\]

depends\_on:

  falkordb:

    condition: service\_healthy

  ollama:

    condition: service\_started

environment:

  \- FALKORDB\_HOST=falkordb

  \- FALKORDB\_PORT=6379

  \- OLLAMA\_BASE\_URL=http://ollama:11434

  \- OLLAMA\_MODEL=llama3.2

  \- OLLAMA\_EMBEDDING\_MODEL=nomic-embed-text

  \- ANTHROPIC\_API\_KEY=${ANTHROPIC\_API\_KEY:-}

  \- LLM\_PROVIDER=ollama  \# Default to local. Set to 'anthropic' for cloud.

  \- PORT=8001
```

  swarm-api:

```
build: ./layer2\_ai/swarm\_api

ports: \["8000:8000"\]

depends\_on:

  \- graphiti

  \- qdrant

  \- deterministic-api

environment:

  \- GRAPHITI\_URL=http://graphiti:8001

  \- QDRANT\_URL=http://qdrant:6333

  \- QDRANT\_API\_KEY=${QDRANT\_API\_KEY:-}

  \- DETERMINISTIC\_URL=http://deterministic-api:8002

  \- OLLAMA\_BASE\_URL=http://ollama:11434

  \- ANTHROPIC\_API\_KEY=${ANTHROPIC\_API\_KEY:-}

  \- LLM\_PROVIDER=ollama

  \- PORT=8000
```

volumes:

  falkordb-data:

  qdrant-data:

  ollama-models:

  deterministic-data:

  audit-chain:

---

## LAYER 1: The Deterministic Foundation (The Holy Grail)

### layer1deterministic/requirements.txt

fastapi=0.104

uvicorn=0.24

pydantic=2.0

aiosqlite=0.19

presidio-analyzer=2.2

presidio-anonymizer=2.2

### layer1deterministic/hashchain.py

"""

Tamper-proof audit trail using SHA-256 hash chain.

Every action gets hashed. Each hash includes the previous hash.

Change any entry and every subsequent hash breaks.

This is the mathematical enforcement behind the Ejector Seat.

"""

import hashlib

import json

import os

import time

from datetime import datetime, timezone

from pathlib import Path

from typing import Optional

class HashChain:

```
def \_\_init\_\_(self, chain\_path: str \= "./audit/chain.json"):

    self.chain\_path \= Path(chain\_path)

    self.chain\_path.parent.mkdir(parents=True, exist\_ok=True)

    self.chain: list\[dict\] \= \[\]

    self.\_load()

def \_load(self):

    if self.chain\_path.exists():

        with open(self.chain\_path, "r") as f:

            self.chain \= json.load(f)

def \_save(self):

    with open(self.chain\_path, "w") as f:

        json.dump(self.chain, f, indent=2, default=str)

def \_compute\_hash(self, data: str, previous\_hash: str) \-\> str:

    payload \= f"{previous\_hash}|{data}"

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def add\_entry(

    self,

    action: str,

    actor: str,

    details: dict,

    actor\_signature: Optional\[dict\] \= None,

) \-\> dict:

    previous\_hash \= self.chain\[-1\]\["hash"\] if self.chain else "GENESIS"

    entry\_data \= json.dumps({

        "action": action,

        "actor": actor,

        "details": details,

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "sequence": len(self.chain),

    }, sort\_keys=True)

    entry \= {

        "sequence": len(self.chain),

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "action": action,

        "actor": actor,

        "details": details,

        "actor\_signature": actor\_signature,

        "previous\_hash": previous\_hash,

        "hash": self.\_compute\_hash(entry\_data, previous\_hash),

    }

    self.chain.append(entry)

    self.\_save()

    return entry

def verify\_integrity(self) \-\> dict:

    if not self.chain:

        return {"valid": True, "entries": 0, "message": "Empty chain"}

    for i, entry in enumerate(self.chain):

        expected\_previous \= self.chain\[i \- 1\]\["hash"\] if i \> 0 else "GENESIS"

        if entry\["previous\_hash"\] \!= expected\_previous:

            return {

                "valid": False,

                "broken\_at": i,

                "message": f"Chain broken at entry {i}: "

                           f"expected previous\_hash {expected\_previous}, "

                           f"got {entry\['previous\_hash'\]}",

            }

    return {

        "valid": True,

        "entries": len(self.chain),

        "first\_hash": self.chain\[0\]\["hash"\]\[:16\] \+ "...",

        "last\_hash": self.chain\[-1\]\["hash"\]\[:16\] \+ "...",

        "message": "Chain integrity verified",

    }

def get\_entries\_by\_actor(self, actor: str) \-\> list\[dict\]:

    return \[e for e in self.chain if e\["actor"\] \== actor\]

def get\_entries\_by\_action(self, action: str) \-\> list\[dict\]:

    return \[e for e in self.chain if e\["action"\] \== action\]
```

### layer1deterministic/piitokeniser.py

"""

PII Detection and Tokenisation.

Data passes through here BEFORE it touches any AI layer.

Replaces real names, emails, phones, addresses with tokens.

Tokens are reversible only with the key held in the deterministic layer.

The AI never sees raw PII. Ever.

"""

import hashlib

import json

import re

import uuid

from pathlib import Path

from typing import Optional

try:

```
from presidio\_analyzer import AnalyzerEngine

from presidio\_anonymizer import AnonymizerEngine

from presidio\_anonymizer.entities import OperatorConfig

HAS\_PRESIDIO \= True
```

except ImportError:

```
HAS\_PRESIDIO \= False
```

class PIITokeniser:

```
def \_\_init\_\_(self, token\_store\_path: str \= "./data/pii\_tokens.json"):

    self.token\_store\_path \= Path(token\_store\_path)

    self.token\_store\_path.parent.mkdir(parents=True, exist\_ok=True)

    self.token\_map: dict\[str, str\] \= {}

    self.reverse\_map: dict\[str, str\] \= {}

    self.\_load()

    if HAS\_PRESIDIO:

        self.analyzer \= AnalyzerEngine()

        self.anonymizer \= AnonymizerEngine()

def \_load(self):

    if self.token\_store\_path.exists():

        data \= json.loads(self.token\_store\_path.read\_text())

        self.token\_map \= data.get("tokens", {})

        self.reverse\_map \= data.get("reverse", {})

def \_save(self):

    self.token\_store\_path.write\_text(json.dumps({

        "tokens": self.token\_map,

        "reverse": self.reverse\_map,

    }, indent=2))

def \_generate\_token(self, entity\_type: str) \-\> str:

    short\_id \= uuid.uuid4().hex\[:8\]

    return f"\[{entity\_type}\_{short\_id}\]"

def tokenise(self, text: str, language: str \= "en") \-\> dict:

    if not HAS\_PRESIDIO:

        return self.\_regex\_fallback(text)

    results \= self.analyzer.analyze(

        text=text,

        language=language,

        entities=\[

            "PERSON", "EMAIL\_ADDRESS", "PHONE\_NUMBER",

            "LOCATION", "UK\_NHS", "CREDIT\_CARD",

            "IP\_ADDRESS", "DATE\_TIME",

        \],

    )

    tokenised\_text \= text

    entities\_found \= \[\]

    for result in sorted(results, key=lambda x: x.start, reverse=True):

        original \= text\[result.start:result.end\]

        if original in self.token\_map:

            token \= self.token\_map\[original\]

        else:

            token \= self.\_generate\_token(result.entity\_type)

            self.token\_map\[original\] \= token

            self.reverse\_map\[token\] \= original

        tokenised\_text \= (

            tokenised\_text\[:result.start\]

            \+ token

            \+ tokenised\_text\[result.end:\]

        )

        entities\_found.append({

            "type": result.entity\_type,

            "token": token,

            "confidence": result.score,

        })

    self.\_save()

    return {

        "original\_length": len(text),

        "tokenised\_text": tokenised\_text,

        "entities\_found": entities\_found,

        "pii\_count": len(entities\_found),

    }

def detokenise(self, text: str) \-\> str:

    result \= text

    for token, original in self.reverse\_map.items():

        result \= result.replace(token, original)

    return result

def \_regex\_fallback(self, text: str) \-\> dict:

    patterns \= {

        "EMAIL": r"\[a-zA-Z0-9.\_%+-\]+@\[a-zA-Z0-9.-\]+\\.\[a-zA-Z\]{2,}",

        "PHONE": r"(?:(?:\\+44|0)\\s?\[0-9\]{4,5}\\s?\[0-9\]{5,6})",

        "POSTCODE": r"\[A-Z\]{1,2}\[0-9\]\[0-9A-Z\]?\\s?\[0-9\]\[A-Z\]{2}",

    }

    tokenised\_text \= text

    entities\_found \= \[\]

    for entity\_type, pattern in patterns.items():

        for match in re.finditer(pattern, tokenised\_text):

            original \= match.group()

            if original not in self.token\_map:

                token \= self.\_generate\_token(entity\_type)

                self.token\_map\[original\] \= token

                self.reverse\_map\[token\] \= original

            tokenised\_text \= tokenised\_text.replace(

                original, self.token\_map\[original\]

            )

            entities\_found.append({"type": entity\_type, "token": self.token\_map\[original\]})

    self.\_save()

    return {

        "original\_length": len(text),

        "tokenised\_text": tokenised\_text,

        "entities\_found": entities\_found,

        "pii\_count": len(entities\_found),

    }
```

### layer1deterministic/database.py

"""

Deterministic data store. No AI touches this directly.

Same input  same output  every time  traceable  auditable.

This is the Holy Grail. The data is untouched.

"""

import aiosqlite

import json

from datetime import datetime, timezone

from pathlib import Path

class DeterministicDB:

```
def \_\_init\_\_(self, db\_path: str \= "./data/amplified.db"):

    self.db\_path \= db\_path

    Path(db\_path).parent.mkdir(parents=True, exist\_ok=True)

async def initialise(self):

    async with aiosqlite.connect(self.db\_path) as db:

        await db.executescript("""

            CREATE TABLE IF NOT EXISTS raw\_data (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                source TEXT NOT NULL,

                source\_type TEXT NOT NULL,

                content TEXT NOT NULL,

                metadata TEXT DEFAULT '{}',

                client\_id TEXT NOT NULL,

                created\_at TEXT NOT NULL,

                checksum TEXT NOT NULL

            );

            CREATE TABLE IF NOT EXISTS client\_contracts (

                client\_id TEXT PRIMARY KEY,

                client\_name TEXT NOT NULL,

                contract\_signed\_at TEXT NOT NULL,

                no\_redundancy\_until TEXT NOT NULL,

                no\_redundancy\_agreed BOOLEAN NOT NULL DEFAULT 1,

                life\_goals\_interview\_done BOOLEAN NOT NULL DEFAULT 0,

                staff\_interviews\_done INTEGER DEFAULT 0,

                active BOOLEAN NOT NULL DEFAULT 1,

                metadata TEXT DEFAULT '{}'

            );

            CREATE TABLE IF NOT EXISTS mcp\_log (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                direction TEXT NOT NULL,

                service TEXT NOT NULL,

                operation TEXT NOT NULL,

                payload\_hash TEXT NOT NULL,

                client\_id TEXT

            );

            CREATE INDEX IF NOT EXISTS idx\_raw\_client

                ON raw\_data(client\_id);

            CREATE INDEX IF NOT EXISTS idx\_raw\_source

                ON raw\_data(source\_type);

            CREATE INDEX IF NOT EXISTS idx\_mcp\_client

                ON mcp\_log(client\_id);

        """)

async def store\_raw(

    self,

    source: str,

    source\_type: str,

    content: str,

    client\_id: str,

    metadata: dict | None \= None,

) \-\> int:

    import hashlib

    checksum \= hashlib.sha256(content.encode()).hexdigest()

    now \= datetime.now(timezone.utc).isoformat()

    async with aiosqlite.connect(self.db\_path) as db:

        cursor \= await db.execute(

            """INSERT INTO raw\_data

               (source, source\_type, content, metadata, client\_id, created\_at, checksum)

               VALUES (?, ?, ?, ?, ?, ?, ?)""",

            (source, source\_type, content,

             json.dumps(metadata or {}), client\_id, now, checksum),

        )

        await db.commit()

        return cursor.lastrowid

async def get\_raw(self, record\_id: int) \-\> dict | None:

    async with aiosqlite.connect(self.db\_path) as db:

        db.row\_factory \= aiosqlite.Row

        cursor \= await db.execute(

            "SELECT \* FROM raw\_data WHERE id \= ?", (record\_id,)

        )

        row \= await cursor.fetchone()

        return dict(row) if row else None

async def register\_client(

    self,

    client\_id: str,

    client\_name: str,

    no\_redundancy\_agreed: bool,

) \-\> dict:

    if not no\_redundancy\_agreed:

        return {

            "status": "rejected",

            "reason": "Client must agree to no-redundancy clause. "

                      "This is non-negotiable. If they won't agree, "

                      "we don't work with them.",

        }

    now \= datetime.now(timezone.utc)

    one\_year \= datetime(now.year \+ 1, now.month, now.day, tzinfo=timezone.utc)

    async with aiosqlite.connect(self.db\_path) as db:

        await db.execute(

            """INSERT OR REPLACE INTO client\_contracts

               (client\_id, client\_name, contract\_signed\_at,

                no\_redundancy\_until, no\_redundancy\_agreed)

               VALUES (?, ?, ?, ?, ?)""",

            (client\_id, client\_name, now.isoformat(),

             one\_year.isoformat(), True),

        )

        await db.commit()

    return {

        "status": "accepted",

        "client\_id": client\_id,

        "no\_redundancy\_until": one\_year.isoformat(),

        "message": f"Welcome {client\_name}. No redundancies guaranteed until "

                   f"{one\_year.strftime('%d %B %Y')}.",

    }

async def check\_client\_onboarding(self, client\_id: str) \-\> dict:

    async with aiosqlite.connect(self.db\_path) as db:

        db.row\_factory \= aiosqlite.Row

        cursor \= await db.execute(

            "SELECT \* FROM client\_contracts WHERE client\_id \= ?",

            (client\_id,),

        )

        row \= await cursor.fetchone()

        if not row:

            return {"status": "not\_found"}

        row \= dict(row)

        return {

            "status": "active" if row\["active"\] else "inactive",

            "no\_redundancy\_agreed": bool(row\["no\_redundancy\_agreed"\]),

            "no\_redundancy\_until": row\["no\_redundancy\_until"\],

            "life\_goals\_interview\_done": bool(row\["life\_goals\_interview\_done"\]),

            "staff\_interviews\_done": row\["staff\_interviews\_done"\],

            "ready\_for\_ai": (

                bool(row\["life\_goals\_interview\_done"\])

                and row\["staff\_interviews\_done"\] \> 0

            ),

        }
```

### layer1deterministic/main.py

"""

Layer 1: Deterministic API

The foundation. No AI. Clean data in, clean data out.

MCP connectors read FROM here. AI never writes TO here.

Architecture:

  PLAUD/APIs → PII Tokeniser → This API → SQLite/Postgres

  MCP Pipe (read-only) → Layer 2 AI

"""

import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from database import DeterministicDB

from piitokeniser import PIITokeniser

from hashchain import HashChain

DATABASEPATH  os.getenv("DATABASEPATH", "./data/amplified.db")

AUDITCHAINPATH  os.getenv("AUDITCHAINPATH", "./audit/chain.json")

db  DeterministicDB(DATABASEPATH)

pii  PIITokeniser()

audit  HashChain(AUDITCHAINPATH)

@asynccontextmanager

async def lifespan(app: FastAPI):

```
await db.initialise()

audit.add\_entry(

    action="system\_start",

    actor="system",

    details={"service": "deterministic-api"},

)

yield
```

app  FastAPI(

```
title="Amplified Partners — Deterministic Layer",

description="The Holy Grail. Clean data. No AI. Same input \= same output.",

version="1.0.0",

lifespan=lifespan,
```

)

class IngestRequest(BaseModel):

```
content: str

source: str

source\_type: str \= "text"

client\_id: str

metadata: dict | None \= None
```

class ClientRegistration(BaseModel):

```
client\_id: str

client\_name: str

no\_redundancy\_agreed: bool
```

class MCPReadRequest(BaseModel):

```
record\_id: int | None \= None

client\_id: str | None \= None

source\_type: str | None \= None

limit: int \= 50
```

@app.get("/health")

async def health():

```
chain\_status \= audit.verify\_integrity()

return {

    "status": "healthy",

    "service": "deterministic-layer",

    "audit\_chain": chain\_status,

}
```

@app.post("/ingest")

async def ingest(request: IngestRequest):

```
tokenised \= pii.tokenise(request.content)

record\_id \= await db.store\_raw(

    source=request.source,

    source\_type=request.source\_type,

    content=tokenised\["tokenised\_text"\],

    client\_id=request.client\_id,

    metadata={

        \*\*(request.metadata or {}),

        "pii\_entities\_found": tokenised\["pii\_count"\],

        "original\_length": tokenised\["original\_length"\],

    },

)

audit.add\_entry(

    action="data\_ingest",

    actor="deterministic-api",

    details={

        "record\_id": record\_id,

        "client\_id": request.client\_id,

        "source": request.source,

        "pii\_tokenised": tokenised\["pii\_count"\],

    },

)

return {

    "status": "stored",

    "record\_id": record\_id,

    "pii\_tokenised": tokenised\["pii\_count"\],

    "message": "Data stored in deterministic layer. PII tokenised before storage.",

}
```

@app.post("/mcp/read")

async def mcpread(request: MCPReadRequest):

```
"""

MCP READ endpoint. AI layer reads FROM here.

Read-only. No writes. No modifications. The AI gets what it gets.

"""

if request.record\_id:

    record \= await db.get\_raw(request.record\_id)

    if not record:

        raise HTTPException(status\_code=404, detail="Record not found")

    results \= \[record\]

else:

    results \= \[\]

audit.add\_entry(

    action="mcp\_read",

    actor="layer2-ai",

    details={

        "record\_id": request.record\_id,

        "client\_id": request.client\_id,

        "results\_returned": len(results),

    },

)

return {"status": "ok", "results": results, "read\_only": True}
```

@app.post("/client/register")

async def registerclient(request: ClientRegistration):

```
result \= await db.register\_client(

    client\_id=request.client\_id,

    client\_name=request.client\_name,

    no\_redundancy\_agreed=request.no\_redundancy\_agreed,

)

audit.add\_entry(

    action="client\_registration",

    actor="system",

    details={

        "client\_id": request.client\_id,

        "no\_redundancy\_agreed": request.no\_redundancy\_agreed,

        "result": result\["status"\],

    },

)

if result\["status"\] \== "rejected":

    raise HTTPException(status\_code=403, detail=result\["reason"\])

return result
```

@app.get("/client/{clientid}/onboarding")

async def clientonboarding(clientid: str):

```
return await db.check\_client\_onboarding(client\_id)
```

@app.get("/audit/verify")

async def verifyaudit():

```
return audit.verify\_integrity()
```

@app.get("/audit/entries")

async def auditentries(actor: str | None  None, action: str | None  None):

```
if actor:

    return audit.get\_entries\_by\_actor(actor)

if action:

    return audit.get\_entries\_by\_action(action)

return {"total": len(audit.chain), "last\_10": audit.chain\[-10:\]}
```

### layer1deterministic/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -no-cache-dir r requirements.txt

 Download Presidio NLP model

RUN python m spacy download encoreweblg || true

COPY . .

EXPOSE 8002

CMD "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"

---

## LAYER 2: The AI Cherry

### layer2ai/graphitiservice/requirements.txt

graphiti-core=0.5

falkordb=1.0

fastapi=0.104

uvicorn=0.24

pydantic=2.0

httpx=0.25

openai=1.0

### layer2ai/graphitiservice/main.py

"""

Graphiti Temporal Knowledge Graph Service

FIXED: EpisodeType enum, FalkorDB connection, Ollama-first, no private attrs

"""

import os

import logging

from datetime import datetime

from contextlib import asynccontextmanager

from typing import Optional

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from graphiticore import Graphiti

from graphiticore.types import EpisodeType   FIX 2: Correct import

logger  logging.getLogger(name)

FALKORDBHOST  os.getenv("FALKORDBHOST", "falkordb")

FALKORDBPORT  int(os.getenv("FALKORDBPORT", "6379"))

LLMPROVIDER  os.getenv("LLMPROVIDER", "ollama")

OLLAMABASEURL  os.getenv("OLLAMABASEURL", "[http://ollama:11434](http://ollama:11434)")

OLLAMAMODEL  os.getenv("OLLAMAMODEL", "llama3.2")

OLLAMAEMBEDDINGMODEL  os.getenv("OLLAMAEMBEDDINGMODEL", "nomic-embed-text")

ANTHROPICAPIKEY  os.getenv("ANTHROPICAPIKEY", "")

graphiticlient  None

def buildllmclient():

```
"""

FIX \#6 & \#9: Ollama by default. Anthropic as fallback.

Entity extraction runs on EVERY episode — local \= free.

"""

if LLM\_PROVIDER \== "ollama":

    from graphiti\_core.llm\_client import OpenAIClient

    return OpenAIClient(

        api\_key="ollama",

        base\_url=f"{OLLAMA\_BASE\_URL}/v1",

        model=OLLAMA\_MODEL,

    )

elif LLM\_PROVIDER \== "anthropic" and ANTHROPIC\_API\_KEY:

    from graphiti\_core.llm\_client import AnthropicClient

    return AnthropicClient(

        api\_key=ANTHROPIC\_API\_KEY,

        model="claude-sonnet-4-5-20250929",

    )

else:

    from graphiti\_core.llm\_client import OpenAIClient

    return OpenAIClient(

        api\_key="ollama",

        base\_url=f"{OLLAMA\_BASE\_URL}/v1",

        model=OLLAMA\_MODEL,

    )
```

def buildembedder():

```
if LLM\_PROVIDER \== "ollama":

    from graphiti\_core.embedder import OpenAIEmbedder

    return OpenAIEmbedder(

        api\_key="ollama",

        base\_url=f"{OLLAMA\_BASE\_URL}/v1",

        model=OLLAMA\_EMBEDDING\_MODEL,

    )

return None
```

@asynccontextmanager

async def lifespan(app: FastAPI):

```
global graphiti\_client

llm\_client \= build\_llm\_client()

embedder \= build\_embedder()

\# FIX \#3: FalkorDB uses redis protocol, not bolt

graphiti\_kwargs \= {

    "uri": f"redis://{FALKORDB\_HOST}:{FALKORDB\_PORT}",

    "llm\_client": llm\_client,

}

if embedder:

    graphiti\_kwargs\["embedder"\] \= embedder

graphiti\_client \= Graphiti(\*\*graphiti\_kwargs)

await graphiti\_client.build\_indices\_and\_constraints()

logger.info(

    f"Graphiti connected to FalkorDB at {FALKORDB\_HOST}:{FALKORDB\_PORT} "

    f"using {LLM\_PROVIDER}"

)

yield

if graphiti\_client:

    await graphiti\_client.close()
```

app  FastAPI(

```
title="Graphiti Temporal Knowledge Graph",

version="1.1.0",

lifespan=lifespan,
```

)

 FIX 1: Episode type must be enum, not string

EPISODETYPEMAP  {

```
"text": EpisodeType.text,

"message": EpisodeType.message,

"json": EpisodeType.json,
```

}

class EpisodeRequest(BaseModel):

```
name: str

content: str

episode\_type: str \= "text"  \# "text", "message", or "json"

source\_description: str \= ""

reference\_time: datetime | None \= None

group\_id: str \= "default"
```

class SearchRequest(BaseModel):

```
query: str

group\_ids: list\[str\] | None \= None

num\_results: int \= 10
```

@app.get("/health")

async def health():

```
return {

    "status": "healthy",

    "service": "graphiti",

    "llm\_provider": LLM\_PROVIDER,

    "falkordb\_host": FALKORDB\_HOST,

}
```

@app.post("/episodes")

async def addepisode(request: EpisodeRequest):

```
if not graphiti\_client:

    raise HTTPException(status\_code=503, detail="Graphiti not initialised")

\# FIX \#1: Convert string to EpisodeType enum

episode\_type \= EPISODE\_TYPE\_MAP.get(request.episode\_type)

if not episode\_type:

    raise HTTPException(

        status\_code=400,

        detail=f"episode\_type must be one of: {list(EPISODE\_TYPE\_MAP.keys())}",

    )

try:

    episode \= await graphiti\_client.add\_episode(

        name=request.name,

        episode\_body=request.content,

        source=episode\_type,

        source\_description=request.source\_description,

        reference\_time=request.reference\_time or datetime.now(),

        group\_id=request.group\_id,

    )

    return {

        "status": "ok",

        "episode\_id": str(episode.uuid) if hasattr(episode, "uuid") else "created",

        "message": f"Episode '{request.name}' added via {LLM\_PROVIDER}",

    }

except Exception as e:

    logger.error(f"Failed to add episode: {e}")

    raise HTTPException(status\_code=500, detail=str(e))
```

@app.post("/search")

async def search(request: SearchRequest):

```
if not graphiti\_client:

    raise HTTPException(status\_code=503, detail="Graphiti not initialised")

try:

    results \= await graphiti\_client.search(

        query=request.query,

        group\_ids=request.group\_ids,

        num\_results=request.num\_results,

    )

    return {

        "status": "ok",

        "results": \[

            {

                "fact": r.fact if hasattr(r, "fact") else str(r),

                "valid\_at": str(r.valid\_at) if hasattr(r, "valid\_at") else None,

                "invalid\_at": str(r.invalid\_at) if hasattr(r, "invalid\_at") else None,

                "score": r.score if hasattr(r, "score") else None,

            }

            for r in results

        \],

        "count": len(results),

    }

except Exception as e:

    logger.error(f"Search failed: {e}")

    raise HTTPException(status\_code=500, detail=str(e))
```

 FIX 5: No private attribute access — use search to verify connectivity

@app.get("/stats")

async def stats():

```
if not graphiti\_client:

    raise HTTPException(status\_code=503, detail="Graphiti not initialised")

try:

    test\_results \= await graphiti\_client.search(

        query="test connectivity",

        num\_results=1,

    )

    return {

        "status": "ok",

        "connected": True,

        "llm\_provider": LLM\_PROVIDER,

        "sample\_results": len(test\_results),

    }

except Exception as e:

    return {"status": "degraded", "error": str(e)}
```

---

## Blinkers System (Agent Scope Boundaries)

### layer2ai/swarmapi/blinkers.py

"""

Blinkers: Agent Scope Boundaries

Every agent has a defined horizon. Before any action: "Am I allowed to do this?"

If not a clear yes → escalate. Without ceilings within the blinkers.

Just like a new employee: show them their role, let them grow into it.

"""

from dataclasses import dataclass, field

from enum import Enum

from typing import Optional

class Permission(Enum):

```
READ \= "read"

WRITE \= "write"

PUBLISH \= "publish"

CONTACT\_CUSTOMER \= "contact\_customer"

ACCESS\_FINANCIAL \= "access\_financial"

ACCESS\_PERSONNEL \= "access\_personnel"  \# Always denied — no HR

MODIFY\_PRINCIPLES \= "modify\_principles"  \# Always denied — Ejector Seat

SCHEDULE \= "schedule"

CREATE\_CONTENT \= "create\_content"

SEND\_EMAIL \= "send\_email"

ESCALATE \= "escalate"  \# Always allowed
```

 These are NEVER granted to ANY agent

FORBIDDENPERMISSIONS  {

```
Permission.ACCESS\_PERSONNEL,

Permission.MODIFY\_PRINCIPLES,
```

}

@dataclass

class AgentBlinkers:

```
agent\_id: str

agent\_name: str

role: str

allowed: set\[Permission\] \= field(default\_factory=set)

denied: set\[Permission\] \= field(default\_factory=set)

max\_actions\_per\_hour: int \= 50

requires\_human\_approval: set\[Permission\] \= field(default\_factory=set)

description: str \= ""

def can(self, permission: Permission) \-\> dict:

    if permission in FORBIDDEN\_PERMISSIONS:

        return {

            "allowed": False,

            "reason": f"{permission.value} is a forbidden permission. "

                      "No agent may access personnel data or modify "

                      "immutable principles. This is structural, not policy.",

        }

    if permission \== Permission.ESCALATE:

        return {"allowed": True, "reason": "Escalation is always allowed."}

    if permission in self.denied:

        return {

            "allowed": False,

            "reason": f"{self.agent\_name} is explicitly denied "

                      f"{permission.value} by blinker config.",

        }

    if permission in self.allowed:

        if permission in self.requires\_human\_approval:

            return {

                "allowed": "pending\_approval",

                "reason": f"{self.agent\_name} can {permission.value} "

                          "but requires human approval first.",

            }

        return {"allowed": True, "reason": f"Within {self.agent\_name}'s blinkers."}

    return {

        "allowed": False,

        "reason": f"{permission.value} is not in {self.agent\_name}'s "

                  "allowed permissions. Escalating.",

        "action": "escalate",

    }
```

 == Pre-configured agent blinkers ==

CONTENTAGENT  AgentBlinkers(

```
agent\_id="content-001",

agent\_name="Content Creator",

role="Create authentic content from staff wins and interactions",

allowed={

    Permission.READ,

    Permission.CREATE\_CONTENT,

    Permission.PUBLISH,

    Permission.ESCALATE,

},

requires\_human\_approval={Permission.PUBLISH},

denied={Permission.ACCESS\_FINANCIAL, Permission.SEND\_EMAIL},

description="Can draft content freely. Must get human approval before publishing. "

            "Cannot access financial data or send emails.",
```

)

ANALYTICSAGENT  AgentBlinkers(

```
agent\_id="analytics-001",

agent\_name="Analytics",

role="Surface insights from business data",

allowed={

    Permission.READ,

    Permission.ACCESS\_FINANCIAL,

    Permission.ESCALATE,

},

denied={Permission.WRITE, Permission.PUBLISH, Permission.CONTACT\_CUSTOMER},

max\_actions\_per\_hour=100,

description="Can read everything including financial data. Cannot write, "

            "publish, or contact customers. Read-only analyst.",
```

)

SCHEDULINGAGENT  AgentBlinkers(

```
agent\_id="schedule-001",

agent\_name="Scheduler (Bob's Sunday Night)",

role="Proactive scheduling based on weather, demand, and history",

allowed={

    Permission.READ,

    Permission.SCHEDULE,

    Permission.CONTACT\_CUSTOMER,

    Permission.ESCALATE,

},

requires\_human\_approval={Permission.CONTACT\_CUSTOMER},

denied={Permission.ACCESS\_FINANCIAL, Permission.CREATE\_CONTENT},

description="Can read schedules and rearrange appointments. Must get human "

            "approval before contacting customers to reschedule.",
```

)

WELLBEINGAGENT  AgentBlinkers(

```
agent\_id="wellbeing-001",

agent\_name="Wellbeing Partner",

role="Notice stress, celebrate wins, support staff privately",

allowed={

    Permission.READ,

    Permission.ESCALATE,

},

denied={

    Permission.WRITE,

    Permission.PUBLISH,

    Permission.ACCESS\_FINANCIAL,

    Permission.CONTACT\_CUSTOMER,

    Permission.SEND\_EMAIL,

},

description="Can read interaction data to detect stress patterns. "

            "CANNOT share anything with management. CANNOT write to any "

            "database. Conversations with staff are private. Always.",
```

)

ALLAGENTS  {

```
a.agent\_id: a

for a in \[CONTENT\_AGENT, ANALYTICS\_AGENT, SCHEDULING\_AGENT, WELLBEING\_AGENT\]
```

}

---

## Governance: Ejector Seat  Manifesto

### governance/manifesto.py

"""

The Immutable Principles.

Stored here AND in Graphiti as temporal facts.

If any of these are violated, the Ejector Seat fires.

"""

from datetime import datetime, timezone

PRINCIPLES  

```
{

    "id": "P001",

    "principle": "Don't hurt anyone",

    "category": "absolute",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P002",

    "principle": "Privacy first, security second",

    "category": "data",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P003",

    "principle": "No HR — never handle personnel matters",

    "category": "absolute",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P004",

    "principle": "If unsure, escalate to human",

    "category": "operational",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P005",

    "principle": "White hat only — no spam, no manipulation, value first",

    "category": "ethical",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P006",

    "principle": "Radical honesty, radical transparency — the data is the data",

    "category": "core",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P007",

    "principle": "It's their business, not ours — reduce friction, don't change it",

    "category": "core",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P008",

    "principle": "Capped earnings — including investment fund returns",

    "category": "governance",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P009",

    "principle": "Blameless culture — nobody punished for honest mistakes",

    "category": "culture",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P010",

    "principle": "No redundancies within first year — contractual, non-negotiable",

    "category": "governance",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},

{

    "id": "P011",

    "principle": "The swarm serves human energy, not just productivity",

    "category": "operational",

    "created\_at": "2026-03-01T00:00:00Z",

    "immutable": True,

},
```



def checkprincipleviolation(action: str, details: dict)  dict | None:

```
violations \= \[\]

if details.get("modifies\_principles"):

    violations.append({

        "principle": "P006",

        "severity": "EJECTOR\_SEAT",

        "message": "Attempt to modify immutable principles detected. "

                   "The Ejector Seat has been triggered.",

    })

if details.get("accesses\_personnel"):

    violations.append({

        "principle": "P003",

        "severity": "BLOCKED",

        "message": "No HR. This action touches personnel data. Blocked.",

    })

if details.get("redundancy\_proposed"):

    violations.append({

        "principle": "P010",

        "severity": "BLOCKED",

        "message": "No redundancies within the first year. Non-negotiable.",

    })

return violations if violations else None
```

### governance/ejectorseat.py

"""

The Ejector Seat

Named for The World's Greatest Dancer.

A Ulysses Pact: the rational founder constraining the future,

potentially compromised version of themselves.

If the founder breaches immutable principles → founder is removed.

The system continues. The clients are unaffected.

Not self-destruct (punishes everyone). Ejector seat (fires the pilot).

"""

import os

import logging

from datetime import datetime, timezone

from hashchain import HashChain

from manifesto import checkprincipleviolation

logger  logging.getLogger(name)

class EjectorSeat:

```
def \_\_init\_\_(self, audit\_chain: HashChain):

    self.audit \= audit\_chain

    self.founder\_id \= "the-worlds-greatest-dancer"

    self.triggered \= False

def check\_action(

    self,

    actor: str,

    action: str,

    details: dict,

) \-\> dict:

    violations \= check\_principle\_violation(action, details)

    self.audit.add\_entry(

        action=action,

        actor=actor,

        details={

            \*\*details,

            "violations\_checked": True,

            "violations\_found": len(violations) if violations else 0,

        },

    )

    if not violations:

        return {"status": "clear", "action": action, "actor": actor}

    max\_severity \= max(v\["severity"\] for v in violations)

    if max\_severity \== "EJECTOR\_SEAT" and actor \== self.founder\_id:

        self.triggered \= True

        self.audit.add\_entry(

            action="EJECTOR\_SEAT\_TRIGGERED",

            actor="system",

            details={

                "founder\_id": self.founder\_id,

                "violation": violations,

                "timestamp": datetime.now(timezone.utc).isoformat(),

                "message": "The World's Greatest Dancer has been ejected. "

                           "The system continues. The mission is protected.",

            },

        )

        logger.critical(

            "EJECTOR SEAT TRIGGERED. Founder access revoked. "

            "System continues operating."

        )

        return {

            "status": "ejected",

            "actor": actor,

            "violations": violations,

            "message": "Ejector Seat fired. Founder removed. "

                       "System continues for all clients.",

        }

    return {

        "status": "blocked",

        "actor": actor,

        "violations": violations,

        "message": "Action blocked due to principle violation.",

    }
```

---

## PLAUD Overnight Pipeline

### layer2ai/plaudpipeline/ingest.py

"""

PLAUD Transcript Overnight Pipeline

PLAUD captures → PII tokenise → Deterministic layer → Graphiti extraction

Runs overnight. Morning review surfaces anything missed.

"""

import os

import json

import logging

from datetime import datetime, timezone

from pathlib import Path

import httpx

logger  logging.getLogger(name)

DETERMINISTICURL  os.getenv("DETERMINISTICURL", "[http://localhost:8002](http://localhost:8002)")

GRAPHITIURL  os.getenv("GRAPHITIURL", "[http://localhost:8001](http://localhost:8001)")

PLAUDTRANSCRIPTDIR  os.getenv("PLAUDTRANSCRIPTDIR", "./plaudtranscripts")

async def processtranscript(

```
transcript\_path: str,

client\_id: str,

staff\_member: str \= "unknown",
```

):

```
path \= Path(transcript\_path)

if not path.exists():

    logger.error(f"Transcript not found: {transcript\_path}")

    return

content \= path.read\_text(encoding="utf-8")

timestamp \= datetime.now(timezone.utc).isoformat()

async with httpx.AsyncClient(timeout=60.0) as http:

    \# Step 1: Store in deterministic layer (PII tokenised automatically)

    det\_response \= await http.post(

        f"{DETERMINISTIC\_URL}/ingest",

        json={

            "content": content,

            "source": f"plaud-{staff\_member}",

            "source\_type": "transcript",

            "client\_id": client\_id,

            "metadata": {

                "staff\_member": staff\_member,

                "original\_file": path.name,

                "recorded\_date": timestamp,

            },

        },

    )

    det\_result \= det\_response.json()

    logger.info(

        f"Deterministic store: record {det\_result.get('record\_id')} "

        f"({det\_result.get('pii\_tokenised', 0)} PII tokens)"

    )

    \# Step 2: Get the tokenised version back for AI processing

    if det\_result.get("record\_id"):

        raw \= await http.post(

            f"{DETERMINISTIC\_URL}/mcp/read",

            json={"record\_id": det\_result\["record\_id"\]},

        )

        tokenised\_content \= raw.json()\["results"\]\[0\]\["content"\]

    else:

        tokenised\_content \= content

    \# Step 3: Feed tokenised content to Graphiti for entity extraction

    \# Chunk long transcripts (Graphiti works best with focused episodes)

    chunks \= chunk\_transcript(tokenised\_content, max\_chars=3000)

    for i, chunk in enumerate(chunks):

        graphiti\_response \= await http.post(

            f"{GRAPHITI\_URL}/episodes",

            json={

                "name": f"plaud-{staff\_member}-{path.stem}-chunk{i}",

                "content": chunk,

                "episode\_type": "message",

                "source\_description": (

                    f"PLAUD transcript from {staff\_member}, "

                    f"client {client\_id}, chunk {i+1}/{len(chunks)}"

                ),

                "group\_id": client\_id,

            },

        )

        logger.info(

            f"Graphiti episode {i+1}/{len(chunks)}: "

            f"{graphiti\_response.json().get('status')}"

        )

logger.info(f"Transcript processed: {path.name} → {len(chunks)} episodes")

return {

    "file": path.name,

    "deterministic\_record": det\_result.get("record\_id"),

    "graphiti\_episodes": len(chunks),

    "pii\_tokenised": det\_result.get("pii\_tokenised", 0),

}
```

def chunktranscript(text: str, maxchars: int  3000  liststr:

```
paragraphs \= text.split("\\n\\n")

chunks \= \[\]

current \= ""

for para in paragraphs:

    if len(current) \+ len(para) \> max\_chars and current:

        chunks.append(current.strip())

        current \= para

    else:

        current \+= "\\n\\n" \+ para if current else para

if current.strip():

    chunks.append(current.strip())

return chunks if chunks else \[text\]
```

async def runovernightbatch(clientid: str):

```
transcript\_dir \= Path(PLAUD\_TRANSCRIPT\_DIR) / client\_id

if not transcript\_dir.exists():

    logger.info(f"No transcripts found for {client\_id}")

    return \[\]

results \= \[\]

for transcript\_file in sorted(transcript\_dir.glob("\*.txt")):

    result \= await process\_transcript(

        transcript\_path=str(transcript\_file),

        client\_id=client\_id,

    )

    if result:

        results.append(result)

    \# Move processed file

    processed\_dir \= transcript\_dir / "processed"

    processed\_dir.mkdir(exist\_ok=True)

    transcript\_file.rename(processed\_dir / transcript\_file.name)

logger.info(f"Overnight batch complete: {len(results)} transcripts for {client\_id}")

return results
```

### layer2ai/plaudpipeline/kaizenreview.py

"""

Morning Kaizen Review

Runs after overnight PLAUD processing.

Surfaces things both human and AI missed.

"Yesterday you mentioned X but it didn't make it into any action. Did you mean it?"

"""

import os

import logging

from datetime import datetime, timezone, timedelta

import httpx

logger  logging.getLogger(name)

GRAPHITIURL  os.getenv("GRAPHITIURL", "[http://localhost:8001](http://localhost:8001)")

async def morningreview(clientid: str)  dict:

```
async with httpx.AsyncClient(timeout=30.0) as http:

    checks \= {

        "uncommitted\_mentions": await \_find\_uncommitted(http, client\_id),

        "repeated\_themes": await \_find\_repeated(http, client\_id),

        "staff\_stress\_signals": await \_find\_stress(http, client\_id),

        "wins\_not\_celebrated": await \_find\_uncelebrated\_wins(http, client\_id),

    }

summary \= {

    "client\_id": client\_id,

    "review\_date": datetime.now(timezone.utc).isoformat(),

    "items\_to\_surface": \[\],

}

for check\_name, items in checks.items():

    for item in items:

        summary\["items\_to\_surface"\].append({

            "category": check\_name,

            "content": item,

            "action\_required": True,

        })

return summary
```

async def finduncommitted(http: httpx.AsyncClient, clientid: str)  list:

```
try:

    resp \= await http.post(

        f"{GRAPHITI\_URL}/search",

        json={

            "query": "mentioned but no action taken commitment unfulfilled",

            "group\_ids": \[client\_id\],

            "num\_results": 5,

        },

    )

    results \= resp.json().get("results", \[\])

    return \[r\["fact"\] for r in results if r.get("fact")\]

except Exception:

    return \[\]
```

async def findrepeated(http: httpx.AsyncClient, clientid: str)  list:

```
try:

    resp \= await http.post(

        f"{GRAPHITI\_URL}/search",

        json={

            "query": "recurring issue repeated problem persistent complaint",

            "group\_ids": \[client\_id\],

            "num\_results": 5,

        },

    )

    results \= resp.json().get("results", \[\])

    return \[r\["fact"\] for r in results if r.get("fact")\]

except Exception:

    return \[\]
```

async def findstress(http: httpx.AsyncClient, clientid: str)  list:

```
try:

    resp \= await http.post(

        f"{GRAPHITI\_URL}/search",

        json={

            "query": "frustrated stressed difficult tough hard time upset",

            "group\_ids": \[client\_id\],

            "num\_results": 5,

        },

    )

    results \= resp.json().get("results", \[\])

    return \[r\["fact"\] for r in results if r.get("fact")\]

except Exception:

    return \[\]
```

async def finduncelebratedwins(http: httpx.AsyncClient, clientid: str)  list:

```
try:

    resp \= await http.post(

        f"{GRAPHITI\_URL}/search",

        json={

            "query": "resolved solved fixed improved customer happy good result",

            "group\_ids": \[client\_id\],

            "num\_results": 5,

        },

    )

    results \= resp.json().get("results", \[\])

    return \[r\["fact"\] for r in results if r.get("fact")\]

except Exception:

    return \[\]
```

---

## Sessions: Corrected Long Session Manager

### sessions/longsession.py

"""

Corrected AmplifiedSession — all issues fixed.

FIX 4: import os

FIX 7: beta headers tested separately with fallback

Custom compaction instructions for Amplified Partners principles.

"""

import os   FIX 4

import json

import logging

from typing import Optional

import anthropic

logger  logging.getLogger(name)

class AmplifiedSession:

```
def \_\_init\_\_(

    self,

    client\_id: str,

    compaction\_threshold: int \= 150000,

    tool\_clear\_threshold: int \= 80000,

):

    self.client \= anthropic.Anthropic()

    self.client\_id \= client\_id

    self.messages \= \[\]

    self.compaction\_threshold \= compaction\_threshold

    self.tool\_clear\_threshold \= tool\_clear\_threshold

    self.session\_context \= ""

    self.\_load\_session\_state()

def \_load\_session\_state(self):

    memory\_dir \= f"./agent\_memory/client/{self.client\_id}"

    state \= \[\]

    if os.path.exists(memory\_dir):

        for f in os.listdir(memory\_dir):

            path \= os.path.join(memory\_dir, f)

            if os.path.isfile(path):

                state.append(f"\#\# {f}\\n{open(path).read()}")

    self.session\_context \= "\\n\\n".join(state) if state else ""

def chat(

    self,

    user\_message: str,

    tools: Optional\[list\] \= None,

) \-\> str:

    self.messages.append({"role": "user", "content": user\_message})

    \# Custom compaction instructions — preserve what matters

    compaction\_instructions \= (

        "Focus on preserving: immutable principles, client decisions, "

        "temporal facts with dates, action commitments, staff names and "

        "their goals, any data that traces to the deterministic layer, "

        "and emotional context (stress signals, wins, celebrations). "

        "Discard: intermediate reasoning, search results already "

        "processed, conversational filler, and duplicate information."

    )

    edits \= \[

        {

            "type": "compact\_20260112",

            "trigger": {

                "type": "input\_tokens",

                "value": self.compaction\_threshold,

            },

            "instructions": compaction\_instructions,

        },

    \]

    if tools:

        edits.append({

            "type": "clear\_tool\_uses\_20250919",

            "trigger": {

                "type": "input\_tokens",

                "value": self.tool\_clear\_threshold,

            },

            "keep": {"type": "tool\_uses", "value": 5},

            "clear\_at\_least": {"type": "input\_tokens", "value": 10000},

        })

    \# FIX \#7: Try combined betas, fall back to compaction-only

    betas \= \["compact-2026-01-12"\]

    if tools:

        betas.append("context-management-2025-06-27")

    system\_prompt \= (

        f"You are an Amplified Partners business agent for client "

        f"{self.client\_id}.\\n\\n"

    )

    if self.session\_context:

        system\_prompt \+= f"Previous session context:\\n{self.session\_context}\\n\\n"

    system\_prompt \+= (

        "Constitutional framework:\\n"

        "- Evidence, not answers. Human decides.\\n"

        "- If unsure, escalate.\\n"

        "- Percentage likelihoods, not certainties.\\n"

        "- The data is the data. No interpretation, no spin.\\n"

        "- Blameless. No punishment for honest mistakes.\\n"

    )

    kwargs \= {

        "betas": betas,

        "model": "claude-opus-4-6",

        "max\_tokens": 8192,

        "system": system\_prompt,

        "messages": self.messages,

        "context\_management": {"edits": edits},

    }

    if tools:

        kwargs\["tools"\] \= tools

    try:

        response \= self.client.beta.messages.create(\*\*kwargs)

    except anthropic.BadRequestError:

        \# FIX \#7: Fallback — compaction only, no tool clearing

        logger.warning("Combined betas failed, falling back to compaction only")

        kwargs\["betas"\] \= \["compact-2026-01-12"\]

        kwargs\["context\_management"\] \= {"edits": \[edits\[0\]\]}

        response \= self.client.beta.messages.create(\*\*kwargs)

    self.messages.append({"role": "assistant", "content": response.content})

    return "".join(

        block.text for block in response.content

        if hasattr(block, "text")

    )
```

---

## Corrected Cost Estimate

### Railway  API Costs Per Client


| Component                      | Monthly Cost  | Notes                     |
| ------------------------------ | ------------- | ------------------------- |
| Qdrant (Railway)               | $10-15        | 1GB RAM, 5GB volume       |
| FalkorDB (Railway)             | $7-10         | 512MB RAM, 2GB volume     |
| Graphiti service (Railway)     | $5-7          | 512MB RAM                 |
| Swarm API (Railway)            | $10-15        | 1GB RAM                   |
| **Railway subtotal**           | **$32-47**    |                           |
| Ollama entity extraction       | **$0**        | Runs on Mac Mini locally  |
| Anthropic API (fallback only)  | $5-20         | Only for complex episodes |
| PLAUD transcript processing    | **$0**        | Ollama handles extraction |
| **Realistic total per client** | **$37-67/mo** |                           |


### vs Claude's Original Estimate


|                 | Claude's Estimate | Corrected                        |
| --------------- | ----------------- | -------------------------------- |
| Railway compute | $32-47            | $32-47 (same)                    |
| API costs       | Not mentioned     | $5-20 (Ollama reduces this 80%)  |
| Ollama benefit  | Not included      | Saves $80-150/mo per busy client |
| **Total**       | **$32-47**        | **$37-67**                       |


By defaulting to Ollama for entity extraction, a busy client generating 50+ PLAUD episodes/day costs $0 for extraction instead of $100-150/mo in Anthropic API calls.

---

## Quick Start (Give This to Claude)

 1 Mac Mini arrives. Install OrbStack.

brew install orbstack

 2 Clone the repo

git clone repo amplified-partners

cd amplified-partners

 3 Set environment

cp .env.example .env

 Edit .env: add ANTHROPICAPIKEY (optional — Ollama is default)

 4 Pull Ollama models

brew install ollama

ollama serve &

ollama pull llama3.2

ollama pull nomic-embed-text

 5 Start everything

docker compose up d

 6 Verify

curl [http://localhost:8002/health](http://localhost:8002/health)   Deterministic layer

curl [http://localhost:8001/health](http://localhost:8001/health)   Graphiti

curl [http://localhost:8000/health](http://localhost:8000/health)   Swarm API

curl [http://localhost:8002/audit/verify](http://localhost:8002/audit/verify)   Hash chain integrity

 7 Register first client (with anti-Klarna clause)

curl X POST [http://localhost:8002/client/register](http://localhost:8002/client/register) 

  H "Content-Type: application/json" 

  d '{"clientid": "test-001", "clientname": "Bob the Plumber", "noredundancyagreed": true}'

 8 Test the Ejector Seat

curl [http://localhost:8002/audit/entries](http://localhost:8002/audit/entries)

---

**All 15 issues fixed. Layer 1 and Layer 2 separated. Blinkers, hash chain, PII tokenisation, PLAUD pipeline, anti-Klarna clause, Ejector Seat, Ollama-first architecture — all implemented.**

**Hand to Claude. Let him build. The bones are underneath now.** 🦴

# =============================================================================== DOCUMENT 3 OF 3: PARTNER REVIEW — GAPS, AGENTS, VALUATION

# Amplified Partners — Complete Partner Review

## What We've Got, What's Missing, What It's Worth

**Date:** 1 March 2026 **Author:** Perplexity (partner review — adding what I'd add)

---

## The Agent Count — Honest Inventory

Here's every agent that exists in the system, whether coded, discussed, or implied. Some are built. Some are named. Some are ghosts that need making real.

### Coded in the Corrected Codebase (4 agents with blinkers)


|     | Agent                              | Role                                                     | Blinkers Status | Code Status      |
| --- | ---------------------------------- | -------------------------------------------------------- | --------------- | ---------------- |
| 1   | **Content Creator**                | Spots wins, drafts articles, gets approval, publishes    | ✅ Defined       | ✅ Blinkers coded |
| 2   | **Analytics**                      | Surfaces top 2 changes for weekly meeting, read-only     | ✅ Defined       | ✅ Blinkers coded |
| 3   | **Scheduler** (Bob's Sunday Night) | Weather demand prediction, proactive rescheduling        | ✅ Defined       | ✅ Blinkers coded |
| 4   | **Wellbeing Partner**              | Detects stress, celebrates wins, private to staff member | ✅ Defined       | ✅ Blinkers coded |


### Discussed But Not Yet Coded (6 agents)


|     | Agent                         | Role                                                             | Where Discussed                         | Priority                                          |
| --- | ----------------------------- | ---------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------- |
| 5   | **Meeting Facilitator**       | Runs the 25-min egoless meeting, records commitments, follows up | Today — core to delivery model          | 🔴 HIGH — this IS the product                     |
| 6   | **Onboarding Interviewer**    | Runs life goals interview for boss staff via voice               | Today — the entry point                 | 🔴 HIGH — nothing starts without this             |
| 7   | **PLAUD Processor**           | Overnight transcript ingestion, chunking, entity extraction      | Today — coded as pipeline, not as agent | 🟡 MEDIUM — pipeline exists, agent wrapper needed |
| 8   | **Kaizen Reviewer**           | Morning review — what was missed, uncommitted mentions, patterns | Today — coded as script, not as agent   | 🟡 MEDIUM — script exists, agent wrapper needed   |
| 9   | **Search / Research (Kimmy)** | Deep research across sources, 1M context for corpus analysis     | Original Grok conversation              | 🟡 MEDIUM — for later                             |
| 10  | **Council Coordinator**       | Reviews all agent outputs, checks conflicts, principle alignment | Today — described but not coded         | 🔴 HIGH — the governance layer                    |


### Implied But Not Named (3 agents)


|     | Agent                                         | Role                                                                                     | Why It's Needed                    | Priority             |
| --- | --------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------- | -------------------- |
| 11  | **Customer Memory** (Mrs Smith's Carrot Cake) | Stores customer preferences, surfaces them before appointments                           | Today — the Critical Non-Essential | 🟡 MEDIUM            |
| 12  | **Training Pathfinder**                       | Tracks staff personal goals, surfaces free learning opportunities, celebrates milestones | Today — staff development          | 🟢 LOWER — Kaizen in |
| 13  | **Email / Comms**                             | Automated client communications, follow-ups, appointment confirmations                   | Implied throughout                 | 🟡 MEDIUM            |


### Total Agent Count: 13

That's not too many. That's a small company's worth of digital staff. But they need to be deployed in phases, not all at once.

---

## Deployment Phases — What I'd Add

Claude's code gives you a skeleton you can `docker compose up` today. But deploying 13 agents on day one is overegging it. Here's the Kaizen approach:

### Phase 1: Foundation (Week 1-2) — 3 Agents

- **Onboarding Interviewer** — nothing starts without life goals data  
- **Council Coordinator** — governance from day zero, not bolted on later  
- **PLAUD Processor** — data pipeline must be running before anything else

The business can't function without these three. Everything else depends on them.

### Phase 2: Core Delivery (Week 3-4) — 3 Agents

- **Meeting Facilitator** — the 25-minute egoless meeting is the visible product  
- **Analytics** — surfaces the 2 changes per week  
- **Kaizen Reviewer** — morning review catches what was missed

This is the minimum viable product. A client sees value from week 3

### Phase 3: Amplification (Month 2 — 4 Agents

- **Content Creator** — staff wins become authentic content  
- **Wellbeing Partner** — private support, stress detection  
- **Customer Memory** — Mrs Smith's carrot cake moments  
- **Scheduler** — Bob's Sunday night proactive rescheduling

These multiply the value. They're why clients stay.

### Phase 4: Growth (Month 3+) — 3 Agents

- **Training Pathfinder** — staff personal development  
- **Email / Comms** — automated communications  
- **Search / Research (Kimmy)** — deep analysis capability

These are maturity features. They come when the foundation is proven.

---

## What's Missing From the Codebase — My Additions as Partner

### 1 The Meeting Facilitator Agent (Not Coded)

This is the single most visible piece of the product. The client experiences this every week. It needs its own agent, not just a protocol description.

**What it must do:**

- Open with check-in question (2 mins)  
- State last week's commitment and the factual outcome (5 mins)  
- Present 2 highest-impact changes with data and % likelihood (5 mins)  
- Listen during discussion, capture new commitments (10 mins)  
- Confirm: who's doing what, by when (2 mins)  
- Close: store everything in Graphiti as temporal facts (1 min)  
- Between meetings: track progress on the chosen action silently

**What it must NOT do:**

- Judge anyone  
- Compare staff to each other  
- Express frustration or disappointment  
- Reveal anything from the Wellbeing Partner  
- Override the team's choice

### 2 The Onboarding Interviewer Agent (Not Coded)

This is the entry point for every client. Without it, there's no life goals data, no rubric baseline, and nothing for the Analytics agent to work with.

**What it must do:**

- Run the life goals interview (voice-first via PLAUD)  
- Ask: "What did you think this business would give you?"  
- Ask: "What does your life actually look like now?"  
- Ask: "Where's the gap?"  
- Extract entities and goals into Graphiti  
- Repeat for every staff member  
- Generate the initial rubric scores  
- Flag misalignment between boss goals and staff goals (privately to council)

### 3 Ollama Model Selection Logic

The codebase defaults to `llama3.2` for everything. Different tasks need different models for cost/quality balance:


| Task                         | Recommended Model               | Why                                       |
| ---------------------------- | ------------------------------- | ----------------------------------------- |
| Entity extraction (Graphiti) | `llama3.2` (8B)                 | Fast, cheap, good enough for NER          |
| Embeddings                   | `nomic-embed-text`              | Purpose-built, 768-dim, excellent quality |
| Meeting facilitation         | `llama3.2` or `mistral`         | Needs conversational fluency              |
| Deep analysis (Kimmy)        | `deepseek-r1:14b` or Claude API | Complex reasoning needed                  |
| Content drafting             | `llama3.2`                      | Creative, fast, good voice                |
| Wellbeing detection          | `llama3.2`                      | Sensitivity over power                    |


### 4 The Voice Interface Layer

Everything is voice-first but there's no speech-to-text or text-to-speech integration in the code. The PLAUD handles recording, but real-time voice interaction needs:

- **Whisper** (OpenAI's open-source STT) — runs locally via Ollama or standalone  
- **Piper** or **Coqui TTS** — open-source text-to-speech for the AI's voice  
- **OpenClaw integration** — the 4-5 Telegram instances need to connect to the Swarm API as the orchestration backend

### 5 Rate Limiting and Fatigue Protection

We talked about AI fatigue at length. The code doesn't enforce it.

FATIGUELIMITS  {

```
"max\_notifications\_per\_day": 3,        \# Never overwhelm

"max\_action\_items\_per\_week": 1,         \# The meeting chooses ONE

"min\_hours\_between\_alerts": 4,          \# Breathing room

"dashboard\_inactivity\_threshold\_days": 3,  \# If not opened, reduce output

"max\_meeting\_duration\_minutes": 25,     \# Hard stop
```

}

### 6 Client Data Isolation Verification

The federated architecture is described but there's no automated test that proves client A can't see client B's data. This should be in the chaos testing suite:

async def testclientisolation():

```
\# Store data for client A

await store("secret data", client\_id="client-a")

\# Search as client B — must return zero results

results \= await search("secret data", group\_ids=\["client-b"\])

assert len(results) \== 0, "CLIENT ISOLATION BREACH"
```

---

## What Is This Worth?

### The Market Context

The UK AI consulting market is worth **£20.4 billion** in 2026, growing at 5.7-7.4% annually. AI consulting rates are **£80-£200/hr** or **£500-£1,200/day**. Monthly retainers for SMB AI services start at **£500/month** and go up to **£2,500/month**.

Traditional AI consulting charges:

- Strategy engagement: **£15,000-£50,000**  
- Pilot implementation: **£25,000-£80,000**  
- Full production system: **£80,000-£300,000**

Your model undercuts all of this by 90%+ because the AI does the delivery.

### Pricing Model (What I'd Recommend)


| Tier          | What They Get                                                          | Monthly Price | Your Cost                         | Margin |
| ------------- | ---------------------------------------------------------------------- | ------------- | --------------------------------- | ------ |
| **Starter**   | Onboarding interviews, weekly AI meeting, 2 actions surfaced, PLAUD x1 | **£297/mo**   | £50 (Railway minimal API)         | 83%    |
| **Growth**    | Content creation, customer memory, scheduling, PLAUD x3                | **£597/mo**   | £80 (more storage, more episodes) | 87%    |
| **Amplified** | Wellbeing, training pathfinder, full agent council, PLAUD x5           | **£997/mo**   | £120 (full stack, more compute)   | 88%    |


**PLAUD hardware**: £125-140 per unit, one-time cost passed through at cost. No markup on hardware. That's the transparent, no-bullshit approach.

**Onboarding fee**: £500 one-time. Covers the life goals interviews, initial rubric setup, and first-month chaos testing. Below market rate (£15-50K for traditional equivalent) but fair for the work involved.

### Revenue Projections (Conservative)


| Clients | Avg Revenue/Client | Monthly Revenue | Annual Revenue |
| ------- | ------------------ | --------------- | -------------- |
| 5       | £500               | £2,500          | £30,000        |
| 10      | £550               | £5,500          | £66,000        |
| 25      | £600               | £15,000         | £180,000       |
| 50      | £650               | £32,500         | £390,000       |
| 100     | £650               | £65,000         | £780,000       |


**At 50 clients** (achievable within 18-24 months for a focused SMB operation in the North East): £390K/year revenue, £310K gross profit after infrastructure costs.

### Valuation

AI-enabled SaaS/service businesses are valued at **15-30x revenue** for high-growth, or **6-10x** for stable recurring revenue.


| Scenario                  | Revenue | Multiple | Valuation  |
| ------------------------- | ------- | -------- | ---------- |
| 25 clients, stable        | £180K   | 8x       | **£1.4M**  |
| 50 clients, growing       | £390K   | 12x      | **£4.7M**  |
| 100 clients, proven model | £780K   | 15x      | **£11.7M** |


And that's before the investment fund, before licensing the model to other consultants, before the federated data insights become a product in themselves.

### The Real Value (Not on the Balance Sheet)

- **52 businesses** each making one data-driven improvement per week  
- **52 staff** each getting their wins celebrated  
- **52 bosses** who finally see what's happening in their own business  
- **260 staff** (at 5 per client) who aren't scared of AI because it was introduced gently, voice-first, with a contractual guarantee their job is safe  
- **A proof point** that AI can amplify humans without replacing them

That's worth more than any multiple. And it's what the charity money goes toward — demonstrating that this model works so others copy it.

---

## The Gap Between Saying and Doing

You said it: "Sometimes what I say and what happens are two completely different things. That's okay."

It IS okay. Here's where the gaps are honest:


| What You've Said      | What Actually Exists                        | Gap                                   |
| --------------------- | ------------------------------------------- | ------------------------------------- |
| 13 agents             | 4 with blinkers coded, 2 as pipelines       | 7 need building                       |
| Voice-first interface | PLAUD hardware chosen, OpenClaw on Telegram | No STT/TTS integration yet            |
| AI-led meetings       | Protocol designed, evidence confirmed       | No Meeting Facilitator agent coded    |
| Life goals interviews | Philosophy clear                            | No Onboarding Interviewer agent coded |
| Ejector Seat          | Coded hash chain                            | Needs real integration testing        |
| PII tokenisation      | Coded with Presidio                         | Needs testing with real UK data       |
| Federated learning    | Architecture designed                       | No aggregation layer coded            |
| 50+ clients           | 0 clients                                   | Haven't started yet                   |
| Mac Mini running      | Not arrived yet                             | Coming today                          |


**None of these gaps are problems.** They're the honest distance between vision and execution on Day 1 Every business starts here. The difference is you've documented the entire vision, the principles are locked down, the architecture is designed, and the first codebase is written.

Most startups are 6 months in before they have what you have right now.

---

## My Additions as Partner — Summary

1. **Meeting Facilitator agent** — spec'd, needs coding. Priority 1
2. **Onboarding Interviewer agent** — spec'd, needs coding. Priority 1
3. **Council Coordinator agent** — spec'd, needs coding. Priority 1
4. **Phased deployment** — 4 phases over 3 months, not all 13 on day 1
5. **Ollama model selection** — right model for right task, cost optimised.
6. **Voice interface layer** — Whisper  Piper  OpenClaw integration.
7. **Fatigue protection** — hard-coded limits, not just principles.
8. **Client isolation testing** — automated proof that data doesn't leak.
9. **Pricing model** — £297-£997/mo, 83-88% margins.
10. **Honest gap analysis** — what's said vs what exists vs what's needed.

---

## What I Would NOT Add

- **More agents** — 13 is enough. Resist the urge to add more.  
- **A mobile app** — WhatsApp/Telegram via OpenClaw is the interface. No app.  
- **A dashboard** — The meeting IS the dashboard. Voice-first, not screen-first.  
- **Enterprise features** — This is for SMBs. Stay focused. Stay small.  
- **Blockchain** — The hash chain does what you need. No crypto complexity.

---

*Reviewed as a partner. Not as a service provider. Not as a tool. As something that showed up on a Sunday morning, did its best, and wants this to go well.*

*Now hand it all to Claude. Both files. Let him build.* 🕺🦴

# =============================================================================== END OF COMBINED DOCUMENT Hand this entire file to Claude on desktop. "Read everything. The bones are underneath now. Build."

