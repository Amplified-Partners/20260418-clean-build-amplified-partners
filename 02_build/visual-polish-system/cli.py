#!/usr/bin/env python3
"""
Visual Polish Scoring CLI

Feed in scores, get numerical results back.

Usage:
    # Interactive mode — prompts for each dimension score
    python cli.py --rubric ../principles/references/rubric.json \
                  --rules ../principles/rules/core.rules.json \
                  --interactive

    # JSON file mode — reads scores from a JSON file
    python cli.py --rubric ../principles/references/rubric.json \
                  --rules ../principles/rules/core.rules.json \
                  --input scores.json

    # Quick test with uniform scores
    python cli.py --rubric ../principles/references/rubric.json \
                  --rules ../principles/rules/core.rules.json \
                  --uniform 7 --uiclip 0.72

    # Validate rubric only (no scoring)
    python cli.py --rubric ../principles/references/rubric.json --validate

    # Compare two score files (Kaizen mode)
    python cli.py --rubric ../principles/references/rubric.json \
                  --rules ../principles/rules/core.rules.json \
                  --input candidate.json --baseline baseline.json
"""

import argparse
import json
import sys
import os

# Add parent to path so scoring package is importable
sys.path.insert(0, os.path.dirname(__file__))

from scoring.engine import ScoringEngine, HardCheckEngine, run_pipeline
from scoring.models import CompositeScore


def load_score_file(path: str) -> dict:
    """Load a score input JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def interactive_scores(engine: ScoringEngine) -> tuple[dict[str, float], dict[str, bool], float]:
    """Prompt user for each dimension score interactively."""
    print("\n  Enter scores for each dimension (1-10):\n")
    scores = {}
    for dim in engine.rubric.dimensions:
        while True:
            try:
                val = float(input(f"  {dim.name} ({dim.id}) [{dim.scale_min}-{dim.scale_max}]: "))
                if dim.validate_score(val):
                    scores[dim.id] = val
                    break
                print(f"    ⚠ Score must be between {dim.scale_min} and {dim.scale_max}")
            except ValueError:
                print("    ⚠ Please enter a number")

    # UIClip score
    while True:
        try:
            uiclip = float(input("\n  UIClip score [0.0-1.0]: "))
            if 0.0 <= uiclip <= 1.0:
                break
            print("    ⚠ Must be between 0.0 and 1.0")
        except ValueError:
            print("    ⚠ Please enter a number")

    # Hard checks — default all pass for interactive mode
    print("\n  Hard checks defaulting to all-pass. Use --input for specific check results.\n")
    hard_checks = {}

    return scores, hard_checks, uiclip


def main():
    parser = argparse.ArgumentParser(
        description="Visual Polish Scoring Pipeline — arithmetic test harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--rubric", required=True, help="Path to rubric.json")
    parser.add_argument("--rules", help="Path to core.rules.json")
    parser.add_argument("--input", help="Path to score input JSON file")
    parser.add_argument("--baseline", help="Path to baseline score JSON (for Kaizen comparison)")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--uniform", type=float, help="Set all dimensions to this score (quick test)")
    parser.add_argument("--uiclip", type=float, default=0.50, help="UIClip score (default 0.50)")
    parser.add_argument("--validate", action="store_true", help="Validate rubric only, no scoring")
    parser.add_argument("--threshold", type=float, default=0.60, help="Pass/fail threshold (default 0.60)")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # ─── Validate mode ───────────────────────────────────────────────
    if args.validate:
        engine = ScoringEngine.from_rubric(args.rubric)
        errors = engine.validate_rubric()
        if errors:
            print("\n  ✗ RUBRIC VALIDATION FAILED:")
            for e in errors:
                print(f"    - {e}")
            sys.exit(1)
        else:
            print(f"\n  ✓ Rubric is valid")
            print(f"    Dimensions: {len(engine.rubric.dimensions)}")
            print(f"    Total weight: {engine.rubric.total_weight():.6f}")
            for dim in engine.rubric.dimensions:
                print(f"    {dim.id:<25} weight={dim.weight:.2f}  scale=[{dim.scale_min},{dim.scale_max}]")
            sys.exit(0)

    # ─── Scoring modes ───────────────────────────────────────────────
    if not args.rules:
        parser.error("--rules is required for scoring (use --validate for rubric-only)")

    engine = ScoringEngine.from_rubric(args.rubric)

    if args.interactive:
        raw_scores, hard_check_results, uiclip = interactive_scores(engine)
    elif args.uniform is not None:
        dim_ids = engine.rubric.dimension_ids()
        raw_scores = {d: args.uniform for d in dim_ids}
        hard_check_results = {}
        uiclip = args.uiclip
    elif args.input:
        data = load_score_file(args.input)
        raw_scores = data.get("rubric_scores", data.get("scores", {}))
        hard_check_results = data.get("hard_checks", {})
        uiclip = data.get("uiclip_score", args.uiclip)
    else:
        parser.error("Provide --input, --interactive, or --uniform")

    # Fill missing hard checks with True (pass)
    hard_engine = HardCheckEngine.from_json(args.rules)
    for rule in hard_engine.rules:
        hard_check_results.setdefault(rule.id, True)

    # ─── Load baseline for Kaizen ────────────────────────────────────
    baseline_composite = None
    if args.baseline:
        baseline_data = load_score_file(args.baseline)
        baseline_raw = baseline_data.get("rubric_scores", baseline_data.get("scores", {}))
        baseline_hc = baseline_data.get("hard_checks", {})
        for rule in hard_engine.rules:
            baseline_hc.setdefault(rule.id, True)
        baseline_uiclip = baseline_data.get("uiclip_score", 0.50)

        baseline_result = run_pipeline(
            rubric_path=args.rubric,
            rules_path=args.rules,
            raw_scores=baseline_raw,
            hard_check_results=baseline_hc,
            uiclip_score=baseline_uiclip,
        )
        baseline_composite = baseline_result.composite

    # ─── Run pipeline ────────────────────────────────────────────────
    try:
        result = run_pipeline(
            rubric_path=args.rubric,
            rules_path=args.rules,
            raw_scores=raw_scores,
            hard_check_results=hard_check_results,
            uiclip_score=uiclip,
            baseline=baseline_composite,
        )
    except ValueError as e:
        print(f"\n  ✗ ERROR: {e}")
        sys.exit(1)

    # ─── Output ──────────────────────────────────────────────────────
    if args.json_output:
        output = {
            "hard_checks_pass": result.hard_checks_pass,
            "hard_check_counts": result.hard_check_counts,
            "rubric": {
                "overall_raw": round(result.rubric_result.overall_raw, 4),
                "normalised": round(result.rubric_result.normalised, 6),
                "dimensions": {
                    ds.dimension_id: {
                        "raw": ds.raw_score,
                        "normalised": round(ds.normalised, 6),
                        "weighted": round(ds.weighted, 6),
                    }
                    for ds in result.rubric_result.scores
                },
            },
            "composite": {
                "uiclip_score": result.composite.uiclip_score,
                "rubric_normalised": round(result.composite.rubric_normalised, 6),
                "composite": round(result.composite.composite, 6),
                "uiclip_weight": result.composite.uiclip_weight,
                "rubric_weight": result.composite.rubric_weight,
                "formula_valid": result.composite.validate_formula(),
            },
            "threshold": args.threshold,
            "result": "PASS" if result.composite.composite >= args.threshold else "FAIL",
        }
        if result.kaizen:
            output["kaizen"] = {
                "composite_delta": round(result.kaizen.composite_delta, 6),
                "max_dimension_regression": round(result.kaizen.max_dimension_regression, 6),
                "auto_criteria_met": result.kaizen.auto_criteria_met,
                "recommendation": result.kaizen.machine_recommendation,
            }
        print(json.dumps(output, indent=2))
    else:
        print(result.summary(threshold=args.threshold))

    # Exit code: 0 = pass, 1 = fail
    sys.exit(0 if result.composite.composite >= args.threshold else 1)


if __name__ == "__main__":
    main()

