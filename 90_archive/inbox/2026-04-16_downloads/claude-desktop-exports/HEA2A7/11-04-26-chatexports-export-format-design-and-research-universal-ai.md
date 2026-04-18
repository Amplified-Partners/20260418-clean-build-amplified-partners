---
export_version: chatexports
export_date: 2026-04-12
original_date: 2026-04-11
title: export-format-design-and-research
section: 1
total_sections: 7
topics:
  - format-research
  - YAML
  - markdown
  - XML
  - LLM-ingestion
  - token-efficiency
participants:
  - user
  - claude
---

# Export Format Design and Research

## What Happened

User pasted a previous chat about a Python chat-exporter script. Claude exported it in two formats. User then challenged the format assumptions — the original script used YAML/JSON/XML hybrid for universal AI and YAML/XML for Claude. User asked Claude to research whether those formats were actually optimal. Claude searched and found benchmarking data across GPT, Gemini, Llama, and other models.

The research showed YAML had the highest accuracy for nested data (62.1% vs JSON 50.3%), Markdown had the best token efficiency (34-38% fewer tokens than JSON), and XML consistently underperformed on all non-Claude models while using 80% more tokens than Markdown. Claude was specifically trained on XML tags as a prompt organising mechanism per Anthropic's official documentation.

User and Claude agreed on revised formats: YAML front matter + Markdown body for universal AI, XML structure with YAML metadata for Claude.

## Decisions Made

- Universal AI format: YAML metadata + Markdown body, no XML
- Claude format: XML structure with YAML metadata inside
- XML dropped from universal format based on benchmarking evidence
- File naming convention: dd-mm-yy-chatexports-{title}-universal-ai.md and dd-mm-yy-chatexports-{title}-claude-format.xml
- Claude decides the title, chunking, and structure — user just pastes

## Conversation

**User:** Pasted a previous chat about a chat-exporter script. Asked Claude to explain it and create export files.

**Claude:** Exported the chat in two formats. Asked for a title.

**User:** Said Claude should decide the title. Then challenged the format assumptions — asked Claude to research whether YAML/MD/XML for universal AI and YAML/XML for Claude were actually the right choices.

**Claude:** Searched for benchmarking data on LLM format performance. Found studies showing YAML best for accuracy, Markdown best for efficiency, XML worst for non-Claude models. Found Anthropic's documentation confirming Claude was trained on XML tags.

**User:** Asked Claude to research what each major AI model prefers.

**Claude:** Searched for GPT, Gemini, Llama, DeepSeek, Mistral preferences. Found GPT and Gemini perform best with YAML, Llama is format-agnostic, DeepSeek prefers Markdown + XML tags. Concluded YAML + Markdown for universal, XML + YAML for Claude.

**User:** Agreed. Asked Claude to rebuild the exports to the revised spec.

**Claude:** Rebuilt all previous exports and created the updated formats.

## Sources

- improvingagents.com — nested data format benchmarking across GPT, Gemini, Llama
- claude.ai artifact — JSON to Markdown performance guide, 62.1% YAML accuracy figure
- tech4teaching.net — format comparison for human and AI readability
- platform.claude.com — Anthropic's official XML tag documentation
- Anthropic prompt engineering courses on GitHub — XML training confirmation
