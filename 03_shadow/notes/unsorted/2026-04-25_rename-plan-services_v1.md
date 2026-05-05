---
title: "Service & Config Neutralisation Plan"
id: "rename-plan-services"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Service & Config Neutralisation Plan

This plan outlines the steps to neutralise brand terms in services and configurations.

## Kilo Code Configuration
**Location:** `.kilocode/`

### Action Items
1.  **Review Modes:** Check `.kilocode/modes.json` (or equivalent) for brand-specific mode names.
    *   *Action:* Rename any brand-specific modes to generic roles (e.g., "Baselayer Dev" -> "Project A Dev").
2.  **Review Rules:** Check `.kilocode/rules/` for brand-specific rules.
    *   *Action:* Rename rule files (e.g., `baselayer-rules.md` -> `project-a-rules.md`) and update content.
3.  **Review Memory Bank:** Check `.kilocode/memory-bank/` for project overviews.
    *   *Action:* Update `PROJECT_OVERVIEW.md` to use neutral names.

## Railway Services
**Scope:** External Service (Railway.app)

### Action Items
1.  **Rename Projects:**
    *   `covered-ai-backend` -> `project-b-backend`
    *   `ai-orchestrator` -> `tool-orchestrator-service`
2.  **Rename Environments:**
    *   Ensure environment names are generic (e.g., `production`, `staging`, `dev`) and do not contain brand qualifiers.
3.  **Review Environment Variables:**
    *   Check for variables like `BASELAYER_API_KEY` or `COVERED_AI_SECRET`.
    *   *Action:* Create new neutral variables (e.g., `PROJECT_A_API_KEY`) and update code to use them. Keep old ones as aliases during transition.

## Qdrant Collections
**Scope:** Vector Database

### Action Items
1.  **List Collections:** Identify collections with brand names (e.g., `baselayer_docs`, `covered_ai_knowledge`).
2.  **Create New Collections:** Create new collections with neutral names (e.g., `project_a_docs`, `project_b_knowledge`).
3.  **Migrate Data:** Re-index data into the new collections.
4.  **Update Code:** Update the AI Orchestrator and other tools to query the new collections.
5.  **Deprecate:** Delete old collections after verification.

## Obsidian Vaults
**Scope:** Knowledge Management

### Action Items
1.  **Vault Names:** If vaults are named after brands, rename the local folders (covered in Local Rename Plan).
2.  **Internal Links:** Use Obsidian's rename functionality (or a script) to update internal links if file names change.
3.  **Tags:** Review tags for brand names (e.g., `#baselayer`, `#covered-ai`).
    *   *Action:* Bulk rename tags to neutral equivalents (e.g., `#project-a`, `#project-b`).
