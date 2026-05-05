---
title: "Kilo Code Setup Documentation"
id: "kilo-setup-docs-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Kilo Code Setup Documentation

**Setup Date:** December 22, 2025  
**Setup Completed By:** Architect Mode (Claude Sonnet 4.5)

---

## Overview

This document provides a complete reference for your Kilo Code configuration. All AI providers and modes have been successfully configured to work together seamlessly.

---

## Configured AI Providers

### 1. Anthropic (Claude)
- **Base URL:** `https://api.anthropic.com`
- **Provider Type:** Anthropic
- **Models Available:**
  - `claude-sonnet-4-5` (Claude Sonnet 4.5)
- **Status:** ✅ Connected and tested
- **Use Case:** Strategic planning, coordination, and orchestration

### 2. OpenAI
- **Base URL:** `https://api.openai.com/v1`
- **Provider Type:** OpenAI
- **Models Available:**
  - `gpt-4o` (GPT-4 Optimized)
  - `o1` (Reasoning model for debugging)
- **Status:** ✅ Connected and tested
- **Use Case:** Code generation backup, deep reasoning for debugging

### 3. Google Gemini
- **Base URL:** `https://generativelanguage.googleapis.com/v1beta`
- **Provider Type:** Google
- **Models Available:** Gemini models
- **Status:** ✅ Connected and tested
- **Use Case:** Alternative AI provider for various tasks

### 4. Ollama (Local)
- **Base URL:** `http://localhost:11434/v1`
- **Provider Type:** OpenAI-Compatible
- **Models Available:**
  - `llama3.2:latest` (Llama 3.2)
- **Status:** ✅ Connected and tested
- **Use Case:** Free local AI for explanations and general queries
- **Note:** Requires Ollama to be running locally

### 5. Qwen (Alibaba Cloud)
- **Base URL:** `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **Provider Type:** OpenAI-Compatible
- **Models Available:**
  - `qwen-coder-plus-latest` (Qwen Coder Plus)
- **Status:** ✅ Connected and tested
- **Use Case:** Fast, specialized coding and implementation

### 6. OpenRouter
- **Base URL:** `https://openrouter.ai/api/v1`
- **Provider Type:** OpenAI-Compatible
- **Models Available:** Multi-model access (Claude, GPT, Llama, etc.)
- **Status:** ✅ Connected and tested
- **Use Case:** Backup provider with access to multiple AI models

### 7. MiniMax
- **Base URL:** `https://api.minimax.chat/v1`
- **Provider Type:** OpenAI-Compatible
- **Models Available:**
  - `abab6.5-chat` (MiniMax M2)
- **Status:** ✅ Connected and tested
- **Use Case:** Additional AI provider option

---

## Mode Configurations

### Architect Mode
- **Provider:** Anthropic
- **Model:** `claude-sonnet-4-5`
- **Temperature:** 0.7
- **Max Tokens:** 8192
- **Purpose:** Planning, design, strategy, and task breakdown
- **When to Use:** When you need to plan projects, design architecture, or break down complex problems

### Orchestrator Mode
- **Provider:** Anthropic
- **Model:** `claude-sonnet-4-5`
- **Temperature:** 0.7
- **Max Tokens:** 8192
- **Purpose:** Coordinating complex multi-step tasks and managing workflows
- **When to Use:** For complex projects requiring coordination across multiple subtasks

### Code Mode
- **Provider:** Qwen
- **Model:** `qwen-coder-plus-latest`
- **Temperature:** 0.3 (focused for coding)
- **Max Tokens:** 8192
- **Purpose:** Fast, specialized code generation and implementation
- **When to Use:** For writing new code, implementing features, making code changes
- **Backup Option:** Can switch to GPT-4o for complex refactoring if needed

### Debug Mode
- **Provider:** OpenAI
- **Model:** `o1`
- **Temperature:** 1.0
- **Max Tokens:** 8192
- **Purpose:** Deep reasoning for debugging and troubleshooting
- **When to Use:** When debugging complex issues, analyzing errors, or investigating root causes

### Ask Mode
- **Provider:** Ollama
- **Model:** `llama3.2:latest`
- **Temperature:** 0.7
- **Max Tokens:** 4096
- **Purpose:** Free local AI for explanations, questions, and learning
- **When to Use:** For general questions, explanations, code understanding (read-only)
- **Note:** Requires Ollama running locally; completely free to use

---

## How to Use Kilo Code

### Switching Between Modes

1. **In VS Code:**
   - Click the Kilo icon in the sidebar
   - You'll see the current mode at the top
   - Click the mode name to see a dropdown of available modes
   - Select the mode you need

2. **Mode Selection Guide:**
   - Planning a project? → **Architect**
   - Complex multi-step task? → **Orchestrator**
   - Need to write code? → **Code**
   - Debugging an issue? → **Debug**
   - Just have questions? → **Ask**

### Typical Workflow

1. **Start with Architect** - Plan your project
2. **Switch to Code** - Implement the solution
3. **Use Debug** if issues arise
4. **Ask Ask mode** for explanations or clarifications

---

## Model Selection Strategy

This configuration follows a strategic allocation:

```
Planning & Strategy ─────→ Claude Sonnet 4.5 (Architect/Orchestrator)
                             │
Code Implementation ────────→ Qwen Coder Plus (Code mode)
                             │
Deep Reasoning ─────────────→ OpenAI o1 (Debug mode)
                             │
General Questions ──────────→ Llama 3.2 via Ollama (Ask mode)
```

---

## Important Notes

### API Key Security
- ✅ All API keys are stored securely in Kilo's configuration
- ✅ API keys are never displayed in full in this documentation
- ⚠️  Never share or commit API keys to version control

### Provider Dependencies
- **Ollama:** Must be running locally (`ollama serve`)
  - Check status: `ollama list`
  - Start if needed: Ollama should auto-start or run `ollama serve`

### Cost Considerations
- **Free/Low Cost:** Ollama (completely free, runs locally)
- **Moderate Cost:** Qwen, Claude (pay per token)
- **Higher Cost:** OpenAI o1, GPT-4o (more expensive reasoning models)
- **Use Free Option:** Ask mode (Ollama) is perfect for general questions

### Base URL Patterns
Important differences to remember:
- Anthropic: No `/v1` suffix
- OpenAI: Requires `/v1` suffix
- Google: Uses `/v1beta` suffix
- OpenAI-compatible (Qwen, OpenRouter, MiniMax, Ollama): Use `/v1` suffix

---

## Troubleshooting

### Provider Connection Issues

**Anthropic/OpenAI/Qwen/OpenRouter/MiniMax:**
- Verify API key is valid and has credits
- Check internet connection
- Confirm base URL is correct

**Google Gemini:**
- Verify API key and Google Cloud project setup
- Ensure Gemini API is enabled in your project

**Ollama:**
- Confirm Ollama is running: `ollama list`
- Start Ollama if needed: `ollama serve`
- Verify model is downloaded: `ollama list` should show `llama3.2:latest`
- Check connection: Test at `http://localhost:11434`

### Mode Not Working
1. Check provider configuration for that mode
2. Verify model name is correct
3. Test provider connection independently
4. Check Kilo logs for specific error messages

### Slow Responses
- Ollama (local) is fastest but lower quality
- Qwen is fast for coding
- o1 is slower due to deep reasoning (this is normal)

---

## Adding More Providers

If you want to add more providers later:

1. Open Kilo Settings (⚙️ icon)
2. Navigate to "API Providers"
3. Click "Add Provider"
4. Fill in provider details:
   - Name, Type, Base URL, API Key
5. Add models for that provider
6. Test the connection
7. Update mode configurations to use new provider if desired

---

## Updating This Configuration

To modify your setup:

1. **Change a Provider:**
   - Settings → API Providers → Select provider → Edit

2. **Change a Mode:**
   - Settings → Modes → Select mode → Change provider/model

3. **Add New Models:**
   - Settings → API Providers → Select provider → Add Model

---

## Quick Reference

| Mode | Provider | Model | Best For |
|------|----------|-------|----------|
| Architect | Anthropic | Claude Sonnet 4.5 | Planning, design |
| Orchestrator | Anthropic | Claude Sonnet 4.5 | Task coordination |
| Code | Qwen | Qwen Coder Plus | Fast coding |
| Debug | OpenAI | o1 | Deep debugging |
| Ask | Ollama | Llama 3.2 | Free explanations |

---

## Success Checklist

- ✅ All 7 providers configured and tested
- ✅ All 5 modes configured with appropriate models
- ✅ Ollama running locally with Llama 3.2
- ✅ API keys securely stored
- ✅ Documentation created

---

## Next Steps

You're all set! Here's how to start using Kilo:

1. **Try each mode** with a simple task to verify everything works
2. **Start with Architect mode** for your next project
3. **Use Ask mode** freely - it's running locally and costs nothing
4. **Switch modes as needed** throughout your workflow

---

## Support

If you need to adjust this configuration:
- Open Kilo Settings (⚙️)
- Refer to this documentation for current setup
- Remember: Architect mode can help you modify configurations

---

**Configuration Complete!** 🎉

Your Kilo Code setup is fully configured and ready to use. You now have access to multiple AI providers across different modes, optimized for different types of tasks.