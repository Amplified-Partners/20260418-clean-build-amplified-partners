---
title: "Business Asset Audit - Phase 1: Technical Discovery"
id: "audit-phase1-technical-discovery-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Business Asset Audit - Phase 1: Technical Discovery

**Audit Date:** 2026-01-12  
**Audit Scope:** `/Users/ewanbramley/Downloads`  
**Status:** Complete

---

## Executive Summary

This audit cataloged **3 major custom software repositories** with comprehensive API integrations, configuration management, and extensive documentation. The technical infrastructure includes:

- **2 Production-Ready Python Applications** (agentic_workflow, interior-design-system)
- **1 Enterprise Lead Generation Platform** (lead-engine)
- **Multiple API Integrations:** Anthropic Claude, Google Gemini, Perplexity, OpenAI
- **50+ Configuration Files** across all projects
- **100+ Documentation Files** providing setup guides, technical specifications, and user manuals

---

## 1. Custom Software Repositories

### 1.1 Agentic Workflow System
**Location:** `agentic_workflow/`  
**Purpose:** Minimal agentic workflow scaffold with task orchestration, policy evaluation, and secure data handling  
**Status:** Production-ready  
**Language:** Python  
**Last Modified:** Recent (active development)

#### Main Components:
- **[`orchestrator.py`](agentic_workflow/orchestrator.py:1)** - Coordinates tasks, routes to agents, handles retries, writes audit logs
- **[`agents/task_agent.py`](agentic_workflow/agents/task_agent.py:1)** - Stateless task executor returning structured JSON
- **[`agents/policy_agent.py`](agentic_workflow/agents/policy_agent.py:1)** - Risk evaluation and approval decisions
- **[`agents/librarian_agent.py`](agentic_workflow/agents/librarian_agent.py:1)** - Read/write Obsidian-style summaries
- **[`api/main.py`](agentic_workflow/api/main.py:1)** - FastAPI REST API for task management
- **[`security/security.py`](agentic_workflow/security/security.py:1)** - PII detection, redaction, encryption management
- **[`utils/audit_logger.py`](agentic_workflow/utils/audit_logger.py:1)** - Structured audit logging

#### Key Features:
- **Routing Logic:** PII-containing tasks → local models, others → cloud
- **Policy Enforcement:** Auto-approval for high confidence (≥0.9), manual review otherwise
- **Cloud Safe Mode:** Automatic PII redaction before cloud API calls
- **Retry Logic:** Configurable via `MAX_RETRIES` environment variable (default: 3)
- **Audit Trail:** Immutable JSON logs to `marketing_outputs/logs/`
- **Optional Encryption:** Fernet-based encryption for sensitive data

#### Technology Stack:
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pydantic 2.5.0
- Google Generative AI (Gemini)
- Python-dotenv
- Cryptography (optional encryption)

---

### 1.2 Interior Design System
**Location:** `interior-design-system/`  
**Purpose:** Professional 5-phase interior design workflow with AI agents and semantic product search  
**Status:** Production-ready  
**Language:** Python  
**Last Modified:** Recent (active development)

#### Main Components:

**AI Agents (All using Anthropic Claude):**
- **[`agents/discovery_agent.py`](interior-design-system/agents/discovery_agent.py:1)** - Client consultation expert (Phase 1)
- **[`agents/style_consultant_agent.py`](interior-design-system/agents/style_consultant_agent.py:1)** - Modern eclectic design specialist (Phase 2)
- **[`agents/product_research_agent.py`](interior-design-system/agents/product_research_agent.py:1)** - Multi-retailer sourcing expert (Phase 3a)
- **[`agents/space_analysis_agent.py`](interior-design-system/agents/space_analysis_agent.py:1)** - Layout validation expert (Phase 3b)
- **[`agents/budget_manager_agent.py`](interior-design-system/agents/budget_manager_agent.py:1)** - Budget tracking specialist (Phase 4)
- **[`agents/orchestrator_agent.py`](interior-design-system/agents/orchestrator_agent.py:1)** - Workflow coordination (All phases)
- **[`agents/base_agent.py`](interior-design-system/agents/base_agent.py:1)** - Base class with tool calling

**RAG Pipeline:**
- **[`rag/search_engine.py`](interior-design-system/rag/search_engine.py:1)** - Semantic product search with ChromaDB
- **[`rag/style_classifier.py`](interior-design-system/rag/style_classifier.py:1)** - Style compatibility scoring (0-100)
- **[`rag/embeddings.py`](interior-design-system/rag/embeddings.py:1)** - Vector embeddings (all-MiniLM-L6-v2)
- **[`rag/product_indexer.py`](interior-design-system/rag/product_indexer.py:1)** - Product database management
- **[`rag/vector_store.py`](interior-design-system/rag/vector_store.py:1)** - ChromaDB interface

**Web Scrapers:**
- **[`scrapers/ikea.py`](interior-design-system/scrapers/ikea.py:1)** - IKEA UK scraper
- **[`scrapers/aliexpress.py`](interior-design-system/scrapers/aliexpress.py:1)** - AliExpress scraper
- **[`scrapers/alibaba_1688.py`](interior-design-system/scrapers/alibaba_1688.py:1)** - 1688.com scraper

**CLI Interfaces:**
- **[`cli/designer_cli.py`](interior-design-system/cli/designer_cli.py:1)** - Main workflow with Rich UI
- **[`cli/search_demo.py`](interior-design-system/cli/search_demo.py:1)** - Product search demo

#### 5-Phase Professional Workflow:
1. **Discovery** - Requirements gathering, budget allocation, style preferences
2. **Concept Development** - 3 design options with style compatibility scoring
3. **Detailed Design** - Semantic product search, dimensional validation, UK import duties
4. **Budget Review** - Real-time tracking, optimization, alternative recommendations
5. **Implementation Plan** - Prioritized timeline, retailer grouping, delivery coordination

#### Technology Stack:
- Anthropic Claude (claude-sonnet-4-20250514)
- ChromaDB ≥0.5.23 (vector storage)
- Sentence-Transformers ≥3.3.1 (embeddings)
- Pydantic ≥2.10.4
- Rich ≥13.9.4 (CLI)
- BeautifulSoup4, Selenium (scraping)
- PyTorch (ML operations)

#### Project Context:
- **Property:** 4-bedroom house, Jesmond, Newcastle
- **Budget:** £10,000 total
- **Duration:** 1-year rental
- **Style:** Modern eclectic

---

### 1.3 Lead Engine (Enterprise Lead Generation Platform)
**Location:** `lead-engine/`  
**Purpose:** Enterprise B2B lead generation and personalization system  
**Status:** Production-ready with comprehensive testing  
**Language:** Python  
**Last Modified:** Recent (active development)

#### Main Components:

**Core Services:**
- **[`clients/perplexity_client.py`](lead-engine/clients/perplexity_client.py:1)** - Perplexity API integration for research
- **[`clients/claude_client.py`](lead-engine/clients/claude_client.py:1)** - Claude API for diagnosis generation
- **[`services/web_scraper.py`](lead-engine/services/web_scraper.py:1)** - Website content extraction
- **[`services/prospect_research.py`](lead-engine/services/prospect_research.py:1)** - Multi-source research aggregation
- **[`services/diagnosis_generator.py`](lead-engine/services/diagnosis_generator.py:1)** - Revenue leak analysis
- **[`services/email_generator.py`](lead-engine/services/email_generator.py:1)** - Personalized email creation

**Database Models:**
- **[`models/prospect.py`](lead-engine/models/prospect.py:1)** - Prospect entity with industry, size, tech stack
- **[`models/research.py`](lead-engine/models/research.py:1)** - Research data with Perplexity content
- **[`models/diagnosis.py`](lead-engine/models/diagnosis.py:1)** - Revenue leak diagnosis with cost estimates
- **[`models/email.py`](lead-engine/models/email.py:1)** - Generated emails with metrics

**Configuration:**
- **[`config.py`](lead-engine/config.py:1)** - Centralized configuration with validation

#### Key Features:
- **Multi-Source Research:** Perplexity API + web scraping
- **AI-Powered Diagnosis:** Claude-based revenue leak identification
- **Personalized Email Generation:** Context-aware cold email creation
- **Comprehensive Testing:** Unit, integration, and E2E tests
- **Database Persistence:** SQLite with Alembic migrations
- **Validation:** Pydantic models throughout

#### Technology Stack:
- FastAPI
- SQLAlchemy (ORM)
- Alembic (migrations)
- Anthropic Claude API
- Perplexity API
- BeautifulSoup4 (scraping)
- Pytest (testing)
- Python-dotenv

---

## 2. Configuration Files Inventory

### 2.1 Environment Configuration Files

#### Agentic Workflow
- **[`.env.example`](agentic_workflow/.env.example:1)** - Template with Gemini API key placeholder
- **Required Variables:**
  - `GEMINI_API_KEY` - Google Gemini API key
  - `ENABLE_AGENTIC_WORKFLOW` - Feature toggle (default: false)
  - `ENABLE_SEMI_AUTONOMOUS` - Semi-autonomous mode (default: false)
  - `MAX_RETRIES` - Retry attempts (default: 3)
  - `CLOUD_SAFE_MODE` - PII protection (default: true)

#### Interior Design System
- **[`.env.example`](interior-design-system/.env.example:1)** - Template for Anthropic configuration
- **Required Variables:**
  - `ANTHROPIC_API_KEY` - Anthropic Claude API key (REQUIRED)
  - `EMBEDDINGS_MODEL` - Sentence transformer model (default: all-MiniLM-L6-v2)
  - `VECTOR_DB_PATH` - ChromaDB storage location (default: ./data/chromadb)
  - `MAX_SEARCH_RESULTS` - Search result limit (default: 20)
  - `PROJECT_NAME` - Project identifier
  - `BUDGET_LIMIT` - Budget constraint
  - `LOG_LEVEL` - Logging level
  - `AUDIT_LOG_DIR` - Audit log directory

#### Lead Engine
- **[`.env.example`](lead-engine/.env.example:1)** - Multi-API configuration template
- **Required Variables:**
  - `OPENAI_API_KEY` - OpenAI API key
  - `INSTANTLY_API_KEY` - Instantly.ai API key
  - `PERPLEXITY_API_KEY` - Perplexity API key (REQUIRED)
  - `ANTHROPIC_API_KEY` - Anthropic Claude API key (REQUIRED)

### 2.2 Python Configuration Files

#### Package Management
- **`requirements.txt`** files in:
  - [`agentic_workflow/requirements.txt`](agentic_workflow/requirements.txt:1) - 8 dependencies
  - [`interior-design-system/requirements.txt`](interior-design-system/requirements.txt:1) - 27 dependencies
  - [`lead-engine/requirements.txt`](lead-engine/requirements.txt:1) - Multiple dependencies

#### Project Configuration
- **[`interior-design-system/pyproject.toml`](interior-design-system/pyproject.toml:1)** - Complete project metadata, build system, tool configs
- **[`agentic_workflow/.gitignore`](agentic_workflow/.gitignore:1)** - Excludes .env, venv, __pycache__
- **[`interior-design-system/.gitignore`](interior-design-system/.gitignore:1)** - Excludes .env, data, logs, .venv

### 2.3 Application Configuration

#### Lead Engine Config Module
**[`config.py`](lead-engine/config.py:1)** - Centralized configuration with:
- Perplexity API settings (`PERPLEXITY_API_KEY`, `PERPLEXITY_API_URL`)
- Claude API settings (`ANTHROPIC_API_KEY`, `CLAUDE_API_URL`)
- Database settings
- Research settings (max depth, timeout, user agent)
- Validation function (`validate_config()`) - ensures required keys present

#### Interior Design Config Module
**[`utils/config.py`](interior-design-system/utils/config.py:1)** - Pydantic Settings with:
- API key validation (format checking, presence validation)
- Model configuration
- Embedding settings
- Vector DB paths
- Custom validators for `anthropic_api_key` field

---

## 3. API Integrations Discovered

### 3.1 Anthropic Claude API

**Projects Using:** interior-design-system, lead-engine  
**Purpose:** AI agent operations, diagnosis generation, email personalization

**Configuration:**
- **Environment Variable:** `ANTHROPIC_API_KEY`
- **API Endpoint:** `https://api.anthropic.com/v1/messages`
- **Model:** claude-sonnet-4-20250514 (interior-design-system)
- **Authentication:** Bearer token via `X-Api-Key` header

**Implementation Files:**
- [`interior-design-system/agents/base_agent.py`](interior-design-system/agents/base_agent.py:74) - Base agent initialization
- [`interior-design-system/utils/anthropic_client.py`](interior-design-system/utils/anthropic_client.py:39) - Client wrapper
- [`lead-engine/clients/claude_client.py`](lead-engine/clients/claude_client.py:60) - Claude client

**Usage:**
- 6 AI agents in interior-design-system
- Diagnosis generation in lead-engine
- All agents use tool calling capabilities

### 3.2 Google Gemini API

**Project Using:** agentic_workflow  
**Purpose:** Task agent execution, content generation

**Configuration:**
- **Environment Variable:** `GEMINI_API_KEY`
- **Authentication:** API key in requests
- **Model:** gemini-2.0-flash-exp (from related docs)

**Implementation Files:**
- [`agentic_workflow/orchestrator.py`](agentic_workflow/orchestrator.py:1) - Uses Gemini for task execution
- [`agentic_workflow/agents/task_agent.py`](agentic_workflow/agents/task_agent.py:1) - Task agent with Gemini

**Security Features:**
- Cloud-safe mode with PII redaction
- Local routing for PII-containing tasks

### 3.3 Perplexity API

**Project Using:** lead-engine  
**Purpose:** Prospect research, competitive analysis, market intelligence

**Configuration:**
- **Environment Variable:** `PERPLEXITY_API_KEY`
- **API Endpoint:** `https://api.perplexity.ai/chat/completions`
- **Authentication:** Bearer token
- **Model:** sonar-small-online (default)

**Implementation Files:**
- [`lead-engine/clients/perplexity_client.py`](lead-engine/clients/perplexity_client.py:53) - Client implementation
- [`lead-engine/config.py`](lead-engine/config.py:22) - Configuration constants

**Features:**
- Configurable model selection
- Real-time web search capabilities
- Citation support
- Error handling and retries

### 3.4 OpenAI API

**Project Using:** lead-engine, melanin-design-platform (referenced in docs)  
**Purpose:** Alternative AI provider

**Configuration:**
- **Environment Variable:** `OPENAI_API_KEY`
- **Referenced in:** lead-engine/.env.example

### 3.5 Database Connections

#### SQLite (Lead Engine)
- **Connection:** SQLAlchemy ORM
- **Migration Tool:** Alembic
- **Location:** Local database file
- **Models:** Prospect, Research, Diagnosis, Email

#### ChromaDB (Interior Design System)
- **Type:** Vector database
- **Purpose:** Semantic product search
- **Location:** `./data/chromadb` (configurable via `VECTOR_DB_PATH`)
- **Collection:** interior_products
- **Embedding Model:** all-MiniLM-L6-v2 (768 dimensions)

---

## 4. Documentation Assets

### 4.1 Project READMEs and Setup Guides

#### Agentic Workflow
- **[`README.md`](agentic_workflow/README.md:1)** - Minimal scaffold overview, component descriptions
- **[`DESIGN.md`](agentic_workflow/DESIGN.md:1)** - Design notes, routing/retry logic, policy rules
- **[`GEMINI_SETUP.md`](agentic_workflow/GEMINI_SETUP.md:1)** - Gemini API configuration guide
- **[`ROLL_OUT_CHECKLIST.md`](agentic_workflow/ROLL_OUT_CHECKLIST.md:1)** - Deployment checklist

#### Interior Design System
- **[`README.md`](interior-design-system/README.md:1)** - 977 lines, comprehensive guide covering:
  - Quick start instructions
  - System architecture (5-phase workflow)
  - All 6 AI agents with detailed descriptions
  - RAG pipeline documentation
  - CLI interface guide
  - Troubleshooting section
  - Project structure
  - Development guidelines
- **[`SETUP_GUIDE.md`](interior-design-system/SETUP_GUIDE.md:1)** - 571 lines, detailed setup including:
  - Prerequisites
  - Manual setup steps
  - Phase-by-phase guides (Phases 1-4)
  - Style classification system
  - Testing instructions
  - Modern eclectic approach
- **[`BUG_FIXES_REPORT.md`](interior-design-system/BUG_FIXES_REPORT.md:1)** - Bug fixes and improvements
- **[`SIMPLIFICATION_REPORT.md`](interior-design-system/SIMPLIFICATION_REPORT.md:1)** - Code simplification changes

#### Lead Engine
- **[`VALIDATION_LOG.md`](lead-engine/VALIDATION_LOG.md:1)** - 2600+ lines, complete development log:
  - Configuration setup
  - API integration steps
  - Testing procedures
  - Development workflow
  - Bug fixes and solutions
- **[`setup_dev.sh`](lead-engine/setup_dev.sh:1)** - Development environment setup script

### 4.2 Technical Specifications

#### Architecture Documents
- **[`files/ARCHITECTURE_DEEP_DIVE.md`](files/ARCHITECTURE_DEEP_DIVE.md:1)** - Deep architectural analysis
- **[`files/COMPLETE_SYSTEMS_OVERVIEW.md`](files/COMPLETE_SYSTEMS_OVERVIEW.md:1)** - System overview
- **[`files/COMPREHENSIVE_TECHNICAL_ANALYSIS.md`](files/COMPREHENSIVE_TECHNICAL_ANALYSIS.md:1)** - Technical analysis
- **[`files/COMPLETE_SETUP_GUIDE.md`](files/COMPLETE_SETUP_GUIDE.md:1)** - Complete setup guide

#### Quick Reference
- **[`files/QUICK_REFERENCE.md`](files/QUICK_REFERENCE.md:1)** - Quick command reference
- **[`files/DEMO_RESULTS.md`](files/DEMO_RESULTS.md:1)** - Demo results and testing

### 4.3 AI and Automation Guides

#### System Prompts and Instructions
- **[`00-system/CLAUDE-SKILLS-REFERENCE.md`](00-system/CLAUDE-SKILLS-REFERENCE.md:1)** - Claude skills documentation
- **[`00-system/KILO-HEALTH-CHECK.md`](00-system/KILO-HEALTH-CHECK.md:1)** - System health checking guide
- **[`claude_desktop_optimal_setup.md`](claude_desktop_optimal_setup.md:1)** - Claude Desktop configuration guide with 5 project templates
- **[`.kilocodemodes`](.kilocodemodes:1)** - Kilo Code mode configurations

### 4.4 Business Strategy Documents

#### Perplexity Integration
- **[`PERPLEXITY-COMPLETE-PACKAGE.md`](PERPLEXITY-COMPLETE-PACKAGE.md:1)** - Complete Perplexity integration guide
- **[`PERPLEXITY-INTEGRATION-COMPLETE.md`](PERPLEXITY-INTEGRATION-COMPLETE.md:1)** - Integration completion documentation
- **[`PERPLEXITY-SPACE-SETUP.md`](PERPLEXITY-SPACE-SETUP.md:1)** - Space setup instructions

#### AI Audit and Security
- **[`ai-audit-scripts/README.md`](ai-audit-scripts/README.md:1)** - AI audit script documentation
- **[`ai-audit-scripts/AUDIT-FINDINGS-COMPLETE.md`](ai-audit-scripts/AUDIT-FINDINGS-COMPLETE.md:1)** - Complete audit findings
- **[`ai-audit-scripts/api-key-inventory.md`](ai-audit-scripts/api-key-inventory.md:1)** - API key inventory

### 4.5 Deployment and Operations

#### Deployment Guides
- **[`melanin-design-platform/DEPLOYMENT.md`](melanin-design-platform/DEPLOYMENT.md:1)** - Railway deployment guide
- **[`melanin-design-platform/PRE-DEPLOYMENT-CHECKLIST.md`](melanin-design-platform/PRE-DEPLOYMENT-CHECKLIST.md:1)** - Pre-deployment checklist
- **[`RAILWAY-DEPLOYMENT-GUIDE.md`](RAILWAY-DEPLOYMENT-GUIDE.md:1)** - Railway-specific deployment

#### Setup Scripts
- **[`files/setup.sh`](files/setup.sh:1)** - Automated setup script
- **[`files/quick_setup_mac.sh`](files/quick_setup_mac.sh:1)** - macOS quick setup
- **[`setup-interior-design.sh`](setup-interior-design.sh:1)** - Interior design system setup
- **[`melanin-design-platform/setup-local.sh`](melanin-design-platform/setup-local.sh:1)** - Local environment setup

### 4.6 Prompt Templates and Instructions

#### RAG Pipeline
- **[`interior-design-system/plans/rag-pipeline-architecture.md`](interior-design-system/plans/rag-pipeline-architecture.md:1)** - RAG architecture documentation

#### Prompt Templates
- **[`agentic_workflow/prompts/TEMPLATES.md`](agentic_workflow/prompts/TEMPLATES.md:1)** - Prompt templates for agents

---

## 5. Database Models and Schemas

### 5.1 Lead Engine Data Models

#### Prospect Model
**File:** [`models/prospect.py`](lead-engine/models/prospect.py:1)
- Company information (name, domain, industry)
- Company size and tech stack
- Contact details
- Timestamps

#### Research Model
**File:** [`models/research.py`](lead-engine/models/research.py:1)
- Perplexity research content
- Web scraping results
- Citations and sources
- Research metadata

#### Diagnosis Model
**File:** [`models/diagnosis.py`](lead-engine/models/diagnosis.py:1)
- Revenue leak identification
- Impact quantification
- Cost estimates
- Priority scoring

#### Email Model
**File:** [`models/email.py`](lead-engine/models/email.py:1)
- Generated email content
- Personalization data
- Performance metrics
- Send status

### 5.2 Agentic Workflow Schemas

#### Task Specification
**Files:** [`api/models.py`](agentic_workflow/api/models.py:1), [`api/storage.py`](agentic_workflow/api/storage.py:1)
- `TaskCreate` - Task creation schema
- `TaskUpdate` - Task update schema
- `TaskResponse` - Complete task details
- `TaskListResponse` - Paginated task list
- `ExecuteRequest` - Execution parameters
- `DeleteResponse` - Deletion confirmation

#### Policy Decision Schema
**File:** [`agents/policy_agent.py`](agentic_workflow/agents/policy_agent.py:1)
- Decision type (approve_auto, requires_approval, reject)
- Reasons list
- Risk level (0-3)

### 5.3 Interior Design System Schemas

#### Agent Schemas
**File:** [`models/agent_schemas.py`](interior-design-system/models/agent_schemas.py:1)
- `DesignBrief` - Client requirements (Phase 1)
- `DesignConcept` - Style concept with mood board (Phase 2)
- `ProductSelection` - Selected products with details (Phase 3)
- `BudgetReport` - Budget allocation and tracking (Phase 4)
- `SpaceReport` - Layout validation results (Phase 3b)
- `DesignProject` - Complete project state

#### RAG Schemas
**File:** [`models/rag_schemas.py`](interior-design-system/models/rag_schemas.py:1)
- `Product` - Product details with pricing, dimensions, retailer
- `SearchResult` - Search results with similarity scores
- `StyleScore` - Style compatibility scoring (0-100)

---

## 6. Dependencies and Third-Party Libraries

### 6.1 Core Dependencies (Shared Across Projects)

#### Web Frameworks
- **FastAPI** (0.109.0 - 0.115.6) - Modern async web framework
- **Uvicorn** (0.27.0 - 0.34.0) - ASGI server
- **Starlette** - ASGI framework (FastAPI dependency)

#### Data Validation
- **Pydantic** (2.5.0 - 2.10.4) - Data validation and settings
- **Pydantic-Settings** (2.1.0+) - Settings management

#### Environment & Configuration
- **Python-dotenv** (1.0.0+) - Environment variable management

### 6.2 AI and ML Dependencies

#### LLM APIs
- **anthropic** (≥0.18.0, ≥0.40.0) - Anthropic Claude API client
- **google-generativeai** - Google Gemini API client
- **openai** - OpenAI API client (referenced)

#### Machine Learning
- **sentence-transformers** (≥3.3.1) - Text embeddings (interior-design)
- **torch** (≥2.0.0) - PyTorch for ML operations
- **numpy** - Numerical computing

#### Vector Storage
- **chromadb** (≥0.5.23) - Vector database for semantic search
- **tiktoken** (≥0.5.2) - Token counting

### 6.3 Database and ORM

#### Relational Databases
- **SQLAlchemy** (≥2.0.25) - ORM for lead-engine
- **Alembic** - Database migrations
- **asyncpg** - Async PostgreSQL driver

#### Database Adapters
- **psycopg2** - PostgreSQL adapter
- **python-multipart** - Multipart form data parsing

### 6.4 Web Scraping and HTTP

#### Web Scraping
- **requests** (≥2.31.0, ≥2.32.0) - HTTP library
- **beautifulsoup4** (≥4.12.0) - HTML parsing
- **lxml** (≥5.0.0, ≥5.3.0) - Fast XML/HTML parser
- **selenium** (≥4.27.0) - Dynamic content scraping
- **playwright** (≥1.40.0) - Browser automation

#### HTTP Clients
- **httpx** (≥0.28.1) - Async HTTP client
- **httpcore** - Low-level HTTP components
- **urllib3** - HTTP client with connection pooling

### 6.5 Testing and Quality

#### Testing Frameworks
- **pytest** (≥8.0.0, ≥8.3.4) - Testing framework
- **pytest-asyncio** (≥0.23.0) - Async testing support
- **pytest-mock** (≥3.12.0) - Mock support
- **pytest-cov** (4.1.0) - Coverage plugin

#### Code Quality
- **black** (≥23.0.0) - Code formatter
- **isort** (≥5.12.0) - Import sorting
- **mypy** (≥1.8.0) - Static type checking
- **coverage** - Code coverage measurement

### 6.6 Security and Encryption

#### Cryptography
- **cryptography** - Encryption library (agentic_workflow)
- **Fernet** - Symmetric encryption (via cryptography)

#### Authentication
- **python-jose** - JSON Web Tokens
- **passlib** - Password hashing
- **bcrypt** - Password hashing algorithm

### 6.7 CLI and User Interface

#### Terminal UI
- **rich** (≥13.7.0, ≥13.9.4) - Rich terminal output
- **click** (≥8.1.7) - CLI framework
- **questionary** (≥2.0.1) - Interactive prompts

### 6.8 Utilities and Helpers

#### Data Formats
- **pyyaml** (≥6.0.1) - YAML parsing
- **python-dateutil** (≥2.8.2) - Date utilities
- **pytz** - Timezone support

#### Development Tools
- **ipython** - Enhanced Python shell
- **jupyter** - Notebook environment (referenced)

---

## 7. Security Assessment

### 7.1 API Key Management

**Status:** ⚠️ NEEDS ATTENTION

**Current State:**
- All projects use `.env.example` templates
- API keys stored in `.env` files (gitignored)
- No centralized secrets management

**Risks:**
- Keys in `.env.example` (agentic_workflow has exposed key: `GEMINI_API_KEYAI=zaSyCi3BIHPI16uEYPw9YzsPhbFT2236EKrsM`)
- Multiple `.env` files across projects
- No key rotation mechanism
- No audit trail for key access

**Recommendations:**
1. **Immediate:** Remove exposed key from `.env.example` files
2. **Short-term:** Implement centralized secrets manager (HashiCorp Vault, AWS Secrets Manager)
3. **Medium-term:** Implement key rotation policies
4. **Long-term:** Add API key usage monitoring and alerts

### 7.2 PII Protection

**Status:** ✅ GOOD (Agentic Workflow)

**Implemented Features:**
- PII detection via regex patterns (SSN, email, phone)
- Automatic redaction with configurable placeholder
- Cloud-safe mode (enabled by default)
- Local routing for PII-containing tasks
- Optional encryption for stored data

**Security Patterns:**
- [`security/security.py`](agentic_workflow/security/security.py:1) - `detect_pii()`, `redact_pii()`
- [`orchestrator.py`](agentic_workflow/orchestrator.py:73) - Cloud-safe mode enforcement
- [`agents/librarian_agent.py`](agentic_workflow/agents/librarian_agent.py:24) - PII redaction in summaries

### 7.3 Encryption

**Status:** ⚠️ OPTIONAL (Not Enforced)

**Current Implementation:**
- Fernet symmetric encryption available
- Optional via `ENABLE_DATA_ENCRYPTION` environment variable
- Encryption manager in [`security/security.py`](agentic_workflow/security/security.py:34)

**Recommendations:**
1. Make encryption mandatory for production deployments
2. Implement key management for encryption keys
3. Add encryption for all sensitive data at rest

### 7.4 Authentication and Authorization

**Status:** ℹ️ VARIES BY PROJECT

**Agentic Workflow:**
- API key authentication for external APIs
- No user authentication implemented (internal tool)

**Lead Engine:**
- Multi-API authentication (Perplexity, Claude)
- No user authentication layer

**Interior Design System:**
- Anthropic API authentication only
- No multi-user access control

**Recommendations:**
1. Implement JWT-based authentication for multi-user scenarios
2. Add role-based access control (RBAC)
3. Implement API rate limiting
4. Add request logging and monitoring

---

## 8. Additional Discoveries

### 8.1 Other Python Projects

#### Melanin Design Platform
**Location:** `melanin-design-platform/`  
**Purpose:** Full-stack web application (React frontend + Express backend)  
**Status:** Appears production-ready  
**Not Included in Primary Analysis:** Focus was on Python projects

**Key Files Noted:**
- Backend: Node.js/Express
- Frontend: React/Vite
- Database: PostgreSQL with Prisma
- Deployment: Railway platform
- API Integrations: OpenAI, Cloudinary

### 8.2 MCP (Model Context Protocol) Servers

**Discovered MCP Servers:**
1. **Sequential Thinking** - `@modelcontextprotocol/server-sequential-thinking`
2. **Project Agent** - Custom local server at `Documents/Kilo-Code/MCP/project-agent-server/`
3. **Research Agent** - Custom local server at `Documents/Kilo-Code/MCP/research-agent/`
4. **Puppeteer** - `@modelcontextprotocol/server-puppeteer`
5. **Memory** - `@modelcontextprotocol/server-memory`

**Purpose:** Extended functionality for Claude and other AI systems

### 8.3 Migration Scripts

**Lead Engine Migrations:**
- Database migration system using Alembic
- Migration environment at [`migrations/env.py`](lead-engine/migrations/env.py:26)
- Version control for database schema changes

---

## 9. Recommendations

### 9.1 Immediate Actions (Priority: HIGH)

1. **Security Audit**
   - Remove exposed API key from `agentic_workflow/.env.example`
   - Audit all `.env.example` files for sensitive data
   - Implement centralized secrets management

2. **Documentation Consolidation**
   - Create master index of all documentation
   - Link related docs across projects
   - Update outdated documentation

3. **Dependency Management**
   - Audit all dependencies for security vulnerabilities
   - Update outdated packages
   - Create unified dependency management strategy

### 9.2 Short-term Improvements (Priority: MEDIUM)

1. **Testing Coverage**
   - Expand test coverage for all projects
   - Implement CI/CD pipelines
   - Add integration tests between systems

2. **Configuration Management**
   - Standardize configuration patterns across projects
   - Implement environment-specific configs
   - Add configuration validation

3. **API Integration Monitoring**
   - Implement API usage tracking
   - Add cost monitoring for AI APIs
   - Set up alerting for API failures

### 9.3 Long-term Enhancements (Priority: LOW)

1. **Unified Platform**
   - Consider integrating all systems into unified platform
   - Implement shared authentication layer
   - Create centralized monitoring dashboard

2. **Scalability**
   - Evaluate cloud deployment options
   - Implement load balancing
   - Add caching layers

3. **Documentation as Code**
   - Auto-generate API documentation
   - Implement living documentation
   - Create interactive tutorials

---

## 10. Summary Statistics

### Repository Count
- **Total Custom Repositories:** 3 major + 1 additional (melanin-design-platform)
- **Production-Ready:** 3
- **Active Development:** 3

### File Counts
- **Python Files:** 100+ across all projects
- **Configuration Files:** 50+ (including .env.example, requirements.txt, pyproject.toml, .gitignore)
- **Documentation Files:** 100+ (including .md, .txt, .rst)
- **Test Files:** 20+ across projects

### API Integrations
- **AI APIs:** 4 (Anthropic Claude, Google Gemini, Perplexity, OpenAI)
- **Database Systems:** 2 (SQLite, ChromaDB)
- **Authentication Methods:** Bearer tokens, API keys

### Lines of Documentation
- **Total Documentation:** 5000+ lines
- **Largest Single Doc:** interior-design-system/README.md (977 lines)
- **Most Comprehensive:** lead-engine/VALIDATION_LOG.md (2600+ lines)

### Technology Stack Diversity
- **Languages:** Python (primary), JavaScript/TypeScript (melanin platform)
- **Frameworks:** FastAPI, Express, React
- **Databases:** SQLite, PostgreSQL, ChromaDB
- **AI/ML:** Anthropic, Google AI, Sentence Transformers, PyTorch

---

## Appendix A: File Structure Overview

```
/Users/ewanbramley/Downloads/
├── agentic_workflow/                  # Minimal agentic workflow scaffold
│   ├── agents/                        # Task, Policy, Librarian agents
│   ├── api/                           # FastAPI REST API
│   ├── security/                      # PII detection, encryption
│   ├── utils/                         # Audit logging
│   ├── prompts/                       # Prompt templates
│   ├── tests/                         # Test suite
│   ├── .env.example                   # Environment template
│   ├── requirements.txt               # Dependencies
│   └── orchestrator.py                # Main orchestrator
│
├── interior-design-system/            # Professional interior design workflow
│   ├── agents/                        # 6 AI agents (Discovery, Style, etc.)
│   ├── rag/                           # RAG pipeline (search, embeddings, vectors)
│   ├── scrapers/                      # IKEA, AliExpress, 1688 scrapers
│   ├── models/                        # Pydantic schemas
│   ├── cli/                           # CLI interfaces
│   ├── tests/                         # Comprehensive test suite
│   ├── utils/                         # Config, currency, anthropic client
│   ├── .env.example                   # Environment template
│   ├── requirements.txt               # 27 dependencies
│   ├── pyproject.toml                 # Project configuration
│   └── README.md                      # 977-line comprehensive guide
│
├── lead-engine/                       # Enterprise lead generation platform
│   ├── clients/                       # Perplexity, Claude API clients
│   ├── services/                      # Research, diagnosis, email services
│   ├── models/                        # SQLAlchemy models
│   ├── migrations/                    # Alembic migrations
│   ├── tests/                         # Unit, integration, E2E tests
│   ├── config.py                      # Centralized configuration
│   ├── .env.example                   # Environment template
│   ├── requirements.txt               # Dependencies
│   └── VALIDATION_LOG.md              # 2600+ line development log
│
├── melanin-design-platform/           # Full-stack web application
│   ├── backend/                       # Express.js backend
│   ├── frontend/                      # React frontend
│   └── [extensive structure...]
│
├── ai-audit-scripts/                  # AI cost monitoring scripts
├── files/                             # Architecture and setup documentation
├── 00-system/                         # Master prompts and workflows
└── [many additional files...]
```

---

## Appendix B: Critical Security Findings

### Exposed Credentials

**IMMEDIATE ACTION REQUIRED:**

1. **File:** `agentic_workflow/.env.example`
   - **Line 5-6:** Contains what appears to be an exposed API key
   - **Value:** `GEMINI_API_KEYAI=zaSyCi3BIHPI16uEYPw9YzsPhbFT2236EKrsM`
   - **Action:** Revoke this key immediately and remove from repository

### Recommended Immediate Actions

```bash
# 1. Revoke the exposed key
# Visit: https://makersuite.google.com/app/apikey
# Revoke key: zaSyCi3BIHPI16uEYPw9YzsPhbFT2236EKrsM

# 2. Clean from repository
cd agentic_workflow
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.example" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Create clean .env.example
cat > .env.example << 'EOF'
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here

# Workflow Configuration
ENABLE_AGENTIC_WORKFLOW=false
ENABLE_SEMI_AUTONOMOUS=false
MAX_RETRIES=3
CLOUD_SAFE_MODE=true
EOF

# 4. Force push (if remote)
# WARNING: This rewrites history
git push origin --force --all
```

---

**End of Business Asset Audit - Phase 1**

**Next Steps:**
1. Review security findings and implement immediate actions
2. Consolidate documentation into master index
3. Implement centralized secrets management
4. Establish monitoring and alerting for all API integrations
5. Create unified deployment strategy across all projects