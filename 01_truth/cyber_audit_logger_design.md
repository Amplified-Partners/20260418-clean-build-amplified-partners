# CyberAuditLogger Design: CoT Tracing
**Antigravity | 2026-05-05 | Status: Phase 2 Blueprint**

## Overview
As Charlie (DeepSeek R1) steps into the Auditor/Devil's Advocate role, we need a mechanism to securely log and analyze his internal reasoning. DeepSeek R1 utilizes explicit `<think>` tokens for Chain of Thought (CoT). The CyberAuditLogger is the middleware responsible for capturing, parsing, and storing these traces before they are flattened into the final response.

## Architecture

### 1. The Interceptor Middleware
Situated within the LiteLLM proxy or directly inside the Hermes FastAPI layer, the Interceptor parses incoming streams from the Ollama R1 container.
- It detects the `<think>` and `</think>` boundaries.
- It extracts the raw CoT string.

### 2. The Logger Sink
- Extracted CoT strings are pushed asynchronously to a dedicated `audit_traces` table in Postgres.
- **Schema**: `id`, `session_id`, `agent_id` (Charlie), `timestamp`, `raw_cot_text`, `decision_id` (foreign key to Hermes memory).

### 3. Analytics & Alerting
- If the CoT length exceeds a defined threshold without producing a valid output (infinite loop detection), the CyberAuditLogger triggers a `SIGINT` to the Hermes container to halt token bleed.
- The logs are made available to the Arbiter (Alpha/Antigravity) to verify that Charlie actually evaluated the counter-arguments rather than fabricating a sycophantic approval.
