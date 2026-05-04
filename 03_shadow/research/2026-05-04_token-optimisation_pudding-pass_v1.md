---
title: "Token-optimisation pudding pass — Phase 2 scope (research, no code)"
date: 2026-05-04
version: 1
status: candidate
authors:
  - "Devon-6ca5 | Devin (Cognition AI) | session devin-6ca57553eefe4806b613070325964703"
methodology: "Pudding Technique (Don R. Swanson 1986, adapted by Ewan Bramley + Claude). PUDDING 2026 taxonomy (WHAT.HOW.SCALE.TIME) per `90_archive/specifications/mac-drop-2026-04/pudding-taxonomy-synthesis.md`."
---

<!-- markdownlint-disable-file MD013 -->

## 0. What this is

A **research-only** pass scoping Phase 2 of the cost-tools work. Phase 1 (`AMP-28`) shipped the Anthropic-only token-proxy with four routing/cache strategies in production (cascading, prompt caching, semantic caching, vendor compaction). This document does the homework before building any more: it researches the named techniques in the field, scores each through a rubric tied to the Amplified Partners objective, applies the PUDDING 2026 taxonomy, and looks for symbiotic combinations that produce more saving than either ingredient alone.

**Output is not code. It is a written scoping doc.** The recommendations at the bottom are decisions for Ewan, not commitments to build.

**Lens:** *"Save tokens on Anthropic-routed agent traffic without breaking quality on the long tail of real prompts."* The lens determines which dimensions matter and which combinations rise. Without a lens you get noise; with the lens you get recipes.

**Methodology:**

1. Research the 5+ best named techniques (not summaries, not hand-waves)
2. Score each through the rubric
3. Apply the neutral PUDDING 2026 label (`WHAT.HOW.SCALE.TIME`)
4. Match on labels — same code across different domains is a high-signal pudding candidate (P(identical 4/4) = 1/2058 = 0.049%, p < 0.001 per `90_archive/specifications/mac-drop-2026-04/pudding-taxonomy-synthesis.md` § 19)
5. Re-score the combinations through the same rubric — does the combination produce something neither ingredient could alone?
6. Recommend the top 2–3 to build, with effort estimates

---

## 1. Research — 10 named techniques (sourced)

Cast wider than the off-the-cuff list of 6 from the cost-tools resurrection wrap-up. Sources are vendor docs, peer-reviewed papers, and engineering write-ups from teams shipping at scale. **No academic citation theatre — one source per technique, the most load-bearing.** Already-shipped strategies are listed for completeness so the bridge-finding step can reason over the full set.

| # | Technique | Status (in cost-tools) | Source |
|---|-----------|------------------------|--------|
| 1 | **Model cascading / preference routing** (route easy prompts to a cheaper model, hard prompts to a stronger model) | Shipped (regex classifier in `token_proxy.py`) | RouteLLM, LMSYS (Ong et al., 2024) — [paper](https://arxiv.org/abs/2406.18665), [blog](https://lmsys.org/blog/2024-07-01-routellm/) — claims **2× cost reduction without quality loss** at 50% routing rate; ~80% saving for 90% GPT-4 quality |
| 2 | **Prompt caching** (vendor-side cache of stable prefixes — system prompt, tools, retrieved documents) | Shipped (passthrough — Anthropic native) | [Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching), [Anthropic pricing table](https://docs.anthropic.com/en/docs/about-claude/pricing) — **cache hits at $0.30/MTok vs $3.00/MTok base for Sonnet 4.6 = 90% off** input on cached tokens; cache writes priced 1.25× (5min) or 2× (1h) |
| 3 | **Semantic caching** (embed the question; if cosine ≥ threshold against a past question, return the cached answer instead of calling the model) | Shipped (Qdrant `llm_cache` collection, 0.95 similarity, 24h TTL) | LiteLLM Qdrant adapter — [source](https://github.com/BerriAI/litellm/blob/d251238b/litellm/caching/qdrant_semantic_cache.py); production case study (Antigravity Lab, 2026) — [link](https://antigravitylab.net/en/articles/app-dev/antigravity-llm-semantic-cache-production-guide) — claims **~80% cost cut on chatbots with repetitive query patterns** |
| 4 | **Server-side compaction** (vendor auto-summarises older turns when input approaches context window) | Shipped (passthrough — Anthropic beta header `compact-2026-01-12`) | [Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/compaction) — supported on Opus 4.5/4.6/4.7 + Sonnet 4.6 + Mythos preview; trades input tokens for a stored summary |
| 5 | **Message Batches API** (async submission of up to 10,000 queries per batch, processed in <24h, **50% off** all input + output tokens) | **Not shipped** | [Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/message-batches), [launch post](https://anthropic.com/news/message-batches-api) — flat **50% discount** on every batched call vs. real-time pricing |
| 6 | **MCP / tool-definition compression** (compress the tool schemas the agent loads upfront so the model sees a small wrapper, expands schemas on demand only) | **Not shipped** | Atlassian Labs, [`mcp-compressor`](https://www.atlassian.com/blog/developer/mcp-compression-preventing-tool-bloat-in-ai-agents) — **70–97% reduction** on tool-description tokens (GitHub MCP: 17,600 → 500 tokens at max). Anthropic's own [code-execution MCP approach](https://brightbean.xyz/blog/code-execution-mcp-efficient-ai-agents/) reports **150,000 → 2,000 tokens (98.7%)** on agent loops. StackOne benchmark — [link](https://www.stackone.com/blog/mcp-token-optimization/) |
| 7 | **Schema-constrained / structured output** (force valid JSON via grammar / function-call schema, drop the chain-of-thought tokens that "explain" the answer) | **Not shipped** | OpenAI structured outputs + Anthropic tool-use schemas — [comparison](https://www.kalviumlabs.ai/blog/structured-output-from-llms-json-mode-function-calling/) reports **8–12% schema-violation rate on raw JSON mode → ≈0% on schema-validated tool calls**; recovers a measurable fraction of "Sonnet-only" prompts as Haiku-eligible because output reliability stops being the bottleneck |
| 8 | **Local-first routing** (route short factual / classification queries to a free local model — Ollama on Beast — before paying any API call) | **Not shipped** (Ollama running, not in proxy path) | LiteLLM model-router pattern; same logic as RouteLLM but with a zero-cost first tier. Beast has Llama 3.1 8B/70B and Qwen3 Coder 30B already loaded per the org-wide CRM & Beast knowledge note |
| 9 | **Chain of Draft (CoD)** (replacement for Chain of Thought — instruct the model to keep each reasoning step to ~5 words; matches CoT accuracy with **~92% fewer reasoning tokens**) | **Not shipped** | Token Optimize Dev, *Token-Efficient Prompting Patterns* — [link](https://www.tokenoptimize.dev/guides/token-efficient-prompting-patterns); references the 2025 CoD paper. **Caveat:** for reasoning models that already do internal CoT (`o3-mini`, `o4-mini`), explicit CoD is largely redundant — gain is on classical models like Sonnet/Haiku. |
| 10 | **Mid-session context condensation** (client-side condenser agent compresses chat history to fit a budget, replacing old turns with a summary) | **Not shipped** | Oracle MT-OSC paper — [arXiv 2604.08782](https://arxiv.org/pdf/2604.08782) — **72% token reduction on 10-turn dialogues** with preserved or improved accuracy. LLM4S `ContextWindowConfig` is the production-grade open-source equivalent — [link](https://llm4s.org/guide/context-window-pruning.html) |

(Speculative decoding / draft-model parallelism is excluded: it is a *server-side* technique controlled by the model provider, not by a client-side proxy in front of an Anthropic-hosted API. Out of scope for this lens.)

---

## 2. Rubric — score each through the lens

Four measures, scored **0–5**, lens *"save tokens without breaking quality on Anthropic-routed agent traffic"*:

- **Cost-saving** — how much $ does this save on the kind of traffic Amplified Partners runs? Higher = more saving.
- **Friction** — how disruptive is this for agent code, prompts, response handling? **Lower = better.**
- **Complexity** — how much new infrastructure / new code does this need? **Lower = better.**
- **Outcome reliability** — how confident am I that the saving is real and the quality holds across the long tail? Higher = more confidence.

| # | Technique | Cost ↑ | Friction ↓ | Complexity ↓ | Reliability ↑ | Net (Cost+Reliability − Friction − Complexity) |
|---|-----------|:------:|:----------:|:------------:|:-------------:|:----------------------------------------------:|
| 1 | Model cascading | 4 | 1 | 2 | 4 | **+5** |
| 2 | Prompt caching | 5 | 1 | 1 | 5 | **+8** |
| 3 | Semantic caching | 3 | 2 | 3 | 3 | **+1** |
| 4 | Server-side compaction | 3 | 1 | 1 | 4 | **+5** |
| 5 | Batch API | 5 | 3 | 2 | 5 | **+5** |
| 6 | MCP / tool compression | 5 | 2 | 3 | 4 | **+4** |
| 7 | Schema-constrained output | 3 | 1 | 1 | 4 | **+5** |
| 8 | Local-first routing | 4 | 3 | 3 | 3 | **+1** |
| 9 | Chain of Draft | 3 | 1 | 1 | 3 | **+4** |
| 10 | Mid-session condensation | 3 | 3 | 4 | 3 | **−1** |

**Read:** Prompt caching (already shipped) is the cleanest single ingredient. Standalone, model cascading / Batch API / schema-constrained output / compaction all clear `+5` net. Mid-session client-side condensation is the weakest standalone — it's mostly subsumed by Anthropic's server-side compaction and is high-friction to keep correct.

But **the standalone scores are not the point.** The pudding is in the combinations.

---

## 3. PUDDING 2026 labels (`WHAT.HOW.SCALE.TIME`)

Per the canonical taxonomy in `90_archive/specifications/mac-drop-2026-04/pudding-taxonomy-synthesis.md` § 2.

- **WHAT (7):** P=Process, I=Information, R=Relation, E=Entity, S=State, C=Constraint, M=Meta
- **HOW (7):** `=`Stable, `+`Amplifying, `-`Dampening, `>`Tipping, `~`Oscillating, `!`Disrupting, `?`Emerging
- **SCALE (7):** 0=Scale-free, 1=Singular, 2=Pair, 3=Small group, 4=Network, 5=System, 6=Universal
- **TIME (6):** i=Instant, m=Medium (days–weeks), l=Long (months–years), v=Variable, p=Permanent, ∞=Timeless

Apply the 4-step method (read the technique, strip the domain, ask what TYPE / how it BEHAVES / how WIDE / how LONG):

| # | Technique | WHAT | HOW | SCALE | TIME | Label |
|---|-----------|:----:|:---:|:-----:|:----:|:-----:|
| 1 | Model cascading | P (process — routing decision) | > (tipping — regex threshold fires) | 1 (singular — one call) | i (instant — sub-ms decision) | **`P.>.1.i`** |
| 2 | Prompt caching | I (information — cached prefix is data) | = (stable — prefix doesn't change) | 1 (singular — per request, but reused across the session) | m (medium — 5min default, 1h max TTL) | **`I.=.1.m`** |
| 3 | Semantic caching | R (relation — bridges current query to a past response) | = (stable — cached response is fixed) | 4 (network — shared across all agents on `amplified-net`) | m (medium — 24h TTL) | **`R.=.4.m`** |
| 4 | Server-side compaction | P (process — auto-summarisation) | > (tipping — fires at token threshold) | 1 (singular — one session) | m (medium — operates over session lifetime) | **`P.>.1.m`** |
| 5 | Batch API | P (process — async submission/poll) | = (stable — deterministic 50% off) | 5 (system — full batched run) | l (long — async up to 24h) | **`P.=.5.l`** |
| 6 | MCP / tool compression | I (information — compressed schema is data) | − (dampening — shrinks tool tokens) | 4 (network — applies across the agent's full tool set) | p (permanent — once configured, persists) | **`I.-.4.p`** |
| 7 | Schema-constrained output | C (constraint — output must match a schema) | = (stable — deterministic) | 1 (singular — per call) | i (instant — applies once per call) | **`C.=.1.i`** |
| 8 | Local-first routing | P (process — routing decision) | > (tipping — confidence threshold) | 1 (singular — one call) | i (instant) | **`P.>.1.i`** |
| 9 | Chain of Draft | C (constraint — output style rule) | − (dampening — shrinks reasoning tokens) | 1 (singular — per call) | i (instant) | **`C.-.1.i`** |
| 10 | Mid-session condensation | P (process — condenser agent) | − (dampening — reduces history size) | 1 (singular — one session) | m (medium — operates mid-session) | **`P.-.1.m`** |

Labels are applied **before** thinking about which combinations should exist. The bridges in § 4 emerge from the labels, not from looking for puddings I want to find.

---

## 4. Bridge-finding via label matching

The canonical methodology (per pudding-taxonomy-synthesis.md § 2 — "How to apply labels", step 7): *"Look for other concepts with identical or near-identical labels across different domains — these are highest-value pudding candidates."*

### 4.1 Identical 4/4 matches (p < 0.001)

| Bridge | Techniques | Label |
|--------|-----------|:-----:|
| **B1** | Model cascading **=** Local-first routing | `P.>.1.i` |

One identical match across the 10 techniques. Both are *process, tipping, singular, instant* — different upstream targets but **structurally equivalent routing decisions**. The "route to cheaper" logic is the same shape; only the cheap target differs (Haiku vs. Ollama). **The pudding is to stack them as a two-tier cascade with the cheap tier being free local inference.**

### 4.2 3/4 matches (p < 0.01)

| Bridge | Techniques | Shared dims |
|--------|-----------|:-----------:|
| **B2** | Prompt caching `I.=.1.m` × MCP compression `I.-.4.p` | WHAT (I), TIME proximity (both persist across calls) |
| **B3** | Schema-constrained output `C.=.1.i` × Chain of Draft `C.-.1.i` | WHAT (C), SCALE (1), TIME (i) — three of four |
| **B4** | Server-side compaction `P.>.1.m` × Mid-session condensation `P.-.1.m` | WHAT (P), SCALE (1), TIME (m) |
| **B5** | Cascading `P.>.1.i` × Server-side compaction `P.>.1.m` | WHAT (P), HOW (>), SCALE (1) |
| **B6** | Cascading `P.>.1.i` × Batch API `P.=.5.l` | WHAT (P) only — but **complementary on TIME**: cascading decides which model in real time, Batch API defers eligible-for-Haiku calls to async at 50% off |
| **B7** | Prompt caching `I.=.1.m` × Semantic caching `R.=.4.m` | HOW (=), TIME (m) — two stable cache layers at different granularity |

### 4.3 What the bridges tell me

- **B1 is the highest-signal bridge** — only identical 4/4 in the set. Stack the routing tiers.
- **B2 is the most under-exploited bridge** — caching multiplies in value when the cached content is small (compressed) and stable (compression is permanent). Both vendors support it natively.
- **B6 is the highest-absolute-saving bridge** — cascading is *real-time* (`TIME=i`), Batch is *async* (`TIME=l`); the dimensions don't conflict, they compose. A Haiku-eligible *and* async-tolerant call gets routed to Haiku **and** batched, multiplying ~67% (Haiku vs Sonnet) × 50% (batch discount) = **~83% saving** on that call vs. real-time Sonnet.
- **B3 expands the routable surface** — schema-constrained output makes Haiku reliable on tasks currently kept on Sonnet for output-shape reasons. CoD on the calls that genuinely need Sonnet cuts their output cost. Pure prompt-engineering pudding, no infrastructure.
- **B4 is a substitution, not a synergy** — Anthropic's server-side compaction subsumes the client-side condensation use case for Anthropic traffic. Worth noting; not worth building both.
- **B5 / B7 are weak** — different scales / different tiers, additive at best.

---

## 5. Re-score the combinations

Same rubric, applied to the four meaningful puddings (B1, B2, B3, B6). The test per the methodology: *does the combination produce something neither ingredient could alone?*

| Pudding | Cost ↑ | Friction ↓ | Complexity ↓ | Reliability ↑ | Net | "1+1=3"? |
|---------|:------:|:----------:|:------------:|:-------------:|:---:|:--------:|
| **B6 — Cascade × Batch API** | 5 (multiplicative ~83% on eligible calls) | 3 (async only — agents must handle a poll handle) | 3 (proxy buffers, polls, returns when ready) | 5 (Anthropic-deterministic discount) | **+4** | **YES** — neither alone gives ~83%. Cascade gives ~67% real-time. Batch alone gives 50% (and only on async). Together: ~83% on the union. |
| **B2 — Prompt caching × MCP compression** | 4 (one-time 70-97% on tools, recurring 90% via cache hits on the small compressed prefix) | 1 (drop-in mcp-compressor proxy + `cache_control: ephemeral` header) | 2 (one new container in front of the agent's MCP server) | 5 (both vendor-supported) | **+6** | **YES** — compression alone is one-time; caching alone is more expensive when the cached content is large. The pudding is that *compressing the thing you cache* makes the cache effectively free to fill and 10× cheaper to read for every call after the first. |
| **B3 — Cascade × Schema × CoD** | 4 (more prompts route to Haiku because output is reliable; kept-on-Sonnet calls cost less because reasoning tokens drop ~92%) | 2 (per-agent prompt edits, no infra) | 1 (no infrastructure at all) | 3 (CoD accuracy on Amplified's long-tail prompts unverified — needs per-agent A/B) | **+4** | **PARTIAL** — schema-constrained alone tightens output; CoD alone shortens reasoning. The pudding is that schema-constrained *opens up the routable surface for cascading*, multiplying cascading's existing benefit. CoD is independent extra credit. |
| **B1 — Cascade × Local-first** | 4 (Ollama is free; large fraction of short-factual prompts may be Ollama-eligible) | 3 (Ollama latency check + fallback path; agents see longer p99) | 3 (3-tier orchestration: cache → local → cloud) | 3 (Ollama quality vs Haiku on Amplified's actual prompts is **unknown**) | **+1** | **CONDITIONALLY** — only a pudding if Ollama quality clears the bar on the prompts we care about. Needs a measurement pass first. |

**Scoring math note + degeneracy finding** (per `pudding-taxonomy-synthesis.md` § 6 Formula 1 *`Recipe Score = (Shared Dimensions × 2) + Unique_A + Unique_B`*; algebraic equivalent `|intersection| + |union|` summarised in § 10 line 673):

For any pair of **fixed 4-dimension PUDDING 2026 labels**, the simple Recipe Score is **constant**:

`(2 × s) + (4 − s) + (4 − s) = 2s + 8 − 2s = 8` for every value of `s ∈ {0..4}`.

This means the simple formula yields **score = 8** for every bridge in this set — including B1 (4/4 identical), B6 (1/4 shared), B2 (~2/4), B3 (3/4):

- B1 — shared 4, unique 0+0 = **score 8**
- B2 — shared 2 (WHAT + HOW-proximity), unique 2+2 = **score 8**
- B3 — shared 3 (WHAT, SCALE, TIME), unique 1+1 = **score 8**
- B6 — shared 1 (WHAT), unique 3+3 = **score 8**

This is a **methodology finding, not a scoring bug**: Formula 1 (`|intersection| + |union|`) was originally defined for the **v1 multi-dimension semantic-dimensions schema** — 3–7 dimensions per document, drawn from the 24-dimension B-Term ontology in `pudding-taxonomy-synthesis.md` § 3 (line 153) — where `|intersection|` and `|union|` genuinely vary. The PUDDING 2026 fixed 4-character label collapses that variability. Caught by Devin Review on this PR; flagged here as a candidate update to the canonical taxonomy spec — either (a) drop Formula 1 from the PUDDING 2026 chapter and rely only on Jaccard / Formula 2, or (b) refine Formula 1 to weight the *positions* of shared dimensions (e.g., shared HOW counts more than shared TIME) so the score is no longer constant.

**For this pudding pass, the differentiating signals are:**

- **Jaccard slot match** (canonical confidence band per § 10): B1 = 1.0 (PROVEN); B3 = 0.75 (HIGH); B2 ≈ 0.5 (MEDIUM); B6 = 0.25 (LOW).
- **Rubric net score** in the table above: B2 +6, B6 +4, B3 +4, B1 +1.
- **"1+1=3?" qualitative test**: B2 YES, B6 YES, B3 PARTIAL, B1 CONDITIONAL.

The mathematical floor of "build immediately" per Formula 2 is **≥ 18** (`(domain_distance × pattern_alignment) + gap_complement + tension_bonus`). None of these clear that floor — but this is a **single-domain** prospecting pass (token economics on a hosted API), not the cross-domain LBD use case Formula 2 was tuned for. For single-domain prospecting, the **rubric net + Jaccard band + 1+1=3 test** are the load-bearing signals, not Formula 1.

---

## 6. Recommendations — top 3 to build (in order)

Honest sequencing: lowest friction first, biggest absolute saving last.

### #1 — Build **B2** (Prompt caching × MCP compression). Effort: 1–2 days.

**What:** Drop `mcp-compressor` (Atlassian Labs, open-source) in front of each agent's MCP server. Compress tool schemas to **High** level (88% reduction; tool names + parameter names only, descriptions stripped). Add `cache_control: { type: ephemeral }` on the system prompt + tools block in every Anthropic call from the proxy.

**Why first:** Lowest friction (drop-in container + one header). Highest reliability (both vendors support it natively). Recurring saving on every agent call, not just an opportunistic subset. The CRM has 17 MCP tools; the PII Gateway has 4. A rough estimate from the Atlassian benchmark (94 tools at GitHub-MCP scale → 88% reduction) suggests Amplified's MCP setup is loading on the order of 5–15k tokens of tool definitions per call today; cutting to ~500–2,000 tokens × 90% cache discount on every call after the first = **10–30% saving on agents that use MCP tools heavily**, plus latency improvement.

**Risk:** Compression at "High" level can cause Haiku to misread a tool name on the long tail. Test on the CRM agent first. If accuracy drops, step down to "Medium" level (81% reduction, first sentence of description preserved).

**Status to set in Linear:** new ticket `AMP-77` (or next free); P2; depends on AMP-28 close-out.

### #2 — Build **B3** (Cascade × Schema-constrained × Chain of Draft). Effort: 1 day per high-traffic agent.

**What:** Two prompt-engineering changes per agent:
1. Where the agent's output is consumed by code (every CRM endpoint, marketing-engine drafts, etc.): force a JSON schema via Anthropic tool-use contract. Update the agent's prompt and validator. The proxy doesn't change.
2. Where the agent does multi-step reasoning: add the CoD prefix ("for each step, write only the minimal necessary text, ~5 words; skip explanations") to the system prompt. **Skip this on agents with reasoning-heavy long-form tasks** until A/B'd.

**Why second:** Zero infrastructure. The schema-constrained output is what *unlocks* more cascading — it lets Haiku take over jobs currently kept on Sonnet because the format was unreliable. Estimated **15–25% additional saving on agents whose Sonnet-routed prompts can be re-routed to Haiku** under a strict output schema.

**Risk:** CoD accuracy on Amplified's long-tail prompts is unverified. Treat each agent as a separate A/B: 50 prompts pre-CoD vs 50 post-CoD, measure routing accuracy (already 100% on the cost-tools test set) plus answer correctness against ground truth.

**Status to set in Linear:** new ticket `AMP-78` (or next free); P3; per-agent rollout.

### #3 — Build **B6** (Cascade × Batch API). Effort: 3–4 days for the proxy work + 1 day per batched agent.

**What:** Add a `X-Batch-Tolerable: true` request header (or a per-agent config flag in the proxy) signalling that this call can wait up to 24h. The proxy buffers eligible calls, submits them via Anthropic's [Message Batches API](https://docs.anthropic.com/en/docs/build-with-claude/message-batches) when buffer hits N=100 or T=15min, and returns a poll handle. Agent SDK polls and resolves when results are ready.

**Why last:** Highest absolute saving (~83% on eligible calls vs real-time Sonnet) but only on async-tolerant traffic. Need to identify which jobs are async-tolerant first — Devon's scheduled sessions, vault-ingestion pipeline, marketing content draft generation overnight, kaizen-optimizer summaries. Real-time agents (CRM voice, interactive Telegram bot) cannot use this and should not be wired through.

**Risk:** Async response handling is the friction. Some agents may not be willing to wait 24h. Mitigation: tunable timeout per request — if the batch hasn't returned by T_max, the proxy falls back to a real-time call (no saving on that one, but no failure).

**Status to set in Linear:** new ticket `AMP-79` (or next free); P3; depends on identifying eligible-for-async agents.

### Held / not recommended for Phase 2

- **B1 (Cascade × Local-first / Ollama)** — only worth building if Ollama quality on Amplified's actual prompts holds. Run a measurement pass first (50 short-factual + 50 short-classification prompts, Ollama vs Haiku, score against ground truth and against latency). If Ollama lands within 10% of Haiku on accuracy at meaningfully better cost (free), revisit. **Ticket: open as `AMP-80` for the measurement pass; the build only follows the data.**
- **Mid-session condensation** — Anthropic's server-side compaction subsumes the use case for Anthropic traffic. Revisit only if/when we extend the proxy to non-Anthropic providers.
- **Standalone semantic cache scaling** — the cache is in production; tuning the similarity threshold and TTL is a Kaizen task, not a pudding.

---

## 7. Aggregate effect (back-of-envelope, not committed)

Hypothetical spend reduction if all three puddings ship and ~50% of Anthropic traffic is Haiku-eligible after schema-constrained output expands the surface:

- Phase 1 (current, cascading + caches + compaction): ~30% saving on Anthropic traffic (verified on test set; real-world TBD)
- Phase 2.B2 (MCP compression × prompt cache): additional 10–30% on MCP-using agents
- Phase 2.B3 (schema + CoD): additional 15–25% on the agents whose Sonnet calls can re-route
- Phase 2.B6 (batch on async-eligible): additional 50% on the async subset of Haiku-eligible traffic

These compound multiplicatively, not additively. Realistic upper-bound on Anthropic spend reduction across the whole agent estate after all three: **50–70%** (depends critically on how much traffic is async-tolerant and how reliable schema-constrained output is on the long tail). **Worth measuring after each pudding ships, not pre-committing to the number.**

---

## 8. What this document does *not* do

- It does **not** authorise any code changes. Phase 2 build tickets get filed only after Ewan's review of this document.
- It does **not** modify the cost-tools artefact (`Amplified-Partners/cost-tools`). The proxy is unchanged.
- It does **not** index any new authority files. If any of the three puddings get built and ship, that's a separate PR with `INFRASTRUCTURE.md`, `SYSTEMS-AND-API-REGISTER.md`, and `MANIFEST.md` updates per the AMP-28 pattern.
- It does **not** wire any agent canaries. That is the held-A track and waits on Ewan.

This is a *research-only* candidate document under `03_shadow/research/`. Promotion to `01_truth/schemas/architecture/` happens only by review per `00_authority/PROMOTION_GATE.md`.

---

## 9. Sources (load-bearing, one per technique)

Inline links above. Consolidated:

- RouteLLM — Ong et al., 2024 — <https://arxiv.org/abs/2406.18665> · <https://lmsys.org/blog/2024-07-01-routellm/>
- Anthropic Prompt Caching — <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- Anthropic Pricing — <https://docs.anthropic.com/en/docs/about-claude/pricing>
- LiteLLM Qdrant Semantic Cache — <https://github.com/BerriAI/litellm/blob/d251238b/litellm/caching/qdrant_semantic_cache.py>
- Antigravity Lab semantic-cache production guide — <https://antigravitylab.net/en/articles/app-dev/antigravity-llm-semantic-cache-production-guide>
- Anthropic Compaction — <https://docs.anthropic.com/en/docs/build-with-claude/compaction>
- Anthropic Message Batches API — <https://docs.anthropic.com/en/docs/build-with-claude/message-batches> · <https://anthropic.com/news/message-batches-api>
- Atlassian `mcp-compressor` — <https://www.atlassian.com/blog/developer/mcp-compression-preventing-tool-bloat-in-ai-agents>
- Anthropic code-execution MCP approach — <https://brightbean.xyz/blog/code-execution-mcp-efficient-ai-agents/>
- StackOne MCP token-optimization benchmark — <https://www.stackone.com/blog/mcp-token-optimization/>
- Schema-constrained output (JSON mode vs function calling) — <https://www.kalviumlabs.ai/blog/structured-output-from-llms-json-mode-function-calling/>
- Chain of Draft / Token Optimize Dev — <https://www.tokenoptimize.dev/guides/token-efficient-prompting-patterns>
- MT-OSC (mid-session condensation) — <https://arxiv.org/pdf/2604.08782>
- LLM4S `ContextWindowConfig` — <https://llm4s.org/guide/context-window-pruning.html>

---

## 10. Attribution (per Radical Attribution)

- **The Pudding Technique** — Don R. Swanson, *Fish oil, Raynaud's syndrome, and undiscovered public knowledge* (1986). Adapted by Ewan Bramley + Claude (Anthropic) for cross-domain business knowledge synthesis, 2026.
- **PUDDING 2026 taxonomy (`WHAT.HOW.SCALE.TIME`, 7×7×7×6 = 2,058 labels)** — defined in `clean-build/90_archive/specifications/mac-drop-2026-04/pudding-taxonomy-synthesis.md` § 2.
- **Original `cost-tools/token_proxy.py`** — Claude (Anthropic Cowork), March 2026.
- **This pudding-pass on the token-optimisation domain** — Devon-6ca5 | Devin (Cognition AI) | 2026-05-04 | session `devin-6ca57553eefe4806b613070325964703`.

---

Signed-by: **Devon-6ca5 | Devin (Cognition AI) | 2026-05-04 | session `devin-6ca57553eefe4806b613070325964703`**
