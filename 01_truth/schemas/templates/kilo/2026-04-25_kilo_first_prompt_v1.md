---
title: "KILO CODE - FIRST PROMPT"
id: "kilo_first_prompt"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# KILO CODE - FIRST PROMPT

## Step 1: Initialize Memory Bank

Open Kilo Code in VS Code, switch to **Architect Mode**, and paste this:

---

```
initialize memory bank
```

---

Kilo Code will read the brief.md and generate the other memory bank files (product.md, context.md, architecture.md, tech.md). Review what it generates and correct any errors.

---

## Step 2: Load the Full Specification

After memory bank is initialized, paste this prompt to load the full project specification:

---

```
Read the MASTER_SPEC.md file in the project root. This is the complete specification for a multi-modal personal assistant app. 

Your job:
1. DO NOT alter the meaning of any requirement in this document
2. Parse it into actionable implementation tasks
3. Identify which parts map to: UI/UX design, Agent architecture, Workflows, Memory/context, Safety/permissions, Behavioural design
4. Create an implementation plan following the phased roadmap in the spec:
   - MVP (0-3 months): Core chat, email summarisation & drafts, basic tasks, daily planning
   - V1 (3-6 months): Calendar, weekly review, coaching, call summaries
   - V2+ (6-12 months): Full telephony, knowledge graph, research mode, analytics

Start with MVP scope only. What are the first files and components we need to create?
```

---

## Step 3: Begin Implementation

After Kilo Code has parsed the spec, ask it to start building:

---

```
Let's begin MVP implementation. Start with:
1. Project scaffolding (folder structure per the spec)
2. Core assistant chat interface
3. The orchestrator logic that routes to different agents

Follow the UI patterns defined in the spec exactly - reference the specific UX laws and behavioural principles when making design decisions.

Create the first files now.
```

---

## Notes

- The ADDENDUM.md file contains my additional suggestions - review these separately and implement only if you approve
- The project-rules.md in .kilocode/rules/ ensures Kilo Code follows the spec exactly
- If Kilo Code tries to deviate from the spec, remind it: "Follow MASTER_SPEC.md exactly"

## Existing Components

Remember you mentioned these are already built:
- Telephone assistant
- Voice interface with Claude  
- Phone app

When you get to those sections, tell Kilo Code to integrate with existing code rather than rebuild.
