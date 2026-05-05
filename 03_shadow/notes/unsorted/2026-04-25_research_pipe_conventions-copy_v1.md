---
title: Research Pipe File Structure & Conventions
author: Ewan + Solace
date: 2026-04-14
status: locked
---

# RESEARCH_PIPE_CONVENTIONS.md

## File Naming Convention

**Pattern:** `{purpose}_{subsystem}.py` or `{purpose}_{type}.md`

AI reads the filename and knows exactly what it does. No guessing.

### Code Files (Python)
- `orchestrator_research_pipe.py` — THE entry point, orchestrates all five stages
- `intake_research_pipe.py` — Stage 1: question intake and metadata extraction
- `interpreter_research_pipe.py` — Stage 2: language neutralization and analysis
- `curator1_research_pipe.py` — Stage 3: search design (Boolean query generation)
- `search_research_pipe.py` — Stage 4: execute queries (Exa + arXiv parallel)
- `curator2_research_pipe.py` — Stage 5: sufficiency check + synthesis + Pudding Technique
- `config_research_pipe.py` — Centralized: API keys, model names, endpoints, paths
- `audit_research_pipe.py` — JSON logging and audit trail management

### Template/Prompt Files (Markdown)
- `template_intake_questions.md` — The four gates (what, why, how, fallback)
- `template_curator1_prompt.md` — Search design spec (three-pass strategy)
- `template_curator2_prompt.md` — Sufficiency check + synthesis spec

### Documentation Files (SCREAMING_CASE.md)
- `RESEARCH_PIPE_SPEC.md` — Full system design and five-stage protocol
- `RESEARCH_PIPE_CONVENTIONS.md` — THIS FILE: naming, paths, where things go
- `RESEARCH_PIPE_BATON_PASS.md` — Handoff notes between sessions

### Output Files
- `output_audit_trails/` — Directory for execution logs only
  - Format: `YYYYMMDD_HHMMSS_question_slug.json`
  - Example: `20260414_102300_persuasion_ethics.json`

### Configuration
- `.env` — Secrets and API keys (never commit, never in Git)

---

## Where Things Go

| Type | Location | Purpose |
|------|----------|---------|
| Logic | `{purpose}_research_pipe.py` | Modular stage implementation |
| Config | `config_research_pipe.py` | API keys, models, endpoints, paths (singleton) |
| Logging | `audit_research_pipe.py` | JSON trail generation |
| Templates | `template_{thing}.md` | Input prompts and intake structure |
| Specs | `RESEARCH_PIPE_*.md` | System design and conventions (locked docs) |
| Outputs | `output_audit_trails/` | JSON execution trails (query results, verdicts, synthesis) |
| Secrets | `.env` | Never committed, loaded at runtime |

---

## Import Pattern

All stage modules import config:
```python
from config_research_pipe import get_config
config = get_config()
```

The orchestrator imports all stages:
```python
from intake_research_pipe import stage_intake
from interpreter_research_pipe import stage_interpreter
# ... etc
```

Audit trail is managed in orchestrator:
```python
from audit_research_pipe import AuditTrail
audit = AuditTrail()
audit.log("STAGE_NAME", data)
audit.save(question_slug)
```

---

## Execution

```bash
cd ~/amplified
python orchestrator_research_pipe.py "What methodologies measure persuasion?" "Strategy" "psychology"
```

Output:
1. Console: Progress (stages, result counts, verdict)
2. JSON file: Full audit trail saved to `output_audit_trails/`
3. Stdout: Final Curator 2 output (sufficiency check + synthesis)

---

## Locked Rules

1. **File names scream purpose.** AI navigates by reading the filename.
2. **One module, one stage.** No god files.
3. **Config is centralized.** No scattered environment variables.
4. **All output is JSON.** No markdown in data, only specs.
5. **Audit trails are immutable.** Write once, never edit. Full traceability.
6. **Imports are explicit.** No circular dependencies. Stages don't import each other.

---

**Locked:** April 14, 2026, 10:47 AM
**By:** Ewan + Solace

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd
