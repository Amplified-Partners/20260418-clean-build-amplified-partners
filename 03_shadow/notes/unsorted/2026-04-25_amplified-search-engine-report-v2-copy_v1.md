---
title: "Amplified Search Engine Report V2 Copy"
id: "amplified-search-engine-report-v2-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Search Engine & API Landscape**

**Complete Reference for Amplified Partners**

Every Search Engine, API, and Verification Tool --- Capabilities, Customisation, and Usefulness for the Amplified Operating System

March 2026

Prepared for Ewan Bramley

**Amplified Partners**

**Executive Summary**

This report maps the full landscape of search engines, APIs, and verification tools available to Amplified Partners\' AI operating system. The goal is simple: find the best, most cost-effective way for Amplified\'s agents to search the web, verify facts, and retrieve specialist information --- without depending on a single provider.

**Key Finding**

Brave Search is now the only commercially available independent search API in the West.[^1] Bing shut down its public API in August 2025, and Google sued SerpAPI. Every other search API either resells Google/Bing results or scrapes them. This makes Brave strategically critical as a Tier 2 fallback.

**The 5-Tier Architecture**

The recommended architecture routes queries through five tiers, from cheapest/fastest to most expensive/powerful:

-   **Tier 1 --- SearXNG:** Self-hosted meta-search on Beast. Handles 80%+ of all queries. Cost: zero.

-   **Tier 2 --- Brave Search API:** Independent web index fallback. Handles \~15% of queries. Cost: \~\$50-100/month.

-   **Tier 3 --- Specialist APIs:** Academic (OpenAlex, Semantic Scholar), people/company (Exa), news (GDELT), code (Sourcegraph). Handles \~5%.

-   **Tier 4 --- Perplexity:** AI-powered synthesis for complex, multi-hop reasoning tasks. Reserved for hard questions.

-   **Tier 5 --- Internal Search:** FalkorDB knowledge graph + optional Meilisearch for vault full-text search.

**Total Estimated Monthly Cost: \~£80-250**

This covers comprehensive multi-tier search across web, academic, specialist, and AI synthesis --- a fraction of what a single enterprise search licence would cost.

**The 5-Tier Search Architecture**

Every search query from any Amplified agent flows through a priority waterfall. The system tries the cheapest, fastest option first, and only escalates to more expensive tiers if the query requires it. This keeps costs low and latency fast for the vast majority of searches.

  ------------------ ---------------------------------------------- ----------------------- ----------------------------------------------------------- ------------------
  **Tier**           **Engine**                                     **Est. Monthly Cost**   **Use Cases**                                               **% of Queries**
  1 --- Default      SearXNG (self-hosted)                          £0                      All general web, image, news, science searches              80%+
  2 --- Fallback     Brave Search API                               £50-100                 When SearXNG fails, independent verification, LLM context   \~15%
  3 --- Specialist   OpenAlex, Semantic Scholar, Exa, GDELT, etc.   £15-50                  Academic, people/company, code, news, legal, patents        \~5%
  4 --- Synthesis    Perplexity AI                                  £50-100                 Complex multi-hop reasoning, PUDDING research, synthesis    \< 1%
  5 --- Internal     FalkorDB + Meilisearch                         £0 (self-hosted)        Knowledge graph, vault search, component lookup             Variable
  ------------------ ---------------------------------------------- ----------------------- ----------------------------------------------------------- ------------------

**How It Works in Practice**

When the Curator agent needs to find something, it sends the query to SearXNG first. SearXNG aggregates results from Google, Bing, Brave, DuckDuckGo, and dozens of other engines --- all through Amplified\'s own server on Beast, with no tracking, no logs, and a 10Gbps connection.

If the results are thin or the query is about a topic where independence matters (e.g. fact-checking a claim), the system escalates to Brave\'s independent index. For academic work, it goes straight to OpenAlex or Semantic Scholar. For people and company intelligence, it uses Exa. Only truly complex synthesis tasks --- like PUDDING cross-domain discovery --- get routed to Perplexity.

The Enforcer agent has its own dedicated verification pipeline (see Category 11) that uses a different combination of these tiers.

**Category 1: Meta-Search Engines**

Meta-search engines don\'t maintain their own index of the web. Instead, they query multiple other search engines simultaneously and combine the results. Think of them as search aggregators --- they give you one set of results drawn from many sources.

**SearXNG (Deployed --- Tier 1)**

SearXNG is Amplified\'s primary search engine, already running on Beast.[^2] It aggregates results from 70+ search engines including Google, Bing, Brave, and DuckDuckGo --- all without tracking or logging.

**Key Features**

-   Aggregates 70+ search engines with configurable weights and priorities

-   Categories: general, images, news, science, files, IT, music, videos, social media, map

-   Output formats: HTML, CSV, JSON, RSS --- perfect for agent integration

-   Full YAML configuration: enable/disable engines, set timeouts, weights, safe search

-   Multiple autocomplete backends (Google, Brave, DuckDuckGo, Bing, etc.)

-   Plugins: calculator, hash generator, unit converter, hostname filtering, tracker URL removal, Open Access DOI rewriting

-   Configurable rate limiting, connection pooling (100 connections, HTTP/2), proxy/Tor support

**Pricing**

-   Free --- self-hosted, open source

**Usefulness for Amplified**

This is the backbone. Every agent search routes here first. Running on Beast\'s 10Gbps Hetzner pipe with 48-core EPYC and 256GB RAM, it can handle massive query volumes with minimal latency. Already integrated with the Curator and Marketing Pipeline.

**Limitations**

-   Depends on upstream engines --- if Google or Bing block the instance, result quality degrades

-   No independent index --- it\'s only as good as the engines it queries

**Other Meta-Search Engines**

  ------------ --------------------------------------------------------------------------- -------------------- ----------------------------------------------------------------------------
  **Engine**   **What It Does**                                                            **Pricing**          **Relevance to Amplified**
  Whoogle      Self-hosted Google proxy --- strips tracking and ads from Google results    Free (self-hosted)   Too narrow --- only Google. SearXNG already covers this.
  MetaGer      German meta-search engine, run by non-profit SUMA-EV. Privacy-focused.      Free                 Limited API. SearXNG is a better fit.
  YaCy         Fully decentralised peer-to-peer search. Each node builds its own index.    Free (self-hosted)   Interesting concept for vault internal search, but too slow for real-time.
  Stract       Was a promising independent open-source search engine with its own index.   Free                 Appears inactive/discontinued as of late 2025. Watch this space.
  ------------ --------------------------------------------------------------------------- -------------------- ----------------------------------------------------------------------------

**Category 2: Independent Web Indexes**

These are search engines that build and maintain their own index of the web --- they actually crawl the internet themselves rather than reselling someone else\'s results. There are only three independent global-scale web indexes in the West: Google, Bing (Microsoft), and Brave.

**Brave Search API (Recommended --- Tier 2)**

Brave Search maintains an independent index of 40+ billion pages, refreshing 100M+ daily.[^3] In the AIMultiple agentic search benchmark (February 2026), Brave scored highest at 14.89, statistically outperforming Tavily and other competitors.[^4]

**Key Features**

-   Independent index built from real human browsing data (Web Discovery Project) --- less SEO spam than Google

-   Endpoints: Web Search, LLM Context (agent-optimised), Images, News, Videos

-   Rate limits up to 100 queries per second

-   SOC2 compliant, zero data retention option available

-   Spellcheck and autocomplete APIs included

**Pricing**

-   \$5 per 1,000 requests, with \$5 free credit per month

-   LLM Context / Answers plans: \$4/1k web + \$5/M tokens

**Usefulness for Amplified**

When SearXNG can\'t find what\'s needed, or when you want results from an index that isn\'t Google or Bing, Brave is the only game in town. Its LLM Context endpoint is purpose-built for AI agents --- it returns pre-processed, citation-ready content.

**Limitations**

-   Smaller index than Google (40B vs hundreds of billions)

-   Newer service --- some edge-case queries may return fewer results

**Other Independent Search Engines**

  ------------ ------------------------------------------------------------------------------------------------------------- ---------------------------------- -------------------------------------------------------------
  **Engine**   **What It Does**                                                                                              **Pricing**                        **Relevance to Amplified**
  Mojeek       UK-based independent crawler with billions of pages indexed. No tracking. Faceted search, domain filtering.   Paid tiers (contact for pricing)   Useful as a third independent index. UK-based is a plus.
  DuckDuckGo   Privacy-focused search using primarily Bing\'s index plus own crawling. Instant Answer API only.              Free (limited API)                 Already available through SearXNG. No direct API advantage.
  Startpage    Proxies Google results with privacy protection. Netherlands-based.                                            No API                             Already available through SearXNG.
  ------------ ------------------------------------------------------------------------------------------------------------- ---------------------------------- -------------------------------------------------------------

**Category 3: AI-Powered Search Engines**

These tools combine search with AI reasoning. Instead of just finding pages, they read, synthesise, and answer questions --- with citations. They\'re most valuable for complex queries that need understanding, not just retrieval.

**Perplexity AI (Recommended --- Tier 4 Synthesis)**

Perplexity is an AI-native answer engine that searches the web, reads the results, and produces synthesised answers with transparent citations.[^5] It excels at multi-hop reasoning --- questions where you need to connect information from multiple sources.

**Key Features**

-   Real-time web grounding with citation transparency

-   Academic and writing modes for different research needs

-   Strong at multi-hop reasoning and research synthesis

-   API available for programmatic access

**Pricing**

-   API: \~\$5 per 1,000 requests for search; higher for research/reasoning

-   Enterprise Pro: \$40/seat/month; Max: \$200/month

**Usefulness for Amplified**

Reserved for the hardest tasks: PUDDING cross-domain research synthesis, complex reasoning, and multi-hop questions where raw search results aren\'t enough. Don\'t waste it on simple lookups.

**Limitations**

-   Less optimised for local/transactional queries

-   Can oversimplify nuanced topics

-   More expensive than raw search --- reserve for high-value queries

**Other AI-Powered Search Engines**

  ---------------- ------------------------------------------------------------------------------- ---------------------------- ---------------------------------------------------------------------
  **Engine**       **What It Does**                                                                **Pricing**                  **Relevance to Amplified**
  ChatGPT Search   AI-enhanced search within ChatGPT. No standalone API.                           N/A (bundled with ChatGPT)   Not useful as infrastructure --- no external API.
  Google Gemini    AI-enhanced traditional search. No open API for AI search mode.                 N/A                          Not useful as infrastructure --- no external API.
  You.com          AI-native search with web, code, and research modes. API available.             API tiers available          Lower priority than Perplexity. Niche use cases.
  Phind            Developer-oriented AI search. Strong on code accuracy.                          Free tier + paid             Useful for Coder agent specifically. Narrow.
  Consensus        AI-powered academic search. Reads papers, gives yes/no answers with evidence.   Free tier + paid             Interesting for Enforcer\'s scientific verification. Worth testing.
  ---------------- ------------------------------------------------------------------------------- ---------------------------- ---------------------------------------------------------------------

**Category 4: Agentic Search APIs**

These are search APIs built specifically for AI agents --- they return clean, structured data optimised for LLM consumption rather than human-readable web pages. They\'re the plumbing that lets your agents search the web programmatically.

**Exa AI (Recommended --- Specialist Tier 3)**

Exa is a neural/semantic search API with its own index of billions of documents.[^6] What makes it special is its people search (1B+ LinkedIn profiles), company search (including pre-Series A startups), and code search capabilities.

**Key Features**

-   Neural/semantic search --- finds meaning, not just keywords

-   People search: 1B+ LinkedIn profiles, 50M+ updates per week

-   Company search: proprietary embeddings, including pre-Series A startups

-   Code search: 1B+ pages with token-succinct excerpts

-   Category filters: company, people, news, tweet, research\_paper, personal\_site, financial\_report

-   1,200 domain include/exclude filters, date filtering, language filtering

-   Benchmark: 81% on WebWalker (vs Tavily 71%), 70% on MKQA

-   Latency: p95 1.4-1.7 seconds; Instant mode sub-200ms

**Pricing**

-   \$1.50 per 1,000 searches; 1,000 free per month

**Usefulness for Amplified**

Excellent for the Marketing Pipeline\'s competitive intelligence, people research for prospecting, and company discovery. Also valuable for PUDDING cross-domain research where you need to find people and companies in specific sectors.

**Limitations**

-   More expensive per query than Brave for general web search

-   Best used for specialist searches rather than general queries

**Agentic API Comparison**

  ----------- ----------------------- --------------------------- ---------------------- ------------------- -----------------------
  **API**     **Own Index?**          **People/Company Search**   **Pricing (per 1k)**   **Latency (p95)**   **Benchmark Score**
  Exa AI      Yes (billions)          Yes --- 1B+ profiles        \$1.50                 1.4-1.7s            81% WebWalker
  Tavily      No (aggregator)         No                          \$8.00                 3.8-4.5s            71% WebWalker
  Firecrawl   No (search + extract)   No                          \~\$0.83/credit        Variable            Top tier (AIMultiple)
  SerpAPI     No (scrapes Google)     No                          Variable               Variable            N/A --- legal risk
  Serper      No (scrapes Google)     No                          \$0.30-1.00            Variable            N/A --- legal risk
  ----------- ----------------------- --------------------------- ---------------------- ------------------- -----------------------

**Tavily**

Acquired by Nebius in February 2026. Source-first discovery with good LangChain/LlamaIndex integration. However, it\'s slower, more expensive, and less capable than Exa on benchmarks. Maximum 20 results per query. No people, company, or code search.

**Firecrawl**

Combines search with full content extraction and an autonomous /agent endpoint plus browser sandbox.[^7] Useful for web extraction tasks --- when you need to read and process entire pages, not just search results.

**SerpAPI & Serper**

Both scrape Google results. Google sued SerpAPI, making this approach legally risky. These are not recommended for any Amplified use. If you need Google results, SearXNG already provides them.

**Category 5: Academic & Scholarly Search**

Academic search engines index research papers, journal articles, conference proceedings, and other scholarly output. For Amplified\'s nightly scientific verification and PUDDING cross-domain research, these are essential.

**OpenAlex (Recommended --- Academic Tier 1)**

OpenAlex is a free, open catalogue of the global research system, covering 480M+ works.[^8] Built on the legacy of Microsoft Academic, it provides a REST API designed for automation and high-throughput use.

**Key Features**

-   480M+ works across all academic disciplines

-   REST API built for agents: search titles/abstracts, stemming, filter by DOI, ORCID, institution, topic, OA status

-   60M open-access PDF and TEI XML full-text downloads

-   CLI for bulk downloads, massively parallelised

-   Entities: works, authors, sources, institutions, topics, concepts

-   Can self-host the entire dataset on Beast for maximum speed

**Pricing**

-   Usage-based: \~\$0.10 per 1,000 requests; free daily allowance covers most use

-   Full dataset download: free

**Usefulness for Amplified**

Primary academic search. The API-first design makes it perfect for agent integration. The option to self-host the entire dataset on Beast is a significant advantage --- zero latency, zero cost, complete independence.

**Limitations**

-   Coverage skews towards English-language research

-   Not all papers have full text available (60M of 480M)

**Semantic Scholar (Recommended --- Academic Tier 2)**

Developed by the Allen Institute for AI, Semantic Scholar covers 233M+ papers with AI-powered features.[^9] Its strength is in recommendation and citation network analysis.

**Key Features**

-   233M+ papers across all fields

-   SPECTER2 embeddings for finding semantically similar papers

-   AI-powered recommendations: \"papers like this\"

-   Full citation network exploration

-   Endpoints: paper search, paper details, author search, citations, recommendations, datasets

-   Full S2AG dataset downloadable for offline use

**Pricing**

-   Free --- unauthenticated: 1,000 RPS shared; authenticated: starts at 1 RPS (can request increase to 10 RPS)

**Usefulness for Amplified**

The recommendation engine is gold for PUDDING research --- find one relevant paper, then let Semantic Scholar find all related work. Citation networks help the Enforcer trace the provenance of scientific claims.

**Limitations**

-   Authenticated rate limits start low (1 RPS) --- needs API key for heavier use

-   Smaller coverage than OpenAlex (233M vs 480M)

**Academic Search Comparison**

  ------------------ --------------------- ------------------------ --------------------- -----------------------------------------
  **Engine**         **Coverage**          **Pricing**              **API**               **Best For**
  OpenAlex           480M+ works           Free / \~\$0.10/1k       REST, bulk download   Primary academic search, self-hosting
  Semantic Scholar   233M+ papers          Free                     REST, S2AG dataset    Recommendations, citation networks
  Google Scholar     \~200M articles       Free (no official API)   Via SearXNG only      Broad search, citation counts
  CORE               136M+ articles        Free                     API available         Open-access papers specifically
  BASE               136M+ articles        Free                     Limited               Supplementary --- covered by OpenAlex
  PubMed             Biomedical only       Free                     E-utilities API       Health/medical research
  Web of Science     Curated journals      Premium (expensive)      Multiple APIs         High-quality journals --- but expensive
  Scopus             Curated journals      Premium (expensive)      API available         Similar to Web of Science
  Science.gov        US federal research   Free                     Basic                 US government research niche
  Crossref           150M+ DOI records     Free                     REST API              DOI resolution, citation metadata
  ------------------ --------------------- ------------------------ --------------------- -----------------------------------------

**Category 6: Specialist Search Engines**

These tools serve specific domains --- code, business intelligence, legal, patents, and news. Each fills a gap that general web search can\'t.

**Code Search**

  -------------------- -------------------------------------------------------- --------------------------------------------------------------------------- ----------------------------- ----------------------------------------------------
  **Tool**             **What It Does**                                         **Key Features**                                                            **Pricing**                   **Relevance to Amplified**
  Sourcegraph          Advanced code search across repositories                 Regex, case-sensitive, diff search, AI \'Deep Search\', cross-repo/branch   Free OSS + enterprise tiers   Best for deep codebase analysis by Coder agent
  GitHub Code Search   Search within GitHub repositories                        Quick lookups, language filters                                             Free                          Limited: 100 results, no multi-line or diff search
  SearchCode           Cross-platform code search (GitHub, GitLab, Bitbucket)   Language/licence filtering                                                  Free                          Supplementary for broader code discovery
  Exa Code Search      Neural code search, 1B+ pages                            Token-succinct excerpts, maxCharacters control                              \$1.50/1k queries             Good for quick code snippets in agent context
  -------------------- -------------------------------------------------------- --------------------------------------------------------------------------- ----------------------------- ----------------------------------------------------

**Business Intelligence**

  --------------------- ----------------------------------------- --------------------------------------------------- ---------------------------- ---------------------------------------------------
  **Tool**              **What It Does**                          **Key Features**                                    **Pricing**                  **Relevance to Amplified**
  Crunchbase            Startup and company ecosystem directory   30M+ verified updates/year, prospecting, lead gen   Free tier + paid plans       Useful for broader company intelligence beyond UK
  PitchBook             Premium private market data               Analyst-verified, VC/PE/M&A data                    Custom pricing (expensive)   Not needed --- overkill for current use
  Companies House API   Free UK company registration data         SIC codes, directors, filing history                Free                         Already integrated in Marketing Pipeline
  --------------------- ----------------------------------------- --------------------------------------------------- ---------------------------- ---------------------------------------------------

**Legal Search**

  ------------------------- ------------------------------------------- ----------------------------------- ---------------- ----------------------------------------
  **Tool**                  **What It Does**                            **Key Features**                    **Pricing**      **Relevance to Amplified**
  UK Legislation API        UK statutes and statutory instruments       Full legislation.gov.uk database    Free             Key for regulatory compliance checks
  CourtListener             US court opinions, open source              API available, full-text search     Free             Useful for US legal research if needed
  Google Scholar Case Law   Search case law by jurisdiction             Free, filtered by courts            Free             Quick case law lookups
  Westlaw / LexisNexis      Most comprehensive legal databases          Enterprise-grade, premium content   Very expensive   Not needed at current scale
  Casetext (Clio)           AI-powered legal intelligence (CoCounsel)   AI search, brief analysis           Paid             Interesting but not priority
  ------------------------- ------------------------------------------- ----------------------------------- ---------------- ----------------------------------------

**Patent Search**

  --------------------------- -------------------------------------------------- ------------------------------------------------------------ ---------------- -------------------------------------------------------
  **Tool**                    **What It Does**                                   **Key Features**                                             **Pricing**      **Relevance to Amplified**
  Lens.org                    Open-access patent + scholarly literature search   100+ jurisdictions, citation analysis, graphical analytics   Free             Best choice --- integrates patents with scholarly lit
  Google Patents              Patent search (USPTO, EPO)                         AI prior art finder, simple interface                        Free             Quick patent checks
  Espacenet (EPO)             150M+ patent documents worldwide                   Machine translation, global coverage                         Free             Comprehensive global patent coverage
  Patsnap / Derwent / Orbit   Enterprise patent analytics                        Advanced analytics, expensive                                Very expensive   Not needed at current scale
  --------------------------- -------------------------------------------------- ------------------------------------------------------------ ---------------- -------------------------------------------------------

**News Search**

  ------------------ ------------------------------------- ----------------------------------------------------------------------------- ------------------- ------------------------------------------
  **Tool**           **What It Does**                      **Key Features**                                                              **Pricing**         **Relevance to Amplified**
  GDELT Project      Global news monitoring and analysis   65 languages, events/entities/themes, updated every 15 min, no registration   Free                Primary for trend detection and analysis
  NewsData.io        87,000+ sources, 206 countries        AI tags, sentiment analysis, 89 languages                                     Free: 200 req/day   Broad coverage news monitoring
  NewsAPI.org        80,000+ sources, 55 countries         Simple API, popular                                                           Free: 100 req/day   Alternative for quick news lookups
  The Guardian API   2.4M+ articles back to 1999           High-quality UK journalism                                                    Free: 500 req/day   Quality UK news specifically
  NewsCatcher        70,000 sources with NLP               Entity extraction, topics                                                     Paid plans          Alternative if more NLP needed
  Perigon            80,000 sources, enterprise            AI-enriched, real-time                                                        Paid plans          Enterprise-grade if needed later
  ------------------ ------------------------------------- ----------------------------------------------------------------------------- ------------------- ------------------------------------------

**Category 7: Internal / Enterprise Search**

These tools search your own data --- documents, databases, knowledge graphs. For Amplified, this means searching the vault, the component library, and the knowledge graph.

**Meilisearch (Recommended --- Vault Search)**

Meilisearch is a Rust-based, open-source search engine built for speed and simplicity.[^10] With sub-50ms latency, built-in typo tolerance, and hybrid keyword + vector search, it\'s an excellent fit for vault full-text search.

**Key Features**

-   Written in Rust, MIT licensed (core)

-   Sub-50ms search latency, disk-based (LMDB)

-   Hybrid search: keyword + vector/semantic

-   Automatic language detection, CJK support

-   Typo tolerance out of the box

-   56.3k GitHub stars, active community

-   v1.38 (March 2026): 7x faster embedding indexing

**Pricing**

-   Free --- self-hosted, open source (MIT core)

**Usefulness for Amplified**

Could replace or supplement FalkorDB\'s text search for the vault. Self-hosted on Beast, it would give near-instant full-text search across all vault documents. The hybrid search means agents can query by meaning, not just keywords.

**Limitations**

-   Not a graph database --- complements FalkorDB rather than replacing it

-   Would require integration work to sync with existing vault

**Internal Search Comparison**

  --------------- -------------- ------------- ----------- --------------------------- ------------ --------------------------------------
  **Tool**        **Language**   **Licence**   **Speed**   **Search Type**             **Scale**    **Relevance**
  Meilisearch     Rust           MIT           Sub-50ms    Hybrid (keyword + vector)   Moderate     Best fit --- self-hosted, fast, easy
  Typesense       C++            GPLv3         Very fast   Keyword + vector + RAG      Moderate     Alternative --- RAM-heavy
  Elasticsearch   Java           SSPL          Fast        Full-text + vector          Petabyte     Overkill for current scale
  Glean           SaaS           Proprietary   Fast        AI + knowledge graph        Enterprise   Not relevant --- building own
  Vectara         SaaS           Proprietary   Fast        RAG + hybrid                Enterprise   Interesting tech but SaaS
  --------------- -------------- ------------- ----------- --------------------------- ------------ --------------------------------------

**Typesense**

Written in C++ with GPLv3 licence.[^11] Blazingly fast (RAM-first architecture) with Raft-based high-availability clustering and conversational search with RAG. 25.3k GitHub stars. The main concern for Amplified is RAM requirements at vault scale.

**Elasticsearch**

The industry standard, Lucene-based, capable of petabyte scale. Powerful but complex to manage. Overkill for Amplified\'s current data volumes, but worth considering if the vault grows significantly.

**Category 8: Fact-Checking & Verification**

Fact-checking is one of the Enforcer agent\'s core responsibilities. This category covers the tools and methods available for automated claim verification --- from simple API lookups to LLM-based reasoning.

**Google Fact Check Tools**

Google maintains a set of fact-checking tools built on the ClaimReview schema.[^12]

**Key Features**

-   Fact Check Explorer: searches claim reviews from multiple fact-checking organisations

-   ClaimReview API: structured data schema for machine-readable fact-check results

-   Fact Check Markup Tool: for publishers to mark claims as reviewed

**Pricing**

-   Free

**Usefulness for Amplified**

Integrate the ClaimReview API into the Enforcer\'s verification pipeline. When a claim has already been fact-checked by a reputable organisation, the Enforcer can use that result immediately --- no need to verify from scratch.

**SkepticReader Approach**

SkepticReader is a Chrome plugin that detects logical fallacies, bias, and counterarguments using GPT models. A key research finding: it is \"really bad at fact-checking but very good at detecting bad reasoning skills, finding patterns in biased language and detecting logical fallacies.\"

**Usefulness for Amplified**

This is an important design principle for the Enforcer: focus on detecting bad reasoning, bias, and logical fallacies rather than trying to \"fact-check\" every specific claim. The Enforcer should catch flawed arguments, not just wrong numbers.

**LLM Parametric Fact-Checking**

Recent research (arXiv, March 2026) demonstrates that LLMs encode factuality signals in their internal representations that can verify claims without any external retrieval.[^13] Across 18 methods tested on 9 datasets, the INTRA approach achieved state-of-the-art results using internal knowledge only.

**Usefulness for Amplified**

The Enforcer can use a cheap LLM (e.g. gpt-4.1-mini) for quick fact-plausibility checks before spending money on expensive verification searches. Think of it as a fast triage step: if the LLM\'s internal knowledge flags a claim as suspicious, then escalate to full verification.

**AVeriTeC Benchmark**

AVeriTeC is a benchmark of real-world factual claims verified by human annotators. It provides a standard test set for evaluating fact-checking systems.

**Usefulness for Amplified**

Use AVeriTeC as a test set to measure the Enforcer\'s verification accuracy. Run periodic evaluations to ensure the verification pipeline is improving over time.

**Systematic Review Methodology**

Academic systematic reviews follow a rigorous 13-step process for comprehensive literature searching.[^14] The PICO framework (Patient, Intervention, Comparison, Outcome) structures search questions for maximum precision.

This methodology includes \"exploding\" thesaurus terms (searching broader terms automatically includes narrower ones), using controlled vocabularies, and documenting the entire search strategy for audit trails. These principles directly inform Amplified\'s hierarchical search strategy.

**Category 9: Hierarchical Search Strategy**

This is how Amplified\'s agents should actually conduct research. Rather than firing off a single search query, the system follows a structured funnel from broad discovery to verified synthesis.

**The 5-Stage Search Funnel**

Each stage uses different tools and has a different goal. The funnel progressively narrows the result set while increasing confidence.

**Stage 1: Broad Discovery**

-   Tools: SearXNG (all engines), OpenAlex (academic), Brave Search (web)

-   Goal: Cast a wide net, collect candidate sources

-   Output: Raw result set --- hundreds of items

**Stage 2: Filtering & Categorisation**

-   Tools: PUDDING labelling system, Curator short-code taxonomy

-   Goal: Categorise results by mechanism, not domain

-   Output: Labelled, deduplicated set --- dozens of items

**Stage 3: Deep Retrieval**

-   Tools: Semantic Scholar (recommendations), Exa AI (semantic), specific database APIs

-   Goal: Find related work, citation networks, cross-references

-   Output: Connected knowledge graph

**Stage 4: Verification**

-   Tools: Google Fact Check API, LLM parametric checking, academic cross-referencing

-   Goal: Validate claims against multiple independent sources

-   Output: Confidence-scored assertions

**Stage 5: Synthesis**

-   Tools: Perplexity (complex reasoning), LLM synthesis

-   Goal: Combine verified findings into actionable intelligence

-   Output: Research report with citations and confidence bands

**The 13-Step Systematic Review (Adapted for AI Agents)**

Adapted from the JMLA systematic review methodology[^15], these steps guide agents through rigorous research:

-   **1. Determine clear question:** Agent receives a structured query with explicit scope

-   **2. Identify key elements:** Extract entities, concepts, and relationships from the query

-   **3. Order by specificity:** Search most specific elements first, broaden progressively

-   **4. Build search strategy:** Define which databases to query, with Boolean logic

-   **5. Identify thesaurus terms:** Use controlled vocabularies where available (e.g. MeSH for medical)

-   **6. Identify synonyms:** Expand query with alternative terms and phrasings

-   **7. Add variations:** Include plurals, abbreviations, related forms

-   **8. Use database syntax:** Adapt the query for each search engine\'s specific syntax

-   **9. Optimise:** Review initial results and adjust the strategy

-   **10. Evaluate:** Check relevance of first page of results from each source

-   **11. Check for errors:** Verify search logic, look for missed terms

-   **12. Document:** Record the entire search strategy for audit trail

-   **13. Validate:** Cross-reference findings across multiple independent sources

**Category 10: Search Customisation and Relevance Tuning**

This section covers how Amplified can improve search quality over time --- not just which engines to use, but how to tune the results they return.

**Key Concepts**

**1. Hybrid Search**

Combines keyword matching (BM25/lexical) with semantic/vector search. Keyword search finds exact terms; semantic search finds meaning. Used together, they catch both precise lookups and conceptual queries. FalkorDB already supports vector search for the Curator\'s component matching. Meilisearch v1.38 added hybrid search natively.

**2. Reranking**

After initial search retrieval, a more expensive model reorders results by relevance. Cross-encoder reranking compares query+document pairs directly --- higher quality than simple keyword matching but slower. Useful when the initial search returns many results and precision matters more than speed.

**3. Learning-to-Rank (LTR)**

Machine learning models that learn optimal ranking from user interaction data. Over time, the system learns which results agents actually use and promotes those. Requires logging agent search interactions and building a feedback loop.

**4. Faceted Search**

Filtering by categories, types, dates, or attributes. Narrowing \"all components\" to \"authentication functions created in 2026\" makes results immediately useful.

**5. Relevance Tuning**

Manual or ML-driven adjustment of how results are ranked. Boosting certain fields (e.g., component name vs. description), adjusting decay functions (newer results ranked higher), or weighting verified sources above unverified.

**How This Applies to Amplified**

  -------------------------- ---------------------------------------------------------------- ----------------------------------------
  **Layer**                  **What It Does**                                                 **Tools**
  Engine-level aggregation   SearXNG decides which sources to query and weights them          SearXNG YAML config
  Knowledge graph search     FalkorDB combines vector similarity with graph relationships     FalkorDB vector index + OpenCypher
  Custom reranking           Score results against PUDDING labels or Curator quality scores   Custom Python, LLM-based
  Learning-to-Rank           Improve ranking based on agent feedback over time                Log interactions → train ranking model
  Full-text vault search     Fast keyword + semantic search across vault documents            Meilisearch hybrid search
  -------------------------- ---------------------------------------------------------------- ----------------------------------------

**Recommendation**

Start with hybrid search (already available via FalkorDB and Meilisearch) and simple relevance tuning (boost component name matches, weight higher-quality-scored components). Add reranking and LTR later once there is enough usage data to train on. Do not over-engineer this upfront --- the 5-tier architecture handles 90% of search quality; tuning is for the last 10%.

**Category 11: Verification Pipeline**

This is the Enforcer agent\'s dedicated fact-checking workflow. Every claim that needs verification passes through these five steps, from cheapest/fastest to most expensive/thorough.

**The 5-Step Verification Pipeline**

  --------------------------- ------------------------------- -------------------- ----------- -------------------------------------------------------------------------------
  **Step**                    **Tool**                        **Cost**             **Speed**   **What It Does**
  1\. Quick Plausibility      gpt-4.1-mini (LLM parametric)   \~\$0.001/check      Instant     Uses the LLM\'s internal knowledge to flag obviously implausible claims
  2\. Claim Lookup            Google Fact Check API           Free                 Fast        Checks if the claim has already been reviewed by a fact-checking organisation
  3\. Academic Verification   OpenAlex + Semantic Scholar     Free / \~\$0.10/1k   Moderate    Finds supporting or contradicting research papers
  4\. Cross-Reference         Brave Search API                \$5/1k queries       Fast        Independent web confirmation from a non-Google/Bing source
  5\. Human Review            Flagged for Ewan                N/A                  Slow        Low-confidence claims escalated for human judgement
  --------------------------- ------------------------------- -------------------- ----------- -------------------------------------------------------------------------------

The pipeline is designed to catch most problems cheaply in steps 1-2, reserve moderate effort for steps 3-4, and only escalate to expensive human review for genuinely uncertain claims. In practice, steps 1-2 should resolve 80%+ of verification requests.

**Design Principles**

-   Speed over perfection: a quick \'probably wrong\' is more useful than a slow \'definitely wrong\'

-   Independence: each step uses a different source to avoid correlated errors

-   Audit trail: every step is logged, so you can always trace how a claim was verified

-   Focus on bad reasoning: inspired by SkepticReader, the Enforcer should catch logical fallacies and bias, not just factual errors

-   Confidence scoring: every verified claim gets a confidence band (high/medium/low) rather than a binary true/false

**Cost Analysis**

All recommended tools with estimated monthly costs, assuming moderate usage by a multi-agent system.

  --------------------- ------------------ ---------------------- ----------------------- -------------------------------------
  **Tool**              **Tier**           **Pricing Model**      **Est. Monthly Cost**   **Notes**
  SearXNG               1 --- Default      Self-hosted            £0                      Already deployed on Beast
  Brave Search API      2 --- Fallback     \$5/1k requests        £50-100                 Includes \$5 free/month credit
  OpenAlex              3 --- Academic     \~\$0.10/1k requests   £10-20                  Free daily allowance; can self-host
  Semantic Scholar      3 --- Academic     Free                   £0                      Rate-limited; request API key
  Exa AI                3 --- Specialist   \$1.50/1k searches     £15-30                  1,000 free/month; people + company
  GDELT                 3 --- News         Free                   £0                      No registration needed
  Google Fact Check     Verification       Free                   £0                      ClaimReview API
  UK Legislation API    3 --- Legal        Free                   £0                      Already identified for pipeline
  Companies House API   3 --- Business     Free                   £0                      Already integrated
  Lens.org              3 --- Patents      Free                   £0                      Patent + scholarly
  Perplexity AI         4 --- Synthesis    \~\$5/1k requests      £50-100                 Reserve for complex reasoning
  Meilisearch           5 --- Internal     Self-hosted            £0                      Optional --- vault full-text search
  FalkorDB              5 --- Internal     Self-hosted            £0                      Already deployed
  --------------------- ------------------ ---------------------- ----------------------- -------------------------------------

**Total estimated monthly cost: £80-250**

This covers comprehensive multi-tier search across web, academic, specialist, and AI synthesis. For context, a single Elastic Cloud Enterprise licence or Glean subscription would cost many times this amount.

**Recommendations**

**Deploy Now**

These tools are ready for immediate integration into the Amplified operating system:

-   **Brave Search API:** Sign up, integrate as Tier 2 fallback. Estimated 5 minutes to get API key, 2 hours to integrate.

-   **OpenAlex API:** Integrate for academic search. Free, well-documented, agent-friendly.

-   **Google Fact Check API:** Add to Enforcer\'s verification pipeline. Free, simple REST API.

-   **GDELT:** Integrate for news monitoring and trend detection. Free, no registration.

**Test Next**

These are worth evaluating with a short pilot (1-2 weeks) before committing:

-   **Exa AI:** Run a trial with 1,000 free monthly searches to evaluate people/company search quality.

-   **Semantic Scholar:** Test recommendation engine for PUDDING research --- find one paper, see if related suggestions are useful.

-   **Meilisearch:** Deploy on Beast for vault full-text search. Evaluate whether it improves on FalkorDB\'s text search.

-   **Consensus:** Test for Enforcer\'s scientific claim verification. See if its yes/no answers with evidence are useful.

**Watch**

Keep an eye on these for future integration:

-   **Mojeek:** Third independent web index. UK-based. Could be valuable if Brave ever becomes unavailable.

-   **Stract:** Open-source independent search. Currently inactive, but if it revives, it\'s worth testing.

-   **Firecrawl:** Web extraction for when agents need to read and process entire pages. Evaluate if/when that need arises.

-   **Phind:** Developer AI search. Evaluate if the Coder agent needs specialised code search beyond Sourcegraph.

-   **Typesense:** Alternative to Meilisearch. Test if RAM requirements are manageable at vault scale.

**Strategic Note**

The most important takeaway from this research is the independence question. The Western web is dominated by three indexes (Google, Bing, Brave). Bing\'s public API is gone. Google is suing people who access its results programmatically. Brave is the last independent, commercially available alternative.

This means Amplified\'s architecture should never depend entirely on any single source. SearXNG\'s multi-engine aggregation provides resilience, and Brave provides independent verification. The specialist APIs (OpenAlex, Exa, GDELT) provide depth in specific domains. Together, this creates a search infrastructure that no single company can shut off.

[^1]: Brave Search API --- <https://brave.com/search/api/>

[^2]: SearXNG Project --- <https://github.com/searxng/searxng>

[^3]: Brave Search API --- <https://brave.com/search/api/>

[^4]: AIMultiple Agentic Search Benchmark (Feb 2026) --- <https://aimultiple.com/agentic-search-api>

[^5]: Perplexity AI --- <https://www.perplexity.ai>

[^6]: Exa AI --- <https://exa.ai>

[^7]: Firecrawl --- <https://www.firecrawl.dev>

[^8]: OpenAlex --- <https://openalex.org>

[^9]: Semantic Scholar API --- <https://api.semanticscholar.org/>

[^10]: Meilisearch --- <https://www.meilisearch.com>

[^11]: Typesense --- <https://typesense.org>

[^12]: Google Fact Check Tools --- <https://toolbox.google.com/factcheck/>

[^13]: LLM Parametric Knowledge for Fact Checking (arXiv, 2026) --- <https://arxiv.org/abs/2503.00662>

[^14]: JMLA Systematic Review Methodology (2018) --- <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6148622/>

[^15]: JMLA Systematic Review Methodology (2018) --- <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6148622/>
