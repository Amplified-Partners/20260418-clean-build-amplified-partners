---
title: "LLM Atomiser Specification"
id: "atomiser_spec"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# LLM Atomiser Specification

## Purpose
Transform labelled documents into the smallest useful knowledge chunks possible. Each atom must be self-contained, genuinely useful, and retrievable via RAG for future projects.

## Core Requirements

### Input
- Source: `Knowledge/labelled/` directory
- File types: `.md`, `.txt` files with YAML frontmatter
- Skip: binary sidecars (`.pdf.md`, `.png.md`), `.symlink.md`, `.error.md`

### Output  
- Destination: `Knowledge/atomised/` (flat folder)
- Format: Markdown with YAML frontmatter
- Naming: `{slug}-{hash}.md` (slug from title, hash for uniqueness)

### Atom Properties
- **Size**: 20-60 words ideal, max 100 words
- **Self-contained**: Readable without source context
- **One idea**: Single fact, insight, principle, decision, or action
- **Properly tagged**: Inherit source tags + add semantic tags

## Atom Types
1. **Fact** - Verifiable statement ("X costs £Y", "A uses B")
2. **Insight** - Non-obvious observation or pattern
3. **Principle** - Reusable rule or guideline
4. **Decision** - Choice made with rationale
5. **Action** - Specific task or step
6. **Definition** - What something means
7. **Reference** - Pointer to resource/tool/person

## Frontmatter Schema
```yaml
---
title: "Short descriptive title (5-10 words)"
type: fact|insight|principle|decision|action|definition|reference
source: "Knowledge/labelled/path/to/source.md"
tags:
- inherited-tag
- semantic-tag
created: "2024-12-14"
---
```

## Extraction Rules

### DO Extract
- Concrete facts with specifics (names, numbers, dates)
- Actionable insights that change behaviour
- Decisions and their reasoning
- Definitions of domain terms
- Contact info, URLs, tool names
- Process steps that stand alone

### DON'T Extract
- Filler, pleasantries, transitions
- Repetition of same idea
- Context-dependent statements
- Incomplete thoughts
- Meta-commentary ("as mentioned earlier")
- Content requiring visual context

## Processing Logic

1. Read source file, parse frontmatter
2. Clean markdown (remove code fences, images, timestamps)
3. Send to LLM with extraction prompt
4. Parse LLM response (JSON array of atoms)
5. For each atom:
   - Validate word count
   - Generate slug from title
   - Create hash from content
   - Write to atomised folder
6. Track source→atom mapping for deduplication

## Deduplication
- Hash each atom body
- Skip if identical hash exists
- Log near-duplicates (>80% similarity) for review

## Error Handling
- Log extraction failures, continue processing
- Create `.error.md` breadcrumb for failed files
- Retry rate-limited API calls with backoff

## Performance
- Batch API calls where possible
- Cache processed file hashes
- Resume from last position on restart
