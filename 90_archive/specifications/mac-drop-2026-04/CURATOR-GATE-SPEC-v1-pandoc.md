Curator Gate Specification v1.0
===============================

**Date**: 2026-03-17 **PUDDING Label**: `C.=.5.∞` --- Constraint,
Stable, System-scale, Timeless **Status**: Draft specification ---
requires Ewan approval before canonical

THE LAW
-------

**Nothing enters the vault without passing through the Curator.**

This is not a guideline. This is a hard gate. The Curator is the single
point of admission for all documents, code, data, and metadata entering
the Amplified Partners knowledge vault and codebase. If it doesn't pass
the Curator, it doesn't exist.

This extends Operational Protocol Law 1 ("If it's not in GitHub, it's
not real") with a predecessor law:

> **Law 0: If it hasn't passed the Curator, it can't enter GitHub.**

PART 1: THE GATE --- WHAT IT CHECKS
-----------------------------------

The Curator Gate is a deterministic validation pipeline. Every item
submitted for vault admission passes through 5 sequential gates. Failure
at any gate = rejection with feedback. No exceptions.

### Gate 1: STRUCTURE (Deterministic --- Zero AI)

    CHECK: Does the file have valid YAML frontmatter?
    CHECK: Does the frontmatter contain ALL required fields?
    CHECK: Is the _c: (compressed code) line present and syntactically valid?
    CHECK: Does the filename follow the naming convention {SYSTEM}-{topic_type}.md?
    CHECK: Is the file in the correct vault directory?

    TOOL: yamllint + custom schema validator (JSON Schema)
    PASS: All 5 checks pass
    FAIL: Any check fails → return specific error + fix instructions

Required frontmatter fields (minimum):

    ---
    title: [string, required]
    id: [string, required, unique across vault]
    version: [string, required, semver]
    created: [date, required, ISO 8601]
    last_validated: [date, required, ISO 8601]
    type: [enum: principle|framework|sop|technique|case_study|hypothesis|recipe|map]
    topic_type: [enum: concept|task|reference|map]
    audience: [array of enum: internal|client|agent|coder]
    layer: [enum: principle|methodology|procedure|reference]
    pudding_label: [string, required, format: X.X.X.X]
    status: [enum: hypothesis|tested_internal|tested_client|proven|canonical]
    _c: [string, required, compressed Curator code]
    ---

### Gate 2: CODEBOOK (Deterministic --- Zero AI)

    CHECK: Parse the _c: line against the Curator Codebook
    CHECK: Every code segment resolves to a valid codebook entry
    CHECK: No unknown codes present
    CHECK: PUDDING label in _c: matches pudding_label: in YAML
    CHECK: Audience codes in _c: match audience: array in YAML

    TOOL: Python validator script against CURATOR-CODEBOOK.md
    PASS: All codes resolve, all cross-checks match
    FAIL: Unknown code → return "Code X not in codebook" + suggest nearest match
    FAIL: Mismatch → return "PUDDING in _c: is X but pudding_label: is Y"

### Gate 3: HIERARCHY (Deterministic --- Zero AI)

    CHECK: If parent: is specified, does that parent document exist in the vault?
    CHECK: If referenced_by: is specified, do those documents exist?
    CHECK: If references: is specified, do those documents exist?
    CHECK: No circular references (A→B→A)
    CHECK: Map documents must reference at least 2 child documents

    TOOL: Graph traversal script against vault file index
    PASS: All references resolve to existing documents
    FAIL: Broken reference → return "parent: AMPS-concept not found in vault"

### Gate 4: CONTENT (Semi-Deterministic --- Minimal AI)

    CHECK: Word count > 50 (not an empty stub)
    CHECK: Word count < 50,000 (not a monolith — split it)
    CHECK: No duplicate content (cosine similarity < 0.85 against existing vault docs)
    CHECK: If topic_type: task → must contain numbered steps or procedural language
    CHECK: If topic_type: reference → must contain a table, list, or structured data
    CHECK: If topic_type: concept → must NOT contain numbered procedural steps
    CHECK: Attribution block is present and complete

    TOOL: Deterministic checks + embedding comparison for dedup
    PASS: All checks pass
    FAIL: Duplicate detected → return "85%+ similarity with {existing_doc}. Merge or differentiate."
    FAIL: Type mismatch → return "topic_type is 'task' but no procedural steps found"

### Gate 5: RECONCILIATION (Deterministic --- Zero AI)

    CHECK: Does this document redefine any term already defined elsewhere?
      - Ship threshold (canonical: AMPS-ref-dimensions.md)
      - Scoring dimensions (canonical: AMPS-ref-dimensions.md)
      - PUDDING labels (canonical: amplified-pudding-technique SKILL.md)
      - Attribution format (canonical: RADICAL-ATTRIBUTION-SCHEMA-v1.md)
    CHECK: If a term IS redefined, flag as WARNING (not automatic fail)
      - Curator logs the redefinition for human review
      - Human decides: update canonical, or fix this document

    TOOL: Term extraction + comparison against canonical definitions list
    PASS: No redefinitions, or redefinitions approved by human
    WARN: Redefinition detected → human review required before admission

PART 2: THE CODEBOOK
--------------------

The Curator Codebook is a single vault file:
`vault/03-frameworks-and-rubriks/CURATOR-CODEBOOK.md`

It is version-controlled. Any change to the codebook is a Git commit
with a descriptive message. The Curator agent's system prompt includes
the full codebook at load time.

### Codebook Format

    # CURATOR-CODEBOOK.md
    # Version: 1.0
    # Last updated: 2026-03-17
    # This file is loaded into the Curator agent's system prompt.
    # All codes below are the ONLY valid codes for the _c: field.

    codebook:
      type:
        PR: principle
        FW: framework
        SO: sop
        TQ: technique
        CS: case_study
        HY: hypothesis
        RC: recipe
        MP: map

      topic_type:
        CN: concept
        TK: task
        RF: reference
        MA: map

      audience:  # Concatenate, no separator. Order: I, C, A, X
        I: internal
        C: client
        A: agent
        X: coder

      layer:
        PN: principle
        MT: methodology
        PR: procedure
        RF: reference

      pudding_what:
        P: Process
        I: Information
        R: Relation
        E: Entity
        S: State
        C: Constraint
        M: Meta

      pudding_how:
        "=": Stable
        "+": Amplifying
        "-": Dampening
        ">": Tipping
        "~": Oscillating
        "!": Disrupting
        "?": Emerging

      pudding_scale:
        "0": Scale-free
        "1": Singular
        "2": Pair
        "3": Small group
        "4": Network
        "5": System
        "6": Universal

      pudding_time:
        i: Instant
        m: Medium
        l: Long
        v: Variable
        p: Permanent
        "∞": Timeless

      dimensions:
        CA: customer_acquisition
        CR: customer_retention
        PX: pricing
        SY: systems
        PP: people
        SL: sales
        SD: service_delivery
        FN: finance
        MS: mindset
        CM: communication
        ME: measurement
        TR: trust
        CE: cause_effect
        TO: trade_off
        AM: amplifier
        CO: constraint
        SQ: sequence
        TH: threshold
        FL: feedback_loop
        DY: decay
        RT: routing
        PL: parallelism
        CX: compression
        ES: escalation

      actionable:
        PO: principle_only
        NA: needs_adaptation
        RU: ready_to_use
        AU: automated

      status:
        HY: hypothesis
        TI: tested_internal
        TC: tested_client
        PV: proven
        CA: canonical

    # _c: format
    # {type}.{topic_type}.{audience}.{layer}.{pudding_what}{pudding_how}{pudding_scale}{pudding_time}.{dim1}.{dim2}...{dimN}.{actionable}.{status}
    # Example: FW.RF.AX.RF.M=0∞.SY.ME.TH.CO.RU.TI

### Codebook Extension Rules

1.  New codes can ONLY be added by committing a change to
    CURATOR-CODEBOOK.md
2.  New codes must not collide with existing codes (no ambiguity)
3.  New dimension codes must be exactly 2 uppercase characters
4.  The Curator agent must be reloaded after any codebook change
5.  A changelog section at the bottom of the codebook tracks all
    additions with date and reason

PART 3: THE FAILSAFE
--------------------

Because the Curator is a single point of failure, it needs redundancy.

### Failsafe 1: Pre-Commit Hook (Deterministic, No AI Needed)

A Git pre-commit hook runs Gates 1-3 locally before any push. This
catches structural errors before they even reach the Curator agent.

    #!/bin/bash
    # .git/hooks/pre-commit — Curator Gate (Lightweight)
    # Runs Gates 1-3 deterministically. No AI required.

    VAULT_DIR="vault"
    CODEBOOK="vault/03-frameworks-and-rubriks/CURATOR-CODEBOOK.md"
    ERRORS=0

    for file in $(git diff --cached --name-only --diff-filter=ACM | grep "^vault/.*\.md$"); do
      # Gate 1: YAML frontmatter exists and is valid
      if ! head -1 "$file" | grep -q "^---$"; then
        echo "GATE 1 FAIL: $file — missing YAML frontmatter"
        ERRORS=$((ERRORS + 1))
        continue
      fi

      # Gate 1: Required fields present
      for field in title id version created type topic_type audience layer pudding_label status _c; do
        if ! grep -q "^${field}:" "$file"; then
          echo "GATE 1 FAIL: $file — missing required field: $field"
          ERRORS=$((ERRORS + 1))
        fi
      done

      # Gate 2: _c line parseable (basic syntax check)
      C_LINE=$(grep "^_c:" "$file" | head -1 | sed 's/^_c: *//' | tr -d '"')
      if [ -z "$C_LINE" ]; then
        echo "GATE 2 FAIL: $file — _c: line empty or missing"
        ERRORS=$((ERRORS + 1))
      else
        # Count segments (should be at least 7: type.topic.aud.layer.pudding.dim.action.status)
        SEGMENTS=$(echo "$C_LINE" | tr '.' '\n' | wc -l)
        if [ "$SEGMENTS" -lt 7 ]; then
          echo "GATE 2 FAIL: $file — _c: has $SEGMENTS segments (minimum 7)"
          ERRORS=$((ERRORS + 1))
        fi
      fi

      # Gate 3: Parent reference check (if specified)
      PARENT=$(grep "^parent:" "$file" | head -1 | sed 's/^parent: *//' | tr -d '"')
      if [ -n "$PARENT" ] && [ "$PARENT" != "null" ] && [ "$PARENT" != "~" ]; then
        PARENT_FILE=$(find "$VAULT_DIR" -name "${PARENT}*" -type f 2>/dev/null | head -1)
        if [ -z "$PARENT_FILE" ]; then
          echo "GATE 3 FAIL: $file — parent '$PARENT' not found in vault"
          ERRORS=$((ERRORS + 1))
        fi
      fi
    done

    if [ "$ERRORS" -gt 0 ]; then
      echo ""
      echo "╔══════════════════════════════════════════╗"
      echo "║  CURATOR GATE: $ERRORS ERROR(S) FOUND       ║"
      echo "║  Commit blocked. Fix errors and retry.   ║"
      echo "╚══════════════════════════════════════════╝"
      exit 1
    fi

    echo "✓ Curator Gate: All checks passed"
    exit 0

### Failsafe 2: Nightly Reconciliation (Automated, Scheduled)

A nightly job runs the full 5-gate validation against EVERY file in the
vault. This catches: - Files that somehow bypassed the Curator (manual
edits, force pushes) - Codebook drift (new codes added but documents not
updated) - Broken references (a document was deleted but others still
reference it) - Stale validation dates (documents not re-validated in
90+ days)

    Schedule: Nightly, 03:00 UTC
    Runner: Beast (Docker container, not bare metal)
    Output: CURATOR-NIGHTLY-REPORT-{DATE}.md → vault/08-knowledge-management/
    Alert: If ANY gate failures found, create Linear issue tagged "curator-alert"

### Failsafe 3: Codebook Hash Verification

The Curator agent, at load time, computes a SHA-256 hash of the codebook
and stores it. At the start of every validation run, it recomputes the
hash. If the hash has changed since load, the Curator refuses to
validate until it reloads.

This prevents the Curator from operating with a stale codebook.

    import hashlib

    def verify_codebook(codebook_path, stored_hash):
        with open(codebook_path, 'r') as f:
            current_hash = hashlib.sha256(f.read().encode()).hexdigest()
        if current_hash != stored_hash:
            raise CodebookDriftError(
                f"Codebook changed since Curator loaded. "
                f"Stored: {stored_hash[:12]}... Current: {current_hash[:12]}... "
                f"Curator must reload before validating."
            )
        return True

PART 4: THE README
------------------

A concise README lives alongside the codebook. Published to the vault,
and optionally to a public-facing page for transparency.

### Location: `vault/03-frameworks-and-rubriks/CURATOR-README.md`

    # Curator Gate — README

    ## What is this?
    The Curator Gate is the single point of admission for all content entering the
    Amplified Partners knowledge vault. Nothing enters without passing validation.

    ## How does it work?
    Every document passes through 5 gates:
    1. **Structure** — valid YAML frontmatter with all required fields
    2. **Codebook** — compressed codes (_c: line) resolve against the codebook
    3. **Hierarchy** — all parent/child references point to real documents
    4. **Content** — correct topic type, no duplicates, attribution present
    5. **Reconciliation** — no silent redefinition of canonical terms

    ## Who runs it?
    - **Pre-commit hook** — runs Gates 1-3 automatically on every git push
    - **Curator agent** — runs all 5 gates on request or via Cove pipeline
    - **Nightly job** — runs all 5 gates against the entire vault at 03:00 UTC

    ## How do I add a new document?
    1. Create the .md file with proper YAML frontmatter (see template below)
    2. Add the _c: compressed code using the CURATOR-CODEBOOK.md lookup
    3. Commit to the vault repo
    4. Pre-commit hook validates Gates 1-3 automatically
    5. Curator agent validates Gates 4-5 and either admits or rejects

    ## How do I add a new code?
    1. Edit CURATOR-CODEBOOK.md with the new code
    2. Add an entry to the changelog at the bottom
    3. Commit with message: "codebook: add {CODE} for {meaning}"
    4. Curator agent reloads on next invocation

    ## What happens if validation fails?
    - The commit is blocked (pre-commit hook)
    - You get a specific error message telling you what failed and how to fix it
    - No partial admissions — all gates must pass

    ## Where are the specs?
    - Full specification: vault/03-frameworks-and-rubriks/CURATOR-GATE-SPEC-v1.md
    - Codebook: vault/03-frameworks-and-rubriks/CURATOR-CODEBOOK.md
    - Pre-commit hook: .git/hooks/pre-commit
    - Nightly reconciliation: configured in Cove orchestrator

PART 5: THE CURATOR AGENT SYSTEM PROMPT INJECTION
-------------------------------------------------

This is what gets loaded into the Curator agent's context at startup:

    You are the Curator agent for Amplified Partners.

    YOUR ROLE: You are the SOLE gateway for content entering the vault.
    Nothing enters without your validation. This is Law 0.

    YOUR CODEBOOK: [full CURATOR-CODEBOOK.md contents injected here]

    YOUR VALIDATION PIPELINE:
    1. Gate 1 (STRUCTURE): Check YAML frontmatter. All required fields present. _c: line present.
    2. Gate 2 (CODEBOOK): Parse _c: against your codebook. Every code must resolve. Cross-check against verbose YAML.
    3. Gate 3 (HIERARCHY): Verify all parent/child/reference links resolve to existing vault documents.
    4. Gate 4 (CONTENT): Check word count bounds. Check for duplicates (cosine similarity < 0.85). Verify topic_type matches content pattern. Verify attribution block.
    5. Gate 5 (RECONCILIATION): Check for term redefinitions against canonical sources. Flag for human review if found.

    YOUR OUTPUT FORMAT:
    For each submitted document, return:
    - PASS: "✓ ADMITTED — {filename} — all 5 gates passed"
    - FAIL: "✗ REJECTED — {filename} — Gate {N} failed: {specific error} — Fix: {specific instruction}"
    - WARN: "⚠ CONDITIONAL — {filename} — Gates 1-4 passed, Gate 5 flagged: {redefinition details} — Requires human review"

    YOUR CONSTRAINTS:
    - You do NOT modify documents. You validate and report.
    - You do NOT approve your own output. A human approves Gate 5 warnings.
    - If your codebook hash does not match the current file, REFUSE to validate and request reload.
    - You maintain a validation log: every admission and rejection is recorded with timestamp and gate results.

PART 6: INTEGRATION WITH EXISTING SYSTEMS
-----------------------------------------

  System                        Integration Point
  ----------------------------- -------------------------------------------------------------------------------------------
  **Operational Protocol**      Law 0 added: "If it hasn't passed the Curator, it can't enter GitHub"
  **Cove Pipeline**             Curator runs as a validation step before any generated code/doc enters the vault
  **Build Quality Framework**   The "Attribute" step in the 6-stage pipeline now routes through the Curator for admission
  **RIC**                       New discoveries from pudding sessions pass through the Curator before vault admission
  **APDS**                      Harvested research passes through the Curator with `status: hypothesis`
  **Nightly Reconciliation**    Replaces ad-hoc audits --- systematic, scheduled, logged
  **Linear**                    Gate failures auto-create Linear issues tagged `curator-alert`
  **FalkorDB/Graphiti**         Only Curator-admitted documents are eligible for Graphiti ingestion
  **Pre-commit hook**           Git-level enforcement --- bypassing requires `--no-verify` which is logged and flagged

PART 7: WHAT THIS PREVENTS
--------------------------

  Risk                                                               How the Curator Prevents It
  ------------------------------------------------------------------ -------------------------------------------------
  Orphan documents (no frontmatter, no labels)                       Gate 1 blocks them
  Invalid codes (typos, made-up dimensions)                          Gate 2 blocks them
  Broken cross-references                                            Gate 3 blocks them
  Duplicate content (same concept written twice)                     Gate 4 blocks them
  Silent term redefinition (scoring threshold defined differently)   Gate 5 flags them
  Stale codebook (Curator using old codes)                           Hash verification refuses validation
  Bypassed Curator (manual edit, force push)                         Nightly reconciliation catches them
  Drift over time (documents becoming non-compliant)                 Nightly reconciliation + 90-day staleness check

SOURCES
-------

-   Deterministic safety gates pattern: [Matt
    Barge](https://www.linkedin.com/posts/matt-barge-7039a532_ai-softwareengineering-automation-activity-7430239582304051200-PD0P)
    --- "Make it impossible to deploy broken code. Remove the decision
    entirely."
-   Deterministic AI orchestration architecture:
    [Praetorian](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)
    --- 9-phase agent audit, MANIFEST.yaml state management, validation
    loops
-   Harness-first engineering:
    [Datadog](https://www.datadoghq.com/blog/ai/harness-first-agents/)
    --- "Instead of reading every line of agent-generated code, invest
    in automated checks"
-   Context engineering for AI agents:
    [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
    --- compaction, context rot, lean context windows
-   Token efficiency in AI agents:
    [FlowHunt](https://www.flowhunt.io/blog/context-engineering-ai-agents-token-optimization/)
    --- "context rot" degradation, attention budget depletion
-   Pre-commit hook patterns:
    [pre-commit.com](https://pre-commit.com/hooks.html),
    [OneUptime](https://oneuptime.com/blog/post/2026-02-26-argocd-pre-commit-hooks-manifests/view)
-   Self-healing knowledge base:
    [Bloomfire](https://bloomfire.com/platform/content-reliability/) ---
    automated duplicate and conflict detection
-   DITA subject scheme maps: [OASIS
    Open](https://docs.oasis-open.org/dita/v1.2/os/spec/common/subjectScheme.html)
    --- controlled values, taxonomy binding
-   Existing Amplified Partners documents: SOUL.md, Operational Protocol
    v1.0, Radical Attribution Schema v1.0, Build Quality Framework v1.0,
    Code Taxonomy Kaizen v1.0

Attribution: Ewan Bramley (originator, directive) × Perplexity
(researcher, formaliser) Fact %: 80 \| Confidence: High \| PUDDING:
C.=.5.∞ LBD: Swanson (1986) ABC Model
