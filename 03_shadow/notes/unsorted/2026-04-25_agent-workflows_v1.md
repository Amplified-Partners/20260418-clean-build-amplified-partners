---
title: "Agent Workflows"
id: "agent-workflows"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Agent Workflows

This document defines reusable workflows for common AI-assisted tasks.

## 1. Feature Implementation Workflow
**Trigger:** "Implement feature [X] based on spec [Y]"

1.  **Spec Review:** Read the spec file and related existing code.
2.  **Test Plan:** Create a test plan (list of test cases) in a temporary markdown file.
3.  **Test Implementation:** Write failing tests (TDD) in the appropriate test directory.
4.  **Code Implementation:** Write the code to pass the tests.
5.  **Verification:** Run tests and fix any failures.
6.  **Refinement:** Refactor code for readability and performance.
7.  **PR Prep:** Delete temporary files and generate a PR description.

## 2. Railway Error Analysis Workflow
**Trigger:** "Analyze this Railway error log: [LOG]"

1.  **Log Parsing:** Identify the error type, timestamp, and service.
2.  **Context Gathering:** Search for the error message in the codebase.
3.  **Local Reproduction:** Attempt to reproduce the error locally (if possible) or create a reproduction script.
4.  **Root Cause Analysis:** Hypothesize the cause (e.g., database timeout, null pointer, OOM).
5.  **Fix Proposal:** Suggest a code fix or configuration change.
6.  **Patching:** Apply the fix and verify (if local reproduction was successful).

## 3. Performance Tuning Workflow
**Trigger:** "Run a perf tuning pass on [Service/Module]"

1.  **Hotspot Identification:** Review code for O(n^2) loops, N+1 queries, or heavy synchronous operations.
2.  **Benchmark Creation:** Create a micro-benchmark script to measure current performance.
3.  **Optimization:** Apply optimizations (caching, indexing, async execution).
4.  **Verification:** Run the benchmark again to measure improvement.
5.  **Regression Check:** Run the full test suite to ensure no breakage.

## 4. Git Workflow for Large Refactors
**Trigger:** "Refactor [Module] to use [New Pattern]"

1.  **Branching:** Create a new feature branch `refactor/[module-name]`.
2.  **Incremental Changes:** Apply changes in small, logical commits.
3.  **Continuous Testing:** Run tests after each significant change.
4.  **Final Review:** Compare the branch against `main` before merging.