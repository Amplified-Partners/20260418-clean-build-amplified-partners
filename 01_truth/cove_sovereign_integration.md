# Cove + Sovereign Fleet Integration
**Antigravity | 2026-05-05 | Status: Phase 5 Blueprint**

## Overview
Cove serves as the visual workspace for collaborative human-AI planning, while the Sovereign Fleet (Hermes, Alpha, Kimmy, Charlie) operates as the headless execution layer. Long-term unification requires bridging Cove's visual canvas with the Fleet's backend processing capabilities.

## Integration Architecture

### 1. Bi-Directional Sync (The Canvas Bridge)
- **Fleet to Cove**: When the Fleet generates a structural plan or a research brief (like Cassian's Perplexity outputs), the Orchestrator (Kimmy) pushes the Markdown directly into a Cove Canvas via API.
- **Cove to Fleet**: When Ewan spatially arranges notes or connects ideas on the Cove Canvas, a webhook triggers the Fleet's ingestion pipeline. The spatial relationships are mapped into Neo4j graph nodes.

### 2. The Agentic Pointer
- Cove's strength is spatial reasoning. The Sovereign Fleet lacks eyes.
- We will integrate an "Agentic Pointer" where Ewan can highlight a section of the Cove canvas and assign it to an entity (e.g., `@Devon: Build this`).
- The Fleet intercepts the mention, pulls the surrounding context from the Canvas, and generates an `implementation_plan.md` in the background.

### 3. Execution Status Overlays
- When Devon executes a build, the status (e.g., `[RUNNING]`, `[FAILED]`, `[IBAC_BLOCKED]`) is overlaid on the Cove canvas block that initiated the task.
- This creates a single pane of glass for Ewan, eliminating the need to drop into the terminal to check background logs.
