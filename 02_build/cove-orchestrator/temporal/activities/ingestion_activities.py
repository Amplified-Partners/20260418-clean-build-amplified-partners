"""Temporal activities — the ingestion pipeline v2.

v2 (AMP-356): Deterministic PUDDING labelling + 20-field packet.

- Replaces Haiku extraction with deterministic keyword-based labeller
  (pudding_labeler.py) for the 5-char PUDDING label.
- Keeps AI only where it adds value: confidence scoring, canonical_summary,
  claim_type classification, evidence_summary generation.
- Writes full 20-field packet to pudding_packets table.
- Writes to AGE business_brain graph for relationship traversal.
- Exposes all 5 PUDDING dimensions as separate queryable fields.
- Adds recurrence_count (spiral detection) and bridge_terms (Swanson joins).

Pipe shape:
  drop file → deduplicate → label (Python/deterministic) → classify (AI/light)
  → score confidence (AI) → generate summary (AI) → build 20-field packet
  → write to AGE business_brain → audit log → receipt

Canonical data layer: PostgreSQL + pgvector (HNSW) + Apache AGE.
FalkorDB and Qdrant are deprecated — see 00_authority/DATA_ARCHITECTURE.md.

Signed-by: Devon-cb28 | 2026-05-16 | devin-cb283993cf974c7babc3307e140d63e4
Based-on: Devon-c329 | devin-c3297c6e5f464d8fb6d912403b7cc3e6
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import uuid as _uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from temporalio import activity

logger = logging.getLogger("cove.ingestion")

# ── Beast-native paths ──────────────────────────────────────────────
ARCHIVE_DIR = Path("/opt/amplified/archive")
STORE_B_CLEAN = ARCHIVE_DIR / "store_b_clean"
RAW_DIR = Path("/opt/amplified/raw-mac-dumps")
SEEN_HASHES = STORE_B_CLEAN / "seen_hashes.json"

# Pipeline version tag for provenance
PIPELINE_VERSION = "v2-deterministic"

# Runtime pipeline identity (used for signed_by — not a build-time session UUID)
SIGNED_BY = "brain_writer_pipeline"

# ── Ollama (Beast internal) ─────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://172.18.0.3:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# ── PostgreSQL amplified_brain (Beast internal) ──────────────────────
# Canonical data layer: pgvector/HNSW for vectors, relational tables for graph.
# See 00_authority/DATA_ARCHITECTURE.md.
BRAIN_DSN = os.getenv(
    "BRAIN_DSN",
    "postgresql://brain_writer@cove-postgres:5432/amplified_brain",
)


# ═════════════════════════════════════════════════════════════════════
# Data Classes
# ═════════════════════════════════════════════════════════════════════

@dataclass
class IngestionInput:
    """Input for the unified ingestion stage."""
    raw_dir: str = str(RAW_DIR)
    clean_archive: str = str(STORE_B_CLEAN)
    full_rebuild: bool = False
    max_workers: int = 8


@dataclass
class IngestionResult:
    """Result from the unified ingestion stage."""
    success: bool
    new_files: int = 0
    total_unique: int = 0
    elapsed_seconds: float = 0.0
    clean_archive: str = ""
    error: str | None = None


@dataclass
class PuddingInput:
    """Input for the deterministic PUDDING labelling stage (v2)."""
    target_dir: str = str(STORE_B_CLEAN)
    max_workers: int = 4
    limit: int = 0  # 0 = unlimited
    ai_enrich: bool = True  # enable AI enrichment (confidence, summary, claim_type)


@dataclass
class PuddingResult:
    """Result from the PUDDING labelling + packet write stage (v2)."""
    success: bool
    labelled: int = 0
    skipped: int = 0
    errors: int = 0
    packets_written: int = 0
    ai_enriched: int = 0
    bridge_terms_found: int = 0
    error: str | None = None


@dataclass
class MemoryStoreInput:
    """Input for writing to amplified_brain PostgreSQL (pgvector + relational graph)."""
    source_dir: str = str(STORE_B_CLEAN)
    brain_dsn: str = BRAIN_DSN
    batch_size: int = 100


@dataclass
class MemoryStoreResult:
    """Result from writing to amplified_brain PostgreSQL."""
    success: bool
    pg_vectors: int = 0
    pg_entities: int = 0
    errors: int = 0
    error: str | None = None


@dataclass
class PipelineRun:
    """Full pipeline run metadata."""
    run_id: str
    started_at: str
    ingestion: IngestionResult | None = None
    pudding: PuddingResult | None = None
    memory_store: MemoryStoreResult | None = None
    completed_at: str | None = None
    status: str = "running"
    pipeline_version: str = PIPELINE_VERSION


# ═════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════

def sha256_file(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_one(args: tuple[Path, Path]) -> dict | None:
    src, _ = args
    try:
        h = sha256_file(src)
        return {"src": str(src), "hash": h, "size": src.stat().st_size}
    except Exception as e:
        import logging
        logging.getLogger("cove.ingestion").warning(f"Hash failed for {src}: {e}")
        return None

# ═════════════════════════════════════════════════════════════════════
# Activity: Unified Ingestion
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="run_unified_ingestion")
async def run_unified_ingestion(input: IngestionInput) -> IngestionResult:
    """Run the unified ingestion pipeline (dedup + radical naming + attribution).

    Reads raw files from the sovereign dump directory, deduplicates against
    seen_hashes.json, and writes clean, attributed files to store_b_clean.
    """
    import hashlib
    import shutil
    import time
    from concurrent.futures import ProcessPoolExecutor, as_completed

    activity.logger.info(
        f"Ingestion: raw={input.raw_dir}, archive={input.clean_archive}, "
        f"full_rebuild={input.full_rebuild}"
    )

    raw = Path(input.raw_dir)
    archive = Path(input.clean_archive)
    vault = archive
    seen_file = archive / "seen_hashes.json"

    if not raw.exists():
        return IngestionResult(
            success=False,
            clean_archive=str(vault),
            error=f"Raw directory not found: {raw}",
        )

    vault.mkdir(parents=True, exist_ok=True)

    # ── Load seen hashes ──────────────────────────────────────────
    seen: set[str] = set()
    if seen_file.exists() and not input.full_rebuild:
        seen = set(json.loads(seen_file.read_text()))
        activity.logger.info(f"Loaded {len(seen)} seen hashes (incremental)")

    if input.full_rebuild:
        activity.logger.info("Full rebuild — clearing vault")
        shutil.rmtree(vault, ignore_errors=True)
        vault.mkdir(parents=True)
        seen = set()

    # ── Helpers ───────────────────────────────────────────────────
    def sanitize(name: str) -> str:
        clean = "".join(c if c.isalnum() else "-" for c in Path(name).stem)
        return clean.strip("-").lower() or "unnamed"

    def radical_name(filepath: Path, file_hash: str) -> str:
        dt = datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d")
        topic = sanitize(filepath.name)
        short = file_hash[:8]
        return f"{dt}_{topic}_Ewan_Sair_{short}{filepath.suffix}"

    # ── Collect candidates ────────────────────────────────────────
    candidates: list[tuple[Path, Path]] = []
    for src in raw.rglob("*"):
        if not src.is_file() or src.name.startswith("._"):
            continue
        candidates.append((src, vault / radical_name(src, "placeholder")))

    activity.logger.info(f"Found {len(candidates)} raw files")

    # ── Hash in parallel ──────────────────────────────────────────
    start = time.time()

    new_items: list[dict] = []
    with ProcessPoolExecutor(max_workers=input.max_workers) as ex:
        futures = {ex.submit(hash_one, c): c for c in candidates}
        for fut in as_completed(futures):
            res = fut.result()
            if res and res["hash"] not in seen:
                seen.add(res["hash"])
                new_items.append(res)

    # ── Copy + attribute ──────────────────────────────────────────
    copied = 0
    for item in new_items:
        src = Path(item["src"])
        real_name = radical_name(src, item["hash"])
        real_target = vault / real_name
        shutil.copy2(src, real_target)

        # Light attribution for JSON dumps
        if real_target.suffix in {".json", ".jsonl"}:
            try:
                data = json.loads(real_target.read_text(errors="ignore"))
                if isinstance(data, dict):
                    data["_ingestion"] = {
                        "date": datetime.now(timezone.utc).isoformat(),
                        "original": str(src),
                        "hash": item["hash"],
                        "status": "cleaned_fast",
                    }
                    real_target.write_text(json.dumps(data, indent=2))
            except Exception:
                pass

        copied += 1
        if copied % 1000 == 0:
            activity.logger.info(f"Progress: {copied} new files cleaned...")

    seen_file.write_text(json.dumps(sorted(seen)))
    elapsed = time.time() - start

    activity.logger.info(
        f"Ingestion complete: {copied} new, {len(seen)} total unique, "
        f"{elapsed:.1f}s"
    )

    return IngestionResult(
        success=True,
        new_files=copied,
        total_unique=len(seen),
        elapsed_seconds=round(elapsed, 1),
        clean_archive=str(vault),
    )


# ═════════════════════════════════════════════════════════════════════
# Deterministic PUDDING Labeller (inlined from pudding_labeler.py)
# ═════════════════════════════════════════════════════════════════════

# PUDDING taxonomy reference — 5 dimensions
WHAT_CODES = {
    "E": "Entity", "R": "Relation", "P": "Process", "S": "State",
    "C": "Constraint", "I": "Information", "M": "Meta",
}
HOW_CODES = {
    "+": "Amplifying", "-": "Dampening", "~": "Oscillating",
    ">": "Tipping", "=": "Stable", "!": "Disrupting", "?": "Emerging",
}
SCALE_CODES = {
    "1": "Singular", "2": "Pair", "3": "Small group",
    "4": "Network", "5": "System", "6": "Universal", "0": "Scale-free",
}
TIME_CODES = {
    "i": "Instant", "s": "Short", "m": "Medium", "l": "Long",
    "p": "Permanent", "inf": "Timeless", "v": "Variable",
}
PATTERN_CODES = {
    "LOG-CAU": "Causal", "LOG-COR": "Correlative", "LOG-CON": "Conditional",
    "LOG-TRA": "Transitive", "LOG-ANA": "Analogical", "LOG-ABD": "Abductive",
    "MAT-LIN": "Linear", "MAT-EXG": "Exponential growth",
    "MAT-EXD": "Exponential decay", "MAT-DIM": "Diminishing returns",
    "MAT-SIG": "S-Curve", "MAT-PAR": "Power Law", "MAT-CYC": "Cyclical",
    "MAT-TIP": "Threshold", "MAT-TRD": "Inverse/Trade-off",
    "SYS-RFL": "Reinforcing feedback", "SYS-BFL": "Balancing feedback",
    "SYS-CAS": "Cascade", "SYS-NET": "Network effect",
    "SYS-BOT": "Bottleneck", "SYS-EMR": "Emergence",
    "SYS-ENT": "Entropy/Decay", "SYS-ACC": "Accumulation",
    "BEH-STA": "Status quo bias", "BEH-LOS": "Loss aversion",
    "BEH-ANC": "Anchoring", "BEH-SUN": "Sunk cost",
    "BEH-COM": "Compounding habits",
    "STR-HUB": "Hub and spoke", "STR-HIE": "Hierarchy",
    "STR-PIP": "Pipeline", "STR-PAR": "Parallel", "STR-LAY": "Layered",
}

# HOW symbol → compressed code mapping (for pudding_code generation)
_HOW_COMPRESSED = {
    "+": "A", "-": "D", "~": "O", ">": "T", "=": "S", "!": "X", "?": "E",
}
# TIME → compressed code mapping
_TIME_COMPRESSED = {
    "i": "I", "s": "S", "m": "M", "l": "L", "p": "P", "inf": "T", "v": "V",
}


def _detect_what(text: str) -> str:
    t = text.lower()
    scores: dict[str, int] = {"E": 0, "R": 0, "P": 0, "S": 0, "C": 0, "I": 0, "M": 0}
    for w in ["agent", "server", "database", "tool", "platform", "software", "engine", "module", "component", "system"]:
        scores["E"] += t.count(w)
    for w in ["connect", "integrat", "depend", "link", "relationship", "between", "bridge", "maps to"]:
        scores["R"] += t.count(w)
    for w in ["pipeline", "workflow", "step", "phase", "process", "ingest", "extract", "transform", "build", "deploy", "execute"]:
        scores["P"] += t.count(w)
    for w in ["status", "current", "state", "snapshot", "healthy", "failed", "running", "complete"]:
        scores["S"] += t.count(w)
    for w in ["rule", "principle", "immutable", "non-negotiable", "must", "never", "constraint", "limit", "gdpr", "compliance"]:
        scores["C"] += t.count(w)
    for w in ["data", "insight", "metric", "report", "finding", "signal", "statistic", "number", "figure", "table"]:
        scores["I"] += t.count(w)
    for w in ["framework", "taxonomy", "model", "architecture", "spec", "design", "abstract", "meta", "rubric", "methodology", "schema", "ontology", "classification", "dimension", "category"]:
        scores["M"] += t.count(w) * 2
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "I"


def _detect_how(text: str) -> str:
    t = text.lower()
    scores: dict[str, int] = {"+": 0, "-": 0, "~": 0, ">": 0, "=": 0, "!": 0, "?": 0}
    scores["+"] += sum(t.count(w) for w in ["grow", "amplif", "scale", "expand", "compound", "accelerat", "viral"])
    scores["-"] += sum(t.count(w) for w in ["decay", "friction", "reduce", "decline", "deprecat", "legacy", "debt"])
    scores["~"] += sum(t.count(w) for w in ["cycle", "recurring", "periodic", "seasonal", "oscillat", "wave"])
    scores[">"] += sum(t.count(w) for w in ["threshold", "tipping", "breaking", "critical", "pivot", "transform"])
    scores["="] += sum(t.count(w) for w in ["stable", "maintain", "standard", "consistent", "baseline", "equilibrium", "persist", "reference", "canonical", "definitive", "specification"])
    scores["!"] += sum(t.count(w) for w in ["disrupt", "innovat", "revolution", "paradigm", "overhaul", "replace"])
    scores["?"] += sum(t.count(w) for w in ["emerging", "prototype", "experiment", "explore", "potential", "uncertain", "mvp", "draft"])
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "="


def _detect_scale(text: str) -> str:
    t = text.lower()
    scores: dict[str, int] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "0": 0}
    scores["1"] += sum(t.count(w) for w in ["individual", "single", "personal", "one person", "sole"])
    scores["2"] += sum(t.count(w) for w in ["pair", "bilateral", "dialogue", "two ", "both"])
    scores["3"] += sum(t.count(w) for w in ["team", "small group", "department", "squad", "crew"])
    scores["4"] += sum(t.count(w) for w in ["organisation", "organization", "company", "network", "ecosystem", "community", "smb", "business"])
    scores["5"] += sum(t.count(w) for w in ["market", "industry", "sector", "economy", "society", "uk smb"])
    scores["6"] += sum(t.count(w) for w in ["universal", "fundamental", "law", "constant", "archetype", "human nature"])
    scores["0"] += sum(t.count(w) for w in ["fractal", "scale-free", "any level", "recursive", "self-similar"])
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "4"


def _detect_time(text: str) -> str:
    t = text.lower()
    scores: dict[str, int] = {"i": 0, "s": 0, "m": 0, "l": 0, "p": 0, "inf": 0, "v": 0}
    scores["i"] += sum(t.count(w) for w in ["instant", "immediate", "real-time", "millisecond", "alert", "trigger"])
    scores["s"] += sum(t.count(w) for w in ["daily", "today", "this week", "sprint", "quick", "urgent"])
    scores["m"] += sum(t.count(w) for w in ["quarter", "monthly", "phase", "milestone", "weeks", "iteration"])
    scores["l"] += sum(t.count(w) for w in ["year", "annual", "long-term", "vision", "strategy", "multi-year", "roadmap"])
    scores["p"] += sum(t.count(w) for w in ["permanent", "forever", "lifetime", "enduring"])
    scores["inf"] += sum(t.count(w) for w in ["timeless", "always true", "universal", "principle", "immutable", "eternal", "non-negotiable", "fundamental", "taxonomy", "canonical", "reference", "definitive"])
    scores["v"] += sum(t.count(w) for w in ["depends", "variable", "context-dependent", "varies"])
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "m"


def _detect_patterns(text: str) -> list[str]:
    t = text.lower()
    scores: dict[str, int] = {}
    kw_map = {
        "LOG-CAU": ["cause", "causes", "because", "therefore", "leads to", "results in"],
        "LOG-COR": ["correlat", "moves together", "linked to", "associated"],
        "LOG-CON": ["if ", "then ", "conditional", "when ", "trigger"],
        "LOG-TRA": ["chain", "transitive", "indirect"],
        "LOG-ANA": ["analogy", "similar to", "like a", "as if", "metaphor"],
        "MAT-LIN": ["proportional", "linear", "each additional", "per unit"],
        "MAT-EXG": ["exponential", "viral", "compound", "snowball", "accelerat"],
        "MAT-EXD": ["death spiral", "declining", "hemorrhaging", "losing"],
        "MAT-DIM": ["diminishing", "plateau", "less effective", "saturat"],
        "MAT-SIG": ["adoption curve", "s-curve", "penetration"],
        "MAT-PAR": ["80/20", "pareto", "power law", "most of the"],
        "MAT-CYC": ["seasonal", "quarterly", "cycle", "recurring", "periodic"],
        "SYS-RFL": ["reinforc", "positive feedback", "virtuous", "flywheel", "success breeds"],
        "SYS-BFL": ["self-correct", "balanc", "thermostat", "homeostasis"],
        "SYS-CAS": ["cascade", "domino", "chain reaction", "ripple"],
        "SYS-NET": ["network effect", "more users", "marketplace", "platform"],
        "SYS-BOT": ["bottleneck", "single point", "constraint", "blocking"],
        "SYS-EMR": ["emergence", "greater than the sum", "synergy", "holistic"],
        "SYS-ACC": ["compound", "accumulate", "build over time", "1% daily"],
        "BEH-STA": ["always done it", "status quo", "resistance to change"],
        "BEH-LOS": ["loss aversion", "fear of", "risk averse", "won't switch"],
        "STR-HUB": ["hub and spoke", "central", "owner who", "single point of contact"],
        "STR-PIP": ["pipeline", "sequential", "step by step", "stage"],
        "STR-PAR": ["parallel", "concurrent", "simultaneous", "multi-stream"],
        "STR-LAY": ["layer", "stack", "tier", "built on top"],
    }
    for pattern, keywords in kw_map.items():
        score = sum(t.count(kw) for kw in keywords)
        if score > 0:
            scores[pattern] = score
    sorted_patterns = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [p[0] for p in sorted_patterns[:3]]


def _extract_bridge_terms(text: str) -> list[str]:
    """Extract candidate bridge terms for Swanson cross-domain joins.

    Bridge terms are nouns/phrases that appear in multiple domain contexts —
    they are the B in A→B→C discovery. We use a keyword heuristic to find
    terms that signal cross-domain connectivity.
    """
    t = text.lower()
    candidates: list[str] = []
    bridge_signals = [
        "feedback", "threshold", "network", "constraint", "bottleneck",
        "compound", "decay", "cycle", "emergence", "signal",
        "pattern", "rhythm", "cascade", "equilibrium", "resilience",
        "amplif", "friction", "leverage", "momentum", "inertia",
        "saturation", "tipping", "contagion", "diffusion", "adaptation",
    ]
    for term in bridge_signals:
        if term in t:
            candidates.append(term)
    return candidates[:10]


def _label_content(content: str, filepath: str) -> dict[str, Any]:
    """Deterministic PUDDING labelling — no LLM, pure keyword heuristics."""
    what = _detect_what(content)
    how = _detect_how(content)
    scale = _detect_scale(content)
    time_val = _detect_time(content)
    patterns = _detect_patterns(content)

    time_display = "∞" if time_val == "inf" else time_val
    base_label = f"{what}.{how}.{scale}.{time_display}"
    full_label = base_label
    if patterns:
        full_label += f".{patterns[0]}"

    # Compressed 4-char code (per PUDDING Code Specification v1)
    compressed = (
        what
        + _HOW_COMPRESSED.get(how, "S")
        + scale
        + _TIME_COMPRESSED.get(time_val, "M")
    )

    return {
        "pudding_label": full_label,
        "pudding_code": compressed,
        "dim_what": what,
        "dim_how": how,
        "dim_scale": scale,
        "dim_time": time_val,
        "dim_pattern": patterns[0] if patterns else None,
        "patterns_all": patterns,
        "bridge_terms": _extract_bridge_terms(content),
        "word_count": len(content.split()),
    }


# ═════════════════════════════════════════════════════════════════════
# AI Enrichment (light pass — confidence, summary, claim_type)
# ═════════════════════════════════════════════════════════════════════

_AI_ENRICHMENT_PROMPT = (
    "You are classifying a document for a knowledge base. Given the text below, "
    "return ONLY a JSON object with these fields:\n"
    '  "confidence": float 0.0-1.0 (how confident are you in the classification),\n'
    '  "canonical_summary": string (one sentence summarising the document),\n'
    '  "claim_type": string (one of: principle, framework, sop, technique, '
    "case_study, hypothesis, recipe, content_asset, business_logic, raw_notes),\n"
    '  "evidence_summary": string (one sentence describing the evidence basis)\n'
    "Return ONLY valid JSON. No markdown, no explanation."
)


async def _ai_enrich(content: str, client: Any, sem: Any) -> dict[str, Any] | None:
    """Light AI pass for fields that need semantic understanding.

    Returns parsed enrichment dict on success, or None on failure.
    Failures are logged at ERROR level with full exception detail
    (Radical Honesty + Radical Transparency — never silently swallow).
    The caller is responsible for recording the failure reason in the
    audit trail so the system remains inspectable.
    """
    try:
        async with sem:
            response = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=_AI_ENRICHMENT_PROMPT,
                messages=[{"role": "user", "content": content[:3000]}],
                temperature=0.0,
            )
            raw = response.content[0].text.strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        logger.error("AI enrichment JSON parse failed: %s", e)
        return None
    except Exception as e:
        logger.error("AI enrichment failed (%s): %s", type(e).__name__, e)
        return None


# ═════════════════════════════════════════════════════════════════════
# Activity: PUDDING Extraction v2 (Deterministic + Light AI)
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="run_pudding_extraction")
async def run_pudding_extraction(input: PuddingInput) -> PuddingResult:
    """Run the PUDDING labeller v2 against clean vault files.

    v2 pipe (AMP-356):
    1. Deterministic keyword labelling (Python — zero LLM cost)
    2. Optional light AI enrichment (confidence, summary, claim_type)
    3. Build 20-field packet
    4. Write packet to pudding_packets table
    5. Write to AGE business_brain graph
    6. Audit log + receipt
    """
    import asyncio
    import asyncpg

    run_id = f"pudding-v2-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{_uuid.uuid4().hex[:8]}"
    activity.logger.info(
        f"PUDDING v2 (deterministic): dir={input.target_dir}, run_id={run_id}"
    )

    target = Path(input.target_dir)
    if not target.exists():
        return PuddingResult(
            success=False,
            error=f"Target directory not found: {target}",
        )

    # ── Collect eligible files ────────────────────────────────────
    files: list[Path] = []
    for fp in target.rglob("*"):
        if fp.is_file() and fp.suffix in {".md", ".txt"}:
            files.append(fp)

    if input.limit > 0:
        files = files[: input.limit]

    activity.logger.info(f"Eligible files: {len(files)}")

    if not files:
        return PuddingResult(success=True, labelled=0, skipped=0)

    # ── Set up AI client (optional) ───────────────────────────────
    ai_client = None
    ai_sem = asyncio.Semaphore(input.max_workers)
    if input.ai_enrich:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            try:
                from anthropic import AsyncAnthropic
                ai_client = AsyncAnthropic(api_key=api_key)
            except ImportError:
                activity.logger.warning(
                    "anthropic package not installed — AI enrichment disabled"
                )

    # ── Connect to amplified_brain ────────────────────────────────
    dsn = os.getenv("BRAIN_DSN", BRAIN_DSN)
    try:
        conn = await asyncpg.connect(dsn)
    except Exception as e:
        return PuddingResult(
            success=False,
            error=f"PostgreSQL connection failed: {e}",
        )

    labelled = 0
    skipped = 0
    errors = 0
    packets_written = 0
    ai_enriched = 0
    bridge_terms_found = 0

    try:
        # ── Initialise AGE for this connection ────────────────────
        await conn.execute("LOAD 'age'")
        await conn.execute(
            "SET search_path = ag_catalog, \"$user\", public"
        )

        for fp in files:
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")

                # Skip empty files
                if not content.strip():
                    skipped += 1
                    continue

                file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

                # Skip already-processed files (dedup by hash)
                existing = await conn.fetchval(
                    "SELECT 1 FROM pudding_packets WHERE file_hash = $1",
                    file_hash,
                )
                if existing:
                    skipped += 1
                    continue

                # ── Step 1: Deterministic labelling ───────────────
                label_result = _label_content(content, str(fp))
                labelled += 1

                # ── Step 2: AI enrichment (optional) ──────────────
                ai_fields: dict[str, Any] = {
                    "confidence": None,
                    "canonical_summary": None,
                    "claim_type": None,
                    "evidence_summary": None,
                }
                ai_enrichment_error: str | None = None
                if ai_client is not None:
                    enrichment = await _ai_enrich(content, ai_client, ai_sem)
                    if enrichment is None:
                        ai_enrichment_error = "AI enrichment returned None (see logs for detail)"
                    if enrichment:
                        ai_fields["confidence"] = min(
                            1.0, max(0.0, float(enrichment.get("confidence", 0.5)))
                        )
                        ai_fields["canonical_summary"] = str(
                            enrichment.get("canonical_summary", "")
                        )[:500]
                        claim = str(enrichment.get("claim_type", "raw_notes"))
                        valid_claims = {
                            "principle", "framework", "sop", "technique",
                            "case_study", "hypothesis", "recipe",
                            "content_asset", "business_logic", "raw_notes",
                        }
                        ai_fields["claim_type"] = (
                            claim if claim in valid_claims else "raw_notes"
                        )
                        ai_fields["evidence_summary"] = str(
                            enrichment.get("evidence_summary", "")
                        )[:500]
                        ai_enriched += 1

                bridge_terms = label_result["bridge_terms"]
                if bridge_terms:
                    bridge_terms_found += len(bridge_terms)

                # ── Step 3: Write 20-field packet ─────────────────
                packet_id = _uuid.uuid4()
                row = await conn.fetchrow(
                    """INSERT INTO pudding_packets (
                        id, file_hash, file_path, filename,
                        pudding_label, pudding_code,
                        dim_what, dim_how, dim_scale, dim_time, dim_pattern,
                        confidence, canonical_summary, claim_type, evidence_summary,
                        bridge_terms, recurrence_count,
                        word_count, source_agent, run_id, signed_by
                    ) VALUES (
                        $1, $2, $3, $4,
                        $5, $6,
                        $7, $8, $9, $10, $11,
                        $12, $13, $14, $15,
                        $16, $17,
                        $18, $19, $20, $21
                    )
                    ON CONFLICT (file_hash) DO UPDATE SET
                        pudding_label = EXCLUDED.pudding_label,
                        pudding_code = EXCLUDED.pudding_code,
                        dim_what = EXCLUDED.dim_what,
                        dim_how = EXCLUDED.dim_how,
                        dim_scale = EXCLUDED.dim_scale,
                        dim_time = EXCLUDED.dim_time,
                        dim_pattern = EXCLUDED.dim_pattern,
                        confidence = EXCLUDED.confidence,
                        canonical_summary = EXCLUDED.canonical_summary,
                        claim_type = EXCLUDED.claim_type,
                        evidence_summary = EXCLUDED.evidence_summary,
                        bridge_terms = EXCLUDED.bridge_terms,
                        recurrence_count = pudding_packets.recurrence_count + 1,
                        updated_at = now()
                    RETURNING (xmax = 0) AS inserted""",
                    packet_id,
                    file_hash,
                    str(fp),
                    fp.name,
                    label_result["pudding_label"],
                    label_result["pudding_code"],
                    label_result["dim_what"],
                    label_result["dim_how"],
                    label_result["dim_scale"],
                    label_result["dim_time"],
                    label_result["dim_pattern"],
                    ai_fields["confidence"],
                    ai_fields["canonical_summary"],
                    ai_fields["claim_type"],
                    ai_fields["evidence_summary"],
                    bridge_terms,
                    1,  # recurrence_count starts at 1
                    label_result["word_count"],
                    "deterministic-labeler-v2",
                    run_id,
                    SIGNED_BY,
                )
                was_insert = row is not None and row["inserted"]
                if was_insert:
                    packets_written += 1

                # ── Step 4: Write to AGE business_brain graph ─────
                def _esc(val: str) -> str:
                    """Escape a value for embedding in Cypher string literals."""
                    return val.replace("\\", "\\\\").replace("'", "''")

                safe_name = _esc(fp.name)
                safe_label = _esc(label_result["pudding_label"])
                safe_code = _esc(label_result["pudding_code"])
                safe_hash = _esc(file_hash)
                safe_dim_what = _esc(label_result["dim_what"])
                safe_dim_how = _esc(label_result["dim_how"])
                safe_dim_scale = _esc(label_result["dim_scale"])
                safe_dim_time = _esc(label_result["dim_time"])

                # Create Document vertex
                await conn.execute(
                    f"""SELECT * FROM cypher('business_brain', $$
                        MERGE (d:Document {{file_hash: '{safe_hash}'}})
                        SET d.name = '{safe_name}',
                            d.pudding_label = '{safe_label}',
                            d.pudding_code = '{safe_code}',
                            d.dim_what = '{safe_dim_what}',
                            d.dim_how = '{safe_dim_how}',
                            d.dim_scale = '{safe_dim_scale}',
                            d.dim_time = '{safe_dim_time}'
                        RETURN d
                    $$) AS (v agtype)"""
                )

                # Create Pattern vertex + edge if pattern detected
                if label_result["dim_pattern"]:
                    safe_pattern = _esc(label_result["dim_pattern"])
                    pattern_name = PATTERN_CODES.get(
                        label_result["dim_pattern"], label_result["dim_pattern"]
                    ) or label_result["dim_pattern"]
                    safe_pattern_name = _esc(pattern_name)
                    await conn.execute(
                        f"""SELECT * FROM cypher('business_brain', $$
                            MERGE (p:Pattern {{code: '{safe_pattern}'}})
                            SET p.name = '{safe_pattern_name}'
                            WITH p
                            MATCH (d:Document {{file_hash: '{safe_hash}'}})
                            MERGE (d)-[:EXHIBITS_PATTERN]->(p)
                            RETURN p
                        $$) AS (v agtype)"""
                    )

                # Create bridge term edges
                for term in bridge_terms[:5]:
                    safe_term = _esc(term)
                    await conn.execute(
                        f"""SELECT * FROM cypher('business_brain', $$
                            MERGE (c:Concept {{name: '{safe_term}'}})
                            WITH c
                            MATCH (d:Document {{file_hash: '{safe_hash}'}})
                            MERGE (d)-[:HAS_CONCEPT]->(c)
                            RETURN c
                        $$) AS (v agtype)"""
                    )

                # ── Step 5: Audit log ─────────────────────────────
                await conn.execute(
                    """INSERT INTO audit_log
                       (actor, action, resource_type, resource_id, details)
                    VALUES ($1, $2, $3, $4, $5::jsonb)""",
                    SIGNED_BY,
                    "pudding.packet_written",
                    "pudding_packet",
                    str(packet_id),
                    json.dumps({
                        "file": fp.name,
                        "file_hash": file_hash,
                        "pudding_label": label_result["pudding_label"],
                        "pudding_code": label_result["pudding_code"],
                        "ai_enriched": ai_client is not None and ai_fields["confidence"] is not None,
                        "ai_enrichment_error": ai_enrichment_error,
                        "bridge_terms_count": len(bridge_terms),
                        "run_id": run_id,
                    }),
                )

                # Progress logging
                if labelled % 100 == 0:
                    activity.logger.info(
                        f"Progress: {labelled} labelled, {packets_written} written, "
                        f"{errors} errors"
                    )

            except Exception as e:
                errors += 1
                activity.logger.warning(f"PUDDING v2 failed for {fp.name}: {e}")

    finally:
        await conn.close()

    activity.logger.info(
        f"PUDDING v2 complete: {labelled} labelled, {packets_written} packets, "
        f"{ai_enriched} AI-enriched, {bridge_terms_found} bridge terms, "
        f"{skipped} skipped, {errors} errors"
    )

    return PuddingResult(
        success=errors == 0,
        labelled=labelled,
        skipped=skipped,
        errors=errors,
        packets_written=packets_written,
        ai_enriched=ai_enriched,
        bridge_terms_found=bridge_terms_found,
        error=f"{errors} labelling failures" if errors else None,
    )


# ═════════════════════════════════════════════════════════════════════
# Activity: Memory Store Writer
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="write_to_memory_stores")
async def write_to_memory_stores(input: MemoryStoreInput) -> MemoryStoreResult:
    """DEPRECATED by AMP-302 — use canonical_writer.write_canonical_vectors instead.

    This activity bypasses the manifest layer and writes without full provenance.
    Kept for backward compatibility but raises on execution.

    Canonical data layer — see 00_authority/DATA_ARCHITECTURE.md.
    Replacement — see canonical_writer.py (AMP-302 Ticket 3).

    Deprecated-by: Devon-0de2 | 2026-05-11 | AMP-302
    """
    raise RuntimeError(
        "DEPRECATED: write_to_memory_stores retired by AMP-302. "
        "Use canonical_writer.write_canonical_vectors instead. "
        "All writes must go through the manifest-first canonical pipeline."
    )
    import asyncpg
    import yaml

    activity.logger.info(
        f"Memory store write: source={input.source_dir}, "
        f"dsn=***@{input.brain_dsn.split('@')[-1] if '@' in input.brain_dsn else 'localhost'}"
    )

    source = Path(input.source_dir)
    if not source.exists():
        return MemoryStoreResult(
            success=False,
            error=f"Source directory not found: {source}",
        )

    pg_vectors = 0
    pg_entities = 0
    errors = 0

    # ── Collect PUDDING-labelled files ────────────────────────────
    labelled_files: list[Path] = []
    for fp in source.rglob("*.md"):
        try:
            head = fp.read_text(encoding="utf-8", errors="ignore")[:2000]
            if "lbd_attribution" in head and "PUDDING" in head:
                labelled_files.append(fp)
        except Exception:
            pass

    activity.logger.info(f"Found {len(labelled_files)} PUDDING-labelled files")

    if not labelled_files:
        return MemoryStoreResult(success=True)

    # ── Connect to amplified_brain ────────────────────────────────
    try:
        conn = await asyncpg.connect(input.brain_dsn)
    except Exception as e:
        return MemoryStoreResult(
            success=False,
            error=f"PostgreSQL connection failed: {e}",
        )

    try:
        # ── Process in batches ────────────────────────────────────
        for i in range(0, len(labelled_files), input.batch_size):
            batch = labelled_files[i : i + input.batch_size]

            for fp in batch:
                try:
                    content = fp.read_text(encoding="utf-8", errors="ignore")

                    # Extract frontmatter fields
                    fm: dict[str, Any] = {"file": str(fp)}
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            try:
                                parsed_fm = yaml.safe_load(parts[1])
                                if isinstance(parsed_fm, dict):
                                    fm.update(parsed_fm)
                            except Exception as e:
                                activity.logger.warning(
                                    f"Failed to parse YAML for {fp.name}: {e}"
                                )

                    # Extract PUDDING taxonomy fields
                    concepts = fm.get("concepts", [])
                    concept_names = [
                        c.get("name")
                        for c in concepts
                        if isinstance(c, dict) and c.get("name")
                    ]
                    domains = fm.get("domains", [])
                    domain_names = [
                        d.get("name")
                        for d in domains
                        if isinstance(d, dict) and d.get("name")
                    ]
                    doc_type = fm.get("type", "unknown")

                    # Deterministic ID from file path
                    file_hash = hashlib.sha256(str(fp).encode()).hexdigest()
                    vec_id = _uuid.UUID(file_hash[:32])

                    # ── Upsert knowledge_vectors row ──────────────
                    metadata = {
                        "taxonomy_version": fm.get("taxonomy_version", "unknown"),
                        "concepts": concept_names,
                        "domains": domain_names,
                        "doc_type": doc_type,
                        "has_recipes": bool(fm.get("recipes")),
                        "has_signals": bool(fm.get("signals")),
                        "source_count": len(fm.get("sources", [])),
                    }

                    await conn.execute(
                        """INSERT INTO knowledge_vectors
                           (id, content, source, source_type, metadata)
                        VALUES ($1, $2, $3, $4, $5::jsonb)
                        ON CONFLICT (id) DO UPDATE SET
                           content = EXCLUDED.content,
                           metadata = EXCLUDED.metadata,
                           updated_at = now()""",
                        vec_id,
                        content[:4000],
                        str(fp),
                        doc_type,
                        json.dumps(metadata),
                    )
                    pg_vectors += 1

                    # ── Upsert entity per concept ─────────────────
                    for concept in concepts:
                        if not isinstance(concept, dict) or not concept.get("name"):
                            continue
                        ent_id = _uuid.UUID(
                            hashlib.sha256(concept["name"].encode()).hexdigest()[:32]
                        )
                        props = {
                            "pudding_code": concept.get("pudding_code", ""),
                            "description": concept.get("description", ""),
                            "confidence": concept.get("confidence", 0.0),
                            "source_file": str(fp),
                        }
                        await conn.execute(
                            """INSERT INTO entities
                               (id, name, entity_type, summary, properties)
                            VALUES ($1, $2, $3, $4, $5::jsonb)
                            ON CONFLICT (id) DO UPDATE SET
                               properties = entities.properties || EXCLUDED.properties,
                               updated_at = now()""",
                            ent_id,
                            concept["name"],
                            "concept",
                            concept.get("description", ""),
                            json.dumps(props),
                        )
                        pg_entities += 1

                except Exception as e:
                    errors += 1
                    activity.logger.warning(
                        f"Memory write failed for {fp.name}: {e}"
                    )

            activity.logger.info(
                f"Batch {i // input.batch_size + 1}: "
                f"vectors={pg_vectors}, entities={pg_entities}, "
                f"errors={errors}"
            )

    finally:
        await conn.close()

    activity.logger.info(
        f"Memory store complete: {pg_vectors} vectors, "
        f"{pg_entities} entities, {errors} errors"
    )

    return MemoryStoreResult(
        success=errors == 0,
        pg_vectors=pg_vectors,
        pg_entities=pg_entities,
        errors=errors,
        error=f"{errors} write failures" if errors else None,
    )


# ═════════════════════════════════════════════════════════════════════
# Activity: Log Pipeline Run
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="log_pipeline_run")
async def log_pipeline_run(run: PipelineRun) -> None:
    """Log a pipeline run to PostgreSQL for observability.

    v2: includes pudding_packets_written, pudding_ai_enriched,
    pudding_bridge_terms_found, and pipeline_version.
    """
    import asyncpg

    dsn = os.getenv("BRAIN_DSN", BRAIN_DSN)
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            """INSERT INTO pipeline_runs
            (run_id, started_at, ingestion_new_files, ingestion_total_unique,
             ingestion_elapsed, pudding_labelled, pudding_skipped, pudding_errors,
             memory_pg_vectors, memory_pg_entities, memory_errors,
             completed_at, status,
             pudding_packets_written, pudding_ai_enriched,
             pudding_bridge_terms_found, pipeline_version)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17)
            ON CONFLICT (run_id) DO UPDATE SET
              completed_at = $12, status = $13,
              pudding_packets_written = $14, pudding_ai_enriched = $15,
              pudding_bridge_terms_found = $16, pipeline_version = $17""",
            run.run_id,
            run.started_at,
            run.ingestion.new_files if run.ingestion else 0,
            run.ingestion.total_unique if run.ingestion else 0,
            run.ingestion.elapsed_seconds if run.ingestion else 0,
            run.pudding.labelled if run.pudding else 0,
            run.pudding.skipped if run.pudding else 0,
            run.pudding.errors if run.pudding else 0,
            run.memory_store.pg_vectors if run.memory_store else 0,
            run.memory_store.pg_entities if run.memory_store else 0,
            run.memory_store.errors if run.memory_store else 0,
            run.completed_at,
            run.status,
            run.pudding.packets_written if run.pudding else 0,
            run.pudding.ai_enriched if run.pudding else 0,
            run.pudding.bridge_terms_found if run.pudding else 0,
            run.pipeline_version,
        )
    finally:
        await conn.close()
