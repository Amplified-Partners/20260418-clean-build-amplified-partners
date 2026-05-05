---
title: "Section 3 Review & Adjusted Plan"
id: "section_3_review_and_plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Section 3 Review & Adjusted Plan

**Date:** 2024-12-16  
**Status:** Planning Phase

---

## Self-Review of Sections 1 & 2

### What's Working Well

1. **PRINCIPLES.md** - Solid foundation
   - 10 evidence-based principles with research citations
   - Clear code references
   - Audit checklist for violations
   - **Assessment:** Ready for use ✓

2. **Obsidian Integration** - Functional
   - Writes to Daily folder directly
   - Appends to existing notes
   - **Assessment:** Ready for testing ✓

3. **UX Refinement** - Modern & Calm
   - Apple glass aesthetic achieved
   - Material backgrounds, soft shadows
   - Collapsible summary panel
   - **Assessment:** Needs real device testing ⚠️

4. **PERSONAS.md** - Comprehensive
   - 4 distinct behavioral patterns
   - Evidence-based, not proprietary
   - Clear simulation parameters
   - **Assessment:** Ready for implementation ✓

### Gaps Identified

1. **No Xcode Project File**
   - All Swift code exists but can't be built yet
   - User needs to create project in Xcode GUI
   - **Impact:** Can't test anything until this is done

2. **No Unit Tests Yet**
   - Core logic untested
   - 3-task limit enforcement unverified
   - Mode validation unverified
   - **Impact:** High risk of bugs

3. **No Simulation Engine**
   - Personas defined but not executable
   - Can't validate behavioral patterns
   - **Impact:** Can't prove system works as intended

4. **LLM Configuration**
   - Currently hardcoded to qwen2.5-coder:14b
   - User mentions DeepSeek and MiniMax options
   - **Impact:** Need flexible model selection

---

## LLM Model Strategy

### Current State
- Hardcoded: `qwen2.5-coder:14b` in ConfigService.swift
- Single model, no fallback

### User's Request
> "I want to add the best visions of deep seek into the mix... there's two visions and and/or a mini max"

### Recommended Approach

**Option A: Multi-Model Ensemble (Best Quality)**
- Use DeepSeek for task extraction (strong reasoning)
- Use MiniMax for natural language understanding
- Fallback to qwen2.5-coder if others unavailable
- **Pros:** Best results, redundancy
- **Cons:** More complex, slower

**Option B: Configurable Single Model (Simplest)**
- Let user choose preferred model in config.json
- Support: DeepSeek, MiniMax, qwen2.5-coder, llama
- **Pros:** Simple, fast, user control
- **Cons:** No ensemble benefits

**Option C: Smart Routing (Balanced)**
- Route by task type:
  - Complex reasoning → DeepSeek
  - Natural language → MiniMax
  - Quick tasks → qwen2.5-coder
- **Pros:** Optimal for each use case
- **Cons:** Requires routing logic

### My Recommendation: **Option B** for v1

**Reasoning:**
1. Simplest to implement and test
2. User maintains full control
3. Easy to upgrade to Option C later
4. Aligns with "100% local" principle

**Implementation:**
```swift
// ConfigService.swift
struct AppConfig: Codable {
    var llmModel: String  // "deepseek-chat", "minimax", "qwen2.5-coder:14b"
    var llmFallbackModel: String?  // Optional fallback
}
```

---

## Adjusted Section 3 Plan

### Phase 1: Foundation (2 hours)
**Priority: HIGH - Blocks everything else**

1. **Update LLM Configuration**
   - Add model selection to ConfigService
   - Support: DeepSeek, MiniMax, qwen2.5-coder, llama
   - Add fallback model option
   - Update LLMService to use configured model

2. **Create Unit Test Framework**
   - Set up XCTest target
   - Test 3-task limit enforcement
   - Test mode validation rules
   - Test storage round-trip
   - Test summary factuality (no guilt/praise)

### Phase 2: Simulation Engine (3 hours)
**Priority: MEDIUM - Validates behavioral design**

1. **Build SimulationEngine.swift**
   - Implement 4 persona behaviors
   - Generate tasks per persona profile
   - Simulate completion/archive decisions
   - Call real summary generation logic
   - Track metrics per persona

2. **Create Report Generator**
   - Markdown reports per persona
   - Aggregate statistics
   - Principle violation detection
   - Pattern analysis

### Phase 3: Automation (1 hour)
**Priority: LOW - Nice to have**

1. **Create run-simulations.sh**
   - Run all unit tests
   - Run all persona simulations
   - Generate dated report
   - Log to REPORTS/overnight-log.txt

2. **Add Safeguards**
   - Max runtime: 8 hours
   - Max iterations: 1000
   - Stop on critical errors
   - No file operations outside project

### Phase 4: Overnight Execution (8 hours unattended)
**What runs:**
- All unit tests (repeated)
- 4 personas × 90 days = 360 simulated days
- Report generation
- Principle violation checks

**What doesn't run:**
- No new features
- No refactoring
- No external API calls
- No system modifications

---

## Revised Timeline

**Tonight (supervised):**
- Phase 1: 2 hours (LLM config + unit tests)
- Phase 2: 3 hours (simulation engine)
- Phase 3: 1 hour (automation script)
- **Total: 6 hours supervised**

**Overnight (unattended):**
- Phase 4: 8 hours (run simulations)
- **Total: 8 hours unattended**

**Morning deliverable:**
- Test results summary
- Simulation findings per persona
- Principle violation report
- Recommended fixes (if any)

---

## Cost Estimate

**Supervised work (6 hours):**
- Coding: ~£120 (6 hrs × £20/hr average)
- Testing: Included

**Overnight (8 hours):**
- Automated: ~£40 (minimal token use, mostly compute)

**Total: ~£160** (slightly over £150 but within reason for comprehensive testing)

---

## Risk Assessment

### Low Risk
- ✅ LLM configuration changes (simple)
- ✅ Unit tests (standard practice)
- ✅ Simulation engine (isolated code)

### Medium Risk
- ⚠️ Overnight automation (needs safeguards)
- ⚠️ Report generation (file I/O)

### High Risk
- ❌ None identified

### Mitigation
- All changes in isolated files
- No modifications to core app logic
- Comprehensive error handling
- Runtime limits and safeguards

---

## Decision Points

### 1. LLM Model Strategy
**Question:** Which approach for multi-model support?
**Recommendation:** Option B (configurable single model)
**Rationale:** Simplest, user control, easy to upgrade later

### 2. Simulation Scope
**Question:** 30 days or 90 days per persona?
**Recommendation:** 90 days (360 total)
**Rationale:** Better pattern detection, validates long-term trajectories

### 3. Overnight Automation
**Question:** Run tonight or wait for review?
**Recommendation:** Run tonight with safeguards
**Rationale:** Maximizes progress, safeguards prevent issues

---

## Next Steps

**Immediate (awaiting your approval):**
1. Implement Phase 1 (LLM config + unit tests)
2. Implement Phase 2 (simulation engine)
3. Implement Phase 3 (automation script)
4. Set up overnight run with safeguards

**Your input needed:**
1. **LLM Model Preference:** DeepSeek, MiniMax, or both?
2. **Simulation Duration:** 30 days or 90 days per persona?
3. **Overnight Approval:** Proceed with automated overnight run?

---

## Conclusion

**Current Status:** Sections 1 & 2 complete, ready for Section 3

**Recommendation:** Proceed with adjusted Section 3 plan using configurable LLM model selection (Option B) and 90-day simulations.

**Confidence Level:** High - plan is well-scoped, risks are mitigated, deliverables are clear.

**Awaiting your approval to proceed.**