---
title: "Pipeline Error Research: File Processing, Document Ingestion & Knowledge Graph Construction"
id: "error-research-pipelines-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Pipeline Error Research: File Processing, Document Ingestion & Knowledge Graph Construction

**Research Date:** 2026-03-17  
**Context:** Amplified Partners stack — ~4,787 files across 25 directories → FalkorDB knowledge graph  
**Scope:** 7 areas × 5–8 documented problems each, with proven solutions, preventability classification, and severity ratings

---

## Severity Legend

| Level | Description |
|---|---|
| **DATA LOSS** | Files, content, or graph nodes are permanently destroyed or unrecoverable |
| **SILENT CORRUPTION** | Data is wrong but no error is raised; system continues as if healthy |
| **PIPELINE HALT** | Processing stops entirely; requires manual intervention to resume |
| **DEGRADED QUALITY** | Pipeline completes but outputs are incomplete, inconsistent, or low-confidence |

---

## Area 1: File Naming and Taxonomy Enforcement

**Problem domain:** Enforcing naming conventions across ~4,787 files with regex, unicode-aware matching, and safe rename operations.

---

### 1.1 Windows 260-Character Path Limit (MAX_PATH)

**What goes wrong:** Python and .NET file I/O functions on Windows fail silently or raise `OSError`/`PathTooLongException` when fully-qualified paths exceed 260 characters (defined as `MAX_PATH`). The drive letter, all directory names, the filename, and null terminator all count. A deeply nested vault — e.g., `C:\Users\ewan\vault\clients\amplified\2024\q4\reports\strategy\` — can exhaust the budget before the filename is added. Directory creation is additionally limited to `MAX_PATH - 12` (248 chars) to allow for 8.3 short filenames.

**Evidence:** [Microsoft Learn — Maximum Path Length Limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation): "the maximum length for a path is MAX_PATH, which is defined as 260 characters." The [Twilio Python SDK GitHub issue #535](https://github.com/twilio/twilio-python/issues/535) documents pip install failures on Windows caused by long paths in deeply nested packages.

**Proven solution:**
- Enable long path support: `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1` (Windows 10 1607+) or Group Policy. This extends effective limit to ~32,767 characters using `\\?\` extended-length prefix.
- In Python, prefix absolute paths with `\\?\` and use `pathlib.Path` with `resolve()` before passing to file I/O.
- For pipelines: enforce a maximum directory depth and filename length budget during taxonomy validation, not only at read/write time.
- Use the `subst` command to map deep roots to a shorter drive letter in CI/CD environments.

**Preventability:** Code-time (path budget validator) + runtime monitoring (log warnings when remaining budget < 50 chars).

**Severity:** PIPELINE HALT (raises exception), occasionally SILENT CORRUPTION when legacy tools truncate without error.

---

### 1.2 Unicode Normalization Mismatches (NFC vs NFD)

**What goes wrong:** macOS HFS+/APFS normalises filenames to NFD (decomposed), storing `café` as `cafe\u0301` (5 code points). Linux ext4 and most Windows NTFS implementations store NFC (composed) forms. A Python regex `re.match(r'^café', filename)` written against NFC input fails silently on NFD filenames. Worse, moving a vault directory on macOS (`mv` across volumes) re-normalises filenames, causing previously matching patterns to stop matching.

**Evidence:** [AbleSet Forum — NFC vs NFD unicode matching](https://forum.ableset.app/t/nfc-vs-nfd-unicode-matching/2128): "macOS automatically normalizes filenames to NFD when moving the entire project to a different location or drive." [Stack Overflow — When to use Unicode Normalization Forms NFC and NFD](https://stackoverflow.com/questions/15985888/when-to-use-unicode-normalization-forms-nfc-and-nfd): "NFC is the best form for general text … programs should always compare canonical-equivalent Unicode strings as equal."

**Proven solution:**
- Normalise all filenames to NFC before any regex or string comparison: `import unicodedata; name = unicodedata.normalize('NFC', filename)`.
- Apply normalisation in both the validator and the rename function so the stored name and the pattern input are always in the same form.
- Run `unicodedata.is_normalized('NFC', name)` as a pre-flight check in the taxonomy enforcer.
- For cross-platform vaults, normalise on ingest and store a normalised index.

**Preventability:** Code-time (add normalisation to all path comparison utilities).

**Severity:** SILENT CORRUPTION (patterns fail to match; files appear to violate conventions when they are actually compliant, or vice versa).

---

### 1.3 Regex Edge Cases: Greedy Matching, Anchoring, and Dot-All Flags

**What goes wrong:** Taxonomy regexes written for simple filenames fail on edge inputs: (a) unanchored patterns match substrings, accepting `2024-01-meeting-notes-DRAFT-v2` when only the date-prefix form is intended; (b) `.` in patterns matches path separators on Linux, causing `../../etc/passwd`-style traversal in validation logic; (c) `re.DOTALL` accidentally set causes multi-line filenames (rare but possible with `\n` in filenames on Linux) to pass; (d) `\w` in Python's `re` matches Unicode word characters including Cyrillic and CJK by default, accepting filenames that are not ASCII-safe.

**Proven solution:**
- Always anchor patterns: `^` and `$` (or `\Z`).
- Use `re.fullmatch()` instead of `re.match()` to prevent partial matching.
- Explicitly use `[a-zA-Z0-9_-]` character classes rather than `\w` when ASCII-only names are required.
- Test regex against a curated adversarial set: empty string, Unicode filenames, path separators, dotfiles, names starting/ending with spaces.

**Preventability:** Code-time (unit tests for the regex validator).

**Severity:** SILENT CORRUPTION (invalid files pass validation) or DEGRADED QUALITY (valid files are incorrectly rejected).

---

### 1.4 Filename Collision During Batch Rename

**What goes wrong:** When normalising or restructuring filenames at scale (e.g., adding date prefixes from YAML frontmatter to 4,787 files), two files can produce identical target names: `project-notes.md` and `Project-Notes.md` both normalise to `project-notes.md` on a case-insensitive filesystem. The second rename silently overwrites the first. Python's `os.rename()` on POSIX is atomic but not safe against this; it will overwrite without warning.

**Evidence:** [USENIX FAST '23 — "Unsafe at Any Copy"](https://www.usenix.org/system/files/fast23-basu.pdf): "improper handling of case-[in]sensitivity and encoding can result in silent data loss and corruption … name collisions introduced by differences in name resolution under case-sensitive and case-insensitive file systems."

**Proven solution:**
- Dry-run: compute all target names before executing any renames. Detect collisions in a dict keyed by `target_name.lower()`.
- Use a collision-resolution strategy: append `_2`, `_3` or incorporate a hash fragment rather than failing.
- On case-insensitive filesystems, always normalise to lowercase before collision detection.
- Log a collision report to a separate file before any destructive operation.

**Preventability:** Code-time (dry-run collision checker).

**Severity:** DATA LOSS (original file silently overwritten).

---

### 1.5 Non-Atomic Rename Leaving Partial State

**What goes wrong:** A naive "copy-then-delete" rename sequence (used when source and destination are on different volumes) is non-atomic. If the process crashes between copy and delete, both the source and destination exist; if between delete-old and write-new, neither exists. Even `os.rename()` is atomic on POSIX only when source and destination are on the same filesystem.

**Evidence:** [Stack Overflow — Is an atomic file rename with overwrite possible on Windows?](https://stackoverflow.com/questions/167414/is-an-atomic-file-rename-with-overwrite-possible-on-windows): "On POSIX systems rename(2) provides for an atomic rename operation, including overwriting of the destination file." Windows requires `NtSetInformationFile` with `FILE_RENAME_POSIX_SEMANTICS` (Windows 10 1607+) for equivalent atomicity. [Python bug tracker #8828](https://bugs.python.org/issue8828) documents that `os.rename` on Windows is non-atomic for cross-drive moves.

**Proven solution:**
- Always use the write-to-temp-then-rename pattern: `open(tmp_path, 'w') → fsync() → os.replace(tmp_path, final_path)`.
- `os.replace()` (Python 3.3+) is preferred over `os.rename()` — it atomically replaces the destination if it exists on POSIX; on Windows it raises `OSError` instead of silently overwriting.
- For cross-volume operations, track a transaction log (pending renames) that can be replayed or rolled back.

**Preventability:** Code-time.

**Severity:** DATA LOSS (file disappears between delete and replace).

---

### 1.6 Timestamp Loss During Rename

**What goes wrong:** `os.rename()` preserves timestamps on POSIX (mtime, atime are unchanged on same-filesystem renames). However, if the pipeline copies the file to a new name and deletes the old one (e.g., cross-volume, or using `shutil.copy2` + `os.remove`), `mtime` is reset to the copy timestamp unless explicitly preserved. For a vault where `mtime` is the canonical "last modified" signal used by indexers and Git, this silently destroys temporal metadata.

**Proven solution:**
- Prefer `os.rename()` / `os.replace()` for same-filesystem renames (timestamps preserved automatically).
- For cross-filesystem: use `shutil.copy2()` (preserves mtime/atime) followed by `os.remove()`.
- Explicitly read and restore timestamps: `stat = os.stat(src); os.utime(dst, (stat.st_atime, stat.st_mtime))`.
- Include mtime in the pre/post rename audit log to detect silent losses.

**Preventability:** Code-time.

**Severity:** SILENT CORRUPTION (metadata wrong; git log, sort-by-date, and incremental processing all use stale timestamps).

---

### 1.7 Case Sensitivity Collision Between macOS and Linux

**What goes wrong:** macOS APFS is case-insensitive (by default). A vault that contains both `Meeting-Notes.md` and `meeting-notes.md` compiles correctly on Linux (case-sensitive ext4) but silently aliases both to the same inode on macOS, meaning only one version is visible. When the vault is pushed to a Linux CI/CD server or Docker container (case-sensitive), both files appear and cause unexpected behaviour in any pipeline that assumes unique paths. This is a [documented Git CVE (CVE-2021-21300)](https://www.usenix.org/system/files/fast23-basu.pdf).

**Proven solution:**
- Enforce lowercase-only filenames as a hard taxonomy rule — eliminates the collision class entirely.
- Add a CI lint step that checks for case-collision pairs: `[f.lower() for f in all_files]` — detect duplicates.
- Configure Git: `git config core.ignoreCase false` to surface collisions at commit time.

**Preventability:** Code-time (taxonomy rule) + CI gate.

**Severity:** DATA LOSS (one file silently masked) or SILENT CORRUPTION (wrong file version read).

---

## Area 2: Document Ingestion Pipelines (LLM-Based)

**Problem domain:** Ingesting thousands of Markdown/PDF/DOCX files via LLM extraction into structured schema for FalkorDB.

---

### 2.1 Rate Limiting and Exponential Backoff Failures

**What goes wrong:** LLM APIs enforce rate limits at two levels: requests-per-minute (RPM) and tokens-per-minute (TPM). Naïve pipelines fire all requests concurrently, exhaust the token budget within seconds, receive HTTP 429 errors, and either crash or retry at a fixed interval — which just repeats the burst. The failure mode is especially bad when processing resumes after a crash: the pipeline replays already-completed files, doubling token spend and resetting rate limit windows. [typedef.ai](https://www.typedef.ai/resources/handle-token-limits-rate-limits-large-scale-llm-inference): "Rate limit violations and token limit errors require explicit handling … teams build LLM pipelines that work perfectly in development, then hit walls at scale."

**Proven solution:**
- Implement token-aware rate limiting: track cumulative `input_tokens + output_tokens` against the TPM limit using a sliding window. Use `time.sleep()` based on actual usage, not fixed delays.
- Use exponential backoff with jitter on 429: `wait = base * 2^attempt + random.uniform(0, 1)`.
- Maintain a persistent completion ledger (SQLite or JSON) indexed by file hash — skip files already successfully processed.
- For OpenAI: use the `x-ratelimit-remaining-tokens` response header to dynamically throttle.

**Preventability:** Code-time (rate limiter implementation) + runtime monitoring.

**Severity:** PIPELINE HALT (unhandled 429 crash) or DEGRADED QUALITY (retry storms miss files).

---

### 2.2 Token Count Estimation Errors and Silent Truncation

**What goes wrong:** Pipelines frequently estimate token counts using character-count heuristics (e.g., `len(text) / 4`) rather than the actual tokeniser. For code-heavy or multilingual content, this underestimates by 40–50%; for prose, it overestimates. The result: requests sent with more tokens than the model's context window, causing silent truncation (the model receives a clipped prompt and extracts only partial content, returning no error). [Galileo.AI tiktoken guide](https://galileo.ai/blog/tiktoken-guide-production-ai): "a batch job spiral from 1.5 million to 5.8 million tokens overnight—no code changes, just an unexpected tokenizer shift … even 10% token count errors translate to massive budget overruns."

**Proven solution:**
- Use `tiktoken` (OpenAI) or the model's own tokenizer library to count tokens before dispatch, not character heuristics.
- Initialise the encoder once and reuse: `encoding = tiktoken.encoding_for_model("gpt-4")` — do not reinitialise per request (performance penalty).
- Set explicit `max_tokens` output budgets rather than relying on defaults.
- When a document exceeds the context window, split into overlapping chunks (e.g., 512-token overlap) and merge extraction results, not simply truncate.

**Preventability:** Code-time.

**Severity:** SILENT CORRUPTION (partial extraction returns no error; missing content is silently dropped).

---

### 2.3 Hallucinated Entities and Relationship Fabrication

**What goes wrong:** LLMs asked to extract structured data (entities, relationships) from documents fabricate plausible but non-existent information. This is particularly severe for: (a) entity attributes not present in the source text; (b) relationships between entities that are mentioned near each other but not actually linked in the text; (c) dates, IDs, and numeric values that sound reasonable but are wrong. [arXiv — How Much Do LLMs Hallucinate in Document Q&A](https://arxiv.org/html/2603.08274v1): "even the best-performing models fabricate answers at a non-trivial rate — 1.19% at best at 32K, with fabrication rising steeply with context length, nearly tripling at 128K."

**Proven solution:**
- Require span-level grounding: instruct the LLM to return the verbatim source text fragment that supports each extracted entity/relationship. Discard extractions with no grounding span.
- Use Pydantic schemas with `description` fields to constrain output format and reduce hallucination surface area.
- Run multi-pass extraction at low temperature and merge only consensus results.
- Post-extraction: verify that entity names appear verbatim (or near-verbatim) in the source chunk — flag any entity absent from the source as a candidate hallucination.
- For high-confidence requirements: apply a re-ranking/self-consistency check pass.

**Preventability:** Code-time (grounding constraints) + runtime monitoring (hallucination rate metrics).

**Severity:** SILENT CORRUPTION (wrong entities/relationships in graph, no error raised).

---

### 2.4 Context Loss Across Chunk Boundaries

**What goes wrong:** Chunking splits documents at arbitrary token boundaries, severing semantic units: a pronoun in chunk N+1 has no referent (the noun is in chunk N); a table header appears in one chunk and its data rows in another; a relationship spans two sentences that end up in separate chunks. The LLM extracts each chunk independently, losing cross-chunk context. [Reddit r/LLMDevs — RAG still hallucinates even with good chunking](https://www.reddit.com/r/LLMDevs/comments/1plynfw/rag_still_hallucinates_even_with_good_chunking/): "The necessary information was located in a neighboring chunk that failed to make it into the top-k results … tables, FAQs, and special cases were divided across boundaries."

**Proven solution:**
- Use semantic/structural chunking rather than fixed-token splits: break at section headings, paragraph boundaries, or logical document units (LlamaParse, LangChain recursive splitter with `separators=["\n\n", "\n", " "]`).
- Add 10–15% overlap between consecutive chunks to preserve sentence-level context at boundaries.
- Pass document-level metadata (title, section path, file path) in every chunk prompt so the LLM has context about what it's extracting.
- For multi-page PDFs: extract page-level text blocks, merge short pages, and include the previous section header in each chunk prompt.

**Preventability:** Code-time.

**Severity:** DEGRADED QUALITY (correct facts missing) or SILENT CORRUPTION (relationships extracted across wrong context).

---

### 2.5 UTF-8 BOM and Encoding Detection Failures

**What goes wrong:** Files authored on Windows commonly contain a UTF-8 BOM (`\xef\xbb\xbf`) or are encoded in Windows-1252/Latin-1. Opening these files with `open(path, encoding='utf-8')` either strips the BOM silently (Python 3) or raises `UnicodeDecodeError` on the first non-ASCII character. More insidiously, the BOM is passed to the LLM as the first character of the prompt, causing regex anchors on the first character to fail and LLM extraction to misparse the beginning of the document. [GitHub — mkdocs issue #1186](https://github.com/mkdocs/mkdocs/issues/1186): "If the file is encoded in UTF-8 BOM (Windows 😞) then the rendering issue occurs."

**Proven solution:**
- Use `open(path, encoding='utf-8-sig')` instead of `utf-8` — this transparently strips the BOM if present, and is identical to `utf-8` for BOM-free files. [Python docs discussion](https://discuss.python.org/t/utf-8-bom-not-being-consumed-when-opening-file/74870).
- For unknown-encoding files: use `chardet` or `charset-normalizer` to detect encoding before opening.
- For Latin-1 files: `open(path, encoding='latin-1', errors='replace')` then normalise to UTF-8 during ingest.
- Pre-flight check: scan all files for encoding before the ingestion run; quarantine non-UTF-8 files to a separate queue.

**Preventability:** Code-time (use `utf-8-sig`) + pre-flight scan.

**Severity:** PIPELINE HALT (`UnicodeDecodeError`) or SILENT CORRUPTION (BOM character passed to LLM corrupts first token).

---

### 2.6 Binary File Detection Failures

**What goes wrong:** Pipelines that use filename extensions to skip non-text files (e.g., `if path.endswith('.md')`) fail when binary files are renamed with text extensions, or when `.md` files contain embedded binary (e.g., images encoded as raw bytes in obscure editors). Passing binary content to an LLM: (a) causes `UnicodeDecodeError` if decoded as text; (b) silently fills the context window with garbage if decoded as `latin-1`; (c) causes the LLM to return nonsense extractions without error.

**Proven solution:**
- Use magic-byte detection (`python-magic` / `libmagic`) in addition to extension checking: `mime = magic.from_file(path, mime=True)`. Only pass `text/*` MIME types to the ingestion pipeline.
- For Markdown files: additionally check for null bytes (`\x00`) in the first 8KB — presence of null bytes indicates binary content.
- Send binary-detected files to a quarantine directory with a log entry rather than silently skipping.

**Preventability:** Code-time (magic-byte pre-filter).

**Severity:** PIPELINE HALT (crash) or SILENT CORRUPTION (garbage extraction, no error).

---

### 2.7 Partial Extraction with No Failure Signal

**What goes wrong:** LLM extraction calls that succeed (HTTP 200, well-formed JSON response) may return structurally valid but semantically empty results: `{"entities": [], "relationships": []}`. This happens when: (a) the chunk was too short to contain useful content; (b) the model decided no entities were present (false negative); (c) the output token budget was hit mid-generation, producing a truncated JSON blob that a forgiving parser fills with defaults. The pipeline marks the file as "processed" and never retries.

**Proven solution:**
- Define minimum-content thresholds per document type: flag any extraction returning zero entities from a document with >500 tokens as a potential failure.
- Validate `finish_reason == "stop"` (not `"length"`) before accepting extraction results — `"length"` means the output was truncated.
- Implement a separate validation pass on a random 5% sample of "empty" extractions to calibrate false-negative rates.
- Store raw LLM response alongside structured extraction for audit.

**Preventability:** Code-time (validation logic) + runtime monitoring.

**Severity:** SILENT CORRUPTION (data missing from graph with no error raised).

---

## Area 3: Knowledge Graph Construction

**Problem domain:** Building a FalkorDB knowledge graph from LLM-extracted entities and relationships across 25 directories.

---

### 3.1 Entity Resolution Ambiguity (Coreference)

**What goes wrong:** The same real-world entity appears under multiple surface forms across documents: "Bob", "Bob Smith", "Mr Smith", "Robert Smith", "Bob S." are all extracted as distinct nodes. In a knowledge graph, this creates node proliferation — the graph has 5 nodes for one person, none of which accumulate a complete relationship set. Queries for "all relationships of Bob Smith" miss connections recorded under alias nodes. This is described as the "hidden make-or-break step for accurate enterprise AI" by [Stack AI](https://www.stack-ai.com/insights/enterprise-knowledge-graphs-the-secret-weapon-for-better-ai-accuracy).

**Proven solution:**
- Apply canonical name resolution during extraction: instruct the LLM to always use the full name when a partial reference can be resolved within the document context.
- Build a coreference resolution pass using string similarity (Jaro-Winkler or trigram similarity) + embedding cosine similarity to cluster entity mentions.
- Merge clusters into canonical nodes with aliases stored as a `aliases` property array.
- For organisation/product names: maintain a controlled vocabulary reference list and fuzzy-match against it during extraction.
- Use graph queries to detect suspiciously isolated nodes (single relationship, short name) as merge candidates.

**Preventability:** Code-time (extraction prompt engineering) + runtime data quality pass.

**Severity:** DEGRADED QUALITY (graph incomplete; queries return partial results without error).

---

### 3.2 Relationship Extraction Errors (False Positives and Type Misclassification)

**What goes wrong:** LLMs extract relationships that are textually proximate but semantically incorrect: "Bob presented to Acme Corp" → `[:WORKS_FOR]` instead of `[:PRESENTED_TO]`. Negated relationships are extracted as positive: "Bob no longer works at Acme" → `[:WORKS_FOR]` (the negation is dropped). Temporal scoping is lost: "Bob was CEO" → present-tense edge with no `start_date`/`end_date` properties. These errors compound: a graph with wrong edge types produces wrong traversal results on every query.

**Proven solution:**
- Provide a fixed, well-defined relationship type vocabulary in the extraction prompt — do not allow free-text relationship labels.
- Include few-shot examples of negated statements and instruct the model to omit relationships with negation markers ("no longer", "not", "former").
- Always extract temporal scope as part of the relationship: `{type: "WORKS_FOR", start_date: "2020", end_date: "2023", confidence: 0.9}`.
- Post-extraction: validate that all relationship types are in the allowed vocabulary; reject and re-extract chunks with out-of-vocabulary types.

**Preventability:** Code-time (schema enforcement).

**Severity:** SILENT CORRUPTION (wrong graph topology; queries return incorrect results).

---

### 3.3 Temporal Edge Conflicts

**What goes wrong:** As documents from different time periods are ingested, contradictory states accumulate in the graph: a node has both `[:EMPLOYED_BY {company: "Acme"}]` and `[:EMPLOYED_BY {company: "Beta Corp"}]` active simultaneously, when in reality they are sequential. The resolution depends on document timestamps, but if document timestamps are not preserved (see Area 1.6) or not passed to the extraction pipeline, the graph cannot distinguish current state from historical state. [TigerGraph — Why Temporal Conflicts in Entity Resolution Cause Chaos](https://www.tigergraph.com/blog/why-temporal-conflicts-in-entity-resolution-cause-chaos/): "temporal conflicts arise when outdated attributes and relationships remain active in a resolved entity."

**Proven solution:**
- Model time on edges, not nodes: every relationship edge carries `valid_from` and `valid_to` timestamps.
- Use `valid_to: null` for currently active relationships. When a contradictory relationship is added, close the existing one: `SET r.valid_to = new_relationship.valid_from`.
- Pass document `mtime` or explicit publication date to the extraction prompt: "This document was created on 2023-11-15. Use this as the reference date for all temporal claims."
- Implement a temporal conflict detector: Cypher/FalkorDB query that finds nodes with two simultaneously-active relationships of the same type to the same entity class.

**Preventability:** Code-time (temporal graph schema) + runtime validation query.

**Severity:** SILENT CORRUPTION (graph state inconsistent; queries return wrong current-state results).

---

### 3.4 Graph Schema Evolution Without Data Loss

**What goes wrong:** As the ontology evolves (renaming a relationship type from `RELATED_TO` to `ASSOCIATED_WITH`, splitting a `Person` node into `Person` and `Organisation`, adding a required property to an existing node type), existing graph data becomes inconsistent: old nodes lack the new required property; old relationship types are not traversed by new queries; renamed types leave orphaned edges. [DEV Community — Schema Evolution Without Breaking Consumers](https://dev.to/alexmercedcoder/schema-evolution-without-breaking-consumers-50a9): "schema changes often happen accidentally … without guardrails, these changes propagate downstream silently."

**Proven solution:**
- Adopt the additive-only pattern for graph schema changes: never remove or rename node labels or relationship types; only add new ones. Deprecate old types by adding a `deprecated: true` property and running a migration in parallel.
- Write explicit migration scripts (Cypher `MATCH` → `SET`/`CREATE`) for every schema change, version-controlled alongside application code.
- Maintain a schema version property on a singleton `GraphMetadata` node; reject ingestion runs whose expected schema version does not match the current graph version.
- Before any schema migration, create a FalkorDB snapshot/backup.

**Preventability:** Code-time (migration scripts) + runtime schema versioning.

**Severity:** PIPELINE HALT (schema mismatch errors) or SILENT CORRUPTION (old nodes not returned by new queries).

---

### 3.5 Orphaned Nodes

**What goes wrong:** Nodes are created during entity extraction but their expected relationships are never successfully written (due to extraction errors, batch interruption, or schema validation rejection). The nodes exist in the graph but have zero relationships — they are "orphaned". Queries that traverse from other nodes never reach them, and they inflate node counts without contributing to graph value. [Graphiti GitHub issue #1083](https://github.com/getzep/graphiti/issues/1083): "entities that lack MENTIONS relationships are not cleaned up, resulting in orphaned Entity nodes."

**Proven solution:**
- Run a post-ingestion orphan detection query: `MATCH (n) WHERE NOT (n)--() RETURN n` (FalkorDB/Cypher syntax). Log and review orphaned nodes before deciding to delete or re-process.
- Implement a two-phase write: create nodes and relationships in a single transaction where possible. If the graph database does not support multi-statement transactions, use a staging table.
- Track node creation and relationship creation counts per document. Flag any document where `relationship_count == 0` but `entity_count > 0`.
- Scheduled cleanup job: nodes orphaned for >7 days with no incoming or outgoing edges are candidates for deletion (with human review).

**Preventability:** Runtime monitoring (orphan detection queries).

**Severity:** DEGRADED QUALITY (graph incomplete, inflated node counts, reduced traversal quality).

---

### 3.6 Duplicate Node Creation (Merge vs Create Race Condition)

**What goes wrong:** Concurrent ingestion workers running in parallel may each extract the same entity from different documents and independently issue `CREATE` (not `MERGE`) statements, producing duplicate nodes. In FalkorDB/Cypher, `MERGE` checks for existence before creating, but under concurrent load without proper locking, two workers can both find "no existing node" and both create, resulting in duplicates. [PuppyGraph — How to Build a Knowledge Graph](https://www.puppygraph.com/blog/how-to-build-knowledge-graph): "don't over-normalize your graph the way you might with a relational database."

**Proven solution:**
- Always use `MERGE` (not `CREATE`) for entity nodes. `MERGE` with a uniqueness constraint is atomic in most graph databases.
- Add a uniqueness constraint on the canonical identifier property: `CREATE CONSTRAINT ON (p:Person) ASSERT p.canonical_name IS UNIQUE`.
- For high-concurrency pipelines: use a deduplication stage before graph writes — accumulate all entities from a batch, deduplicate in memory, then write.
- Post-ingestion deduplication query: `MATCH (n:Person) WITH n.canonical_name AS name, COLLECT(n) AS nodes WHERE SIZE(nodes) > 1 RETURN name, nodes`.

**Preventability:** Code-time (use MERGE + constraints).

**Severity:** SILENT CORRUPTION (duplicate nodes fragment the graph; queries return incomplete results).

---

## Area 4: YAML Frontmatter Processing

**Problem domain:** Parsing YAML frontmatter from ~4,787 Markdown files for metadata extraction, taxonomy validation, and indexing.

---

### 4.1 Special Characters in Unquoted Values

**What goes wrong:** YAML uses `:`, `#`, `{`, `}`, `[`, `]`, `|`, `>`, `*`, `&`, `!` as syntax characters. An unquoted value containing any of these causes a parse error or silent misparse. The most common culprit is `:` in titles: `title: Strategy: Phase 1` is parsed as a mapping, not as the string "Strategy: Phase 1". [GitHub — zk issue #24](https://github.com/mickael-menu/zk/issues/24): `title: A title with: special characters` → `yaml: mapping values are not allowed in this context`.

**Proven solution:**
- Enforce quoting policy in the taxonomy: all string values must be wrapped in double quotes. Write a linter that flags unquoted string values.
- In the parser, use `ruamel.yaml` instead of PyYAML for better error recovery and YAML 1.2 compliance.
- Wrap the parse call in a try/except and emit the file path and line number in the error: `except yaml.YAMLError as e: log.error(f"{path}:{e.problem_mark.line}: {e.problem}"`).
- Pre-validate frontmatter blocks with `yamllint` in CI before ingestion.

**Preventability:** Code-time (linting) + CI gate.

**Severity:** PIPELINE HALT (parse error) or SILENT CORRUPTION (value truncated at special character).

---

### 4.2 PyYAML Automatic Type Coercion (Datetime Ambiguity)

**What goes wrong:** PyYAML (YAML 1.1) auto-coerces values that look like dates into Python `datetime.date` or `datetime.datetime` objects without any explicit type tag. `date: 2024-01-15` becomes a `datetime.date` object, not the string `"2024-01-15"`. This breaks downstream code that expects strings and attempts string operations on the value. Worse, values like `version: 1.0` become floats; `enabled: yes`/`no`/`on`/`off` become booleans (a YAML 1.1 quirk not present in YAML 1.2). [Reddit r/learnpython](https://www.reddit.com/r/learnpython/comments/1qlw812/how_is_type_determined/): "In YAML, there exists a timestamp type … the library interprets and transforms into a proper Python datetime object." [GitHub — equinor/webviz-config issue #396](https://github.com/equinor/webviz-config/issues/396) documents this as a breaking bug.

**Proven solution:**
- Use `yaml.safe_load()` and explicitly cast values after parsing: `str(frontmatter.get('date', ''))`.
- Switch to `ruamel.yaml` with `yaml.version = (1, 2)` to disable YAML 1.1 implicit type coercion.
- Alternatively, wrap date strings in quotes in the source files: `date: "2024-01-15"` to force string interpretation even under YAML 1.1.
- Add type assertions in the frontmatter schema validator: `assert isinstance(fm['date'], str), f"date must be string, got {type(fm['date'])}"`).

**Preventability:** Code-time (use YAML 1.2 parser or explicit casting).

**Severity:** SILENT CORRUPTION (downstream type errors; date comparisons produce wrong results).

---

### 4.3 Indentation Errors and Multiline String Mishandling

**What goes wrong:** YAML is indentation-sensitive. Two common failures: (a) block scalar content that begins at the wrong indentation level causes parse errors or incorrect content capture; (b) automated tools that rewrite YAML (e.g., Prettier, yq) change indentation style inconsistently — `tags:` followed by an inline list `[a, b]` is converted to a block list but with wrong indent, breaking the parser. [Reddit r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1pln99r/til_skill_descriptions_must_be_singleline_in_yaml/): "Prettier had automatically converted it into multiline strings … the parser doesn't handle YAML multiline strings (the indented block style)."

**Proven solution:**
- Use `|` (literal block) for multi-line values where newlines are meaningful; use `>` (folded block) where newlines are just soft wraps. Avoid implicit multi-line strings (continuation lines without a block indicator).
- Standardise indentation to 2 spaces across the vault using a `.editorconfig` rule and enforce via `yamllint`.
- When programmatically rewriting YAML frontmatter, use `ruamel.yaml` with `yaml.best_map_flow_style` to preserve existing style, rather than re-serializing to a default style.

**Preventability:** Code-time (yamllint CI gate).

**Severity:** PIPELINE HALT (parse error) or SILENT CORRUPTION (multi-line content incorrectly captured).

---

### 4.4 Missing Required Fields (Silent vs. Loud Failures)

**What goes wrong:** Files missing required frontmatter fields (e.g., no `title`, no `date`, no `status`) are silently accepted by a permissive parser that returns `None` for missing keys. Downstream code then dereferences `None` and either crashes at an unrelated location or silently propagates `None` into the graph (e.g., a node with `title: None`). The error is hard to trace back to the source file.

**Proven solution:**
- Define a Pydantic model for frontmatter schema with `required` fields; validate every parsed frontmatter block against it.
- On validation failure: emit a structured error with file path, field name, and expected type. Route to a quarantine queue rather than silently skipping.
- For required fields with sensible defaults (e.g., `status: draft`), apply defaults explicitly and log that a default was applied.
- Run a bulk validation pass as a pipeline pre-flight check: report all files with missing required fields before any ingestion begins.

**Preventability:** Code-time (Pydantic validation).

**Severity:** PIPELINE HALT (None dereference crash) or SILENT CORRUPTION (graph nodes missing key properties).

---

### 4.5 Frontmatter Delimiter Detection Failures

**What goes wrong:** YAML frontmatter is delimited by `---` on its own line. Failures occur when: (a) the file begins with a BOM (`\xef\xbb\xbf`) before `---`, causing the delimiter not to match; (b) the closing `---` delimiter is missing (file was truncated); (c) the file contains `---` inside the body (e.g., a Markdown horizontal rule), causing the parser to misidentify the frontmatter end. Parsers vary in how they handle these — some silently consume the entire document as frontmatter.

**Proven solution:**
- Always strip BOM before delimiter detection (see Area 2.5).
- Limit frontmatter scanning to the first 8KB of the file — `---` appearing after 8KB is a body rule, not a delimiter.
- Require both opening and closing `---` delimiters; files with only an opening delimiter are quarantined as malformed.
- Use a well-maintained library (e.g., `python-frontmatter`) rather than ad-hoc string splitting.

**Preventability:** Code-time.

**Severity:** PIPELINE HALT or SILENT CORRUPTION (entire document body parsed as YAML).

---

## Area 5: Git-Based Vault Management

**Problem domain:** Managing a ~4,787-file Markdown vault in Git with concurrent editing across devices.

---

### 5.1 Merge Conflicts in Concurrent Edits to the Same File

**What goes wrong:** When the same Markdown file is edited on two devices (laptop + desktop, or two team members) without an intermediate sync, both produce divergent commits. `git merge` or `git pull` inserts conflict markers (`<<<<<<`, `=======`, `>>>>>>>`) directly into the file body. If the pipeline reads files without first checking for conflict markers, it ingests the conflict markers as document content — corrupting LLM extraction by including raw Git annotations. [Obsidian Forum](https://forum.obsidian.md/t/merge-conflicts-when-i-pull-my-vault/91334): "my files having version of changes from both devices and weird lines like `>>>>>>> origin/master`."

**Proven solution:**
- Pre-ingestion conflict marker scan: `grep -rl '^<<<<<<' vault/` — quarantine any file containing conflict markers before ingestion.
- Use `git pull --rebase` instead of merge-based pull to reduce conflict frequency for sequential (not truly concurrent) edits.
- Set auto-merge strategies for non-critical metadata files: `echo ".obsidian/workspace.json merge=ours" >> .gitattributes`.
- For vault-wide sync: consider a CRDT-based sync (Obsidian LiveSync) for concurrent editing rather than Git merge for frequently co-edited files.

**Preventability:** Code-time (conflict marker scanner as pipeline gate).

**Severity:** SILENT CORRUPTION (conflict markers ingested as document content).

---

### 5.2 Binary File History Bloat (Git Object Database Growth)

**What goes wrong:** Binary files (PDFs, images, compiled attachments) committed directly to Git grow the object database proportionally to their size × version count. A 2MB PDF updated 50 times = ~100MB in `.git/objects`. This causes: `git clone` to be prohibitively slow, CI checkout time to balloon, and `git gc` to run for hours. [GitHub Well-Architected — Large Git Repositories](https://wellarchitected.github.com/library/architecture/recommendations/scaling-git-repositories/large-git-repositories/): "The extensive commit history, including large binary files and outdated dependencies, makes the repository bloated and difficult to manage."

**Proven solution:**
- Set up Git LFS for binary extensions before any binary files are committed: `git lfs track "*.pdf" "*.docx" "*.png"`.
- For repos already bloated: use `git-filter-repo` or the [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) to rewrite history and remove large blobs. Run `git gc --prune=now --aggressive` after BFG.
- Set `git config http.postBuffer 524288000` for large LFS uploads over slow connections.
- Add a pre-commit hook that rejects binary files over a threshold (e.g., 500KB) if LFS is not configured.

**Preventability:** Code-time (LFS setup before first commit).

**Severity:** PIPELINE HALT (CI checkout timeout) or DEGRADED QUALITY (slow clone discourages sync).

---

### 5.3 Obsidian/Editor Metadata Files Causing Spurious Conflicts

**What goes wrong:** Obsidian writes `.obsidian/workspace.json`, `.obsidian/workspace-mobile.json`, and plugin state files on every session open. These binary-adjacent JSON files change on every device. When committed without exclusion, they generate merge conflicts on nearly every `git pull`, even when no actual notes were edited. [GitHub — obsidian-livesync issue #671](https://github.com/vrtmrz/obsidian-livesync/issues/671): "I very rarely get file conflicts however I do get regular conflicts for `.obsidian/workspace-mobile.json`."

**Proven solution:**
- Add to `.gitignore`: `.obsidian/workspace.json`, `.obsidian/workspace-mobile.json`, `.obsidian/plugins/*/data.json` (for plugins that write transient state).
- Track only truly shared configuration: `.obsidian/app.json`, `.obsidian/appearance.json`, plugin manifests.
- For files that must be tracked: add to `.gitattributes` with `merge=ours` to always prefer the local version on conflict.

**Preventability:** Code-time (`.gitignore` and `.gitattributes` setup).

**Severity:** DEGRADED QUALITY (sync friction; developers avoid committing to skip the conflict cycle).

---

### 5.4 Large File Handling: Git LFS Quota and Pointer File Corruption

**What goes wrong:** Git LFS stores file content in a separate object store (GitHub/GitLab LFS server) and commits pointer files (text stubs referencing the content by hash). If the LFS server quota is exceeded, pushes fail with "This repository is over its data quota." More dangerously: if a collaborator pulls without LFS installed, they receive the pointer file as the document content — the pipeline then ingests a 134-byte pointer stub instead of the actual document. [GitHub — git-lfs issue #1101](https://github.com/git-lfs/git-lfs/issues/1101): "This repository is over its data quota. Purchase more data packs to restore access."

**Proven solution:**
- Monitor LFS usage via API and alert before hitting quota thresholds.
- Add LFS pointer file detection to the ingestion pipeline: any file matching `^version https://git-lfs.github.com/spec/v1` is a pointer, not content — skip and alert.
- Run `git lfs prune` regularly to remove unreferenced LFS objects locally.
- For vaults that don't need LFS binary diffing: consider storing large attachments in object storage (S3/R2) and referencing by URL in Markdown, keeping Git free of binaries entirely.

**Preventability:** Code-time (LFS pointer detector) + runtime monitoring (quota alerts).

**Severity:** DATA LOSS (failed push loses file) or SILENT CORRUPTION (pointer file ingested as document).

---

### 5.5 Branch Sync Conflicts and Stale Branch Divergence

**What goes wrong:** Long-lived feature branches in a vault diverge significantly from `main` when multiple contributors add files. Merging after weeks of divergence produces conflicts across dozens of files simultaneously, making automated resolution impossible. For a vault used as a pipeline input, ingesting from a stale or partially-merged branch produces an inconsistent snapshot: some files are at old versions, others at new.

**Proven solution:**
- Enforce a short-lived branch policy for content vaults: merge or rebase at least every 48 hours.
- Use a dedicated `ingest` branch that is always fast-forwarded from `main` — the pipeline reads only from this branch.
- Before each pipeline run: `git fetch origin && git reset --hard origin/main` on the ingest branch to ensure a clean, current state.
- Tag the commit hash used for each pipeline run in the graph metadata — enables reproducibility and rollback.

**Preventability:** Code-time (branch policy) + runtime (pipeline reads pinned commit).

**Severity:** DEGRADED QUALITY (pipeline processes stale content) or SILENT CORRUPTION (inconsistent document versions in graph).

---

## Area 6: Batch File Processing

**Problem domain:** Processing ~4,787 files in batches — memory management, checkpointing, and error isolation.

---

### 6.1 Memory Exhaustion on Large Batches (OOM)

**What goes wrong:** Loading all files into memory simultaneously, or accumulating processed results in a growing list without flushing, exhausts available RAM. On systems without memory limits, the OS begins swapping, causing throughput to collapse. Under container memory limits (common in CI/CD), the process is killed by the OOM killer with no cleanup, leaving the checkpoint in a potentially corrupt state. For a 4,787-file vault where each file may involve LLM API responses of several KB, the total in-memory footprint can exceed several GB.

**Evidence:** [Stack Overflow — Loading and processing large file throws OOM](https://stackoverflow.com/questions/79336536/loading-and-processing-large-file-120mb-in-memory-throws-oom-when-ram-is-still): "the app used to be throwing OOM when processing a 90Mb file … even when running locally, I have the same OOM issues and still have about 40% free RAM" (due to heap fragmentation). [Microsoft Learn — Out of Memory Exception](https://learn.microsoft.com/en-us/answers/questions/1725893/how-to-fix-out-of-memory-exception-while-processin): "break down the data into smaller chunks or batches."

**Proven solution:**
- Process files in streaming fashion: use a generator (`yield`) to process one file at a time rather than loading all results into a list.
- Set an explicit batch size (100–500 files per batch) and flush results to disk/database after each batch.
- Use `del result; gc.collect()` after processing each file to release memory promptly.
- Monitor memory usage: `import psutil; psutil.Process().memory_info().rss` — alert when above 80% of available RAM and pause ingestion.
- For containerised pipelines: set both memory requests and limits in Kubernetes/Docker; configure the OOM limiter to kill the batch worker gracefully.

**Preventability:** Code-time (streaming architecture) + runtime monitoring.

**Severity:** PIPELINE HALT (OOM kill) + potential checkpoint corruption.

---

### 6.2 Checkpoint/Resume Failures

**What goes wrong:** Long-running batch pipelines (processing 4,787 files over several hours) must be resumable after interruption. Common checkpoint failures: (a) checkpoint state is written to a file that is also being read by the batch worker — race condition corrupts the checkpoint; (b) checkpoint records "file X started" but not "file X completed", so on resume the file is processed twice (duplicate graph writes); (c) checkpoint uses mutable file paths as keys — if files are renamed between runs, the checkpoint is stale and the entire batch re-runs; (d) checkpoint file is not atomically written — a crash during checkpoint write leaves a partial/corrupt checkpoint.

**Proven solution:**
- Use file content hash (SHA-256 of first 4KB + filesize) as the checkpoint key, not the file path — survives renames.
- Write checkpoint state atomically: write to a `.tmp` file, `fsync()`, then `os.replace()` to the checkpoint file (see Area 1.5).
- Record two states per file: `STARTED` and `COMPLETED`. On resume, re-process all `STARTED` (incomplete) files. Use `MERGE` (not `INSERT`) in the graph to make re-processing idempotent.
- Use SQLite for the checkpoint store instead of JSON — SQLite writes are transactional by default. [OneUptime — How to Build Batch Retry Strategies](https://oneuptime.com/blog/post/2026-01-30-batch-processing-retry-strategies/view).

**Preventability:** Code-time.

**Severity:** DATA LOSS (completed work lost and not re-processed) or SILENT CORRUPTION (duplicate graph writes from double-processing).

---

### 6.3 Error Propagation vs. Isolation (One Bad File Killing the Batch)

**What goes wrong:** A single malformed file — a PDF that crashes the parser, an encoding that raises `UnicodeDecodeError`, a file the LLM returns an error for — can kill the entire batch if exceptions propagate uncaught. Conversely, silently swallowing all exceptions (`except: pass`) hides real errors and leads to large portions of the vault being silently skipped.

**Evidence:** [OneUptime — Batch Retry Strategies](https://oneuptime.com/blog/post/2026-01-30-batch-processing-retry-strategies/view) implements a `RetryOrSkipProcessor` with dead letter queue: "Non-retryable errors are sent to a dead letter queue for later analysis."

**Proven solution:**
- Wrap each file's processing in a `try/except` that catches and logs the error, then routes the file to a **dead letter queue** (DLQ) — a separate directory or database table of files that failed with their error details.
- Classify errors as retryable (429 rate limit, transient network) vs. non-retryable (parse error, encoding error). Only retry retryable errors.
- Define an abort threshold: if >10% of files in a batch fail, halt the batch and alert rather than continuing (prevents silently skipping most of the vault).
- After every batch run, report: files processed, files succeeded, files in DLQ, DLQ error breakdown by type.

**Preventability:** Code-time.

**Severity:** PIPELINE HALT (unhandled exception) or SILENT CORRUPTION (swallowed exceptions hide mass failures).

---

### 6.4 Partial Completion Tracking (Incomplete Write Detection)

**What goes wrong:** A file is read, processed, and the graph write begins — but the write is interrupted (network timeout to FalkorDB, container killed). The checkpoint records the file as `COMPLETED` but the graph write is partially committed: some nodes exist, some do not; some edges exist, pointing to non-existent target nodes. On resume, the checkpoint skips the file, and the partial graph state persists permanently.

**Proven solution:**
- Use graph transactions: wrap all Cypher writes for a single document in a transaction. If the transaction fails, roll back entirely — no partial state.
- Separate the checkpoint marker from the graph write: mark `COMPLETED` only after the graph transaction commits successfully.
- Implement a reconciliation query: for each file, count expected entities (stored in checkpoint) vs. actual graph nodes tagged with `source_file = path`. Alert on any discrepancy.
- For FalkorDB specifically: confirm whether multi-statement transactions are supported and structure writes accordingly.

**Preventability:** Code-time (transactional writes).

**Severity:** SILENT CORRUPTION (partial graph state; nodes exist without relationships).

---

### 6.5 Concurrency Race Conditions in Parallel Workers

**What goes wrong:** Running multiple parallel ingestion workers (e.g., `ThreadPoolExecutor` or `multiprocessing.Pool`) without proper coordination causes: (a) two workers processing the same file (checkpoint read before write, TOCTOU race); (b) both workers creating the same graph node (duplicate nodes — see Area 3.6); (c) shared mutable state (a list of processed files, a counter) corrupted by unsynchronised access.

**Proven solution:**
- Use a queue-based work distribution model: a single coordinator pushes file paths onto a queue; workers pull from the queue. Queue operations are atomic — no two workers receive the same item.
- Use `multiprocessing.Queue` instead of `threading.Queue` for CPU-bound workers to avoid GIL contention.
- For graph writes: use `MERGE` with uniqueness constraints as the deduplication mechanism rather than pre-write existence checks.
- Limit parallelism to match LLM API rate limits: `max_workers = rpm_limit / avg_requests_per_file`.

**Preventability:** Code-time.

**Severity:** SILENT CORRUPTION (duplicate nodes) or DEGRADED QUALITY (uneven work distribution, files skipped).

---

## Area 7: Cross-Platform File Handling

**Problem domain:** A vault developed on macOS, deployed on Linux CI/CD, with potential Windows contributors.

---

### 7.1 Windows Reserved Filenames (CON, PRN, NUL, COM1–COM9, LPT1–LPT9)

**What goes wrong:** Windows reserves 22 device names as special file-like handles (legacy DOS devices). Attempting to create, open, or delete a file named `NUL`, `CON`, `PRN`, `AUX`, `COM1`–`COM9`, or `LPT1`–`LPT9` (case-insensitive, with or without any extension — `NUL.txt` is also reserved) results in `System.IO.IOException` or unexpected device I/O. A pipeline that creates temp files using auto-generated names could land on a reserved name. Crucially, `Path.GetInvalidFileNameChars()` does NOT include reserved names — they are not caught by the standard invalid character check. [Meziantou's blog — Reserved filenames on Windows](https://www.meziantou.net/reserved-filenames-on-windows-con-prn-aux-nul.htm): "CON, PRN, AUX, NUL, COM0 through COM9, LPT0 through LPT9 … Path.GetInvalidFileNameChars() does not include these reserved names." [Claude Code GitHub issue #16642](https://github.com/anthropics/claude-code/issues/16642): "Claude Code continuously creates 'nul' files in Windows."

**Proven solution:**
- Add an explicit reserved name check to all filename validators: `RESERVED = {'CON','PRN','AUX','NUL','COM0','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','LPT0','LPT1','LPT2','LPT3','LPT4','LPT5','LPT6','LPT7','LPT8','LPT9'}; assert name.upper().split('.')[0] not in RESERVED`.
- For temp file creation, use `tempfile.mkstemp()` which generates names that cannot be reserved.
- Add this check to the taxonomy regex validator as a post-match assertion.

**Preventability:** Code-time (explicit validator).

**Severity:** PIPELINE HALT (Windows I/O exception) or SILENT CORRUPTION (writes go to device instead of file on Windows).

---

### 7.2 Case Sensitivity and Case Collision on Case-Insensitive Filesystems

**What goes wrong:** Linux filesystems (ext4, XFS) are case-sensitive; macOS APFS and Windows NTFS are case-insensitive by default. A vault developed on Linux may contain both `README.md` and `readme.md`. When cloned on macOS, only one is visible — Git even has a CVE for this. During pipeline processing on macOS/Windows, `open('README.md')` and `open('readme.md')` open the same inode, so deduplication logic fails. [Stack Overflow — Case-sensitive path collisions](https://stackoverflow.com/questions/63468346/case-sensitive-path-collisions-on-case-insensitive-file-system-when-i-do-git-clone): "User and user are not allowed to co-exist at the same time inside the components directory on a case-insensitive filesystem." [USENIX FAST '23](https://www.usenix.org/system/files/fast23-basu.pdf): "silent data loss and corruption … symbolic link traversal" from case sensitivity mismatches.

**Proven solution:**
- Enforce lowercase filenames as a hard taxonomy rule — eliminates the entire collision class.
- Add `git config core.ignoreCase false` to surface collisions at commit time.
- In the pipeline, build the file index using `path.lower()` as the key and assert no duplicates before processing.

**Preventability:** Code-time (taxonomy rule) + CI gate.

**Severity:** DATA LOSS (one file silently shadows another) or SILENT CORRUPTION (wrong file version processed).

---

### 7.3 Path Separator Hardcoding

**What goes wrong:** Code that hardcodes `/` as a path separator fails on Windows (`\\`). Code that hardcodes `\\` fails on macOS/Linux. String-based path construction (`base + '/' + filename`) is brittle and breaks in edge cases (trailing slash on `base`, absolute `filename`, UNC paths). This is particularly common in pipeline logging, error messages, and configuration files where paths are constructed manually.

**Evidence:** [Stack Overflow — cross-platform splitting of path in Python](https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python): "Windows has the concept of multiple drives … `c:foo` and `c:\foo` are often not the same."

**Proven solution:**
- Use `pathlib.Path` exclusively for all path construction. The `/` operator on `Path` objects handles platform-specific separators automatically: `base_path / subdir / filename`.
- Never store paths as raw strings in configuration or checkpoints — store as POSIX paths (`path.as_posix()`) and reconstruct with `Path(stored_posix)`.
- Replace all `os.path.join()` and string concatenation with `pathlib` in the codebase.

**Preventability:** Code-time.

**Severity:** PIPELINE HALT (FileNotFoundError) on cross-platform deployments.

---

### 7.4 Symlink Handling Differences

**What goes wrong:** Linux and macOS support symbolic links natively. Windows requires administrator privileges to create symlinks by default (a policy restriction, not an OS limitation). A vault that uses symlinks for cross-directory references (e.g., a shared templates directory linked into multiple project directories) behaves differently: on Linux/macOS, `os.listdir()` follows symlinks transparently; `os.walk()` with `followlinks=False` (default) skips them. On Windows without developer mode enabled, symlink creation raises `OSError: [WinError 1314]`. A pipeline that processes symlinked directories on Linux silently misses them on Windows.

**Proven solution:**
- Avoid vault-level symlinks; prefer relative path references in Markdown links instead.
- If symlinks are necessary: explicitly check `path.is_symlink()` and resolve with `path.resolve()` before processing.
- In `os.walk()`, use `followlinks=True` consistently, but detect and skip circular symlinks: `seen_inodes = set(); skip if os.stat(path).st_ino in seen_inodes`.
- Document the symlink dependency in CI requirements; enable Windows developer mode in CI if symlinks are required.

**Preventability:** Code-time.

**Severity:** PIPELINE HALT (Windows symlink permission error) or DEGRADED QUALITY (symlinked directories silently skipped).

---

### 7.5 Extended Attributes and Hidden Metadata Files

**What goes wrong:** macOS writes extended attributes (resource forks, Finder metadata) as `.DS_Store` files and `._*` AppleDouble files. These files appear in `os.listdir()`, `glob.glob()`, and `pathlib.Path.iterdir()`, causing pipelines to attempt processing of hidden system files. `.DS_Store` is binary and will fail text extraction. `._*` AppleDouble files appear as malformed twins of real files, causing duplicate-processing logic to misfire.

**Proven solution:**
- Add a filename filter to skip hidden files: `if name.startswith('.') or name.startswith('._'): continue`.
- Add to `.gitignore`: `.DS_Store`, `._*`, `Thumbs.db`, `desktop.ini`.
- In `os.walk()`, add `dirnames` filtering: remove `.git`, `.obsidian`, `.DS_Store` directories from the traversal in-place.
- For the ingestion pipeline, define an explicit allowlist of processed extensions (`{'.md', '.txt', '.pdf'}`) rather than relying on a denylist.

**Preventability:** Code-time.

**Severity:** PIPELINE HALT (binary `.DS_Store` causes extraction crash) or DEGRADED QUALITY (system files inflate counts and consume API calls).

---

### 7.6 Line Ending Differences (CRLF vs. LF)

**What goes wrong:** Windows tools write files with CRLF (`\r\n`) line endings; macOS/Linux use LF (`\n`). Git can be configured to auto-convert (`core.autocrlf = true` on Windows), but if configured inconsistently, files in the vault have mixed line endings. For YAML frontmatter parsing, `\r` before `\n` causes the delimiter `---\r` to not match the regex `^---$`, causing the frontmatter to be silently skipped or the entire file treated as non-frontmatter content. For LLM ingestion, CRLF doubles newline counts in token estimates.

**Proven solution:**
- Normalise line endings at ingest: `text = content.replace('\r\n', '\n').replace('\r', '\n')` before any parsing.
- Set `.gitattributes`: `*.md text eol=lf` to enforce LF in the repository for Markdown files.
- Add `core.autocrlf = input` to repository `.git/config` to strip CRLF on commit without converting LF files.

**Preventability:** Code-time (.gitattributes) + pipeline preprocessing.

**Severity:** SILENT CORRUPTION (YAML parse failure, wrong token counts, incorrect line-number references in error logs).

---

## Summary Matrix

| # | Area | Problem | Severity | Preventable |
|---|---|---|---|---|
| 1.1 | File Naming | Windows 260-char path limit | PIPELINE HALT | Code-time |
| 1.2 | File Naming | NFC/NFD unicode mismatch | SILENT CORRUPTION | Code-time |
| 1.3 | File Naming | Regex edge cases (anchoring, `\w`) | SILENT CORRUPTION | Code-time |
| 1.4 | File Naming | Filename collision on rename | DATA LOSS | Code-time |
| 1.5 | File Naming | Non-atomic rename | DATA LOSS | Code-time |
| 1.6 | File Naming | Timestamp loss during rename | SILENT CORRUPTION | Code-time |
| 1.7 | File Naming | Case sensitivity collision | DATA LOSS | Code-time + CI |
| 2.1 | Ingestion | Rate limiting / 429 crashes | PIPELINE HALT | Code-time + Monitoring |
| 2.2 | Ingestion | Token count errors / truncation | SILENT CORRUPTION | Code-time |
| 2.3 | Ingestion | Hallucinated entities | SILENT CORRUPTION | Code-time + Monitoring |
| 2.4 | Ingestion | Context loss across chunks | DEGRADED QUALITY | Code-time |
| 2.5 | Ingestion | UTF-8 BOM / encoding failures | PIPELINE HALT / SILENT | Code-time |
| 2.6 | Ingestion | Binary file detection failure | PIPELINE HALT | Code-time |
| 2.7 | Ingestion | Partial extraction no signal | SILENT CORRUPTION | Code-time + Monitoring |
| 3.1 | KG | Entity resolution ambiguity | DEGRADED QUALITY | Code-time + Data Quality |
| 3.2 | KG | Relationship type errors | SILENT CORRUPTION | Code-time |
| 3.3 | KG | Temporal edge conflicts | SILENT CORRUPTION | Code-time |
| 3.4 | KG | Schema evolution data loss | PIPELINE HALT / SILENT | Code-time |
| 3.5 | KG | Orphaned nodes | DEGRADED QUALITY | Monitoring |
| 3.6 | KG | Duplicate node race condition | SILENT CORRUPTION | Code-time |
| 4.1 | YAML | Special characters parse error | PIPELINE HALT | Code-time + CI |
| 4.2 | YAML | PyYAML auto type coercion | SILENT CORRUPTION | Code-time |
| 4.3 | YAML | Indentation / multiline errors | PIPELINE HALT / SILENT | Code-time + CI |
| 4.4 | YAML | Missing required fields | PIPELINE HALT / SILENT | Code-time |
| 4.5 | YAML | Delimiter detection failure | SILENT CORRUPTION | Code-time |
| 5.1 | Git | Merge conflict markers ingested | SILENT CORRUPTION | Code-time |
| 5.2 | Git | Binary file history bloat | PIPELINE HALT | Code-time |
| 5.3 | Git | Editor metadata file conflicts | DEGRADED QUALITY | Code-time |
| 5.4 | Git | LFS quota / pointer file ingestion | DATA LOSS / SILENT | Code-time + Monitoring |
| 5.5 | Git | Stale branch divergence | DEGRADED QUALITY | Code-time |
| 6.1 | Batch | Memory exhaustion (OOM) | PIPELINE HALT | Code-time + Monitoring |
| 6.2 | Batch | Checkpoint/resume failures | DATA LOSS / SILENT | Code-time |
| 6.3 | Batch | Error propagation vs. isolation | PIPELINE HALT / SILENT | Code-time |
| 6.4 | Batch | Partial write detection | SILENT CORRUPTION | Code-time |
| 6.5 | Batch | Concurrency race conditions | SILENT CORRUPTION | Code-time |
| 7.1 | Cross-Platform | Windows reserved filenames | PIPELINE HALT | Code-time |
| 7.2 | Cross-Platform | Case sensitivity collisions | DATA LOSS | Code-time + CI |
| 7.3 | Cross-Platform | Path separator hardcoding | PIPELINE HALT | Code-time |
| 7.4 | Cross-Platform | Symlink handling differences | PIPELINE HALT / SILENT | Code-time |
| 7.5 | Cross-Platform | Hidden metadata files (.DS_Store) | PIPELINE HALT | Code-time |
| 7.6 | Cross-Platform | CRLF line ending corruption | SILENT CORRUPTION | Code-time |

---

## High-Priority Items for Amplified Partners Stack

Based on the research, the following are the **highest-risk** issues for a ~4,787-file, macOS-developed, Linux-deployed vault processing into FalkorDB:

1. **UTF-8 BOM encoding (2.5)** — Windows-authored Markdown files will silently corrupt LLM prompts. Fix: `open(path, encoding='utf-8-sig')`. Zero cost, immediate.
2. **NFC/NFD unicode mismatch (1.2)** — macOS APFS normalises to NFD; all regex patterns must normalise input first. Fix: one-line `unicodedata.normalize('NFC', ...)` wrapper.
3. **Filename collision on rename (1.4)** — A dry-run collision check before any batch rename operation must be the first step. Fix: compute all target names, check for `lower()` duplicates before touching the filesystem.
4. **YAML special characters / datetime coercion (4.1, 4.2)** — Switch to `ruamel.yaml` with YAML 1.2 mode; add `yamllint` to CI.
5. **Merge conflict markers ingested (5.1)** — A one-line `grep` scan for `<<<<<<<` before any ingestion run prevents this entirely.
6. **Partial extraction with no signal (2.7)** — Check `finish_reason == "stop"` and implement a minimum entity threshold per document type.
7. **Orphaned nodes (3.5)** — Add a post-ingestion Cypher query: `MATCH (n) WHERE NOT (n)--() RETURN count(n)` as a data quality gate.
8. **Checkpoint atomicity (6.2)** — Use SQLite for the checkpoint store; mark `COMPLETED` only after the graph transaction commits.

---

## Sources

- [Microsoft Learn — Maximum Path Length Limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)
- [Stack Overflow — Atomic file rename on Windows](https://stackoverflow.com/questions/167414/is-an-atomic-file-rename-with-overwrite-possible-on-windows)
- [Stack Overflow — NFC vs NFD Unicode Normalization](https://stackoverflow.com/questions/15985888/when-to-use-unicode-normalization-forms-nfc-and-nfd)
- [AbleSet Forum — NFC vs NFD filename matching](https://forum.ableset.app/t/nfc-vs-nfd-unicode-matching/2128)
- [USENIX FAST '23 — Unsafe at Any Copy (case sensitivity data loss)](https://www.usenix.org/system/files/fast23-basu.pdf)
- [Meziantou's blog — Windows reserved filenames](https://www.meziantou.net/reserved-filenames-on-windows-con-prn-aux-nul.htm)
- [GitHub — Claude Code issue #16642 (NUL file on Windows)](https://github.com/anthropics/claude-code/issues/16642)
- [Python Discussions — UTF-8 BOM handling](https://discuss.python.org/t/utf-8-bom-not-being-consumed-when-opening-file/74870)
- [GitHub — mkdocs issue #1186 (UTF-8 BOM rendering)](https://github.com/mkdocs/mkdocs/issues/1186)
- [typedef.ai — Handle Token Limits and Rate Limits](https://www.typedef.ai/resources/handle-token-limits-rate-limits-large-scale-llm-inference)
- [Galileo.AI — Tiktoken production guide](https://galileo.ai/blog/tiktoken-guide-production-ai)
- [GitHub — tiktoken issue #236 (token truncation)](https://github.com/openai/tiktoken/issues/236)
- [arXiv — How Much Do LLMs Hallucinate in Document Q&A](https://arxiv.org/html/2603.08274v1)
- [Reddit r/LLMDevs — RAG hallucinations beyond chunking](https://www.reddit.com/r/LLMDevs/comments/1plynfw/rag_still_hallucinates_even_with_good_chunking/)
- [LinkedIn — 12 Common RAG Pipeline Failure Points](https://www.linkedin.com/posts/vpriya-krishnamurthy_ai-llm-rag-activity-7368976125600997376-crAU)
- [TigerGraph — Temporal Conflicts in Entity Resolution](https://www.tigergraph.com/blog/why-temporal-conflicts-in-entity-resolution-cause-chaos/)
- [Stack AI — Enterprise Knowledge Graphs entity resolution](https://www.stack-ai.com/insights/enterprise-knowledge-graphs-the-secret-weapon-for-better-ai-accuracy)
- [DEV Community — Schema Evolution Without Breaking Consumers](https://dev.to/alexmercedcoder/schema-evolution-without-breaking-consumers-50a9)
- [PuppyGraph — How to Build a Knowledge Graph](https://www.puppygraph.com/blog/how-to-build-knowledge-graph)
- [Graphiti GitHub issue #1083 — Orphaned nodes on episode deletion](https://github.com/getzep/graphiti/issues/1083)
- [GitHub — zk issue #24 (YAML special character parse error)](https://github.com/mickael-menu/zk/issues/24)
- [Stack Overflow — Parsing invalid YAML with PyYAML](https://stackoverflow.com/questions/54589582/parsing-probably-invalid-yaml-with-pyyaml)
- [GitHub — equinor webviz-config issue #396 (PyYAML datetime coercion)](https://github.com/equinor/webviz-config/issues/396)
- [Reddit r/ClaudeAI — YAML multiline strings in frontmatter](https://www.reddit.com/r/ClaudeAI/comments/1pln99r/til_skill_descriptions_must_be_singleline_in_yaml/)
- [Reddit r/learnpython — YAML datetime auto-typing](https://www.reddit.com/r/learnpython/comments/1qlw812/how_is_type_determined/)
- [Obsidian Forum — Merge conflicts on vault pull](https://forum.obsidian.md/t/merge-conflicts-when-i-pull-my-vault/91334)
- [Reddit r/ObsidianMD — Merge issues with Obsidian Git](https://www.reddit.com/r/ObsidianMD/comments/16key0o/merge_issues_with_obsidian_git/)
- [GitHub Well-Architected — Large Git Repositories](https://wellarchitected.github.com/library/architecture/recommendations/scaling-git-repositories/large-git-repositories/)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitHub — git-lfs issue #1101 (LFS quota)](https://github.com/git-lfs/git-lfs/issues/1101)
- [GitHub — obsidian-livesync issue #671 (metadata conflicts)](https://github.com/vrtmrz/obsidian-livesync/issues/671)
- [OneUptime — How to Fix Data Pipeline Failures](https://oneuptime.com/blog/post/2026-01-24-fix-data-pipeline-failures/view)
- [OneUptime — How to Build Batch Retry Strategies](https://oneuptime.com/blog/post/2026-01-30-batch-processing-retry-strategies/view)
- [Stack Overflow — Checkpoint long-running function](https://stackoverflow.com/questions/34155841/how-to-checkpoint-a-long-running-function-pythonically)
- [Python bug tracker #8828 — Atomic file rename](https://bugs.python.org/issue8828)
- [FalkorDB — How to Build a Knowledge Graph](https://www.falkordb.com/blog/how-to-build-a-knowledge-graph/)
- [GitHub — FalkorDB GraphRAG-SDK issue #53](https://github.com/FalkorDB/GraphRAG-SDK/issues/53)
- [Michael Brenndoerfer — Text Normalization: Unicode Forms](https://mbrenndoerfer.com/writing/text-normalization-unicode-nlp)
- [Stack Overflow — Case-sensitive path collisions on case-insensitive FS](https://stackoverflow.com/questions/63468346/case-sensitive-path-collisions-on-case-insensitive-file-system-when-i-do-git-clone)
- [Stack Overflow — Cross-platform path splitting in Python](https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python)
- [NSF PAR — Building Knowledge Graphs from Unstructured Texts](https://par.nsf.gov/servlets/purl/10401615)
- [arXiv — gBuilder: Scalable Knowledge Graph Construction](https://arxiv.org/html/2208.09705v3)
