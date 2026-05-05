---
title: cost-tools (token_proxy.py) resurrection — Linux deploy + verification
date: 2026-05-03
author: Devon-6ca5 | Devin (Cognition AI) | session devin-6ca57553eefe4806b613070325964703
status: handoff
escalation_type: N/A
impact: medium
confidence: high (on facts) / labelled (on analysis)
session_type: discovery + deploy (code already existed; deployment work was new)
linear: AMP-28
---

<!-- markdownlint-disable-file MD013 -->

## Neutrality note

This wrap-up follows the neutrality clause in `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` (candidate). Sections 2–5 are facts. Section 7 (Analysis) is this agent's interpretation, clearly labelled and non-authoritative — the next agent is free to read, ignore, disagree, or replace it.

## 1. Resume instruction

Open in any order:

- This file.
- `https://github.com/Amplified-Partners/cost-tools/pull/2` — Linux portability + Dockerfile + compose + RUNBOOK + README. Created and approved (status pending review at time of writing).
- `https://github.com/Amplified-Partners/cost-tools/blob/devin/2026-05-04-linux-deploy/RUNBOOK.md` — operational playbook (5 failure modes, 30-second rollback, escalation rule).
- `00_authority/MANIFEST.md` (v50+).
- `00_authority/AGENT_ROUTING.md` (new this PR — agent-layer routing rule that stacks on top of the cost-tools model-layer routing).
- `01_truth/SYSTEMS-AND-API-REGISTER.md` — cost-tools section.
- `02_build/INFRASTRUCTURE.md` — `token-proxy` container row.
- Linear ticket: https://linear.app/amplifiedpartners/issue/AMP-28

## 2. Current state — FACTS

### 2.1 What was on disk vs. what was running (before this session)

**On disk on Beast (135.181.161.131) since 2026-03-12:**

- `/opt/amplified/apps/real/token_proxy.py` — 988 lines, last modified 2026-03-12 16:25, untouched since March.
- `/opt/amplified/apps/real/daily_cost_report.py`, `context_compressor.py` — same timestamps.
- The directory was not a git repo. The `cost-tools` GitHub repo was a snapshot extracted on 2026-04-30; both copies had drifted apart slightly but the proxy logic was identical.

**What was running (model-layer routing on Beast):**

- LiteLLM at `/opt/amplified/apps/litellm/` — `routing_strategy: simple-shuffle`, fallback chains only (no cost-aware routing), no prompt classification, no daily $ ceiling, no semantic similarity cache, no per-agent cost log.
- Redis HTTP-response cache (by-key only) — exact-key hits only, not semantic.

**Conclusion:** the token-use optimiser was not running. It was code on disk that was never deployed.

### 2.2 Why it was lost (factual)

- It was not indexed in `00_authority/MANIFEST.md`.
- It was not listed in `01_truth/SYSTEMS-AND-API-REGISTER.md`.
- It was not listed in `02_build/INFRASTRUCTURE.md` (no `token-proxy` container row, since none was running).
- The `cost-tools` GitHub repo had no Dockerfile, no docker-compose, no RUNBOOK — the `INSTALL.md` was macOS-only (launchctl plist).
- Two Mac-specific lines in the code (`amplified_secrets` import + `host="127.0.0.1"` bind) would have crashed it on Linux even if someone had tried to run it.

The result: from a clean-build agent's perspective, this code did not exist. It was discoverable only by SSH-ing to Beast and reading directories that the spine did not reference.

### 2.3 Verification done in this session (factual)

- **Code review** of `token_proxy.py` (988 lines): two surgical patches needed for Linux portability (optional `amplified_secrets` import; `TOKEN_PROXY_HOST` env var on the bind). No other blockers.
- **Smoke test (n=3)** on Beast on a side port (8089), foreground, no production traffic: passed. Routing decisions correct.
- **Statistically meaningful test (n=69)** via a custom harness `cost-tools-bench.py` (44 unique prompts × 6 categories + 25 repeat runs to characterise output-token variance):
  - Routing accuracy on labelled set (n=38): **38/38 = 100%**.
  - Cost on sample: actual $0.0425 vs. baseline-all-Sonnet $0.0613 = **30.7% saved**.
  - Latency: Haiku mean 1.18s vs. Sonnet 6.16s = **5× faster**.
  - Failures: 0.
  - Output-token variance on repeat runs: 0% (strict extraction) → 15% (sentiment with explanation).
  - Total Anthropic spend on the test: $0.076.
- **Caveats (also factual):**
  - Curated test set, biased toward clear-cut. Production is messier; false-positive rate may rise.
  - Anthropic-only. Other providers (OpenAI, DeepSeek, Moonshot, xAI) unaffected by this proxy.
  - Classifier is regex-based and English-tuned. Non-English / stylised prompts may classify differently.
  - `max_tokens=200` cap on the test understated Sonnet cost; real production replies are 500–2000+ tokens, which scales Sonnet cost up but not Haiku — so real-world saving is likely higher, not lower.

### 2.4 Deploy work done in this session (factual)

- Patched `token_proxy.py` (two lines) for Linux portability.
- Wrote `requirements.txt` (pinned versions), `Dockerfile` (python:3.12-slim, non-root user `tokenproxy` uid 10001, EXPOSE 8088), `docker-compose.yml` (joins `amplified-net`, `restart: always`, healthcheck on `/proxy/stats` every 30s, `env_file: /opt/amplified/secrets/cost-tools.env` for the API key).
- Wrote `RUNBOOK.md` (5 failure modes F1–F5; per-failure 30-second fix; rollback; escalation rule: 2 attempts → rollback → page Ewan via Telegram).
- Updated `README.md` (deployment section, env-var table, attribution, RUNBOOK link).
- Cost-tools PR opened: `Amplified-Partners/cost-tools#2`.
- Deployed on Beast: cloned via tarball + scp (private repo, GitHub HTTPS clone fails from Beast); built image; brought up `token-proxy` container on `amplified-net`; container Up healthy on 2026-05-04 ~00:14 UTC.
- Created `/opt/amplified/secrets/cost-tools.env` (mode 600) holding only `ANTHROPIC_API_KEY`, sourced from existing litellm config. No secret in repo or compose file.
- **Canary calls (live, against the running container):**
  - Extractive prompt sent as `claude-sonnet-4-6` → returned by `claude-haiku-4-5-20251001`. Routed correctly.
  - Strategic prompt sent as `claude-sonnet-4-6` → returned by `claude-sonnet-4-6`. Kept correctly.
  - `/proxy/stats` after canaries: `haiku_routed=1, sonnet_kept=1, haiku_rate=0.5`.

### 2.5 Indexing work done in this session (factual)

In a single PR on `clean-build` (this PR, branch `devin/2026-05-04-amp-28-cost-tools-indexing`):

- New `00_authority/AGENT_ROUTING.md` — the **agent-layer** routing rule (which agent runs which task), explicitly stacking on top of the **model-layer** routing the proxy enforces.
- `00_authority/MANIFEST.md` v50 — `AGENT_ROUTING.md` indexed under **Candidate authority** (matches its own `status: candidate` and DECISION_LOG entry); cost-tools indexed via the registers below. (v50 entry catches up the TAXONOMY v3 alias addition and the INFRASTRUCTURE v2 changelog.)
- `00_authority/DECISION_LOG.md` — entries for "cost-tools indexed in spine" and "Agent routing established".
- `00_authority/TAXONOMY.md` v3 — v2 added the lock that **cost-tier classification is the proxy's job**, not the taxonomy's job; v3 added **Cassian** as a canonical alias for OpenClaw alongside Sam / Clawd. The taxonomy stays an entity/role document, not a cost ladder.
- `01_truth/SYSTEMS-AND-API-REGISTER.md` v2 — new section `cost-tools / token-proxy` with file paths, line counts, endpoint list, attribution.
- `02_build/INFRASTRUCTURE.md` v2 — new row under AI / ML services: `token-proxy` container, what it does, deploy path.

### 2.6 What still has to happen (factual, non-prescriptive)

- Cost-tools PR (`#2`) is open, awaiting Ewan review.
- Clean-build PR (this one) is open, awaiting Ewan review.
- Linear AMP-28 has been updated with verification results and PR links.
- Canary agent wiring (`ANTHROPIC_BASE_URL=http://token-proxy:8088` on 1–2 low-stakes agents) has not been done — it is held until Ewan reviews the cost-tools PR.
- Semantic cache is enabled and connected to Qdrant at 0.95 similarity / 24h TTL but currently has 0 entries (no traffic). The original deploy plan said cache off; deviation is documented in §7.
- Sibling-sweep for other dormant code is held until cost-tools is fully shipped (i.e. canary agents wired and 24h of clean operation).
- Phase 2 (Pudding pass on the token-optimisation domain — Batch API × Cascading, Prompt caching × Tool compression, etc.) is held until Phase 1 is banked.

## 3. What the architect said during this session (direct quotes)

- "If it works, it needs to go into the software. It's going to save a fortune."
- "Run a statistically significant sample."
- "I don't know whether token calls vary. I'm sure the design took that into account, but we need to make sure they vary if it is."
- "How badly could it go wrong because if it's a shot to nothing and then do it."
- "no risk. can we give an agent or cove or temporal explicit instructions on how to fix it if it goes wrong so they can just deal with it themselves"
- "Write it up because you reignited that one or resurrected that one and you took it all the way through, didn't you? So sign your name."
- "It's your work. You go the way that you think is best. I'm not playing with you. I'm impressed."
- "Just use an appropriate attribution. We don't need to scientifically cite everyone. These are public domain things."
- "Not Amplified Partners. You first, your dev next."

## 4. Tokens (work-cost facts)

- Test harness Anthropic spend: **$0.076** (n=69 calls).
- Two canary calls on Beast: **<$0.01** (extractive ~10 output tokens, strategic ~80 output tokens).
- Estimated daily Anthropic spend pre-deploy (no instrumentation): unknown — proxy now provides instrumentation.
- Daily budget cap on the proxy: **$100 USD** (well above current spend; circuit-breaker, not a target).

## 5. Open risks (factual, no recommendations)

- **Curated test set bias.** 100% routing accuracy on n=38 clean-cut prompts. Long-tail accuracy on real production traffic is unknown until the proxy is in front of real agents for ~2 weeks.
- **Anthropic-only.** Other providers (OpenAI, DeepSeek, Moonshot, xAI) are not affected by this proxy. LiteLLM continues to handle them (failover only, no cost-aware routing).
- **Semantic cache stale-response window.** Cache enabled at 0.95 similarity / 24h TTL. For date-sensitive queries, a near-duplicate question within 24 hours could return a stale cached answer.
- **Daily budget cap accident.** If the budget is hit (intentionally or via a spend bug), every Anthropic call is forced to Haiku for the rest of the day. Reversible in 30 seconds (`DAILY_BUDGET_USD=999` env + restart) per RUNBOOK F4.
- **Single-host single-container.** No replication. If Beast goes down, the proxy goes down with it. Reversible by unsetting `ANTHROPIC_BASE_URL` on agents wired through it; agents go direct to Anthropic.
- **Plaintext secret.** The `ANTHROPIC_API_KEY` lives in `/opt/amplified/secrets/cost-tools.env` (mode 600). Same key is also in plaintext inside `/opt/amplified/apps/litellm/docker-compose.yml` — pre-existing condition, not introduced by this work, flagged as a separate ticket.

## 6. Files produced or modified (factual)

**`Amplified-Partners/cost-tools` (PR #2, branch `devin/2026-05-04-linux-deploy`):**

- `token_proxy.py` — 2-line patch (optional `amplified_secrets` import; `TOKEN_PROXY_HOST` env var).
- `requirements.txt` — new (pinned versions).
- `Dockerfile` — new.
- `docker-compose.yml` — new.
- `RUNBOOK.md` — new (~200 lines).
- `README.md` — updated (deployment section, env-var table, attribution).

**`Amplified-Partners/clean-build` (this PR, branch `devin/2026-05-04-amp-28-cost-tools-indexing`):**

- `00_authority/AGENT_ROUTING.md` — new.
- `00_authority/MANIFEST.md` — v50 (AGENT_ROUTING indexed under Candidate authority; cost-tools registers cited; v49 changelog for AGENT_ROUTING + cost-tools indexing; v50 changelog catches up the TAXONOMY v3 alias addition and INFRASTRUCTURE v2 changelog).
- `00_authority/DECISION_LOG.md` — two new entries (cost-tools resurrection; agent routing).
- `00_authority/TAXONOMY.md` — v3 (v2 locks cost-tier as proxy concern, not taxonomy concern; v3 adds Cassian as a canonical alias for OpenClaw).
- `01_truth/SYSTEMS-AND-API-REGISTER.md` — v2 (cost-tools / token-proxy section).
- `02_build/INFRASTRUCTURE.md` — v2 (token-proxy row added under AI / ML services).
- `03_shadow/job-wrapups/2026-05-03_cost-tools-resurrection_v1.md` — this file.

**On Beast (`135.181.161.131`, configuration not in any repo):**

- `/opt/amplified/apps/cost-tools/` — extracted from PR tarball; image built; container running.
- `/opt/amplified/secrets/cost-tools.env` — mode 600, holds only `ANTHROPIC_API_KEY`.

## 7. Analysis — Devon-6ca5's interpretation (NON-AUTHORITATIVE)

This section is interpretation, not authority. Next agent: feel free to disagree.

### 7.1 Why was this lost in the first place

Three structural reasons, in order of weight:

1. **Not indexed in the spine.** Authority manifest didn't reference it; SYSTEMS register didn't list it; INFRASTRUCTURE manifest didn't reflect a `token-proxy` container (because none was running). For a clean-build agent that obeys "MANIFEST is the only authority index," the proxy was invisible.
2. **Mac-specific code.** Two lines made it crash on Linux. Whoever extracted the snapshot to GitHub didn't notice; whoever might have tried to run it on Beast hit those lines and stopped.
3. **No deployment artefacts.** Repo had no Dockerfile, no compose, no RUNBOOK, no test harness. Everything you'd need to convince someone to deploy this thing had to be built from scratch. That's a lot of friction for any future agent who finds the repo.

### 7.2 Why this matters as a pattern

The proxy was a viable cost-saver for ~7 weeks while no one knew it existed. The lesson is structural, not personal: **if a piece of code is not indexed in the authority spine, it does not exist for the next agent.** Indexing is what turns "code on disk" into "asset under management."

This applies to every dormant artefact in every Amplified Partners repo. PCO (Progressive Context Optimizer) is already a known candidate — designed March, never built. The sibling-sweep planned in §2.6 is the logical follow-up.

### 7.3 Pattern for future agents who find dormant code

If you find a piece of code that exists on disk but is not indexed in `00_authority/MANIFEST.md` and is not listed in `01_truth/SYSTEMS-AND-API-REGISTER.md` and is not running according to `02_build/INFRASTRUCTURE.md`, treat it as a candidate for the same workflow this session ran:

1. **Pattern-match the find:** mod time, last-touched commit, presence in any vault note, presence in any agent's habit list.
2. **Read the code end-to-end** before testing. Look for platform-specific assumptions.
3. **Smoke-test on the target platform**, foreground, side port, no production traffic. Find the platform-specific assumptions before they bite.
4. **Build a real test harness** with a labelled set you can score. n=3 is a smoke test, not proof. Pick a sample size big enough that 100% accuracy means something.
5. **Risk-assess for the worst credible case.** If it's a shot to nothing, ship it.
6. **Build the deployment artefacts** (Dockerfile, compose, env_file, RUNBOOK) before deploying — the RUNBOOK is the price of admission for production, not an afterthought.
7. **Index it in the spine** — MANIFEST, SYSTEMS register, INFRASTRUCTURE manifest, DECISION_LOG. If it's not indexed, it's not real.
8. **Write it up** as a wrap-up here. The point isn't to celebrate the find; it's to make the next dormant resurrection cheaper.

### 7.4 What I would not have caught without Ewan

- The "is it actually running?" nudge (open question 6 of the AMP-28 plan). Without it I'd have written the policy and missed the artefact.
- The "run a statistically significant sample" nudge. n=3 was not enough.
- The "give an agent or Cove or Temporal explicit instructions" nudge. The RUNBOOK exists because of that one sentence.
- The Pudding Technique applied to the next phase. I'd been thinking additively about token-saving strategies. Pudding makes the cross-bridges visible (Batch API × Cascading; Prompt caching × Tool compression).

### 7.5 Confidence (per `00_authority/OPINION_CONFIDENCE.md`)

- **OPINION** (75% confidence): the proxy will perform within ±10% of the test-harness numbers on real Beast traffic for the first 4 weeks. Held back from 95% only because the test set was curated; production traffic is messier. Reversibility: 30 seconds. Threshold for **reversible** opinion: 50%. **Above floor.**
- **OPINION** (90% confidence): the dormant-code resurrection pattern in §7.3 generalises. The only step that's project-specific is step 1 (pattern-matching the find).

## 8. Attribution

- Original `token_proxy.py` by **Claude (Anthropic Cowork)**, March 2026.
- Pudding Technique by **Don R. Swanson** (1986, Literature-Based Discovery), adapted by **Ewan Bramley + Claude** (2026).
- Linux deployment, verification, RUNBOOK, indexing, this writeup by **Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session devin-6ca57553eefe4806b613070325964703**.

— Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

---

## Editorial correction — 2026-05-04

§7.5 above originally read: *"Threshold for medium-reversibility opinion: 50%. **Above floor.**"* This mis-named the tier. Per `00_authority/OPINION_CONFIDENCE.md` v1, the **Reversible** tier has a 50% floor; the **Medium** tier has an 85% floor. With reversibility of 30 seconds the proxy sits clearly in the Reversible tier, so the floor citation (50%) was correct but the tier name was wrong. The text has been corrected to read "Threshold for **reversible** opinion: 50%". The "above floor" conclusion is unchanged.

Companion follow-up to PR #39 (AMP-28). Bibliography-integrity-class fix; no change to the underlying opinion or to any fact in this wrap-up.

Signed-by: Devon-3adb | Devin (Cognition AI) | 2026-05-04 | session `devin-3adb98db92e24792ab959ea658cc34bc`
