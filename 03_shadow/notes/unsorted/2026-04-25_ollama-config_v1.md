---
title: "Ollama Configuration for M4 (24GB RAM)"
id: "ollama-config"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Ollama Configuration for M4 (24GB RAM)

This configuration is optimized for an Apple Silicon M4 with 24GB Unified Memory.

## 1. Model Selection Strategy

### Coding (Primary)
- **Model:** `qwen2.5-coder:7b`
- **Why:** Best-in-class coding performance for its size. Fast inference on M4.
- **VRAM Usage:** ~5GB (leaving plenty for OS + IDE).

### General Reasoning / Chat
- **Model:** `llama3:8b` or `mistral:7b`
- **Why:** Good general knowledge, fast.
- **VRAM Usage:** ~5-6GB.

### Deep Reasoning (Fallback)
- **Model:** `qwen2.5:14b` or `mistral-nemo:12b`
- **Why:** Better reasoning capabilities but slower.
- **VRAM Usage:** ~10-12GB (Use with caution if running heavy IDEs).

## 2. Concurrency Settings
To avoid thrashing swap, limit concurrent model loads.

- **`OLLAMA_MAX_LOADED_MODELS=1`**: Only keep one model in VRAM at a time.
- **`OLLAMA_NUM_PARALLEL=2`**: Allow 2 parallel requests to the *same* model (e.g., autocomplete + chat).

## 3. Context Window
- Default: 2048
- **Recommended:** 8192 for coding tasks.
- **Command:** `ollama run qwen2.5-coder:7b --ctx 8192` (or configure in Modelfile).

## 4. Modelfile Template (Custom)
Create a custom Modelfile for the coding assistant:

```dockerfile
FROM qwen2.5-coder:7b

# Set parameters
PARAMETER temperature 0.1
PARAMETER num_ctx 8192
PARAMETER stop "<|endoftext|>"
PARAMETER stop "<|im_end|>"

# System prompt
SYSTEM """
You are an expert coding assistant. Write clean, efficient, and type-safe code.
"""
```

## 5. Memory Management
- **Monitor:** Use `setup/local-benchmarks.py` to check memory usage.
- **Warning Zone:** If "Memory Pressure" in Activity Monitor turns Yellow, stop the model (`ollama stop <model>`) or close unused browser tabs.
