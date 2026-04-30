---
title: "Error Research Infrastructure"
id: "error-research-infrastructure"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "error-research-infrastructure.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners Infrastructure Error Research
**Generated:** 2026-03-17  
**Scope:** Common bugs, known issues, proven workarounds, and risk classification for the core Amplified Partners technology stack.

---

## How to Read This Document

Each issue entry includes:
- **Type:** `coding-time` (preventable in code/config) or `deployment-time` (requires runtime monitoring)
- **Severity:** `data-loss` | `service-downtime` | `silent-corruption` | `degraded-performance`
- **Source:** Linked to GitHub issues, official docs, or community forums

---

## 1. FalkorDB

> Graph database built on GraphBLAS sparse-matrix engine. Uses Redis as the host process. Supports OpenCypher with extensions, native HNSW vector search, and property-graph schema.

### Issue 1.1 — Variable-Length Path Queries Cause OOM Crash (DoS)
- **Description:** Executing unbounded variable-length path queries (`-[*]->`) on densely connected graphs exhausts memory and triggers a fatal abort in the Redis/FalkorDB process rather than returning a clean error. The server crashes entirely.
- **Solution/Workaround:** Always bound variable-length traversals: `MATCH (a)-[*1..5]->(b)`. Avoid `[*]` without depth limits on any graph with more than ~10k edges. Set `ulimit` on the host process. Monitor memory with `GRAPH.MEMORY USAGE`.
- **Type:** `coding-time` — enforced in query design
- **Severity:** `service-downtime` (process crash kills all graphs)
- **Source:** [FalkorDB GitHub Issue #1580](https://github.com/FalkorDB/FalkorDB/issues/1580)

---

### Issue 1.2 — `collect()` and Aggregate Functions Fail in Multi-WITH Queries
- **Description:** Complex Cypher queries using `collect()` or `count()` inside map projections across multiple `WITH` clauses fail with `_AR_EXP_UpdateEntityIdx: Unable to locate a value with alias X within the record`. Values don't survive through multiple `WITH` passes when aggregated in nested projections.
- **Solution/Workaround:** Break complex projections into simpler `WITH` steps. Avoid placing `collect()` or `count()` inside map literals (`{ key: collect(x) }`). Flatten aggregations to top-level `WITH` clauses before projecting.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (query returns error, breaking dependent read paths)
- **Source:** [FalkorDB GitHub Issue #946](https://github.com/FalkorDB/FalkorDB/issues/946)

---

### Issue 1.3 — LIMIT Clause Does Not Constrain Eager Write Operations
- **Description:** `LIMIT` applied in a `WITH` or `RETURN` clause does not restrict `CREATE`, `SET`, `DELETE`, `MERGE`, or aggregate projections that precede it. A query like `UNWIND range(1,3) AS x CREATE (n {v:x}) RETURN n LIMIT 1` creates 3 nodes but returns 1.
- **Solution/Workaround:** Apply `LIMIT` before write operations using an explicit `WITH ... LIMIT N` before the `CREATE`/`MERGE`. Never rely on post-write `LIMIT` to prevent over-creation.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (extra unintended nodes/edges written to graph)
- **Source:** [FalkorDB Known Limitations Docs](https://docs.falkordb.com/cypher/known-limitations.html)

---

### Issue 1.4 — Index Does Not Support Not-Equal (`<>`) Filters
- **Description:** When a `WHERE` clause uses `<>` on an indexed property, FalkorDB's query planner does not use the index — it falls back to a full scan. The `GRAPH.EXPLAIN` output will show `Node By Label Scan` instead of `Index Scan`.
- **Solution/Workaround:** Rewrite `<>` filters using `NOT (n.prop = value)` or split into a range filter. Validate query plans with `GRAPH.EXPLAIN` before deploying any query that is performance-sensitive.
- **Type:** `coding-time`
- **Severity:** `degraded-performance`
- **Source:** [FalkorDB Known Limitations Docs](https://docs.falkordb.com/cypher/known-limitations.html)

---

### Issue 1.5 — Relationship Uniqueness: Non-Referenced Relations Counted Once
- **Description:** When a relationship pattern is not referenced by an alias elsewhere in the query, FalkorDB verifies only that *at least one* matching relationship exists rather than operating over all matching relationships. `MATCH (a)-[e]->(b) RETURN COUNT(b)` with 2 relationships between a→b returns 1, not 2.
- **Solution/Workaround:** Force the alias to be referenced: add `WHERE ID(e) >= 0` or include `e.dummyval` in the RETURN. Always alias relationships when counting or collecting them.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (query returns incorrect counts silently)
- **Source:** [FalkorDB Known Limitations Docs](https://docs.falkordb.com/cypher/known-limitations.html)

---

### Issue 1.6 — HNSW Vector Index Returns Incorrect Top-K Results
- **Description:** Top-K vector similarity searches (`db.idx.vector.queryNodes`) with fetch_k values near certain thresholds return nodes with very poor similarity scores while the genuinely best matches are skipped. The issue appears on graphs with 100k+ nodes and is sensitive to the exact value of `fetch_k`.
- **Solution/Workaround:** Use a `fetch_k` value that is meaningfully larger than the desired K (e.g., `fetch_k = k * 3` minimum). Periodically rebuild the vector index if recall degrades. Test recall against ground-truth sets after bulk ingestion.
- **Type:** `deployment-time`
- **Severity:** `silent-corruption` (wrong results returned without error)
- **Source:** [FalkorDB GitHub Issue #716](https://github.com/FalkorDB/FalkorDB/issues/716)

---

### Issue 1.7 — FalkorDB Hangs Under Heavy Write Load
- **Description:** Long-running write queries do not yield control back to the Redis event loop. Under concurrent heavy write load, the Redis process can appear to hang — connections are accepted but not processed — until the write query completes.
- **Solution/Workaround:** Break large batch writes into smaller transactions. Avoid large single-query bulk imports. Set Redis `timeout` to detect stalled clients. Monitor with `CLIENT LIST` for stuck connections. Feature request open to yield control mid-write.
- **Type:** `deployment-time`
- **Severity:** `service-downtime`
- **Source:** [FalkorDB GitHub Issue #1056](https://github.com/FalkorDB/FalkorDB/issues/1056), [Feature Request #1181](https://github.com/FalkorDB/FalkorDB/issues/1181)

---

### Issue 1.8 — Delta Matrix Slow After Transaction Rollback
- **Description:** When a transaction is rolled back, the delta matrix (used to track pending graph changes) takes an abnormally long time to drain/clean up, causing subsequent write queries to run slowly until the state is fully reconciled.
- **Solution/Workaround:** Minimise transaction rollbacks in hot paths. If using error-handling patterns that may rollback frequently, prefer smaller atomic operations. Monitor with `GRAPH.PROFILE`.
- **Type:** `deployment-time`
- **Severity:** `degraded-performance`
- **Source:** [FalkorDB GitHub Issue #1062](https://github.com/FalkorDB/FalkorDB/issues/1062)

---

### Issue 1.9 — String Memory Bloat From Repeated Attribute Values
- **Description:** Without string interning, each repeated string value (e.g., `"status": "active"` across millions of nodes) is stored as a separate allocation. On large graphs, this can inflate heap usage by 30–60% compared to interned graphs.
- **Solution/Workaround:** Use `SET n.property = intern(n.property)` during bulk ingestion for high-cardinality-repeated fields. Available as of FalkorDB v4.10. Run `GRAPH.MEMORY USAGE` before and after to quantify impact. Batch interning in chunks of 10k–50k nodes.
- **Type:** `coding-time`
- **Severity:** `degraded-performance` (can escalate to OOM if left unchecked on large graphs)
- **Source:** [FalkorDB String Interning Blog](https://www.falkordb.com/blog/string-interning-graph-database/)

---

## 2. Graphiti by Zep

> Temporal knowledge graph framework built on FalkorDB (or Neo4j). Handles episodic memory ingestion, bi-temporal edge management, entity extraction via LLM, and entity resolution/deduplication.

### Issue 2.1 — `add_triplet()` Does Not Persist Edge UUIDs on FalkorDB
- **Description:** When using the FalkorDB provider, `graphiti.add_triplet()` creates edge relationships but stores `source_node_uuid` and `target_node_uuid` as `None` instead of actual node UUIDs. This silently breaks edge deduplication and UUID-based filtering for all subsequently written triplets.
- **Root Cause:** The FalkorDB `SET` statement in `get_entity_edge_save_bulk_query()` explicitly lists properties but omits `source_node_uuid` and `target_node_uuid`. Also uses `MATCH` (fails if nodes absent) instead of `MERGE`.
- **Solution/Workaround:** Patch `graphiti_core/models/edges/edge_db_queries.py`: change `MATCH` to `MERGE`, and add the UUID fields to the FalkorDB `SET` clause. No official fix as of writing.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` + `data-loss` (UUID-based lookups return nothing; deduplication fails permanently)
- **Source:** [Graphiti GitHub Issue #1001](https://github.com/getzep/graphiti/issues/1001)

---

### Issue 2.2 — Duplicate Entity Creation on Custom Database Names (FalkorDB/Neo4j)
- **Description:** Graphiti fails to deduplicate entities against the existing graph when using a non-default database name. New episodes create duplicate `Person`, `Organization`, etc. nodes rather than merging with existing ones. Consistent across multiple LLM backends.
- **Root Cause:** Database-name routing bug; deduplication queries target the wrong namespace when a custom DB name is specified.
- **Solution/Workaround:** Use the default database name (`neo4j` for Neo4j provider). For FalkorDB, avoid custom graph naming in multi-tenant setups until patched. Test deduplication explicitly after any schema/config change.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (graph grows with duplicate nodes; retrieval quality degrades silently)
- **Source:** [Graphiti GitHub Issue #875](https://github.com/getzep/graphiti/issues/875), [Issue #963](https://github.com/getzep/graphiti/issues/963)

---

### Issue 2.3 — Basic FalkorDB Quickstart Fails with `GroupIdValidationError`
- **Description:** The default `group_id` generated for FalkorDB by `get_default_group_id()` is `'\\_'` (escaped underscore), which fails the `validate_group_id()` regex `r'^[a-zA-Z0-9_-]+$'` — making Graphiti completely unusable on FalkorDB without patching.
- **Root Cause:** Escaped underscore (`\\_`) introduced in commit `d725fcd` is incorrectly treated as invalid by the validator.
- **Solution/Workaround:** Patch `helpers.py` to return a valid `group_id` (e.g., `'default'` or `'falkordb'`) for `GraphProvider.FALKORDB`. Alternatively, pass an explicit `group_id` in all `add_episode()` calls.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (Graphiti completely non-functional on FalkorDB without this fix)
- **Source:** [Graphiti GitHub Issue #1319](https://github.com/getzep/graphiti/issues/1319)

---

### Issue 2.4 — Custom Edge Types Not Visible / Not Saved with FalkorDB
- **Description:** Custom edge types defined by the user do not appear in graph visualisations (FalkorDB Browser) and may not persist correctly when using the FalkorDB provider. Neo4j provider works correctly for the same payload.
- **Solution/Workaround:** Verify all custom edge properties are explicitly mapped in the FalkorDB Cypher `SET` clauses. Test edge roundtrip (write + read back) after every schema extension. Use the Neo4j provider as a reference implementation for validation.
- **Type:** `coding-time`
- **Severity:** `silent-corruption`
- **Source:** [Graphiti GitHub Issue #903](https://github.com/getzep/graphiti/issues/903)

---

### Issue 2.5 — Entity Resolution Accuracy Degrades with Poor LLM Extraction
- **Description:** Graphiti relies on LLM calls to extract entities and determine equivalence. If the LLM produces inconsistently named entities (e.g., "Acme Corp" vs "Acme Corporation"), the deduplication step fails to merge them and the graph accumulates fragmented representations of the same real-world entity.
- **Solution/Workaround:** Use consistent entity naming in prompt templates. Supply canonical entity examples in the system prompt. Implement post-ingestion entity audits querying for near-duplicate node names. Consider using a normalisation step (lowercasing, company suffix stripping) before ingestion.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (silently growing graph with inconsistent entities degrades retrieval)
- **Source:** [Graphiti GitHub README](https://github.com/getzep/graphiti), [FalkorDB Graphiti Architecture Blog](https://www.falkordb.com/blog/building-temporal-knowledge-graphs-graphiti/)

---

### Issue 2.6 — Temporal Edge Invalidation Not Triggered for Contradictory Facts
- **Description:** When a new episode contains a fact that contradicts an existing edge (e.g., "Alice now works at Acme" when graph has "Alice works at Beta"), temporal invalidation of the old edge depends on the LLM correctly identifying the contradiction. Hallucinated or missed comparisons leave stale edges as valid, giving agents incorrect temporal context.
- **Solution/Workaround:** Implement explicit post-episode validation: query for edges involving modified entities and compare `valid_at`/`invalid_at` timestamps. Use point-in-time queries (`as_of` parameter) to audit state consistency.
- **Type:** `deployment-time`
- **Severity:** `silent-corruption` (agents receive stale, contradicted facts without error)
- **Source:** [Graphiti GitHub README — Bi-Temporal Model](https://github.com/getzep/graphiti)

---

### Issue 2.7 — LiteLLM/Ollama Non-Standard Port Integration Fails with `APIConnectionError`
- **Description:** When Graphiti is configured to use LiteLLM or Ollama running on a non-default port, persistent `APIConnectionError` exceptions occur during episode ingestion, preventing any graph writes.
- **Solution/Workaround:** Ensure `api_base` in the LLM client config explicitly includes the full URL with port. Validate connectivity from the Graphiti container to LiteLLM before startup. Use Docker Compose health checks to gate Graphiti startup on LiteLLM availability.
- **Type:** `deployment-time`
- **Severity:** `service-downtime`
- **Source:** [Graphiti GitHub Issues](https://github.com/getzep/graphiti/issues)

---

## 3. Temporal.io

> Durable execution / workflow orchestration platform. Runs as a cluster (frontend, history, matching, worker services) with a persistence backend (PostgreSQL). Workers poll task queues and execute workflow/activity code.

### Issue 3.1 — Non-Determinism Errors After Code Changes to Running Workflows
- **Description:** Deploying updated workflow code that changes the order, type, or presence of commands (activities, timers, signals) causes `NonDeterministicError` / `DeterminismViolationError` on any in-flight workflow instance during replay. The workflow stalls silently — it doesn't move to `Failed` state by default, making it invisible in dashboards.
- **Solution/Workaround:** Use `workflow.patching()` / `Workflow.getVersion()` to branch code paths by version. Run `WorkflowReplayer` against a captured history snapshot in CI before every deployment. Configure workers to fail workflows on NDE: `setFailWorkflowExceptionTypes(NonDeterministicException.class)`. Monitor `workflow_task_execution_failed` SDK metric for NDE occurrences.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (in-flight workflows freeze indefinitely)
- **Source:** [Temporal Community — Non-determinism in UI](https://community.temporal.io/t/find-non-determinism-issues-from-the-web-ui/12155), [Bitovi Replay Testing Guide](https://www.bitovi.com/blog/replay-testing-to-avoid-non-determinism-in-temporal-workflows)

---

### Issue 3.2 — Workers Stop Polling / Disappear from Task Queue Over Time
- **Description:** Available task slots on workflow or activity workers drain continuously without a corresponding increase in load. After several hours, all workers become invisible in the Temporal UI (DescribeTaskQueue). Restarting pods restores functionality.
- **Root Cause:** Activity code blocking the event loop (synchronous calls, connection waits, high CPU) causes activity timeouts and retries, which consume all activity task slots. Workflow task slots then become depleted when the activity workers can't accept new tasks.
- **Solution/Workaround:** Separate workflow workers and activity workers onto different task queues. Add heartbeat calls in all long-running activities. Instrument SDK metrics (`activity_task_slots_available`, `workflow_task_slots_available`). Set resource limits on worker pods to expose CPU starvation. Never place synchronous blocking calls in async activity functions.
- **Type:** `deployment-time`
- **Severity:** `service-downtime` (all new workflow executions queue indefinitely)
- **Source:** [Temporal Community — Workers Not Polling #18780](https://community.temporal.io/t/help-workers-not-pooling-for-task-task-queue-are-decreasing-in-workers-until-0/18780)

---

### Issue 3.3 — Sticky Queue Task Timeout After Worker Restart
- **Description:** When a workflow worker restarts (even gracefully), the next workflow task is still routed to the now-dead sticky queue of the terminated worker. The task times out (10 second default `stickyQueueScheduleToStartTimeout`), causing a `Workflow Task Timed Out` event in history before re-routing to the normal queue.
- **Solution/Workaround:** This is partially expected behaviour, not a crash. However, minimise impact by: ensuring replacement workers come up before old ones terminate; using `stickyQueueScheduleToStartTimeout = 0` on batch workers where caching isn't critical; monitoring for repeated task timeouts as a signal of persistent worker instability.
- **Type:** `deployment-time`
- **Severity:** `degraded-performance` (temporary delay, not data loss)
- **Source:** [GitHub SDK-Python Issue #783](https://github.com/temporalio/sdk-python/issues/783), [Temporal Community — Sticky Queue Timeout](https://community.temporal.io/t/handling-workflow-task-timeout-due-to-sticky-queue-task-timeout/16443)

---

### Issue 3.4 — Activity Timeout Misconfiguration Causes Infinite Retry Loops
- **Description:** With default retry policy (`MaxAttempts = 0` = unlimited) and no `ScheduleToClose` timeout set, a persistently failing activity will retry for up to 10 years with exponential backoff. This is not visible as an error — the workflow appears running.
- **Solution/Workaround:** Always set `ScheduleToClose` timeout on activities that call external services. Use `NonRetryableErrorTypes` to mark application-level failures (e.g., invalid input) as non-retryable. Set explicit `MaxAttempts` on activities where bounded retry is required.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (resources consumed indefinitely; downstream services load-hammered)
- **Source:** [Temporal Activity Timeouts Blog](https://temporal.io/blog/activity-timeouts), [Temporal Retry Policy Docs](https://docs.temporal.io/encyclopedia/retry-policies)

---

### Issue 3.5 — Workflow Versioning `getVersion` Removal Causes NDE
- **Description:** Removing a `Workflow.getVersion()` / `workflow.patching()` call prematurely (before all workflows that executed the versioned path have completed) causes a `NonDeterministicError` on replay for those in-flight instances, because the `MarkerRecorded` event in history no longer has matching code.
- **Solution/Workaround:** Query `TemporalChangeVersion="<change_id>-<version>"` visibility to confirm zero running workflows on the old version before removing any `getVersion` call. Use Worker Versioning (Build IDs) as a complementary strategy to route old executions to old workers.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [Temporal Community — getVersion Removal](https://community.temporal.io/t/clarification-on-workflow-getversion-and-when-it-s-safe-to-remove/17961)

---

### Issue 3.6 — PostgreSQL Connection Failures in Self-Hosted Temporal
- **Description:** Self-hosted Temporal clusters report PostgreSQL connection errors (`postgres connection not working`) during periods of high load or after database restarts, causing the Temporal history service to become unavailable.
- **Solution/Workaround:** Configure connection pool settings in Temporal's `config.yaml` (`sql.maxConns`, `sql.maxIdleConns`). Add health checks and restart policies to both the DB and Temporal services. Monitor Temporal's internal metrics for persistence-layer error rates.
- **Type:** `deployment-time`
- **Severity:** `service-downtime`
- **Source:** [Temporal GitHub Issue #8211](https://github.com/temporalio/temporal/issues/8211)

---

### Issue 3.7 — Task Queue Routing Mismatch Causes Workflows to Queue Indefinitely
- **Description:** Workflows scheduled on task queue `X` but workers registered on task queue `Y` cause all workflow executions to sit in `Running` state with no activity. Often introduced by environment variable misconfiguration or copy-paste errors in worker setup.
- **Solution/Workaround:** Add startup assertion checks that verify registered task queue names match deployment config. Use `DescribeTaskQueue` API to confirm worker presence before accepting traffic. Alert on `schedule_to_start_latency` exceeding 30 seconds.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [Temporal Community — Workflows Stuck](https://www.reddit.com/r/Temporal/comments/1ms7jt3/workflows_stuck/), [Temporal Task Routing Docs](https://docs.temporal.io/task-routing)

---

## 4. LangGraph

> Agentic AI orchestration framework built on LangChain. Compiles directed graphs of nodes (LLM calls, tool calls, human-in-the-loop) with persistent checkpoints and stateful resumption.

### Issue 4.1 — Invalid State Saved to Checkpoint Causes Permanent Corruption
- **Description:** LangGraph validates node *input* when preparing the next task, but does not validate node *output* after execution. If a node returns an invalid value (e.g., `None` in a `List[str]` field), the invalid state is checkpointed. Any subsequent `get_state_history()` or resumption call raises a `ValidationError`, permanently corrupting that thread.
- **Solution/Workaround:** Manually validate state within node functions before returning. Use `State(items=new_items)` explicit construction to trigger Pydantic validation at node exit. Use `try/except` around state updates and return safe defaults on error.
- **Type:** `coding-time`
- **Severity:** `data-loss` (thread permanently unusable; historical data inaccessible)
- **Source:** [LangGraph GitHub Issue #6491](https://github.com/langchain-ai/langgraph/issues/6491)

---

### Issue 4.2 — Infinite Agent Loops Until Recursion Limit Error
- **Description:** Multi-agent graphs (e.g., research + analysis loops) can enter silent coordination loops where agents cycle indefinitely without making progress. LangGraph's default recursion limit is 25 steps; once hit, the graph raises `GraphRecursionError` without meaningful context. The loop often consumes significant token budget before detection.
- **Solution/Workaround:** Implement explicit termination conditions in conditional edges. Add a `step_counter` field to state and enforce a hard ceiling. Compute a state hash at each step and terminate if the same hash appears twice. Set `recursion_limit` explicitly per invocation. Use LangSmith to trace node visit patterns. Never use `while True` patterns without a convergence condition.
- **Type:** `coding-time`
- **Severity:** `degraded-performance` (+ cost overrun)
- **Source:** [LangGraph Issue #6731](https://github.com/langchain-ai/langgraph/issues/6731), [Reddit Multi-Agent Loop Analysis](https://www.reddit.com/r/LangChain/comments/1r2mdz1/detecting_infinite_loops_in_langgraph_multiagent/)

---

### Issue 4.3 — Sub-Graph State Updates Not Visible to Parent Graph
- **Description:** When a sub-graph is interrupted mid-execution (`interrupt_before`), updates made by nodes inside the sub-graph are not propagated to the parent graph's state until the sub-graph completes fully. The parent sees stale values.
- **Solution/Workaround:** Read sub-graph state explicitly via `snapshot.tasks` to traverse nested `StateSnapshot` objects. Alternatively, restructure so interrupts happen at the top-level graph, not inside sub-graphs. Move shared state fields to the top-level `StateGraph`.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (parent agent makes decisions on stale state)
- **Source:** [LangChain Forum — State Not Updating](https://forum.langchain.com/t/langraph-state-not-updating/2672), [LangGraph GitHub Issue #4748](https://github.com/langchain-ai/langgraph/issues/4748)

---

### Issue 4.4 — Parent Graph State Lost When Updated During Sub-Graph Interrupt
- **Description:** Updating parent graph state via `update_state()` while a sub-graph is mid-execution (interrupted) causes the sub-graph to restart from the beginning rather than resuming from the interrupt point. The parent's latest update is not reflected in `state.values`.
- **Solution/Workaround:** Avoid calling `update_state()` on a parent graph while any nested sub-graph is in an interrupted state. Complete or cancel the sub-graph execution before modifying parent state.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` + potential `data-loss`
- **Source:** [LangGraph GitHub Issue #4748](https://github.com/langchain-ai/langgraph/issues/4748)

---

### Issue 4.5 — Tool Call Failures Provide No Model Context for Self-Correction
- **Description:** When a tool call fails inside `ToolNode`, the resulting `ToolMessage` contains only the exception text. The model never receives its own output metadata (stop reason, token count, content filter flag), making it impossible for the agent to diagnose *why* its tool call was malformed. Agents typically retry identically, looping on the same error.
- **Solution/Workaround:** Use `handle_tool_errors=True` in `ToolNode` to convert exceptions to messages. Implement custom error routing that appends structured error context. Reference [PR #7139](https://github.com/langchain-ai/langgraph/pull/7139) which adds model metadata to tool error messages.
- **Type:** `coding-time`
- **Severity:** `degraded-performance` (+ infinite tool retry loop risk)
- **Source:** [LangChain Forum — Tool Error Handling](https://forum.langchain.com/t/raising-tool-call-errors-so-agents-can-be-self-healing/3152)

---

### Issue 4.6 — Recursion Limit Config Silently Overridden by Frameworks
- **Description:** Setting `recursion_limit=100` via `.with_config()` is silently overridden back to the default 25 when the graph is invoked through certain wrapper frameworks (e.g., CopilotKit). This causes premature `GraphRecursionError` on legitimate long-running workflows.
- **Solution/Workaround:** Pass `recursion_limit` directly in the invocation config dict: `graph.invoke(input, config={"recursion_limit": 100})`. Do not rely on `.with_config()` when using third-party wrappers. Verify effective limit at invocation time via tracing.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (workflow terminates prematurely)
- **Source:** [LangChain Forum — Recursion Limit Overridden](https://forum.langchain.com/t/i-had-set-recursion-limit-100-but-got-error-recursion-limit-of-25-reached/2569)

---

### Issue 4.7 — PostgreSQL Checkpoint: `thread_id` Too Long
- **Description:** Using `AsyncPostgresSaver` / `PostgresSaver` as a checkpoint backend fails when `thread_id` values exceed the column's varchar limit, raising a database truncation or constraint error.
- **Solution/Workaround:** Normalise `thread_id` to UUIDs (36 chars) rather than using arbitrary strings. Verify the checkpoint schema DDL against your expected ID format. Run `checkpointer.setup()` on first boot to ensure the schema is created.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [LangGraph GitHub Issue #6239](https://github.com/langchain-ai/langgraph/issues/6239)

---

## 5. Docker + Docker Compose

> Multi-container orchestration for 35+ services on a single Hetzner AX162-R bare-metal server. Uses Docker Compose v2 with named networks, bind-mount volumes, and dependency-ordered startup.

### Issue 5.1 — `depends_on` with `condition: service_healthy` Hangs on Startup
- **Description:** A service configured with `depends_on: {db: {condition: service_healthy}}` can hang indefinitely if the health check itself fails silently — e.g., because the health check command is not installed in the container image, or the `start_period` is too short for slow-starting databases. No error is surfaced; the dependent container simply never starts.
- **Solution/Workaround:** Always verify the health check command is available inside the target image (`pg_isready` for PostgreSQL, `redis-cli ping` for Redis). Set generous `start_period` (≥30s for databases). Test health checks in isolation with `docker inspect --format='{{json .State.Health}}'`. Use `restart: on-failure` as a secondary safety net.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [Docker Compose Health Checks Guide](https://last9.io/blog/docker-compose-health-checks/), [Stack Overflow — depends_on healthcheck hang](https://stackoverflow.com/questions/79818922)

---

### Issue 5.2 — DNS Resolution Failures Between Containers on Same Network
- **Description:** Containers on the same Compose-defined network intermittently fail to resolve each other's service names via DNS, producing `Name or service not known` errors. Most common immediately after startup during the brief window before the embedded Docker DNS cache populates, or after container restarts that change IP assignments.
- **Solution/Workaround:** Always use service names (not IPs) for inter-container communication. Implement retry logic with exponential backoff for initial connection attempts. Verify resolution with `docker compose exec <service> nslookup <target>`. For 35+ containers, consider explicit `networks:` assignment to avoid accidental cross-network isolation.
- **Type:** `deployment-time`
- **Severity:** `service-downtime` (intermittent startup failures)
- **Source:** [OneUptime — Debug Docker Compose Network Issues](https://oneuptime.com/blog/post/2026-01-25-debug-docker-compose-network-issues/view)

---

### Issue 5.3 — OOM Kill: No Per-Container Memory Limits Causes Host Instability
- **Description:** Without `mem_limit` / `deploy.resources.limits.memory` set per service, a single container (e.g., FalkorDB during a large query, or LiteLLM under burst load) can consume all available host memory. Linux OOM Killer then terminates processes unpredictably — often killing unrelated containers rather than the offending one.
- **Solution/Workaround:** Set explicit memory limits on all containers. For a 35-container stack on AX162-R (128GB RAM), budget memory per tier. Add `restart: unless-stopped` policies. Monitor host memory pressure via `journalctl -p 4` and `docker stats`. Alert when any container exceeds 80% of its limit.
- **Type:** `deployment-time`
- **Severity:** `service-downtime` (cascading container kills)
- **Source:** [Docker CPU/Memory Limits Guide](https://oneuptime.com/blog/post/2026-01-16-docker-limit-cpu-memory/view), [Reddit — Containers Stopping Constantly](https://www.reddit.com/r/selfhosted/comments/17yuwau/)

---

### Issue 5.4 — Volume Bind-Mount Permission Mismatches (UID/GID)
- **Description:** Host directories bind-mounted into containers fail with `Permission denied` when the process inside the container runs as a different UID/GID than the host directory owner. Common for databases (PostgreSQL runs as UID 999) and application containers (Node.js often UID 1000).
- **Solution/Workaround:** Match the container's expected UID/GID by running `chown -R <uid>:<gid> ./data` on the host mount point before starting. Use Docker named volumes (not bind mounts) for database data directories where possible — Docker manages ownership automatically. Explicitly set `user: "<uid>:<gid>"` in the Compose service definition.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (database fails to start; data directory unwritable)
- **Source:** [Docker Forums — Volume Permissions](https://forums.docker.com/t/trouble-with-volume-permissions/118503), [OneUptime — Volume Issues](https://oneuptime.com/blog/post/2026-01-25-debug-docker-compose-volume-issues/view)

---

### Issue 5.5 — Startup Hang on 35+ Simultaneous Containers
- **Description:** Starting a large number of containers simultaneously (35+) can cause processes inside containers to hang with `futex(FUTEX_WAIT_PRIVATE)` — waiting for system resources. The root cause is contention on kernel primitives (network namespace creation, cgroup setup) when many containers initialise at once.
- **Solution/Workaround:** Stagger startup using `depends_on` chains to serialise initialisation. Use `docker compose up --scale` or split the stack into independent compose files started in sequence. Add `start_period: 30s` health checks to absorb kernel-level startup lag.
- **Type:** `deployment-time`
- **Severity:** `service-downtime`
- **Source:** [Docker Forums — 35 Containers Hanging](https://forums.docker.com/t/processes-are-getting-hung-when-we-start-35-containers-using-docker-compose-and-without-that/80360)

---

### Issue 5.6 — Legacy `docker-compose` vs `docker compose` CLI Incompatibility
- **Description:** The legacy `docker-compose` (v1, Python binary) is incompatible with modern Docker Engine and fails with `KeyError: 'ContainerConfig'` on `--force-recreate`. Many CI scripts and startup scripts still reference the legacy binary.
- **Solution/Workaround:** Migrate all scripts to use `docker compose` (v2, Go plugin). Verify the Docker Compose plugin is installed: `docker compose version`. Remove any `docker-compose` (hyphenated) references from Makefile, CI scripts, and systemd units.
- **Type:** `deployment-time`
- **Severity:** `service-downtime` (deployment scripts fail on modern Docker)
- **Source:** [Stack Overflow — ContainerConfig Error 2024](https://stackoverflow.com/questions/78380867/docker-compose-run-issue-2024-error-containerconfig)

---

## 6. LiteLLM

> Unified LLM proxy and router. Translates calls to a common OpenAI-compatible API, handles model aliases, fallback chains, cost tracking, and rate limiting.

### Issue 6.1 — Fallback Not Triggered When Using Model Group Alias
- **Description:** When a model is referenced via a `model_group` alias in the fallback config, the fallback mechanism uses the *original* underlying model name rather than the alias, causing `NotFoundError` and preventing fallback execution. The fallback chain silently breaks.
- **Solution/Workaround:** Define fallbacks using the exact `model_name` strings as listed in `model_list`, not aliased group names. Test fallback behaviour explicitly with `mock_testing_fallbacks=True`. Monitor for `NotFoundError (404)` in LiteLLM logs as a signal of broken fallback chains.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (requests fail without fallback when primary model is unavailable)
- **Source:** [LiteLLM GitHub Issue #15493](https://github.com/BerriAI/litellm/issues/15493), [LiteLLM GitHub Issue #21377](https://github.com/BerriAI/litellm/issues/21377)

---

### Issue 6.2 — `$0` Cost Tracking for Certain Models / Provider Misattribution
- **Description:** Some models (e.g., Codestral, Azure GPT-4.1) report `$0.00` spend in LiteLLM's cost tracking dashboard. Root cause: `cost_per_token` values serialised in exponential notation (`3e-07`) are not parsed correctly as floats during spend calculation. Additionally, failed requests are attributed to "unknown" provider rather than the actual provider, undercounting total spend by category.
- **Solution/Workaround:** Use decimal notation for all `input_cost_per_token` / `output_cost_per_token` values in the model config (e.g., `0.0000003` not `3e-07`). Monitor spend by querying the underlying LiteLLM PostgreSQL tables directly, not just the dashboard. Upgrade to latest stable LiteLLM version where fixes may be available per-model.
- **Type:** `coding-time`
- **Severity:** `silent-corruption` (cost attribution wrong; budget controls ineffective)
- **Source:** [LiteLLM GitHub Issue #11266](https://github.com/BerriAI/litellm/issues/11266), [LiteLLM GitHub Issue #11929](https://github.com/BerriAI/litellm/issues/11929)

---

### Issue 6.3 — Timeout Setting Silently Ignored for Streaming Requests (Bedrock/Vertex)
- **Description:** Per-model `timeout` and `stream_timeout` values configured in `litellm_params` or `router_settings` are silently dropped for streaming requests to Bedrock and Vertex AI providers. A hanging streaming response from these providers will never time out, blocking the connection indefinitely.
- **Solution/Workaround:** Set timeouts at the router level (`router_settings.request_timeout`) as well as per-model. For streaming, use `stream_timeout` explicitly in `litellm_params`. Monitor for long-running streaming connections in infrastructure metrics. Add an application-level timeout wrapper around streaming calls.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (connection pool exhausted by hung streaming requests)
- **Source:** [LiteLLM GitHub Issue #23375](https://github.com/BerriAI/litellm/issues/23375)

---

### Issue 6.4 — ConnectTimeout Under High Concurrency
- **Description:** Under high concurrency, LiteLLM's outbound connection pool to provider APIs becomes exhausted, resulting in `ConnectTimeout: Connection timeout to host` errors that are not retried through the fallback chain.
- **Solution/Workaround:** Increase `httpx` connection pool limits in LiteLLM config. Use `num_retries` with connection-timeout errors mapped to fallback models. Monitor `litellm_proxy_requests_total` and `latency_p99` to detect pool exhaustion early. Scale LiteLLM horizontally if single-instance limits are reached.
- **Type:** `deployment-time`
- **Severity:** `service-downtime`
- **Source:** [LiteLLM GitHub Issue #14895](https://github.com/BerriAI/litellm/issues/14895)

---

### Issue 6.5 — Vertex AI / Other Providers Routed to Wrong Endpoint
- **Description:** LiteLLM proxy incorrectly routes `vertex_ai/*` models to the OpenAI endpoint due to provider-resolution and prefix-normalisation bugs in the proxy layer. Requests fail with auth errors or incorrect response formats.
- **Solution/Workaround:** Validate model routing by checking LiteLLM debug logs (`set_verbose: true`) for every new model configuration. Explicitly set `custom_llm_provider` in model definitions rather than relying on prefix inference. Test each model alias immediately after config changes.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [LiteLLM GitHub Issue #21147](https://github.com/BerriAI/litellm/issues/21147)

---

### Issue 6.6 — Client Disconnect Does Not Cancel Ongoing LLM Request
- **Description:** When a client disconnects mid-stream, LiteLLM proxy does not cancel the upstream LLM API call. The provider continues generating tokens, billing continues, and the proxy's outbound connection is held open until the provider finishes.
- **Solution/Workaround:** Implement application-level request cancellation tokens. Use `asyncio.shield()` carefully — it prevents cancellation propagation. Monitor for orphaned long-running upstream connections. This is an open bug; check latest LiteLLM releases for fix status.
- **Type:** `deployment-time`
- **Severity:** `degraded-performance` (+ unnecessary API cost)
- **Source:** [LiteLLM GitHub Issue #22805](https://github.com/BerriAI/litellm/issues/22805)

---

## 7. FastAPI

> High-performance async Python web framework. Used as the API gateway for the stack, handling auth, routing, request validation, and middleware composition.

### Issue 7.1 — Synchronous Blocking Code Inside `async def` Blocks the Event Loop
- **Description:** Calling synchronous blocking functions (e.g., `time.sleep()`, synchronous database drivers, CPU-bound operations) inside `async def` route handlers blocks the entire FastAPI event loop. All other requests stall until the blocking call completes. This is the single most common FastAPI production failure.
- **Solution/Workaround:** Use `await asyncio.to_thread(sync_function)` or `loop.run_in_executor()` to offload blocking calls to a thread pool. For CPU-bound work, use `multiprocessing`. Use only async-native libraries (`asyncpg`, `httpx`, `aiobotocore`) inside `async def` endpoints. Define CPU-bound or legacy-sync routes as `def` (not `async def`) — FastAPI will run them in a thread pool automatically.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (entire API unresponsive while one request blocks)
- **Source:** [FastAPI Async Docs](https://fastapi.tiangolo.com/async/), [Reddit — FastAPI Blocking](https://www.reddit.com/r/FastAPI/comments/1euhq69/fastapi_is_blocked_when_an_endpoint_takes_longer/)

---

### Issue 7.2 — CORS Errors Despite Correct `CORSMiddleware` Configuration
- **Description:** `CORSMiddleware` fails to add CORS headers when it is not the *first* middleware registered. If an auth middleware or error handler precedes it and raises an exception, the error response lacks CORS headers. The browser surfaces a CORS error instead of the underlying auth/validation error.
- **Solution/Workaround:** Always register `CORSMiddleware` as the **first** middleware via `app.add_middleware()`. Ensure `allow_origins` entries exactly match the browser's `Origin` header (scheme, host, port — case-sensitive, no trailing slash). When `allow_credentials=True`, do not use `allow_origins=["*"]` — list origins explicitly.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (all cross-origin API calls blocked)
- **Source:** [Stack Overflow — FastAPI CORS Despite Config](https://stackoverflow.com/questions/79741598), [David Muraya CORS Guide](https://davidmuraya.com/blog/fastapi-cors-configuration/)

---

### Issue 7.3 — Middleware Order Determines Execution, Not Declaration Order
- **Description:** FastAPI middleware runs in LIFO (last-in, first-out) order relative to the order `add_middleware()` is called. Auth middleware added after CORS middleware will execute *before* CORS middleware, meaning unauthenticated requests can receive CORS errors instead of 401s — confusing clients and logs.
- **Solution/Workaround:** Register middleware in reverse execution order: add the middleware you want to run *last* first. Typical correct order: `app.add_middleware(CORSMiddleware, ...)` → `app.add_middleware(AuthMiddleware, ...)` → results in auth running first, CORS running second. Verify with a `debug=True` trace.
- **Type:** `coding-time`
- **Severity:** `degraded-performance` (incorrect error responses confuse clients)
- **Source:** [FastAPI Official CORS Docs](https://fastapi.tiangolo.com/tutorial/cors/), [David Muraya CORS Guide](https://davidmuraya.com/blog/fastapi-cors-configuration/)

---

### Issue 7.4 — `InjectedState` Treated as Required Tool Parameter
- **Description:** FastAPI (via LangGraph CLI integration) incorrectly treats `InjectedState` annotated parameters as required request body fields, causing validation failures on valid tool calls that rely on injected state rather than explicit parameters.
- **Solution/Workaround:** Ensure `InjectedState` parameters are explicitly marked with `Annotated` in the function signature. Use LangGraph's `ToolNode` rather than raw FastAPI routing for tool registration when using LangGraph's framework.
- **Type:** `coding-time`
- **Severity:** `service-downtime`
- **Source:** [LangGraph GitHub Issue — InjectedState](https://github.com/langchain-ai/langgraph/issues)

---

### Issue 7.5 — Request Validation Errors Return 422 Without Client-Readable Detail
- **Description:** When Pydantic model validation fails, FastAPI returns `422 Unprocessable Entity` with a detailed error body. However, if the error body is large or deeply nested, some HTTP clients truncate it. Additionally, validation errors from nested models can expose internal field names to external clients.
- **Solution/Workaround:** Implement a custom `RequestValidationError` exception handler that normalises and sanitises error output. Log full validation details server-side while returning a simplified error to clients. Use `response_model_exclude_unset=True` to prevent over-exposure.
- **Type:** `coding-time`
- **Severity:** `degraded-performance`
- **Source:** [FastAPI Exception Handling Docs](https://fastapi.tiangolo.com/tutorial/handling-errors/)

---

## 8. PostgreSQL + pgvector + TimescaleDB

> Relational database layer. pgvector adds approximate nearest-neighbour vector search (HNSW and IVFFlat). TimescaleDB adds hypertables, continuous aggregates, and time-based partitioning for time-series workloads.

### Issue 8.1 — PgBouncer Transaction Mode Incompatible with Prepared Statements
- **Description:** PgBouncer in `transaction` pooling mode (the recommended high-performance mode) does not support prepared statements, which operate at session level. Applications using prepared statements (SQLAlchemy with `statement_cache_size > 0`, JDBC with `prepareThreshold > 0`) will intermittently fail with `ERROR: prepared statement "X" already exists`.
- **Solution/Workaround:** Disable client-side prepared statements: set `prepare_threshold=0` in psycopg, `preparedStatementCacheQueries=0` in JDBC. Alternatively, configure PgBouncer to `pool_mode=session` for affected databases only. pgBouncer ≥1.21 has experimental server-side prepared statement tracking — test under load before enabling in production.
- **Type:** `coding-time`
- **Severity:** `service-downtime` (intermittent errors at scale)
- **Source:** [Opensource-DB — PgBouncer Prepared Statements](https://opensource-db.com/how-we-solved-prepared-statement-issues-with-pgbouncers-transaction-pooling/), [Stack Overflow — PgBouncer Transaction Mode](https://stackoverflow.com/questions/60318413)

---

### Issue 8.2 — pgvector HNSW Index: Index Not Used for Filtered Vector Queries
- **Description:** When combining vector similarity search with `WHERE` clause filters (`WHERE category = 'X' ORDER BY embedding <-> $1 LIMIT 10`), PostgreSQL's query planner often falls back to a sequential scan with post-filter rather than using the HNSW index with pre-filter. This makes filtered vector search O(N) on large tables.
- **Solution/Workaround:** Use partial indexes (`CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) WHERE category = 'X'`) for commonly filtered subsets. Use `SET hnsw.ef_search = 200` for better recall at the cost of latency. Always run `EXPLAIN ANALYZE` to verify index usage. Increase `max_parallel_workers_per_gather` for parallelised exact scans when approximate indexes are impractical.
- **Type:** `coding-time`
- **Severity:** `degraded-performance`
- **Source:** [Microsoft — Optimise pgvector Performance](https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-optimize-performance-pgvector), [GitHub pgvector Issue #455](https://github.com/pgvector/pgvector/issues/455)

---

### Issue 8.3 — HNSW Index Rebuild Is Memory-Intensive and Blocks Production
- **Description:** HNSW index builds allocate large amounts of contiguous memory (controlled by `maintenance_work_mem`). On large tables (millions of vectors), a rebuild can require tens of GB of RAM and take hours, degrading query performance for all other workloads on the same instance while running.
- **Solution/Workaround:** Load all data *before* creating the index — building index on pre-loaded data is faster and produces better graph structure. Use `maintenance_work_mem = '4GB'` for index builds in a maintenance window. For online rebuilds, use `CREATE INDEX CONCURRENTLY` to avoid blocking writes. Consider pre-warming the index post-build with `pg_prewarm`.
- **Type:** `deployment-time`
- **Severity:** `degraded-performance` (can escalate to OOM on constrained hosts)
- **Source:** [Alex Jacobs — The Case Against pgvector](https://alex-jacobs.com/posts/the-case-against-pgvector/), [Railway — Hosting Postgres with pgvector](https://blog.railway.com/p/hosting-postgres-with-pgvector)

---

### Issue 8.4 — IVFFlat Index Recall Degrades Over Time as Data Grows
- **Description:** IVFFlat clusters are computed at index creation time. As new data is inserted, cluster assignments become suboptimal — newer vectors may land in poorly-matching clusters. Search recall degrades silently over time without any error, often not detected until retrieval quality drops noticeably.
- **Solution/Workaround:** Periodically `REINDEX` the IVFFlat index (ideally in a maintenance window). Monitor recall by comparing approximate results against exact search (`SET enable_indexscan = off`) on a sample. Consider migrating to HNSW, which does not require periodic rebuilds.
- **Type:** `deployment-time`
- **Severity:** `silent-corruption` (wrong search results returned without error)
- **Source:** [Alex Jacobs — The Case Against pgvector](https://alex-jacobs.com/posts/the-case-against-pgvector/)

---

### Issue 8.5 — TimescaleDB `cagg_migrate()` Fails on Continuous Aggregates with Time Bucket Offsets
- **Description:** Migrating continuous aggregates from old to new format using `cagg_migrate()` fails with `cannot find time_partition_col` when the aggregate uses `time_bucket()` with an interval offset parameter. This blocks database upgrades and leaves the system on outdated TimescaleDB/PostgreSQL versions.
- **Solution/Workaround:** Migrate non-offset continuous aggregates first, then offset ones separately. Manually add the `user_view_definition` text column to `_timescaledb_catalog.continuous_agg_migrate_plan` if missing. Ensure the migrating user has `SELECT, INSERT, UPDATE` grants on the relevant catalog tables.
- **Type:** `deployment-time`
- **Severity:** `service-downtime` (upgrade blocker; risks data loss if retention policies run during failed migration)
- **Source:** [TimescaleDB GitHub Issue #7236](https://github.com/timescale/timescaledb/issues/7236)

---

### Issue 8.6 — Continuous Aggregate Watermark in the Future Suppresses Real-Time Data
- **Description:** In certain conditions, the continuous aggregate watermark advances into the future, causing all buckets — including the most recent — to be materialized. Queries return only historical materialized data with no real-time appended data, silently returning stale results.
- **Solution/Workaround:** Check the watermark with `SELECT _timescaledb_functions.cagg_watermark(<cagg_hypertable_id>)`. Manually refresh the aggregate: `CALL refresh_continuous_aggregate('<cagg_name>', NULL, NULL)`. Add monitoring alerts that compare cagg query output against direct hypertable query for the most recent time bucket.
- **Type:** `deployment-time`
- **Severity:** `silent-corruption` (stale aggregates returned without error)
- **Source:** [TimescaleDB Continuous Aggregates Troubleshooting](https://www.tigerdata.com/docs/use-timescale/latest/continuous-aggregates/troubleshooting)

---

### Issue 8.7 — Stale Query Statistics Cause Suboptimal Vector Query Plans
- **Description:** PostgreSQL's query planner uses statistics from the most recent `ANALYZE`. After heavy inserts of vector data, statistics become stale — the planner underestimates row counts and chooses sequential scans over index scans, or vice versa. For pgvector, this is especially acute because the planner doesn't natively understand vector distribution.
- **Solution/Workaround:** Schedule `ANALYZE VERBOSE <table>` to run after large ingestion batches. Increase `default_statistics_target` for vector columns: `ALTER TABLE ... ALTER COLUMN embedding SET STATISTICS 1000`. Use `pg_stat_user_tables` to monitor last-analyze timestamps. Consider enabling `autovacuum_analyze_scale_factor = 0.01` on large vector tables.
- **Type:** `deployment-time`
- **Severity:** `degraded-performance`
- **Source:** [Microsoft — Optimise pgvector Performance](https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-optimize-performance-pgvector)

---

### Issue 8.8 — TimescaleDB Historical Data Inserts Not Reflected in Real-Time Aggregates
- **Description:** Inserting historical data (timestamps earlier than the last materialization watermark) into a hypertable does not trigger an update to the continuous aggregate. Real-time aggregates are only appended *after* the watermark — backfilled data is silently excluded until a manual refresh.
- **Solution/Workaround:** After any historical data load, manually call `CALL refresh_continuous_aggregate('<cagg_name>', <start>, <end>)` covering the historical range. Set up monitoring to detect discrepancies between hypertable row counts and continuous aggregate coverage.
- **Type:** `coding-time`
- **Severity:** `silent-corruption`
- **Source:** [TimescaleDB Continuous Aggregates Troubleshooting](https://www.tigerdata.com/docs/use-timescale/latest/continuous-aggregates/troubleshooting)

---

## Summary Risk Matrix

| Technology | Issue Count | Data Loss Risk | Downtime Risk | Silent Corruption Risk |
|---|---|---|---|---|
| FalkorDB | 9 | Medium (OOM crash) | High (unbounded query crash, write hang) | High (wrong vector results, LIMIT bypass, relation count) |
| Graphiti | 7 | High (edge UUID null) | High (GroupId bug, LiteLLM port) | High (duplicate entities, stale temporal edges) |
| Temporal.io | 7 | Low | High (NDE stall, worker drain, routing mismatch) | Medium (silent retry loops) |
| LangGraph | 7 | High (checkpoint corruption) | Medium (recursion limit, tool loops) | High (sub-graph state isolation, stale parent state) |
| Docker Compose | 6 | Medium (volume permissions) | High (OOM kill, startup hang, DNS) | Low |
| LiteLLM | 6 | Low | High (fallback break, timeout ignored) | High ($0 cost tracking, provider misattribution) |
| FastAPI | 5 | Low | High (event loop blocking, CORS) | Low |
| PostgreSQL/pgvector/TimescaleDB | 8 | Medium (cagg migration) | Medium (PgBouncer, HNSW rebuild) | High (IVFFlat recall, watermark, stale stats) |

---

## Operational Recommendations (Stack-Wide)

1. **Query bounding (FalkorDB):** Enforce depth limits on all graph traversals. Make unbounded `[*]` patterns a linting error in code review.
2. **Checkpoint validation (LangGraph):** Add output validation hooks in every node. Never trust unvalidated LLM output going into state.
3. **Replay testing (Temporal):** Run `WorkflowReplayer` in CI on every PR that touches workflow code. This is non-negotiable.
4. **Explicit memory limits (Docker):** Every container must have `mem_limit` set. Budget RAM per tier before deployment.
5. **Cost tracking audit (LiteLLM):** Query LiteLLM's PostgreSQL spend tables directly weekly. Do not rely solely on the dashboard.
6. **Event loop hygiene (FastAPI):** Use `asyncio.to_thread()` for any sync call inside `async def`. Add a middleware that logs requests exceeding 5 seconds response time.
7. **pgvector recall monitoring:** Run scheduled exact-vs-approximate recall tests on a sample query set. Alert when recall drops below 90%.
8. **Graphiti deduplication testing:** After any ingestion run, query for duplicate entity names. This is not checked automatically.

---

*Sources: [FalkorDB GitHub Issues](https://github.com/FalkorDB/FalkorDB/issues) · [FalkorDB Docs — Known Limitations](https://docs.falkordb.com/cypher/known-limitations.html) · [Graphiti GitHub Issues](https://github.com/getzep/graphiti/issues) · [Temporal Community Forum](https://community.temporal.io) · [Temporal Docs](https://docs.temporal.io) · [LangGraph GitHub Issues](https://github.com/langchain-ai/langgraph/issues) · [LangChain Forum](https://forum.langchain.com) · [LiteLLM GitHub Issues](https://github.com/BerriAI/litellm/issues) · [Docker Forums](https://forums.docker.com) · [pgvector GitHub Issues](https://github.com/pgvector/pgvector/issues) · [TimescaleDB GitHub Issues](https://github.com/timescale/timescaledb/issues) · [TimescaleDB Docs](https://www.tigerdata.com/docs/use-timescale/latest/continuous-aggregates/troubleshooting) · [FastAPI Docs](https://fastapi.tiangolo.com) · [Microsoft pgvector Optimisation](https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-optimize-performance-pgvector)*
