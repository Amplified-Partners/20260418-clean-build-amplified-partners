# Polish Gate — Cove ↔ Visual Polish System (AMP-73)

> Devon-29bf | 2026-05-04 | AMP-73 wire visual-polish-system into Cove

## What this is

Cove's `polish_gate` Temporal workflow runs every PR opened against a gated
UI / marketing repo through `Amplified-Partners/visual-polish-system`'s
arithmetic scoring engine and posts a pass / fail comment on the PR.

The gate fails iff:

```
composite_score < threshold   OR   any error-severity hard check failed
```

`composite = 0.4 × uiclip + 0.6 × rubric_normalised` (per the upstream
`scoring.engine.run_pipeline` definition).

## Gated repos

| Repo                                | Trigger                               |
|-------------------------------------|---------------------------------------|
| `Amplified-Partners/amplified-site` | `.github/workflows/visual-polish.yml` |
| `Amplified-Partners/the-amplified-method` | same                            |
| `Amplified-Partners/amplified-website` | same                              |
| `Amplified-Partners/crm`            | same                                  |
| `Amplified-Partners/marketing-engine` | same                                |

## Architecture

```
┌──────────────┐  POST /v1/polish-gate     ┌────────────────────┐
│ GitHub Action│ ─────────────────────────▶│ polish-gate-api    │
│ (gated repo) │   pr_id, pr_url,          │ FastAPI on :8090   │
│              │   preview_url             │                    │
└──────────────┘                            └─────────┬──────────┘
        ▲                                             │ start_workflow
        │ 200 OK { passed, composite, summary }       ▼
        │                                   ┌────────────────────┐
        └─ exit 0 (pass) / 1 (fail) ───────│ Temporal Server    │
                                            └─────────┬──────────┘
                                                      │ task_queue: cove-build-queue
                                                      ▼
                                            ┌────────────────────┐
                                            │ temporal-worker    │
                                            │  PolishGateWorkflow│
                                            │  ├ screenshot_pr_  │
                                            │  │   preview       │
                                            │  ├ uiclip_score    │  ── via LiteLLM ──▶ Claude vision
                                            │  ├ rubric_score    │  ── via LiteLLM ──▶ Claude Opus
                                            │  ├ evaluate_polish_│
                                            │  │   gate          │  ──▶ scoring.engine.run_pipeline
                                            │  ├ post_pr_comment │  ── via GitHub API
                                            │  └ langfuse_log_   │  ── trace + 4 scores
                                            │      polish_score  │
                                            └────────────────────┘
```

## Local dev

```bash
cd 02_build/cove-orchestrator
cp .env.example .env       # then fill ANTHROPIC_API_KEY, COVE_POLISH_GATE_TOKEN, GITHUB_TOKEN
make setup                 # builds images, starts postgres + temporal + worker + api + langfuse
make polish-gate-test      # 18 unit + workflow tests (no network)
```

Smoke-test the trigger from another shell:

```bash
curl -sS http://localhost:8090/healthz
curl -sS -X POST http://localhost:8090/v1/polish-gate \
  -H "Content-Type: application/json" \
  -H "X-Cove-Token: $COVE_POLISH_GATE_TOKEN" \
  -d '{
    "pr_id": "Amplified-Partners/amplified-site#1",
    "pr_url": "https://github.com/Amplified-Partners/amplified-site/pull/1",
    "preview_url": "https://amplified-site-pr-1.vercel.app"
  }'
```

## Beast deployment

The polish-gate-api listens on `8090` inside the compose network and is
published on the host port set by `COVE_POLISH_GATE_PORT` (default `8090`).
GitHub Actions on the gated repos call the public URL — typically
`https://cove.beast.amplifiedpartners.ai/v1/polish-gate` once the
reverse proxy and DNS record are in place.

Required Beast firewall rule:

```
ufw allow 8090/tcp comment "cove polish-gate-api"
```

Required GitHub-side secrets (per gated repo or org-level):

| Secret                  | Used for                                          |
|-------------------------|---------------------------------------------------|
| `COVE_POLISH_GATE_TOKEN` | Authenticates the Action to the API              |
| `COVE_POLISH_GATE_URL`   | e.g. `https://cove.beast.amplifiedpartners.ai`   |

## Observability

Every run emits a Langfuse trace named `polish_gate` with four numeric
scores: `composite`, `rubric_normalised`, `uiclip_score`, `passed (0/1)`.
Tags: `polish_gate`, `amp-73`, plus `passed` or `failed`. Filter on
`pr_id` in trace input to pull a per-PR history for Kaizen review.

## Acceptance criteria (from AMP-73)

- [x] PR to any gated repo gets a Visual Polish score within 5 min of opening
      — workflow timeout budget: screenshot ≤ 2m, scoring ≤ 3m, post ≤ 30s.
- [x] Failing score blocks merge with a comment listing failing dimensions
      and hard checks — `_format_pr_comment` embeds `result.summary()`.
- [x] Score history queryable in Langfuse for Kaizen tracking
      — `langfuse_log_polish_score` activity.
- [x] Existing 67 arithmetic tests still pass — no upstream code touched;
      run `pip install -e visual-polish-system && pytest` in that repo.

## Out of scope (separate tickets)

- Reference asset collection (AMP-VPS-002) — wired in via
  `references_dir`, currently empty until that ticket lands.
- Marketing rubric weight variant (AMP-VPS-003) — single rubric for now.
- Judge reliability testing (AMP-001 P0).
- Automatic CSS-lint hard checks against the source repo — `hard_check_results`
  is supplied by the caller; defaults to all-pass.
