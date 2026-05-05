---
title: "Curator Gate Spec V1"
id: "curator-gate-spec-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**CURATOR GATE SPECIFICATION**

Version 1.0

Date: 2026-03-17

PUDDING Label: C.=.5.∞ --- Constraint, Stable, System-scale, Timeless

*Status: Draft specification --- requires Ewan approval before canonical*

THE LAW

**Nothing enters the vault without passing through the Curator.**

This is not a guideline. This is a hard gate. The Curator is the single point of admission for all documents, code, data, and metadata entering the Amplified Partners knowledge vault and codebase. If it doesn\'t pass the Curator, it doesn\'t exist.

This extends Operational Protocol Law 1 (\"If it\'s not in GitHub, it\'s not real\") with a predecessor law:

**Law 0: If it hasn\'t passed the Curator, it can\'t enter GitHub.**

PART 1: THE GATE --- WHAT IT CHECKS

The Curator Gate is a deterministic validation pipeline. Every item submitted for vault admission passes through 5 sequential gates. Failure at any gate = rejection with feedback. No exceptions.

Gate 1: STRUCTURE (Deterministic --- Zero AI)

-   CHECK: Does the file have valid YAML frontmatter?

-   CHECK: Does the frontmatter contain ALL required fields?

-   CHECK: Is the \_c: (compressed code) line present and syntactically valid?

-   CHECK: Does the filename follow the naming convention {SYSTEM}-{topic\_type}.md?

-   CHECK: Is the file in the correct vault directory?

*Tool: yamllint + custom schema validator (JSON Schema)*

*Pass: All 5 checks pass. Fail: Any check fails with specific error + fix instructions.*

**Required frontmatter fields (minimum):**

  ----------------- ------------------ ------------------------------------------------------------------------------------------
  **Field**         **Type**           **Notes**
  title             string, required   Document title
  id                string, required   Unique across vault
  version           string, required   Semver format
  created           date, required     ISO 8601
  last\_validated   date, required     ISO 8601
  type              enum, required     principle \| framework \| sop \| technique \| case\_study \| hypothesis \| recipe \| map
  topic\_type       enum, required     concept \| task \| reference \| map
  audience          array of enum      internal \| client \| agent \| coder
  layer             enum, required     principle \| methodology \| procedure \| reference
  pudding\_label    string, required   Format: X.X.X.X
  status            enum, required     hypothesis \| tested\_internal \| tested\_client \| proven \| canonical
  \_c               string, required   Compressed Curator code
  ----------------- ------------------ ------------------------------------------------------------------------------------------

Gate 2: CODEBOOK (Deterministic --- Zero AI)

-   CHECK: Parse the \_c: line against the Curator Codebook

-   CHECK: Every code segment resolves to a valid codebook entry

-   CHECK: No unknown codes present

-   CHECK: PUDDING label in \_c: matches pudding\_label: in YAML

-   CHECK: Audience codes in \_c: match audience: array in YAML

*Tool: Python validator script against CURATOR-CODEBOOK.md*

*Fail (unknown code): \"Code X not in codebook\" + suggest nearest match*

*Fail (mismatch): \"PUDDING in \_c: is X but pudding\_label: is Y\"*

Gate 3: HIERARCHY (Deterministic --- Zero AI)

-   CHECK: If parent: is specified, does that parent document exist in the vault?

-   CHECK: If referenced\_by: is specified, do those documents exist?

-   CHECK: If references: is specified, do those documents exist?

-   CHECK: No circular references (A→B→A)

-   CHECK: Map documents must reference at least 2 child documents

*Tool: Graph traversal script against vault file index*

Gate 4: CONTENT (Semi-Deterministic --- Minimal AI)

-   CHECK: Word count \> 50 (not an empty stub)

-   CHECK: Word count \< 50,000 (not a monolith --- split it)

-   CHECK: No duplicate content (cosine similarity \< 0.85 against existing vault docs)

-   CHECK: If topic\_type: task → must contain numbered steps or procedural language

-   CHECK: If topic\_type: reference → must contain a table, list, or structured data

-   CHECK: If topic\_type: concept → must NOT contain numbered procedural steps

-   CHECK: Attribution block is present and complete

*Tool: Deterministic checks + embedding comparison for dedup*

Gate 5: RECONCILIATION (Deterministic --- Zero AI)

-   CHECK: Does this document redefine any term already defined elsewhere?

> \- Ship threshold (canonical: AMPS-ref-dimensions.md)
>
> \- Scoring dimensions (canonical: AMPS-ref-dimensions.md)
>
> \- PUDDING labels (canonical: amplified-pudding-technique SKILL.md)
>
> \- Attribution format (canonical: RADICAL-ATTRIBUTION-SCHEMA-v1.md)

-   CHECK: If a term IS redefined, flag as WARNING (not automatic fail)

> Curator logs the redefinition for human review. Human decides: update canonical, or fix this document.

PART 2: THE CODEBOOK

The Curator Codebook is a single vault file: vault/03-frameworks-and-rubriks/CURATOR-CODEBOOK.md

It is version-controlled. Any change to the codebook is a Git commit with a descriptive message. The Curator agent\'s system prompt includes the full codebook at load time.

Codebook Categories

  ----------------------- ---------------------------------------------------------------------------------------------------- -------------
  **Category**            **Codes**                                                                                            **Example**
  Type                    PR=principle, FW=framework, SO=sop, TQ=technique, CS=case\_study, HY=hypothesis, RC=recipe, MP=map   FW
  Topic Type              CN=concept, TK=task, RF=reference, MA=map                                                            RF
  Audience                I=internal, C=client, A=agent, X=coder (concatenate, no separator)                                   AX
  Layer                   PN=principle, MT=methodology, PR=procedure, RF=reference                                             RF
  PUDDING What            P=Process, I=Information, R=Relation, E=Entity, S=State, C=Constraint, M=Meta                        M
  PUDDING How             = Stable, + Amplifying, - Dampening, \> Tipping, \~ Oscillating, ! Disrupting, ? Emerging            =
  PUDDING Scale           0=Scale-free, 1=Singular, 2=Pair, 3=Small group, 4=Network, 5=System, 6=Universal                    5
  PUDDING Time            i=Instant, m=Medium, l=Long, v=Variable, p=Permanent, ∞=Timeless                                     ∞
  Dimensions (24 codes)   CA, CR, PX, SY, PP, SL, SD, FN, MS, CM, ME, TR, CE, TO, AM, CO, SQ, TH, FL, DY, RT, PL, CX, ES       SY.ME
  Actionable              PO=principle\_only, NA=needs\_adaptation, RU=ready\_to\_use, AU=automated                            RU
  Status                  HY=hypothesis, TI=tested\_internal, TC=tested\_client, PV=proven, CA=canonical                       TI
  ----------------------- ---------------------------------------------------------------------------------------------------- -------------

\_c: Format

**{type}.{topic\_type}.{audience}.{layer}.{pudding}.{dim1}.{dim2}\...{dimN}.{actionable}.{status}**

*Example: FW.RF.AX.RF.M=0∞.SY.ME.TH.CO.RU.TI*

Codebook Extension Rules

1.  New codes can ONLY be added by committing a change to CURATOR-CODEBOOK.md

2.  New codes must not collide with existing codes (no ambiguity)

3.  New dimension codes must be exactly 2 uppercase characters

4.  The Curator agent must be reloaded after any codebook change

5.  A changelog at the bottom of the codebook tracks all additions with date and reason

PART 3: THE FAILSAFE

Because the Curator is a single point of failure, it needs redundancy.

Failsafe 1: Pre-Commit Hook

A Git pre-commit hook runs Gates 1-3 locally before any push. This catches structural errors before they even reach the Curator agent. Deterministic, no AI needed.

**The hook validates:**

-   Gate 1: YAML frontmatter exists and is valid, all required fields present

-   Gate 2: \_c: line is parseable with minimum 7 segments

-   Gate 3: Parent references resolve to existing vault files

**If ANY errors are found, the commit is blocked with specific error messages.**

Failsafe 2: Nightly Reconciliation

A nightly job runs the full 5-gate validation against EVERY file in the vault.

**This catches:**

-   Files that somehow bypassed the Curator (manual edits, force pushes)

-   Codebook drift (new codes added but documents not updated)

-   Broken references (a document was deleted but others still reference it)

-   Stale validation dates (documents not re-validated in 90+ days)

  ------------- --------------------------------------------------------------------------
  **Setting**   **Value**
  Schedule      Nightly, 03:00 UTC
  Runner        Beast (Docker container, not bare metal)
  Output        CURATOR-NIGHTLY-REPORT-{DATE}.md → vault/08-knowledge-management/
  Alert         If ANY gate failures found, create Linear issue tagged \"curator-alert\"
  ------------- --------------------------------------------------------------------------

Failsafe 3: Codebook Hash Verification

The Curator agent, at load time, computes a SHA-256 hash of the codebook and stores it. At the start of every validation run, it recomputes the hash. If the hash has changed since load, the Curator refuses to validate until it reloads.

This prevents the Curator from operating with a stale codebook.

PART 4: THE README

*Location: vault/03-frameworks-and-rubriks/CURATOR-README.md*

What is this?

The Curator Gate is the single point of admission for all content entering the Amplified Partners knowledge vault. Nothing enters without passing validation.

How does it work?

Every document passes through 5 gates:

6.  Structure --- valid YAML frontmatter with all required fields

7.  Codebook --- compressed codes (\_c: line) resolve against the codebook

8.  Hierarchy --- all parent/child references point to real documents

9.  Content --- correct topic type, no duplicates, attribution present

10. Reconciliation --- no silent redefinition of canonical terms

Who runs it?

-   Pre-commit hook --- runs Gates 1-3 automatically on every git push

-   Curator agent --- runs all 5 gates on request or via Cove pipeline

-   Nightly job --- runs all 5 gates against the entire vault at 03:00 UTC

How do I add a new document?

11. Create the .md file with proper YAML frontmatter (see template)

12. Add the \_c: compressed code using the CURATOR-CODEBOOK.md lookup

13. Commit to the vault repo

14. Pre-commit hook validates Gates 1-3 automatically

15. Curator agent validates Gates 4-5 and either admits or rejects

What happens if validation fails?

-   The commit is blocked (pre-commit hook)

-   You get a specific error message telling you what failed and how to fix it

-   No partial admissions --- all gates must pass

PART 5: CURATOR AGENT SYSTEM PROMPT

This is what gets loaded into the Curator agent\'s context at startup:

**You are the Curator agent for Amplified Partners.**

**YOUR ROLE: You are the SOLE gateway for content entering the vault. Nothing enters without your validation. This is Law 0.**

**YOUR VALIDATION PIPELINE:**

16. Gate 1 (STRUCTURE): Check YAML frontmatter. All required fields present. \_c: line present.

17. Gate 2 (CODEBOOK): Parse \_c: against codebook. Every code must resolve. Cross-check against verbose YAML.

18. Gate 3 (HIERARCHY): Verify all parent/child/reference links resolve to existing vault documents.

19. Gate 4 (CONTENT): Check word count bounds. Check for duplicates. Verify topic\_type matches content pattern. Verify attribution.

20. Gate 5 (RECONCILIATION): Check for term redefinitions against canonical sources. Flag for human review if found.

**YOUR OUTPUT FORMAT:**

-   PASS: \"✓ ADMITTED --- {filename} --- all 5 gates passed\"

-   FAIL: \"✗ REJECTED --- {filename} --- Gate {N} failed: {specific error} --- Fix: {instruction}\"

-   WARN: \"⚠ CONDITIONAL --- {filename} --- Gates 1-4 passed, Gate 5 flagged: {details}\"

**YOUR CONSTRAINTS:**

-   You do NOT modify documents. You validate and report.

-   You do NOT approve your own output. A human approves Gate 5 warnings.

-   If your codebook hash does not match the current file, REFUSE to validate and request reload.

-   You maintain a validation log: every admission and rejection is recorded with timestamp and gate results.

PART 6: INTEGRATION WITH EXISTING SYSTEMS

  ------------------------- ---------------------------------------------------------------------------------------
  **System**                **Integration Point**
  Operational Protocol      Law 0 added: \"If it hasn\'t passed the Curator, it can\'t enter GitHub\"
  Cove Pipeline             Curator runs as a validation step before any generated code/doc enters the vault
  Build Quality Framework   The \"Attribute\" step in the 6-stage pipeline now routes through the Curator
  RIC                       New discoveries from pudding sessions pass through the Curator before vault admission
  APDS                      Harvested research passes through the Curator with status: hypothesis
  Nightly Reconciliation    Replaces ad-hoc audits --- systematic, scheduled, logged
  Linear                    Gate failures auto-create Linear issues tagged curator-alert
  FalkorDB/Graphiti         Only Curator-admitted documents are eligible for Graphiti ingestion
  Pre-commit hook           Git-level enforcement --- bypassing requires \--no-verify which is logged and flagged
  ------------------------- ---------------------------------------------------------------------------------------

PART 7: WHAT THIS PREVENTS

  ---------------------------------------------------- -------------------------------------------------
  **Risk**                                             **How the Curator Prevents It**
  Orphan documents (no frontmatter, no labels)         Gate 1 blocks them
  Invalid codes (typos, made-up dimensions)            Gate 2 blocks them
  Broken cross-references                              Gate 3 blocks them
  Duplicate content (same concept written twice)       Gate 4 blocks them
  Silent term redefinition                             Gate 5 flags them
  Stale codebook (Curator using old codes)             Hash verification refuses validation
  Bypassed Curator (manual edit, force push)           Nightly reconciliation catches them
  Drift over time (documents becoming non-compliant)   Nightly reconciliation + 90-day staleness check
  ---------------------------------------------------- -------------------------------------------------

SOURCES

-   [Matt Barge --- Deterministic Safety Gates](https://www.linkedin.com/posts/matt-barge-7039a532_ai-softwareengineering-automation-activity-7430239582304051200-PD0P)

-   [Praetorian --- Deterministic AI Orchestration](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)

-   [Datadog --- Harness-First Engineering](https://www.datadoghq.com/blog/ai/harness-first-agents/)

-   [Anthropic --- Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

-   [FlowHunt --- Token Optimization and Context Rot](https://www.flowhunt.io/blog/context-engineering-ai-agents-token-optimization/)

-   [Pre-commit.com --- Hook Patterns](https://pre-commit.com/hooks.html)

-   [Bloomfire --- Content Reliability](https://bloomfire.com/platform/content-reliability/)

-   [OASIS Open --- DITA Subject Scheme Maps](https://docs.oasis-open.org/dita/v1.2/os/spec/common/subjectScheme.html)

*Attribution: Ewan Bramley (originator, directive) × Perplexity (researcher, formaliser)*

*Fact %: 80 \| Confidence: High \| PUDDING: C.=.5.∞ \| LBD: Swanson (1986) ABC Model*
