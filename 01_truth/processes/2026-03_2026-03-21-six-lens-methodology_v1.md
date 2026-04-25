---
title: "2026-03-21-SIX-LENS-METHODOLOGY"
id: "2026-03-21-six-lens-methodology"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "2026-03-21-SIX-LENS-METHODOLOGY.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Six-Lens Technique
**Created**: 2026-03-21 by Prism (Claude Code, Opus 4.6) + Ewan Bramley
**What it is**: A reusable method for extracting maximum value from any batch of files, code, or data using parallel agents with different analytical lenses.
**Key insight**: This is generalised PUDDING. Same Inventory-Classify-Score-Connect-Gap pattern, different starting assumptions per lens.

---

## Base Methodology (Same For All Lenses)

1. **INVENTORY** — What's actually here? Count it. List it. No interpretation yet.
2. **CLASSIFY** — What category does each thing fall into? (built/specced/vapourware, story/quote/diagram, supported/unsupported, etc.)
3. **SCORE** — How good is it? Grade it honestly.
4. **CONNECT** — What links to what? Dependencies, cross-references, hidden connections.
5. **GAP** — What's missing? The negative space. What SHOULD be here but isn't?
6. **VERDICT** — One honest sentence. No hedging.

---

## The Six Lenses

### Lens 1: CONTENT
**Agent name**: (unnamed, first pass)
**Scores for**: Voice, narrative quality, quotability, visual/diagram potential
**Gap means**: Missing stories, weak one-liners, untold moments
**Use when**: You need to extract publishable content, find the human voice, identify what's compelling

### Lens 2: BLUEPRINT (Technical Architecture)
**Agent name**: Blueprint
**Scores for**: Functional code, integration points, infrastructure specs, dependency chains
**Gap means**: Single points of failure, missing plumbing, unbuilt components
**Use when**: You need to know what's actually built vs specced vs vapourware

### Lens 3: LEDGER (Commercial)
**Agent name**: Ledger
**Scores for**: Revenue evidence, market proof, unit economics, competitive moat
**Gap means**: No customers, no sales process, untested pricing, missing go-to-market
**Use when**: You need brutal commercial honesty — could you sell this tomorrow?

### Lens 4: ENFORCER (Risk & Quality)
**Agent name**: Enforcer
**Scores for**: Evidence behind claims, consistency between files, security, data protection
**Gap means**: Contradictions, unsupported claims, GDPR risks, processes with no rollback
**Use when**: You need a hostile auditor to find what could go wrong

### Lens 5: SWANSON (Cross-Domain / PUDDING)
**Agent name**: Swanson
**Scores for**: Non-obvious connections between files, metaphor bridges, missing middles
**Gap means**: Unlinked domains, connections nobody has spotted yet
**Use when**: You need cross-pollination, unexpected insights, the PUDDING technique at scale
**Named after**: Don Swanson, who discovered fish oil treats Raynaud's disease by connecting two literatures that had never been connected

### Lens 6: ROOT (Why The Gaps Exist)
**Agent name**: Root
**Scores for**: The reason behind each gap — is it a sequencing choice, a session boundary, or a real problem?
**Gap means**: Premature optimization, genuine oversight, or evidence of correct build order
**Use when**: You've found gaps from the other five lenses and need to know which ones to care about

**ROOT's three patterns**:
- Gap is solo-founder-shaped → Don't fill it yet. Fixes itself at scale.
- Gap is session-boundary-shaped → Run the lenses again. The connection is waiting.
- Gap is function-over-narrative → Extract from voice captures. The story is already recorded.

---

## How To Run It

### Setup
- Any batch of files (markdown, code, JSON, transcripts — anything readable)
- Claude Code or equivalent with ability to dispatch parallel agents
- Minimum: 3 lenses. Full suite: all 6.

### Execution
1. Pick your lenses based on what you need (content extraction? technical audit? commercial reality check?)
2. Dispatch one agent per lens, ALL IN PARALLEL
3. Each agent reads EVERY file in the batch
4. Each agent applies the six-step base methodology through their specific lens
5. When all agents return, have each lens review the others' findings (one more pass)
6. Run ROOT lens last — it needs the gaps from all other lenses as input

### Customisation
- The base methodology never changes
- The lens determines what you're scoring and what counts as a gap
- Add new lenses by defining: what it scores for, what a gap means, when to use it
- Each lens gets a name (helps agents stay in character)

### Time
- 80 files through 5 parallel lenses: ~1 hour
- Cross-lens review: ~15 minutes
- ROOT analysis: ~15 minutes
- Total: ~90 minutes for comprehensive extraction

---

## What This Produces

Per lens:
- Complete inventory of every file
- Classification and scoring
- Connections found
- Gaps identified
- One-sentence verdict

Across lenses:
- Points of agreement (all lenses say the same thing)
- Points of disagreement (productive tensions)
- Hidden connections (Swanson puddings)
- Root causes of gaps (ROOT analysis)
- Publishable content (stories, quotes, diagrams, case studies)

---

## Origin

Designed during a live session on 2026-03-21. Ewan Bramley had been trying to extract value from 80 recovery-staging files for two months. Five parallel agents with different lenses did it in one hour. The technique was recognised as generalised PUDDING — the same Inventory-Classify-Score-Connect-Gap pattern that Ewan had already invented, applied through different analytical assumptions.

The ROOT lens was added when Ewan asked: "There's another valuable lens — turns gaps into completeness. Why were the gaps there?" That question completed the methodology.
