---
title: "Ultimate AI Consultant Skill - Installation & Usage Guide"
id: "guide-ai-consultant-install-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "guide"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Ultimate AI Consultant Skill - Installation & Usage Guide

## What You've Got

A comprehensive Claude Desktop skill that combines:

1. **World-Class Kilo Code Prompting** - Master-level prompt engineering for coding workflows
2. **Elite Information Comprehension** - Multi-layer analysis framework for deep understanding
3. **Advanced Second Brain Design** - Knowledge graph architecture with CODE methodology
4. **Flawless Organization & Documentation** - Professional documentation standards
5. **Strategic AI Consulting** - Dan Kennedy + Paddi Lund + business frameworks

This skill makes Claude Desktop operate as an elite AI consultant who understands your:
- Business context (UK SMB consulting, Newcastle focus)
- Tech stack (M4 Mac, Kilo Code, Claude, Neo4j, Qdrant, Obsidian)
- Expert frameworks (Kennedy, Lund, Ziglar)
- Project structure and methodology

---

## Installation

### For Claude Desktop (Primary Use)

**Step 1: Create Skills Directory**

```bash
# Navigate to your home directory
cd ~

# Create .claude directory if it doesn't exist
mkdir -p .claude/skills

# Create skill folder
mkdir -p .claude/skills/ultimate-ai-consultant
```

**Step 2: Install the Skill**

```bash
# Download the skill file you received
# Move it to the skills directory
mv ~/Downloads/ultimate-ai-consultant-skill.md ~/.claude/skills/ultimate-ai-consultant/SKILL.md
```

**Step 3: Verify Installation**

Open Claude Desktop and ask:

```
"What skills do you have access to?"
```

You should see "Ultimate AI Consultant & Knowledge Architect" in the list.

---

### For Kilo Code (VS Code Extension)

**Step 1: Create Kilo Code Configuration**

```bash
# Create Kilo Code config directory if needed
mkdir -p ~/.kilo-code/prompts
```

**Step 2: Create Custom Mode**

In Kilo Code settings:
1. Open VS Code
2. Click Kilo Code icon in left sidebar
3. Click ⚙️ gear icon
4. Go to "Modes" tab
5. Create new mode: "Elite Consultant"
6. Paste the skill content as the system prompt

**Step 3: Configure Profiles**

Create three profiles as described in the skill:

**Profile: "Coding"**
- Model: Claude 3.7 Sonnet
- Use for: Complex logic, architecture, system design

**Profile: "Nano"**
- Model: GPT-4.1-Nano
- Use for: Prompt enhancement, documentation, simple tasks

**Profile: "Speed"**
- Model: MiniMax M2.1
- Use for: Production builds, file operations, batch processing

---

### For Cursor (Optional)

**Step 1: Create Cursor Rules**

```bash
# Create .cursorrules file in your project root
cd /Users/ewanbramley/Projects/[your-project]
touch .cursorrules
```

**Step 2: Add Skill Content**

Copy the skill content into `.cursorrules` file (remove the YAML frontmatter).

---

## How to Use

### Scenario 1: Kilo Code Prompting

**When you're coding and need Kilo Code to build something:**

Instead of:
```
Build an authentication system
```

Use the skill framework:
```
Context: FastAPI app for UK SMB clients
Goal: JWT-based authentication system
Constraints: Must use Redis for sessions, deploy to Railway
Tech: Python 3.11, FastAPI, SQLAlchemy, bcrypt

Analyze current auth structure, plan implementation with:
1. File structure and dependencies
2. Security best practices
3. Error handling strategy
4. Testing approach

Then implement incrementally with validation at each step.
```

The skill will guide Claude to:
1. **Think** - Analyze current state and requirements
2. **Plan** - Create implementation roadmap
3. **Execute** - Build incrementally with tests
4. **Review** - Validate quality before marking complete

---

### Scenario 2: Knowledge Management

**When you need to process information into your second brain:**

```
Process this information into my second brain format:

[Paste content from article/PDF/conversation]

Extract:
- Core principles
- Actionable insights  
- Related concepts in my knowledge base
- Applications to my SMB consulting business
- Neo4j Cypher queries to add this to my knowledge graph
```

The skill will:
1. Create structured markdown notes
2. Generate appropriate tags and connections
3. Provide Neo4j Cypher to add to your knowledge graph
4. Link to existing expert frameworks (Kennedy, Lund, etc.)
5. Suggest applications to your business

---

### Scenario 3: Client Consulting

**When assessing a new client opportunity:**

```
New client inquiry:
- Industry: Dental practice
- Location: Newcastle
- Revenue: ~£800K/year
- Pain: Too many no-shows, manual booking system
- Budget: £500-1000/month for solution

Apply the SMB assessment framework and provide:
1. Quick win opportunity
2. Expected ROI calculation
3. Phased implementation plan (1-2-3)
4. Proposal draft using Kennedy principles
```

The skill will:
1. Run through discovery framework
2. Identify AI automation opportunities
3. Calculate realistic ROI in GBP terms
4. Draft proposal with Kennedy direct response principles
5. Apply Lund client selection criteria

---

### Scenario 4: Documentation Creation

**When you need to document a system:**

```
Document this project:
- FastAPI workflow automation platform
- Uses Neo4j, Redis, Stripe
- Deployed on Railway
- Target: SMB clients for business automation

Generate:
- README.md
- ARCHITECTURE.md
- API.md
- RUNBOOK.md

Follow the documentation excellence standards in the skill.
```

The skill will:
1. Create comprehensive docs following the hierarchy
2. Include code examples that actually run
3. Provide deployment and operations guides
4. Follow professional documentation standards

---

### Scenario 5: System Architecture

**When designing a new system:**

```
Design architecture for:
- AI voice assistant for UK SMBs
- Handles: Bookings, inquiries, basic FAQs
- Integrates: Stripe, Calendar APIs, CRM
- Constraints: <£50/month per client, sub-2s response time
- Scale: 100 concurrent clients

Provide:
1. Component diagram
2. Technology recommendations with rationale
3. Data flow explanation
4. File structure
5. Deployment strategy
```

The skill will:
1. Apply best practices for your tech stack
2. Consider cost optimization (crucial for SMB economics)
3. Design for your M4 Mac development environment
4. Plan Railway/Netlify deployment
5. Include security and scalability considerations

---

## Quick Activation Phrases

To activate specific aspects of the skill, use these phrases:

### Kilo Code Mastery
- "Help me structure this prompt for Kilo Code"
- "Analyze this codebase and plan the implementation"
- "Optimize my Kilo Code workflow for this task"

### Knowledge Architecture
- "Process this into my second brain format"
- "Create Neo4j schema for these principles"
- "Design knowledge architecture for [domain]"

### Business Consulting
- "Assess this client opportunity"
- "Apply Kennedy principles to this offer"
- "Evaluate this using Lund's client selection framework"

### Documentation
- "Generate comprehensive docs for this system"
- "Create professional documentation following best practices"
- "Write API documentation for these endpoints"

### System Design
- "Design architecture for [project]"
- "Create file structure for [application type]"
- "Plan deployment strategy for [system]"

---

## Pro Tips

### 1. Chain Skills with Context

Build complex workflows by chaining skill capabilities:

```
Step 1: Analyze this client problem using business consulting framework
Step 2: Design system architecture to solve it
Step 3: Create Kilo Code prompts to build it
Step 4: Generate comprehensive documentation
```

### 2. Combine with Memory

The skill integrates with your profile information, so it automatically:
- Uses your tech stack (M4 Mac, Docker, Railway)
- Applies your business model (UK SMB, 0-3M revenue)
- References your expert frameworks (Kennedy, Lund, Ziglar)
- Understands your project paths and preferences

### 3. Iterative Refinement

Start broad, then narrow:

```
1. "Design system architecture for voice AI assistant"
   [Claude provides high-level design]

2. "Now create detailed file structure for the auth module"
   [Claude zooms into specific component]

3. "Generate Kilo Code prompts to build the JWT token handler"
   [Claude provides executable coding instructions]
```

### 4. Cross-Reference Your Knowledge

The skill knows your knowledge structure:

```
"Link this new insight about client retention to my existing 
Paddi Lund principles in my knowledge graph. Generate the 
Neo4j Cypher to create the relationship."
```

### 5. Export for Team Use

Once you've refined workflows with the skill:

```
"Document this workflow as a reusable SOP that I can give 
to a VA or team member. Follow the documentation standards 
in the skill."
```

---

## Integration with Your Existing Systems

### Obsidian Integration

The skill outputs are designed to work with your Obsidian vaults:

```markdown
---
type: principle
source: Client call - Jan 2026
date: 2026-01-18
tags: [automation, smb, voice-ai]
expert: Ewan Bramley
confidence: high
---

# Voice AI Response Time Optimization

## Context
Sub-2-second response time is critical for SMB phone systems. 
Anything longer feels "robotic" and kills trust.

## Core Insight
Use lightweight models (Groq/Whisper) for transcription, 
cached responses for common questions, streaming for natural feel.

## Application
- Dental: "I'd like to book an appointment" → instant → calendar check
- Vet: "Is the vet available?" → instant → schedule lookup
- General: FAQ responses cached, served from edge

## Related Concepts
- [[Cost Optimization Strategies]]
- [[Client Experience Standards]]
- [[Technical Architecture]]

## Evidence
- Tested response times: Groq (0.3s) vs OpenAI (1.2s)
- Client feedback: <1s = "instant", >2s = "slow"

## Questions/Gaps
- How to handle edge cases that need reasoning?
- Fallback strategy for API failures?
```

### Neo4j Integration

The skill generates Cypher queries ready to paste:

```cypher
// Create new principle
CREATE (p:Principle {
  id: "EWB_001",
  name: "Sub-2-Second Response Time Rule",
  description: "Voice AI must respond in under 2 seconds for natural conversation",
  domain: "voice-ai",
  confidence: "high",
  date_added: "2026-01-18",
  source: "Client testing + feedback"
})

// Link to expert (you)
MATCH (expert:Expert {name: "Ewan Bramley"})
CREATE (p)-[:CREATED_BY]->(expert)

// Link to related principle
MATCH (related:Principle {id: "DK_003"})
CREATE (p)-[:RELATES_TO]->(related)

RETURN p;
```

### GitHub/Project Integration

The skill follows your project structure:

```
/Users/ewanbramley/Projects/
├── business-factory/
│   └── [Skill generates structure here]
├── voice-ai-assistant/
│   └── [Skill generates structure here]
└── client-projects/
    └── [Skill generates structure here]
```

---

## Maintenance & Updates

### When to Update the Skill

**Add new expert principles:**
When you learn from a new expert (e.g., read new Kennedy material), update the skill with those principles.

**Refine based on usage:**
Every month, review what parts of the skill you used most. Expand those areas, simplify or remove unused parts.

**Tech stack changes:**
When you adopt new tools (e.g., switch from Railway to different hosting), update the constraints section.

**Client patterns:**
As you discover patterns in client work, add them to the consulting framework section.

### Version Control

Keep your skill in Git:

```bash
cd ~/.claude/skills/ultimate-ai-consultant
git init
git add SKILL.md
git commit -m "Initial version - Jan 2026"

# After updates
git add SKILL.md
git commit -m "Added: New Kennedy principle on pricing"
git tag v1.1
```

---

## Troubleshooting

### Skill Not Activating

**Problem**: Claude doesn't seem to use the skill

**Solutions**:
1. Check file is named `SKILL.md` (not .txt or .markdown)
2. Verify YAML frontmatter is properly formatted
3. Restart Claude Desktop
4. Ask explicitly: "Use the Ultimate AI Consultant skill to..."

### Skill Too Verbose

**Problem**: Responses are overly detailed when you want quick answers

**Solution**: Add to your request:
```
"Brief mode: Give me just the 3-sentence summary"
```

### Skill Conflicts with Project Context

**Problem**: Skill assumes UK SMB context when working on different type of project

**Solution**: Override explicitly:
```
"Ignore SMB context for this project. This is a SaaS tool for 
US enterprises with $100M+ revenue. Apply skill's technical 
and documentation standards only."
```

---

## Advanced Usage

### Create Domain-Specific Sub-Skills

As you specialize, create focused variants:

```
~/.claude/skills/
├── ultimate-ai-consultant/        # Master skill
├── dental-practice-consultant/    # Dental-specific variant
├── voice-ai-architect/            # Voice AI specialist
└── automation-engineer/           # Pure technical, no business
```

Each inherits from the master but adds domain-specific knowledge.

### Integrate with MCP Servers

Connect the skill to your tools:

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"]
    },
    "neo4j": {
      "command": "mcp-neo4j",
      "args": ["localhost", "7687"]
    }
  }
}
```

Now the skill can:
- Read/write Notion databases directly
- Query/update Neo4j knowledge graph
- Execute file operations on your Mac

### Build Skill Chains

Create workflows that chain multiple skills:

```
Skill 1: Research (gather information)
   ↓
Skill 2: Analyze (apply Ultimate AI Consultant frameworks)
   ↓
Skill 3: Build (use Kilo Code prompting)
   ↓
Skill 4: Document (generate professional docs)
```

---

## Expected Outcomes

After installing and using this skill, you should experience:

### Week 1: Faster Workflows
- Kilo Code prompts are more effective (fewer iterations)
- Documentation is comprehensive without extra effort
- Client assessments follow proven frameworks

### Week 2-4: Better Quality
- Code follows consistent patterns
- Knowledge captured systematically
- Client proposals use Kennedy principles effectively

### Month 2-3: Compounding Returns
- Knowledge graph grows intelligently
- Past decisions inform new ones
- Reusable patterns emerge
- Client work becomes more profitable (less time, better results)

### Month 3-6: System Thinking
- You stop thinking about "how to prompt Claude"
- Systems design becomes second nature
- Documentation happens automatically
- Client consulting follows proven playbooks

---

## Support & Iteration

### Improve the Skill

This skill is designed to evolve with your business. As you:

- Learn new frameworks → Add to consultant section
- Discover new patterns → Add to Kilo Code prompting
- Refine knowledge structure → Update second brain section
- Standardize documentation → Update doc templates

Keep the skill as a living document in your knowledge system.

### Community & Sharing

If you create valuable additions to the skill:
1. Export the relevant section
2. Share with other consultants/developers
3. Build on each other's improvements

### Need Help?

For issues specific to:
- Claude Desktop → Anthropic docs: code.claude.com/docs
- Kilo Code → Kilo docs: kilo.ai/docs
- Knowledge architecture → Revisit your Meta-Prompt document
- Business frameworks → Your Business Command Center in Notion

---

**Skill Version**: 1.0  
**Installation Date**: 2026-01-18  
**Next Review**: 2026-02-18 (monthly)  
**Status**: Production Ready

---

## Quick Start Checklist

- [ ] Skill file moved to `~/.claude/skills/ultimate-ai-consultant/SKILL.md`
- [ ] Claude Desktop restarted
- [ ] Verified skill appears in "What skills do you have?"
- [ ] Tested with simple prompt: "Help me structure a Kilo Code prompt"
- [ ] Tested with business prompt: "Assess this client opportunity: [details]"
- [ ] Tested with knowledge prompt: "Process this into second brain format: [content]"
- [ ] Kilo Code profiles configured (Coding, Nano, Speed)
- [ ] Documentation standards tested on a sample project
- [ ] Integration with Notion/Neo4j verified (if using)
- [ ] Skill added to version control
- [ ] First improvement captured in skill's improvement log

You're ready to operate as a world-class AI consultant. Go build something exceptional.