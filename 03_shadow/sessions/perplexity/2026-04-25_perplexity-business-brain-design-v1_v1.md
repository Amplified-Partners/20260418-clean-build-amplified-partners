---
title: "Can you do it or at least packaged up as an MD file?"
id: "perplexity-business-brain-design-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "perplexity-session"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Can you do it or at least packaged up as an MD file?

Here it is, fully packaged as a `.md` file – you can copy everything below into a file named, for example, `Business Brain Appliance – Design Summary.md`:

***

# Business Brain Appliance – Design Summary

## Purpose

Create a **Business Brain Appliance**: a serious, on‑prem box that plugs into an SMB’s IT, mines data continuously, and serves fast, framework‑driven AI assistance (coaching, SOPs, telephony) using a hybrid local + cloud design.

***

## Hardware decisions

### Target use

- Always‑on “head” for:
    - Local LLM (coaching, SOPs, assistants).
    - Vector database (Qdrant) and graph database (Neo4j).
    - Fast, conversational queries (telephony, chat, SOP lookup).
    - Continuous ingestion and background mining.


### Chosen form factor

- **Custom high‑end mini PC**, not a gamer tower.
- Reasons:
    - Looks and feels like serious business kit.
    - Quiet, 24/7‑rated, compact.
    - Easy to standardise and replicate as a demo fleet and reference design.[^1][^2][^3]


### Baseline spec (v1 Appliance)

- **CPU**: Intel i7 (13th gen‑class) or AMD Ryzen 7 (8–12 cores).
    - Enough parallelism for LLM + Qdrant + Neo4j + integrations.[^4][^5]
- **RAM**: **64 GB**.
    - Neo4j cache + heap (graph).[^6][^7]
    - Qdrant hot vectors in memory.[^8]
    - Quantised 7–9B LLM + runtime + OS.[^9][^10]
- **Storage**: **2 TB NVMe SSD** (PCIe 4).
    - Fast store for Qdrant, Neo4j, curated Business Brain, logs.[^7][^8]
- **GPU**: none required initially (integrated is fine).
    - Use small, efficient models; optional later “Pro+” with RTX 4060‑class GPU.[^11][^9]
- **Networking/Power**:
    - Dual 1 Gbps NICs, optional Wi‑Fi backup.
    - Small UPS for clean shutdown and resilience.

**Why this spec:** big enough for serious multi‑service AI workloads, small enough to be affordable (~£1.1k–£1.3k per unit in UK custom builds).[^2][^1]

***

## Architecture decisions

### Hot vs cold tiers

- **Hot tier (fast, local)** – lives on this box (NVMe/RAM):
    - Local LLM (7–9B, quantised).
    - Qdrant “hot” collections (framework + curated Business Brain + recent data).[^8]
    - Neo4j “hot” graph (current org, processes, issues).[^6][^7]
    - Telephony/chat/SOP/coaching endpoints.
- **Cold tier (slow, batch)** – lives on NAS and/or cloud:
    - Raw logs, emails, recordings, long‑term history.
    - Old embeddings and graph segments.
    - Heavy analytics, deep mining, cross‑client learning.[^12][^13]

**Why:** fast conversational work stays small, local and snappy; long‑term growth and heavy jobs don’t crush the appliance.

### Hybrid local + cloud

- **Local box = security and performance boundary**
    - Holds raw personal/operational data.
    - Runs tokenisation and keeps keys/mappings.
    - Runs all real‑time conversational workloads.
- **Cloud = muscle and long‑term memory**
    - Stores pseudonymised/tokenised data and aggregates.[^14][^15]
    - Runs heavy batch jobs and global pattern learning, when permitted.[^13][^16]

**Why:** cloud is effectively limitless, but sensitive work happens on‑prem; this keeps both performance and risk where you want them.

***

## Data \& privacy decisions (at a high level)

- **Tokenisation / pseudonymisation**
    - Before data goes to cloud, identifiers are replaced with tokens (vaulted or vaultless tokenisation).[^15][^17][^14]
    - Mapping or keys stay only on the appliance, in encrypted storage.
    - Cloud sees patterns, not identities; re‑identification only happens back on‑site.

**Why:** lets you scale and learn in the cloud while aligning with strong GDPR pseudonymisation practices.[^18][^19][^20]

***

## Model decisions

### Do we need an LLM?

Yes.

- Qdrant + Neo4j:
    - Find the right chunks.
    - Represent structure and relationships.[^21][^7][^6][^8]
- LLM:
    - Turns retrieved context into answers, SOPs, coaching dialogue.
    - Follows your framework and tone.
    - Decides when deeper retrieval or background jobs are needed.[^22][^21]

**Pattern:** RAG (Retrieval‑Augmented Generation) – recommended when you have strong internal knowledge bases.[^21][^22]

### Size and family

- **Target size**: **7–9B parameters, quantised**, tuned for:
    - Good instruction following.
    - Solid reasoning over structured/business info.
    - Fast inference on CPU / modest hardware.[^23][^9][^11]
- **Vendor/jurisdiction preference**:
    - Use **non‑Chinese, widely adopted open‑source models** (e.g. Mistral/Ministral, LLaMA‑family instruct) to avoid perception and jurisdiction risk.[^24][^25][^11][^18][^23]
    - Architect the model behind an API so it’s swappable as the ecosystem evolves.[^26][^22]

**Why:** you get good quality and speed, keep security/sales conversations simple, and avoid locking into one model family.

***

## Behavioural / performance strategy

- **Prioritise “in‑conversation” tasks**
    - Telephony, chat, SOP lookup, live coaching get priority on CPU/IO.
    - Background mining and re‑indexing run at lower priority and can be paused.
- **Keep the curated Business Brain compact**
    - Only high‑signal, framework‑aligned content lives in hot vector + graph stores.
    - Raw detail is summarised and pushed to cold storage over time.
- **Measure and forecast growth**
    - Log daily ingestion volume, vector counts, graph size.
    - Use simple forecasting to decide when to:
        - Expand local storage.
        - Offload more to cloud archives.[^27][^8]

**Why:** you maintain responsiveness at the “front door” while allowing total data volume to grow massively in the background.

***

## Commercial / deployment stance

- Standardise on this **one appliance spec** as:
    - Your demo fleet hardware.
    - The reference design you ask clients to buy or rent if they continue.
- Sales narrative:
    - “This is your **Business Brain**, running on enterprise‑grade hardware we can show you and you can own.”
    - “The sensitive thinking happens here; the cloud is just extra muscle and long‑term memory, under strict controls.”

<div align="center">⁂</div>

[^1]: https://inside-tech.co.uk/mini-pcs/

[^2]: https://inside-tech.co.uk/mini-pcs/custom-mini-pcs/

[^3]: https://2ndboot.com/mini-pc-buying-guide-2026/

[^4]: https://www.techradar.com/best/mini-pcs

[^5]: https://www.lenovo.com/gb/en/p/desktops/thinkcentre/m-series-tiny/11tc1mtm7g2/11tc1mtm7g2?displayrulevalidation=false\&bvstate=pg%3A2%2Fct%3Ar

[^6]: https://houseofgraphs.com/blog/neo4j-scalability/

[^7]: https://graphable.ai/blog/neo4j-performance/

[^8]: https://qdrant.tech/documentation/guides/capacity-planning/

[^9]: https://www.siliconflow.com/articles/en/best-small-llms-for-edge-devices

[^10]: https://localllm.in/blog/how-to-run-local-llm-guide-2025

[^11]: https://localllm.in/blog/best-local-llms-8gb-vram-2025

[^12]: https://datacentrereview.com/2025/03/navigating-the-edge-and-smb-cloud-challenge-whats-the-alternative/

[^13]: https://www.sganalytics.com/blog/7-big-data-trends-to-look-forward-by-2025/

[^14]: https://www.protecto.ai/blog/advanced-data-tokenization/

[^15]: https://www.shadecoder.com/topics/reversible-tokenization-a-comprehensive-guide-for-2025

[^16]: https://www.cloudtech.com/resources/smb-cloud-adoption-trends-impact

[^17]: https://www.bluefin.com/data-security/tokenization/

[^18]: https://secureprivacy.ai/blog/privacy-by-design-gdpr-2025

[^19]: https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf

[^20]: https://www.hunton.com/insights/publications/edpb-advises-on-pseudonymisation-for-gdpr-compliance

[^21]: https://www.oxfordsemantic.tech/blog/what-is-knowledge-based-rag-and-why-do-enterprises-need-it

[^22]: https://kanerika.com/blogs/rag-vs-llm/

[^23]: https://apidog.com/blog/small-local-llm/

[^24]: https://www.rightdigitalsolutions.com/it-decision-maker-priorities-what-smbs-must-focus-on-in-2025/

[^25]: https://censinet.com/perspectives/pseudonymization-gdpr-privacy-standards

[^26]: https://pinggy.io/blog/top_5_local_llm_tools_and_models_2025/

[^27]: https://superagi.com/ai-powered-sales-forecasting-in-2025-predictive-analytics-for-accurate-revenue-projections/

