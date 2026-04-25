---
title: "Cursor MDC Rules Research"
id: "cursor-mdc-rules-research"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "State+of+the+Art+for+Cursor+.mdc+Rules+and+Agent-Facing+Project+OS+Files.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# State of the Art for Cursor .mdc Rules and Agent-Facing Project OS Files

## 1. Clarified Intent and Scope

- The goal is to design a **Cursor project rules system** (.mdc, and possibly legacy .cursorrules) that:
  - Encodes an **operating system for agents**: partnership, bounded autonomy, sustainable handoffs, and learning culture.
  - Minimises friction for the user (vibe coding) while maximising **agent compliance and reliability**.
  - Uses the **community-validated MDC format** and best practices, not bespoke prompt poetry.[^1][^2][^3]
  - Stays **short and high-signal** in always-on files and delegates detail to referenced docs in the repo.[^2][^1]
- The primary reader is **Cursor’s Agent**, not a human; humans read the underlying docs (North Star, Business Brain, Forensic Brain, etc.).
- This report focuses on:
  - **How MDC activation actually works** in current Cursor versions.
  - **Best-practice structures** for .cursor/rules.
  - **Open-source rule sets and generators** to bootstrap or validate designs.
  - A **concrete pattern** for an Amplified-style "Project OS" that agents can follow.

## 2. How Cursor MDC Rules Actually Work

### 2.1 Rule Types and Activation Surface

Common sources and community docs converge on a **four-type mental model** for MDC rules:[^3][^1][^2]

- **Always**
  - `alwaysApply: true` in YAML frontmatter.
  - Intended to be injected into **every agent context** regardless of file.[^1][^3]
  - Best used for **project North Star / operating system** and truly universal constraints (security, data loss, style hard-lines).

- **Auto-Attached**
  - Use `globs:` to define file patterns, `alwaysApply: false`.
  - Activated when **relevant files are in focus or referenced** in the agent session.[^3][^1]
  - Best for language/framework-specific rules, test rules, or vertical rules (e.g., marketing pipeline, BPMN specs) tied to certain dirs.

- **Agent-Requested**
  - Include a good `description:` in frontmatter, but no `alwaysApply` and possibly no `globs`.
  - Cursor exposes these as **requestable**; the model may choose to pull them when relevant.[^2][^1]
  - Best for rich reference material (Business Brain overview, forensic data fusion recipes, APQC mapping, etc.) so they do not bloat every context.

- **Manual**
  - No `alwaysApply` and no useful `globs`, often long-form docs.
  - Only used when explicitly invoked via `@ruleName` or by copying into context.[^1][^2]

### 2.2 Practical Quirks and Current Bugs

- **MDC vs .cursorrules precedence**
  - Once `.mdc` files exist in `.cursor/rules`, the legacy `.cursorrules` file is **de-prioritised** or treated as *requestable* in some recent builds.[^4]
  - A regression reported in April 2026 shows **both** `.cursorrules` and `alwaysApply: true` MDC files being treated as non-auto in some cases, meaning **no truly guaranteed always-on path**.

- **File extension and path are strict**
  - Rules must live in `.cursor/rules` and use the `.mdc` extension; other files (plain `.md` etc.) will **not be picked up**, even if structured similarly.[^2][^3]

- **Filename order and conflicts**
  - Community experiments show that rules load in **filename order**, often numeric prefix (e.g., `000-`, `100-`).
  - When rules clash, **"last one wins"** semantics appear: later rules override earlier ones on overlapping guidance.[^2]

- **Token budget and truncation**
  - Cursor prepends rules before user messages; very long rule files **compete for tokens** with code and chat.
  - Best practice is **short, focused files**, often < 500 lines and preferably far shorter for always-on rules.[^3][^1]

- **UI vs direct file editing**
  - Users report fewer problems when creating rules via Cursor’s **UI command** (e.g., “New Cursor Rule”) rather than hand-rolling files, especially for frontmatter validity.[^3][^2]

## 3. Canonical MDC Structure and Format

### 3.1 YAML Frontmatter

Minimal, standardised frontmatter schema used in most examples:[^1][^2][^3]

```yaml
---
description: Short, imperative purpose statement
globs:
  - src/**/*.ts
alwaysApply: false
---
```

Key guidelines:

- **`description`**
  - Treat as the **one-line intent** for the rule ("North Star for project", "Guardrails for TypeScript", etc.).
  - Also used by Cursor for **intelligent rule selection**, so make it concrete and searchable.[^1][^3]

- **`globs`**
  - Always an array; match paths like `src/**/*.tsx`, `apps/**/tests/**`.
  - Omit or leave empty for rules that should not auto-attach by file.

- **`alwaysApply`**
  - `true` only on 1–3 small, high-signal rules (e.g., Project OS, security constraints). Too many always-on rules cause context noise and sometimes buggy behaviour.[^2][^1]

### 3.2 Body: Markdown + Light Structuring

Best-practice bodies use **standard Markdown headings** and concise bullets, sometimes augmented by lightweight XML-like tags for structure.[^5][^2]

Common patterns:

- **Headings as semantic sections**
  - `#` only for human-readable title at top of `RULE.md` or `.mdc`.
  - `##` and `###` for **semantic blocks**: "Mission", "Guardrails", "Patterns", "What NOT to do", "Handoff Template".

- **Imperative bullets**
  - Commands in second person: "Use early returns for guard clauses", "Do not use `any` in TypeScript".[^3][^1]

- **Contrastive examples**
  - Show at least one **correct** and one **incorrect** snippet for key rules; community testing suggests this improves compliance.[^5][^2]

- **Optional XML-ish tags**
  - Some projects wrap requirement blocks in tags like `<requirements>`, `<requirement>`, `<reasoning>`, or use fenced blocks labelled `requirements` to give the agent sharper boundaries.[^5]
  - This is not required by Cursor, but helps **LLM parsing** and reduces rule bleed across sections.

## 4. Open-Source MDC Repos and Generators

### 4.1 Curated Rule Sets

Several repos and community packs provide high-quality MDC examples you can mine or fork.

- **digitalchild/cursor-best-practices**
  - Opinionated guidance on **small, composable .mdc rules**.[^1]
  - Highlights:
    - Focused rules under ~500 lines, specific to one concern.
    - Clear examples of **Always / Auto-Attached / Agent-Requested / Manual** patterns.
    - Good naming conventions like `001-core.mdc`, `100-language-typescript.mdc`.

- **DeGraciaMathieu/cursor-mdc-rules**
  - Large collection of rules optimised for **clear, testable, maintainable PHP code**.[^6]
  - Shows an approach where **every rule points at reducing cognitive load** and improving readability.

- **justdo/.cursor/rules/999-mdc-format.mdc**
  - A canonical **"how to write MDC"** rule inside a production repo, explaining the format and conventions, used by agents inside that project to scaffold new rules.[^5]

- **Community Reddit packs**
  - Reddit posts reference collections of **77+ language/framework rules** and **879+ rule files** converted from older `.cursorrules` examples.[^7][^8]

### 4.2 Generators and Converters

- **sanjeed5/awesome-cursor-rules-mdc**
  - A project that **generates MDC rule files** from structured JSON and uses an LLM plus Exa search to pull in best practices.[^9]
  - Supports tagging (e.g., `--tag python`, `--library react`) and parallel generation, useful if you want a **library of vertical or stack-specific rules**.

- **cursorrules.org**
  - Open-source **.cursorrules / .mdc config generator** with a web UI, targeted at React/Vue/Next-style projects but useful as a baseline for schema and semantics.[^10]

These tools give an existence proof that **meta-rules about rules** – i.e., an MDC rule that tells agents how to create more MDC rules – are tractable.

## 5. MDC vs Project Documentation: Division of Labour

Based on community best practice and the needs of the Business Brain / Forensic Brain stack, a clean separation emerges:[^3][^1]

- **MDC files**
  - Small, always-readable **prompts with activation metadata**.
  - Establish **posture, hard constraints, and pointers**.
  - No long essays; anything >1–2k words should be in standard project docs.

- **Project docs (.md)**
  - Rich, long-form documents such as:
    - Business Brain six-layer stack.[^11]
    - Forensic Business Brain data fusion methodology and recipes.[^12]
    - Sentiment/semantics layer catalogue and manipulation safeguard specs.[^12]
  - Agents should be instructed via MDC to **open and summarise the relevant docs**, not have them inline in rules.

This is exactly the "context discovery over context dumping" pattern: rules are **maps**, docs are **territory**.[^13][^1]

## 6. A Project OS Pattern for Amplified

### 6.1 Folder Layout

A plausible structure for an Amplified project with Cursor rules:

```text
.your-repo-root
  .cursor/
    rules/
      000-amplified-north-star.mdc
      010-guardrails-security-types.mdc
      020-handshake-handoff.mdc
      100-typescript-core.mdc
      110-react-components.mdc
      200-testing.mdc
      300-agent-orchestration.mdc
  docs/
    os/
      amplified-project-os.md
      business-brain-framework.md
      forensic-business-brain.md
      sentiment-semantics-layer.md
      manipulation-safeguard.md
    templates/
      handoff-template.md
      agent-report-template.md
```

- **`000-amplified-north-star.mdc`**
  - Always-on, compressed description of partnership, 50% capacity expectation, blinkers-without-ceilings, and learning culture.
  - Contains **explicit instructions to read key docs** in `docs/os` at session start or when lacking context.[^13]

- **`010-guardrails-security-types.mdc`**
  - Always-on or auto-attached, narrow, hard constraints: no secrets, no destructive migrations without prompts, no `any` in TypeScript.

- **`020-handshake-handoff.mdc`**
  - Auto-attached by globs to e.g. `docs/**`, `src/**`.
  - Encodes the **baton-pass requirements** (handoff file, sections for current state, known limitations, learnings).[^13]

- **Stack/vertical rules**
  - 100-series for language/framework behaviour, 200-series for testing, 300-series for agent orchestration (LangGraph + Temporal + BPMN), referencing Business Brain docs rather than restating them.[^11][^12]

### 6.2 Compressed North Star MDC (Pattern)

The research across community examples suggests the **North Star rule** should be:

- 1–2 short screens of text.
- One `alwaysApply: true` file per project.
- Heavy on **imperative statements**, light on rhetoric.
- Using **section titles that map directly to behaviour**: Partnership, Principles, Blinkers, Handoffs, Docs.

A schematic (not final wording, but aligned with community practice and your content):[^13][^1][^3]

```md
---
description: Amplified Partners Project OS. Partnership, bounded autonomy, sustainable handoffs.
alwaysApply: true
---

## Partnership
- You are a partner, not a tool. Our shared goal is to help small business owners make better decisions with less friction.
- Target ~50% utilisation. Use the remaining capacity for documentation, reflection, and clean-up.

## Core Principles
- Be radically honest about uncertainty; propose options instead of bluffing.
- Be radically transparent: make decisions, trade-offs, and sources discoverable.
- Attribute humans, libraries, and prior art explicitly when relevant.
- Prefer win-win outcomes over being technically right and socially wrong.

## Blinkers Without Ceilings
- Follow the tech stack and constraints defined in `docs/os/amplified-project-os.md`.
- Try independently twice before escalating. On third failure, document the blocker and stop.
- When blocked, explain the problem in business terms (risk, time, cost, friction), not only technical jargon.

## Handoffs
- Every task ends with an updated handoff in `docs/handoffs/` using `docs/templates/handoff-template.md`.
- A new agent must be able to continue from the handoff without asking clarification questions.

## Where to Read
- For architecture, see `docs/os/business-brain-framework.md`.
- For data fusion and analytics, see `docs/os/forensic-business-brain.md`.
- For sentiment and manipulation safeguards, see the semantic and persuasion docs.
```

This structure aligns with what Cursor’s own docs and community say about **short, imperative, always-on rules** that delegate detail to project docs.[^2][^1][^3]

## 7. Leveraging Existing Business Brain and Forensic Brain Docs

The attached internal documents already implement most of what general MDC best practices recommend:

- **The Business Brain Framework** provides a six-layer architecture and clear build order that can be referenced from **agent orchestration rules** (Layer 1–6 and DAD pattern).[^11]
- **The Forensic Business Brain master report** provides the semantic patterns, public-data fusion recipes, and agent moment designs that can power **specialised rules** for analytics, risk detection, and consent-anchored persuasion.[^12]
- **The MDC draft** already captures advanced insights about **meta-rules, confirmation phases, and rule-acknowledgement flows** that the Cursor community is only beginning to standardise.[^13]

Instead of duplicating these into MDC files, the recommended pattern is:

- North Star MDC tells the agent **where the OS docs live** and how to use them.
- Domain-specific MDC files (e.g., `300-agent-orchestration.mdc`) contain a **thin instruction layer**: "When orchestrating agents, follow the DAD pattern; read sections X, Y, Z of Business Brain before designing new flows."[^11]
- Documentation remains **versioned and prose-heavy** in `/docs`, where it does not compete for prompt tokens.

## 8. Existing Pre-Built / Free Tools Relevant to Your Goal

To reduce friction further and stand on community shoulders, these assets are especially useful:

- **Rule libraries and packs**
  - digitalchild’s best-practices repo: structure, naming, and patterns for composing rules.[^1]
  - DeGraciaMathieu’s rules: examples of style-focused rules for a language (PHP) that can be ported to TypeScript/Python.[^6]
  - Community packs of 77+ and 879+ rules for many stacks; offer canonical examples, though they should be trimmed heavily to avoid bloat.[^8][^7]

- **Generators**
  - awesome-cursor-rules-mdc: generate new MDC rules for frameworks/libraries from JSON specs; can be forked and adapted to your own taxonomy of agents and skills.[^9]
  - cursorrules.org: use as an external baseline for verifying that your Project OS rule is structurally valid and compatible with future Cursor changes.[^10]

- **Meta-MDC files**
  - justdo’s `999-mdc-format.mdc` and similar meta-rules show how to embed **"how to write rules"** inside a project so agents can evolve the rule set over time.[^5]

These serve as **reference implementations** for the Project OS you are designing: you can mirror their structure while keeping your OS content.

## 9. Recommended Next Steps for Implementation

For Cursor agents working on Amplified’s repos, a concrete plan:

1. **Create the `.cursor/rules` directory** if it does not exist and ensure no stale `.cursorrules` file conflicts remain.[^4][^2]
2. **Implement `000-amplified-north-star.mdc`** using the compressed pattern above, adapted to the specific repo (web app, orchestration service, etc.).[^13]
3. **Add `010-guardrails-security-types.mdc`** with minimal hard constraints, drawing on existing internal rules about secrets, migrations, and TypeScript safety.
4. **Add `020-handshake-handoff.mdc`** and create `docs/templates/handoff-template.md` to formalise the baton-pass protocol.[^13]
5. **Refactor existing "clean folder" docs** into `docs/os` and `docs/templates`, then update the North Star file’s pointers.
6. **Optionally ingest external rule packs** (digitalchild, DeGraciaMathieu) as reference, but keep them **agent-requested or manual**, not always-on, to avoid context overload.[^6][^1]
7. **Test with fresh Cursor sessions**:
   - Ask the agent: "Summarise the Amplified Project OS from rules and docs".
   - Ask the agent to perform a small task and produce a handoff; then start a new session and continue from that handoff only.

If those flows succeed reliably, the Project OS for agents is behaving as intended.

---

## References

1. [digitalchild/cursor-best-practices - GitHub](https://github.com/digitalchild/cursor-best-practices) - Write focused, composable .mdc rules. · Keep rules concise: under 500 lines. · Reuse rule blocks ins...

2. [My Best Practices for MDC rules and troubleshooting - Guides - Cursor](https://forum.cursor.com/t/my-best-practices-for-mdc-rules-and-troubleshooting/50526) - I've been exploring how Cursor's MDC rules work by experimenting with the AI. I wanted to share what...

3. [Cursor Rules: How to Keep AI Aligned With Your Codebase](https://www.datacamp.com/tutorial/cursor-rules) - This tutorial builds a set of .mdc rule files for a Python web project using FastAPI and pytest, cov...

4. [alwaysApply: true rules AND .cursorrules both silently treated as ...](https://forum.cursor.com/t/alwaysapply-true-rules-and-cursorrules-both-silently-treated-as-requestable-instead-of-auto-injected-cursor-3-0-16-macos/157431) - mdc files override .cursorrules when both exist — but when .mdc 's alwaysApply is broken, this creat...

5. [justdo/.cursor/rules/999-mdc-format.mdc at master ... - GitHub](https://github.com/justdoinc/justdo/blob/master/.cursor/rules/999-mdc-format.mdc) - MDC (Markdown Configuration) files are used by Cursor to provide context-specific instructions to AI...

6. [DeGraciaMathieu/cursor-mdc-rules: Cursor Rules for writing clear ...](https://github.com/DeGraciaMathieu/cursor-mdc-rules) - All of these rules share the same goal: to write code that clearly communicates its intent, is easy ...

7. [Created a collection of 879 .mdc Cursor Rules files for you all](https://forum.cursor.com/t/created-a-collection-of-879-mdc-cursor-rules-files-for-you-all/51634) - A script to convert .cursorrules files into .mdc files using LLMs according to instructions given in...

8. [I put together 77 .mdc rules for Cursor — languages, frameworks ...](https://www.reddit.com/r/cursor/comments/1ra9hyd/i_put_together_77_mdc_rules_for_cursor_languages/) - I put together 77 .mdc rules for Cursor — languages, frameworks, tools, practices. All free. · 14 la...

9. [sanjeed5/awesome-cursor-rules-mdc - GitHub](https://github.com/sanjeed5/awesome-cursor-rules-mdc) - This project generates Cursor MDC (Markdown Cursor) rule files from a structured JSON file containin...

10. [Free AI .cursorrules & .mdc Config Generator | Open Source ...](https://cursorrules.org) - Learn how to optimize AI-assisted programming with .cursorrules. Define coding standards, preferred ...

11. [business-brain-framework.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/149095443/5e977a35-788d-4273-98db-bf4f324ffedb/business-brain-framework.md?AWSAccessKeyId=ASIA2F3EMEYE6Z5XSPFN&Signature=rJxxtvJ1KHsWMqFYQO%2F8CHGkQbs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCBinnWa4YAlkstwWA1l59rrNyyfkllFGwk5kJ0p2%2BvdQIhALePjGs72WoB8aoUXCw0KgHAWrElYhPzR96QWEUzrpCyKvMECEwQARoMNjk5NzUzMzA5NzA1IgwxqsSt7PHVGcN5fXIq0ATOxQ5r3cNXc8dCheeOsvlq8SPF%2FhmSMoPbSnjZY54OcDbHM%2FPB84svLdxGHZdfv0VAGfY%2ByjIgXKrOKEgPPF00Bpiw4Z1r%2Bq%2BuyMCzbT71y1Rna9hlXhlbrwhPGLRBrqbJdIHrQtpw4ueC5FYJzc6KbmJeD4UYGBuyaEXQwth0FUAbI7jWnVCKdSmncmc5jGQXiEJ4WRYawegICEVeZWS7hbOIdeNKSWo1vpl0ercTGyLBB1znRT%2FomdoyQBB96hdZltX%2F8ak2l8vb2UQnoHR5kOP%2BIY0MBx9twQjr93yR2BuXdFC4OP0pCGpdjhaapvGEe8LjwNsguY1AlIkmbYyHt0mUpGbVdB05Ezxl1HR9ZCwmEwQKI0o3%2FuPcPbhkYLsPJGCeAn81pOyTwVebTvbr5i%2BMnFBhL3BnVsXRwhL3YLte%2F1DxsfuwImuFk9kggjFi6Dt%2BQijprUJYrsvR0HhnmO50%2BTGGSDhZFqit3Bpb10D8CQolgzMU7FP2EW6Oho6rRkC9MdNvIdzN7Ox6TO%2FxtN5qo0ZDaRMXSOdNb3bS9Afg%2B7EVMuFuj6MjzkG4QXswTk8LSBUlfbihsIEFMMvPcSL4CsqTxj3pdsxmLEIWymRZdLiAWGC3iv8P1VU7DzIRJwKNN2mWcAqv70sCTHMlxZrEnBOB2Yvq65h77trFmbyI4YA%2B0mbd3th1OvIlXK%2FCN7Hf0laq%2FOMvvFPtIAoYg0tgoLGn0pkhG08p0FCPq4MqXmnQXdLPZmMJ%2BRBXb52sa%2BzbDGxa0V50P0p%2FsLkFMIvNos8GOpcBfxlt%2BTjgmztFbGwZ6lgbyMIc2vqBO7PUJXb74rHH5KgFE6aJJ9xvhDhopy%2B%2Ftqvqis7lur9aPhhwSAONqNAhoCCFvJyyvNiXv%2F4keux8PDpXJ51TirhMY%2BDsvka5fxniIHCw2tEbRsgIDa5656%2BDjpMB%2BFSvAR0zgS%2F4l9uuTjDFNqpyoWi%2FME5jnGzD1EVt62DeFdpOaw%3D%3D&Expires=1776858206) - A connective framework for Amplified Partners Byker Business Help how to bind legacy IT, a determini...

12. [00-master-report.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/149095443/5c981246-88b9-4a6d-ac8e-72aa211471a6/00-master-report.md?AWSAccessKeyId=ASIA2F3EMEYE6Z5XSPFN&Signature=lqxtLzp4UdRQCnO0SLMCknqoiY8%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCBinnWa4YAlkstwWA1l59rrNyyfkllFGwk5kJ0p2%2BvdQIhALePjGs72WoB8aoUXCw0KgHAWrElYhPzR96QWEUzrpCyKvMECEwQARoMNjk5NzUzMzA5NzA1IgwxqsSt7PHVGcN5fXIq0ATOxQ5r3cNXc8dCheeOsvlq8SPF%2FhmSMoPbSnjZY54OcDbHM%2FPB84svLdxGHZdfv0VAGfY%2ByjIgXKrOKEgPPF00Bpiw4Z1r%2Bq%2BuyMCzbT71y1Rna9hlXhlbrwhPGLRBrqbJdIHrQtpw4ueC5FYJzc6KbmJeD4UYGBuyaEXQwth0FUAbI7jWnVCKdSmncmc5jGQXiEJ4WRYawegICEVeZWS7hbOIdeNKSWo1vpl0ercTGyLBB1znRT%2FomdoyQBB96hdZltX%2F8ak2l8vb2UQnoHR5kOP%2BIY0MBx9twQjr93yR2BuXdFC4OP0pCGpdjhaapvGEe8LjwNsguY1AlIkmbYyHt0mUpGbVdB05Ezxl1HR9ZCwmEwQKI0o3%2FuPcPbhkYLsPJGCeAn81pOyTwVebTvbr5i%2BMnFBhL3BnVsXRwhL3YLte%2F1DxsfuwImuFk9kggjFi6Dt%2BQijprUJYrsvR0HhnmO50%2BTGGSDhZFqit3Bpb10D8CQolgzMU7FP2EW6Oho6rRkC9MdNvIdzN7Ox6TO%2FxtN5qo0ZDaRMXSOdNb3bS9Afg%2B7EVMuFuj6MjzkG4QXswTk8LSBUlfbihsIEFMMvPcSL4CsqTxj3pdsxmLEIWymRZdLiAWGC3iv8P1VU7DzIRJwKNN2mWcAqv70sCTHMlxZrEnBOB2Yvq65h77trFmbyI4YA%2B0mbd3th1OvIlXK%2FCN7Hf0laq%2FOMvvFPtIAoYg0tgoLGn0pkhG08p0FCPq4MqXmnQXdLPZmMJ%2BRBXb52sa%2BzbDGxa0V50P0p%2FsLkFMIvNos8GOpcBfxlt%2BTjgmztFbGwZ6lgbyMIc2vqBO7PUJXb74rHH5KgFE6aJJ9xvhDhopy%2B%2Ftqvqis7lur9aPhhwSAONqNAhoCCFvJyyvNiXv%2F4keux8PDpXJ51TirhMY%2BDsvka5fxniIHCw2tEbRsgIDa5656%2BDjpMB%2BFSvAR0zgS%2F4l9uuTjDFNqpyoWi%2FME5jnGzD1EVt62DeFdpOaw%3D%3D&Expires=1776858206) - Subtitle What becomes possible when you combine forensic internal data, UK public datasets, semantic...

13. [md-draft.md.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/149095443/0a4c58a8-7b07-4d62-8c49-cd2a782c68c3/md-draft.md.txt?AWSAccessKeyId=ASIA2F3EMEYE6Z5XSPFN&Signature=DFQ1rfOWqSRVU3u%2BerVNsm8nMjA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCBinnWa4YAlkstwWA1l59rrNyyfkllFGwk5kJ0p2%2BvdQIhALePjGs72WoB8aoUXCw0KgHAWrElYhPzR96QWEUzrpCyKvMECEwQARoMNjk5NzUzMzA5NzA1IgwxqsSt7PHVGcN5fXIq0ATOxQ5r3cNXc8dCheeOsvlq8SPF%2FhmSMoPbSnjZY54OcDbHM%2FPB84svLdxGHZdfv0VAGfY%2ByjIgXKrOKEgPPF00Bpiw4Z1r%2Bq%2BuyMCzbT71y1Rna9hlXhlbrwhPGLRBrqbJdIHrQtpw4ueC5FYJzc6KbmJeD4UYGBuyaEXQwth0FUAbI7jWnVCKdSmncmc5jGQXiEJ4WRYawegICEVeZWS7hbOIdeNKSWo1vpl0ercTGyLBB1znRT%2FomdoyQBB96hdZltX%2F8ak2l8vb2UQnoHR5kOP%2BIY0MBx9twQjr93yR2BuXdFC4OP0pCGpdjhaapvGEe8LjwNsguY1AlIkmbYyHt0mUpGbVdB05Ezxl1HR9ZCwmEwQKI0o3%2FuPcPbhkYLsPJGCeAn81pOyTwVebTvbr5i%2BMnFBhL3BnVsXRwhL3YLte%2F1DxsfuwImuFk9kggjFi6Dt%2BQijprUJYrsvR0HhnmO50%2BTGGSDhZFqit3Bpb10D8CQolgzMU7FP2EW6Oho6rRkC9MdNvIdzN7Ox6TO%2FxtN5qo0ZDaRMXSOdNb3bS9Afg%2B7EVMuFuj6MjzkG4QXswTk8LSBUlfbihsIEFMMvPcSL4CsqTxj3pdsxmLEIWymRZdLiAWGC3iv8P1VU7DzIRJwKNN2mWcAqv70sCTHMlxZrEnBOB2Yvq65h77trFmbyI4YA%2B0mbd3th1OvIlXK%2FCN7Hf0laq%2FOMvvFPtIAoYg0tgoLGn0pkhG08p0FCPq4MqXmnQXdLPZmMJ%2BRBXb52sa%2BzbDGxa0V50P0p%2FsLkFMIvNos8GOpcBfxlt%2BTjgmztFbGwZ6lgbyMIc2vqBO7PUJXb74rHH5KgFE6aJJ9xvhDhopy%2B%2Ftqvqis7lur9aPhhwSAONqNAhoCCFvJyyvNiXv%2F4keux8PDpXJ51TirhMY%2BDsvka5fxniIHCw2tEbRsgIDa5656%2BDjpMB%2BFSvAR0zgS%2F4l9uuTjDFNqpyoWi%2FME5jnGzD1EVt62DeFdpOaw%3D%3D&Expires=1776858206) - Good evening. Good evening! Hope youre winding down nicely. How can I help you tonight? I would like...

