---
title: "Interior Design Multi-Agent System Architecture"
id: "interior-design-agent-system-architecture"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Interior Design Multi-Agent System Architecture

## Executive Summary

This system replicates a world-class interior designer's workflow using AI agents that research products, manage budgets, and coordinate design decisions. The system uses modern RAG (Retrieval-Augmented Generation) to search UK retailers and provides actionable recommendations within your £10k budget for a 1-year rental.

## Core Principles

1. **Process Over Speed**: Thorough research and validation at each step
2. **User Approval Gates**: No major decisions without your sign-off
3. **Actionable Outputs**: Real product links with prices, not generic suggestions
4. **Budget Discipline**: Constant tracking against £10k limit
5. **Professional Workflow**: Mirrors how top interior designers actually work

---

## System Architecture

### Agent Hierarchy

```
Main Orchestrator (Coordination Layer)
├── Discovery Agent (Phase 1: Requirements Gathering)
├── Space Analysis Agent (Phase 1: Space Understanding)
├── Style Consultant Agent (Phase 2: Concept Development)
├── Product Research Agent (Phase 3: Product Selection)
│   └── RAG Engine (Vector Search + Web Scraping)
├── Budget Manager Agent (All Phases: Financial Tracking)
└── Validation Layer (Quality Checks)
    ├── Price Validator
    ├── Style Consistency Checker
    ├── Dimension Compatibility Checker
    └── Delivery Feasibility Checker
```

### Professional Designer Workflow (5 Phases)

#### Phase 1: Discovery
- **Discovery Agent** gathers:
  - Style preferences (modern/traditional/minimalist/etc.)
  - Functional requirements per room
  - Lifestyle needs
  - Existing furniture to keep
  - Color preferences
  - Rental restrictions
- **Space Analysis Agent** processes:
  - Floor plans (if provided)
  - Room measurements
  - Natural light assessment
  - Architectural features
  - Storage needs

**Output**: Comprehensive client brief document
**User Approval**: ✓ Required before Phase 2

#### Phase 2: Concept Development
- **Style Consultant Agent** creates:
  - Mood boards for each room
  - Color palette recommendations
  - Style direction document
  - Initial product categories needed
  - Design principles guide

**Output**: Visual concept presentation with 2-3 style directions
**User Approval**: ✓ Required - choose preferred direction

#### Phase 3: Detailed Design
- **Product Research Agent** using RAG:
  - Searches UK retailers (IKEA, Dunelm, Wayfair UK, Made.com)
  - Semantic search for items matching style + budget
  - Generates product recommendations with:
    - Direct purchase links
    - Exact prices
    - Dimensions
    - Delivery times
    - Alternative options
- **Budget Manager Agent** tracks:
  - Running total per room
  - Category spending (furniture/lighting/textiles/etc.)
  - Alerts when approaching limits
  - Suggests cost-saving alternatives

**Output**: Room-by-room product lists with links and prices
**User Approval**: ✓ Required per room or as complete package

#### Phase 4: Budget Review
- **Budget Manager Agent** produces:
  - Final budget breakdown
  - Priority ranking of purchases
  - Phased buying strategy (immediate vs later)
  - Contingency recommendations

**Output**: Financial summary and purchasing plan
**User Approval**: ✓ Required before implementation

#### Phase 5: Implementation Planning
- **Coordination Agent** creates:
  - Purchase order sequence
  - Delivery schedule
  - Setup priorities
  - Contingency plans

**Output**: Actionable implementation timeline
**User Approval**: ✓ Final sign-off

---

## Technical Architecture

### Tech Stack

**Backend Framework**
- Python 3.11+
- FastAPI for REST API
- Pydantic for data validation

**AI & LLM**
- Anthropic Claude API (Sonnet 4)
- Structured outputs with JSON schemas
- Extended thinking for complex decisions

**RAG System**
- LangChain/LlamaIndex for orchestration
- sentence-transformers (all-MiniLM-L6-v2) for embeddings
- ChromaDB for vector storage
- Semantic search with metadata filtering

**Web Scraping**
- Playwright for dynamic content
- Beautiful Soup for parsing
- Firecrawl for clean extraction
- Rate limiting and retry logic

**Database**
- ChromaDB for product embeddings
- SQLite for project state
- JSON for agent communication logs

**Interface**
- CLI (Phase 1): Rich terminal UI
- Web UI (Optional Phase 2): React + FastAPI
- Markdown reports for deliverables

### Project Structure

```
interior-design-system/
├── README.md
├── requirements.txt
├── .env.example
├── pyproject.toml
├── main.py                    # Entry point
│
├── orchestrator/
│   ├── __init__.py
│   ├── main_orchestrator.py   # Coordinates all agents
│   ├── workflow_manager.py    # Manages phase transitions
│   └── approval_gate.py       # User approval checkpoints
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base class
│   ├── discovery_agent.py
│   ├── space_analysis_agent.py
│   ├── style_consultant_agent.py
│   ├── product_research_agent.py
│   ├── budget_manager_agent.py
│   └── coordination_agent.py
│
├── rag/
│   ├── __init__.py
│   ├── embeddings.py          # Vector embedding generation
│   ├── vector_store.py        # ChromaDB interface
│   ├── retriever.py           # Semantic search
│   └── reranker.py            # Result optimization
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── ikea_scraper.py
│   ├── dunelm_scraper.py
│   ├── wayfair_scraper.py
│   └── made_scraper.py
│
├── validators/
│   ├── __init__.py
│   ├── price_validator.py
│   ├── style_validator.py
│   ├── dimension_validator.py
│   └── delivery_validator.py
│
├── models/
│   ├── __init__.py
│   ├── schemas.py             # Pydantic models
│   ├── product.py
│   ├── room.py
│   └── project.py
│
├── api/
│   ├── __init__.py
│   ├── main.py                # FastAPI app
│   ├── routes.py
│   └── dependencies.py
│
├── cli/
│   ├── __init__.py
│   ├── interface.py           # Rich CLI
│   └── commands.py
│
├── prompts/
│   ├── __init__.py
│   ├── discovery_prompts.py
│   ├── style_prompts.py
│   ├── product_prompts.py
│   └── budget_prompts.py
│
├── utils/
│   ├── __init__.py
│   ├── anthropic_client.py    # Claude API wrapper
│   ├── audit_logger.py
│   ├── config.py
│   └── helpers.py
│
└── tests/
    ├── __init__.py
    ├── test_agents.py
    ├── test_rag.py
    ├── test_scrapers.py
    └── mocks/
        └── mock_responses.py
```

---

## Agent Specifications

### 1. Discovery Agent

**Role**: Gather comprehensive client requirements

**Input Schema**:
```python
{
  "mode": "interactive" | "questionnaire",
  "previous_responses": {...}
}
```

**Output Schema**:
```python
{
  "client_brief": {
    "style_preferences": [str],
    "room_priorities": [str],
    "budget_allocation": {room: float},
    "functional_requirements": {room: [str]},
    "constraints": [str],
    "timeline": str
  },
  "confidence_score": float
}
```

**Anthropic Prompt Pattern**:
```xml
<role>You are an expert interior design consultant conducting a client discovery session</role>
<task>Gather comprehensive requirements for furnishing a 4-bedroom house in Jesmond, Newcastle</task>
<constraints>
- Budget: £10,000 total
- Timeframe: 1 year rental
- Location: Jesmond Dene Rd, Newcastle
</constraints>
<output_format>Structured JSON with client_brief object</output_format>
```

### 2. Product Research Agent (with RAG)

**Role**: Find and recommend specific products from UK retailers

**RAG Pipeline**:
1. **Query Understanding**: Parse style requirements and constraints
2. **Vector Search**: Semantic search in product embedding database
3. **Metadata Filtering**: Price range, dimensions, delivery location
4. **Reranking**: Prioritize by style match + budget fit
5. **Validation**: Check availability, current pricing
6. **Output**: Top 3-5 options per item with justification

**Input Schema**:
```python
{
  "item_type": str,  # e.g., "sofa", "dining table"
  "style_direction": str,
  "dimensions": {
    "max_width": float,
    "max_depth": float,
    "max_height": float
  },
  "budget": {
    "min": float,
    "max": float
  },
  "room_context": str
}
```

**Output Schema**:
```python
{
  "recommendations": [
    {
      "product_name": str,
      "retailer": str,
      "price": float,
      "url": str,
      "dimensions": {...},
      "style_match_score": float,
      "justification": str,
      "delivery_estimate": str,
      "alternatives": [...]
    }
  ],
  "search_metadata": {
    "total_products_searched": int,
    "filters_applied": [...],
    "search_duration_ms": int
  }
}
```

### 3. Budget Manager Agent

**Role**: Track spending, enforce limits, suggest optimizations

**Input Schema**:
```python
{
  "current_selections": [{product: ..., price: float}],
  "total_budget": float,
  "room_allocations": {room: float}
}
```

**Output Schema**:
```python
{
  "budget_status": {
    "spent": float,
    "remaining": float,
    "per_room": {...}
  },
  "alerts": [str],
  "recommendations": [
    {
      "type": "swap" | "downgrade" | "defer",
      "item": str,
      "savings": float,
      "alternative": {...}
    }
  ],
  "is_within_budget": bool
}
```

---

## RAG Implementation Details

### Product Database Schema

**Vector Embeddings** (768 dimensions):
- Product description
- Style keywords
- Room type associations
- Color palette
- Material descriptions

**Metadata** (for filtering):
```python
{
  "product_id": str,
  "retailer": str,
  "name": str,
  "category": str,
  "price_gbp": float,
  "dimensions": {
    "width_cm": float,
    "depth_cm": float,
    "height_cm": float
  },
  "style_tags": [str],
  "color_palette": [str],
  "material": [str],
  "delivery_to_newcastle": bool,
  "delivery_days": int,
  "in_stock": bool,
  "url": str,
  "image_url": str,
  "last_scraped": datetime,
  "price_history": [...]
}
```

### Scraping Strategy

**Retailers to Scrape**:
1. IKEA UK - Wide range, budget-friendly
2. Dunelm - Mid-range, good for textiles/accessories
3. Wayfair UK - Large selection, various price points
4. Made.com - Higher end, design-focused

**Scraping Frequency**:
- Initial build: Full catalog scrape
- Ongoing: Daily price updates
- Weekly: New product discovery

**Data Quality**:
- Validation: Price format, dimension units, availability
- Deduplication: Similar products across retailers
- Freshness: Remove discontinued items

---

## Validation Layers

### 1. Price Validator
- Verify current prices (scrape again if old)
- Check for discounts/sales
- Validate total against budget
- Alert on price increases

### 2. Style Consistency Checker
- Semantic similarity between selected items
- Color palette harmony
- Style coherence across rooms
- Flag outliers

### 3. Dimension Compatibility Checker
- Furniture fits in specified spaces
- Doorway clearance
- Room proportions
- Layout feasibility

### 4. Delivery Feasibility Checker
- All items ship to Newcastle
- Delivery timeframes align
- Assembly requirements noted
- Returns policy verified

---

## User Interaction Flow

### CLI Commands

```bash
# Start new project
design-system init --project "Jesmond House"

# Run discovery phase
design-system discover --interactive

# Generate style concepts
design-system concepts --rooms "living,bedroom1"

# Research products for a room
design-system research --room "living" --style "modern-minimalist"

# Review budget
design-system budget --summary

# Generate final report
design-system report --format pdf

# Export shopping list
design-system export --format csv
```

### Approval Checkpoints

Each phase ends with:
1. Markdown report generated
2. CLI displays summary
3. User prompted: "Approve and continue? (yes/no/modify)"
4. System waits for user input
5. If "modify": Re-run with feedback
6. If "yes": Proceed to next phase
7. All decisions logged in audit trail

---

## Testing Strategy

### Unit Tests
- Each agent in isolation
- Mocked Claude API responses
- Validation logic
- Database operations

### Integration Tests
- Multi-agent workflows
- RAG pipeline end-to-end
- Scraper functionality
- API endpoints

### Mock Data
- Sample floor plans
- Synthetic product catalog
- Historical pricing data
- User preference profiles

---

## Anthropic Best Practices Implementation

### 1. Clear Role Definition
Each agent has explicit role in system prompt:
```xml
<role>You are a specialized {agent_type} within an interior design system</role>
```

### 2. Structured Outputs
All agent responses use JSON schemas validated by Pydantic

### 3. Extended Thinking
Complex decisions use `<thinking>` tags:
```xml
<thinking>
Analyzing budget constraints...
Considering style compatibility...
Evaluating delivery options...
</thinking>
```

### 4. Few-Shot Examples
Agent prompts include 2-3 examples of good outputs

### 5. Chain-of-Thought
Multi-step reasoning explicitly documented

### 6. Error Handling
Retry logic with improved prompts on failure

---

## Deployment Options

### Option 1: Local Development (Recommended First)
- Run on macOS locally
- SQLite database
- CLI interface
- No deployment needed

### Option 2: Cloud Deployment (Optional Later)
- Railway/Heroku for API
- PostgreSQL for persistence
- Web interface
- Scheduled scraping

---

## Success Metrics

### System Performance
- Response time per phase < 2 minutes
- RAG retrieval accuracy > 85%
- Budget compliance 100%
- Scraping success rate > 95%

### User Outcomes
- Complete 4-bedroom design within £10k
- Actionable product list with real links
- Clear implementation timeline
- Satisfaction with recommendations

---

## Next Steps for Implementation

1. **Set up development environment**
   - Python 3.11+ virtual environment
   - Install dependencies
   - Configure Anthropic API key

2. **Build RAG foundation**
   - Set up ChromaDB
   - Implement embedding generation
   - Test vector search

3. **Create first agent (Discovery)**
   - Implement base agent class
   - Write discovery prompts
   - Test with mock data

4. **Develop scraping infrastructure**
   - Start with one retailer (IKEA)
   - Build product schema
   - Store in vector database

5. **Iterate and expand**
   - Add remaining agents
   - Enhance validation
   - Build CLI interface

---

## Questions for You

Before we proceed with implementation, I need clarification on:

1. **Style Preferences**: Do you have any initial style direction (modern/traditional/Scandinavian/industrial/etc.)?

2. **Room Priorities**: Which rooms are most important to furnish first?

3. **Existing Furniture**: Will you keep any existing furniture, or starting from scratch?

4. **Floor Plans**: Do you have floor plans or photos of the house? Can provide now or later?

5. **Rental Restrictions**: Any limitations (e.g., can't paint walls, no permanent fixtures)?

6. **Special Requirements**: Home office setup, guest accommodation, specific storage needs?

7. **Implementation Preferences**: 
   - Start with CLI or build web interface from start?
   - Prefer detailed technical involvement or hands-off automation?

---

## Estimated System Capabilities

Once built, this system will:

✅ Autonomously research 1000+ products from UK retailers
✅ Generate room-by-room designs with exact product specifications
✅ Maintain strict budget tracking with real-time price updates
✅ Provide clickable purchase links for every recommendation
✅ Adapt to your feedback and refine suggestions
✅ Create professional-quality mood boards and reports
✅ Plan implementation timeline with delivery coordination
✅ Save complete audit trail of all decisions

The system will be accurate, thorough, and production-ready - not a proof-of-concept.