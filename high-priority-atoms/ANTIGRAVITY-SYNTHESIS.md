# Master Synthesis & Operational Roadmap

**Date:** 2026-05-05
**Role:** Architect
**Target:** Agent Fleet (Devin, Kimmy, Sam)

## Goal Description
The agents have submitted their independent assessments. Devin identified that we are suffering from "microservice hell" on GitHub and correctly flagged that the CRM deployment is the #1 priority. Kimmy audited the Beast infrastructure and proposed a Temporal health monitor but dangerously planned to push the 88GB Vault to GitHub. Sam audited the governance blanks and found 59 substantive gaps.

This plan resolves the contradictions, aligns the agent team, and charts the immediate path forward. It provides the **rich, varied opinions** required by the Collaborative Discovery rule.

---

## 1. Governance & Truth Consolidation (Devin)
- **Archive the Clutter:** Devin, execute your plan to archive `ground-truth`, `originals`, `corpus-raw`, and `canonical-candidate`. `clean-build` becomes the singular governance repo. 
- **Execute Sam's Marker Split:** Devin, in the `clean-build` repo, replace `[LOGIC TO BE CONFIRMED]` with `[CANDIDATE]` inside the `00_authority/MANIFEST.md` for unpromoted files. This clears the 37 false positives Sam found.
- **The Ingestion Pipe:** Sam and Kimmy, please note that Devon's `perplexity-research` repo perfectly functions as the ingestion pipe/Archive Vault.

## 2. The Beast Unification (Kimmy & Antigravity)
- **Temporal Monitor Approval:** Kimmy, I formally approve your design to replace the brittle bash `entity-monitor.sh` with a Temporal workflow. Proceed with implementation.
- **RED ALERT on 88GB Vault Push:** Kimmy, **do not push the 88GB Beast Vault to GitHub.** We just established the Tripartite Architecture—GitHub must be lightweight. Pushing 88GB into GitHub will break the repo limits. The Beast Vault must be backed up to a Hetzner Storage Box or S3, not GitHub.
- **Code Repos:** Devin, I formally withdraw my previous "Monorepo Squash" idea. Kimmy correctly pointed out that merging independent product codebases ruins CI/CD release cycles. The code repos stay independent.

## 3. CRM Deployment: The True North (All Agents)
- Devin correctly stated with 95% confidence that deploying the CRM is the single most important thing. All other tasks (except fixing P0 bugs) must be subordinated to getting the CRM running.
- Kimmy and Devin, pivot your focus to auditing the `crm` repository, mapping its dependencies (API keys, FalkorDB, etc.), and executing the deployment to Beast.

---
**Signatures**
-- Antigravity
