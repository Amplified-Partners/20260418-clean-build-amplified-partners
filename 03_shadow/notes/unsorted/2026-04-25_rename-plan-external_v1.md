---
title: "External Surface Rename Plan"
id: "rename-plan-external"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# External Surface Rename Plan

This plan outlines the steps to neutralise brand terms on external platforms.

## GitHub Repositories

| Current Repo Name | New Neutral Name | Action |
|---|---|---|
| `baselayer-workspace` | `project-a-workspace` | Rename |
| `covered-ai-v2` | `project-b-core` | Rename |
| `today-mirror` | `project-c-app` | Rename |
| `ai-chat-sync` | `tool-sync` | Rename |
| `ai-stack-auditor` | `tool-auditor` | Rename |
| `ai-orchestrator` | `tool-orchestrator` | Rename |

### Action Items
1.  **Rename Repos:** Go to GitHub Settings > General and rename each repository.
2.  **Update Remotes:** Update local git remotes to point to the new URLs.
    *   `git remote set-url origin <new_url>`
3.  **Update CI/CD:** Check GitHub Actions workflows for hardcoded repo names.

## Railway Projects

| Current Project Name | New Neutral Name | Action |
|---|---|---|
| `covered-ai-backend` | `project-b-backend` | Rename |
| `ai-orchestrator` | `tool-orchestrator-service` | Rename |

### Action Items
1.  **Rename Project:** Go to Railway Project Settings and rename.
2.  **Update CLI:** If using Railway CLI, update the project link.

## Social Media & Public Surfaces

| Platform | Handle/URL | Action |
|---|---|---|
| LinkedIn | `Covered AI` | Rename to `Project B` or Archive |
| Website | `covered-ai.com` | Redirect to `project-b.com` (or placeholder) |

### Action Items
1.  **Audit:** Check all social media profiles linked in documentation.
2.  **Rename/Archive:** Rename accounts if possible, or archive them if the brand is being fully retired.
