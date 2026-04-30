Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

# Amplified Partners — Universal File Naming Convention v1

## THE LAW

**Every file in the system follows this convention. No exceptions.**

An AI agent encountering a file reads this spec first. A human creating a file follows this spec. An automation script producing a file conforms to this spec. If a file doesn't conform, it gets renamed before it enters any pipeline.

This is v1. It is built to evolve. New file types can be added. Existing rules can be refined. But the structure is constitutional — it doesn't change on a whim.

---

## 1. THE FORMAT

Every file name follows this pattern:

```
{type}-{slug}-{date}-v{N}.{ext}
```

### The Four Segments

| Segment | Required? | What It Is | Rules |
|---------|-----------|------------|-------|
| **type** | YES | What kind of file this is | From the controlled vocabulary (Section 2). Lowercase. Single token. |
| **slug** | YES | What the file is about | Lowercase kebab-case. 2-6 words. Descriptive. No LLM session titles. |
| **date** | CONDITIONAL | When it was created or last substantively updated | `YYYY-MM-DD` (ISO 8601). Required for dated content. Omitted for evergreen files. See Section 3. |
| **v{N}** | CONDITIONAL | Which version this is | `v1`, `v2`, `v3`... Required for versioned content. Omitted for one-off content. See Section 4. |
| **.{ext}** | YES | File format | Lowercase. `.md`, `.py`, `.sh`, `.json`, `.yaml`, `.pdf`, etc. |

### Separator Rules

| Rule | Standard |
|------|----------|
| **Word separator** | Hyphen (`-`) — always |
| **Segment separator** | Hyphen (`-`) — same as word separator; segments are distinguished by position and controlled vocabulary, not by a different character |
| **Never use** | Spaces, underscores, dots (except before extension), parentheses, ampersands, percent signs, or any special characters |
| **Case** | All lowercase — always. No Title-Case, no ALL-CAPS, no camelCase, no mixed |

### Character Rules

| Rule | Standard |
|------|----------|
| **Allowed characters** | `a-z`, `0-9`, `-` (hyphen), `.` (only before extension) |
| **Maximum filename length** | 80 characters (including extension). Enough to be descriptive, short enough to display cleanly in terminals and file browsers |
| **Minimum filename length** | `{type}-{slug}.{ext}` = at least ~10 characters |

---

## 2. THE TYPE VOCABULARY (Controlled)

Every filename begins with a type token. This is a controlled vocabulary — you pick from this list or propose a new addition through the codebook review process.

### Document Types

| Type Token | What It Is | Typical Directory | Example |
|------------|-----------|-------------------|---------|
| `strategy` | Business strategy, plans, roadmaps | 01-business-strategy | `strategy-four-pillars-master-2026-03-17-v2.md` |
| `spec` | Technical specification, architecture doc | 02-technical-architecture | `spec-falkordb-graphiti-arch-2026-03-11-v1.md` |
| `framework` | Scoring rubric, methodology, system definition | 03-frameworks-and-rubriks | `framework-pudding-2026-canonical-v1.md` |
| `rubric` | Scoring rubric specifically (subset of framework) | 03-frameworks-and-rubriks | `rubric-raei-scoring-v1.md` |
| `product` | Product spec, feature definition | 04-products | `product-bob-voice-first-2026-03-11-v1.md` |
| `agent` | Agent architecture, prompt, role definition | 05-agent-architecture | `agent-council-architecture-v1.md` |
| `brand` | Brand spec, identity, marketing asset | 06-brand-and-marketing | `brand-amplified-spec-v2.md` |
| `governance` | Legal, compliance, governance document | 07-governance-and-legal | `governance-immutable-code-v1.md` |
| `knowledge` | Knowledge management, taxonomy, ontology | 08-knowledge-management | `knowledge-deduplication-guide-2026-01-24.md` |
| `infra` | Infrastructure, hosting, deployment | 09-infrastructure | `infra-beast-docker-compose-2026-03-02-v3.md` |
| `personal` | Personal context, voice mirror, private notes | 10-personal | `personal-voice-mirror-v1.md` |
| `session` | AI conversation session export | 11-claude-misc, 11-gemini-misc, 12-claude-short-sessions | `session-claude-vault-cleanup-2026-03-10.md` |
| `transcript` | Monologue transcript, voice capture | 13-monologue-transcripts, 14-voice-captures | `transcript-ewan-0042-2026-01-15.md` |
| `principle` | Named principle from expert library | 15-principles-library | `principle-dalio-radical-transparency-v1.md` |
| `bible` | Business bible section | 15-principles-library | `bible-01-vision-strategy-v1.md` |
| `legacy` | Pre-Amplified era content | 16-covered-ai-work | `legacy-covered-ai-brand-spec-2025-11.md` |
| `import` | Externally sourced document | 17-imported-business-docs | `import-dave-demo-bible-v1.md` |
| `research` | Research output, deep dive, analysis | 18-research | `research-voice-ai-comparison-2026-02-24.md` |
| `brief` | Short summary, briefing, status update | Any | `brief-weekly-status-2026-03-17.md` |
| `ref` | Reference document (canonical, living) | Any | `ref-infrastructure-master-v4.md` |
| `recipe` | PUDDING recipe (cross-domain mix) | 03-frameworks-and-rubriks | `recipe-kennedy-lund-graceful-deadlines-v1.md` |
| `mix` | PUDDING mix session output | 03-frameworks-and-rubriks | `mix-001-cross-domain-discovery-2026-03-10.md` |
| `audit` | Audit report, system check, review | Any | `audit-vault-naming-patterns-2026-03-17.md` |
| `plan` | Action plan, implementation plan | Any | `plan-marketing-engine-build-2026-03-11.md` |
| `sop` | Standard operating procedure | Any | `sop-vault-ingestion-pipeline-v2.md` |
| `template` | Reusable template | Any | `template-client-config-yaml-v1.yaml` |
| `config` | Configuration file | Any | `config-jesmond-plumbing-v1.yaml` |
| `test` | Test data, test results, validation output | Any | `test-pudding-validation-30-atoms-2026-03-17.md` |
| `index` | Index file for a directory or collection | Any | `index-monologue-transcripts-2026-03.md` |
| `script` | Automation script, utility code | 23-scripts | `script-vault-sync-github.py` |
| `prompt` | System prompt, agent prompt | 05-agent-architecture | `prompt-gatekeeper-capture-v2.md` |
| `handover` | Session-to-session continuity document | 00-handover | `handover-cowork-session-7-2026-03-15.md` |
| `project` | Claude project memory file | 00-claude-projects | `project-business-brain-v1.md` |
| `log` | Daily log, steward report, changelog | Any | `log-mac-steward-daily-2026-01-16.md` |
| `draft` | Work in progress, not yet final | Any (temporary) | `draft-substack-pudding-story-2026-03-10.md` |
| `erratum` | Correction, fix record, known error | Any | `erratum-pudding-label-e3-fix-2026-03-17.md` |

### Adding New Types

New type tokens can be proposed. The process:

1. Check existing types — does one already cover this?
2. If genuinely new, propose the token (single lowercase word, ≤ 12 characters)
3. Add it to this table with a definition and example
4. Update the validation script
5. Document the change in the version history of this file

---

## 3. DATE RULES

### When to Include a Date

| Content Type | Date Required? | Rationale |
|-------------|---------------|-----------|
| Session exports, transcripts, logs | YES | Time-specific content — the date IS the identity |
| Research outputs | YES | Findings are time-bound — they age |
| Strategy docs, plans, briefs | YES | Context changes — when matters |
| Audits, reviews, test results | YES | Point-in-time assessments |
| Principles, frameworks, rubrics | NO (use version) | Evergreen content — evolves by version, not date |
| Scripts, configs, templates | NO (use version) | Functional content — works or doesn't |
| Reference docs | NO (use version) | Living documents — version tracks evolution |
| Agent prompts, SOPs | NO (use version) | Operational content — versioned |

### Date Format

```
YYYY-MM-DD
```

Always ISO 8601. Always hyphenated. Always 10 characters.

| Format | Status |
|--------|--------|
| `2026-03-17` | CORRECT |
| `20260317` | WRONG — not allowed |
| `2026-03` | ALLOWED — when day is unknown or irrelevant (month-precision) |
| `2026` | ALLOWED — when month is unknown (year-precision) |
| `17-03-2026` | WRONG — DD-MM-YYYY is never used |
| `March-2026` | WRONG — no English month names |
| `29th-of-February-26th` | WRONG — obviously |

### Date Placement

The date always comes after the slug and before the version number:

```
{type}-{slug}-{date}-v{N}.{ext}
         ↑        ↑       ↑
      content   when   evolution
```

If a file has both a date AND a version:
```
research-voice-ai-comparison-2026-02-24-v2.md
```
The date is when the content was created. The version is which revision.

If a file has only a date (no version):
```
session-claude-vault-cleanup-2026-03-10.md
```

If a file has only a version (no date):
```
framework-pudding-2026-canonical-v1.md
```

---

## 4. VERSION RULES

### Format

```
v{N}
```

Always lowercase `v`. Always a plain integer. No leading zeros.

| Format | Status |
|--------|--------|
| `v1` | CORRECT |
| `v2` | CORRECT |
| `v30` | CORRECT (even high numbers) |
| `V1` | WRONG — uppercase |
| `_v1` | WRONG — underscore |
| `-1` | WRONG — ambiguous (is it version 1 or collision suffix 1?) |
| `v1.2` | WRONG — no sub-versions in the filename (use YAML frontmatter for minor versions) |

### Version vs Date

- **Version** = the file has been substantively revised. The new version replaces the old one for current use.
- **Date** = when the content was created or captured.

A file can have both (research updated after new findings), one, or neither (extremely rare — a truly static, unversioned, undated utility file).

### The "Latest" Problem

Never name a file `latest`, `current`, `final`, or `new`. These words decay immediately.

```
WRONG:  strategy-master-plan-latest.md
WRONG:  strategy-master-plan-final.md
WRONG:  strategy-master-plan-final-v2.md    ← "final" but there's a v2?
RIGHT:  strategy-master-plan-v3.md
```

### Version History

When a file is versioned, all previous versions remain in the same directory. They are not deleted. The convention is:

```
framework-pudding-2026-canonical-v1.md   ← original
framework-pudding-2026-canonical-v2.md   ← revision
framework-pudding-2026-canonical-v3.md   ← current
```

The highest version number is always the current version. No ambiguity.

---

## 5. THE SLUG (How to Write It)

The slug is the descriptive core of the filename. It tells you what the file is about.

### Rules

| Rule | Standard | Example |
|------|----------|---------|
| **Length** | 2-6 words | `vault-cleanup-guide` (3 words) |
| **Style** | Lowercase kebab-case | `falkordb-graphiti-arch` |
| **Content** | Descriptive of the file's content | NOT the session title, NOT the first question asked |
| **Specificity** | Specific enough to distinguish from similar files | `voice-ai-comparison` not `research` |
| **No LLM titles** | Never use verbatim AI conversation titles | NOT `building-a-comprehensive-business-bible-from-project-materials` |
| **No trivial names** | Never use `oops`, `test`, `untitled`, `temp` as the whole slug | `test-pudding-30-atoms` is fine; `test` alone is not |
| **Author in slug** | Include when the file is about a specific person's work | `principle-dalio-radical-transparency` |
| **Sequence numbers** | Use zero-padded numbers for series | `mix-001`, `mix-002`, `transcript-ewan-0042` |

### Slug Examples (Good)

```
vault-cleanup-guide
falkordb-graphiti-arch
voice-ai-comparison
pudding-2026-canonical
dalio-radical-transparency
bob-voice-first
beast-docker-compose
kennedy-lund-graceful-deadlines
cross-domain-discovery
weekly-status
```

### Slug Examples (Bad)

```
building-a-coaching-business-master-guide     ← too long, LLM title
unable-to-determine-screenshot-not-provided   ← LLM error message as filename
casual-greeting                               ← trivial
it-is-a-logo-for-a-company-called-base-layer  ← prompt as filename
world-class-prompt-to-ensure-effective         ← truncated prompt as filename
jaunty-kindling-shore                         ← random codename, meaningless
unnamed-048b499c                              ← system-generated, meaningless
```

---

## 6. THE README HEADER (What AI Reads First)

Every markdown file in the vault carries a YAML frontmatter header. This is the first thing any AI agent reads before processing the file. It is the file's identity card.

### Minimum Required Header

```yaml
---
filename: "{type}-{slug}-{date}-v{N}.md"
type: "{type token from Section 2}"
title: "Human-readable title"
created: YYYY-MM-DD
version: N
status: draft | active | canonical | deprecated | archived
---
```

### Full Header (for production files)

```yaml
---
# IDENTITY
filename: "framework-pudding-2026-canonical-v1.md"
type: framework
title: "The Pudding Technique — PUDDING 2026 Labelling System"
created: 2026-01-22
updated: 2026-03-17
version: 1

# CLASSIFICATION
status: canonical
vault_directory: 03-frameworks-and-rubriks
pudding_label: "M.=.0.∞"
pudding_reading: "Meta, Stable, Scale-free, Timeless"
atom_id: "AMP-0803-001-v1"

# TAXONOMY (5 layers)
layer_1_structural: "M.=.0.∞"
layer_2_functional: "classification-system"
layer_3_domain: "knowledge-management"
layer_4_temporal: "permanent"
layer_5_maturity: "canonical"

# RELATIONSHIPS
parent: null
children:
  - "mix-001-cross-domain-discovery-2026-03-10.md"
  - "mix-002-biological-decision-logic-2026-03-10.md"
replaces: null
replaced_by: null
related:
  - "rubric-raei-scoring-v1.md"
  - "spec-falkordb-graphiti-arch-2026-03-11-v1.md"

# ATTRIBUTION
attribution:
  human:
    - name: "Ewan Bramley"
      role: originator
  ai:
    - name: "Claude"
      provider: "Anthropic"
      role: formaliser
  fact_percentage: 85
  confidence_band: high
  lbd_attribution: "Swanson (1986) ABC Model"

# AI INSTRUCTIONS
ai_instructions: |
  This is a canonical framework document. Do not modify without explicit
  human approval. When referencing this file, cite it by atom_id.
  Cross-reference with rubric-raei-scoring-v1.md for scoring details.
---
```

### Header Rules

| Rule | Standard |
|------|----------|
| **filename field** | Must match the actual filename exactly. If they disagree, the actual filename wins and the header must be corrected. |
| **status values** | `draft` (work in progress), `active` (in use, may be updated), `canonical` (authoritative reference), `deprecated` (superseded, kept for history), `archived` (no longer relevant) |
| **ai_instructions** | Free text. Tells any AI agent what to do (and what NOT to do) with this file. This is the "README before you touch it" field. |
| **pudding_label** | Only present if the file has been through the labeling pipeline. Not mandatory for drafts. |
| **atom_id** | Only present if the file has been assigned an atom ID. Not mandatory for session exports or transcripts. |

### What AI Agents Do With the Header

1. **Read the header FIRST** — before processing any content
2. **Check `status`** — if `deprecated` or `archived`, flag to the user before proceeding
3. **Check `ai_instructions`** — follow them. If they say "do not modify", do not modify.
4. **Check `version`** — if referencing this file, always use the latest version
5. **Check `related`** — if context would benefit from cross-referencing, load related files
6. **Check `replaces` / `replaced_by`** — if this file has been superseded, use the replacement instead
7. **Preserve the header** — when editing a file, never delete or corrupt the YAML frontmatter

---

## 7. VAULT DIRECTORY ROUTING

The type token determines which vault directory a file belongs in. This is the routing table.

| Type Token | Primary Directory | Notes |
|------------|------------------|-------|
| `strategy` | `01-business-strategy` | |
| `spec` | `02-technical-architecture` | |
| `framework` | `03-frameworks-and-rubriks` | |
| `rubric` | `03-frameworks-and-rubriks` | |
| `recipe` | `03-frameworks-and-rubriks` | |
| `mix` | `03-frameworks-and-rubriks` | |
| `product` | `04-products` | |
| `agent` | `05-agent-architecture` | |
| `prompt` | `05-agent-architecture` | |
| `brand` | `06-brand-and-marketing` | |
| `governance` | `07-governance-and-legal` | |
| `knowledge` | `08-knowledge-management` | |
| `infra` | `09-infrastructure` | |
| `personal` | `10-personal` | |
| `session` | `11-claude-misc` / `11-gemini-misc` / `12-claude-short-sessions` | Route by AI provider and length |
| `transcript` | `13-monologue-transcripts` / `14-voice-captures` | Route by source type |
| `principle` | `15-principles-library` | |
| `bible` | `15-principles-library` | |
| `legacy` | `16-covered-ai-work` | |
| `import` | `17-imported-business-docs` | |
| `research` | `18-research` | |
| `script` | `23-scripts` | |
| `config` | Directory depends on what's being configured | |
| `template` | Directory depends on domain | |
| `test` | Directory depends on what's being tested | |
| `audit` | Directory depends on what's being audited | |
| `brief` | Directory depends on domain | |
| `ref` | Directory depends on domain | |
| `plan` | Directory depends on domain | |
| `sop` | Directory depends on domain | |
| `log` | Directory depends on domain | |
| `draft` | Directory depends on domain (move to final type when promoted) | |
| `handover` | `00-handover` | |
| `project` | `00-claude-projects` | |
| `index` | Same directory as the files it indexes | |
| `erratum` | Same directory as the file it corrects | |

### The Single-Source-of-Truth Rule

**A file lives in ONE directory. Not five. Not eight. One.**

If a file is relevant to multiple domains (e.g., a strategy doc that also covers technical architecture), it lives in the directory matching its PRIMARY type token. Other directories can reference it via the `related` field in their own files' headers.

The current vault has files duplicated across 5-8 directories. This stops. One file. One location. Cross-references in headers.

---

## 8. SESSION ROUTING (Special Case)

Session exports from AI conversations are the most common file type in the vault and the most inconsistently named. This section defines the routing rules.

### Naming

```
session-{provider}-{slug}-{date}.md
```

Where `{provider}` is one of: `claude`, `gemini`, `gpt`, `perplexity`, `grok`, `other`.

### Examples

```
session-claude-vault-cleanup-2026-03-10.md
session-gemini-youtube-analysis-2025-11-27.md
session-perplexity-pudding-validation-2026-03-17.md
```

### Routing by Provider and Length

| Condition | Route To |
|-----------|----------|
| Claude session, substantial (>500 words) | `11-claude-misc` |
| Claude session, short (<500 words) | `12-claude-short-sessions` |
| Gemini session | `11-gemini-misc` |
| Other providers | Create `11-{provider}-misc` if needed |

### The Slug Must Be Meaningful

The slug is NOT the LLM-generated conversation title. It is a human (or AI-assigned) summary of what the session actually covered.

```
WRONG:  session-claude-casual-greeting-2026-02-25.md
WRONG:  session-claude-oops-2026-01-21.md
WRONG:  session-claude-unable-to-determine-screenshot-not-provided-2026-01-14.md
RIGHT:  session-claude-vault-sync-debugging-2026-02-25.md
RIGHT:  session-claude-pudding-taxonomy-design-2026-01-22.md
```

If a session is genuinely trivial (a greeting with no substance), it does not enter the vault.

---

## 9. TRANSCRIPT ROUTING (Special Case)

### Monologue Transcripts

```
transcript-{speaker}-{NNNN}-{date}.md
```

Where:
- `{speaker}` = who is speaking (e.g., `ewan`, `dave`, `unknown` only if genuinely unidentified)
- `{NNNN}` = zero-padded sequence number (4 digits, expandable to 5 if needed)
- `{date}` = date of recording if known

### Examples

```
transcript-ewan-0042-2026-01-15.md
transcript-ewan-0043-2026-01-15.md
transcript-unknown-0950.md              ← date unknown, no date segment
```

### Voice Captures

```
transcript-voice-{speaker}-{NNNN}-{date}.md
```

The `voice` qualifier distinguishes processed voice captures from text monologue transcripts.

---

## 10. SCRIPT AND CODE FILES

Scripts follow the same convention but with code-appropriate extensions.

```
script-{slug}.{ext}
```

Scripts typically don't need dates (they're functional, not temporal) but may need versions:

```
script-vault-sync-github.py
script-vault-push-github-v2.py
script-classify-content.py
script-bake-pudding.py
script-manual-vault-sync.sh
config-vault-sync-rules.json
```

### Database Migrations

Migrations are a special case — they use numeric ordering because execution order matters:

```
script-migrate-{NNN}-{slug}.py
```

```
script-migrate-006-add-interview-tables.py
script-migrate-007-add-call-transcripts.py
```

---

## 11. VALIDATION (How to Check)

### Filename Validation Regex

```python
import re

FILENAME_PATTERN = re.compile(
    r'^'
    r'[a-z]+'              # type token (lowercase alpha)
    r'(-[a-z0-9]+)+'       # slug segments (lowercase alphanumeric, hyphen-separated)
    r'(-\d{4}(-\d{2})?(-\d{2})?)?'  # optional date (YYYY, YYYY-MM, or YYYY-MM-DD)
    r'(-v\d+)?'            # optional version
    r'\.[a-z0-9]+'         # file extension
    r'$'
)

VALID_TYPES = {
    'strategy', 'spec', 'framework', 'rubric', 'product', 'agent', 'brand',
    'governance', 'knowledge', 'infra', 'personal', 'session', 'transcript',
    'principle', 'bible', 'legacy', 'import', 'research', 'brief', 'ref',
    'recipe', 'mix', 'audit', 'plan', 'sop', 'template', 'config', 'test',
    'index', 'script', 'prompt', 'handover', 'project', 'log', 'draft',
    'erratum',
}

MAX_LENGTH = 80

def validate_filename(filename: str) -> dict:
    """Validate a filename against the Amplified Partners convention."""
    errors = []

    if len(filename) > MAX_LENGTH:
        errors.append(f"Too long: {len(filename)} chars (max {MAX_LENGTH})")

    if ' ' in filename:
        errors.append("Contains spaces")

    if filename != filename.lower():
        errors.append("Not all lowercase")

    if not FILENAME_PATTERN.match(filename):
        errors.append("Does not match expected pattern: {type}-{slug}[-{date}][-v{N}].{ext}")

    # Extract type token
    type_token = filename.split('-')[0]
    if type_token not in VALID_TYPES:
        errors.append(f"Unknown type token: '{type_token}'. Must be one of: {sorted(VALID_TYPES)}")

    return {
        'filename': filename,
        'valid': len(errors) == 0,
        'errors': errors,
    }
```

### Batch Validation

```bash
# Validate all files in a vault directory
find /opt/amplified/vault/ -type f -name "*.md" | while read f; do
    basename=$(basename "$f")
    python validate_filename.py "$basename"
done
```

---

## 12. MIGRATION (From Current State)

The vault currently has ~4,787 files using 5+ different naming conventions. Migration is a project, not a one-off rename.

### Migration Priority

| Priority | What | Count (est.) | Approach |
|----------|------|-------------|----------|
| 1 | Canonical framework docs (`03-frameworks-and-rubriks`) | ~80 | Manual rename — these are high-value, need careful slugs |
| 2 | Active strategy docs (`01-business-strategy`) | ~80 | Semi-automated — AI proposes slug, human approves |
| 3 | Infrastructure and specs (`02-`, `04-`, `05-`) | ~200 | Semi-automated |
| 4 | Principles library (`15-`) | ~57 | Already close — mostly needs `principle-` prefix standardisation |
| 5 | Research outputs (`18-research`) | ~380 | Automated — strip hex IDs and codenames, assign meaningful slugs |
| 6 | Session exports (`11-`, `12-`) | ~30 | Semi-automated — AI reads content, proposes slug |
| 7 | Monologue transcripts (`13-`) | ~700+ | Automated — fix `unknown` to `ewan`, fix NNNN-NNNN duplicates |
| 8 | Voice captures (`14-`) | ~954 | Automated — add `transcript-voice-` prefix |
| 9 | Inbox raw (`19-`) | ~300+ | Triage first — many should be deleted, not renamed |
| 10 | Everything else | ~150 | Case-by-case |

### Migration Rules

1. **Never break links** — if other files reference an old filename, update all references before renaming
2. **Git tracks history** — the rename is a `git mv`, not a delete + create. History is preserved.
3. **Batch carefully** — rename in batches of 20-50. Verify after each batch.
4. **Header update** — when renaming, update the `filename` field in the YAML header to match
5. **No rush** — this is a gradual migration. Priority 1-4 first. The rest can wait.

### What Happens to Non-Conforming Files During Migration

```
OLD: Building-a-coaching-business-master-guide-2026-01-16.md
NEW: strategy-coaching-business-guide-2026-01-16.md

OLD: FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md
NEW: spec-falkordb-graphiti-arch-2026-03-11-v1.md

OLD: world class promt to ensure effective orchestratio (3).md
NEW: prompt-orchestration-effectiveness-2026-01-25-v3.md

OLD: 2026-02-24-jaunty-kindling-shore-8251ac.md
NEW: research-[read-content-to-determine-slug]-2026-02-24.md

OLD: monologue-unknown-0042.md
NEW: transcript-ewan-0042.md (add date if discoverable from content)

OLD: SOUL.md
NEW: ref-soul-mission-values-v1.md (or framework-soul-v1.md — depends on content)

OLD: AGENTS-v4.md
NEW: ref-agent-roster-v4.md
```

---

## 13. EDGE CASES

### Files with No Clear Type

If a file genuinely doesn't fit any type token, use `ref` (reference) as a catch-all. But ask first: should this file exist, or should it be split into files that DO have clear types?

### Files Spanning Multiple Domains

Use the PRIMARY domain's type token. Cross-reference in the header. One file, one directory, one type.

### Very Short Filenames

```
WRONG:  ref-soul.md         ← too vague
RIGHT:  ref-soul-mission-values-v1.md
```

The slug should be at least 2 words.

### Files That Are Truly Temporary

Use `draft-` type. When the content is finalised, rename to its proper type. Drafts should not accumulate indefinitely.

### Binary Files (Images, Audio, Video, PDFs)

Same convention applies. The type and extension distinguish them:

```
brand-amplified-logo-dark-v2.png
brand-amplified-logo-light-v2.svg
research-market-sizing-report-2026-03.pdf
transcript-voice-ewan-0042-2026-01-15.mp3
```

---

## 14. VERSION HISTORY

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1 | 2026-03-17 | Initial specification | Ewan Bramley (originator) × Perplexity AI (researcher, formaliser) |

---

## Attribution

```
Human: Ewan Bramley (originator — directive for universal naming convention, architectural decisions)
AI: Perplexity AI (researcher — vault audit, naming convention research, specification writing)
Research Sources:
  - Digital Preservation Coalition — File Naming and Formats (DP Note 4)
  - U.S. National Archives — Best Practices for File Naming (2017)
  - Smithsonian Libraries — Best Practices for File Naming and Organizing
  - Harvard Biomedical Data Management — File Naming Conventions
  - Princeton University Records Management — File Naming Conventions and Version Control
  - ISO 8601:2004 — Date and Time Format Standard
Fact %: 90 | Confidence: High | PUDDING: C.=.5.p
LBD: Swanson (1986) ABC Model
```
