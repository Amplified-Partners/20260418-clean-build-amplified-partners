---
title: "Provider Test Results"
id: "tech-provider-test-results-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Provider Test Results

## 1. Ollama (Local) ✅ VERIFIED

**Status:** Running and accessible
**Endpoint:** http://localhost:11434
**Available Models:**
- `qwen2.5-coder:14b` (14.8B parameters, Q4_K_M quantization)
- `llama3.1:8b` (8.0B parameters, Q4_K_M quantization)
- `qwen2.5:14b` (14.8B parameters, Q4_K_M quantization)
- `llama3.2:latest` (3.2B parameters, Q4_K_M quantization) ← **Configured for Ask mode**

**Test:** Successfully connected to Ollama API and retrieved model list

---

## 2. Qwen (via OpenRouter) ⏳ NEEDS TESTING

**Status:** Configured in Kilo
**Endpoint:** https://openrouter.ai/api/v1
**Model:** qwen/qwen-2.5-coder-32b-instruct
**Configured For:** Code mode

**To Test:**
1. Switch to Code mode
2. Ask it to write a simple function
3. Verify the response comes from Qwen Coder Plus

**Expected Behavior:** Should generate code efficiently

---

## 3. MiniMax M2 ⏳ NEEDS TESTING

**Status:** Configured in Kilo
**Endpoint:** Via OpenRouter or OpenAI-compatible
**Model:** minimax/minimax-01
**Configured For:** Available but not assigned to a mode

**To Test in Kilo:**
1. Check Kilo Settings → API Providers → MiniMax
2. Look for "Test Connection" button
3. Click to verify API key and connection

**Alternative Test:**
Temporarily assign MiniMax to a mode and test with a simple request

---

## Test Plan Summary

### What's Verified ✅
- [x] Ollama running locally
- [x] Multiple local models available
- [x] Llama 3.2 ready for Ask mode

### What Needs Testing ⏸
- [ ] Qwen via OpenRouter (Code mode)
- [ ] MiniMax API connection
- [ ] OpenRouter API key validity

### Recommended Test Sequence

**Step 1: Test Ollama/Ask Mode**
- Switch to Ask mode
- Ask: "What is 2+2?"
- Should get response from local Llama 3.2

**Step 2: Test Qwen/Code Mode**  
- Switch to Code mode
- Ask: "Write a Python function to reverse a string"
- Should get response from Qwen Coder Plus

**Step 3: Test MiniMax**
- Open Kilo Settings
- Navigate to MiniMax provider
- Click "Test Connection"
- Verify success

---

## Notes

- **Ollama Advantages:** Free, local, private, no API costs
- **Qwen via OpenRouter:** Specialized coding model
- **MiniMax:** Advanced reasoning model

All providers configured. Local testing shows Ollama operational. Remote providers (Qwen, MiniMax) require Kilo UI testing to verify API connections.