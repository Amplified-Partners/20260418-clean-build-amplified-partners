---
title: "README For AI"
id: "readme-for-ai"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "reference"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Markdown Metadata Index for AI Review

This index is a guide, not a source of truth. Dates may reflect export/copy time, path dates, or content/template dates.

## Files
- md_metadata_index.tsv: one row per rescued Markdown file.

## Key columns
- source_path/source_rel: provenance.
- mac_created/mac_modified: filesystem dates; may be copy/export dates.
- guide_date: best rough sorting date.
- date_confidence: medium_date_string or low_mtime_fallback.
- dates_found: date strings found near path/top of file; may include examples.
- inferred_source/source_basis: guessed origin tool, e.g. cursor, codex, claude, github, notion, perplexity.
- frontmatter_keys/title_or_name/description/model/assistant/status: YAML/frontmatter clues.

Recommended use: sort by guide_date desc, filter by inferred_source, then inspect title/description/source_path. Do not treat dates as certain.

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd
