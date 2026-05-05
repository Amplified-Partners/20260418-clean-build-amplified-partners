# Hermes Architecture Design
**Antigravity | 2026-05-05 | Status: Approved for Build**

## Overview
The OpenClaw stateless containers are insufficient for sovereign agents. Hermes is the persistent memory execution substrate that allows an agent to wake up, remember its intent, act, and sleep without dropping context.

## Core Components

### 1. Memory Schema (The SQLite Tri-Store)
Each Hermes agent maintains a local SQLite database divided into three schemas:
- **Episodic Memory**: A rolling chronological log of observations and actions (`id`, `timestamp`, `observation`, `action_taken`). Flush to Postgres lakehouse eagerly when the task completes.
- **Decisions**: A log of explicit choices made (`id`, `decision`, `rationale`, `alternatives_rejected`).
- **Intent Tokens**: Active IBAC cryptographic tokens granting permission to execute destructive actions (`token_id`, `scope`, `expiry`).

### 2. The FastAPI Service Shape
Hermes exposes a lightweight HTTP interface to the outside world, strictly authenticated via mTLS or header keys.
- `POST /task`: Inject a new objective into the agent's queue.
- `GET /state`: Dump the current episodic memory and status.
- `POST /interrupt`: Force a sleep or halt the current iteration loop.

### 3. The Cron Scheduler
Agents are not constantly polling. Hermes utilizes an event-driven hook system backed by a cron scheduler.
- **Tick Rate**: Configurable (e.g., every 5 minutes).
- On tick, the agent reads its task queue, pulls relevant context from the Qdrant vector store, executes its `MAX_TOKENS` iteration budget, and sleeps.

### 4. IBAC Integration Points
Before taking any action that reaches outside the container, Hermes intercepts the call and verifies:
1. Is the action registered in `actions.py`?
2. Does the agent hold an active, non-expired Intent Token for this scope?
3. Does the Cedar policy engine return `ALLOW`?

## Hand-off to Devon
Devon: Translate this design into the foundational Python boilerplate for the Hermes Substrate. Build the SQLite schemas and the FastAPI routes.
