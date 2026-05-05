---
title: Hazel-driven Mac → GitHub consolidation pack
date: 2026-05-05
version: 1
status: draft
ticket: AMP-83
sub_ticket: AMP-80
signed_by: "Devon-fad5 — 2026-05-05 — devin-fad59f8cffd245618655e5b692895bbc"
---

# Hazel pack — flatten `~/` to GitHub

<!-- markdownlint-disable-file MD013 -->

## What this is

A phased, non-destructive pipeline that takes everything signal-bearing under
`~/` on Ewan's Mac, classifies it, stages it, and promotes it into the right
`Amplified-Partners/*` GitHub repos. The Mac stops being source of truth.
GitHub becomes source of truth.

## Why Hazel + shell

Hazel watches folders and triggers actions. Shell scripts do the deterministic
work. The split keeps logic in version-controlled code (`02_build/hazel/scripts/`)
and reduces Hazel to a thin trigger layer (`hazel-rules.hazelrules`).

This is **Spine principle 7** in practice — narrow radius of hand-off. Each
phase is an airlock. Output of one phase is the input of the next.

## Phased flow

| # | Phase | What runs | Side-effect | Reversible? |
|---|-------|-----------|-------------|-------------|
| 1 | Inventory | `01_inventory.sh` | Writes `~/_hazel_work/manifest.jsonl` | Read-only |
| 2 | Classify | `02_classify.sh` | Writes `~/_hazel_work/plan.jsonl` | Read-only |
| 3 | Stage    | `03_stage.sh`    | Copies SIGNAL → `~/_consolidated/`, moves BLOAT/AMBIGUOUS/SECRET to staging trees. Originals untouched. | Yes |
| 4 | Promote  | `04_promote.sh`  | `git push` of `~/_consolidated/` subtrees into the right org repos | Yes (git history) |
| 5 | Reap     | `05_reap.sh`     | Deletes originals after Ewan confirms `--i-have-verified-github` | **NO** |

Ewan triggers each phase. **No phase auto-advances.** Hazel is configured as
the conveyor belt for Phase 3-4 file events, but the phase commands themselves
are run manually (or via a Hazel "Run rules now" on the appropriate folder).

## File classification

Five mutually-exclusive classes:

| Class | Definition | Action |
|-------|------------|--------|
| `SIGNAL_KEEP` | Human-curated content with knowledge value | Copy to `~/_consolidated/<route>/` |
| `BLOAT_DROP` | App-rebuildable artefacts and pure noise | Move to `~/__trash_staging/` |
| `AMBIGUOUS_REVIEW` | Below confidence threshold for either bucket | Move to `~/__review/` |
| `PROTECTED_LEAVE_ALONE` | Working-machine state apps depend on | Skip; never touched |
| `SECRET_QUARANTINE` | Anything matching token / key patterns | Move to `~/__quarantine/`; logged but never pushed |

Policy lives in `policy.yaml`. Classifications are tentative at Phase 1 and
final at Phase 2. Ewan can override per-path before Phase 3 by editing
`plan.jsonl` directly.

## Working directory layout

The pack uses `~/_hazel_work/` as its scratch and `~/_consolidated/` as the
staging output. Nothing under `~/` is moved or deleted before Phase 3.

```
$HOME/
├── _hazel_work/
│   ├── manifest.jsonl       # Phase 1 output
│   ├── plan.jsonl           # Phase 2 output
│   ├── routes.json          # Phase 4 input: class → org repo mapping
│   └── log/<phase>-<ts>.log
├── _consolidated/
│   ├── code/<repo>/...      # SIGNAL_KEEP routed by source repo
│   ├── notes/...
│   ├── transcripts/...
│   └── unmapped/...
├── __trash_staging/         # BLOAT_DROP
├── __review/                # AMBIGUOUS_REVIEW
└── __quarantine/            # SECRET_QUARANTINE (gitignored everywhere)
```

## Default protected paths (never touched)

- `~/.ssh/**`
- `~/Library/Keychains/**`
- `~/Library/Mail/**`
- `~/Library/Photos Library.photoslibrary/**`
- `~/Library/Application Support/{1Password 7,1Password,com.apple.*,Hazel,Notion,Slack,Cursor,Code,iTerm2,Obsidian}/**`
- `~/Library/Containers/**`
- `~/Library/CloudStorage/**`
- `~/Library/Group Containers/**`
- Anything matching `*.app/**` (application bundles)

Override list in `policy.yaml` under `protected_globs:`.

## Default secret patterns

```
ghp_[A-Za-z0-9]{20,}        # GitHub PAT (classic)
gho_[A-Za-z0-9]{20,}        # GitHub OAuth
ghu_[A-Za-z0-9]{20,}        # GitHub user-to-server
ghs_[A-Za-z0-9]{20,}        # GitHub server-to-server
github_pat_[A-Za-z0-9_]{50,}# GitHub fine-grained
sk-[A-Za-z0-9]{20,}         # OpenAI / Anthropic style
AKIA[0-9A-Z]{16}            # AWS access key id
-----BEGIN [A-Z ]+ KEY----- # PEM private keys
xoxb-|xoxp-|xoxa-           # Slack tokens
hf_[A-Za-z0-9]{30,}         # HuggingFace
```

Anything matching these = `SECRET_QUARANTINE`. Logged with redacted prefix
(`ghp_***`) and the path. **The matched secret value is never written to logs
or to GitHub.**

## Promotion routes (Phase 4)

`routes.json` maps content classes / source repos to existing
`Amplified-Partners/*` repos. The default mapping is conservative — anything
unmapped goes to `unmapped/` for explicit Ewan decision before commit.

| Source pattern (in `~/_consolidated/`) | Destination repo |
|----------------------------------------|------------------|
| `code/<repo>/**` where `<repo>` exists in org | `Amplified-Partners/<repo>` |
| `notes/**` | `Amplified-Partners/vault` |
| `transcripts/**` | `Amplified-Partners/corpus-raw` |
| `research/**` | `Amplified-Partners/perplexity-research` |
| `screenshots-with-signal/**` | `Amplified-Partners/corpus-raw` (subdir) |
| `unmapped/**` | **No auto-push** — Ewan decides per-tree |

## Acceptance criteria for closing AMP-83

1. Phase 1 manifest covers `≥ 95%` of files under `~/` (some may be unreadable; logged).
2. Phase 2 plan classifies `≥ 90%` as SIGNAL or BLOAT (high-confidence). AMBIGUOUS bucket reviewable in one sitting.
3. Phase 3 stage produces `~/_consolidated/` with no `SECRET_QUARANTINE` content.
4. Phase 4 promote pushes all routable content to org repos. Each push commit signed `Devon-fad5` (or whichever agent runs it).
5. Phase 5 reap runs successfully; `~/` is reduced to PROTECTED set + working app data.
6. AMP-80 closed (PAT exposure scrubbed by Phase 3 quarantine).

## Failure modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Phase 3 SIGNAL copy fails partway | `03_stage.sh` exits non-zero, logs file | Re-run; idempotent (skips already-copied files by hash) |
| Phase 4 push fails (auth, conflicts) | git error in log | Fix auth via `gh auth login`; re-run; commits coalesce |
| Phase 5 deletes a file Ewan still needed | Detected only by Ewan after the fact | **Time Machine restore.** Pre-condition for Phase 5 is verified TM backup. |
| Hazel rule misfires and moves a file early | Hazel log + folder watch | Move file back; tighten the Hazel rule's condition. |

## Signed
*Devon-fad5 | 2026-05-05 | devin-fad59f8cffd245618655e5b692895bbc | parent: AMP-83 | child: AMP-80*
