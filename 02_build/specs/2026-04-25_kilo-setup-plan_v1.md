---
title: "Kilo Code Multi-AI Setup Plan"
id: "kilo-setup-plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Kilo Code Multi-AI Setup Plan

**Date:** 2025-12-22
**Status:** Ready for Implementation

## 📋 Approved Model Allocation

| Mode | Primary Model | Provider | Purpose |
|------|--------------|----------|---------|
| **Architect** | Claude Sonnet 4.5 | Anthropic | Planning & strategy |
| **Orchestrator** | Claude Sonnet 4.5 | Anthropic | Coordination & task management |
| **Code** | Qwen-Coder-32B | Qwen Direct | Fast, specialized coding |
| **Code (Alt)** | GPT-4o | OpenAI | Complex refactoring backup |
| **Debug** | OpenAI o1 | OpenAI | Deep reasoning for bugs |
| **Ask** | Ollama Llama 3.2 | Ollama Local | Free local explanations |

---

## 🔧 Implementation Steps

### Phase 1: Configure Providers

#### Step 1: Anthropic (Claude)
**What You'll Need:**
- Your Anthropic API key

**Instructions:**
1. Open Kilo Code settings (Cmd/Ctrl + ,)
2. Search for "Kilo: API Providers"
3. Click "Add Provider"
4. Fill in:
   - **Name:** `Anthropic`
   - **Type:** `Anthropic`
   - **Base URL:** `https://api.anthropic.com`
   - **API Key:** [Paste your key here]
5. Click "Save"
6. Click "Test Connection" to verify

**Test Command:**
```
Ask a simple question in Kilo to test: "What is 2+2?"
```

---

#### Step 2: OpenAI (GPT-4o & o1)
**What You'll Need:**
- Your OpenAI API key

**Instructions:**
1. In Kilo settings, click "Add Provider"
2. Fill in:
   - **Name:** `OpenAI`
   - **Type:** `OpenAI`
   - **Base URL:** `https://api.openai.com/v1`
   - **API Key:** [Paste your key here]
3. Click "Save"
4. Click "Test Connection"

**Models Available:**
- `gpt-4o` - For coding
- `o1-preview` or `o1-mini` - For debugging

---

#### Step 3: Google Gemini
**What You'll Need:**
- Your Google AI Studio API key

**Instructions:**
1. In Kilo settings, click "Add Provider"
2. Fill in:
   - **Name:** `Google`
   - **Type:** `Google`
   - **Base URL:** `https://generativelanguage.googleapis.com/v1beta`
   - **API Key:** [Paste your key here]
3. Click "Save"
4. Click "Test Connection"

**Models Available:**
- `gemini-1.5-flash` - Fast & cheap
- `gemini-1.5-pro` - More capable

---

#### Step 4: OpenRouter
**What You'll Need:**
- Your OpenRouter API key

**Instructions:**
1. In Kilo settings, click "Add Provider"
2. Fill in:
   - **Name:** `OpenRouter`
   - **Type:** `OpenAI-Compatible`
   - **Base URL:** `https://openrouter.ai/api/v1`
   - **API Key:** [Paste your key here]
3. Click "Save"
4. Click "Test Connection"

**Note:** OpenRouter gives access to many models including MiniMax, DeepSeek, and others. Keep this as a backup.

---

#### Step 5: Qwen
**What You'll Need:**
- Your Qwen API key or endpoint

**Instructions:**
1. In Kilo settings, click "Add Provider"
2. Fill in:
   - **Name:** `Qwen`
   - **Type:** `OpenAI-Compatible` (Qwen uses OpenAI-compatible API)
   - **Base URL:** `https://dashscope.aliyuncs.com/compatible-mode/v1` (or your specific endpoint)
   - **API Key:** [Paste your key here]
3. Click "Save"
4. Click "Test Connection"

**Models Available:**
- `qwen-coder-plus` or `qwen-coder-32b`

---

#### Step 6: MiniMax
**What You'll Need:**
- Your MiniMax API key

**Instructions:**
1. In Kilo settings, click "Add Provider"
2. Fill in:
   - **Name:** `MiniMax`
   - **Type:** `OpenAI-Compatible`
   - **Base URL:** [Your MiniMax endpoint - check MiniMax docs]
   - **API Key:** [Paste your key here]
3. Click "Save"
4. Click "Test Connection"

---

#### Step 7: Ollama (Local)
**What You'll Need:**
- Ollama running on your Mac (`ollama serve`)
- Models downloaded (e.g., `ollama pull llama3.2`)

**Instructions:**
1. Verify Ollama is running: Open Terminal and run `ollama list`
2. In Kilo settings, click "Add Provider"
3. Fill in:
   - **Name:** `Ollama`
   - **Type:** `Ollama` or `OpenAI-Compatible`
   - **Base URL:** `http://localhost:11434/v1` or `http://localhost:11434`
   - **API Key:** `ollama` (not required, but some UIs need a value)
4. Click "Save"
5. Click "Test Connection"

**Models Available:**
- `llama3.2` or `llama3.2:latest`
- Check your downloaded models with `ollama list`

---

### Phase 2: Configure Modes

#### Configure Architect Mode
1. Open Kilo settings
2. Navigate to "Modes" → "Architect"
3. Set:
   - **Provider:** `Anthropic`
   - **Model:** `claude-sonnet-4-5` (or latest Sonnet)
   - **Temperature:** `0.7`
   - **Max Tokens:** `4096`
4. Save changes

---

#### Configure Orchestrator Mode
1. Navigate to "Modes" → "Orchestrator"
2. Set:
   - **Provider:** `Anthropic`
   - **Model:** `claude-sonnet-4-5`
   - **Temperature:** `0.7`
   - **Max Tokens:** `4096`
3. Save changes

---

#### Configure Code Mode
1. Navigate to "Modes" → "Code"
2. Set:
   - **Provider:** `Qwen`
   - **Model:** `qwen-coder-32b` (or `qwen-coder-plus`)
   - **Temperature:** `0.3` (lower for more precise code)
   - **Max Tokens:** `8192`
3. **Optional Backup:**
   - **Secondary Provider:** `OpenAI`
   - **Secondary Model:** `gpt-4o`
4. Save changes

---

#### Configure Debug Mode
1. Navigate to "Modes" → "Debug"
2. Set:
   - **Provider:** `OpenAI`
   - **Model:** `o1-preview` or `o1-mini`
   - **Temperature:** `1.0` (o1 models use different settings)
   - **Max Tokens:** `16384`
3. Save changes

**Note:** o1 models are reasoning-focused and more expensive. Use them specifically for complex debugging.

---

#### Configure Ask Mode
1. Navigate to "Modes" → "Ask"
2. Set:
   - **Provider:** `Ollama`
   - **Model:** `llama3.2` (or whatever you have locally)
   - **Temperature:** `0.7`
   - **Max Tokens:** `2048`
3. **Optional Backup:**
   - **Secondary Provider:** `Google`
   - **Secondary Model:** `gemini-1.5-flash`
4. Save changes

---

### Phase 3: Test Each Configuration

#### Test 1: Architect Mode
1. Switch to Architect mode (Cmd/Ctrl + Shift + P → "Kilo: Switch Mode" → "Architect")
2. Ask: "Create a plan to build a simple todo app"
3. Verify Claude Sonnet 4.5 responds with a structured plan

#### Test 2: Code Mode
1. Switch to Code mode
2. Ask: "Write a Python function to calculate fibonacci numbers"
3. Verify Qwen responds with working code

#### Test 3: Debug Mode
1. Switch to Debug mode
2. Provide a buggy code snippet
3. Ask: "Debug this code and explain the issue"
4. Verify o1 provides systematic debugging

#### Test 4: Ask Mode
1. Switch to Ask mode
2. Ask: "What is the difference between let and const in JavaScript?"
3. Verify Ollama (local) responds quickly

#### Test 5: Orchestrator Mode
1. Switch to Orchestrator mode
2. Give it a multi-step task
3. Verify it breaks down and coordinates the work

---

### Phase 4: Create Final Documentation

Create [`kilo-setup.md`](kilo-setup.md) in workspace root with:

```markdown
# Kilo Code Setup - Configured Providers

**Last Updated:** [DATE]

## Connected Providers

| Provider | Status | Models Available |
|----------|--------|-----------------|
| Anthropic | ✅ Active | claude-sonnet-4-5 |
| OpenAI | ✅ Active | gpt-4o, o1-preview |
| Google | ✅ Active | gemini-1.5-flash, gemini-1.5-pro |
| OpenRouter | ✅ Active | Multiple models |
| Qwen | ✅ Active | qwen-coder-32b |
| MiniMax | ✅ Active | [your model] |
| Ollama | ✅ Active | llama3.2 (local) |

## Mode Configuration

| Mode | Model | Provider | Use Case |
|------|-------|----------|----------|
| Architect | claude-sonnet-4-5 | Anthropic | Planning & design |
| Orchestrator | claude-sonnet-4-5 | Anthropic | Task coordination |
| Code | qwen-coder-32b | Qwen | Writing code |
| Debug | o1-preview | OpenAI | Debugging |
| Ask | llama3.2 | Ollama | Quick questions (free) |

## Switching Between Modes

1. Press `Cmd/Ctrl + Shift + P`
2. Type "Kilo: Switch Mode"
3. Select your desired mode

## Important Notes

- **Costs:** Claude (Architect/Orchestrator) and o1 (Debug) are premium. Use strategically.
- **Local Option:** Ask mode uses free Ollama for most questions
- **Backup:** OpenRouter provides access to additional models if needed
- **API Keys:** Never commit API keys to version control

## Limitations

Things I cannot do without your help:
- Access files outside this workspace
- Create accounts or get API keys for you
- Modify system-level settings on your Mac
- Install software or packages
```

---

## 🎯 Success Criteria

- [ ] All 7 providers configured and tested
- [ ] All 5 modes assigned correct models
- [ ] Each mode tested with a sample task
- [ ] Documentation file created
- [ ] User can switch between modes smoothly

---

## 🚨 Troubleshooting

### Provider Won't Connect
- Verify API key is correct (no extra spaces)
- Check base URL matches provider's documentation
- Ensure API key has appropriate permissions

### Ollama Not Working
- Run `ollama serve` in Terminal
- Verify with `ollama list` that models are downloaded
- Check `http://localhost:11434` is accessible

### Model Not Found
- Check provider's documentation for exact model names
- Some providers use different naming (e.g., `claude-3-5-sonnet-20241022` vs `claude-sonnet-4-5`)
- Verify your API key has access to that model

### Mode Switch Not Working
- Restart VS Code
- Check Kilo extension is updated to latest version
- Verify mode configuration is saved

---

## 📝 Next Steps

Once all providers are configured:
1. Test each mode with real work
2. Adjust temperature/token settings based on results
3. Set up keyboard shortcuts for quick mode switching
4. Consider creating custom modes for specialized tasks

---

**Ready to implement?** Start with Phase 1, Step 1 (Anthropic) and work through each provider systematically. Test after each one before moving to the next.