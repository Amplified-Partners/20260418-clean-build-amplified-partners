---
title: "🧠 Knowledge Graph Integration Guide"
id: "knowledge-graph-setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# 🧠 Knowledge Graph Integration Guide

## What This Does

Connects your Command Centre to **your cloud infrastructure**:

- **Pinecone** → Stores vector embeddings of every task
- **Neo4j** → Creates knowledge graph of relationships & patterns
- **Weaviate** → Enables semantic search across your work
- **Ollama** → Local embeddings (free, no API calls needed)

**Result:** System learns from every task and gets smarter automatically.

---

## Architecture

```
COMMAND CENTRE EXECUTION
        ↓
   Task Input
        ↓
┌─────────────────────────────────────┐
│ INTELLIGENT DECISION LAYER          │
│                                     │
│ 1. Search Pinecone                  │
│    "Find similar tasks"             │
│    ↓                                │
│    Get embeddings of past work      │
│                                     │
│ 2. Query Neo4j                      │
│    "What models worked?"            │
│    ↓                                │
│    Get success patterns             │
│                                     │
│ 3. Semantic Search Weaviate         │
│    "What's contextually similar?"   │
│    ↓                                │
│    Understand task context          │
└─────────────────────────────────────┘
        ↓
   RECOMMENDATION
        ↓
Execute Task
        ↓
┌─────────────────────────────────────┐
│ STORE OUTCOME                       │
│                                     │
│ 1. Add vector to Pinecone           │
│ 2. Create Neo4j nodes & links       │
│ 3. Add to Weaviate for search       │
│ 4. Update statistics                │
│ 5. Suggest rule improvements        │
└─────────────────────────────────────┘
```

---

## Setup (10 Minutes)

### Step 1: Get Cloud Credentials

**Pinecone:**
```bash
# Get from https://app.pinecone.io/
PINECONE_API_KEY=xxx-xxx-xxx
PINECONE_ENVIRONMENT=us-west1-gcp
```

**Neo4j:**
```bash
# Get from https://neo4j.com/cloud/aura/
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=xxxxxxxxxxxxx
```

**Weaviate:**
```bash
# Get from https://console.weaviate.cloud/
WEAVIATE_API_KEY=xxx-xxx-xxx
WEAVIATE_HOST=https://xxxxx.weaviate.network
```

### Step 2: Create .env File

```bash
cd ~/Projects/ai-command-centre

cat > .env << 'EOF'
# Pinecone
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=us-west1-gcp

# Neo4j
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# Weaviate
WEAVIATE_API_KEY=your-key-here
WEAVIATE_HOST=https://xxxxx.weaviate.network

# Ollama (local - no credentials needed)
OLLAMA_HOST=http://localhost:11434
EOF

chmod 600 .env  # Make it private
```

### Step 3: Install Dependencies

```bash
npm install axios dotenv
# neo4j-driver, @pinecone-database/pinecone optional
```

### Step 4: Test Connection

```bash
node knowledge-graph.js
```

**Expected output:**
```
✓ Pinecone connected
✓ Neo4j connected
✓ Weaviate connected
✓ Knowledge Graph initialized
✓ Task stored: req_test_001

Task Statistics:
{
  "total": 1,
  "successful": 1,
  "successRate": 100,
  "avgQuality": 0.94
}
```

---

## How It Works

### 1. **Every Task Gets Stored 3 Ways**

```
Task: "Write Node.js authentication module"
Result: Quality 0.94, Cost $0.038

PINECONE (Vector Store):
├── Embedding of task input
├── Model used: claude-3-7-sonnet
├── Quality: 0.94
├── Cost: $0.038
└── Timestamp

NEO4J (Knowledge Graph):
├── [Task] --[used_model]--> [Claude-3-7]
├── [Task] --[is_type]--> [CodeGeneration]
├── [CodeGeneration] --[avg_quality]--> 0.94
├── [CodeGeneration] --[success_rate]--> 100%
└── Relationships updated for future queries

WEAVIATE (Semantic Search):
├── Object with full task data
├── Semantic vectors for searching
├── Links to Neo4j relationships
└── Metadata for filtering
```

### 2. **Next Time Similar Task Arrives**

```
New task: "Build authentication system"

SEARCH:
1. Get embedding from Ollama
2. Search Pinecone for similar tasks
   → Finds 5 previous auth tasks
   
3. Query Neo4j for those tasks:
   "What models were used?"
   → Claude-3-7: 4/5 times, 0.96 quality
   → Claude-3-5: 1/5 times, 0.88 quality
   
4. Search Weaviate semantically
   → Confirms "authentication" context
   → Finds 3 similar client projects

RECOMMENDATION:
"Use Claude-3-7 (95% quality over 5 uses)"

EXECUTE:
→ Use Claude-3-7
→ Get quality 0.95
→ Store outcome
→ Pattern confirmed
```

### 3. **System Improves Over Time**

**Week 1:**
```
code_generation:
  - Claude-3-7: 0.91 quality
  - Haiku: 0.72 quality
  → Recommendation: Use Claude-3-7
```

**Week 2:**
```
code_generation (10 tasks):
  - Claude-3-7: 0.94 quality (consistent)
  - Haiku: 0.71 quality (consistently worse)
  → Suggestion: LOCK IN Claude-3-7
         AVOID Haiku
```

**Week 3:**
```
code_generation (20 tasks):
  - Claude-3-7: 0.93 quality (proven)
  - Quality gate now: minimum 0.93
  - Cost savings: $0.05 per task by avoiding worse models
  → RULE LOCKED
```

---

## Query Examples

### Get Best Model for Task Type

```javascript
const kg = new KnowledgeGraphManager();

// What's the best model for pricing tools?
const best = await kg.getBestModelForTaskType('pricing_tool');

// Result:
{
  model: 'claude-3-7-sonnet',
  timesUsed: 15,
  avgQuality: 0.92,
  totalCost: 2.34
}
```

### Find Similar Tasks

```javascript
// Find previous similar work
const similar = await kg.findSimilarTasks(
  'Build pricing calculator for SMBs',
  'code_generation'
);

// Result: Previous 5 similar tasks with:
// - What model was used
// - What quality was achieved
// - What it cost
```

### Get Statistics

```javascript
// How well are we doing on research tasks?
const stats = await kg.getTaskStatistics('research_synthesis');

// Result:
{
  total: 47,
  successful: 42,
  successRate: 89.36,
  avgQuality: 0.89
}
```

### Get Trending Models

```javascript
// What models are working best this week?
const trends = await kg.getTrendingPatterns(7);

// Result:
[
  { model: 'claude-3-7-sonnet', usage: 23, avgQuality: 0.94, totalCost: 15.2 },
  { model: 'claude-3-5-opus', usage: 12, avgQuality: 0.91, totalCost: 18.5 },
  { model: 'ollama-qwen', usage: 45, avgQuality: 0.85, totalCost: 0.0 }
]
```

### Suggest Rule Improvements

```javascript
// Should we change how we handle X?
const improvement = await kg.suggestRuleImprovement('pricing_tools');

// Result could be:
{
  suggestion: 'lock_rule',
  model: 'claude-3-7-sonnet',
  reason: 'Proven over 15 executions with 92.0% quality',
  evidence: {
    timesUsed: 15,
    avgQuality: 0.92,
    totalCost: 2.34,
    successRate: 100
  }
}
```

---

## Neo4j Queries (Direct)

### Find All Successful Patterns

```cypher
MATCH (type:TaskType)-[r:USED_BY]-(model:Model)
WHERE type.successRate > 85
RETURN type.name, model.name, type.successRate
ORDER BY type.successRate DESC
```

### Most Expensive Tasks

```cypher
MATCH (task:Task)-[:USED_MODEL]->(model:Model)
WHERE task.timestamp > datetime(NOW()) - duration({days: 7})
RETURN task.type, model.name, task.cost
ORDER BY task.cost DESC
LIMIT 10
```

### Quality Trend Over Time

```cypher
MATCH (type:TaskType {name: 'code_generation'})<-[:IS_TYPE]-(task:Task)
RETURN task.timestamp, task.quality, COUNT(*) as count
ORDER BY task.timestamp
```

### Model Comparison

```cypher
MATCH (model:Model)<-[:USED_MODEL]-(task:Task)-[:IS_TYPE]->(type:TaskType)
WITH model.name as model, 
     COUNT(*) as usage,
     AVG(task.quality) as avgQuality,
     MIN(task.quality) as minQuality,
     MAX(task.quality) as maxQuality
RETURN model, usage, avgQuality, minQuality, maxQuality
ORDER BY avgQuality DESC
```

---

## Cost Analysis

### Track Spending by Model

```javascript
// Which models are costing the most?
const spending = await kg.neo4j.run(`
  MATCH (task:Task)-[:USED_MODEL]->(model:Model)
  WHERE task.timestamp > datetime(NOW()) - duration({days: 30})
  RETURN model.name, COUNT(*) as usage, SUM(task.cost) as totalSpend
  ORDER BY totalSpend DESC
`);
```

### Cost vs Quality

```javascript
// Are we spending on quality?
const analysis = await kg.neo4j.run(`
  MATCH (model:Model)<-[:USED_MODEL]-(task:Task)
  RETURN model.name,
         AVG(task.quality) as quality,
         SUM(task.cost) as totalCost,
         SUM(task.cost) / COUNT(*) as costPerTask
  ORDER BY quality DESC
`);
```

---

## Integration with Command Centre

### Modified processRequest

```javascript
const { AICommandCentre } = require('./command-centre.js');
const { KnowledgeGraphManager } = require('./knowledge-graph.js');

class SmartCommandCentre {
  constructor() {
    this.centre = new AICommandCentre();
    this.kg = new KnowledgeGraphManager();
  }

  async processRequest(input, options = {}) {
    // 1. Find similar past work
    const similar = await this.kg.findSimilarTasks(input, options.taskType);
    
    // 2. Get recommendation
    const best = await this.kg.getBestModelForTaskType(options.taskType);
    if (best && best.avgQuality > 0.90) {
      options.recommendedModel = best.model;
    }
    
    // 3. Process
    const result = await this.centre.processRequest(input, options);
    
    // 4. Store in knowledge graph
    await this.kg.storeTaskExecution(result.metadata, {
      quality: 0.85,  // Your rating
      cost: result.metadata.cost,
      success: result.success
    });
    
    // 5. Return enhanced result
    return {
      ...result,
      insights: {
        similarTasks: similar.length,
        recommendedModel: best?.model,
        improvement: await this.kg.suggestRuleImprovement(options.taskType)
      }
    };
  }
}
```

---

## What Gets Stored Where

### Pinecone (Vector Search)
```
Index: ai-command-centre
├── Task embeddings (1536-dim vectors)
├── Model performance history
├── Client project context
└── Searchable by semantic similarity
```

### Neo4j (Knowledge Graph)
```
Nodes:
├── Task (with quality, cost, timestamp)
├── Model (with usage stats)
├── TaskType (with success rate)
├── Client (with project history)
└── Relationships track everything

Queries answer:
- Which model for X task?
- What's the success rate?
- Which client uses which models?
- What's the trend over time?
```

### Weaviate (Semantic Search)
```
Objects:
├── AITask (full task record)
├── ModelPerformance (stats)
├── ClientProject (project info)
└── Semantic vectors for context-aware search
```

---

## Privacy & Security

✅ **Your data stays in your cloud accounts**
- Pinecone: Your account
- Neo4j: Your database
- Weaviate: Your instance
- Ollama: Local, on your machine

✅ **No data sharing**
- Direct connections only
- API keys in .env (not committed)
- All processing is yours

✅ **Audit trails**
- Every decision logged
- Full traceability
- Historical patterns available

---

## Troubleshooting

### "Can't connect to Pinecone"
```bash
# Check API key
echo $PINECONE_API_KEY

# Test connection
curl https://<index>-<env>.pinecone.io/describe_index_stats \
  -H "Api-Key: $PINECONE_API_KEY"
```

### "Neo4j connection failed"
```bash
# Check URI and credentials
echo $NEO4J_URI
echo $NEO4J_USERNAME

# Test with neo4j-shell (if installed)
cypher-shell -a $NEO4J_URI -u $NEO4J_USERNAME
```

### "Ollama embedding failed"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve

# Pull embedding model:
ollama pull nomic-embed-text
```

---

## Next Steps

1. **Get credentials** from Pinecone, Neo4j, Weaviate
2. **Create .env file** with credentials
3. **Run knowledge-graph.js** to test
4. **Integrate with Command Centre**
5. **Start accumulating data** (1 week to see patterns)
6. **Review metrics** weekly
7. **Adjust rules** based on evidence

---

**Built for Ewan - Make your system learn and improve automatically**
