# Marketing Engine — Amplified Partners

## What This Is

The marketing engine is our first real workload. It generates, schedules, and publishes content for SMBs who don't have the time, money, or expertise to do marketing properly.

**First client**: Dave at Jesmond Plumbing.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  MARKETING ENGINE                     │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Research  │→ │ Content  │→ │ Publishing       │  │
│  │ Agent    │  │ Agent    │  │ Agent            │  │
│  │          │  │          │  │                  │  │
│  │ SearXNG  │  │ LiteLLM  │  │ Social APIs     │  │
│  │ FalkorDB │  │ Rubrics  │  │ Google My Biz   │  │
│  │          │  │ Enforcer │  │ Website CMS     │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                       │
│  ┌──────────────────────────────────────────────┐    │
│  │            Shared Services                    │    │
│  │  Langfuse (tracing) | Redis (queue/cache)    │    │
│  │  PostgreSQL (state) | FalkorDB (knowledge)   │    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## Three Agents

### 1. Research Agent
- Searches for local market insights using SearXNG
- Pulls competitor analysis (what are other plumbers in Newcastle posting?)
- Queries FalkorDB knowledge graph for client-specific context
- Identifies trending topics, seasonal relevance, local events

### 2. Content Agent
- Takes research output and generates content
- Uses LiteLLM to route to appropriate model (Tier 2 for content = gpt-4.1-mini)
- Applies rubrics: tone, accuracy, brand voice, compliance
- The Enforcer validates output quality before publishing
- Generates: social posts, blog articles, Google My Business updates, email newsletters

### 3. Publishing Agent
- Schedules content to appropriate platforms
- Handles platform-specific formatting (Twitter length, Instagram captions, LinkedIn tone)
- Manages posting cadence (not too frequent, not too sparse)
- Tracks engagement metrics back to Langfuse for learning

## Content Types

| Type | Platform | Cadence | Model Tier |
|------|----------|---------|------------|
| Social posts | Facebook, Instagram, Twitter, LinkedIn | 3-5/week | Tier 2 (gpt-4.1-mini) |
| Blog articles | Website | 1-2/week | Tier 1 (claude-sonnet-4) |
| Google My Business | GMB | 2-3/week | Tier 3 (gpt-4.1-nano) |
| Email newsletter | Email list | 1/week | Tier 1 (claude-sonnet-4) |
| Review responses | Google/Facebook | As needed | Tier 2 (gpt-4.1-mini) |

## Client Onboarding

What we need from each client:
1. **Business basics**: Name, address, services, service area
2. **Brand voice**: How do they talk? Formal? Friendly? Technical?
3. **Competitors**: Who are they competing against locally?
4. **Goals**: More calls? More website visits? Brand awareness?
5. **Existing content**: Social accounts, website, Google My Business listing
6. **No-go topics**: Anything they don't want us to post about

## Dave at Jesmond Plumbing — First Run

### What we know:
- Plumbing business in Jesmond, Newcastle upon Tyne
- Local service area
- Needs consistent online presence
- Probably has Google My Business, maybe Facebook

### Phase 1 deliverables:
1. Content calendar for March 2026
2. 10 social media posts (ready to publish)
3. 2 blog articles (seasonal: spring plumbing tips, emergency plumbing guide)
4. Google My Business optimization recommendations
5. Review response templates

## File Structure

```
marketing-engine/
├── README.md                    # This file
├── config/
│   ├── engine_config.yaml       # Engine settings
│   └── clients/
│       └── jesmond-plumbing.yaml # Dave's config
├── agents/
│   ├── research_agent.py        # Market research
│   ├── content_agent.py         # Content generation
│   └── publishing_agent.py      # Scheduling & publishing
├── rubrics/
│   ├── tone_rubric.yaml         # Brand voice scoring
│   ├── quality_rubric.yaml      # Content quality scoring
│   └── compliance_rubric.yaml   # Legal/compliance scoring
├── templates/
│   ├── social_post.md           # Social post template
│   ├── blog_article.md          # Blog template
│   └── gmb_update.md            # Google My Business template
└── outputs/
    └── clients/
        └── jesmond-plumbing/    # Generated content per client
```

## How It Runs

On The Beast, the marketing engine runs as a scheduled Docker service:
- Research agent runs daily at 6am (fresh market data)
- Content agent runs daily at 7am (generates from research)
- Publishing agent runs at scheduled post times
- All LLM calls routed through LiteLLM, traced by Langfuse
- The Enforcer validates quality before any publish action

## Dependencies

- SearXNG (search.beast.amplifiedpartners.ai)
- LiteLLM (llm.beast.amplifiedpartners.ai)
- Langfuse (observe.beast.amplifiedpartners.ai)
- The Enforcer (enforcer.beast.amplifiedpartners.ai)
- FalkorDB (knowledge graph on Beast)
- Redis (job queue + cache)
- PostgreSQL (client state + content history)
