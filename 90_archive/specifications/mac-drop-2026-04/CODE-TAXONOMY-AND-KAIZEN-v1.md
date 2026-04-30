Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

# Amplified Partners — Code Taxonomy, Error Anticipation Registry & Kaizen Department v1

## THE LAW

**Every error is anticipated. Every module is named. Every node reports back. No exceptions.**

This document is constitutional. It defines three pillars of the Amplified Partners code system:

1. **Error Anticipation Registry** — We research the problems we are likely to have when we code and when we deploy. We build the code with that in mind.
2. **Code Taxonomy** — We create a taxonomy for the code that identifies bits we can reuse. One module, many pipelines. No duplication.
3. **Kaizen Department** — We have a department that tests all the time and Kaizens it. Not a one-off test suite. A permanent, always-running department.

Mathematics decides. Not vibes. Not urgency. Not "we'll fix it later." Gates don't change. Every node reports back.

---

## How This Document Connects

| Document | Relationship |
|----------|-------------|
| `FILE-NAMING-CONVENTION-v1.md` | The code taxonomy extends the file taxonomy. Same naming philosophy, same controlled vocabulary approach. Code modules follow `{type}-{descriptive-slug}` just as files follow `{type}-{slug}-{date}-v{N}.{ext}`. |
| `VALIDATION-METHODOLOGY-v2.md` | The gates and rubrics are the enforcement mechanism. Every error in the registry maps to a validation gate. Every Kaizen cycle feeds back into the gate system. |
| `error-research-infrastructure.md` | Raw research input — 55 infrastructure errors across 8 technologies. Synthesised into Section 1. |
| `error-research-pipelines.md` | Raw research input — 41 pipeline errors across 7 areas. Synthesised into Section 1. |

---

# SECTION 1: ERROR ANTICIPATION REGISTRY

> "We research the problems we are likely to have when we code and when we deploy. We build the code with that in mind."

This is the master registry. Every known error pattern from the research phase is catalogued here with a unique ERR-ID, a defence strategy, and a mapping to the validation gate that catches it. This registry is a living document — the Kaizen Department feeds it continuously (see Section 3).

**Status definitions:**
- `researched` — Error identified, documented, not yet defended in code
- `defended` — Code defence written (guard, transform, or monitor module exists)
- `tested` — Automated test added to regression suite
- `verified` — Kaizen agent confirms defence works in production for 7 consecutive days

---

## 1.1 FalkorDB Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-FALK-001 | coding-time | service-downtime | Unbounded variable-length path queries (`[*]`) cause OOM crash, killing all graphs on the Redis process. | `guard-cypher-depth-limit`: lint all Cypher queries to reject unbounded `[*]` patterns; enforce `[*1..N]` with N ≤ 10. Monitor memory with `GRAPH.MEMORY USAGE`. | G1 (Structure) | researched |
| ERR-FALK-002 | coding-time | service-downtime | `collect()` and aggregate functions fail in multi-WITH Cypher queries — values don't survive through chained `WITH` clauses in map projections. | `guard-cypher-aggregate`: break complex projections into simpler `WITH` steps; ban `collect()` inside map literals. | G1 (Structure) | researched |
| ERR-FALK-003 | coding-time | silent-corruption | `LIMIT` clause does not constrain eager write operations — `CREATE` executes fully before `LIMIT` is applied, writing extra unintended nodes. | `guard-cypher-write-limit`: enforce `WITH ... LIMIT N` before any `CREATE`/`MERGE` in write queries. Code review lint rule. | G1 (Structure) | researched |
| ERR-FALK-004 | coding-time | degraded-performance | Index does not support not-equal (`<>`) filters — query planner falls back to full scan instead of using index. | `guard-cypher-query-plan`: validate all performance-sensitive queries with `GRAPH.EXPLAIN`; rewrite `<>` to range filters. | G5 (Benchmark) | researched |
| ERR-FALK-005 | coding-time | silent-corruption | Non-referenced relationship aliases counted only once — `MATCH (a)-[e]->(b) RETURN COUNT(b)` returns 1 instead of 2 when 2 relationships exist. | `guard-cypher-alias-ref`: lint rule requiring all relationship aliases to be referenced in `RETURN` or `WHERE`. | G1 (Structure) | researched |
| ERR-FALK-006 | deployment-time | silent-corruption | HNSW vector index returns incorrect top-K results at certain `fetch_k` thresholds on graphs with 100k+ nodes. | `monitor-vector-recall`: periodic recall test against ground truth; use `fetch_k = k * 3` minimum. Rebuild index after bulk ingestion. | G5 (Benchmark) | researched |
| ERR-FALK-007 | deployment-time | service-downtime | Long-running write queries block Redis event loop — all connections hang until write completes. | `guard-batch-write-size`: break large writes into transactions of ≤ 500 operations. Set Redis `timeout`. Monitor with `CLIENT LIST`. | G7 (Ship) | researched |
| ERR-FALK-008 | deployment-time | degraded-performance | Delta matrix drains slowly after transaction rollback, slowing subsequent write queries. | `monitor-write-latency`: track post-rollback write performance with `GRAPH.PROFILE`. Minimise rollbacks in hot paths. | G5 (Benchmark) | researched |
| ERR-FALK-009 | coding-time | degraded-performance | String memory bloat from repeated attribute values — no interning causes 30–60% heap inflation on large graphs. | `transform-string-intern`: batch `intern()` during bulk ingestion for high-cardinality-repeated fields. Monitor with `GRAPH.MEMORY USAGE`. | G5 (Benchmark) | researched |

---

## 1.2 Graphiti (Zep) Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-GRPH-001 | coding-time | data-loss | `add_triplet()` stores `source_node_uuid` and `target_node_uuid` as `None` on FalkorDB — breaks edge deduplication permanently. | `guard-graphiti-uuid-patch`: patch `edge_db_queries.py` — change `MATCH` to `MERGE`, add UUID fields to `SET` clause. Validate roundtrip after every write. | G1 (Structure) | researched |
| ERR-GRPH-002 | coding-time | silent-corruption | Duplicate entity creation when using custom database names — deduplication queries target wrong namespace. | `guard-graphiti-namespace`: use default database name; run post-ingestion duplicate-entity audit query. | G3 (Reliability) | researched |
| ERR-GRPH-003 | coding-time | service-downtime | Default `group_id` for FalkorDB is `'\_'` which fails `validate_group_id()` regex — Graphiti completely non-functional. | `guard-graphiti-group-id`: patch `helpers.py` to return valid `group_id`; pass explicit `group_id` in all `add_episode()` calls. | G1 (Structure) | researched |
| ERR-GRPH-004 | coding-time | silent-corruption | Custom edge types not persisted correctly with FalkorDB provider — properties silently dropped. | `test-graphiti-edge-roundtrip`: write + read back test after every schema extension. Verify all custom properties in `SET` clauses. | G3 (Reliability) | researched |
| ERR-GRPH-005 | coding-time | silent-corruption | Entity resolution degrades with inconsistent LLM naming — "Acme Corp" vs "Acme Corporation" not merged. | `guard-entity-normalise`: lowercasing, suffix stripping, canonical examples in prompt. Post-ingestion near-duplicate audit. | G3 (Reliability) | researched |
| ERR-GRPH-006 | deployment-time | silent-corruption | Temporal edge invalidation not triggered when LLM misses contradictory facts — stale edges remain valid. | `monitor-temporal-edge-consistency`: post-episode validation querying modified entities for `valid_at`/`invalid_at` conflicts. | G5 (Benchmark) | researched |
| ERR-GRPH-007 | deployment-time | service-downtime | LiteLLM/Ollama non-standard port integration fails with `APIConnectionError` — no graph writes possible. | `hook-pre-ingest-validate`: connectivity check from Graphiti container to LiteLLM before startup. Docker health check gate. | G7 (Ship) | researched |

---

## 1.3 Temporal.io Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-TEMP-001 | coding-time | service-downtime | Non-determinism errors after code changes to running workflows — in-flight workflows stall silently during replay. | `gate-temporal-replay`: run `WorkflowReplayer` against captured history in CI on every PR that touches workflow code. Configure `setFailWorkflowExceptionTypes`. | G1 (Structure) | researched |
| ERR-TEMP-002 | deployment-time | service-downtime | Workers stop polling / disappear from task queue — activity slots drain continuously without visible error. | `monitor-temporal-worker-slots`: instrument `activity_task_slots_available` and `workflow_task_slots_available`. Separate workflow/activity task queues. Heartbeat in all long-running activities. | G7 (Ship) | researched |
| ERR-TEMP-003 | deployment-time | degraded-performance | Sticky queue task timeout after worker restart — next workflow task routed to dead worker's queue, causing 10s delay. | `config-temporal-sticky-timeout`: set `stickyQueueScheduleToStartTimeout = 0` on batch workers. Ensure replacement workers start before old ones terminate. | G5 (Benchmark) | researched |
| ERR-TEMP-004 | coding-time | service-downtime | Infinite retry loops from uncapped activity retry policy — default `MaxAttempts = 0` means unlimited retries for 10 years. | `guard-activity-timeout`: mandatory `ScheduleToClose` timeout and explicit `MaxAttempts` on every activity. Lint rule rejects activities without timeout config. | G1 (Structure) | researched |
| ERR-TEMP-005 | coding-time | service-downtime | Premature removal of `getVersion()` / `workflow.patching()` call causes NDE on in-flight workflows. | `guard-temporal-version-removal`: query `TemporalChangeVersion` visibility to confirm zero running workflows before removing versioning code. | G1 (Structure) | researched |
| ERR-TEMP-006 | deployment-time | service-downtime | PostgreSQL connection failures in self-hosted Temporal during high load or after DB restarts. | `config-temporal-db-pool`: configure `sql.maxConns` and `sql.maxIdleConns` in Temporal's config. Health checks and restart policies on both DB and Temporal services. | G7 (Ship) | researched |
| ERR-TEMP-007 | coding-time | service-downtime | Task queue routing mismatch — workflows scheduled on queue X but workers polling queue Y. Everything queues indefinitely. | `guard-temporal-queue-assert`: startup assertion verifying registered task queue matches deployment config. `DescribeTaskQueue` check before accepting traffic. | G1 (Structure) | researched |

---

## 1.4 LangGraph Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-LANG-001 | coding-time | data-loss | Invalid state saved to checkpoint — node output not validated, corrupt state permanently bricks the thread. | `guard-langgraph-state-validate`: explicit Pydantic validation in every node function before return. Safe defaults on error. | G1 (Structure) | researched |
| ERR-LANG-002 | coding-time | degraded-performance | Infinite agent loops until recursion limit — multi-agent graphs cycle without progress, consuming token budget. | `guard-langgraph-loop-detect`: state hash at each step; terminate on duplicate hash. Explicit `step_counter` with hard ceiling. `recursion_limit` set per invocation. | G1 (Structure) | researched |
| ERR-LANG-003 | coding-time | silent-corruption | Sub-graph state updates not visible to parent graph during interrupts — parent makes decisions on stale values. | `guard-langgraph-subgraph-state`: read sub-graph state via `snapshot.tasks`. Restructure interrupts to top-level graph. | G1 (Structure) | researched |
| ERR-LANG-004 | coding-time | data-loss | Parent graph state lost when updated during sub-graph interrupt — sub-graph restarts from beginning. | `guard-langgraph-interrupt-update`: never call `update_state()` on parent while sub-graph is interrupted. Complete or cancel sub-graph first. | G1 (Structure) | researched |
| ERR-LANG-005 | coding-time | degraded-performance | Tool call failures provide no model context — agent retries identically, looping on same error. | `guard-langgraph-tool-error`: use `handle_tool_errors=True` in `ToolNode`. Custom error routing with structured context. | G3 (Reliability) | researched |
| ERR-LANG-006 | coding-time | service-downtime | Recursion limit silently overridden by wrapper frameworks — effective limit resets to 25. | `guard-langgraph-recursion-config`: pass `recursion_limit` directly in invocation config dict, never via `.with_config()`. Verify at invocation time. | G1 (Structure) | researched |
| ERR-LANG-007 | coding-time | service-downtime | PostgreSQL checkpoint `thread_id` too long — exceeds varchar limit. | `guard-langgraph-thread-id`: normalise `thread_id` to UUID (36 chars). Run `checkpointer.setup()` on first boot. | G1 (Structure) | researched |

---

## 1.5 Docker / Docker Compose Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-DOCK-001 | coding-time | service-downtime | `depends_on` with `condition: service_healthy` hangs indefinitely when health check command missing from image or `start_period` too short. | `guard-docker-healthcheck`: verify health check binary exists in image. Set `start_period ≥ 30s`. Test with `docker inspect --format='{{json .State.Health}}'`. | G7 (Ship) | researched |
| ERR-DOCK-002 | deployment-time | service-downtime | DNS resolution failures between containers on same network — intermittent `Name or service not known` after restarts. | `guard-docker-dns-retry`: retry logic with exponential backoff on initial connections. Use service names, never IPs. | G7 (Ship) | researched |
| ERR-DOCK-003 | deployment-time | service-downtime | OOM killer terminates containers without `mem_limit` set — no error in Docker logs, container simply disappears. | `config-docker-mem-limits`: mandatory `mem_limit` on every container. Budget RAM per tier before deployment. Monitor with `docker stats`. | G7 (Ship) | researched |
| ERR-DOCK-004 | coding-time | degraded-performance | Bind-mount volume permissions mismatch between host UID and container UID — writes fail silently or with obscure permission errors. | `guard-docker-volume-perms`: match container user UID to host directory owner. Test write access in entrypoint health check. | G7 (Ship) | researched |
| ERR-DOCK-005 | deployment-time | service-downtime | Docker Compose v2 `--abort-on-container-exit` kills all containers when any container exits — including short-lived migration containers. | `config-docker-compose-profiles`: use Compose profiles to separate long-running services from one-shot tasks. Never use `--abort-on-container-exit` in production. | G7 (Ship) | researched |
| ERR-DOCK-006 | deployment-time | degraded-performance | Log driver default (`json-file`) fills disk on high-throughput containers — no rotation configured. | `config-docker-log-rotation`: set `max-size` and `max-file` on all containers. Monitor disk usage. | G7 (Ship) | researched |

---

## 1.6 LiteLLM Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-LITE-001 | deployment-time | service-downtime | Fallback model routing fails when primary model raises unexpected error format — fallback logic depends on specific exception types. | `test-litellm-fallback`: integration test that simulates primary failure and verifies fallback activates. Test all configured model aliases. | G3 (Reliability) | researched |
| ERR-LITE-002 | coding-time | degraded-performance | Timeout configuration ignored for streaming responses — `timeout` parameter applies only to first chunk, not total stream duration. | `guard-litellm-stream-timeout`: implement application-level stream timeout using `asyncio.wait_for()`. Monitor total stream duration. | G5 (Benchmark) | researched |
| ERR-LITE-003 | deployment-time | silent-corruption | Cost tracking reports $0 for custom/local models — LiteLLM's pricing DB lacks entries for Ollama and custom deployments. | `monitor-litellm-cost`: weekly direct query of LiteLLM's PostgreSQL spend tables. Cross-check against provider invoices. Alert on $0 entries. | G5 (Benchmark) | researched |
| ERR-LITE-004 | deployment-time | silent-corruption | Provider misattribution in logs — Anthropic responses logged as OpenAI when using compatibility mode. | `monitor-litellm-provider-audit`: validate `model` field in response metadata matches request routing. | G3 (Reliability) | researched |
| ERR-LITE-005 | coding-time | service-downtime | Vertex AI / other providers routed to wrong endpoint due to prefix-normalisation bugs in proxy layer. | `guard-litellm-model-routing`: set `custom_llm_provider` explicitly in all model definitions. Validate routing with debug logs after config changes. | G1 (Structure) | researched |
| ERR-LITE-006 | deployment-time | degraded-performance | Client disconnect does not cancel ongoing LLM request — provider continues billing for orphaned generation. | `monitor-litellm-orphan-requests`: track active upstream connections. Alert on connections persisting after client disconnect. | G5 (Benchmark) | researched |

---

## 1.7 FastAPI Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-FAST-001 | coding-time | service-downtime | Synchronous blocking code inside `async def` blocks the entire event loop — all other requests stall. | `guard-async-hygiene`: lint rule banning `time.sleep()`, sync DB drivers, CPU-bound ops in `async def`. Use `asyncio.to_thread()` for sync calls. | G1 (Structure) | researched |
| ERR-FAST-002 | coding-time | service-downtime | CORS errors despite correct `CORSMiddleware` — middleware not registered first; auth exceptions bypass CORS headers. | `guard-fastapi-middleware-order`: `CORSMiddleware` must be first middleware registered. Explicit origin list when `allow_credentials=True`. | G1 (Structure) | researched |
| ERR-FAST-003 | coding-time | degraded-performance | Middleware execution order is LIFO, not declaration order — auth middleware added after CORS executes before it. | `guard-fastapi-middleware-order`: register middleware in reverse execution order. Document expected order in config comments. | G1 (Structure) | researched |
| ERR-FAST-004 | coding-time | service-downtime | `InjectedState` treated as required tool parameter — validation failures on valid tool calls via LangGraph CLI. | `guard-fastapi-injected-state`: use `Annotated` with `InjectedState`. Route tool registration through `ToolNode` not raw FastAPI. | G1 (Structure) | researched |
| ERR-FAST-005 | coding-time | degraded-performance | Request validation 422 errors expose internal field names and may be truncated by clients. | `guard-fastapi-validation-handler`: custom `RequestValidationError` handler that sanitises output. Log full details server-side. | G3 (Reliability) | researched |

---

## 1.8 PostgreSQL / pgvector / TimescaleDB Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-PGVT-001 | coding-time | service-downtime | PgBouncer transaction mode incompatible with prepared statements — intermittent `prepared statement already exists` errors. | `config-pgbouncer-no-prepare`: set `prepare_threshold=0` in psycopg. Disable client-side prepared statements for all pooled connections. | G1 (Structure) | researched |
| ERR-PGVT-002 | coding-time | degraded-performance | pgvector HNSW index not used for filtered vector queries — planner falls back to sequential scan with WHERE clauses. | `guard-pgvector-filtered-index`: use partial indexes for common filter subsets. `EXPLAIN ANALYZE` all vector queries. Set `hnsw.ef_search` appropriately. | G5 (Benchmark) | researched |
| ERR-PGVT-003 | deployment-time | degraded-performance | HNSW index rebuild is memory-intensive — requires GBs of RAM, blocks production queries during rebuild. | `config-pgvector-index-maintenance`: load data before index creation. Use `CREATE INDEX CONCURRENTLY`. Schedule in maintenance windows. | G5 (Benchmark) | researched |
| ERR-PGVT-004 | deployment-time | silent-corruption | IVFFlat index recall degrades silently as data grows — cluster assignments become suboptimal with no error signal. | `monitor-vector-recall`: periodic exact-vs-approximate recall test. Alert when recall drops below 90%. Consider HNSW migration. | G5 (Benchmark) | researched |
| ERR-PGVT-005 | deployment-time | service-downtime | TimescaleDB `cagg_migrate()` fails on continuous aggregates with time bucket offsets — blocks database upgrades. | `guard-timescale-cagg-migrate`: migrate non-offset aggregates first. Pre-check catalog schema. Test migration in staging. | G7 (Ship) | researched |
| ERR-PGVT-006 | deployment-time | silent-corruption | Continuous aggregate watermark in the future suppresses real-time data — queries return stale results silently. | `monitor-timescale-watermark`: check watermark with `cagg_watermark()`. Alert when watermark > `now()`. Compare cagg vs hypertable for latest bucket. | G5 (Benchmark) | researched |
| ERR-PGVT-007 | deployment-time | degraded-performance | Stale query statistics cause suboptimal vector query plans after heavy inserts. | `hook-post-ingest-analyze`: run `ANALYZE VERBOSE` after every bulk ingestion batch. Increase `default_statistics_target` for vector columns. | G5 (Benchmark) | researched |
| ERR-PGVT-008 | coding-time | silent-corruption | Historical data inserts not reflected in TimescaleDB real-time aggregates — backfilled data silently excluded. | `hook-post-backfill-refresh`: mandatory `refresh_continuous_aggregate()` after any historical data load. | G3 (Reliability) | researched |

---

## 1.9 File Naming & Taxonomy Enforcement Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-NAME-001 | coding-time | service-downtime | Windows 260-character path limit (`MAX_PATH`) causes silent failures or `OSError` on deeply nested vault paths. | `guard-path-length`: path budget validator capping total path at 240 chars. Log warning when remaining budget < 50 chars. | G1 (Structure) | researched |
| ERR-NAME-002 | coding-time | silent-corruption | Unicode normalisation mismatches (NFC vs NFD) — macOS uses NFD, Linux uses NFC. Same filename appears different to regex. | `transform-nfc-normalise`: apply `unicodedata.normalize('NFC', ...)` to all path comparison utilities. Normalise at ingest. | G1 (Structure) | researched |
| ERR-NAME-003 | coding-time | silent-corruption | Regex edge cases — greedy matching, missing anchors, dot-all flags cause validators to accept invalid filenames or reject valid ones. | `test-regex-adversarial`: adversarial test suite with 100+ edge cases per pattern. Anchored patterns only. | G3 (Reliability) | researched |
| ERR-NAME-004 | coding-time | data-loss | Filename collision during batch rename — target name already exists, original file silently overwritten. | `guard-collision-check`: dry-run collision detection before any batch rename. Abort on collision. | G1 (Structure) | researched |
| ERR-NAME-005 | coding-time | data-loss | Non-atomic rename leaving partial state — file disappears between delete and replace on crash. | `guard-atomic-rename`: use `os.replace()` (atomic on POSIX) or write-to-temp-then-rename pattern. | G1 (Structure) | researched |
| ERR-NAME-006 | coding-time | silent-corruption | Timestamp metadata lost during rename — `mtime`/`ctime` reset, breaking sort-by-date and incremental processing. | `guard-rename-preserve-meta`: capture and restore `os.stat()` timestamps around rename operations. | G3 (Reliability) | researched |
| ERR-NAME-007 | coding-time | data-loss | Case sensitivity collision between macOS (case-insensitive) and Linux (case-sensitive) — one file silently masked. | `guard-case-normalise`: enforce lowercase-only rule from naming convention. CI gate rejects mixed-case filenames. | G1 (Structure) | researched |

---

## 1.10 Document Ingestion Pipeline Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-INGS-001 | coding-time | service-downtime | Rate limiting and exponential backoff failures — naïve concurrent requests exhaust TPM, pipeline crashes on 429. | `guard-rate-limiter`: token-aware sliding window rate limiter. Exponential backoff with jitter. Persistent completion ledger by file hash. | G3 (Reliability) | researched |
| ERR-INGS-002 | coding-time | silent-corruption | Token count estimation errors cause silent truncation — LLM receives partial content, returns partial extraction with no error. | `guard-token-count`: use model-specific tokeniser for exact counts. Chunk at 80% of context window. Validate output completeness against input section count. | G3 (Reliability) | researched |
| ERR-INGS-003 | coding-time | silent-corruption | Hallucinated entities and relationship fabrication — LLM invents entities not present in source. | `guard-entity-ground`: constrained extraction prompts requiring source citations. Post-extraction entity verification against source text. Hallucination rate metrics. | G3 (Reliability) | researched |
| ERR-INGS-004 | coding-time | silent-corruption | Context loss across chunk boundaries — entities split across chunks produce incomplete or incorrect relationships. | `guard-chunk-overlap`: sliding window chunking with 15% overlap. Cross-chunk entity linking pass. | G3 (Reliability) | researched |
| ERR-INGS-005 | coding-time | service-downtime | UTF-8 BOM and encoding detection failures — BOM character corrupts first token or causes `UnicodeDecodeError`. | `transform-encoding-normalise`: use `utf-8-sig` codec. Pre-flight encoding scan with `chardet`. Strip BOM before processing. | G1 (Structure) | researched |
| ERR-INGS-006 | coding-time | silent-corruption | Binary file detection failures — PDFs, images, or compiled files fed to text extraction pipeline, producing garbage. | `guard-binary-detect`: magic-byte pre-filter using `python-magic`. Reject non-text MIME types before ingestion. | G1 (Structure) | researched |
| ERR-INGS-007 | coding-time | silent-corruption | Partial extraction with no failure signal — LLM returns subset of entities, pipeline marks file as complete. | `gate-extraction-completeness`: compare extracted entity count against expected density. Flag files with suspiciously low extraction yield. | G3 (Reliability) | researched |

---

## 1.11 Knowledge Graph Construction Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-KGRA-001 | coding-time | degraded-performance | Entity resolution ambiguity (coreference) — "Ewan", "Mr Bramley", "the founder" not linked to same node. | `guard-entity-coreference`: canonical entity examples in extraction prompt. Post-ingestion coreference resolution pass. | G3 (Reliability) | researched |
| ERR-KGRA-002 | coding-time | silent-corruption | Relationship extraction false positives and type misclassification — wrong graph topology from LLM errors. | `guard-relationship-schema`: enforce allowed relationship types via schema constraint. Reject unrecognised types. Confidence threshold on extraction. | G3 (Reliability) | researched |
| ERR-KGRA-003 | coding-time | silent-corruption | Temporal edge conflicts — contradictory `valid_at`/`invalid_at` timestamps on same relationship when multiple episodes processed concurrently. | `guard-temporal-edge-resolve`: serialise writes per entity. Post-write consistency check on temporal edges. | G3 (Reliability) | researched |
| ERR-KGRA-004 | coding-time | service-downtime | Graph schema evolution without migration — new node types break queries expecting old schema. | `guard-schema-version`: schema versioning with migration scripts. Backward-compatible additions only; breaking changes require migration. | G7 (Ship) | researched |
| ERR-KGRA-005 | deployment-time | degraded-performance | Orphaned nodes — nodes with no relationships accumulate, inflating counts and degrading traversal quality. | `monitor-orphan-nodes`: scheduled query for nodes with zero relationships. Alert on orphan count exceeding threshold. | G5 (Benchmark) | researched |
| ERR-KGRA-006 | coding-time | silent-corruption | Duplicate node creation from MERGE vs CREATE race condition — parallel workers both CREATE instead of MERGE. | `guard-node-constraint`: unique constraint on entity key properties. Use `MERGE` exclusively; ban `CREATE` for entity nodes. | G1 (Structure) | researched |

---

## 1.12 YAML Frontmatter Processing Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-YAML-001 | coding-time | service-downtime | Special characters in unquoted YAML values — colons, brackets, ampersands break parsing. | `guard-yaml-parse`: always quote string values containing special characters. CI yamllint gate. | G1 (Structure) | researched |
| ERR-YAML-002 | coding-time | silent-corruption | PyYAML automatic type coercion — date-like strings auto-parsed to `datetime`, booleans from `yes`/`no`. | `guard-yaml-coercion`: use `ruamel.yaml` in YAML 1.2 mode or explicit `!!str` tags. Validate output types post-parse. | G1 (Structure) | researched |
| ERR-YAML-003 | coding-time | silent-corruption | Indentation errors and multiline string mishandling — content silently truncated or merged with adjacent fields. | `guard-yaml-indent`: yamllint CI gate with strict indentation rules. Validate multiline fields round-trip. | G1 (Structure) | researched |
| ERR-YAML-004 | coding-time | silent-corruption | Missing required fields — pipeline continues with `None` values, downstream crashes or graph nodes missing properties. | `guard-yaml-required-fields`: Pydantic model for frontmatter with required fields. Reject files missing required fields at ingest. | G1 (Structure) | researched |
| ERR-YAML-005 | coding-time | service-downtime | Frontmatter delimiter detection failures — `---` in document body or `\ufeff---` with BOM treated as delimiter. | `guard-yaml-delimiter`: use `python-frontmatter` library with strict mode. Handle BOM before delimiter detection. | G1 (Structure) | researched |

---

## 1.13 Git-Based Vault Management Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-GITS-001 | coding-time | silent-corruption | Merge conflicts in concurrent edits — conflict markers (`<<<<<<<`) ingested as document content. | `guard-conflict-marker-scan`: pipeline gate that scans for conflict markers before ingestion. Reject files with markers. | G1 (Structure) | researched |
| ERR-GITS-002 | coding-time | degraded-performance | Binary file history bloat — large binaries in Git grow `.git/objects`, causing slow clones and CI timeouts. | `guard-git-lfs-setup`: Git LFS for files > 1MB. Pre-commit hook rejecting large binary additions to main repo. | G5 (Benchmark) | researched |
| ERR-GITS-003 | coding-time | degraded-performance | Obsidian/editor metadata files (`.obsidian/`, `.DS_Store`) causing spurious merge conflicts. | `config-gitignore`: comprehensive `.gitignore` including `.obsidian/workspace.json`, `.DS_Store`, `Thumbs.db`. | G1 (Structure) | researched |
| ERR-GITS-004 | coding-time | data-loss | Git LFS pointer file corruption — pointer file ingested as document content instead of actual file. | `guard-lfs-pointer-detect`: check for LFS pointer format (`version https://git-lfs.github.com/...`) before ingestion. | G1 (Structure) | researched |
| ERR-GITS-005 | deployment-time | silent-corruption | Branch sync conflicts and stale branch divergence — pipeline processes outdated content from un-merged branches. | `guard-git-pinned-commit`: pipeline reads from pinned commit hash, not branch HEAD. Validate freshness against main. | G3 (Reliability) | researched |

---

## 1.14 Batch File Processing Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-BATC-001 | coding-time | service-downtime | Memory exhaustion on large batches (OOM) — loading full file list into memory instead of streaming. | `guard-batch-streaming`: generator-based file iteration. Process one file at a time. Set container `mem_limit`. | G7 (Ship) | researched |
| ERR-BATC-002 | coding-time | data-loss | Checkpoint/resume failures — hash mismatch on file content between checkpoint and resume loses completed work or double-processes. | `guard-checkpoint-integrity`: hash-based completion ledger using content hash, not filename. Idempotent write operations. | G3 (Reliability) | researched |
| ERR-BATC-003 | coding-time | service-downtime | Error propagation — one bad file kills entire batch via unhandled exception. | `guard-batch-isolation`: per-file try/except with structured error logging. Dead-letter queue for failed files. Continue processing remaining. | G3 (Reliability) | researched |
| ERR-BATC-004 | coding-time | silent-corruption | Partial completion tracking — write interrupted mid-operation leaves graph in inconsistent state (nodes without relationships). | `guard-transactional-write`: wrap node + relationship creation in single transaction. Verify write completeness. | G3 (Reliability) | researched |
| ERR-BATC-005 | coding-time | silent-corruption | Concurrency race conditions in parallel workers — duplicate nodes from concurrent MERGE operations on same entity. | `guard-worker-partitioning`: partition files by entity namespace to prevent concurrent writes to same graph region. | G3 (Reliability) | researched |

---

## 1.15 Cross-Platform File Handling Errors

| Error ID | Phase | Severity | Description | Defence | Gate | Status |
|----------|-------|----------|-------------|---------|------|--------|
| ERR-PLAT-001 | coding-time | service-downtime | Windows reserved filenames (CON, PRN, NUL, COM1–COM9, LPT1–LPT9) — writes go to device instead of file. | `guard-reserved-filename`: explicit validator rejecting Windows reserved names. Block at naming convention enforcement. | G1 (Structure) | researched |
| ERR-PLAT-002 | coding-time | data-loss | Case sensitivity collision on case-insensitive filesystems — `README.md` and `readme.md` shadow each other. | `guard-case-normalise`: enforce lowercase-only (already in naming convention). CI gate scans for case collisions. | G1 (Structure) | researched |
| ERR-PLAT-003 | coding-time | service-downtime | Path separator hardcoding — `\` vs `/` breaks cross-platform deployments. | `guard-path-separator`: use `pathlib.Path` or `os.path.join()` exclusively. Lint rule banning hardcoded separators. | G1 (Structure) | researched |
| ERR-PLAT-004 | coding-time | degraded-performance | Symlink handling differences — Windows requires elevated permissions for symlinks; Linux follows them silently. | `guard-symlink-policy`: resolve all symlinks at pipeline entry. Document symlink behaviour per platform. | G3 (Reliability) | researched |
| ERR-PLAT-005 | coding-time | degraded-performance | Extended attributes and hidden metadata files (`.DS_Store`, `Thumbs.db`) — binary files crash text extraction or inflate counts. | `guard-hidden-file-filter`: exclude hidden files and system metadata at pipeline entry. Pattern-based blocklist. | G1 (Structure) | researched |
| ERR-PLAT-006 | coding-time | silent-corruption | Line ending differences (CRLF vs LF) — YAML parse failures, wrong token counts, incorrect line-number references. | `transform-line-ending-normalise`: `.gitattributes` with `* text=auto`. Pipeline normalisation to LF at ingest. | G1 (Structure) | researched |

---

## Defence Coverage Matrix

### Errors by Technology

| Technology | Code | Total Errors | Coding-Time | Deployment-Time | Data-Loss | Service-Downtime | Silent-Corruption | Degraded-Performance |
|-----------|------|-------------|-------------|-----------------|-----------|------------------|-------------------|---------------------|
| FalkorDB | FALK | 9 | 5 | 4 | 0 | 3 | 3 | 3 |
| Graphiti (Zep) | GRPH | 7 | 5 | 2 | 1 | 2 | 4 | 0 |
| Temporal.io | TEMP | 7 | 4 | 3 | 0 | 6 | 0 | 1 |
| LangGraph | LANG | 7 | 7 | 0 | 2 | 2 | 1 | 2 |
| Docker/Compose | DOCK | 6 | 2 | 4 | 0 | 4 | 0 | 2 |
| LiteLLM | LITE | 6 | 2 | 4 | 0 | 2 | 2 | 2 |
| FastAPI | FAST | 5 | 5 | 0 | 0 | 3 | 0 | 2 |
| PostgreSQL/pgvector/TimescaleDB | PGVT | 8 | 3 | 5 | 0 | 2 | 3 | 3 |
| File Naming & Taxonomy | NAME | 7 | 7 | 0 | 3 | 1 | 3 | 0 |
| Document Ingestion | INGS | 7 | 7 | 0 | 0 | 2 | 5 | 0 |
| Knowledge Graph Construction | KGRA | 6 | 5 | 1 | 0 | 1 | 3 | 2 |
| YAML Frontmatter | YAML | 5 | 5 | 0 | 0 | 2 | 3 | 0 |
| Git Vault Management | GITS | 5 | 4 | 1 | 1 | 0 | 2 | 2 |
| Batch Processing | BATC | 5 | 5 | 0 | 1 | 2 | 2 | 0 |
| Cross-Platform | PLAT | 6 | 6 | 0 | 1 | 2 | 1 | 2 |
| **TOTAL** | | **96** | **72** | **24** | **9** | **34** | **32** | **21** |

### Defence Type Distribution

| Defence Type | Count | Description |
|-------------|-------|-------------|
| `guard-*` | 62 | Input validation, sanitisation, gate enforcement — prevents error at coding-time |
| `monitor-*` | 12 | Health check, metric collection — detects error at deployment-time |
| `transform-*` | 5 | Data normalisation — corrects data before processing |
| `config-*` | 8 | Configuration enforcement — prevents misconfiguration |
| `test-*` | 4 | Dedicated test suites — verifies defence works |
| `hook-*` | 3 | Pre/post action triggers — enforces sequencing |
| `gate-*` | 2 | Mandatory checkpoints — blocks progression on failure |

### Automated vs Manual

| Category | Automated Test Possible | Manual Check Only |
|----------|------------------------|-------------------|
| Coding-time defences (72) | 68 | 4 |
| Deployment-time defences (24) | 18 | 6 |
| **Total** | **86 (90%)** | **10 (10%)** |

---

# SECTION 2: CODE TAXONOMY — REUSABLE COMPONENTS

> "We create a taxonomy for the code that may identify bits we can reuse."

Every code module in the Amplified Partners stack has a type, a name, and a known set of consumers. One module, many pipelines. No duplication. If you write a guard for Unicode normalisation once, every pipeline that touches a filename uses that same guard.

---

## 2.1 Code Module Types (Controlled Vocabulary)

Same philosophy as the file naming convention: controlled vocabulary, lowercase tokens, no ambiguity. Each module type has a clear purpose and a clear boundary.

| Token | What It Is | Example Module | Boundary |
|-------|-----------|----------------|----------|
| `guard` | Input validation, sanitisation, gate enforcement | `guard-unicode-normalise`, `guard-yaml-parse`, `guard-cypher-depth-limit` | Checks input. Returns pass/fail. Never transforms data — that's `transform`'s job. |
| `adapter` | Interface between two systems | `adapter-falkordb-graphiti`, `adapter-litellm-proxy`, `adapter-linear-graphql` | Translates protocols. Doesn't contain business logic. |
| `pipeline` | Multi-step data processing flow | `pipeline-vault-ingest`, `pipeline-file-rename`, `pipeline-graphiti-extract` | Orchestrates a sequence of guards, transforms, and writes. |
| `monitor` | Health check, metric collection, alerting | `monitor-vector-recall`, `monitor-orphan-nodes`, `monitor-temporal-worker-slots` | Reads state. Never writes. Emits metrics and alerts. |
| `gate` | Mandatory quality/validation checkpoint | `gate-naming-convention`, `gate-pudding-score`, `gate-extraction-completeness` | Blocks progression. Returns pass/fail with evidence. Constitutional — cannot be skipped. |
| `transform` | Data transformation, normalisation | `transform-nfc-normalise`, `transform-yaml-frontmatter`, `transform-line-ending-normalise` | Transforms data deterministically. No side effects. Idempotent. |
| `test` | Test suite, fixture, assertion | `test-regex-adversarial`, `test-graphiti-dedup`, `test-litellm-fallback` | Validates behaviour. Does not change system state. |
| `hook` | Pre/post action trigger | `hook-pre-ingest-validate`, `hook-post-deploy-verify`, `hook-post-ingest-analyze` | Fires automatically at lifecycle points. Thin — delegates to guards, monitors, or transforms. |
| `client` | API client, external service wrapper | `client-linear`, `client-falkordb`, `client-litellm` | Wraps external API. Handles auth, retry, serialisation. No business logic. |
| `worker` | Background job processor | `worker-temporal-build`, `worker-kaizen-cycle`, `worker-chaos-nightly` | Long-running process polling a task queue. Executes workflows. |
| `prompt` | LLM prompt template | `prompt-architect-v2`, `prompt-enforcer-v1`, `prompt-extractor-entity` | Text template with variable slots. Versioned. |
| `rubric` | Scoring/evaluation criteria | `rubric-code-quality`, `rubric-extraction-accuracy`, `rubric-pudding-score` | Defines scoring dimensions and thresholds. Used by gates. |
| `config` | Configuration, env vars, feature flags | `config-docker-compose`, `config-litellm-models`, `config-temporal-db-pool` | Static or environment-driven settings. Never contains logic. |
| `util` | Shared utility function | `util-path-safe`, `util-collision-check`, `util-hash-content` | Pure function. No side effects. Used by multiple modules. |
| `schema` | Data schema definition | `schema-node-report`, `schema-frontmatter`, `schema-error-registry-entry` | Pydantic model, JSON Schema, or TypedDict. Defines shape. |
| `migration` | Database/schema migration | `migration-006-add-interview-tables`, `migration-007-graph-schema-v2` | Ordered, idempotent, reversible. Numbered sequentially. |
| `fixture` | Test data, seed data, ground truth | `fixture-recall-ground-truth`, `fixture-adversarial-filenames`, `fixture-sample-vault` | Static data for testing. Never generated at runtime. |
| `workflow` | Temporal workflow definition | `workflow-planner`, `workflow-build`, `workflow-kaizen`, `workflow-chaos` | Deterministic orchestration code. No direct I/O — delegates to activities. |
| `activity` | Temporal activity definition | `activity-fetch-linear-issue`, `activity-run-agent`, `activity-git-commit` | Side-effectful operation called by workflows. Has timeout and retry config. |
| `mcp-server` | MCP (Model Context Protocol) server | `mcp-server-telegram`, `mcp-server-postgresql`, `mcp-server-filesystem` | JSON-RPC over stdio. Exposes tools to agents. |

### Adding New Type Tokens

Same process as the file naming convention:

1. Check existing types — does one already cover this?
2. If genuinely new, propose the token (single lowercase word or hyphenated compound, ≤ 16 characters)
3. Add it to this table with a definition, example, and boundary description
4. Update the convention enforcer
5. Document the change in this file's version history

---

## 2.2 Module Naming Convention

Every code module follows:

```
{type}-{descriptive-slug}
```

### Rules

| Rule | Standard |
|------|----------|
| **Format** | `{type}-{descriptive-slug}` — type token from Section 2.1, then hyphen, then kebab-case description |
| **Case** | All lowercase, always |
| **Separator** | Hyphens only — no underscores, no dots, no spaces |
| **Slug length** | 1-5 words — enough to be descriptive, short enough to type |
| **Versioning** | Append `-v{N}` only for prompts and rubrics where multiple versions coexist. Code modules use git, not filename versions. |
| **File extension** | Determined by implementation language: `.py`, `.ts`, `.sh`, `.yaml`, `.md` |

### Cross-Reference to File Naming Convention

| File Naming Type Token | Code Module Type Token | Relationship |
|----------------------|----------------------|-------------|
| `script` | `util`, `guard`, `transform` | Scripts may contain multiple code module types — decompose to typed modules |
| `config` | `config` | Same token, same purpose |
| `test` | `test`, `fixture` | Code taxonomy splits test data (fixture) from test logic (test) |
| `prompt` | `prompt` | Same token, same purpose |
| `rubric` | `rubric` | Same token, same purpose |
| `template` | `schema` | File templates map to schema definitions in code |

### Examples

```
guard-unicode-normalise.py          ← guard module, Python
guard-cypher-depth-limit.py         ← guard module, validates Cypher queries
adapter-falkordb-graphiti.py        ← adapter between FalkorDB and Graphiti
pipeline-vault-ingest.py            ← multi-step ingestion pipeline
monitor-vector-recall.py            ← scheduled recall test
gate-naming-convention.py           ← blocks non-compliant files
transform-nfc-normalise.py          ← Unicode NFC normalisation
test-regex-adversarial.py           ← adversarial regex test suite
hook-pre-ingest-validate.py         ← fires before ingestion starts
client-linear.py                    ← Linear API wrapper
worker-kaizen-cycle.py              ← Kaizen department worker
prompt-enforcer-v1.md               ← enforcer agent prompt
rubric-extraction-accuracy.md       ← extraction quality scoring
config-docker-compose.yaml          ← Docker stack configuration
util-hash-content.py                ← content hashing utility
schema-node-report.py               ← node report data structure
workflow-kaizen.py                   ← Temporal KaizenWorkflow definition
activity-run-agent.py               ← Temporal activity for agent execution
mcp-server-telegram.py              ← Telegram MCP server
```

---

## 2.3 Reusability Matrix

This is the key deliverable. One module, many pipelines. The checkmarks show where each module is used.

| Module | HoundDog Discovery | Vault Ingestion | Graphiti Extraction | Cove Build Pipeline | Naming Convention Enforcement | PUDDING Validation | Kaizen Testing |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `guard-unicode-normalise` | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| `guard-yaml-parse` | — | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| `guard-yaml-required-fields` | — | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| `guard-collision-check` | — | — | — | — | ✓ | — | ✓ |
| `guard-path-length` | ✓ | ✓ | — | — | ✓ | — | ✓ |
| `guard-binary-detect` | ✓ | ✓ | ✓ | — | — | — | ✓ |
| `guard-conflict-marker-scan` | — | ✓ | ✓ | ✓ | — | — | ✓ |
| `guard-entity-normalise` | — | — | ✓ | — | — | ✓ | ✓ |
| `guard-entity-ground` | — | — | ✓ | — | — | ✓ | ✓ |
| `guard-cypher-depth-limit` | ✓ | — | ✓ | — | — | — | ✓ |
| `guard-cypher-write-limit` | — | — | ✓ | — | — | — | ✓ |
| `guard-rate-limiter` | ✓ | ✓ | ✓ | ✓ | — | — | — |
| `guard-batch-isolation` | — | ✓ | ✓ | ✓ | ✓ | — | — |
| `guard-async-hygiene` | — | — | — | ✓ | — | — | ✓ |
| `guard-langgraph-state-validate` | — | — | — | ✓ | — | — | ✓ |
| `guard-temporal-replay` | — | — | — | ✓ | — | — | ✓ |
| `guard-activity-timeout` | — | — | — | ✓ | — | — | ✓ |
| `transform-nfc-normalise` | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| `transform-encoding-normalise` | — | ✓ | ✓ | — | — | — | ✓ |
| `transform-line-ending-normalise` | — | ✓ | ✓ | — | ✓ | — | ✓ |
| `transform-yaml-frontmatter` | — | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| `monitor-vector-recall` | — | — | ✓ | — | — | — | ✓ |
| `monitor-orphan-nodes` | — | — | ✓ | — | — | — | ✓ |
| `monitor-temporal-worker-slots` | — | — | — | ✓ | — | — | ✓ |
| `monitor-litellm-cost` | ✓ | ✓ | ✓ | ✓ | — | — | ✓ |
| `monitor-timescale-watermark` | — | — | — | — | — | — | ✓ |
| `gate-naming-convention` | — | ✓ | — | ✓ | ✓ | — | ✓ |
| `gate-pudding-score` | — | — | — | — | — | ✓ | ✓ |
| `gate-extraction-completeness` | — | ✓ | ✓ | — | — | — | ✓ |
| `client-falkordb` | ✓ | — | ✓ | — | — | — | ✓ |
| `client-linear` | — | — | — | ✓ | — | — | ✓ |
| `client-litellm` | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| `util-hash-content` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `util-path-safe` | ✓ | ✓ | — | — | ✓ | — | ✓ |
| `schema-node-report` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `schema-error-registry-entry` | — | — | — | — | — | — | ✓ |

### Reuse Counts (Top Modules)

| Module | Used By (# pipelines) |
|--------|----------------------|
| `util-hash-content` | 7 |
| `schema-node-report` | 7 |
| `guard-unicode-normalise` | 6 |
| `transform-nfc-normalise` | 6 |
| `client-litellm` | 6 |
| `guard-yaml-parse` | 5 |
| `guard-yaml-required-fields` | 5 |
| `transform-yaml-frontmatter` | 5 |
| `monitor-litellm-cost` | 5 |
| `guard-path-length` | 4 |
| `util-path-safe` | 4 |

This is the anti-duplication payoff. Seven modules are shared across 5+ pipelines. Writing them once, testing them once, hardening them once — and every pipeline benefits.

---

## 2.4 Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                              │
│                                                                         │
│  workflow-planner ──▶ workflow-build ──▶ workflow-quality-gate           │
│       │                    │                    │                        │
│       ▼                    ▼                    ▼                        │
│  activity-fetch-     activity-run-agent   activity-quality-check        │
│  linear-issue             │                    │                        │
│       │                   │                    │                        │
│       ▼                   ▼                    ▼                        │
│  client-linear       client-litellm      rubric-code-quality           │
│                           │               rubric-extraction-accuracy    │
│                           ▼                                             │
│                    prompt-architect-v2                                   │
│                    prompt-enforcer-v1                                    │
│                    prompt-extractor-entity                               │
└─────────────────────────────────────────────────────────────────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE LAYER                                   │
│                                                                         │
│  pipeline-vault-ingest ──────────────────▶ pipeline-graphiti-extract    │
│       │                                           │                     │
│       ▼                                           ▼                     │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  GUARD WALL │  │  TRANSFORM WALL  │  │   GATE WALL      │          │
│  │             │  │                  │  │                   │          │
│  │ guard-      │  │ transform-nfc-   │  │ gate-naming-     │          │
│  │  binary-    │  │  normalise       │  │  convention      │          │
│  │  detect     │  │                  │  │                   │          │
│  │             │  │ transform-       │  │ gate-extraction-  │          │
│  │ guard-      │  │  encoding-       │  │  completeness    │          │
│  │  yaml-parse │  │  normalise       │  │                   │          │
│  │             │  │                  │  │ gate-pudding-     │          │
│  │ guard-      │  │ transform-line-  │  │  score           │          │
│  │  conflict-  │  │  ending-         │  │                   │          │
│  │  marker-    │  │  normalise       │  └──────────────────┘          │
│  │  scan       │  │                  │                                  │
│  │             │  │ transform-yaml-  │                                  │
│  │ guard-rate- │  │  frontmatter     │                                  │
│  │  limiter    │  │                  │                                  │
│  │             │  └──────────────────┘                                  │
│  │ guard-      │                                                        │
│  │  entity-    │                                                        │
│  │  normalise  │                                                        │
│  └─────────────┘                                                        │
└─────────────────────────────────────────────────────────────────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                       │
│                                                                         │
│  client-falkordb ◄──── adapter-falkordb-graphiti ────▶ Graphiti SDK    │
│       │                                                                 │
│       ▼                                                                 │
│  FalkorDB (graph + vector)                                              │
│  PostgreSQL + pgvector + TimescaleDB (relational + vector + time)       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        KAIZEN LAYER (always running)                    │
│                                                                         │
│  worker-kaizen-cycle                                                    │
│       │                                                                 │
│       ├──▶ monitor-vector-recall                                        │
│       ├──▶ monitor-orphan-nodes                                         │
│       ├──▶ monitor-temporal-worker-slots                                │
│       ├──▶ monitor-litellm-cost                                         │
│       ├──▶ monitor-timescale-watermark                                  │
│       │                                                                 │
│  worker-chaos-nightly                                                   │
│       │                                                                 │
│       ├──▶ test-regex-adversarial                                       │
│       ├──▶ test-graphiti-dedup                                          │
│       ├──▶ test-litellm-fallback                                        │
│       │                                                                 │
│  schema-node-report ◄── (every node in every pipeline reports here)     │
│  schema-error-registry-entry ◄── (new errors feed the registry)         │
│                                                                         │
│  util-hash-content ◄── (shared by all layers)                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Module Dependency Summary

```
Guards depend on: utils, schemas
Transforms depend on: utils
Gates depend on: guards, rubrics, schemas
Monitors depend on: clients, schemas
Pipelines depend on: guards, transforms, gates, clients, adapters
Workflows depend on: activities
Activities depend on: pipelines, clients, prompts
Workers depend on: workflows
Tests depend on: fixtures, guards, transforms, clients
Hooks depend on: guards, monitors, transforms
```

---

# SECTION 3: THE KAIZEN DEPARTMENT — CONTINUOUS TESTING

> "We have a department that tests all the time and Kaizens it."

The Kaizen Department is not a one-off test suite. It is a permanent, always-running division of the system that:
1. Detects errors in production
2. Registers them in the Error Anticipation Registry
3. Builds defences
4. Tests the defences
5. Verifies they hold
6. Promotes them to constitutional gates

It maps to existing Temporal workflows (`KaizenWorkflow`, `ChaosWorkflow`) and extends them with four new monitors.

---

## 3.1 Department Structure

### Existing Agents (Enhanced)

| Agent | Schedule | Temporal Workflow | Enhancement |
|-------|----------|------------------|-------------|
| **Kaizen Agent** | Daily at 03:00 UTC | `KaizenWorkflow` | Now cross-references Error Anticipation Registry. Prioritises errors by severity. Runs all regression tests for `defended` and `tested` status errors. Promotes `tested` → `verified` after 7 consecutive clean days. |
| **Chaos Agent** | Nightly 01:00–04:00 UTC | `ChaosWorkflow` | Now informed by registry. Targets error patterns from `researched` entries — specifically tries to trigger them. Never touches PostgreSQL data or Temporal state. Generates structured failure reports. |

### New Agents

| Agent | Schedule | Purpose | Implementation |
|-------|----------|---------|----------------|
| **Recall Monitor** | Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC) | Tests vector search recall against ground truth set. Compares FalkorDB HNSW results and pgvector HNSW results against exact search. Alerts when recall drops below 90%. Catches ERR-FALK-006, ERR-PGVT-004. | New Temporal schedule → `RecallMonitorWorkflow` |
| **Graph Health Monitor** | Every 6 hours (01:00, 07:00, 13:00, 19:00 UTC) | Checks for orphaned nodes, duplicate entities, stale temporal edges, and schema consistency. Catches ERR-KGRA-005, ERR-KGRA-006, ERR-GRPH-002, ERR-GRPH-006. | New Temporal schedule → `GraphHealthWorkflow` |
| **Convention Enforcer** | On every file change (webhook-triggered) | Validates naming convention compliance on new/modified files. Blocks non-compliant files from entering any pipeline. Catches ERR-NAME-001 through ERR-NAME-007. | Git webhook → FastAPI endpoint → `ConventionEnforcerWorkflow` |
| **Regression Sentinel** | On every deployment | Re-runs all tests for `verified` status errors. If any previously-verified defence fails, immediately reverts to `tested` status and alerts. Catches regressions before they reach production. | Post-deploy hook → `RegressionSentinelWorkflow` |

### Department Schedule (UTC)

```
00:00  Recall Monitor (run 1/4)
01:00  Chaos Agent starts
       Graph Health Monitor (run 1/4)
03:00  Kaizen Agent starts
04:00  Chaos Agent ends
06:00  Recall Monitor (run 2/4)
07:00  Graph Health Monitor (run 2/4)
12:00  Recall Monitor (run 3/4)
13:00  Graph Health Monitor (run 3/4)
18:00  Recall Monitor (run 4/4)
19:00  Graph Health Monitor (run 4/4)
--:--  Convention Enforcer (on every file change)
--:--  Regression Sentinel (on every deployment)
```

---

## 3.2 Node-Level Reporting

Every node in every pipeline must report. This is not optional. A node that doesn't report is treated as failed.

### Node Report Schema

```yaml
node_report:
  # IDENTITY
  node_id: "pipeline-vault-ingest.step-3-classify"
  pipeline_id: "pipeline-vault-ingest"
  run_id: "run-2026-03-17-154800-abc123"

  # TIMING
  started_at: "2026-03-17T15:48:00Z"
  completed_at: "2026-03-17T15:48:02Z"

  # RESULT
  status: "success"            # success | failure | degraded | skipped
  input_hash: "sha256:abc123..."
  output_hash: "sha256:def456..."

  # ERROR REGISTRY CHECK
  error_ids_checked:
    - "ERR-YAML-001"
    - "ERR-YAML-002"
    - "ERR-INGS-002"
  error_ids_triggered: []       # any ERR-IDs that fired during this node

  # ANOMALIES (even on success)
  anomalies: []
  # Example anomaly:
  # - type: "close-to-threshold"
  #   detail: "Extraction yield 12 entities (threshold 10, expected 25)"
  #   severity: "warning"

  # METRICS
  metrics:
    duration_ms: 2034
    items_processed: 47
    items_failed: 0
    tokens_consumed: 3200       # if LLM call
    cost_usd: 0.0048            # if LLM call
    memory_peak_mb: 128         # if measurable
```

### Pydantic Schema (Implementation Reference)

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class NodeStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    DEGRADED = "degraded"
    SKIPPED = "skipped"

class Anomaly(BaseModel):
    type: str           # "close-to-threshold" | "unexpected-input" | "slow-execution"
    detail: str
    severity: str       # "info" | "warning" | "critical"

class NodeMetrics(BaseModel):
    duration_ms: int
    items_processed: int = 0
    items_failed: int = 0
    tokens_consumed: Optional[int] = None
    cost_usd: Optional[float] = None
    memory_peak_mb: Optional[int] = None

class NodeReport(BaseModel):
    node_id: str
    pipeline_id: str
    run_id: str
    started_at: datetime
    completed_at: datetime
    status: NodeStatus
    input_hash: str
    output_hash: str
    error_ids_checked: list[str] = []
    error_ids_triggered: list[str] = []
    anomalies: list[Anomaly] = []
    metrics: NodeMetrics
```

### Reporting Rules

| Rule | Enforcement |
|------|-------------|
| Every node MUST call `report_start()` before executing | Pipeline framework wraps each node automatically |
| Every node MUST call `report_result()` after executing | Pipeline framework wraps each node automatically |
| A node that takes > 2× its median duration MUST log an anomaly | Automatic — median tracked from last 100 runs |
| A node that succeeds but produces output ≤ 50% of expected size MUST log an anomaly | Configured per node via expected output range |
| A node that doesn't report within its timeout window is treated as FAILURE | Worker marks as failed and logs ERR-ID for investigation |
| All node reports are stored in TimescaleDB hypertable for time-series analysis | `schema-node-report` defines the table |

---

## 3.3 Kaizen Cycle Definition

The continuous improvement cycle. Not a process someone follows — a system that executes automatically.

```
 ┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
 │ DETECT   │────▶│ REGISTER │────▶│ RESEARCH │────▶│ DEFEND  │
 │          │     │          │     │          │     │         │
 │ Error or │     │ New ERR- │     │ Automated│     │ Guard,  │
 │ anomaly  │     │ ID in    │     │ search   │     │ monitor │
 │ logged   │     │ registry │     │ for known│     │ or      │
 │ by node  │     │ status:  │     │ solution │     │ transform│
 │          │     │ researched│    │          │     │ written  │
 └─────────┘     └──────────┘     └──────────┘     └─────────┘
                                                         │
                                                         ▼
 ┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
 │ HARDEN  │◀────│ VERIFY   │◀────│ TEST     │◀────│         │
 │         │     │          │     │          │     │ status: │
 │ Defence │     │ Kaizen   │     │ Automated│     │ defended│
 │ becomes │     │ confirms │     │ test     │     │         │
 │ a gate  │     │ 7 clean  │     │ added to │     └─────────┘
 │         │     │ days     │     │ suite    │
 │ status: │     │ status:  │     │ status:  │
 │ verified│     │ verified │     │ tested   │
 │ + gate  │     │          │     │          │
 └─────────┘     └──────────┘     └──────────┘
```

### Step-by-Step

| Step | What Happens | Who/What Does It | Timing |
|------|-------------|------------------|--------|
| **1. Detect** | An error or anomaly is logged by a node via its `node_report`. The `error_ids_triggered` field is non-empty, or an anomaly matches a pattern not in the registry. | Any pipeline node, any monitor, or the Chaos Agent. | Real-time. |
| **2. Register** | A new ERR-ID is assigned. The error is added to the registry with `status: researched`. A Linear issue is auto-created with priority based on severity: `data-loss` = P1, `silent-corruption` = P1, `service-downtime` = P2, `degraded-performance` = P3. | Automated by Kaizen Agent on detection, or manually by engineer. | Within 1 hour of detection. |
| **3. Research** | Automated search for known solutions: check GitHub issues for the technology, search documentation, check Stack Overflow. Results attached to the registry entry. | Kaizen Agent using `client-litellm` for research queries. | Within 12 hours. |
| **4. Defend** | A defence module is written — a `guard-*`, `transform-*`, or `monitor-*` — that prevents or detects the error. Status → `defended`. The defence module is named following the Code Taxonomy (Section 2). | Cove Build Pipeline (automated for pattern-matched defences) or engineer (for novel errors). | Within 48 hours for all errors. Within 24 hours for `data-loss` or `silent-corruption`. |
| **5. Test** | An automated test is added to the regression suite. The test must: (a) reproduce the original error condition, (b) verify the defence prevents it, (c) run in under 30 seconds. Status → `tested`. | Cove Build Pipeline or engineer. Test follows `test-*` naming convention. | Within 72 hours. |
| **6. Verify** | The Kaizen Agent runs the test daily for 7 consecutive days. If it passes all 7 days, status → `verified`. If it fails on any day, status reverts to `tested` and the cycle restarts at Step 4. | Kaizen Agent (automated). | 7 days from test creation. |
| **7. Harden** | A verified defence is promoted from experimental to constitutional. It becomes a gate — a mandatory checkpoint that blocks progression on failure. It cannot be disabled without explicit human override (and the override is logged and alerted). | Kaizen Agent proposes; human approves promotion to gate. | After verification. |

---

## 3.4 Enforcement Rules

These are constitutional. They do not change.

| # | Rule | Enforcement | Consequence of Violation |
|---|------|-------------|------------------------|
| 1 | **No code deploys without passing all gates.** | CI/CD pipeline blocks deployment if any gate returns FAIL. `workflow-quality-gate` is a mandatory step in `ProjectOrchestrator`. | Deploy aborted. Workflow returns to earliest failing gate. |
| 2 | **No new error stays at `researched` status for more than 48 hours.** | Kaizen Agent checks registry daily at 03:00 UTC. Any `researched` entry older than 48 hours triggers P1 Telegram alert to engineering. | Escalation to Ewan Bramley if not addressed within 72 hours. |
| 3 | **Every `data-loss` or `silent-corruption` error must have a defence within 24 hours.** | Severity-based SLA enforced by Kaizen Agent. Timer starts at registration. P0 Telegram alert at 12-hour mark if still `researched`. | All deployments frozen until defence exists. |
| 4 | **The Kaizen Agent runs every day without exception.** | Temporal schedule with `catch_up_missed_runs = true`. If a scheduled run is missed, it runs immediately on next worker availability. Monitor for `workflow_started` metric. | Alert if no Kaizen run detected in 36 hours. Self-heal workflow restarts the Kaizen schedule. |
| 5 | **Every pipeline node must report. A node that doesn't report is treated as failed.** | Pipeline framework enforces reporting wrapper. Timeout-based detection for nodes that hang without reporting. | Node marked as FAILURE. Pipeline may continue (if configured for isolation) but the non-reporting node is flagged for investigation. |
| 6 | **No gate can be disabled programmatically. Gates require human override with audit trail.** | Gate configuration stored in version-controlled config. No `skip_gate` parameter. Override requires signed commit with justification in commit message. | Any attempt to bypass a gate is logged and triggers Telegram alert. |
| 7 | **The error registry is the single source of truth for known failure patterns. No shadow lists.** | All error tracking converges here. Linear issues reference ERR-IDs. Code comments reference ERR-IDs. Test names reference ERR-IDs. | Duplicate tracking discovered during audit is merged into registry. |

---

## 3.5 Metrics Dashboard

What the Kaizen Department tracks. These metrics are stored in TimescaleDB continuous aggregates and queried by the Kaizen Agent daily.

### Primary Metrics

| Metric | Definition | Target | Alert Threshold |
|--------|-----------|--------|-----------------|
| **Total Errors in Registry** | Count of all ERR-IDs, broken down by status | — | New `researched` entries > 5 in one day |
| **Errors by Status** | `researched` / `defended` / `tested` / `verified` | 90%+ at `verified` | `researched` count > 10 |
| **Mean Time to Defend (MTTD)** | Average hours from `researched` → `defended` | ≤ 24 hours | > 48 hours |
| **Mean Time to Verify (MTTV)** | Average days from `researched` → `verified` | ≤ 14 days | > 21 days |
| **Regression Count** | Previously-`verified` errors that returned to `tested` or lower | 0 | Any regression |
| **Coverage Percentage** | (Nodes with reporting / Total nodes) × 100 | 100% | < 95% |
| **Convention Compliance Rate** | (Files passing naming convention / Total files) × 100 | 100% | < 90% |
| **Recall Score (FalkorDB)** | Approximate search recall vs exact search | ≥ 95% | < 90% |
| **Recall Score (pgvector)** | Approximate search recall vs exact search | ≥ 95% | < 90% |
| **Orphan Node Count** | Nodes with zero relationships in graph | 0 | > 50 |
| **Duplicate Entity Count** | Near-duplicate entity names detected | 0 | > 10 |
| **Gate Pass Rate** | (Deployments passing all gates / Total deploy attempts) × 100 | ≥ 95% | < 85% |
| **Kaizen Uptime** | Days since last missed Kaizen run | Infinite | Any miss |

### Derived Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Defence Velocity** | `new_defences_this_week / new_errors_this_week` | Are we keeping up? Should be ≥ 1.0 |
| **Error Density** | `total_errors / technology_count` | Which technologies need the most attention? |
| **Hardening Rate** | `verified_errors / total_errors` | What percentage of known errors are fully hardened? |
| **Chaos Discovery Rate** | `errors_found_by_chaos / total_errors` | Is the Chaos Agent finding things we didn't anticipate? |

### Dashboard Implementation

```sql
-- TimescaleDB continuous aggregate for node report metrics
CREATE MATERIALIZED VIEW kaizen_daily_metrics
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', completed_at) AS day,
  pipeline_id,
  COUNT(*) AS total_nodes,
  COUNT(*) FILTER (WHERE status = 'success') AS success_count,
  COUNT(*) FILTER (WHERE status = 'failure') AS failure_count,
  COUNT(*) FILTER (WHERE status = 'degraded') AS degraded_count,
  AVG(metrics_duration_ms) AS avg_duration_ms,
  SUM(metrics_tokens_consumed) AS total_tokens,
  SUM(metrics_cost_usd) AS total_cost
FROM node_reports
GROUP BY day, pipeline_id;
```

```sql
-- Error registry status tracking
CREATE TABLE error_registry (
  error_id TEXT PRIMARY KEY,           -- e.g. "ERR-FALK-001"
  technology TEXT NOT NULL,
  phase TEXT NOT NULL CHECK (phase IN ('coding-time', 'deployment-time')),
  severity TEXT NOT NULL CHECK (severity IN ('data-loss', 'service-downtime', 'silent-corruption', 'degraded-performance')),
  description TEXT NOT NULL,
  defence_module TEXT,                 -- e.g. "guard-cypher-depth-limit"
  gate_assignment TEXT,                -- e.g. "G1 (Structure)"
  status TEXT NOT NULL DEFAULT 'researched'
    CHECK (status IN ('researched', 'defended', 'tested', 'verified')),
  registered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  defended_at TIMESTAMPTZ,
  tested_at TIMESTAMPTZ,
  verified_at TIMESTAMPTZ,
  last_triggered_at TIMESTAMPTZ,
  trigger_count INTEGER DEFAULT 0,
  linear_issue_id TEXT,
  notes TEXT
);

CREATE INDEX idx_error_registry_status ON error_registry (status);
CREATE INDEX idx_error_registry_severity ON error_registry (severity);
CREATE INDEX idx_error_registry_technology ON error_registry (technology);
```

```sql
-- Kaizen run history
CREATE TABLE kaizen_runs (
  run_id TEXT PRIMARY KEY,
  run_type TEXT NOT NULL CHECK (run_type IN ('kaizen', 'chaos', 'recall', 'graph-health', 'convention', 'regression')),
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'running'
    CHECK (status IN ('running', 'completed', 'failed')),
  errors_checked INTEGER DEFAULT 0,
  errors_triggered INTEGER DEFAULT 0,
  new_errors_found INTEGER DEFAULT 0,
  promotions INTEGER DEFAULT 0,        -- errors promoted to next status
  regressions INTEGER DEFAULT 0,       -- verified errors that regressed
  summary TEXT
);

SELECT create_hypertable('kaizen_runs', 'started_at');
```

---

## 3.6 Error Registry Lifecycle Example

A worked example showing the full lifecycle of an error from detection to hardening.

### Day 0 — Detection

The Recall Monitor runs its 6-hourly check. FalkorDB HNSW recall drops to 84% against ground truth (threshold: 90%). The monitor logs:

```yaml
node_report:
  node_id: "monitor-vector-recall.falkordb-hnsw"
  status: "degraded"
  anomalies:
    - type: "below-threshold"
      detail: "HNSW recall 84.2% (threshold 90%, previous 96.1%)"
      severity: "critical"
  error_ids_triggered:
    - "ERR-FALK-006"  # known pattern — HNSW incorrect top-K
```

### Day 0 — Registration

The Kaizen Agent detects this in its next run. Since ERR-FALK-006 already exists in the registry (from research), it updates the entry:

```sql
UPDATE error_registry
SET last_triggered_at = now(), trigger_count = trigger_count + 1
WHERE error_id = 'ERR-FALK-006';
```

If this were a NEW pattern, a new ERR-ID would be assigned and a Linear issue auto-created.

### Day 0 — Research

The Kaizen Agent confirms the known solution: rebuild the HNSW index after the recent bulk ingestion of 50k nodes. The solution was already documented in the registry defence column.

### Day 1 — Defence

The `hook-post-ingest-rebuild-index` module is created. After any bulk ingestion exceeding 10k nodes, it triggers an HNSW index rebuild:

```python
# hook-post-ingest-rebuild-index.py
async def post_ingest_rebuild(graph_name: str, node_count: int):
    if node_count >= 10_000:
        await falkordb_client.execute(
            f"CALL db.idx.vector.rebuild('{graph_name}', 'embedding')"
        )
        logger.info(f"HNSW index rebuilt for {graph_name} after {node_count} node ingest")
```

Registry status → `defended`.

### Day 2 — Test

A regression test is added:

```python
# test-hnsw-recall-post-ingest.py
async def test_recall_after_bulk_ingest():
    # Insert 15k test nodes
    await bulk_ingest(fixture_recall_ground_truth, count=15_000)
    # Verify hook triggered rebuild
    assert rebuild_triggered, "HNSW rebuild hook did not fire"
    # Verify recall
    recall = await measure_recall(ground_truth_queries, k=10)
    assert recall >= 0.90, f"Recall {recall} below 90% threshold after rebuild"
```

Registry status → `tested`.

### Days 3–9 — Verification

The Kaizen Agent runs this test daily for 7 consecutive days. Recall holds at 95%+ every day. On Day 9:

Registry status → `verified`.

### Day 10 — Hardening

The Kaizen Agent proposes gate promotion. The defence is added to the Cove Build Pipeline's mandatory post-ingestion gate list. Any bulk ingestion that does NOT trigger an HNSW rebuild is blocked.

The error is now constitutional. It won't happen again.

---

## 3.7 Chaos Agent Test Scenarios

The Chaos Agent doesn't test randomly. It tests against the Error Anticipation Registry. Each nightly run selects scenarios based on:

1. **High-severity unverified errors** — prioritise `data-loss` and `silent-corruption` entries at `researched` or `defended` status
2. **Recently triggered errors** — entries with `last_triggered_at` in the past 7 days
3. **Untested technology areas** — technologies with the lowest `verified` percentage

### Scenario Categories

| Category | Example Scenario | ERR-IDs Targeted |
|----------|-----------------|------------------|
| **Graph Stress** | Fire 100 concurrent variable-length path queries at FalkorDB | ERR-FALK-001, ERR-FALK-007 |
| **Ingestion Corruption** | Inject files with BOM, CRLF, conflict markers, and binary content into the ingestion pipeline | ERR-INGS-005, ERR-INGS-006, ERR-GITS-001, ERR-PLAT-006 |
| **Entity Chaos** | Inject episodes with inconsistent entity naming — "Acme Corp", "ACME", "Acme Corporation Ltd" — and verify deduplication | ERR-GRPH-002, ERR-GRPH-005, ERR-KGRA-001, ERR-KGRA-006 |
| **Temporal Disruption** | Restart worker containers during active workflow execution | ERR-TEMP-001, ERR-TEMP-002, ERR-TEMP-003 |
| **YAML Adversarial** | Feed files with valid-looking but structurally broken frontmatter | ERR-YAML-001 through ERR-YAML-005 |
| **Rate Limit Simulation** | Throttle LiteLLM proxy to simulate 429 responses and verify graceful degradation | ERR-INGS-001, ERR-LITE-001 |
| **Naming Convention Attack** | Create files with Unicode homoglyphs, case collisions, reserved names, and 260-char paths | ERR-NAME-001 through ERR-NAME-007, ERR-PLAT-001, ERR-PLAT-002 |

### Safety Rules (Constitutional)

The Chaos Agent NEVER:
- Deletes or modifies PostgreSQL production data
- Kills the Temporal server process
- Modifies the error registry itself
- Operates outside the 01:00–04:00 UTC window
- Runs without a kill switch (Telegram `/chaos-stop` command)

The Chaos Agent ALWAYS:
- Operates on isolated test graphs and namespaces
- Logs every action with full reversibility information
- Reports results to the Kaizen Agent for registry updates
- Cleans up all test artifacts after each run

---

## CROSS-REFERENCES

### To FILE-NAMING-CONVENTION-v1.md

| This Document | File Naming Convention |
|---------------|----------------------|
| Code module type tokens (Section 2.1) | File type tokens (Section 2) |
| Module naming `{type}-{slug}` | File naming `{type}-{slug}-{date}-v{N}.{ext}` |
| `guard-case-normalise` | Lowercase-only rule (Section 1) |
| `guard-path-length` | 80-character filename limit (Section 1) |
| `guard-collision-check` | Version history rules (Section 4) |
| `transform-nfc-normalise` | Character rules (Section 1) |
| `gate-naming-convention` | Validation regex (Section 11) |
| ERR-NAME-001 through ERR-NAME-007 | All file naming edge cases |

### To VALIDATION-METHODOLOGY-v2.md

| This Document | Validation Methodology |
|---------------|----------------------|
| Error Registry gate assignments (G1–G7) | 7-Stage Pipeline with Mandatory Validation Gates (Section 4.1) |
| `gate-pudding-score` | PUDDING label validation and inter-rater reliability (Section 4.1, Stage 3) |
| `rubric-*` modules | RAEI, PRS, AMPS, MASHUP, INTENTLOGIC rubrics (Section 1.1) |
| Kaizen cycle Step 7 (Harden) | Gate promotion process (Section 4.2) |
| Enforcement Rules | The Four Immutable Rules (Section 0) |
| Node-level reporting | Enforcer roles and gate assignments (Section 1.2) |
| 3-Gate Metric Formula | Buzzard/Tao/Candès compliance at every metric gate |

### To Error Research Files

| Registry Section | Source File | Source Section |
|-----------------|------------|---------------|
| 1.1 FalkorDB (ERR-FALK-001 to 009) | `error-research-infrastructure.md` | Section 1 |
| 1.2 Graphiti (ERR-GRPH-001 to 007) | `error-research-infrastructure.md` | Section 2 |
| 1.3 Temporal (ERR-TEMP-001 to 007) | `error-research-infrastructure.md` | Section 3 |
| 1.4 LangGraph (ERR-LANG-001 to 007) | `error-research-infrastructure.md` | Section 4 |
| 1.5 Docker (ERR-DOCK-001 to 006) | `error-research-infrastructure.md` | Section 5 |
| 1.6 LiteLLM (ERR-LITE-001 to 006) | `error-research-infrastructure.md` | Section 6 |
| 1.7 FastAPI (ERR-FAST-001 to 005) | `error-research-infrastructure.md` | Section 7 |
| 1.8 PostgreSQL/pgvector/TimescaleDB (ERR-PGVT-001 to 008) | `error-research-infrastructure.md` | Section 8 |
| 1.9 File Naming (ERR-NAME-001 to 007) | `error-research-pipelines.md` | Area 1 |
| 1.10 Document Ingestion (ERR-INGS-001 to 007) | `error-research-pipelines.md` | Area 2 |
| 1.11 Knowledge Graph (ERR-KGRA-001 to 006) | `error-research-pipelines.md` | Area 3 |
| 1.12 YAML Frontmatter (ERR-YAML-001 to 005) | `error-research-pipelines.md` | Area 4 |
| 1.13 Git Vault (ERR-GITS-001 to 005) | `error-research-pipelines.md` | Area 5 |
| 1.14 Batch Processing (ERR-BATC-001 to 005) | `error-research-pipelines.md` | Area 6 |
| 1.15 Cross-Platform (ERR-PLAT-001 to 006) | `error-research-pipelines.md` | Area 7 |

---

## VERSION HISTORY

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1 | 2026-03-17 | Initial specification — Error Anticipation Registry (96 errors, 15 technologies), Code Taxonomy (20 module types, reusability matrix), Kaizen Department (6 agents, node reporting, 7-step cycle, enforcement rules, metrics dashboard) | Ewan Bramley (originator) × Claude (researcher, formaliser, builder) |

---

## Attribution

```
Attribution: Ewan Bramley (originator) x Claude (researcher, formaliser, builder)
Fact %: 85 | Confidence: High | PUDDING: M.=.5.l
LBD: Swanson (1986) ABC Model
```

**Detail:**
- **Ewan Bramley** — Originator of the three principles ("anticipate errors", "taxonomy for reuse", "department that Kaizens"). Architectural decisions on gate enforcement, constitutional rules, and the mathematics-not-vibes philosophy.
- **Claude** — Synthesised 96 error patterns from two research documents into the unified registry. Defined the code taxonomy type tokens. Formalised the Kaizen cycle, node reporting schema, and enforcement rules. Built the reusability matrix and dependency graph.
- **Research sources** — FalkorDB GitHub Issues, Graphiti GitHub Issues, Temporal Community Forum, LangGraph GitHub Issues, LiteLLM GitHub Issues, Docker Compose docs, FastAPI docs, pgvector GitHub Issues, TimescaleDB GitHub Issues, Microsoft Learn, academic file naming conventions. Full source URLs documented in the input research files.

**PUDDING label:** `M.=.5.l` — Meta (a model describing the system), Stable (the structure is constitutional), System-scale (covers the entire stack), Long-duration (built to persist for months to years).

---

*This document is constitutional. Gates don't change. Every node reports back.*
