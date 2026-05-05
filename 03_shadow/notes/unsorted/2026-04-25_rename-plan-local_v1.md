---
title: "Local Rename Plan"
id: "rename-plan-local"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Local Rename Plan

This plan outlines the steps to neutralise local directory and file names.

## Git Safety Protocol
Before executing any rename:
1.  Ensure all repositories are clean (no uncommitted changes).
2.  Create a backup branch/tag: `git tag pre-neutral-rename-20260114`.

## Directory Renames

| Current Path | New Neutral Path | Notes |
|---|---|---|
| `Baselayer/` | `PROJECT_A/` | Top-level container |
| `Baselayer/covered-ai-v2/` | `PROJECT_A/project-b-core/` | Core SaaS platform |
| `Baselayer/covered-ai-website/` | `PROJECT_A/project-b-website/` | Marketing website |
| `Baselayer/covered-ai-marketing/` | `PROJECT_A/project-b-marketing/` | Marketing assets |
| `Baselayer/covered-ai-brand-system/` | `PROJECT_A/project-b-brand-system/` | Brand guidelines |
| `today-mirror/` | `PROJECT_C/` | macOS App |
| `superwhisper/` | `PROJECT_D/` |  |
| `harwebsit/` | `PROJECT_E/` |  |
| `ai-chat-sync/` | `TOOL_SYNC/` |  |
| `ai-stack-auditor/` | `TOOL_AUDITOR/` |  |
| `ai-orchestrator/` | `TOOL_ORCHESTRATOR/` |  |
| `invoice-service/` | `SERVICE_INVOICE/` |  |
| `invoice-api-speedtest/` | `SERVICE_INVOICE_TEST/` |  |

## File Content Neutralisation (Stage 2)

For each renamed directory, perform a search and replace for the original brand terms within the code and documentation.

### PROJECT_A (formerly Baselayer)
-   Replace "Baselayer" with "PROJECT_A"
-   Replace "Covered AI" with "PROJECT_B"

### PROJECT_C (formerly Today Mirror)
-   Replace "Today Mirror" with "PROJECT_C"

### TOOL_SYNC (formerly AI Chat Sync)
-   Replace "AI Chat Sync" with "TOOL_SYNC"

### TOOL_AUDITOR (formerly AI Stack Auditor)
-   Replace "AI Stack Auditor" with "TOOL_AUDITOR"

### TOOL_ORCHESTRATOR (formerly AI Orchestrator)
-   Replace "AI Orchestrator" with "TOOL_ORCHESTRATOR"

## Execution Steps
1.  **Rename Directories**: Execute `mv` commands for top-level directories.
2.  **Update References**: Use `sed` or similar tools to update references in `package.json`, `README.md`, and other config files.
3.  **Verify**: Check for broken links and imports.
