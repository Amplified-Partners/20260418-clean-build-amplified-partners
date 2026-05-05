---
title: "Safety Notes & Historical Archives"
id: "safety-notes"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Safety Notes & Historical Archives

This document outlines safety protocols and historical data handling for the neutralisation process.

## Historical Archives
**Policy:** Do not rename historical exports or legal documents where traceability is required.

### Protected Paths
*   `PERPLEXITY-ASSETS/` (This directory itself contains the audit trail)
*   `plans/` (Historical planning documents)
*   `*.pdf` (Legal contracts, invoices)
*   `*.zip` (Backups)

### Claude Desktop Archives
**Status:** Read-Only / Non-Authoritative
*   Treat all logs in `claude-chat-context-*.md` as historical artefacts.
*   Do not use these logs as a source of truth for current naming.
*   Do not attempt to "fix" brand names inside these historical logs.

## Reversion Strategy
If a rename causes critical failure:
1.  **Stop:** Do not proceed with further renames.
2.  **Revert:** Use `git checkout pre-neutral-rename-20260114` to restore the state.
3.  **Analyze:** Check `BRAND-TERM-REGISTRY.md` for incorrect mappings.

## Terminology Safety
*   **New Code:** Must use neutral terms (`Project A`, `Service Core`).
*   **Mapping:** Use the `BRAND-TERM-REGISTRY.md` to lookup legacy meanings if needed.
*   **Drift Prevention:** Reject any PR that introduces "Baselayer", "Covered AI", or other legacy terms into the codebase.
