---
title: "AI Self-Reflection & Debugging — Research Synthesis"
id: "self-reflection-research-synthesis-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# AI Self-Reflection & Debugging — Research Synthesis
## Raw findings from March 2026 research sprint

### 1. Reflexion Framework (Shinn et al., NeurIPS 2023)
- **Paper:** "Reflexion: Language Agents with Verbal Reinforcement Learning"
- **URL:** https://proceedings.neurips.cc/paper_files/paper/2023/file/1b44b878bb782e6954cd888628510e90-Paper-Conference.pdf
- **GitHub:** https://github.com/noahshinn/reflexion
- **Key Innovation:** Reinforces language agents NOT by updating weights, but through linguistic feedback
- **Architecture:** 3 models — Actor (generates), Evaluator (scores), Self-Reflection (generates verbal cues)
- **Mechanism:** Agent verbally reflects on task feedback → maintains reflective text in episodic memory buffer → better decisions in subsequent trials
- **Results:** 91% pass@1 on HumanEval (vs GPT-4's 80% at the time)
- **Strategies:** Last-attempt trace as context, self-reflection as context, or both
- **Key insight:** "Self-reflection acts as a 'semantic gradient signal' — concrete direction for improvement, akin to how humans iteratively learn"
- **Relevance to Amplified:** This IS the Kaizen loop applied to AI — PDCA for agents. Verbal reflection = the post-mortem Ewan described.

### 2. ReflexiCoder (Jiang et al., March 2026)
- **Paper:** "ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning"
- **URL:** https://arxiv.org/html/2603.05863v1
- **GitHub:** https://github.com/juyongjiang/ReflexiCoder
- **Key Innovation:** RL framework that INTERNALIZES self-reflection into model weights (not just prompting)
- **Architecture:** RL-zero training — no supervised fine-tuning, discovers reflection-correction patterns autonomously
- **Mechanism:** Structured trajectory: initial reasoning → code generation → bug/optimization-aware reflection → correction
- **Results:** 94.51% HumanEval, 35% BigCodeBench, competes with GPT-5.1
- **Token Efficiency:** 40% fewer tokens than base models — nearly 50% reduction in reasoning tokens
- **Key insight:** "Intrinsic debugging capability that mimics human-like cognitive oversight" — exactly one reflection cycle in virtually all cases
- **Relevance to Amplified:** Proves that disciplined self-reflection is MORE efficient, not less. Quality AND speed. Aligns with "test-test-test" principle.

### 3. AGENTS.md Pattern (Eric Ma, Addy Osmani, Ryan Carson et al., 2026)
- **Eric Ma:** https://ericmjl.github.io/blog/2026/1/17/how-to-build-self-improving-coding-agents-part-1/
- **Addy Osmani:** https://addyosmani.com/blog/self-improving-agents/
- **Stormy AI guide:** https://stormy.ai/blog/mastering-agents-md-ai-coding-memory
- **Key Innovation:** Durable repository memory + reusable playbooks = agent improvement like "runbooks plus postmortems"
- **Two levers:** AGENTS.md (persistent memory per repo) + Skills (reusable playbooks)
- **Loop:** Observe mismatch → Tell agent what must be true → Agent writes correction into AGENTS.md → Agent reads it next time
- **Self-correction built in:** "When the agent notices the code map looks stale, it should update the code map"
- **Maturity model:** Ad hoc prompting → Repo-local memory → Global/shared skills
- **Relevance to Amplified:** This IS the Baton Pass Protocol. AGENTS.md = SESSION-STATE.md + vault. Skills = our 10 Perplexity custom skills. We're ALREADY doing this at a higher level.

### 4. Anthropic 2026 Agentic Coding Trends
- **Report:** https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf
- **Code Review launch:** https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/
- **Predictions:**
  - "Agentic quality control becomes standard" — AI agents reviewing AI-generated output
  - "Agents learn when to ask for help" — recognizing situations requiring human judgment
  - "Human oversight shifts from reviewing everything to reviewing what matters"
- **Code Review tool:** Multi-agent system, parallel analysis from different perspectives, final aggregator agent
  - Focus on logic errors, not style (exactly right for Amplified)
  - Red/yellow/purple severity labeling
  - $15-25 per review (expensive but proves the pattern)
- **Relevance to Amplified:** Validates our Quality Framework approach — agents should check agents. The council voting protocol IS this pattern.

### 5. Self-Correcting Agent Architecture (Composite research)
- **3 Pillars:** Error Detection → Reflection → Retry Logic
- **Oracle article:** https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it
- **4 memory types (converging industry standard):** Working, Procedural, Semantic, Episodic
  - Maps to human memory — exactly the Business Brain architecture
- **Context Amnesia solutions:** https://hadijaveed.me/2025/11/26/escaping-context-amnesia-ai-agents/
  - Session Handoff / Compaction via Recursive Summarization
  - "100k tokens of messy history → 500 tokens of pure signal"
  - Handoff Note format: Current Goal, Progress Made, Files Modified, Current State, Next Steps
- **Persistent memory via files:** MEMORY.md, SOUL.md, progress.txt, daily logs
- **Agent reliability science:** https://arxiv.org/html/2602.16666v1
  - "Post-mortem analysis of failures feeding back into improved monitoring and agent design"
  - Confidence self-assessment: agents rate their own confidence upon completion

### 6. Ewan's Key Insight — The Self-Critical Post-Mortem
Ewan's discovery: "Self-reflection really helps on debugging. If the original coder's partner criticizes itself and says the problem that it's had, how it was built, that might help the next AI to improve it."

This maps DIRECTLY to:
- Reflexion's verbal self-reflection in episodic memory
- AGENTS.md self-correction loop
- Anthropic's agent-reviewing-agent pattern
- ReflexiCoder's internalized debugging capability
- The Baton Pass Protocol's "Save Everything" rule

**The innovation for Amplified:** Every AI build session produces a SELF-CRITICAL POST-MORTEM that:
1. States what was attempted
2. States what went wrong (with honesty, not excuses)
3. States HOW it was built (architecture decisions, trade-offs)
4. States what the AI would do differently next time
5. Provides a logical README for the next AI to read
6. Rates its own confidence in the output
7. Gets stored in the vault as permanent institutional memory

This creates a "Department of Continuous Improvement" — whether human-reviewed or AI-reviewed, failures compound into knowledge.
