---
title: "Neutral Factory Rebuild Plan"
id: "neutral-factory-rebuild"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Neutral Factory Rebuild Plan

This plan outlines the steps to rebuild the "factory" (the development system) to be brand-agnostic.

## Core Documentation Rewrite

### KILO-BUILD-FACTORY.md
**Current State:** Likely contains references to "Baselayer" or specific project workflows.
**Goal:** Rewrite as a generic "Multi-Agent AI Development Factory".

**Changes:**
1.  **Title:** Change to "AI Development Factory - Build Guide".
2.  **Terminology:**
    *   Replace "Baselayer" with "Target Project".
    *   Replace "Covered AI" with "SaaS Product".
    *   Replace specific agent names if they are branded (e.g., "Baselayer Architect" -> "System Architect").
3.  **Examples:** Ensure all code examples use generic placeholders like `project-x`, `service-y`.

### README.md (Factory Root)
**Goal:** Create a neutral entry point for the system.

**Content Structure:**
1.  **Introduction:** "Welcome to the AI Development Factory."
2.  **Capabilities:** List generic capabilities (e.g., "SaaS Builder", "iOS App Generator").
3.  **Getting Started:** "To start a new project, run..."
4.  **Terminology Safety:** Link to the Terminology Safety Guidelines.

### EXECUTIONCHECKLIST.md
**Goal:** A generic checklist for running the factory.

**Changes:**
1.  **Steps:** Ensure steps are generic (e.g., "Define Project Scope" instead of "Define Baselayer Module").
2.  **Variables:** Use `${PROJECT_NAME}` notation in commands.

## Terminology Safety Guidelines
**Location:** `PERPLEXITY-ASSETS/TERMINOLOGY-SAFETY.md` (to be created)

**Content:**
1.  **The Rule:** "Brand semantics live in a separate layer."
2.  **Mapping:** "Always use the Brand Term Registry to map generic names to specific brands."
3.  **Prohibition:** "Never hardcode brand names in factory prompts or configurations."
4.  **Enforcement:** "Code reviews must check for brand leakage."

## Implementation Steps
1.  **Draft:** Create neutral versions of the documents in `PERPLEXITY-ASSETS/neutral-docs/`.
2.  **Review:** Verify no brand terms exist.
3.  **Replace:** Overwrite the original files in the root directory (after backup).
