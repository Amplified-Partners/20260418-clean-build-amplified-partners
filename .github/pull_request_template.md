<!--
Reviewer: see AGENTS.md § "PR reviewers" for what to flag vs. ignore.
Author: tick only what applies. Keep answers short.
-->

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
