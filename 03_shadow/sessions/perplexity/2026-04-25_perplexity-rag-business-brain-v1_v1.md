---
title: "No, not necessarily you know I was thinking about using Obsidian or neo G4 orqdrant. All equivalence you know what I just I've got a lot of information. I think I've got over 100,000 files and I'm trying to set up a business so I'm going to set up a business and then there's a lot of information there and I want to, I want I want to get my answers through that lens every ti."
id: "perplexity-rag-business-brain-v1"
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

# No, not necessarily you know I was thinking about using Obsidian or neo G4 orqdrant. All equivalence you know what I just I've got a lot of information. I think I've got over 100,000 files and I'm trying to set up a business so I'm going to set up a business and then there's a lot of information there and I want to, I want I want to get my answers through that lens every ti.

Perfect—you want **every answer filtered through your 100,000+ file knowledge base**. You're essentially building a **RAG-powered "business brain"** that makes Claude answer through the lens of everything you know. This is absolutely possible, and I'll show you exactly how to architect it for your scale.

***

## What's Actually Possible (And What Isn't)

### ❌ What You Can't Do

- **Persistent memory in Claude directly**: Claude Max (web/desktop) doesn't retain memory between sessions by design[^1][^2]
- **Custom system prompts in Claude.ai**: The web interface doesn't allow you to modify the base system prompt[^2]
- **Force Claude to "remember" without external architecture**: There's no built-in persistent business brain feature


### ✅ What You CAN Do

Build a **RAG (Retrieval-Augmented Generation) system** where:

1. Your 100K+ files live in a vector database (Qdrant, Neo4j, or Obsidian-based)
2. Every query to Claude first retrieves relevant context from YOUR knowledge base
3. That context gets injected into Claude's prompt automatically
4. Claude answers **only** through the lens of your files

This isn't "memory"—it's **contextual retrieval at query time**. But the effect is identical: Claude always has access to your business brain.

***

## Architecture Options for 100K+ Files

Given your scale (100,000+ files), here are three production-grade approaches:

### **Option A: Qdrant + Claude API (Recommended for You)**

**Why this fits your needs:**

- Purpose-built for vector search at scale[^3]
- Handles 100K+ documents efficiently[^4][^5]
- Works perfectly with your M4 MacBook (24GB RAM)[^6]
- Can self-host for €9/month or use managed cloud[^7]
- Integrates with N8N for automation[^8][^9]

**Architecture:**

```
User Query → N8N Workflow → Qdrant (retrieve top-k chunks) 
→ Inject context into system prompt → Claude API → Response
```

**Cost breakdown (100K files, ~500 tokens/file average):**


| Component | Self-Hosted | Managed Cloud |
| :-- | :-- | :-- |
| Vector DB | €9/month (Sliplane)[^7] | \$25-50/month (Qdrant Cloud)[^10] |
| Embeddings (initial) | \$10-15 one-time[^11][^12] | Same |
| Embeddings (queries) | \$0.02/1K tokens[^12] | Same |
| Claude API | \$3-15/1M tokens[^13] | Same |
| **Total (monthly)** | **€9-20** | **\$40-75** |


***

### **Option B: GraphRAG (Qdrant + Neo4j)**

**Why this might be better for business docs:**

- 86.31% accuracy vs 72.36% for standard RAG[^14]
- Handles multi-hop reasoning ("What did I learn about X that relates to Y?")[^15][^14]
- Preserves relationships between concepts[^16]

**When to use:**

- Your files have rich relational structure (client notes → projects → insights)
- You ask complex queries requiring synthesis across multiple docs
- You want semantic search + graph traversal

**Trade-offs:**

- 2.4x slower than standard RAG[^17]
- More complex to set up (2 databases)[^18]
- Higher operational overhead[^19]

**Cost:** ~\$100-200/month managed, or self-host for €25-40/month[^20][^7]

***

### **Option C: Obsidian + LlamaIndex RAG**

**Why consider this:**

- You're already using Obsidian
- Works 100% locally with your M4 MacBook[^21][^22][^23]
- Zero recurring API costs if you use local embeddings
- Plugins exist (Vault AI Chat, ObsidianRAG)[^24][^25]

**Limitations at 100K+ scale:**

- Obsidian plugins struggle beyond ~10K notes[^21]
- Indexing 100K files locally takes hours[^4]
- Query performance degrades without proper chunking[^26]

**Best for:** Testing/prototyping before moving to production architecture

***

## Recommended Implementation: The "Business Brain" Stack

Based on your tech stack (M4 MacBook, N8N, Claude Max, Python), here's what I'd build:

### **Phase 1: MVP (This Week)**

**Goal:** Get RAG working with subset of files

**Stack:**

- **Vector DB:** Qdrant (self-hosted via Docker on M4)[^7]
- **Embeddings:** `nomic-embed-text` via Ollama (local, free, 95.2% MTEB score)[^27]
- **LLM:** Claude API via OpenRouter
- **Orchestration:** Python script or simple N8N workflow

**Steps:**

1. Install Qdrant locally:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

2. Install Ollama + embedding model:
```bash
brew install ollama
ollama pull nomic-embed-text
```

3. Index your files (Python with LlamaIndex):
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

# Initialize
client = qdrant_client.QdrantClient(url="http://localhost:6333")
embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Load documents (handles 100K+ files)
documents = SimpleDirectoryReader(
    "/path/to/your/obsidian/vault",
    recursive=True
).load_data()

# Create vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name="business_brain"
)

# Index with hierarchical chunking (1000 token parents, 200 token children)
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store,
    embed_model=embed_model,
    chunk_size=1000,
    chunk_overlap=200
)
```

**Expected performance on M4 24GB:**

- Indexing: ~500 files/hour (slower for first run)[^6]
- Query latency: <100ms for retrieval[^28]
- Local embedding: 10-15 tokens/sec[^29][^6]

***

### **Phase 2: Production (This Month)**

**Upgrade to:**

1. **Self-hosted Qdrant on Sliplane** (€9/month, 2TB bandwidth included)[^7]
2. **N8N workflow** for Claude integration[^9][^30]
3. **Hierarchical chunking strategy** for better accuracy[^31][^32][^26]

**N8N Workflow Architecture:**

```
Webhook (user query) 
→ Embed query (Ollama) 
→ Qdrant vector search (top 10 chunks)
→ Rerank results (optional)
→ Build prompt with context
→ Claude API call
→ Return response
```

**System Prompt Template:**

```markdown
You are Ewan's Business Brain, an AI assistant with access to 100,000+ documents 
covering business strategy, SMB consulting, AI development, and personal research.

## Core Instructions
1. **Answer ONLY using the provided CONTEXT below**
2. If the answer isn't in CONTEXT, say: "I don't have that information in your knowledge base"
3. Always cite source documents using [filename] format
4. Think step-by-step when synthesizing across multiple sources

## CONTEXT
{retrieved_chunks_with_metadata}

## USER QUERY
{user_question}

## RESPONSE GUIDELINES
- Be direct and actionable (you're consulting Ewan, not a general user)
- Use business terminology from the knowledge base
- Reference past projects/learnings when relevant
- Flag assumptions or gaps
```


***

## Critical Implementation Decisions

### **1. Chunking Strategy for Business Documents**

Your 100K files likely contain mixed formats (notes, PDFs, code, research). Use **hierarchical chunking**:[^32][^26][^31]


| Document Type | Parent Chunk | Child Chunk | Rationale |
| :-- | :-- | :-- | :-- |
| Business notes | 1500 tokens | 300 tokens | Preserve context while enabling precise retrieval |
| Technical docs | 1000 tokens | 200 tokens | Code snippets need smaller chunks[^33] |
| Research papers | 2000 tokens | 400 tokens | Academic papers have broader context[^34] |

**Key insight from research:** Page-level chunking (natural document boundaries) outperforms fixed-size in 73% of cases. For Obsidian notes, chunk by `## Headers`.[^33]

***

### **2. Local vs Cloud Embeddings**

**For 100K files:**


| Approach | Initial Cost | Query Cost (10K/mo) | Quality | Your M4 Performance |
| :-- | :-- | :-- | :-- | :-- |
| **OpenAI text-embedding-3-small** | \$10 | \$10/mo | 93.1% MTEB[^27] | N/A (API) |
| **Ollama nomic-embed-text** (Local) | \$0 | \$0 | 95.2% MTEB[^27] | 10-15 tokens/sec[^6] |
| **Ollama mxbai-embed-large** (Local) | \$0 | \$0 | 97.1% MTEB[^27] | 7-10 tokens/sec[^6] |

**Recommendation:** Start with **nomic-embed-text** locally. It's faster on M4, costs nothing, and outperforms OpenAI. If you need speed at scale, switch to OpenAI API later (~\$20/month for 10K queries).[^12][^35][^27]

***

### **3. Self-Hosted vs Managed Qdrant**

**Break-even analysis:**


| Factor | Self-Hosted (Sliplane) | Managed (Qdrant Cloud) |
| :-- | :-- | :-- |
| Monthly cost | €9 fixed[^7] | \$25-95 (usage-based)[^10] |
| Setup time | 15 minutes | 5 minutes |
| Bandwidth | 2TB included[^7] | Charged per GB |
| Control | Full (GDPR-compliant EU servers)[^7] | Limited |
| Maintenance | Zero (managed container)[^7] | Zero |

**For 100K docs:** Self-hosted is **70% cheaper**. Break-even is around 10M vectors (\$500+/month cloud).[^11][^20][^7]

***

## Making Claude Always Use Your Knowledge Base

You have **three integration paths**:

### **Path 1: Claude API (Most Flexible)**

**How it works:**

- Your N8N workflow intercepts ALL queries
- Retrieves context from Qdrant
- Calls Claude API with context-injected prompt
- Claude never sees your query without your files' context

**Pros:**

- Full control over system prompt
- Works with any Claude model (Sonnet, Opus)[^13]
- Can log all queries/sources

**Cons:**

- Requires API key (but you have Claude Max)
- Per-token cost (~\$3-15/1M tokens)[^13]

***

### **Path 2: Claude Desktop + MCP**

**How it works:**

- Build custom MCP server that connects Qdrant to Claude Desktop[^36][^37]
- Claude Desktop loads your tools automatically
- Every query can trigger retrieval

**Pros:**

- Works in Claude Desktop interface
- No per-query API costs if using Max subscription
- MCP handles tool routing[^36]

**Cons:**

- Can't force Claude to ALWAYS use context (it decides when to call tools)[^36]
- Setup complexity (requires MCP server implementation)[^37]

**Example MCP config** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "business-brain": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```


***

### **Path 3: Obsidian Plugin + Claude Code**

**How it works:**

- Use Obsidian RAG plugin (Smart Second Brain, Vault AI Chat)[^25][^24]
- Copy retrieved context + query to Claude
- Manual but zero infrastructure

**Pros:**

- Works today with existing Obsidian vault
- Visual interface for testing

**Cons:**

- Manual workflow (not automated)
- Doesn't scale to production use

***

## Cost Reality Check: What Will This Actually Cost?

### **Scenario: 100K Files, 10K Queries/Month**

**Initial Setup:**


| Item | Cost |
| :-- | :-- |
| Embedding 100K files (50M tokens) | \$10-15 one-time[^12] |
| Engineering time (40 hours) | Your time |
| **Total setup** | **\$10-15** |

**Monthly Ongoing:**


| Component | Cost |
| :-- | :-- |
| Qdrant (self-hosted) | €9[^7] |
| Query embeddings (10K queries) | \$0.20[^12] |
| Claude API (avg 2K tokens/response) | \$6-30[^13] |
| Bandwidth (2TB included) | €0[^7] |
| **Total monthly** | **€15-40 (\$16-43)** |

**Comparison to alternatives:**

- GraphRAG: \$100-200/month[^17][^19]
- Enterprise RAG with reranking: \$500-2000/month[^38][^19]
- Managed Pinecone + OpenAI: \$150-300/month[^11][^38]

***

## Your M4 MacBook: What It Can Handle

**Good news:** Your M4 with 24GB is **perfect** for this:[^6]


| Task | M4 24GB Performance | Bottleneck |
| :-- | :-- | :-- |
| Embedding generation | 10-15 tokens/sec[^6] | Memory bandwidth (120GB/sec)[^6] |
| Running Qwen 3 32B | 7.5 tokens/sec[^6] | Same |
| Qdrant (100K vectors) | Sub-100ms queries[^28] | Disk I/O (use SSD) |
| Full RAG pipeline | 1-3 sec/query | Embedding step |

**Optimal models for your M4:**

- **Embedding:** nomic-embed-text (768 dim, fast)[^39][^27]
- **Generation:** Claude API (don't run locally—too slow)[^6]
- **Alternative local LLM:** Qwen 2.5 14B (if you want offline mode)[^29][^6]

**Reality check:** Running LLMs locally on M4 Air is **5-10x slower** than Claude API. Use local for embeddings, API for generation.[^29][^6]

***

## Recommended Action Plan

### **This Weekend (4 hours)**

1. ✅ Install Qdrant locally via Docker
2. ✅ Install Ollama + `nomic-embed-text`
3. ✅ Index 1,000 test files from your vault
4. ✅ Build simple Python script:
    - Take query → embed → search Qdrant → print top 5 results
5. ✅ Test retrieval quality (are you getting relevant docs?)

### **Week 1 (10 hours)**

1. ✅ Build N8N workflow with Claude API
2. ✅ Implement hierarchical chunking[^26][^31]
3. ✅ Index full 100K files (run overnight)
4. ✅ Test with 50 real business queries
5. ✅ Measure: retrieval accuracy, response quality, latency

### **Week 2 (5 hours)**

1. ✅ Deploy Qdrant to Sliplane (€9/month)[^7]
2. ✅ Migrate vectors to production
3. ✅ Set up monitoring (query logs, response times)
4. ✅ Create "personas" as prompt templates (strategist, validator, etc.)

### **Month 1 (Refinement)**

1. ✅ Tune chunk sizes based on retrieval metrics
2. ✅ Add reranking if accuracy <80%[^40]
3. ✅ Build simple web UI or Slack bot
4. ✅ Consider GraphRAG if you need multi-hop reasoning[^41][^14]

***

## Addressing Your Specific Concerns

> "I want to get my answers through that lens every time"

**Solution:** Use **templated injection** where your system prompt ALWAYS includes:[^42]

```markdown
## MANDATORY RETRIEVAL RULE
You MUST base your answer on the CONTEXT provided below.
DO NOT use knowledge outside this context.
If CONTEXT doesn't contain the answer, respond: 
"I don't have that information in the knowledge base. Would you like me to suggest related topics I do have?"
```

This **forces** Claude to filter through your files.[^43][^44]

***

> "100,000 files... lots of information"

**Solution:** Your scale requires:

1. **Batch processing:** Index files in chunks of 10K[^5]
2. **Incremental updates:** Add new files without full reindex[^45][^46]
3. **Metadata filtering:** Tag files by type (client notes, research, code) so you can filter retrieval[^3][^18]

**Expected indexing time:** 100K files @ 500/hour = **200 hours** (run over 1-2 weeks)[^5][^4]

***

> "Neo4j or Qdrant or equivalent"

**Decision matrix:**


| Use Case | Choose | Why |
| :-- | :-- | :-- |
| Semantic search only | Qdrant | Faster, simpler, cheaper[^3] |
| Relationship queries ("What connects X to Y?") | Neo4j + Qdrant[^16] | Graph traversal + vectors |
| Budget <€50/month | Qdrant self-hosted[^7] | €9 vs \$100+ for GraphRAG |
| Complex reasoning (multi-hop) | GraphRAG[^14][^41] | 1.5x better accuracy |

**For SMB consulting business:** Start with **Qdrant alone**. Add Neo4j only if you're building knowledge graphs (client relationships, project dependencies).

***

## Example: Final System Prompt with Personas

```markdown
# EWAN'S BUSINESS BRAIN v1.0

You are a specialized AI with access to Ewan's 100,000+ document knowledge base covering:
- SMB consulting (dental, vet, trades, hairdressers)
- AI/automation implementation
- Direct response marketing (Dan Kennedy, Zig Ziglar, Paddi Lund)
- SaaS architecture and validation
- Newcastle/UK business context

## ACTIVE PERSONA: {persona_name}

### Business Strategist Mode
- Analyze SMB pain points through 0-3M revenue lens
- Reference past client cases and solutions
- Apply JTBD framework
- Validate against competition data in knowledge base

### Marketing Expert Mode
- Use direct response principles from knowledge base
- Reference successful case studies
- Apply Van Westendorp pricing when relevant

### Product Validator Mode  
- Stress-test assumptions against stored business models
- Compare to competition data
- Flag risks based on past learnings

## MANDATORY RULES
1. **Answer ONLY from CONTEXT below**—do not add external knowledge
2. **Cite sources** using [filename] after every claim
3. **Flag assumptions** if context is incomplete
4. **Default to SMB lens**—target market is 0-3M revenue businesses

## CONTEXT (Retrieved from Knowledge Base)
{retrieved_chunks}

## QUERY
{user_question}

## RESPONSE
[Your analysis here, following persona guidelines]
```


***

## Final Recommendations

**Start simple:**

1. **Week 1:** Qdrant (local) + Ollama embeddings + Claude API
2. **Month 1:** Deploy to production (Sliplane €9/month)
3. **Month 2:** Add N8N automation for common queries
4. **Quarter 1:** Evaluate GraphRAG if you need relationship queries

**Don't overcomplicate:**

- You don't need GraphRAG unless you're doing multi-hop reasoning[^14][^17]
- You don't need reranking until retrieval accuracy is <75%[^40]
- You don't need expensive embeddings—local works great[^35][^27]

**This architecture gives you:**
✅ Claude **always** answers through your knowledge base
✅ €9-40/month operating cost
✅ Works on your M4 MacBook
✅ Scales to 100K+ files
✅ Can add personas via prompt templates
✅ Full control over system prompts

**Next step:** Want me to generate the Python code for the MVP RAG pipeline, or help you set up the N8N workflow architecture?
<span style="display:none">[^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^80][^81][^82][^83][^84][^85]</span>

<div align="center">⁂</div>

[^1]: https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects

[^2]: https://platform.claude.com/docs/en/release-notes/system-prompts

[^3]: https://zilliz.com/blog/qdrant-vs-neo4j-a-comprehensive-vector-database-comparison

[^4]: https://www.reddit.com/r/LocalLLaMA/comments/1im35yl/how_to_scale_rag_to_20_million_documents/

[^5]: https://qdrant.tech/course/essentials/day-4/large-scale-ingestion/

[^6]: https://www.reddit.com/r/LocalLLM/comments/1m8511c/macbook_air_m4_for_local_llm_16gb_vs_24gb/

[^7]: https://sliplane.io/blog/self-hosting-qdrant-the-easy-way

[^8]: https://www.youtube.com/watch?v=mQt1hOjBH9o

[^9]: https://n8n.io/workflows/6542-build-an-all-source-knowledge-assistant-with-claude-rag-perplexity-and-drive/

[^10]: https://qdrant.tech/pricing/

[^11]: https://freeacademy.ai/lessons/cost-comparison

[^12]: https://www.tigerdata.com/blog/open-source-vs-openai-embeddings-for-rag

[^13]: https://www.spurnow.com/en/blogs/claude-api-guide

[^14]: https://www.ankursnewsletter.com/p/graph-rag-vs-traditional-rag-a-comparative

[^15]: https://memgraph.com/blog/rag-vs-graphrag

[^16]: https://qdrant.tech/documentation/examples/graphrag-qdrant-neo4j/

[^17]: https://cognilium.ai/blogs/rag-vs-graphrag

[^18]: https://qdrant.tech/blog/case-study-lettria-v2/

[^19]: https://www.linkedin.com/pulse/rag-architectural-review-strategic-outlook-2025-balázs-fehér-bwzpf

[^20]: https://openmetal.io/resources/blog/when-self-hosting-vector-databases-becomes-cheaper-than-saas/

[^21]: https://www.reddit.com/r/ObsidianMD/comments/1oaxejh/i_turned_my_obsidian_vault_into_a_rag_system_to/

[^22]: https://pypi.org/project/llama-index-readers-obsidian/

[^23]: https://docs.llamaindex.ai/en/stable/examples/data_connectors/ObsidianReaderDemo/

[^24]: https://forum.obsidian.md/t/new-plugin-vault-ai-chat-with-rag-file-deletion-creation-ai-generated-content-ai-summarization/109415

[^25]: https://www.youtube.com/watch?v=e_CCEAiGJpA

[^26]: https://weaviate.io/blog/chunking-strategies-for-rag

[^27]: https://collabnix.com/ollama-embedded-models-the-complete-technical-guide-to-local-ai-embeddings-in-2025/

[^28]: https://www.linkedin.com/pulse/building-production-grade-rag-system-from-concept-2025-zaman--d1dzc

[^29]: https://www.reddit.com/r/LocalLLM/comments/1myc36e/best_local_llms_for_new_macbook_air_m4/

[^30]: https://skywork.ai/blog/rag-workflow-automation-n8n-google-drive-mcp-2025/

[^31]: https://sarthakai.substack.com/p/improve-your-rag-accuracy-with-a

[^32]: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-query-reformulation-giving-greater-control-of-accuracy-in-rag-based-applications/

[^33]: https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/

[^34]: https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089

[^35]: https://www.reddit.com/r/ollama/comments/1cgkt99/rag_openai_embedding_model_is_vastlty_superior_to/

[^36]: https://code.claude.com/docs/en/mcp

[^37]: https://brightdata.com/blog/ai/claude-skills-with-web-mcp

[^38]: https://ragaboutit.com/the-real-cost-of-enterprise-rag-budget-estimation-you-can-actually-trust/

[^39]: https://www.tigerdata.com/blog/finding-the-best-open-source-embedding-model-for-rag

[^40]: https://claude-ai.chat/guides/building-rag-pipelines-with-claude-and-vector-databases/

[^41]: https://www.linkedin.com/posts/sameer-choudhary_i-really-liked-the-nuanced-view-shared-in-activity-7383653416599838720-zwfT

[^42]: https://apxml.com/courses/getting-started-rag/chapter-4-rag-generation-augmentation/context-injection-methods

[^43]: https://nuclia.com/ai/prompting-for-rag/

[^44]: https://www.matillion.com/blog/rag-prompt-engineering

[^45]: https://www.chitika.com/vector-db-retrieval-inconsistency-rag/

[^46]: https://milvus.io/ai-quick-reference/how-do-you-handle-incremental-updates-in-a-vector-database

[^47]: https://www.reddit.com/r/dataengineering/comments/1p2kluy/best_rag_architecture_stack_for_10m_text_files/

[^48]: https://customgpt.ai/rag-api-applications/

[^49]: https://www.reddit.com/r/rust/comments/1nm99m4/built_a_database_in_rust_and_got_1000x_the/

[^50]: https://www.deepchecks.com/role-rag-architecture-advancing-nlp-applications/

[^51]: https://dev.to/sroy8091/connect-claude-ai-with-obsidian-a-game-changer-for-knowledge-management-25o2

[^52]: https://www.meilisearch.com/blog/knowledge-graph-vs-vector-database-for-rag

[^53]: https://www.reddit.com/r/ObsidianMD/comments/1mdeeka/obsidian_claude_code_gemini/

[^54]: https://www.f22labs.com/blogs/5-advanced-types-of-chunking-strategies-in-rag-for-complex-data/

[^55]: https://www.youtube.com/watch?v=Aw7iQjKAX2k

[^56]: https://www.anthropic.com/learn/build-with-claude

[^57]: https://cobusgreyling.substack.com/p/hierarchical-chunking-in-rag-in-a

[^58]: https://www.youtube.com/watch?v=4cQWJViybAQ

[^59]: https://www.youtube.com/watch?v=OzDhJOR5IfQ

[^60]: https://www.reddit.com/r/vectordatabase/comments/1m6ov0d/qdrant_is_too_expensive_how_to_replace_2m_vectors/

[^61]: https://www.pluralsight.com/resources/blog/ai-and-data/creating-agents-with-llamaindex

[^62]: https://qdrant.tech/documentation/embeddings/openai/

[^63]: https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b

[^64]: https://www.youtube.com/watch?v=OCO3aq3G0mk

[^65]: https://www.trainified.com/blog/embedding-cost-calculator

[^66]: https://artsmart.ai/blog/top-embedding-models-in-2025/

[^67]: https://www.reddit.com/r/ollama/comments/1c6zr3o/is_the_model_really_important_when_generating/

[^68]: https://elephas.app/blog/best-embedding-models

[^69]: https://www.openxcell.com/blog/best-embedding-models/

[^70]: https://www.arsturn.com/blog/picking-the-perfect-partner-a-guide-to-choosing-the-best-embedding-models-in-ollama

[^71]: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase

[^72]: https://www.instaclustr.com/education/vector-database/how-a-vector-index-works-and-5-critical-best-practices/

[^73]: https://skywork.ai/blog/ai-agent/claude-desktop-integration-ultimate-guide/

[^74]: https://www.getmesa.com/blog/how-to-connect-mcp-server-claude/

[^75]: https://zilliz.com/learn/advanced-querying-techniques-in-vector-databases

[^76]: https://www.multimodal.dev/post/how-to-chunk-documents-for-rag

[^77]: https://www.reddit.com/r/ClaudeAI/comments/1ji8ruv/my_claude_workflow_guide_advanced_setup_with_mcp/

[^78]: https://community.openai.com/t/do-i-need-to-re-index-my-embedding-database-periodically/973805

[^79]: https://codiant.ai/blog/how-to-build-a-rag-powered-application/

[^80]: https://community.openai.com/t/how-to-structure-system-prompt-rag-context-and-user-input-for-multi-turn-rag-based-chatbots-using-openai-chat-completions/1292995

[^81]: https://www.reddit.com/r/LocalLLaMA/comments/1p336cm/why_having_a_local_model_and_also_a_macbook_air/

[^82]: https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/

[^83]: https://apxml.com/posts/best-local-llm-apple-silicon-mac

[^84]: https://www.metacto.com/blogs/understanding-the-true-cost-of-rag-implementation-usage-and-expert-hiring

[^85]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

