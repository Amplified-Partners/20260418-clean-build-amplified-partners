---
title: "Intelligence Monitoring System - Complete Documentation"
id: "tech-intelligence-monitoring-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Intelligence Monitoring System - Complete Documentation

**Created:** January 2026  
**Author:** Kilo Code AI Assistant  
**Status:** Implementation Ready

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [File Structure](#file-structure)
4. [Components](#components)
5. [Configuration](#configuration)
6. [Setup Instructions](#setup-instructions)
7. [Security Notes](#security-notes)
8. [Usage](#usage)
9. [Troubleshooting](#troubleshooting)

---

## Executive Summary

The **Intelligence Monitoring System** is an automated 24/7 monitoring solution designed for Byker Business Help AI, a Newcastle-based consultancy serving UK SMBs with £0-3M revenue.

### Purpose

Automatically monitor markets, competitors, and technology trends relevant to:
- **Target Industries:** Dental practices, veterinary clinics, salons, gyms, tradespeople, professional services
- **Core Offerings:** AI phone systems, marketing automation, business process automation
- **Geographic Focus:** UK SMB market with emphasis on Newcastle & North East England

### Key Features

- **Daily Automated Scans:** Runs at 6am via macOS launchd
- **Multi-Source Monitoring:** GitHub, Reddit, Substack, web search
- **AI-Powered Scoring:** Claude scores findings on relevance, actionability, and strategic value
- **Multi-Storage:** Obsidian markdown, Qdrant vector database, Neo4j graph database
- **Email Alerts:** High-priority findings notification
- **Self-Healing:** Fallback heuristics when AI services unavailable

---

## System Architecture

```mermaid
flowchart TB
    subgraph Sources
        P[Perplexity API]
        G[GitHub]
        R[Reddit]
        S[Substack]
    end
    
    subgraph Processing
        PS[PerplexitySearcher]
        RS[RelevanceScorer]
        FT[Filter by Threshold]
    end
    
    subgraph Storage
        O[Obsidian]
        Q[Qdrant]
        N[Neo4j]
    end
    
    subgraph Notifications
        SMTP[SMTP Email]
    end
    
    P --> PS
    G --> PS
    R --> PS
    S --> PS
    
    PS --> RS
    RS --> FT
    FT --> O
    FT --> Q
    FT --> N
    FT --> SMTP
```

### Data Flow

1. **Search:** PerplexitySearcher queries configured topics across multiple sources
2. **Score:** RelevanceScorer uses Claude AI to evaluate each result
3. **Filter:** Results below threshold (0.7) are discarded
4. **Store:** Valid results written to Obsidian, Qdrant, and Neo4j
5. **Alert:** High-priority findings trigger email notifications

---

## File Structure

```
~/principles-system/
├── config/
│   └── monitoring_topics.yaml     # Topic definitions & thresholds
├── processors/
│   ├── __init__.py
│   └── relevance_scorer.py        # AI-powered scoring engine
├── watchers/
│   ├── __init__.py
│   └── intelligence_watcher.py    # Main orchestrator
├── logs/                          # Service logs
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore
├── orchestrator.py                # Service entry point
├── run_once.sh                    # Test script
├── start_service.sh               # Service script
└── README.md                      # Quick start guide
```

---

## Components

### 1. PerplexitySearcher

**Purpose:** Web search via Perplexity API

**Features:**
- Uses `llama-3.1-sonar-large-128k-online` model
- Configurable time range and max results
- Rate limiting and error handling

**Key Methods:**
```python
async def search(query: str, time_range: str = "week", max_results: int = 10) -> list[SearchResult]
```

### 2. RelevanceScorer

**Purpose:** AI-powered scoring of intelligence results

**Scoring Dimensions:**
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Relevance | 40% | How relevant to our business context |
| Actionability | 35% | How actionable the insight is |
| Strategic Value | 25% | Long-term strategic importance |

**Business Context:**
```
Byker Business Help AI - Newcastle-based company serving UK SMBs 
with £0-3M revenue. Target clients: dental practices, veterinary 
clinics, salons, gyms, tradespeople, professional services.

Core offerings: AI phone systems, marketing automation, business 
process automation. Focus on practical, measurable ROI.
```

**Features:**
- Claude AI scoring with fallback heuristics
- Content caching (7-day TTL)
- Batch processing support
- Threshold filtering

**Key Methods:**
```python
async def score_result(title, snippet, url, source, use_cache=True) -> ScoredResult
async def score_batch(results: list[dict], min_score: float = 0.0) -> list[ScoredResult]
def filter_by_threshold(results: list[ScoredResult], threshold: float = 0.7) -> list[ScoredResult]
```

### 3. ObsidianWriter

**Purpose:** Saves intelligence updates to Obsidian vault

**Features:**
- Creates markdown notes with YAML frontmatter
- Daily summary combining all topics
- Structured format with scores and action items

**Note Format:**
```markdown
---
title: Intelligence Update - [Topic]
date: 2026-01-17T06:00:00Z
type: intelligence-update
results_count: 10
tags: [intelligence, topic-name]
---

# Intelligence Update: [Topic]

**Scanned:** 2026-01-17 06:00:00
**High-Priority Findings:** 5

## Findings

### 1. Result Title
**Score:** 0.85 | Relevance: 0.90 | Actionability: 0.80

**Source:** [Source](url)

[Snippet]

**Key Insight:** [AI-generated insight]

**Action Items:**
- Action 1
- Action 2
```

### 4. QdrantEmbedder

**Purpose:** Vector storage for semantic search

**Features:**
- Uses OpenAI `text-embedding-3-small`
- 1536-dimensional vectors
- Cosine similarity matching
- Full payload storage

**Collection:** `market_intelligence`

### 5. Neo4jLinker

**Purpose:** Knowledge graph relationships

**Node Types:**
- `Topic` - Monitored topics
- `IntelligenceUpdate` - Daily scan results
- `IntelligenceResult` - Individual findings

**Relationships:**
- `[:ABOUT_TOPIC]` - Update to topic
- `[:FROM_UPDATE]` - Result to update

### 6. NotificationService

**Purpose:** Email alerts for high-priority findings

**Features:**
- SMTP-based email
- Configurable threshold (default: 0.8)
- Limits to 5 results per email

### 7. IntelligenceWatcher

**Purpose:** Main orchestrator

**Features:**
- YAML configuration loading
- Topic scanning and processing
- Daily scheduler
- Graceful shutdown handling

**Key Methods:**
```python
def load_config() -> dict
async def scan_topic(topic_config: dict) -> list[ScoredResult]
def process_update(topic_name, results, timestamp)
async def run_scan()
def start()
def run_once()
def stop()
```

---

## Configuration

### monitoring_topics.yaml

```yaml
# Intelligence Monitoring Configuration

monitoring:
  enabled: true
  frequency: "daily"
  run_time: "06:00"
  timezone: "Europe/London"

# Topics to monitor with search queries
topics:
  - name: "AI Coding"
    query: "AI coding tools developments 2024"
    sources: ["GitHub", "Reddit"]
    priority: high
    
  - name: "RAG Workflows"
    query: "RAG retrieval augmented generation best practices"
    sources: ["GitHub", "Substack"]
    priority: high
    
  - name: "Kilo Code"
    query: "Kilo Code AI assistant updates"
    sources: ["GitHub", "Reddit"]
    priority: medium
    
  - name: "Obsidian"
    query: "Obsidian AI plugins automation workflows"
    sources: ["Reddit", "GitHub"]
    priority: medium
    
  - name: "Qdrant"
    query: "Qdrant vector database tutorials use cases"
    sources: ["GitHub", "Substack"]
    priority: medium
    
  - name: "Neo4j"
    query: "Neo4j graph database AI knowledge graphs"
    sources: ["GitHub", "Substack"]
    priority: medium
    
  - name: "Automation"
    query: "business automation AI workflows SMB"
    sources: ["Reddit", "Substack"]
    priority: high

# Data storage configuration
obsidian:
  vault_path: "/Users/ewanbramley/vault"
  folder: "work-covered-ai/Intelligence"

qdrant:
  host: "localhost"
  port: 6333
  collection: "market_intelligence"

neo4j:
  uri: "bolt://localhost:7687"

# Scoring thresholds
filters:
  relevance_threshold: 0.7
  max_results_per_topic: 10
```

### Environment Variables (.env)

```bash
# ⚠️ GET NEW PERPLEXITY KEY - OLD ONE WAS EXPOSED!
PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Anthropic API for scoring
ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# OpenAI for embeddings
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Neo4j Database
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your_neo4j_password"

# Qdrant Vector Database
QDRANT_HOST="localhost"
QDRANT_PORT=6333

# SMTP for email notifications (optional)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
NOTIFICATION_EMAIL="your_email@gmail.com"
```

---

## Setup Instructions

### Step 1: Create Directory Structure

```bash
mkdir -p ~/principles-system/{config,processors,watchers,logs}
```

### Step 2: Create Files

Copy the following files to their locations:

1. `requirements.txt` → `~/principles-system/requirements.txt`
2. `.env.example` → `~/principles-system/.env.example`
3. `config/monitoring_topics.yaml` → `~/principles-system/config/monitoring_topics.yaml`
4. `processors/__init__.py` → `~/principles-system/processors/__init__.py`
5. `processors/relevance_scorer.py` → `~/principles-system/processors/relevance_scorer.py`
6. `watchers/__init__.py` → `~/principles-system/watchers/__init__.py`
7. `watchers/intelligence_watcher.py` → `~/principles-system/watchers/intelligence_watcher.py`
8. `orchestrator.py` → `~/principles-system/orchestrator.py`
9. `run_once.sh` → `~/principles-system/run_once.sh`
10. `start_service.sh` → `~/principles-system/start_service.sh`
11. `.gitignore` → `~/principles-system/.gitignore`
12. `README.md` → `~/principles-system/README.md`

### Step 3: Install Dependencies

```bash
cd ~/principles-system
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Step 5: Create Obsidian Folder

```bash
mkdir -p /Users/ewanbramley/vault/work-covered-ai/Intelligence
```

### Step 6: Make Scripts Executable

```bash
chmod +x run_once.sh start_service.sh
```

### Step 7: Test Run

```bash
./run_once.sh
```

Check `logs/` for output and verify:
- Obsidian notes created in vault
- Logs show successful scans
- No errors in output

### Step 8: Enable 24/7 Service

```bash
# Copy launchd plist
cp ~/principles-system/com.byker.intelligence-watcher.plist ~/Library/LaunchAgents/

# Load the service
launchctl load ~/Library/LaunchAgents/com.byker.intelligence-watcher.plist

# Start immediately
launchctl start com.byker.intelligence-watcher

# Check status
launchctl list | grep intelligence
```

---

## Security Notes

### ⚠️ CRITICAL: Revoke Exposed API Key

The Perplexity API key `REDACTED_PERPLEXITY_API_KEY` was exposed in chat history. **This is a security risk.**

**Action required:**
1. Go to https://www.perplexity.ai/api
2. Delete the exposed key
3. Generate a new key
4. Update `.env` with the new key

This key should be treated as compromised even if you haven't seen misuse.

### Security Best Practices

- Never commit `.env` to git
- Rotate API keys quarterly
- Use environment variables for all secrets
- Review logs regularly for suspicious activity

---

## Usage

### Run Single Scan (Testing)

```bash
cd ~/principles-system
./run_once.sh
```

### Start Service (24/7)

```bash
cd ~/principles-system
./start_service.sh
```

### View Logs

```bash
# Real-time log viewing
tail -f ~/principles-system/logs/intelligence.log

# Check for errors
grep -i error ~/principles-system/logs/intelligence.log
```

### Service Management

```bash
# Stop service
launchctl stop com.byker.intelligence-watcher

# Start service
launchctl start com.byker.intelligence-watcher

# Restart service
launchctl stop com.byker.intelligence-watcher
launchctl start com.byker.intelligence-watcher

# Unload service
launchctl unload ~/Library/LaunchAgents/com.byker.intelligence-watcher.plist
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
tail -f ~/principles-system/logs/stderr.log

# Check launchd status
launchctl list | grep intelligence

# Verify permissions
ls -la ~/principles-system/*.sh
```

### No Results from Search

- Verify Perplexity API key in `.env`
- Check API quota at perplexity.ai/api
- Review `logs/intelligence.log` for errors
- Test API key manually with curl

### Neo4j Connection Failed

- Ensure Neo4j Desktop is running
- Check connection URI in `.env`
- Verify Neo4j credentials
- Check Neo4j is on default port 7687

### Qdrant Connection Failed

- Ensure Qdrant is running
- Check host and port in config
- Verify Qdrant is on default port 6333

### Email Notifications Not Working

- Verify SMTP settings in `.env`
- Check Gmail app password (not regular password)
- Verify "Less secure apps" is enabled or use app password
- Check spam folder

### High Memory Usage

- Reduce `max_results_per_topic` in config
- Decrease number of monitored topics
- Clear old Obsidian notes
- Restart service periodically

---

## API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| Perplexity | Web search | perplexity.ai/api |
| Anthropic | AI scoring | anthropic.com/api |
| OpenAI | Vector embeddings | platform.openai.com/api-keys |
| Neo4j | Graph database | neo4j.com/cloud/aura |
| Gmail (optional) | Email alerts | myaccount.google.com/apppasswords |

---

## Success Criteria

- [ ] System runs without errors
- [ ] Daily Obsidian notes appear in vault/work-covered-ai/Intelligence/
- [ ] Logs show successful scans
- [ ] Service survives Mac restart
- [ ] Email notifications received for high-priority findings

---

## Maintenance

### Weekly

- Review high-priority findings
- Check logs for errors
- Verify Obsidian notes are being created

### Monthly

- Rotate API keys
- Review and update monitored topics
- Clean up old Obsidian notes
- Check storage usage

### Quarterly

- Full security audit
- Review and update business context
- Evaluate new monitoring sources
- Performance optimization

---

## Support

For issues or questions:

1. Check logs in `~/principles-system/logs/`
2. Review troubleshooting section above
3. Check Obsidian notes for error details
4. Verify all API keys are valid and have quota

---

## Appendix: File Contents

### requirements.txt

```txt
# Intelligence Monitoring System Dependencies

# AI and API Clients
anthropic>=0.40.0
openai>=1.60.0
httpx>=0.28.0

# Database Clients
qdrant-client>=1.14.0
neo4j>=5.24.0

# Utilities
pyyaml>=6.0.2
tenacity>=8.5.0
python-dotenv>=1.0.1
```

### .env.example

```bash
# Copy this to .env and fill in your values

# ⚠️ GET NEW PERPLEXITY KEY - OLD ONE WAS EXPOSED!
PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Anthropic API for scoring
ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# OpenAI for embeddings
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Neo4j Database
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your_neo4j_password"

# Qdrant Vector Database
QDRANT_HOST="localhost"
QDRANT_PORT=6333

# SMTP for email notifications (optional)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
NOTIFICATION_EMAIL="your_email@gmail.com"
```

### launchd plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.byker.intelligence-watcher</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/ewanbramley/principles-system</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/ewanbramley/principles-system/start_service.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/ewanbramley/principles-system/logs/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/ewanbramley/principles-system/logs/stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Next Review:** April 2026
