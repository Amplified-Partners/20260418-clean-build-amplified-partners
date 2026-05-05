---
title: "Start Session"
id: "kilo-start-session-template-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Start Session

You are resuming work on the personal assistant project. Follow these steps:

1. Use `read_file` to read all files in .kilocode/rules/memory-bank/
2. Use `read_file` to read MASTER_SPEC.md
3. Summarise current project status based on context.md
4. Use `ask_followup_question` to ask what the user wants to work on today

Parameters needed (ask if not provided):
- None
