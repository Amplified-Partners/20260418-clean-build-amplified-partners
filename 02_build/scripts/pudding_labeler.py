#!/usr/bin/env python3
"""
PUDDING Labeler — Assigns PUDDING 2026 labels to documents
==========================================================

Labels format: [WHAT].[HOW].[SCALE].[TIME].[PATTERN]

WHAT:  E(ntity) R(elation) P(rocess) S(tate) C(onstraint) I(nformation) M(eta)
HOW:   +(amplify) -(dampen) ~(oscillate) >(tip) =(stable) !(disrupt) ?(emerge)
SCALE: 1(singular) 2(pair) 3(small group) 4(network) 5(system) 6(universal) 0(scale-free)
TIME:  i(instant) s(short) m(medium) l(long) p(permanent) ∞(timeless) v(variable)
PATTERN: LOG-xxx, MAT-xxx, SYS-xxx, BEH-xxx, STR-xxx (optional 5th dimension)

Built for Amplified Partners vault ingestion pipeline.
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# PUDDING Taxonomy Reference
# ---------------------------------------------------------------------------

WHAT_CODES = {
    "E": "Entity — object, agent, noun, thing",
    "R": "Relation — connection, link, dependency, bond",
    "P": "Process — action, change, transformation, verb",
    "S": "State — condition, status, snapshot, phase",
    "C": "Constraint — rule, limit, boundary, law",
    "I": "Information — pattern, signal, data, message",
    "M": "Meta — model, frame, abstraction, description",
}

HOW_CODES = {
    "+": "Amplifying — growth, viral spread, compounding",
    "-": "Dampening — decay, friction, forgetting",
    "~": "Oscillating — cycles, waves, rhythms",
    ">": "Tipping — threshold, phase change, breaking point",
    "=": "Stable — equilibrium, homeostasis, persistence",
    "!": "Disrupting — shock, interruption, discontinuity",
    "?": "Emerging — uncertain, forming, becoming",
}

SCALE_CODES = {
    "1": "Singular — one atom, one thought, one word",
    "2": "Pair — dyad, binary, dialogue, bond",
    "3": "Small group — team, family, molecule, cluster",
    "4": "Network — organisation, community, ecosystem",
    "5": "System — market, society, biosphere",
    "6": "Universal — fundamental law, constant, archetype",
    "0": "Scale-free — fractal, applies at any level",
}

TIME_CODES = {
    "i": "Instant — flash, impulse, single moment",
    "s": "Short — minutes to days",
    "m": "Medium — weeks to months",
    "l": "Long — years to decades",
    "p": "Permanent — lifespan, era, geological",
    "inf": "Timeless — always true, universal constant",
    "v": "Variable — duration depends on context",
}

PATTERN_CODES = {
    # Logical
    "LOG-CAU": "Causal — A directly causes B",
    "LOG-COR": "Correlative — A and B move together",
    "LOG-CON": "Conditional — If A then B",
    "LOG-TRA": "Transitive — A→B→C therefore A→C",
    "LOG-ANA": "Analogical — A:B as C:D",
    "LOG-ABD": "Abductive — best explanation",
    # Mathematical
    "MAT-LIN": "Linear — proportional change",
    "MAT-EXG": "Exponential growth — compound acceleration",
    "MAT-EXD": "Exponential decay — death spiral",
    "MAT-DIM": "Diminishing returns — each unit adds less",
    "MAT-SIG": "S-Curve/Sigmoid — slow-fast-plateau",
    "MAT-PAR": "Power Law/Pareto — 80/20 distribution",
    "MAT-CYC": "Cyclical — repeating pattern",
    "MAT-TIP": "Threshold/Tipping point — sudden state change",
    "MAT-TRD": "Inverse/Trade-off — more A = less B",
    # Systems
    "SYS-RFL": "Reinforcing feedback — success breeds success",
    "SYS-BFL": "Balancing feedback — self-correcting",
    "SYS-CAS": "Cascade/Domino — sequential chain reaction",
    "SYS-NET": "Network effect — more users = more value",
    "SYS-BOT": "Bottleneck/Constraint — everything through one narrow point",
    "SYS-EMR": "Emergence — whole > sum of parts",
    "SYS-ENT": "Entropy/Decay — falls apart without maintenance",
    "SYS-ACC": "Accumulation/Compounding — small deposits, massive results",
    # Behavioural
    "BEH-STA": "Status quo bias — we've always done it this way",
    "BEH-LOS": "Loss aversion — fear of loss > desire for gain",
    "BEH-ANC": "Anchoring — first number dominates",
    "BEH-SUN": "Sunk cost — can't abandon past investment",
    "BEH-COM": "Compounding habits — 1% daily = 37x annually",
    # Structural
    "STR-HUB": "Hub and spoke — central node",
    "STR-HIE": "Hierarchy/Tree — top-down branching",
    "STR-PIP": "Pipeline/Sequential — step 1 → step 2 → step 3",
    "STR-PAR": "Parallel — multiple simultaneous streams",
    "STR-LAY": "Layered/Stack — each layer builds on below",
}


# ---------------------------------------------------------------------------
# Keyword-based heuristic labeler (deterministic, no LLM needed)
# ---------------------------------------------------------------------------

def detect_what(text: str) -> str:
    """Detect the WHAT dimension from content."""
    text_lower = text.lower()
    scores = {"E": 0, "R": 0, "P": 0, "S": 0, "C": 0, "I": 0, "M": 0}

    # Entity signals
    for w in ["agent", "server", "database", "tool", "platform", "software", "engine", "module", "component", "system"]:
        scores["E"] += text_lower.count(w)

    # Relation signals
    for w in ["connect", "integrat", "depend", "link", "relationship", "between", "bridge", "maps to"]:
        scores["R"] += text_lower.count(w)

    # Process signals
    for w in ["pipeline", "workflow", "step", "phase", "process", "ingest", "extract", "transform", "build", "deploy", "execute"]:
        scores["P"] += text_lower.count(w)

    # State signals
    for w in ["status", "current", "state", "snapshot", "healthy", "failed", "running", "complete"]:
        scores["S"] += text_lower.count(w)

    # Constraint signals
    for w in ["rule", "principle", "immutable", "non-negotiable", "must", "never", "constraint", "limit", "gdpr", "compliance"]:
        scores["C"] += text_lower.count(w)

    # Information signals (raw data, reports, findings — NOT frameworks or specs)
    for w in ["data", "insight", "metric", "report", "finding", "signal", "statistic", "number", "figure", "table"]:
        scores["I"] += text_lower.count(w)

    # Meta signals (frameworks, specs, taxonomies, architectures — WEIGHTED HIGHER)
    # Meta documents describe HOW to think about things, not the things themselves
    for w in ["framework", "taxonomy", "model", "architecture", "spec", "design", "abstract", "meta", "rubric", "methodology", "schema", "ontology", "classification", "dimension", "category"]:
        scores["M"] += text_lower.count(w) * 2  # Double weight — specs are clearly meta

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "I"


def detect_how(text: str) -> str:
    """Detect the HOW dimension from content."""
    text_lower = text.lower()
    scores = {"+": 0, "-": 0, "~": 0, ">": 0, "=": 0, "!": 0, "?": 0}

    scores["+"] += sum(text_lower.count(w) for w in ["grow", "amplif", "scale", "expand", "compound", "accelerat", "viral"])
    scores["-"] += sum(text_lower.count(w) for w in ["decay", "friction", "reduce", "decline", "deprecat", "legacy", "debt"])
    scores["~"] += sum(text_lower.count(w) for w in ["cycle", "recurring", "periodic", "seasonal", "oscillat", "wave"])
    scores[">"] += sum(text_lower.count(w) for w in ["threshold", "tipping", "breaking", "critical", "pivot", "transform"])
    scores["="] += sum(text_lower.count(w) for w in ["stable", "maintain", "standard", "consistent", "baseline", "equilibrium", "persist", "reference", "canonical", "definitive", "specification"])
    scores["!"] += sum(text_lower.count(w) for w in ["disrupt", "innovat", "revolution", "paradigm", "overhaul", "replace"])
    scores["?"] += sum(text_lower.count(w) for w in ["emerging", "prototype", "experiment", "explore", "potential", "uncertain", "mvp", "draft"])

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "="


def detect_scale(text: str) -> str:
    """Detect the SCALE dimension from content."""
    text_lower = text.lower()
    scores = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "0": 0}

    scores["1"] += sum(text_lower.count(w) for w in ["individual", "single", "personal", "one person", "sole"])
    scores["2"] += sum(text_lower.count(w) for w in ["pair", "bilateral", "dialogue", "two ", "both"])
    scores["3"] += sum(text_lower.count(w) for w in ["team", "small group", "department", "squad", "crew"])
    scores["4"] += sum(text_lower.count(w) for w in ["organisation", "organization", "company", "network", "ecosystem", "community", "smb", "business"])
    scores["5"] += sum(text_lower.count(w) for w in ["market", "industry", "sector", "economy", "society", "uk smb"])
    scores["6"] += sum(text_lower.count(w) for w in ["universal", "fundamental", "law", "constant", "archetype", "human nature"])
    scores["0"] += sum(text_lower.count(w) for w in ["fractal", "scale-free", "any level", "recursive", "self-similar"])

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "4"


def detect_time(text: str) -> str:
    """Detect the TIME dimension from content."""
    text_lower = text.lower()
    scores = {"i": 0, "s": 0, "m": 0, "l": 0, "p": 0, "inf": 0, "v": 0}

    # NOTE: "now" and "current" removed from instant — they appear in state descriptions, not temporal context
    scores["i"] += sum(text_lower.count(w) for w in ["instant", "immediate", "real-time", "millisecond", "alert", "trigger"])
    scores["s"] += sum(text_lower.count(w) for w in ["daily", "today", "this week", "sprint", "quick", "urgent"])
    scores["m"] += sum(text_lower.count(w) for w in ["quarter", "monthly", "phase", "milestone", "weeks", "iteration"])
    scores["l"] += sum(text_lower.count(w) for w in ["year", "annual", "long-term", "vision", "strategy", "multi-year", "roadmap"])
    scores["p"] += sum(text_lower.count(w) for w in ["permanent", "forever", "lifetime", "enduring"])
    scores["inf"] += sum(text_lower.count(w) for w in ["timeless", "always true", "universal", "principle", "immutable", "eternal", "non-negotiable", "fundamental", "taxonomy", "canonical", "reference", "definitive"])
    scores["v"] += sum(text_lower.count(w) for w in ["depends", "variable", "context-dependent", "varies"])

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "m"


def detect_patterns(text: str) -> list[str]:
    """Detect dominant PATTERN dimensions (5th position). Returns up to 3."""
    text_lower = text.lower()
    scores = {}

    pattern_keywords = {
        "LOG-CAU": ["cause", "causes", "because", "therefore", "leads to", "results in"],
        "LOG-COR": ["correlat", "moves together", "linked to", "associated"],
        "LOG-CON": ["if ", "then ", "conditional", "when ", "trigger"],
        "LOG-TRA": ["chain", "a leads to b leads to", "transitive", "indirect"],
        "LOG-ANA": ["analogy", "similar to", "like a", "as if", "metaphor"],
        "MAT-LIN": ["proportional", "linear", "each additional", "per unit"],
        "MAT-EXG": ["exponential", "viral", "compound", "snowball", "accelerat"],
        "MAT-EXD": ["death spiral", "declining", "hemorrhaging", "losing"],
        "MAT-DIM": ["diminishing", "plateau", "less effective", "saturat"],
        "MAT-SIG": ["adoption curve", "s-curve", "penetration", "tipping then plateau"],
        "MAT-PAR": ["80/20", "pareto", "power law", "most of the"],
        "MAT-CYC": ["seasonal", "quarterly", "cycle", "recurring", "periodic"],
        "SYS-RFL": ["reinforc", "positive feedback", "virtuous", "flywheel", "success breeds"],
        "SYS-BFL": ["self-correct", "balanc", "thermostat", "homeostasis"],
        "SYS-CAS": ["cascade", "domino", "chain reaction", "ripple"],
        "SYS-NET": ["network effect", "more users", "marketplace", "platform"],
        "SYS-BOT": ["bottleneck", "single point", "constraint", "blocking"],
        "SYS-EMR": ["emergence", "greater than the sum", "synergy", "holistic"],
        "SYS-ACC": ["compound", "accumulate", "build over time", "1% daily"],
        "BEH-STA": ["always done it", "status quo", "resistance to change", "legacy thinking"],
        "BEH-LOS": ["loss aversion", "fear of", "risk averse", "won't switch"],
        "STR-HUB": ["hub and spoke", "central", "owner who", "single point of contact"],
        "STR-PIP": ["pipeline", "sequential", "step by step", "stage"],
        "STR-PAR": ["parallel", "concurrent", "simultaneous", "multi-stream"],
        "STR-LAY": ["layer", "stack", "tier", "built on top"],
    }

    for pattern, keywords in pattern_keywords.items():
        score = sum(text_lower.count(kw) for kw in keywords)
        if score > 0:
            scores[pattern] = score

    # Return top 3 patterns
    sorted_patterns = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [p[0] for p in sorted_patterns[:3]]


def label_document(filepath: str) -> dict:
    """Label a single document with PUDDING 2026 codes."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8", errors="replace")
    filename = path.name

    # Extract category from path if it's a vault file
    parts = path.parts
    category = None
    for part in parts:
        if re.match(r"\d{2}-", part):
            category = part
            break

    what = detect_what(content)
    how = detect_how(content)
    scale = detect_scale(content)
    time = detect_time(content)
    patterns = detect_patterns(content)

    # Build the label
    time_display = "∞" if time == "inf" else time
    base_label = f"{what}.{how}.{scale}.{time_display}"
    full_label = base_label
    if patterns:
        full_label += f".{patterns[0]}"

    word_count = len(content.split())

    return {
        "filepath": str(filepath),
        "filename": filename,
        "category": category,
        "pudding_label": full_label,
        "pudding_base": base_label,
        "what": what,
        "what_desc": WHAT_CODES.get(what, "Unknown"),
        "how": how,
        "how_desc": HOW_CODES.get(how, "Unknown"),
        "scale": scale,
        "scale_desc": SCALE_CODES.get(scale, "Unknown"),
        "time": time_display,
        "time_desc": TIME_CODES.get(time, "Unknown"),
        "patterns": patterns,
        "pattern_descs": [PATTERN_CODES.get(p, p) for p in patterns],
        "word_count": word_count,
        "labeled_at": datetime.now().isoformat(),
    }


def label_directory(dirpath: str, output_file: str = None) -> list[dict]:
    """Label all markdown files in a directory."""
    results = []
    path = Path(dirpath)
    
    for md_file in sorted(path.rglob("*.md")):
        result = label_document(str(md_file))
        results.append(result)
        label = result.get("pudding_label", "ERROR")
        print(f"  {label:20s}  {md_file.name}")

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nLabels saved to: {output_file}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pudding_labeler.py <file_or_directory> [output.json]")
        print("  Label a single file:  python pudding_labeler.py document.md")
        print("  Label a directory:    python pudding_labeler.py /path/to/vault/ labels.json")
        sys.exit(1)

    target = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    if os.path.isfile(target):
        result = label_document(target)
        print(f"\n{'='*60}")
        print(f"File:    {result['filename']}")
        print(f"Label:   {result['pudding_label']}")
        print(f"WHAT:    [{result['what']}] {result['what_desc']}")
        print(f"HOW:     [{result['how']}] {result['how_desc']}")
        print(f"SCALE:   [{result['scale']}] {result['scale_desc']}")
        print(f"TIME:    [{result['time']}] {result['time_desc']}")
        if result['patterns']:
            print(f"PATTERNS:")
            for p, d in zip(result['patterns'], result['pattern_descs']):
                print(f"  [{p}] {d}")
        print(f"Words:   {result['word_count']}")
        print(f"{'='*60}")
        if output:
            with open(output, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
    elif os.path.isdir(target):
        print(f"Labeling all .md files in: {target}\n")
        results = label_directory(target, output)
        print(f"\nTotal files labeled: {len(results)}")
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)
