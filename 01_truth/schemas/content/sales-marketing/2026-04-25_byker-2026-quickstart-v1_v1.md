---
title: "Byker 2026 - Quick Start Reference"
id: "byker-2026-quickstart-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "sales-marketing"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Byker 2026 - Quick Start Reference

## The Stack at a Glance

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│    📱 OBSIDIAN                    ☁️ RAILWAY                             │
│    Your Brain                     Your Cloud                            │
│    ┌─────────────┐               ┌─────────────┐                        │
│    │ 00-INBOX    │               │ FastAPI     │                        │
│    │ 10-CLIENTS  │◄──────────────│ Backend     │                        │
│    │ 20-KNOWLEDGE│               └─────────────┘                        │
│    │ 30-CONTENT  │               ┌─────────────┐                        │
│    │ 40-OPERATIONS│              │ React       │                        │
│    │ 50-SYSTEMS  │               │ Dashboard   │                        │
│    │ 60-REFERENCE│               └─────────────┘                        │
│    │ 90-META     │               ┌─────────────┐                        │
│    └─────────────┘               │ N8N         │                        │
│           │                      │ Workflows   │                        │
│           │                      └─────────────┘                        │
│           │                      ┌─────────────┐                        │
│           │                      │ PostgreSQL  │                        │
│           ▼                      │ Database    │                        │
│    ┌─────────────────────────────└─────────────┘                        │
│    │                                                                     │
│    │         🤖 LLM ORCHESTRATION LAYER                                 │
│    │                                                                     │
│    │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│    │   │ Claude   │ │ Gemini   │ │ Qwen     │ │ Ollama   │             │
│    │   │ (Quality)│ │ (Context)│ │ (Budget) │ │ (Free)   │             │
│    │   └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│    │                                                                     │
│    └─────────────────────────────────────────────────────────────────────┘
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 4-Kilo Agent Architecture

| Kilo | Focus | Skills | When to Use |
|------|-------|--------|-------------|
| **1** | Content & Leads | content-factory, lead-magnet, outbound | Content creation, lead gen |
| **2** | Client Delivery | diagnostic, onboarding, helpdesk | Serving clients |
| **3** | Systems & Ops | sop-builder, retention, gamification | Building systems |
| **4** | Business Strategy | principles-coach, orchestrator | Planning, coaching |

## LLM Routing Quick Reference

| Task Type | Model | Why |
|-----------|-------|-----|
| Client report | Claude Sonnet | Quality matters |
| Quick question | Local Qwen | Free, fast |
| Bulk summaries | DeepSeek | Cheap, good |
| Long document | Gemini Pro | 1M+ context |
| Code | DeepSeek Coder | Specialised |
| Private data | Local only | Data sovereignty |
| Embeddings | Local Nomic | Free, fast |

## Week 1 Checklist

### Day 1-2: Obsidian
- [ ] Install from ~/Downloads/Obsidian*.dmg
- [ ] Create vault at ~/Documents/Byker-Vault
- [ ] Create folder structure (00-90)
- [ ] Install plugins: Smart Connections, Copilot, Dataview, Templater

### Day 3-4: Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b         # 4.4GB
ollama pull llama3.1:8b        # 4.7GB
ollama pull nomic-embed-text   # 274MB
```

### Day 5-7: APIs
- [ ] Verify Gemini API key
- [ ] Add Anthropic API key
- [ ] Configure Qwen/DeepSeek keys
- [ ] Test all providers

## Key Automations (N8N)

1. **Lead → Client Pipeline**
   - Form submit → Score → Segment → Nurture → Book call

2. **Content Machine**
   - Calendar trigger → Generate → Review → Publish → Track

3. **Client Onboarding**
   - Contract → Welcome email series → Portal → Kickoff

4. **Retention Loop**
   - Monthly → Metrics → Health score → Alert if needed → Win report

## Monthly Costs

| Component | Estimated |
|-----------|-----------|
| Railway | £15-45 |
| Claude API | £50-100 |
| Other APIs | £15-75 |
| **Total** | **£80-220** |

## ROI Calculator

- Hours saved per week: 10+
- Your hourly rate: £100+
- Monthly value: £4,000+
- Infrastructure cost: £150 avg
- **Net ROI: £3,850+/month**

---

## What Makes This Ingenious

1. **70% cost reduction** via intelligent LLM routing
2. **Local-first** - Your data, your machine, GDPR-safe
3. **Fail-safe** - Every automation has manual override
4. **Scalable** - Same system works for 1 or 100 clients
5. **Beautiful** - Obsidian as command center, visual N8N workflows

---

*Full architecture: BYKER-2026-ARCHITECTURE.md*
*Skills package: byker-skills-complete.zip*
