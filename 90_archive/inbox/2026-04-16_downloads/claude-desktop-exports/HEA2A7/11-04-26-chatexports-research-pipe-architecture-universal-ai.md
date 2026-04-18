---
export_version: chatexports
export_date: 2026-04-12
original_date: 2026-04-11
title: research-pipe-architecture
section: 5
total_sections: 7
topics:
  - research-pipe
  - interpreter
  - neutraliser
  - curator-1
  - curator-2
  - multi-agent
  - anti-bias-architecture
  - Claude-API
participants:
  - user
  - claude
---

# Research Pipe Architecture

## What Happened

User described an architecture for a research pipe. Initially described as three roles (interpreter, curator 1, curator 2), then refined to four roles by adding a neutraliser between interpreter and curator 1.

User specified the interpreter classifies input as fact/opinion/science/logic, identifies the goal, and identifies what the information is for. A separate role — the neutraliser — strips the goal from the language before it reaches curator 1, so search terms are not shaped by what the answer is "supposed to be." Curator 1 receives a neutral brief, knows methodology for search terms, breadth, depth, source selection, and sends searches to four search engines. Curator 2 receives results and compares them against the neutral brief curator 1 was given — not against the original question. Curator 2 evaluates whether results deliver what the brief asked for.

User specified the original goal only comes back into play when results are presented to the human. The system's job is complete and unbiased research. The human decides if it answers their question.

User stated this is not about being right, it's about being accurate. It is preferable to be told you're on the wrong track as soon as possible. Every role's instructions include: your job is not to support the premise, your job is to find what's there.

Claude researched multi-agent architectures and found the design validated by Anthropic's own research system, Microsoft's Local Research Desk, Google's Agent Development Kit patterns, Amazon's MAC framework, and multiple academic papers. All confirmed separation of roles, generator-critic patterns, feedback loops, and the principle that each agent should do one job well.

User identified the biggest problem as themselves — unclear speech input. Said a structured intake conversation that forces clarity and allows Claude room for refinement, extrapolation, and amplification is the first thing to build. Speed is way down the list, accuracy is way up.

## Decisions Made

- Four roles: interpreter, neutraliser, curator 1, curator 2
- Interpreter classifies input: fact, opinion, science, logic. Identifies goal and purpose.
- Neutraliser strips goal from language before it reaches curator 1 — prevents confirmation bias at search stage
- Curator 1 receives neutral brief, generates search terms, sends to four search engines. Doesn't judge results.
- Curator 2 compares results against curator 1's neutral brief, not against original question. Evaluates completeness.
- Original goal returns only when results are presented to the human
- Claude API at each stage with clear guidelines
- Structured intake conversation forces user clarity before anything enters the pipe
- Speed is secondary to accuracy
- "This is not about being right, this is about being accurate"
- Every role: "your job is not to support the premise, your job is to find what's there"
- If results contradict the premise, say so immediately — that's the system working
- Aspirational: strip emotional terms, maintain goal without corrupting it
- Practical: strict rules on maintaining the goal in each role's instructions

## To Do

- Set up Claude Code using existing subscription
- Build structured intake conversation
- Generate clear XML prompt from interpreter
- Pass to curator 1 who sends to four search engines
- Results return to curator 2 who compares against neutral brief
- Present to user when curator 2 confirms completeness

## Sources

- Anthropic engineering blog — multi-agent research system, separation of concerns, subagent architecture
- Microsoft — Local Research Desk, retriever/critic/writer separation, feedback loops
- Google Agent Development Kit — generator-critic pattern, sequential pipeline
- Amazon MAC framework — multi-agent clarification, modular role distribution
- arxiv — multi-agent RAG framework for entity resolution
- Medium — multi-agent system patterns, context curator role
- arxiv — conversational prompt rewriting for improved LLM responses
- arxiv — "If we misunderstand the client we misspend 100 hours" — elicitation research
