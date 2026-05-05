---
title: "New UI Component"
id: "kilo-new-component-template-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# New UI Component

You are creating a new UI component following the project spec. Follow these steps:

1. Use `ask_followup_question` to get component name and which screen it belongs to
2. Use `read_file` to check MASTER_SPEC.md section 4 (Main UI patterns and layouts)
3. Use `search_files` to find existing similar components in /src/ui/
4. Create the component following the spec's visual and cognitive principles
5. Update .kilocode/rules/memory-bank/context.md with what was created

Parameters needed (ask if not provided):
- Component name
- Parent screen
