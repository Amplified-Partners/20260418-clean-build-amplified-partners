---
title: "MEMORY.md Starter Template"
id: "memory-md-starter-template"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "MEMORY_md_Starter.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# MEMORY.md Starter Template
# Agent Builder Academy — agentbuilderacademy.com

## What This File Is

MEMORY.md is not a file you write. It is a file the agent maintains.

Place it at your project root: `MEMORY.md`

Then instruct the agent (in CLAUDE.md) to read it at the start of each session and update it at the end.

The distinction that matters:

| /docs | MEMORY.md |
|-------|-----------|
| Standards and patterns you define | Decisions and learnings the agent accumulates |
| Prescriptive — the blueprint | Operational — the project diary |
| You write and maintain it | The agent writes and maintains it |
| Stable | Evolves every session |

---

## How to Tell the Agent to Use It

Add this to your CLAUDE.md:

```
## Session Memory

At the start of each session: read MEMORY.md for project context and recent decisions.
At the end of each session: update MEMORY.md with any decisions made, problems solved,
or patterns discovered. Keep entries concise. Date each entry.

MEMORY.md is the project diary. /docs is the blueprint. Do not confuse them.
```

---

## MEMORY.md Template

Copy this as your starting point. The agent will expand it over time.

---

# Project Memory

## Project Context
[The agent fills this in based on CLAUDE.md and the first session]

## Active Work
[What is currently being built or changed]

## Recent Decisions

### [Date] — [Topic]
[What was decided and why. Keep to 2-3 sentences.]

### [Date] — [Topic]
[...]

## Patterns Discovered
[Recurring patterns the agent has noticed and should remember]

- [Pattern]: [Where it applies and why it matters]

## Known Issues
[Problems that exist and have not been resolved yet]

- [Issue]: [What it is, when it was noticed, workaround if any]

## What Worked
[Approaches that were effective — worth repeating]

## What Did Not Work
[Approaches that failed or caused problems — avoid repeating]

## Open Questions
[Unresolved decisions or things to investigate]

---

## Keeping MEMORY.md Useful

- Keep entries short. One decision = 2-3 sentences.
- Date every entry. Old entries become noise — remove them after they are no longer relevant.
- Do not duplicate /docs. If something belongs in /docs, write it there, not here.
- Review and trim every few sessions. A long MEMORY.md loses its value.

Rule of thumb: if the agent has to scroll past old context to find recent context, it is time to clean up.

---

Source: Agent Builder Academy — agentbuilderacademy.com
Framework: Agent Orchestration Layer (AOL) — AOL 3 (Informed)
