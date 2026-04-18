---
export_version: chatexports
export_date: 2026-04-12
original_date: 2026-04-11
title: chatexport-skill-development-and-accuracy-methodology
section: 2
total_sections: 7
topics:
  - skill-creation
  - accuracy-vs-interpretation
  - chinese-whispers
  - living-document
  - feedback-loop
participants:
  - user
  - claude
---

# Chatexport Skill Development and Accuracy Methodology

## What Happened

Claude built a chatexport skill. User reviewed the first exports and identified that Claude was interpreting rather than reflecting — adding editorial framing, narrative, emotional labels not present in the original text. User said the exports were "interpretations not reflections."

User identified the root cause as the instructions, not the execution. The skill's wording — "summarising," "capture meaning," "condensed to their essential point" — invited interpretation. User directed Claude to fix the instructions, not the output.

The skill was rewritten multiple times. User added requirements: this is a living document, understanding intent is critical before proceeding, every execution must document what/where/when/how/went well/caused problem. User stated "the instructions are the problem not the execution of them."

User also specified the process for handling a chat: read once for overview, break into logical sections, refresh context for each section, examine in detail, export in two formats, validate before saving, repeat. User wrote this as a separate handling document.

## Decisions Made

- Exports must reflect what was said, not interpret what it meant
- No adjectives, narrative framing, or emotional labels not in the original
- "No Chinese whispers" — the next intelligence reads what happened, not the exporter's version
- The goal is to avoid the cascade of errors that comes from corrupted data
- The instructions are the system. The AI is the partner. Fix the instructions when output is wrong.
- Every export includes a feedback report: what, where, when, how, went well, caused problem
- This is a living document — it improves from honest records of what worked and what didn't
- Understanding intent is critical — do not proceed without it

## Conversation

**User:** Reviewed the OpenClaw chat exports. Said they were "interpretations not reflections."

**Claude:** Acknowledged the editorialising. Asked whether to redo the files or apply the correction going forward.

**User:** Said to fix the instructions that allowed the interpretation, not the output. "The goal to avoid Chinese whispers."

**Claude:** Identified the ambiguous wording in the skill — "summarising," "capture meaning," "condensed to their essential point." Rewrote those sections to say "reflect what was said" and "no adjectives not in the original."

**User:** Specified the full process: read once for overview, break into sections, refresh context, examine in detail, export, validate, repeat. Said each section should be a separate file pair. Said statistics are secondary to clarity.

**Claude:** Rewrote the skill from scratch with the new process.

**User:** Added: this is a living document, understanding intent is critical, document successes and failures every time. Said "the instructions are the problem not the execution of them."

**Claude:** Added living document section, intent section, and feedback loop to the skill.

**User:** Added: this is a critical foundational skill, everything will be built from this, leave space for the AI to do its best work.

**Claude:** Added the foundational context and space for judgment to the skill.

**User:** Asked Claude to research the principle that instructions are the problem, not the execution.

**Claude:** Found Deming's "blame the process not the people" principle (1992) — 94% of performance variation is caused by the system, not the worker. Found the LLM taxonomy paper classifying prompt defects with "Specification & Intent" as the first category of failure. Both supported user's position.
