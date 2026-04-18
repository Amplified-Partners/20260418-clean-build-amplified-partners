---
title: Promotion gate (candidate → authoritative)
date: 2026-04-16
version: 1
status: draft
---

## Purpose

Define the **minimum bar** for promoting an artifact from **Candidate authority** to **Authoritative now**.

This gate is designed to be:

- minimal (low friction)
- mechanical (repeatable)
- scalable (works when hundreds of documents arrive)

## Minimum bar (must all hold)

An artifact may be promoted only if it:

1. **Has provenance**: includes a source path (or is natively created in this repo) and no invented claims.
2. **Is runnable**: written so an agent can execute it without guessing (inputs → steps → outputs → failure modes).
3. **Is denoised**: contains only content that reduces cognitive load or produces changes to routing/constraints/acceptance criteria or resolves a `[DECISION REQUIRED]`.
4. **Has explicit tokens**: any uncertainty is marked (`[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`, `[DECISION REQUIRED]`); no silent ambiguity.
5. **Does not violate privacy**: no secrets; no unnecessary personal identifiers.

## Promotion procedure (mechanical)

1. Update `00_authority/MANIFEST.md`: move the artifact entry from **Candidate authority** to **Authoritative now**.
2. Add a short entry to `00_authority/DECISION_LOG.md` recording the promotion (what, why, and any remaining tokens).
