"""Visual Polish System — Temporal activities.

Activities that wire `Amplified-Partners/visual-polish-system` (Python scoring
engine, 67 passing tests) into Cove's Temporal worker so every UI / marketing
PR runs through it as a merge gate.

Three activities map 1:1 to AMP-73's ticket text:

    screenshot_pr_preview(pr_url)           → list of screenshot paths
    uiclip_score(screenshot_path)           → float in [0.0, 1.0]
    rubric_score(screenshot_path,
                 rubric_path,
                 references_dir)            → dict[dim_id, int 1..10]

Three supporting activities round out the gate:

    evaluate_polish_gate(...)               → composite score + pass/fail
    post_pr_comment(...)                    → posts result.summary() on the PR
    langfuse_log_polish_score(...)          → trace per-PR score for Kaizen

All vision-model calls go through the LiteLLM proxy on Beast (Beast has no
GPU). The composite arithmetic is delegated to the upstream
`scoring.engine.run_pipeline` — never re-implemented here.

Devon-29bf | 2026-05-04 | AMP-73 wire visual-polish-system into Cove
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from temporalio import activity

logger = logging.getLogger("cove.polish")


# ─── Inputs / Outputs ───────────────────────────────────────────────────────


@dataclass
class ScreenshotInput:
    pr_id: str                 # canonical PR id (e.g. "amplified-site#42")
    pr_url: str                # GitHub PR URL — used for traceability only
    preview_url: str           # the deployed preview the screenshot targets
    out_dir: str = "/tmp/cove-polish"
    desktop: tuple[int, int] = (1440, 900)
    mobile: tuple[int, int] = (390, 844)
    settle_ms: int = 1500      # pause after navigation for fonts / motion


@dataclass
class ScreenshotResult:
    pr_id: str
    paths: list[str]           # absolute paths on the worker, ordered desktop→mobile
    captured_at: str


@dataclass
class UIClipInput:
    pr_id: str
    screenshot_path: str
    model: str = "premium"     # routed by LiteLLM (Claude Opus by default)


@dataclass
class UIClipResult:
    pr_id: str
    screenshot_path: str
    score: float               # in [0.0, 1.0]
    model_used: str
    raw_output: str            # for trace / debugging


@dataclass
class RubricScoreInput:
    pr_id: str
    screenshot_path: str
    rubric_path: str
    references_dir: str = ""   # optional — directory of positive/negative refs
    model: str = "premium"


@dataclass
class RubricScoreResult:
    pr_id: str
    screenshot_path: str
    dimension_scores: dict[str, int]    # {dim_id: 1..10}
    rationales: dict[str, str]
    model_used: str


@dataclass
class GateEvaluationInput:
    pr_id: str
    rubric_path: str
    rules_path: str
    dimension_scores: dict[str, int]
    uiclip_score: float
    hard_check_results: dict[str, bool] = field(default_factory=dict)
    threshold: float = 0.65
    scorer: str = "cove:polish_gate"


@dataclass
class GateEvaluationResult:
    pr_id: str
    passed: bool                       # composite ≥ threshold AND all error-severity hard checks pass
    composite: float
    rubric_normalised: float
    uiclip_score: float
    threshold: float
    hard_checks_pass: bool
    summary: str                       # human-readable, posted as PR comment


@dataclass
class PRCommentInput:
    pr_id: str                 # "owner/repo#number"
    body: str
    github_token: str = ""     # optional override; falls back to env GITHUB_TOKEN


@dataclass
class LangfusePolishInput:
    pr_id: str
    pr_url: str
    composite: float
    rubric_normalised: float
    uiclip_score: float
    threshold: float
    passed: bool
    dimension_scores: dict[str, int]
    summary: str


# ─── Helpers ────────────────────────────────────────────────────────────────


def _safe_pr_slug(pr_id: str) -> str:
    """Sanitise a PR id like 'owner/repo#42' for use in filenames."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", pr_id)


def _read_image_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def _load_rubric_dimensions(rubric_path: str) -> list[dict[str, Any]]:
    """Return the rubric dimensions list from rubric.json without importing scoring."""
    with open(rubric_path, "r") as f:
        data = json.load(f)
    return list(data["rubric"]["dimensions"])


# ─── Activity: screenshot_pr_preview ────────────────────────────────────────


@activity.defn(name="screenshot_pr_preview")
async def screenshot_pr_preview(input: ScreenshotInput) -> ScreenshotResult:
    """Render the PR's preview deployment at desktop + mobile viewports.

    Uses Playwright Chromium. The preview URL is supplied by the caller —
    this activity does not resolve PR → preview itself (that lives in the
    GitHub Actions workflow which already knows its own preview URL).
    """
    from playwright.async_api import async_playwright

    Path(input.out_dir).mkdir(parents=True, exist_ok=True)
    slug = _safe_pr_slug(input.pr_id)
    desktop_path = str(Path(input.out_dir) / f"{slug}_desktop.png")
    mobile_path = str(Path(input.out_dir) / f"{slug}_mobile.png")

    activity.logger.info(
        "screenshot_pr_preview pr_id=%s preview=%s", input.pr_id, input.preview_url
    )

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        try:
            for path, viewport in (
                (desktop_path, {"width": input.desktop[0], "height": input.desktop[1]}),
                (mobile_path, {"width": input.mobile[0], "height": input.mobile[1]}),
            ):
                ctx = await browser.new_context(viewport=viewport)
                page = await ctx.new_page()
                await page.goto(input.preview_url, wait_until="networkidle", timeout=60_000)
                await page.wait_for_timeout(input.settle_ms)
                await page.screenshot(path=path, full_page=True)
                await ctx.close()
        finally:
            await browser.close()

    return ScreenshotResult(
        pr_id=input.pr_id,
        paths=[desktop_path, mobile_path],
        # gmtime() — `Z` suffix means UTC; localtime would be a silent bug
        # outside Docker (which usually pins TZ=UTC).
        captured_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


# ─── Activity: uiclip_score ─────────────────────────────────────────────────


_UICLIP_PROMPT = (
    "You are UIClip, a calibrated visual-quality scorer for product UIs. "
    "Look at the supplied screenshot and rate its overall aesthetic and "
    "functional polish on a single 0.0–1.0 scale, where:\n"
    "  0.0 = unusable / amateur / broken layout\n"
    "  0.5 = adequate / generic / uninspired\n"
    "  1.0 = best-in-class (Linear, Stripe, Apple)\n\n"
    "Reply with a single JSON object: {\"score\": <float in [0, 1]>, "
    "\"reasoning\": <one short sentence>}. No other text."
)


@activity.defn(name="uiclip_score")
async def uiclip_score(input: UIClipInput) -> UIClipResult:
    """Holistic 0..1 visual-quality score from a vision model via LiteLLM.

    Beast has no GPU so we don't run the open UIClip checkpoint locally;
    we use a vision model behind LiteLLM as a calibrated stand-in. The
    interface (single float in [0, 1]) is identical to UIClip and feeds
    directly into `scoring.engine`'s composite formula.
    """
    import httpx

    litellm_url = os.getenv("LITELLM_API_BASE", os.getenv("LITELLM_URL", "http://localhost:4000"))
    litellm_key = os.getenv("LITELLM_API_KEY", "")
    img_b64 = _read_image_b64(input.screenshot_path)

    headers = {"Content-Type": "application/json"}
    if litellm_key:
        headers["Authorization"] = f"Bearer {litellm_key}"

    payload = {
        "model": input.model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _UICLIP_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                    },
                ],
            }
        ],
        "temperature": 0.0,
        "max_tokens": 200,
        "metadata": {"trace_name": f"polish-gate.uiclip:{input.pr_id}"},
    }

    activity.logger.info("uiclip_score pr_id=%s model=%s", input.pr_id, input.model)

    async with httpx.AsyncClient(timeout=90.0) as client:
        resp = await client.post(f"{litellm_url}/v1/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    raw = data["choices"][0]["message"]["content"].strip()
    score = _parse_uiclip_score(raw)

    return UIClipResult(
        pr_id=input.pr_id,
        screenshot_path=input.screenshot_path,
        score=score,
        model_used=data.get("model", input.model),
        raw_output=raw,
    )


def _parse_uiclip_score(raw: str) -> float:
    """Extract a [0, 1] float from a JSON-ish reply.

    Out-of-range or unparseable replies raise ``ValueError`` so the activity
    fails fast and Temporal retries; we deliberately do **not** clamp
    silently — a model returning 1.4 means the prompt is broken, not that
    the UI is great.
    """
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"UIClip response had no JSON object: {raw!r}")
    obj = json.loads(match.group(0))
    score = float(obj["score"])
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"UIClip score out of [0, 1]: {score}")
    return score


# ─── Activity: rubric_score ─────────────────────────────────────────────────


def _build_rubric_prompt(dimensions: list[dict[str, Any]]) -> str:
    lines = [
        "You are a senior product-design reviewer scoring a UI screenshot "
        "against the Amplified Partners visual rubric.",
        "",
        "Score every dimension on a 1-10 integer scale (1 = anchor_low, "
        "10 = anchor_high). Be honest — most real UIs land between 4 and 8.",
        "",
        "Dimensions:",
    ]
    for d in dimensions:
        scale = d["scale"]
        lines.append(
            f"- id: {d['id']} | weight: {d['weight']:.2f}\n"
            f"  prompt: {d['prompt']}\n"
            f"  anchor_low (1): {scale.get('anchor_low', '')}\n"
            f"  anchor_high (10): {scale.get('anchor_high', '')}"
        )
    lines.extend(
        [
            "",
            "Reply with a single JSON object:",
            '  {"scores": {"<dimension_id>": <int 1..10>, ...},',
            '   "rationales": {"<dimension_id>": "<one short sentence>", ...}}',
            "",
            "Every dimension id above must appear in both 'scores' and 'rationales'. "
            "No other keys, no commentary outside the JSON.",
        ]
    )
    return "\n".join(lines)


@activity.defn(name="rubric_score")
async def rubric_score(input: RubricScoreInput) -> RubricScoreResult:
    """Per-dimension rubric scoring (10 anchored prompts) via Claude vision.

    Returns a dict[dim_id, int] suitable for direct use as
    `scoring.engine.run_pipeline(..., raw_scores=<this>, ...)`.
    """
    import httpx

    dimensions = _load_rubric_dimensions(input.rubric_path)
    expected_ids = {d["id"] for d in dimensions}
    prompt = _build_rubric_prompt(dimensions)
    img_b64 = _read_image_b64(input.screenshot_path)

    user_content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    # Few-shot reference assets — wired in for AMP-VPS-002 once it lands.
    if input.references_dir and Path(input.references_dir).is_dir():
        for ref in sorted(Path(input.references_dir).glob("*.png"))[:4]:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{_read_image_b64(str(ref))}"},
                }
            )
    user_content.append(
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img_b64}"},
        }
    )

    litellm_url = os.getenv("LITELLM_API_BASE", os.getenv("LITELLM_URL", "http://localhost:4000"))
    litellm_key = os.getenv("LITELLM_API_KEY", "")
    headers = {"Content-Type": "application/json"}
    if litellm_key:
        headers["Authorization"] = f"Bearer {litellm_key}"

    activity.logger.info("rubric_score pr_id=%s model=%s", input.pr_id, input.model)

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{litellm_url}/v1/chat/completions",
            json={
                "model": input.model,
                "messages": [{"role": "user", "content": user_content}],
                "temperature": 0.0,
                "max_tokens": 1500,
                "metadata": {"trace_name": f"polish-gate.rubric:{input.pr_id}"},
            },
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

    raw = data["choices"][0]["message"]["content"].strip()
    parsed = _parse_rubric_response(raw, expected_ids)

    return RubricScoreResult(
        pr_id=input.pr_id,
        screenshot_path=input.screenshot_path,
        dimension_scores=parsed["scores"],
        rationales=parsed.get("rationales", {}),
        model_used=data.get("model", input.model),
    )


def _parse_rubric_response(raw: str, expected_ids: set[str]) -> dict[str, Any]:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Rubric response had no JSON object: {raw!r}")
    obj = json.loads(match.group(0))

    scores = obj.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("Rubric response missing 'scores' object")
    missing = expected_ids - set(scores.keys())
    if missing:
        raise ValueError(f"Rubric response missing dimensions: {sorted(missing)}")
    extra = set(scores.keys()) - expected_ids
    if extra:
        raise ValueError(f"Rubric response had unknown dimensions: {sorted(extra)}")

    coerced: dict[str, int] = {}
    for k, v in scores.items():
        iv = int(v)
        if not 1 <= iv <= 10:
            raise ValueError(f"Rubric score for {k} out of [1, 10]: {v}")
        coerced[k] = iv

    rationales = obj.get("rationales", {})
    if not isinstance(rationales, dict):
        rationales = {}

    return {"scores": coerced, "rationales": rationales}


# ─── Activity: evaluate_polish_gate ─────────────────────────────────────────


@activity.defn(name="evaluate_polish_gate")
async def evaluate_polish_gate(input: GateEvaluationInput) -> GateEvaluationResult:
    """Run the upstream `scoring.engine.run_pipeline` and decide pass/fail.

    Pass criteria (gate semantics, per AMP-73):
      composite ≥ threshold  AND  all error-severity hard checks pass.

    Note: `PipelineResult.passed` upstream is hard-checks-only by design;
    we additionally enforce the composite threshold here so the gate can
    block low-aesthetic-quality PRs even when no hard rule failed.
    """
    # Imported here so the `temporal/` package can still be loaded by tooling
    # that doesn't have visual-polish-system installed (e.g. lint-only CI).
    from scoring.engine import run_pipeline  # type: ignore[import-not-found]

    # run_pipeline is synchronous (reads rubric.json + rules.json, does pure
    # arithmetic). Offload to a thread so we don't block the worker's event
    # loop during execution — same pattern as langfuse_log_polish_score below.
    result = await asyncio.to_thread(
        run_pipeline,
        rubric_path=input.rubric_path,
        rules_path=input.rules_path,
        raw_scores=input.dimension_scores,
        hard_check_results=input.hard_check_results,
        uiclip_score=input.uiclip_score,
        scorer=input.scorer,
    )
    composite = result.composite.composite
    passed = result.hard_checks_pass and composite >= input.threshold

    return GateEvaluationResult(
        pr_id=input.pr_id,
        passed=passed,
        composite=composite,
        rubric_normalised=result.composite.rubric_normalised,
        uiclip_score=result.composite.uiclip_score,
        threshold=input.threshold,
        hard_checks_pass=result.hard_checks_pass,
        summary=result.summary(threshold=input.threshold),
    )


# ─── Activity: post_pr_comment ──────────────────────────────────────────────


@activity.defn(name="post_pr_comment")
async def post_pr_comment(input: PRCommentInput) -> bool:
    """Post a comment on the PR (issue comment, not a review).

    `pr_id` is parsed as 'owner/repo#number'. Returns True on 2xx.
    """
    import httpx

    token = input.github_token or os.getenv("GITHUB_TOKEN", "")
    if not token:
        activity.logger.warning("post_pr_comment: no GITHUB_TOKEN set, skipping")
        return False

    m = re.match(r"^(?P<owner>[^/]+)/(?P<repo>[^#]+)#(?P<number>\d+)$", input.pr_id)
    if not m:
        raise ValueError(f"pr_id must be 'owner/repo#number', got {input.pr_id!r}")

    url = (
        f"https://api.github.com/repos/{m['owner']}/{m['repo']}"
        f"/issues/{m['number']}/comments"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json={"body": input.body}, headers=headers)
    if resp.is_success:
        return True
    activity.logger.error("post_pr_comment failed pr_id=%s status=%s", input.pr_id, resp.status_code)
    return False


# ─── Activity: langfuse_log_polish_score ────────────────────────────────────


@activity.defn(name="langfuse_log_polish_score")
async def langfuse_log_polish_score(input: LangfusePolishInput) -> bool:
    """Emit a Langfuse trace + score so PR-level polish history is queryable.

    Returns False (and logs) if Langfuse env vars aren't set, so the gate
    still works in dev environments without observability wired up.
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    if not public_key or not secret_key:
        activity.logger.warning("langfuse_log_polish_score: keys not set, skipping")
        return False

    try:
        # langfuse v2 sync client; called inside an activity so blocking is fine.
        from langfuse import Langfuse  # type: ignore[import-not-found]
    except Exception as e:  # noqa: BLE001
        activity.logger.warning("langfuse import failed: %s", e)
        return False

    def _emit() -> None:
        client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
        trace = client.trace(
            name="polish_gate",
            id=f"polish-{_safe_pr_slug(input.pr_id)}-{int(time.time())}",
            input={"pr_id": input.pr_id, "pr_url": input.pr_url},
            output={"summary": input.summary, "passed": input.passed},
            metadata={
                "composite": input.composite,
                "rubric_normalised": input.rubric_normalised,
                "uiclip_score": input.uiclip_score,
                "threshold": input.threshold,
                "dimension_scores": input.dimension_scores,
            },
            tags=["polish_gate", "amp-73", "passed" if input.passed else "failed"],
        )
        trace.score(name="composite", value=input.composite, comment="weighted UIClip+rubric")
        trace.score(name="rubric_normalised", value=input.rubric_normalised)
        trace.score(name="uiclip_score", value=input.uiclip_score)
        trace.score(name="passed", value=1.0 if input.passed else 0.0)
        client.flush()

    await asyncio.to_thread(_emit)
    return True
