<!--
Reviewer: see AGENTS.md § "PR reviewers" for what to flag vs. ignore.
Author: tick only what applies. Keep answers short.

Authored by Devon (Devin session 4cc8b0d727684f94a8f055853099d8e6), 2026-04-23.
Updated by Devon-4330 | 2026-05-03 | session devin-4330c661a80b4770aa8f62980c21366a — added Linear ticket section per AMP-70.
-->

## Linear ticket

<!-- Required. PR title or this section must reference an AMP-NNN ticket (where NNN is the actual ticket number). -->
<!-- Replace the placeholder below with the real ticket number. -->

AMP-

## What changed

One or two sentences. What and why.

## Mode (per AGENTS.md)

- [ ] Act — reversible or contained-impact
- [ ] Surface — significant / irreversible, with `DECISION_LOG.md` pointer below
- [ ] Park — stuck, escalation note attached

## Pre-merge checklist

- [ ] Signatures present on every committed artefact (`00_authority/SIGNATURES.md`)
- [ ] If `00_authority/*` touched: version bumped + changelog entry added
- [ ] If new authoritative rule or irreversible commit: `00_authority/DECISION_LOG.md` pointer added
- [ ] Every file reference points to a thing that exists (or is marked `[SOURCE REQUIRED]`)
- [ ] Examples do not contradict their own rule
- [ ] New indexable files (`00_authority/*`, `01_truth/processes/*`, etc.) appear in `00_authority/MANIFEST.md`

## Surface link (only if Mode = Surface)

<!-- Link to the DECISION_LOG.md entry this PR surfaces -->

## Notes to reviewer

Anything the reviewer should know that is not in the diff — e.g. a known limitation, a follow-up PR planned, an open question for the architect.
