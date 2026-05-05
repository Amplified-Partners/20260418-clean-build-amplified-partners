---
title: "Baselayer Workspace Setup"
id: "workspace-setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Baselayer Workspace Setup

## Purpose
Centralized workspace for AI-driven development across all Baselayer projects.

## Structure
```
baselayer-workspace/
├── WORKSPACE-SETUP.md          # This file
├── BUSINESS-FACTORY-AGENT.md   # Main agent specification
├── .kilocode/                  # Kilo Code configuration
│   └── rules/                  # Workspace-wide rules
└── projects/                   # Symlinks to actual repos
    ├── baselayer-core/         → ~/Projects/baselayer-core
    ├── voice-ai/               → ~/Projects/voice-ai
    ├── quickformai/            → ~/Projects/quickformai
    └── ai-orchestrator/        → ~/Documents/ai-orchestrator
```

## Active Projects

### 1. baselayer-core
- **Purpose**: Core Covered AI v2 platform
- **Tech**: Python (FastAPI), React, PostgreSQL
- **Status**: Production

### 2. voice-ai
- **Purpose**: Voice AI calling system
- **Tech**: Python, Twilio, OpenAI
- **Status**: Active development

### 3. quickformai
- **Purpose**: Quick form builder
- **Tech**: Node.js, React
- **Status**: Active development

### 4. ai-orchestrator
- **Purpose**: Model routing layer (Claude/local)
- **Tech**: Python
- **Status**: Infrastructure - needs wiring

## Next Steps
1. ✅ Create workspace folder
2. ⏳ Create project symlinks
3. ⏳ Add CLAUDE.md to each project
4. ⏳ Configure Kilo Code indexing
5. ⏳ Install local models (Ollama)
6. ⏳ Wire AI Orchestrator

## Kilo Code Indexing
- **Embedder**: OpenAI (text-embedding-3-small)
- **Vector Store**: Qdrant (local Docker)
- **Command**: `docker run -p 6333:6333 qdrant/qdrant`

## Local Models Setup
See: `~/Documents/Knowledge/00-system/LOCAL-MODELS-SETUP.md`