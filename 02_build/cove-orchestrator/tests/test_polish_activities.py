"""Unit tests for the parsing / pure helpers in `polish_activities`.

The activities themselves talk to LiteLLM, GitHub, and Playwright, so the
network-bound surface is mocked in `test_polish_gate_workflow.py`. Here we
cover the deterministic helpers that don't need a worker to test.
"""

from __future__ import annotations

import json

import pytest

from temporal.activities.polish_activities import (
    _build_rubric_prompt,
    _parse_rubric_response,
    _parse_uiclip_score,
    _safe_pr_slug,
)


# ─── _safe_pr_slug ──────────────────────────────────────────────────────────


def test_safe_pr_slug_replaces_specials() -> None:
    assert _safe_pr_slug("Amplified-Partners/amplified-site#42") == "Amplified-Partners_amplified-site_42"


def test_safe_pr_slug_keeps_dots_and_dashes() -> None:
    assert _safe_pr_slug("foo.bar-baz") == "foo.bar-baz"


# ─── _parse_uiclip_score ────────────────────────────────────────────────────


def test_parse_uiclip_valid_json() -> None:
    raw = '{"score": 0.72, "reasoning": "clean"}'
    assert _parse_uiclip_score(raw) == 0.72


def test_parse_uiclip_extracts_from_padding() -> None:
    raw = "Sure, here you go:\n{\"score\": 0.5, \"reasoning\": \"meh\"}\nThanks!"
    assert _parse_uiclip_score(raw) == 0.5


def test_parse_uiclip_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match="out of"):
        _parse_uiclip_score('{"score": 1.4}')


def test_parse_uiclip_rejects_missing_json() -> None:
    with pytest.raises(ValueError, match="no JSON"):
        _parse_uiclip_score("score: 0.5")


# ─── _build_rubric_prompt ───────────────────────────────────────────────────


_DIM = {
    "id": "calm_surface",
    "name": "Calm Surface",
    "weight": 0.15,
    "prompt": "Rate visual calmness.",
    "scale": {"min": 1, "max": 10, "anchor_low": "noisy", "anchor_high": "serene"},
}


def test_build_rubric_prompt_mentions_each_dim() -> None:
    out = _build_rubric_prompt([_DIM])
    assert "calm_surface" in out
    assert "weight: 0.15" in out
    assert "noisy" in out and "serene" in out


def test_build_rubric_prompt_demands_strict_json() -> None:
    out = _build_rubric_prompt([_DIM])
    assert '"scores"' in out and '"rationales"' in out
    assert "No other keys" in out


# ─── _parse_rubric_response ────────────────────────────────────────────────


_EXPECTED = {"calm_surface", "clear_hierarchy"}


def _ok_payload() -> str:
    return json.dumps(
        {
            "scores": {"calm_surface": 7, "clear_hierarchy": 8},
            "rationales": {"calm_surface": "ok", "clear_hierarchy": "ok"},
        }
    )


def test_parse_rubric_happy_path() -> None:
    out = _parse_rubric_response(_ok_payload(), _EXPECTED)
    assert out["scores"] == {"calm_surface": 7, "clear_hierarchy": 8}
    assert set(out["rationales"]) == _EXPECTED


def test_parse_rubric_coerces_string_ints() -> None:
    payload = json.dumps({"scores": {"calm_surface": "7", "clear_hierarchy": "8"}})
    out = _parse_rubric_response(payload, _EXPECTED)
    assert out["scores"]["calm_surface"] == 7
    assert isinstance(out["scores"]["calm_surface"], int)


def test_parse_rubric_rejects_missing_dimension() -> None:
    payload = json.dumps({"scores": {"calm_surface": 7}})
    with pytest.raises(ValueError, match="missing dimensions"):
        _parse_rubric_response(payload, _EXPECTED)


def test_parse_rubric_rejects_unknown_dimension() -> None:
    payload = json.dumps(
        {"scores": {"calm_surface": 7, "clear_hierarchy": 8, "made_up": 9}}
    )
    with pytest.raises(ValueError, match="unknown dimensions"):
        _parse_rubric_response(payload, _EXPECTED)


def test_parse_rubric_rejects_out_of_range() -> None:
    payload = json.dumps({"scores": {"calm_surface": 11, "clear_hierarchy": 8}})
    with pytest.raises(ValueError, match="out of"):
        _parse_rubric_response(payload, _EXPECTED)


def test_parse_rubric_rejects_missing_scores_object() -> None:
    payload = json.dumps({"rationales": {}})
    with pytest.raises(ValueError, match="missing 'scores'"):
        _parse_rubric_response(payload, _EXPECTED)
