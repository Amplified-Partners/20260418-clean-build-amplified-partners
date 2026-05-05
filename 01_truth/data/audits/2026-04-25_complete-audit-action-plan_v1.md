---
title: "Complete AI Software Audit - Action Plan"
id: "complete-audit-action-plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Complete AI Software Audit - Action Plan

**Purpose:** Step-by-step guide to complete the audit and gather all missing information

---

## Phase 1: Information Gathering (Do This First)

### 1.1 Check Bloom Installation & Models

```bash
# Find Bloom application
open -a Bloom

# Or check if installed
ls -la /Applications/ | grep -i bloom

# Check Bloom data directory (common locations)
ls -la ~/Library/Application\ Support/Bloom/
ls -la ~/.bloom/
ls -la ~/.config/bloom/

# Find all Bloom-related files
find ~ -name "*bloom*" -type d 2>/dev/null | head -20

# Check disk usage
du -sh ~/Library/Application\ Support/Bloom/ 2>/dev/null
```

**What to document:**
- Version number
- Installed models (list names and sizes)
- Total disk usage
- Default settings

### 1.2 Check Comet Installation & Purpose

```bash
# Find Comet application
open -a Comet

# Check if installed
ls -la /Applications/ | grep -i comet

# Check Comet data directory
ls -la ~/Library/Application\ Support/Comet/
ls -la ~/.comet/

# Find all Comet-related files
find ~ -name "*comet*" -type d 2>/dev/null | head -20
```

**What to document:**
- What Comet is used for (LLM runner, image gen, other?)
- Version and configuration
- Disk usage
- Is it different from Bloom?

### 1.3 Locate All API Keys

```bash
# Search for .env files
find ~ -name ".env" -type f 2>/dev/null

# Search for API key patterns (careful - don't expose keys)
grep -r "OPENAI_API_KEY\|ANTHROPIC_API_KEY\|CLAUDE_API_KEY" ~/.config/ ~/.local/ ~/Documents/ 2>/dev/null | grep -v ".git"

# Check common config locations
ls -la ~/.config/openai/
ls -la ~/.config/anthropic/
ls -la ~/.aws/credentials
cat ~/.zshrc | grep -i "API_KEY"
cat ~/.bashrc | grep -i "API_KEY"

# Check VSCode settings
cat ~/Library/Application\ Support/Code/User/settings.json | grep -i "api"
```

**What to document:**
- Location of each API key file
- Which services you have keys for
- Which tools use which keys

### 1.4 Check API Usage & Costs

**OpenAI:**
```bash
# Visit: https://platform.openai.com/usage
# Or use API:
curl https://api.openai.com/v1/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Anthropic:**
```bash
# Visit: https://console.anthropic.com/settings/usage
# Check monthly spend
```

**Google Gemini:**
```bash
# Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
# Check usage metrics
```

**What to document:**
- Last month's spend per provider
- Current month's spend so far
- Usage patterns (which days/times)

### 1.5 Check Local LLM Models

```bash
# If using Ollama
ollama list 2>/dev/null

# If using LM Studio
ls -la ~/Library/Application\ Support/LM\ Studio/models/ 2>/dev/null

# If using Jan
ls -la ~/Library/Application\ Support/jan/models/ 2>/dev/null

# General search for model files
find ~ -name "*.gguf" -o -name "*.safetensors" 2>/dev/null | head -20

# Check total disk usage of models
du -sh ~/Library/Application\ Support/*/models/ 2>/dev/null
```

**What to document:**
- All installed models
- Model sizes
- Total storage used
- Which models you actually use

---

## Phase 2: Tool Usage Analysis

### 2.1 Track Kilo Code Mode Usage

Create a usage tracking script:

```bash
# Save this as: track-kilo-usage.sh
#!/bin/bash

# Analyze Kilo Code logs (adjust path as needed)
LOG_FILE="$HOME/.kilocode/logs/usage.log"

if [ -f "$LOG_FILE" ]; then
    echo "=== Kilo Code Mode Usage ==="
    echo "Most used modes:"
    grep "mode:" "$LOG_FILE" | awk '{print $NF}' | sort | uniq -c | sort -rn
    
    echo -e "\n=== API Calls ==="
    grep "api_call" "$LOG_FILE" | wc -l
    
    echo -e "\n=== Costs ==="
    grep "cost:" "$LOG_FILE" | awk '{sum += $NF} END {print "Total: $" sum}'
else
    echo "Log file not found. Enable logging in Kilo Code settings."
fi
```

Run it:
```bash
chmod +x track-kilo-usage.sh
./track-kilo-usage.sh
```

### 2.2 MCP Server Usage Check

```bash
# Check which MCP servers are actually running
ps aux | grep -i "mcp\|puppeteer\|memory"

# Check MCP server logs (adjust paths)
ls -la ~/.mcp/logs/
tail -n 50 ~/.mcp/logs/*.log

# Count MCP tool calls (if logged)
grep "mcp_tool" ~/.kilocode/logs/*.log 2>/dev/null | wc -l
```

### 2.3 Knowledge Tool Overlap Analysis

```bash
# Check Obsidian vault size
du -sh ~/Documents/Obsidian\ Vault/ 2>/dev/null

# Check Notion local cache
du -sh ~/Library/Application\ Support/Notion/ 2>/dev/null

# Check Memory MCP database size
du -sh ~/.mcp/memory/ 2>/dev/null

# Count files in each
find ~/Documents/Obsidian\ Vault/ -type f 2>/dev/null | wc -l
```

---

## Phase 3: Cost Optimization Analysis

### 3.1 Calculate Current Monthly Spend

Create a spreadsheet or use this template:

```
Service              | Monthly Cost | Usage Level | Notes
---------------------|--------------|-------------|------------------
Kilo Code (Claude)   | $___         | ___ requests| Primary coding
OpenAI API           | $___         | ___ requests| ___
Anthropic Direct     | $___         | ___ requests| ___
Google Gemini        | $___         | ___ requests| Agentic workflow
Bloom (Local)        | $0           | N/A         | One-time cost
Comet (Local)        | $0           | N/A         | One-time cost
---------------------|--------------|-------------|------------------
TOTAL                | $___         |             |
```

### 3.2 Identify Redundancies

**Questions to answer:**

1. **Local vs Cloud:**
   - What tasks use Bloom vs cloud APIs?
   - Could any cloud tasks move to local models?
   - Cost savings estimate: $___

2. **Multiple Cloud Providers:**
   - Do you need both OpenAI and Claude?
   - Which performs better for your use cases?
   - Consolidation savings: $___

3. **MCP Servers:**
   - Which servers haven't been used in 30 days?
   - Can any be disabled temporarily?
   - Resource savings: ___

4. **Knowledge Tools:**
   - Obsidian vs Notion vs Memory MCP - can you pick one?
   - What's unique about each?
   - License cost savings: $___

---

## Phase 4: Create Optimization Scripts

### 4.1 Cost Monitoring Script

```bash
# Save as: monitor-ai-costs.sh
#!/bin/bash

REPORT_FILE="ai-costs-$(date +%Y-%m).txt"

echo "AI Software Cost Report - $(date)" > $REPORT_FILE
echo "=================================" >> $REPORT_FILE

# Check OpenAI
echo -e "\n[OpenAI]" >> $REPORT_FILE
curl -s https://api.openai.com/v1/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY" | \
  jq '.data[0].cost' >> $REPORT_FILE 2>/dev/null || echo "Not configured"

# Check Anthropic (manual - add your API call)
echo -e "\n[Anthropic]" >> $REPORT_FILE
echo "Check: https://console.anthropic.com/settings/usage" >> $REPORT_FILE

# Check disk usage
echo -e "\n[Local Models Disk Usage]" >> $REPORT_FILE
du -sh ~/Library/Application\ Support/Bloom/ 2>/dev/null >> $REPORT_FILE
du -sh ~/Library/Application\ Support/Comet/ 2>/dev/null >> $REPORT_FILE

cat $REPORT_FILE
```

### 4.2 MCP Server Health Check

```bash
# Save as: check-mcp-servers.sh
#!/bin/bash

echo "=== MCP Server Status ==="

# Check if servers are running
echo -e "\n[Sequential Thinking]"
pgrep -f "sequential-thinking" && echo "✓ Running" || echo "✗ Stopped"

echo -e "\n[Project Agent]"
pgrep -f "project-agent" && echo "✓ Running" || echo "✗ Stopped"

echo -e "\n[Research Agent]"
pgrep -f "research-agent" && echo "✓ Running" || echo "✗ Stopped"

echo -e "\n[Puppeteer]"
pgrep -f "puppeteer" && echo "✓ Running" || echo "✗ Stopped"

echo -e "\n[Memory]"
pgrep -f "server-memory" && echo "✓ Running" || echo "✗ Stopped"
```

### 4.3 Model Cleanup Script

```bash
# Save as: cleanup-unused-models.sh
#!/bin/bash

echo "=== Finding Unused AI Models ==="
echo "This script finds models older than 30 days with no recent access"

# Find large model files not accessed in 30 days
find ~ -name "*.gguf" -o -name "*.safetensors" -atime +30 2>/dev/null | while read file; do
    size=$(du -h "$file" | cut -f1)
    echo "Unused: $file ($size)"
done

echo -e "\nWould you like to remove these? (Review carefully first)"
```

---

## Phase 5: Implementation Plan

Once you've gathered all data, create this action plan:

### 5.1 Quick Wins (Do This Week)

- [ ] Disable unused MCP servers
- [ ] Set API budget alerts ($XXX/month)
- [ ] Remove 1 unused local model
- [ ] Consolidate to 1 knowledge tool

**Expected savings:** $___/month

### 5.2 Medium-term (This Month)

- [ ] Migrate X tasks from cloud to local models
- [ ] Cancel unused API subscriptions
- [ ] Implement response caching
- [ ] Set up cost monitoring dashboard

**Expected savings:** $___/month

### 5.3 Long-term (This Quarter)

- [ ] Evaluate provider consolidation
- [ ] Implement usage-based routing (local vs cloud)
- [ ] Create cost allocation tracking
- [ ] Regular quarterly review

**Expected savings:** $___/month

---

## Phase 6: Security Hardening

### 6.1 API Key Rotation Schedule

```bash
# Create a key rotation tracker
cat > api-key-rotation.md << 'EOF'
# API Key Rotation Schedule

| Provider | Current Key Created | Last Rotated | Next Rotation | Status |
|----------|-------------------|--------------|---------------|--------|
| OpenAI   | YYYY-MM-DD        | YYYY-MM-DD   | YYYY-MM-DD    | ⚠️ Due |
| Anthropic| YYYY-MM-DD        | YYYY-MM-DD   | YYYY-MM-DD    | ✓ OK   |
| Gemini   | YYYY-MM-DD        | YYYY-MM-DD   | YYYY-MM-DD    | ✓ OK   |

Rotation Policy: Every 90 days
EOF
```

### 6.2 Centralized Secrets Management

**Option 1: Use a secrets manager**
```bash
# Install pass (Unix password manager)
brew install pass

# Initialize
pass init your-gpg-key-id

# Store keys
pass insert ai/openai-key
pass insert ai/anthropic-key
pass insert ai/gemini-key

# Retrieve in scripts
export OPENAI_API_KEY=$(pass show ai/openai-key)
```

**Option 2: Use .env files (simpler)**
```bash
# Create centralized .env
cat > ~/.ai-secrets.env << 'EOF'
# AI API Keys - DO NOT COMMIT
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
EOF

chmod 600 ~/.ai-secrets.env

# Source in your scripts
source ~/.ai-secrets.env
```

---

## Phase 7: Reporting & Monitoring

### 7.1 Monthly Review Template

```markdown
# AI Software Monthly Review - [Month Year]

## Costs This Month
- Total: $___
- vs Last Month: +/- $___
- vs Budget: $___

## Usage Breakdown
- Kilo Code: ___ requests
- OpenAI: ___ requests  
- Gemini: ___ requests
- Local Models: ___ hours

## What Worked
- ___
- ___

## What to Optimize
- ___
- ___

## Actions for Next Month
- [ ] ___
- [ ] ___
```

### 7.2 Automated Weekly Report

```bash
# Save as: weekly-ai-report.sh
#!/bin/bash

cat << EOF
=== Weekly AI Software Report ===
Generated: $(date)

[Last 7 Days Activity]
- Kilo Code sessions: $(grep -c "session_start" ~/.kilocode/logs/*.log 2>/dev/null)
- MCP tool calls: $(grep -c "mcp_tool" ~/.kilocode/logs/*.log 2>/dev/null)
- Estimated cost: $$(grep "cost:" ~/.kilocode/logs/*.log 2>/dev/null | awk '{sum += $NF} END {print sum}')

[Active Services]
$(./check-mcp-servers.sh)

[Disk Usage]
- Local models: $(du -sh ~/Library/Application\ Support/*/models/ 2>/dev/null | awk '{sum+=$1} END {print sum}')GB

Next Review: $(date -v +7d)
EOF
```

Run weekly:
```bash
chmod +x weekly-ai-report.sh
./weekly-ai-report.sh | tee reports/week-$(date +%V).txt
```

---

## Deliverables Checklist

Complete these and return the results:

### Data Collection
- [ ] Bloom models list with sizes
- [ ] Comet purpose and usage
- [ ] All API key locations documented
- [ ] Last 3 months costs per provider
- [ ] Local model inventory with sizes
- [ ] Kilo Code mode usage statistics
- [ ] MCP server usage frequency
- [ ] Knowledge tool usage patterns

### Analysis
- [ ] Total monthly cost calculated
- [ ] Redundancies identified
- [ ] Quick win opportunities listed
- [ ] Long-term optimization plan created
- [ ] Security gaps identified

### Implementation
- [ ] Cost monitoring script running
- [ ] MCP health check automated
- [ ] API key rotation scheduled
- [ ] Weekly reporting automated
- [ ] Budget alerts configured

---

## Next Steps

1. **Run all Phase 1 commands** - Gather missing data
2. **Fill in the cost spreadsheet** - Get actual numbers
3. **Create the tracking scripts** - Automate monitoring
4. **Share results with me** - I'll create specific optimizations
5. **Implement quick wins** - Start saving immediately

---

## Questions to Answer

After running these commands, please provide:

1. **Bloom:**
   - Models installed: [list]
   - Total size: [GB]
   - Usage frequency: [daily/weekly/rarely]

2. **Comet:**
   - Purpose: [what it does]
   - Different from Bloom?: [yes/no]
   - Keep or remove?: [decision]

3. **API Costs:**
   - OpenAI last month: $___
   - Anthropic last month: $___
   - Gemini last month: $___

4. **Priorities:**
   - Main goal: [cost reduction / performance / both]
   - Keep local models?: [yes/no]
   - Willing to switch providers?: [yes/no]

5. **Quick Wins:**
   - Which MCP servers can we disable?: [list]
   - Which knowledge tool is primary?: [Obsidian/Notion/Memory]
   - Unused models to remove?: [list]

---

## Support Scripts Location

I recommend creating this directory structure:

```
~/ai-audit/
├── scripts/
│   ├── monitor-ai-costs.sh
│   ├── check-mcp-servers.sh
│   ├── cleanup-unused-models.sh
│   ├── track-kilo-usage.sh
│   └── weekly-ai-report.sh
├── reports/
│   ├── week-XX.txt
│   └── monthly-YYYY-MM.txt
├── data/
│   ├── api-costs.csv
│   ├── model-inventory.csv
│   └── usage-stats.csv
└── plans/
    ├── optimization-plan.md
    └── implementation-checklist.md
```

Create it with:
```bash
mkdir -p ~/ai-audit/{scripts,reports,data,plans}
cd ~/ai-audit