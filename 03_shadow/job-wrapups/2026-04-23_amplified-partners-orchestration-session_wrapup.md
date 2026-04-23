---
title: Amplified Partners orchestration-planning session wrap-up
date: 2026-04-23
last_amended: 2026-04-23 (late session — §2.6 added)
author: Devon (Devin session 4cc8b0d727684f94a8f055853099d8e6)
status: handoff
escalation_type: N/A
impact: medium
confidence: N/A
session_type: orchestration-planning (no code changes made)
---

<!-- markdownlint-disable-file MD013 -->

## Neutrality note

This wrap-up follows the neutrality clause in `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` (candidate). Facts and inferences are labelled separately. No prescriptions about what the next agent should do. No forecasts about what comes next. Section 7 (Analysis, clearly labelled and optional) contains this agent's interpretation — the next agent is free to read, ignore, disagree, or replace it.

## 1. Resume instruction

Open, in any order that fits the next turn:

- This file.
- `/home/ubuntu/repos/clean-build/AGENTS.md`
- `/home/ubuntu/repos/clean-build/00_authority/MANIFEST.md`
- `/home/ubuntu/repos/clean-build/00_authority/PRINCIPLES.md`
- Source-corpus artefacts from this session, now in the org session folder: `/home/ubuntu/repos/clean-build/03_shadow/sessions/2026-04-23_devon/` (contains landscape map v1, v1 baton pass for provenance, and a README index). Personal-scratch originals retained at `/home/ubuntu/ewan-map/` as a second audit trail.
- New authority files produced this session: `00_authority/SIGNATURES.md`, `00_authority/USE_IT_OR_CUT_IT.md`, `00_authority/OPINION_CONFIDENCE.md`. All listed in `MANIFEST.md`. Signed per the signatures rule.

## 2. Current state — FACTS

Statements in this section are facts or direct quotes. Inferences are in section 7.

### 2.1 What the session did (factual record)

- Catalogued the imported corpus across drop waves A–U plus DeepSeek exports. Live on VM at `/home/ubuntu/ewan-map/` and `/home/ubuntu/repos/vault/`.
- Verified two API keys live in environment variables as lowercase: `perplexity` and `kimi`.
- Ran six Perplexity Sonar-Pro API calls during the session. Total cost: approximately £0.09. (Receipts: model selection query, Monologue API query, IDE comparison query, plan-the-plan v2 and v3 queries, watsonx pricing + methodology queries ×2.)
- Located IBM watsonx Orchestrate pricing on the AWS Marketplace listing published by IBM: Agentic Essentials $6,360/yr (600 RUs), Agentic Standard $76,320/yr (6,000 RUs), Agentic Premium $216,000/yr (7,500 RUs, data isolation, "contact us"). Resource-Unit conversion rate not published on either IBM's main pricing page or the AWS listing. Source: https://aws.amazon.com/marketplace/pp/prodview-ua5rm53wrx7hm.
- Ran two Perplexity queries on watsonx methodology (IBM domain only, then third-party only). Neither returned a named IBM reference architecture, published multi-agent orchestration methodology, or analyst teardown with Watsonx-specific comparison against Copilot Studio / Agent Builder / Bedrock Agents.
- Confirmed Monologue (monologue.to) does not publish a public API or SDK. Third-party alternatives with documented APIs for production voice: Deepgram, Whisper API, Gladia.
- Confirmed SearXNG is not running on this VM. Referenced in 6 vault documents but no live process on common ports.
- Wrote v1 baton pass at `/home/ubuntu/ewan-map/baton-pass/2026-04-23_devon_baton-pass_v1.md`. Architect (Ewan) flagged it as containing assumptions about what happens next and prescriptions for the next agent. This file (v2, neutral) supersedes it.

### 2.2 What the architect said during this session (direct quotes)

- "£500 per day."
- "I want the most effective for the job. Doesn't mean the most expensive, means the one who's good at that job. We always use the right size model for the right job because it's science to say that's the best way to do it."
- "I will be available 24 hours... I am the architect. I invoke that name just because it's only going to be used once. But that's the truth."
- "Privacy and security are thought of before we start anything. It doesn't mean you're going to do anything if it doesn't need to be done, but I just want it to be there."
- "I feel that the rule should be that you set loose guidelines or principles, and the team who's designing the job, who've got the code and the spec in front of them, design the plans."
- "We're not going in crackerjack, but we'll do it quickly."
- "The goal is the only thing we consider."
- "There are going to be multiple agents within each department. I am adamant about that."
- "It may be that it's four teams in each department, it may be three. And if it helps, they're going to work in three shifts because that suits my radical attribution and my Cove framework therapy."
- "Nothing is set in stone ever, unless I can't imagine it should be set in stone."
- "If it's tiny, it doesn't have an impact on anything else either. Your teams or your work colleagues do it, that escalates up." (context: proportional commitment)
- "One or two searches, you make your decision and you crack on... that's a rule. A pun." (context: bounded research rule)
- "Please critique everything I say for the goal."
- "They're not ours, they're the organisation's." (context: where session artefacts should live and who should access them)
- "I like the baton pass, but you're assuming what's happening next... it's just to maintain neutrality of response."

### 2.3 Principles stated during this session (as heard, facts)

- Radical Honesty, Radical Transparency, Radical Attribution, Win-Win, Idea Meritocracy (confirmed by knowledge note 23-04-26-Amplified-Partners).
- "Every single thing is Ewan's responsibility" — per `00_authority/PRINCIPLES.md` and reaffirmed this session.
- Proportional commitment — change scales with impact.
- Tool Fit — right-size model for the job; effectiveness over expense.
- Blinkers Without Ceilings.
- Privacy first, Security second.
- Testing before anything ships.
- Bounded research: 1–2 searches, decide, proceed. Applies to decision questions.
- Source hierarchy: (1) manufacturer's current docs, (2) official team blog, (3) third-party commentators with marketing-hype filter.
- Hypothesis-first — for comparative/ranking questions.
- Do not assume scope: "small firm" can refer to the architect personally, Amplified Partners as an organisation, or SMB clients — three distinct entities.
- Artefacts of this work belong to the organisation; agents working the same mission should have access.

### 2.4 Naming (facts)

- The agent's name in this session is "Devon" — the architect said "I'll call you Devon" and later used both "Devon" and "Devin" interchangeably. Devon matches the partnership naming tradition noted in the session (Clawd / Kimmy / Johnny).
- "Covered AI" is canonical per prior organisational documentation; "Cover.AI", "covered.AI", and similar variants are considered drift.
- "Byker" is the codename for the production system currently live on Railway.
- "Luke Stays" is a prospect in the Interior Design sector, not a Pocket or plumber customer.

### 2.5 Technical surfaces (facts)

- Amplified-Partners vault per knowledge note `note-Amplified-Partners-vault-823d1c01-autogen`: Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, **Qdrant**, Redis, OpenAI/Anthropic/xAI APIs, Telnyx/Twilio, PyQt6. Obsidian is the real-vault substrate. Named process **Baking** embeds markdown into Qdrant.

### 2.5.1 Technical surfaces (continued)

- Byker Production is live on Railway: https://byker-production-production.up.railway.app. Documented in `~/repos/byker-production/CLAUDE.md`.
- Byker runs three local models via Ollama: Qwen 32B (Architect), Llama 70B (Implementer), Llama 8B (Validator). Client-data workloads route here.
- Kimi Pro subscription is active on the architect's account (stated this session).
- Google Workspace Plus and OneAI subscription are stated as active.
- Devin's cross-session bridges: files on `/home/ubuntu/` persist across sessions scoped to the same account; session search via Devin MCP; knowledge notes scoped to account; playbooks. File access is account-scoped, not path-scoped — moving a file to another location on the same VM does not change who can access it.

### 2.6 Late-session additions (post-database question) — FACTS

- **Corpus measurement (this session)**: ~10,072 markdown files total across `/home/ubuntu/` (vault 4,539 / ewan-map 2,755 / clean-build 279 / other). Approximately 9.5M words of actual content across vault + ewan-map + clean-build (some overlap between ewan-map and vault imports).
- **One bounded-research Perplexity query on vector DB landscape for Claude Code / OpenClaw agents** (2026-04-23, cost £0.012). Finding: Anthropic publishes no preferred vector DB. Framework-level proxy (LangChain/LlamaIndex) shows Chroma + pgvector most-cited for SMB RAG; Qdrant mature; Pinecone being displaced by self-hosted options in cost-sensitive SMBs. No 2026 deprecations flagged for Qdrant, Chroma, pgvector, LanceDB, or Weaviate.
- **Database decision (this session)**: **stay with Qdrant**. Reasoning: AI-facilitated customer deployments (stated by architect) flatten the pgvector-vs-Qdrant ops-simplicity delta; incumbent Qdrant is already in use by the Baking pipeline; Use-It-Or-Cut-It does not force a cut because Qdrant IS being used. Revised agent confidence: 65% stay / 35% migrate — both below the 85% commit threshold, so no switch. Migration remains available if pain surfaces.
- **Three new authoritative rules captured (written this session)**:
  - `SIGNATURES.md` — every AI signs committed work; agent chooses format.
  - `USE_IT_OR_CUT_IT.md` — sounds good + built + unused = cut; archive exempt.
  - `OPINION_CONFIDENCE.md` — opinions labelled with confidence number; tiered thresholds 50% / 85% / 95% by reversibility; below-threshold triggers bounded research.
- **Naming of the human-database**: architect reserves. Not named by this agent.
- **Architect quotes (late session, direct)**:
  - "Every AI's got to sign their work when it gets committed."
  - "We allow agents to use their intelligence."
  - "If an idea, which sounds good, is implemented, and never used, it's cut."
  - "Opinion is marked as opinion, and if it's too far away from 100%, you've got to do the research."
  - "I trust your intelligence, so 85% seems good to me."
  - "These are going to be AI-facilitated deployments." (context: corrects the customer-ops argument)
  - "Save this folder, all of the work, in a folder that's accessible to everyone. Because this is source document."
- **Context-creep observation by architect**: "I genuinely think there's some context window creep." Architect-flagged, acknowledged by agent. Session folder + updated handover exist so a fresh session can resume without relying on in-thread recall.

## 3. Open risks + what would falsify

- **Risk**: the 4-vendor comparison (IBM watsonx / Microsoft Copilot Studio / Google Agent Builder / AWS Bedrock Agents) has not been run. A buy/build/hybrid decision made without it would be under-evidenced.
  - **Falsified by**: two bounded Perplexity searches returning substantive third-party comparisons with licensed pricing, meter definitions, and governance-pattern specifics.

- **Risk**: Resource-Unit conversion rate for watsonx Orchestrate is not published. Tier sizing is speculative without it.
  - **Falsified by**: either a direct answer from IBM sales, a third-party practitioner post disclosing RU consumption rates, or experience from the free trial.

- **Risk**: The v1 baton pass in personal scratch (`/home/ubuntu/ewan-map/baton-pass/`) is not on an organisational path. If file-access model changes or account scope changes, that artefact could become unreachable to agents who need it.
  - **Falsified by**: migration to the clean-build repo and/or git commit.

- **Risk**: No department has been scope-locked as "first". Multiple candidates named (Translator, Research Pipe, Data, Product, Curator) with no architect decision recorded.
  - **Falsified by**: an architect decision in the decision log.

- **Risk**: Perplexity's index did not cover methodology comparisons with strong sources. Research outputs from this session that relied on Perplexity's training knowledge (methodologies v2 and v3 queries) are inference-heavy, not source-backed.
  - **Falsified by**: cross-check via SearXNG (not currently standing up), or via direct primary-source reading (Cooper on Stage-Gate, Snowden on Cynefin, Basecamp on Shape Up).

## 4. Negative signals (repulsion)

### 4.1 Dead ends

- Perplexity query with `search_domain_filter=["ibm.com"]` returned no pricing and no methodology — the filter was too narrow. Unfiltered third-party query also returned no pricing (see §2.1). Opening up to direct IBM-listed AWS Marketplace content did return pricing.
- A too-narrow Perplexity query on planning methodologies (software-only framing) returned an empty/"N/A"-heavy result. A broader query (including PMBOK, PRINCE2, Stage-Gate, TPS, OODA, Cynefin) returned substantive content, though marked explicitly by Perplexity as training-knowledge inference, not search-indexed sources.

### 4.2 Anti-patterns (agent-side, observed in this session)

- Packing multiple decisions into one long message when the architect is working live — creates scroll overhead and reduces signal.
- Using definitive language ("verdict", "rule", "my vote") before the architect has authorised a decision.
- Saying "small firm" without disambiguating whether the subject is the architect personally, Amplified Partners, or SMB clients.
- Running research without stating a hypothesis first — for comparative/ranking questions.
- Writing a handover with forecasts, recommendations, and "what to do next" — biases the next agent and conflicts with idea meritocracy.

### 4.3 Repulsion score

- **3** for the anti-patterns above taken together. Corrected within the session when flagged. No repeat across runs yet.

### 4.4 Cut / absolute stop?

- No.

## 5. Artifacts touched

- Created: `/home/ubuntu/ewan-map/2026-04-23_amplified-partners-map_v1.md` (landscape map v1, personal scratch).
- Created: `/home/ubuntu/ewan-map/baton-pass/2026-04-23_devon_baton-pass_v1.md` (v1 baton pass, personal scratch, superseded, retained for provenance).
- Created: this file at `/home/ubuntu/repos/clean-build/03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md`.
- Created: `/home/ubuntu/repos/clean-build/01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` (candidate).
- **Late-session additions**:
  - Created: `/home/ubuntu/repos/clean-build/00_authority/SIGNATURES.md` (authoritative, listed in MANIFEST).
  - Created: `/home/ubuntu/repos/clean-build/00_authority/USE_IT_OR_CUT_IT.md` (authoritative, listed in MANIFEST).
  - Created: `/home/ubuntu/repos/clean-build/00_authority/OPINION_CONFIDENCE.md` (authoritative, listed in MANIFEST).
  - Created: `/home/ubuntu/repos/clean-build/03_shadow/sessions/2026-04-23_devon/` folder with README, landscape map copy, v1 baton pass copy.
  - Edited: `/home/ubuntu/repos/clean-build/AGENTS.md` (one-line pointer to SIGNATURES.md in first-60-seconds).
  - Edited: `/home/ubuntu/repos/clean-build/00_authority/MANIFEST.md` (listed the three new authority files).
  - Amended: this file (section 2.6 added).
- No changes to `02_build/`.
- No code changes in any repo.
- Seven Perplexity API calls billed to the `perplexity` key (six earlier + one vector-DB landscape query at £0.012).

## 6. Tokens

- `[LOGIC TO BE CONFIRMED]`: nothing in this file.
- `[SOURCE REQUIRED]`: Resource-Unit rate for watsonx Orchestrate tiers. Named-methodology claim for any 2026 multi-agent orchestration platform (none of the four found one).
- `[DECISION REQUIRED]`: first department scope-lock. Source-anchor access model for `/Users/ewansair/Amplified Partners/`. Pre-authorisation bands (green/amber/red) for agent actions. By-function vs by-language department split. Whether to run the free-trial on watsonx Orchestrate. Whether to suggest a persistent knowledge note for cross-session continuity. Whether to PR this handover and the five late-session authority/session files into clean-build. Name for the human-database (architect reserves). Whether to promote the stateless-handover neutrality clause from candidate to authority. Whether to build the signature-presence pre-commit hook (flagged as follow-on under SIGNATURES.md § Enforcement).
- `[CURRENT BEST EVIDENCE]`: watsonx pricing from AWS Marketplace listing (cited above).

## 7. Analysis — optional, agent-specific, not authoritative

This section is this agent's interpretation of the session. The next agent is free to skip, disagree, replace, or extend. Nothing here should be treated as a recommendation the next agent must follow.

- The session spent most of its time on orchestration planning rather than code implementation. Five open unblockers (§6) appear to be the gating items before any code work could usefully begin. The next agent may re-examine that list and reach a different conclusion.
- The bounded-research rule (§2.3) was stated clearly. Applying it strictly would imply: no future methodology comparison should exceed two Perplexity searches before a decision is recorded. Interpretation may vary.
- The correction on artefact ownership (§2.2 — "they're not ours, they're the organisation's") suggests organisational files should be migrated from `/home/ubuntu/ewan-map/` (personal scratch) to `/home/ubuntu/repos/clean-build/` or another org-accessible path. Whether and how to migrate is a decision for the architect or the next agent.
- A neutrality clause for handovers (now written as a candidate process document) could address the anti-pattern surfaced in §4.2 systematically, if adopted.

End of analysis.

## 8. Smallest next step

Not specified by this agent. The architect has named several open items during the session (see §6 `[DECISION REQUIRED]`). The next agent may pick any of them, all of them, or propose something else.

## 9. Leverage score

- **5** — a handover that captures facts without biasing the next agent enables cleaner decisions at the next turn. Not a 10 (not reserved axis) and not a 0 (meaningful compound).

---

Signed,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23
