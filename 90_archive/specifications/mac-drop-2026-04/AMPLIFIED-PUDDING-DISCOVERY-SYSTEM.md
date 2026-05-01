Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

+----------------------------------------------------------------------+
| **AMPLIFIED PUDDING**                                                |
|                                                                      |
| **DISCOVERY SYSTEM**                                                 |
|                                                                      |
| *Automated Cross-Domain Pattern Detection for Literature-Based       |
| Discovery on Beast*                                                  |
|                                                                      |
| v1.0 --- March 2026                                                  |
|                                                                      |
| *INTERNAL --- Amplified Partners*                                    |
+----------------------------------------------------------------------+

**PART 1: SYSTEM OVERVIEW**

**1.1 What This System Does**

The Amplified Pudding Discovery System (APDS) is an automated pipeline
that continuously scans related websites, industry sources, academic
repositories, and data feeds to discover Pudding connections ---
cross-domain symbiotic patterns that produce 1+1=3 insights when
combined.

The system applies Don Swanson\'s Literature-Based Discovery (LBD) ABC
model at scale:

-   **A → B** (known connection, one domain/site)

-   **B → C** (known connection, different domain/site)

-   **Therefore A → C** (undiscovered connection --- the Pudding)

**Key innovation**: Instead of manual pudding sessions, APDS runs 24/7
on Beast, reading the \"body language\" of data --- recurring patterns,
anomalies, weak signals, drift, and structural equivalences --- and
surfacing candidate recipes automatically for human review.

**1.2 Design Principles**

1.  **Slime Mold Logic (R.?.4.v)**: The system explores ALL paths
    simultaneously, reinforces those that find connections, starves
    those that don\'t. The discovery engine IS a slime mold.

2.  **Radical Attribution**: Every discovered connection traces back to
    its source sites, search queries, and the Swanson ABC chain.

3.  **Score Everything 0-10**: Every signal, every candidate, every
    recipe gets scored. PRS \>= 7.0 ships to review, \>= 9.0 is gold
    standard.

4.  **Token Efficiency**: 60-70% local (Ollama on Beast), 20-30%
    standard API (Claude Sonnet via LiteLLM), 5-10% premium (Opus for
    recipe validation).

5.  **Deterministic vs AI**: Run both deterministic pattern matching AND
    AI-based discovery in parallel. Score both. Data decides winner.

6.  **Blinkers Without Ceilings**: Bounded on financial/operational data
    (0.90+ confidence), Creative freedom on discovery and innovation
    (0.85 threshold).

**1.3 System PUDDING Label**

**M.+.5.l** --- Meta-framework, Amplifying, System-scale, Long-duration

**PART 2: ARCHITECTURE**

**2.1 Five-Stage Pipeline**

The APDS operates as a five-stage pipeline, from harvesting raw content
through to scoring and surfacing discovered recipes for human review.

![Diagram showing the five stages: Harvest, Extract, Label, Match, Score
&
Surface](media/bf3158ca15c34c012e8a946e32b0c410fb1a7222.png "APDS Five-Stage Pipeline"){width="5.625in"
height="7.8125in"}

*Figure 1: APDS Five-Stage Pipeline*

**2.2 Detailed Architecture Diagram**

The following diagram shows the complete architecture of the APDS system
running on Beast, including all sub-components within each pipeline
stage.

![Detailed architecture diagram showing all components of the APDS
system](media/0d2fc7ed3e0848379b0fbd4227c9211e9a3729c0.png "APDS Detailed Architecture on Beast"){width="5.625in"
height="7.447916666666667in"}

*Figure 2: APDS Detailed Architecture on Beast*

**2.3 Beast Infrastructure Mapping**

  --------------- ---------------- ---------- ------------------------------------------------------------
  **Component**   **Container**    **Port**   **Role in APDS**
  SearXNG         searxng          8888       Primary harvest engine, 243+ sources
  Ollama          ollama           11434      Entity extraction (8b), PUDDING labelling (70b)
  LiteLLM         litellm          4000       Model routing: local → standard → premium
  FalkorDB        falkordb         6379       Knowledge graph: entities, relationships, recipes
  Graphiti        (via FalkorDB)   ---        Temporal edges, entity resolution, contradiction detection
  PostgreSQL      postgres         5432       Harvest logs, change detection state, audit trail
  MinIO           minio            ---        Raw content archive (append-only backup)
  Enforcer        enforcer         ---        Pipeline health monitoring, 10-min checks
  Langfuse        langfuse         ---        Token tracking, cost monitoring per pipeline stage
  Temporal        cove-temporal    7233       Workflow orchestration for multi-step discovery runs
  --------------- ---------------- ---------- ------------------------------------------------------------

**2.4 FalkorDB Graph Schema for APDS**

// Source Registry

(:Source {id, url, name, tier, domain, scan\_frequency, last\_scanned,
status})

// Harvested Content

(:Content {id, source\_id, url, title, text\_hash, harvested\_at,
change\_type})

// Extracted Entities (neutral mechanism labels)

(:Concept {

id, // AMP-{APQC\#}-{SEQ}-{VERSION}

mechanism\_label, // Neutral label (no domain name)

pudding\_label, // WHAT.HOW.SCALE.TIME

dimensions, // Array of semantic dimensions

relevance\_score, // 0-5

actionability\_score, // 0-5

evidence\_score, // 0-5

impact\_score, // 0-5

total\_pudding\_score, // 0-20

source\_domain, // Which domain this came from

extracted\_at,

validated\_at

})

// Relationships (influence triples)

(:Concept)-\[:PROMOTES\|INHIBITS\|ENABLES\|REQUIRES\|CONTRADICTS {

confidence, source\_url, extracted\_at

}\]-\>(:Concept)

// Pudding Recipes

(:Recipe {

id,

concept\_a\_id,

bridge\_b\_id,

concept\_c\_id,

hypothesis,

one\_plus\_one\_equals\_three, // The named emergent insight

simple\_score, // (SharedDims×2) + Unique\_A + Unique\_B

advanced\_score, // (DomainDist×PatternAlignment) + GapComp + Tension

jaccard\_slot, // Label overlap score

domain\_distance, // 1-6 how far apart

status, // hypothesis \| tested\_internal \| tested\_client \| proven

testable\_prediction,

discovered\_at,

discovered\_by, // deterministic \| ai \| hybrid

reviewed\_by, // null until human review

reviewed\_at

})

// Body Language Signals

(:Signal {

id,

type, // anomaly \| drift \| spike \| weak\_signal \| convergence

source\_ids, // Which sources triggered this

description,

severity, // 0-10

detected\_at,

resolved\_at

})

// Cross-domain edges

(:Concept)-\[:BRIDGES {jaccard, pmi, recipe\_id}\]-\>(:Concept)

(:Signal)-\[:INDICATES\]-\>(:Recipe)

(:Content)-\[:CONTAINS\]-\>(:Concept)

(:Source)-\[:PROVIDES\]-\>(:Content)

**PART 3: RELATED SITES TAXONOMY**

**3.1 Source Tier System**

The system scans sources organised into 4 tiers, each with different
scan frequencies, confidence weights, and token budgets.

  ---------- --------------------------- -------------------- ----------------------- ------------------------ ----------------------------------------------------------------------------------------------------------------------
  **Tier**   **Name**                    **Scan Frequency**   **Confidence Weight**   **Token Routing**        **Examples**
  T1         Primary Domain Sources      Every 4 hours        1.0                     80% Ollama               Industry bodies, trade publications, regulators (FCA, HMRC, ICO, Companies House)
  T2         Cross-Domain Intelligence   Every 8 hours        0.8                     70% Ollama, 30% Sonnet   Adjacent industries, technology news, academic preprints (arXiv, SSRN), patent databases
  T3         Weak Signal Horizons        Daily                0.6                     60% Ollama, 40% Sonnet   Frontier research, biology/neuroscience, emerging tech, philosophy of science, obscure trade journals
  T4         Serendipity Pool            Weekly               0.4                     50% Ollama, 50% Sonnet   Completely unrelated domains --- agriculture, art criticism, linguistics, materials science. Highest-value puddings.
  ---------- --------------------------- -------------------- ----------------------- ------------------------ ----------------------------------------------------------------------------------------------------------------------

**3.2 Source Categories**

**A. SMB Business Domain (T1)**

-   Companies House filings, FCA regulatory updates

-   HMRC guidance changes, pension regulations

-   Trade body publications (FSB, BCC, IoD)

-   Accounting standards updates (IFRS, UK GAAP)

-   Employment law changes (ACAS, CIPD)

-   Insurance market reports

-   Banking/fintech announcements

**B. Technology & AI (T1-T2)**

-   arXiv cs.AI, cs.CL, cs.IR papers

-   Hacker News front page

-   AI safety research (Anthropic, DeepMind blogs)

-   LLM benchmarks and evaluations

-   Graph database developments (FalkorDB, Neo4j blogs)

-   RAG architecture research

**C. Adjacent Industries (T2)**

-   Healthcare informatics

-   Legal tech developments

-   Education technology

-   Government digital services (GOV.UK)

-   Supply chain management

-   Real estate technology

**D. Science & Biology (T3)**

-   Neuroscience (decision-making, pattern recognition)

-   Evolutionary biology (adaptation, competition)

-   Network science (graph theory, emergence)

-   Complexity science (Santa Fe Institute)

-   Systems biology (feedback loops, signalling)

-   Mycology (mycelial networks --- literally the Wood Wide Web)

**E. Serendipity (T4)**

-   Art criticism (pattern recognition in visual arts)

-   Linguistics (semantic drift, language evolution)

-   Materials science (structural properties, composites)

-   Urban planning (infrastructure networks)

-   Music theory (harmony, resonance, interference patterns)

-   Culinary science (ingredient combinations --- actual pudding
    science)

**3.3 SearXNG Query Templates**

Each source tier uses structured query templates that run on schedule
via the APDS cron system.

\# T1 Primary Query Template

queries:

success\_pattern:

template: \"{topic} best practices {year}\"

engines: \[\"google\", \"bing\", \"duckduckgo\"\]

categories: \[\"general\", \"news\"\]

time\_range: \"month\"

failure\_pattern:

template: \"{topic} failures lessons learned {year}\"

engines: \[\"google\", \"bing\"\]

categories: \[\"general\", \"news\"\]

time\_range: \"month\"

\# T2 Cross-Domain Query Template

queries:

technique\_scan:

template: \"{mechanism} technique methodology framework\"

engines: \[\"google scholar\", \"semantic scholar\"\]

categories: \[\"science\"\]

time\_range: \"year\"

\# T3 Weak Signal Template

queries:

emerging:

template: \"{concept} novel approach emerging 2026\"

engines: \[\"google scholar\", \"arxiv\"\]

categories: \[\"science\", \"it\"\]

time\_range: \"year\"

\# T4 Serendipity Template

queries:

random\_walk:

template: \"{random\_mechanism\_dimension} applied
{random\_unrelated\_domain}\"

engines: \[\"google\", \"google scholar\"\]

categories: \[\"general\", \"science\"\]

**PART 4: BODY LANGUAGE OF DATA**

**4.1 What \"Body Language\" Means**

Data has body language --- unconscious signals that reveal what\'s
really happening beneath the surface. The APDS reads six types of body
language:

  ----------------- ------------------- ------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------- ----------------------
  **Signal Type**   **PUDDING Label**   **Description**                                                                            **Detection Method**                                                                                          **Biological Logic**
  Anomaly           S.!.1.i             A value or pattern that deviates significantly from the norm                               Clipped SGD (Amazon GuardDuty approach) --- handles both anomalies and distribution drift simultaneously      Bacterial / Quorum
  Drift             S.-.4.m             Gradual change in data distribution over time                                              Moving-average baseline comparison + KL divergence scoring                                                    Slime Mold
  Spike             S.\>.1.i            Sudden increase in mentions, citations, or activity around a topic                         Z-score on rolling window, threshold at 3σ                                                                    Bacterial / Quorum
  Weak Signal       I.?.4.v             Low-frequency terms appearing across multiple unrelated sources                            Ansoff weak signal criteria: low frequency + novel + temporal evolution. Evolution rate scoring per cluster   Slime Mold
  Convergence       R.+.4.l             Multiple independent sources pointing to the same mechanism                                Quorum detection: when N \>= threshold independent signals converge, flag as convergent                       Bacterial / Quorum
  Structural Echo   M.=.0.p             Two concepts from different domains receiving identical or near-identical PUDDING labels   Jaccard slot matching on PUDDING labels. P(4/4 match by chance) = 1/2058 = 0.049%                             Mycelial
  ----------------- ------------------- ------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------- ----------------------

**4.2 Signal Processing Pipeline**

The signal processing pipeline takes raw content through four analysis
stages before passing results to the LABEL stage.

![Diagram showing the signal processing pipeline: Frequency Analysis,
Semantic Clustering, Weak Signal Filter, Convergence
Detection](media/78da8da92dc7f9eaae2b6fc18bad1b8c4b3d442f.png "Signal Processing Pipeline"){width="5.625in"
height="6.71875in"}

*Figure 3: Body Language of Data --- Signal Processing Pipeline*

**4.3 Deterministic vs AI --- Running Both**

The system runs both deterministic code and AI inference in parallel for
every signal detection task, then scores both outputs.

  ------------------------- ------------------------------------ ----------------------------------- ---------------------------------------
  **Task**                  **Deterministic Approach**           **AI Approach**                     **Winner Decided By**
  Entity extraction         Regex + NER (spaCy)                  Ollama llama3.1:8b                  F1 score on validation set
  Relationship extraction   Dependency parsing + pattern rules   Ollama llama3.1:8b                  Precision on manual sample
  PUDDING labelling         Rule-based taxonomy mapper           Ollama llama3.1:70b                 Inter-rater agreement vs human labels
  Pattern matching          Jaccard + PMI (pure math)            Claude Sonnet (semantic bridging)   Recipe validation rate
  Anomaly detection         Z-score + KL divergence              Ollama (contextual anomaly)         True positive rate
  Weak signal detection     Frequency filter + evolution rate    Ollama (semantic novelty)           Expert validation rate
  ------------------------- ------------------------------------ ----------------------------------- ---------------------------------------

**Scoring**: Each approach gets a 0-10 score for accuracy, cost, and
latency. The weighted composite determines routing for that task going
forward. Scores update weekly via Kaizen cycle.

**PART 5: OPERATIONAL SPECIFICATION**

**5.1 Cron Schedule**

\# APDS Cron Jobs on Beast

apds\_harvest\_t1:

cron: \"0 \*/4 \* \* \*\" \# Every 4 hours

task: \"Harvest T1 primary sources\"

container: apds-harvester

apds\_harvest\_t2:

cron: \"0 \*/8 \* \* \*\" \# Every 8 hours

task: \"Harvest T2 cross-domain sources\"

container: apds-harvester

apds\_harvest\_t3:

cron: \"0 3 \* \* \*\" \# Daily at 3am UTC

task: \"Harvest T3 weak signal horizons\"

container: apds-harvester

apds\_harvest\_t4:

cron: \"0 2 \* \* 0\" \# Weekly Sunday 2am UTC

task: \"Harvest T4 serendipity pool\"

container: apds-harvester

apds\_extract:

cron: \"30 \*/4 \* \* \*\" \# 30 min after harvest

task: \"Extract entities, relationships, signals from new content\"

container: apds-extractor

apds\_label:

cron: \"0 \*/6 \* \* \*\" \# Every 6 hours

task: \"PUDDING label new concepts, score with 4-criteria rubric\"

container: apds-labeller

apds\_match:

cron: \"0 \*/12 \* \* \*\" \# Every 12 hours

task: \"Run cross-domain pattern matching, assemble recipes\"

container: apds-matcher

apds\_score:

cron: \"0 6 \* \* \*\" \# Daily at 6am UTC

task: \"Score all new recipes, rank, push to review queue\"

container: apds-scorer

apds\_kaizen:

cron: \"0 0 \* \* 1\" \# Weekly Monday midnight UTC

task: \"Kaizen review: compare deterministic vs AI scores, update
routing\"

container: apds-kaizen

**5.2 Container Architecture**

\# /opt/amplified/apps/apds/docker-compose.yml

services:

apds-harvester:

build: ./harvester

container\_name: apds-harvester

environment:

\- SEARXNG\_URL=http://searxng:8888

\- FALKORDB\_HOST=falkordb

\- FALKORDB\_PORT=6379

\- POSTGRES\_HOST=postgres

\- MINIO\_HOST=minio

networks:

\- amplified-net

labels:

\- \"traefik.enable=false\" \# Internal only

apds-extractor:

build: ./extractor

container\_name: apds-extractor

environment:

\- OLLAMA\_URL=http://ollama:11434

\- LITELLM\_URL=http://litellm:4000

\- FALKORDB\_HOST=falkordb

networks:

\- amplified-net

apds-labeller:

build: ./labeller

container\_name: apds-labeller

environment:

\- OLLAMA\_URL=http://ollama:11434

\- LITELLM\_URL=http://litellm:4000

\- FALKORDB\_HOST=falkordb

networks:

\- amplified-net

apds-matcher:

build: ./matcher

container\_name: apds-matcher

environment:

\- FALKORDB\_HOST=falkordb

\- LITELLM\_URL=http://litellm:4000

networks:

\- amplified-net

apds-scorer:

build: ./scorer

container\_name: apds-scorer

environment:

\- FALKORDB\_HOST=falkordb

\- TELEGRAM\_BOT\_TOKEN=\${TELEGRAM\_BOT\_TOKEN}

networks:

\- amplified-net

apds-dashboard:

build: ./dashboard

container\_name: apds-dashboard

labels:

\- \"traefik.enable=true\"

\-
\"traefik.http.routers.apds.rule=Host(\`pudding.beast.amplifiedpartners.ai\`)\"

\- \"traefik.http.routers.apds.tls=true\"

\- \"traefik.http.routers.apds.tls.certresolver=letsencrypt\"

\- \"traefik.http.services.apds.loadbalancer.server.port=3000\"

networks:

\- amplified-net

networks:

amplified-net:

external: true

**5.3 Cost Estimates**

  ----------------------- ---------------------------------------------- ----------------------- ----------------
  **Stage**               **Model**                                      **Tokens/Day (est.)**   **Cost/Day**
  Harvest                 SearXNG (free, self-hosted)                    N/A                     \$0.00
  Extract (bulk)          Ollama llama3.1:8b                             \~500K tokens           \$0.00 (local)
  Extract (complex)       Claude Sonnet via LiteLLM                      \~50K tokens            \~\$0.15
  Label                   Ollama llama3.1:70b                            \~200K tokens           \$0.00 (local)
  Match (deterministic)   Pure code                                      N/A                     \$0.00
  Match (AI)              Claude Sonnet                                  \~30K tokens            \~\$0.09
  Score/Validate          Claude Opus (premium, for gold recipes only)   \~10K tokens            \~\$0.15
  TOTAL                                                                                          \~\$0.39/day
  ----------------------- ---------------------------------------------- ----------------------- ----------------

Annual estimate: \~\$142/year --- well within the daily \$5 budget cap
during build phase.

**5.4 Monitoring & Quality Gates**

  ---------------------------- ------------------- ----------------------------- ------------------------------------
  **Check**                    **Frequency**       **Tool**                      **Alert Threshold**
  Harvest success rate         Every harvest run   Enforcer                      \< 90% sources responding
  Extract quality (sample)     Daily               Kaizen worker                 Precision \< 0.7 on manual sample
  Label consistency            Weekly              Inter-rater agreement check   Kappa \< 0.6
  Recipe false positive rate   Weekly              Human review feedback loop    \> 40% recipes rejected
  Token spend                  Daily               Langfuse                      \> \$5/day
  Pipeline latency             Per run             Enforcer                      Harvest-to-recipe \> 6 hours
  FalkorDB graph health        Every 10 min        Enforcer                      Connection failures, memory \> 7GB
  ---------------------------- ------------------- ----------------------------- ------------------------------------

**PART 6: THE MATCHING ALGORITHM IN DETAIL**

**6.1 Step 1: Pair Generation**

For N concepts in the graph, there are N(N-1)/2 possible pairs. With
1,000 concepts, that\'s \~500,000 pairs. PUDDING label filtering
compresses this 3,000:1.

Filter 1: Same-domain pairs → DISCARD (not cross-domain, not pudding)

Filter 2: Pudding score \< 12/20 → DISCARD (low-quality ingredients)

Filter 3: Jaccard slot \< 0.5 → DISCARD (insufficient structural match)

Remaining: \~75-150 candidate pairs from \~500K

**6.2 Step 2: B-Term Discovery**

For each surviving pair (A, C), the system searches for bridging
B-terms:

**Deterministic B-term search:**

// FalkorDB Cypher query for shared neighbours

MATCH (a:Concept {id:
\$concept\_a})-\[:PROMOTES\|ENABLES\]-\>(b:Concept)

\<-\[:PROMOTES\|ENABLES\]-(c:Concept {id: \$concept\_c})

WHERE a.source\_domain \<\> c.source\_domain

AND b.total\_pudding\_score \>= 12

RETURN b,

SIZE(\[d IN a.dimensions WHERE d IN c.dimensions\]) as shared\_dims,

SIZE(\[d IN a.dimensions WHERE NOT d IN c.dimensions\]) as unique\_a,

SIZE(\[d IN c.dimensions WHERE NOT d IN a.dimensions\]) as unique\_c

ORDER BY shared\_dims DESC

**AI B-term search (Claude Sonnet):**

Given:

\- Concept A: {mechanism\_label} from domain {source\_domain},

PUDDING label {pudding\_label}

\- Concept C: {mechanism\_label} from domain {source\_domain},

PUDDING label {pudding\_label}

These share {shared\_dimensions} semantic dimensions.

What mechanism could serve as a bridge between these two concepts?

The bridge must be:

1\. A neutral mechanism (not named after either domain)

2\. Something that both A and C connect to but have never been

connected through

3\. Expressible as a PUDDING label

State the B-term, the A→B and B→C connections, and the

hypothesised A→C insight.

**6.3 Step 3: Recipe Scoring**

**Simple Score** (for initial filtering):

Score = (Shared Dimensions × 2) + Unique\_A + Unique\_B

Minimum viable: \>= 5

**Advanced Score** (for cross-domain mixes):

Score = (Domain Distance × Pattern Alignment) + Gap Complement + Tension
Bonus

Where:

\- Domain Distance (1-6): How far apart are the source tiers/domains?

\- Pattern Alignment (1-10): How closely do PUDDING labels match?

\- Gap Complement (1-5): Does the combination fill a gap neither fills
alone?

\- Tension Bonus (0-3): Is there productive tension between approaches?

Score \>= 13: Worth reviewing

Score \>= 18: Build immediately

Score \>= 20: Highest priority --- alert Ewan via Telegram

**Pudding Rank** (for automated prioritisation):

Pudding Rank = (Jaccard\_slot × Domain\_Distance) + (Unique\_dimensions
/ Total\_dimensions)

Filters applied:

\- Jaccard\_slot \>= 0.75

\- Domain\_Distance \>= 3/6

\- Individual rubric score \>= 12/20 for both concepts

**6.4 Step 4: Hypothesis Generation**

For each recipe that passes scoring, the system generates:

1.  **The ABC Chain**: A (technique from domain 1) → B (shared bridge
    mechanism) → C (technique from domain 2)

2.  **The Hypothesis**: What does A→C reveal that neither A nor C
    revealed alone?

3.  **The 1+1=3 Insight**: Named explicitly. If it can\'t be named,
    it\'s not pudding.

4.  **Testable Prediction**: A concrete, falsifiable prediction that can
    be tested.

5.  **Validation Status**: hypothesis \| tested\_internal \|
    tested\_client \| proven

**PART 7: DATA PARTITIONING**

**7.1 Living Data (FalkorDB)**

kg\_pudding\_discovery // APDS main graph --- concepts, recipes, signals

kg\_internal // Amplified Partners operational data (existing)

kg\_expert\_library // 27 experts, principles, rubrics (existing)

**7.2 Backup Data (PostgreSQL → MinIO)**

apds\_harvest\_log // Every URL fetched, response code, content hash

apds\_content\_archive // Raw text, append-only (MinIO buckets)

apds\_recipe\_audit // Every recipe scored, reviewed, accepted/rejected

apds\_signal\_history // All signals detected, resolution status

**7.3 Testing Data**

kg\_testing // Testing graph (existing)

rd-sandbox // Isolated network for experimental runs

**PART 8: INTEGRATION WITH EXISTING SYSTEMS**

**8.1 Graphiti Integration**

APDS feeds into the existing Graphiti temporal knowledge graph:

-   New concepts → Graphiti episodic ingestion

-   Temporal edges: when concepts first appeared, when connections were
    discovered

-   Entity resolution: \"machine learning\", \"ML\", \"deep learning\" →
    disambiguated

-   Contradiction detection: new evidence that invalidates old
    connections

**8.2 Kaizen Integration**

-   Weekly Kaizen cycle reviews APDS performance

-   Compare deterministic vs AI scores → update routing

-   Track recipe acceptance rate → tune scoring thresholds

-   Measure token spend → optimise local/API ratio

**8.3 Chaos Testing Integration**

-   Monthly chaos tests inject fake signals to test detection accuracy

-   Inject known-false connections to test recipe rejection rate

-   Introduce drift in source quality to test body language detection

-   All chaos test results feed back into scoring calibration

**8.4 Vault Integration**

-   High-scoring recipes (\>= 18) automatically written to vault as
    hypothesis documents

-   YAML frontmatter applied per vault standard

-   Filed to 18-research/pudding-discoveries/

-   Cross-referenced in Graphiti for knowledge graph enrichment

**PART 9: IMPLEMENTATION ROADMAP**

**Phase 1: Foundation (Weeks 1-2)**

> ☐ Create FalkorDB graph schema for APDS (kg\_pudding\_discovery)
>
> ☐ Build source registry (50 initial sources across all 4 tiers)
>
> ☐ Implement SearXNG harvest cron (T1 only initially)
>
> ☐ Build content change detection using SemHash
>
> ☐ Deploy apds-harvester container on Beast

**Phase 2: Extraction (Weeks 3-4)**

> ☐ Build entity extraction pipeline (Ollama 8b)
>
> ☐ Build relationship extraction (influence triples)
>
> ☐ Implement PUDDING labelling (Ollama 70b)
>
> ☐ Build 4-criteria scoring
>
> ☐ Deploy apds-extractor and apds-labeller containers

**Phase 3: Discovery (Weeks 5-6)**

> ☐ Implement deterministic pattern matcher (Jaccard + PMI)
>
> ☐ Implement AI pattern matcher (Claude Sonnet)
>
> ☐ Build recipe assembler and scorer
>
> ☐ Build Telegram alert integration
>
> ☐ Deploy apds-matcher and apds-scorer containers

**Phase 4: Body Language (Weeks 7-8)**

> ☐ Implement signal detection pipeline (all 6 signal types)
>
> ☐ Build frequency analysis + semantic clustering
>
> ☐ Build weak signal filter (Ansoff criteria)
>
> ☐ Build convergence detector (quorum logic)
>
> ☐ Integrate with Enforcer health monitoring

**Phase 5: Dashboard & Review (Weeks 9-10)**

> ☐ Build APDS dashboard (pudding.beast.amplifiedpartners.ai)
>
> ☐ Recipe review workflow
>
> ☐ Deterministic vs AI comparison dashboard
>
> ☐ Token spend tracking
>
> ☐ Weekly Kaizen report generation

**Phase 6: Validation & Tuning (Weeks 11-12)**

> ☐ Run chaos testing suite
>
> ☐ Calibrate scoring thresholds based on human review
>
> ☐ Expand source registry to 200+ sources
>
> ☐ Enable T2-T4 harvesting
>
> ☐ First client-facing pudding discoveries

**PART 10: RESEARCH SOURCES (Radical Attribution)**

**Literature-Based Discovery**

**1.** Swanson, D.R. (1986). \"Fish oil, Raynaud\'s syndrome, and
undiscovered public knowledge.\" Perspectives in Biology and Medicine,
30(1), 7-18.

**2.** Kastrin, A., Cestnik, B., Lavrač, N. (2025). \"Recent Advances
and Future Directions in Literature-Based Discovery.\" arXiv:2506.12385.
<https://arxiv.org/abs/2506.12385>

**3.** Kastrin, A. (2025). IDA2025 LBD Reproducible Pipelines. GitHub.
<https://github.com/akastrin/ida2025lbd>

**4.** Hahn-Powell, G., Valenzuela-Escarcega, M.A., Surdeanu, M.
\"Swanson Linking Revisited: Accelerating LBD Across Domains Using a
Conceptual Influence Graph.\" ACL 2017.
<https://aclweb.org/anthology/P17-4018>

**5.** Beck, D., Verspoor, K., Pu, Y. (2025). \"Enriched Knowledge
Representation in Biological Fields: A Case Study of LBD in Alzheimer\'s
Disease.\" Journal of Biomedical Semantics.
<https://pmc.ncbi.nlm.nih.gov/articles/PMC11924609/>

**6.** Taleb, I., Navaz, A.N., Serhani, M. (2024). \"Leveraging Large
Language Models for Enhancing Literature-Based Discovery.\" Big Data and
Cognitive Computing, 8(11), 146.
<https://www.mdpi.com/2504-2289/8/11/146>

**Automated Knowledge Graph Construction**

**7.** TrustGraph Architecture Documentation.
<https://docs.trustgraph.ai/overview/architecture.html>

**8.** FalkorDB + TrustGraph Integration.
<https://www.falkordb.com/news-updates/trustgraph-autonomous-knowledge-extraction/>

**9.** FalkorDB Knowledge Graph Construction Guide.
<https://www.falkordb.com/blog/how-to-build-a-knowledge-graph/>

**Weak Signal Detection & Anomaly Detection**

**10.** Bouktaib, A., Fennan, A. (2021). \"A Framework for Weak Signal
Detection in Competitive Intelligence using Semantic Clustering
Algorithms.\" IJACSA, 12(12).
<https://thesai.org/Downloads/Volume12No12/Paper_71-A_Framework_for_Weak_Signal_Detection_in_Competitive_Intelligence.pdf>

**11.** Amazon Science (2023). \"Real-time anomaly detection under
distribution drift.\"
<https://www.amazon.science/blog/real-time-anomaly-detection-under-distribution-drift>

**12.** ADKGD (2025). \"Anomaly Detection in Knowledge Graphs with
Dual-Channel Training.\" arXiv:2501.07078.
<https://arxiv.org/html/2501.07078v1>

**Cross-Domain Pattern Detection**

**13.** Gu, X., Krenn, M. (2025). \"Interesting Scientific Idea
Generation using Knowledge Graphs and LLMs.\" SciMuse.
<https://arxiv.org/abs/2405.17044>

**14.** Nature (2024). \"Modification and Completion of Geological
Structure Knowledge Graph Using Approximate Subgraph Matching.\"
<https://www.nature.com/articles/s41598-024-60618-1>

**SearXNG API**

**15.** SearXNG Search API Documentation.
<https://docs.searxng.org/dev/search_api.html>

**Amplified Partners Internal**

**16.** Bramley, E. + Claude (2026). PUDDING Technique Skill. Amplified
Partners.

**17.** Bramley, E. + Claude (2026). Mathematical Validation of the
Pudding Technique. Amplified Partners.

**18.** Bramley, E. + Claude (2026). Build Quality Framework v1.0.
Amplified Partners.

**19.** Bramley, E. + Claude (2026). Token Strategy and Research
Framework. Amplified Partners.

**20.** Bramley, E. + Claude (2026). Gap Analysis and Finite Lenses.
Amplified Partners.

**Attribution: Ewan Bramley (originator, system vision) ×
Claude/Perplexity (researcher, formaliser, architect)**

Fact %: 85 \| Confidence: High \| PUDDING: M.+.5.l

LBD: Swanson (1986) ABC Model
