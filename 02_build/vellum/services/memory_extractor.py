"""Memory candidate extractor — parse session entries for memory-worthy items.

Scans sheet entries and extracts candidates that might change future
behaviour. The extractor proposes; the ingestion gate decides.

Candidate kinds (from Ewan's verdict):
- preference:           user/agent preference discovered
- correction:           something was wrong, now corrected
- task_outcome:         task completed with measurable result
- new_entity:           new person/tool/system/concept encountered
- repeated_pattern:     same thing observed multiple times
- failed_approach:      tried X, it didn't work
- tool_quirk:           tool behaves unexpectedly
- procedure_improvement: found a better way to do Y
- if_then_lesson:       IF condition THEN do/avoid action
- explicit_remember:    author explicitly says "remember this"

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging
import re

from vellum.models.entry import SheetEntry
from vellum.models.memory import CandidateKind, MemoryCandidate

log = logging.getLogger("vellum.memory_extractor")

# Patterns that signal memory-worthy content
_FAILURE_PATTERNS = re.compile(
    r"(?i)(failed|broke|didn't work|error|bug|regression|reverted|rollback|"
    r"couldn't|blocked|timed out|crashed|wrong)",
)
_CORRECTION_PATTERNS = re.compile(
    r"(?i)(corrected|fixed|was wrong|actually|correction|mistake|"
    r"misunderstood|clarified|updated to)",
)
_LESSON_PATTERNS = re.compile(
    r"(?i)(lesson|learned|takeaway|next time|in future|"
    r"if .+ then|never again|always .+ before|remember to)",
)
_REMEMBER_PATTERNS = re.compile(
    r"(?i)(remember this|note for future|important:|don't forget|"
    r"save this|capture this|record this)",
)
_PREFERENCE_PATTERNS = re.compile(
    r"(?i)(prefer|rather|instead of|better to|default to|always use|never use)",
)
_OUTCOME_PATTERNS = re.compile(
    r"(?i)(completed|delivered|shipped|merged|deployed|passed|"
    r"tests? pass|ci green|pr merged|done)",
)
_PROCEDURE_PATTERNS = re.compile(
    r"(?i)(better way|improved process|streamlined|optimised|"
    r"shortcut|workflow improvement|faster if|easier to)",
)
_TOOL_QUIRK_PATTERNS = re.compile(
    r"(?i)(quirk|workaround|hack|unexpected behaviour|"
    r"undocumented|gotcha|watch out for|caveat)",
)

# Entry types that are worth scanning for memory candidates
_SCANNABLE_TYPES = {
    "agent_write",
    "baton_pass",
    "brief_summary",
    "human_comment",
    "council_answer",
}


def extract_candidates(entry: SheetEntry) -> list[MemoryCandidate]:
    """Extract memory candidates from a single entry.

    Returns zero or more candidates. Each candidate has a kind,
    the extracted content, and a confidence score.
    """
    if entry.entry_type not in _SCANNABLE_TYPES:
        return []

    content = entry.content
    if not content or len(content.strip()) < 10:
        return []

    candidates: list[MemoryCandidate] = []

    def _add(kind: CandidateKind, reasoning: str, confidence: float = 0.6) -> None:
        candidates.append(
            MemoryCandidate(
                source_entry_id=entry.id,
                source_sheet_id=entry.sheet_id,
                agent_id=entry.author,
                kind=kind,
                content=content,
                reasoning=reasoning,
                confidence=confidence,
                epistemic_tier=entry.epistemic_tier,
            )
        )

    if _REMEMBER_PATTERNS.search(content):
        _add("explicit_remember", "Author explicitly flagged for memory", 0.9)

    if _FAILURE_PATTERNS.search(content):
        _add("failed_approach", "Contains failure/error language", 0.7)

    if _CORRECTION_PATTERNS.search(content):
        _add("correction", "Contains correction language", 0.75)

    if _LESSON_PATTERNS.search(content):
        _add("if_then_lesson", "Contains lesson/conditional language", 0.8)

    if _PREFERENCE_PATTERNS.search(content):
        _add("preference", "Contains preference language", 0.65)

    if _PROCEDURE_PATTERNS.search(content):
        _add("procedure_improvement", "Contains process improvement language", 0.7)

    if _TOOL_QUIRK_PATTERNS.search(content):
        _add("tool_quirk", "Contains tool quirk/workaround language", 0.7)

    if entry.entry_type == "baton_pass":
        baton_meta = entry.metadata or {}
        actions = baton_meta.get("actions_required", [])
        if actions:
            _add("task_outcome", "Baton pass with pending actions", 0.65)

    if entry.entry_type == "baton_pass" and _OUTCOME_PATTERNS.search(content):
        _add("task_outcome", "Baton pass with completion language", 0.7)

    return candidates


def extract_from_sheet_entries(entries: list[SheetEntry]) -> list[MemoryCandidate]:
    """Extract memory candidates from a list of entries."""
    all_candidates: list[MemoryCandidate] = []
    for entry in entries:
        candidates = extract_candidates(entry)
        all_candidates.extend(candidates)

    log.info(
        "Extracted %d memory candidates from %d entries",
        len(all_candidates),
        len(entries),
    )
    return all_candidates
