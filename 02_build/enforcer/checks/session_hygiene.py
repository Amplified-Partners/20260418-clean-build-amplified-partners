# Authored by Claude (Haiku 4.5), 2026-03-11
# Merged into clean-build/02_build/enforcer/checks/ by Devon (Devin session devin-1bdaf31798874921940598bed17ca9e3), 2026-05-04 (AMP-77)
"""Session hygiene checks — validates SESSION-STATE.md baton file."""

import os
import re
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from pathlib import Path


@dataclass
class SessionCheckResult:
    name: str
    status: str
    message: str
    severity: str
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


async def check_session_state(
    session_state_path: str,
    max_age_hours: int = 24,
) -> SessionCheckResult:
    now = datetime.now(timezone.utc)
    path = Path(session_state_path)

    if not path.exists():
        return SessionCheckResult(
            name="session_hygiene", status="fail",
            message="SESSION-STATE.md not found",
            severity="critical",
            timestamp=now.isoformat(),
            duration_ms=0,
            details={"path": session_state_path, "exists": False}
        )

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")

        # Check required sections
        required = ["What Happened This Session", "What This Means", "Ewan Needs To Do"]
        found_sections = []
        missing_sections = []
        for section in required:
            if section.lower() in content.lower():
                found_sections.append(section)
            else:
                missing_sections.append(section)

        # Parse timestamp - look for "Last updated" line
        file_age_hours = None
        for line in lines[:10]:
            # Match patterns like "Last updated: 2026-03-12..." or "**Last updated**: 12 March 2026, 15:00 UTC"
            match = re.search(r"(\d{4})-(\d{2})-(\d{2})", line)
            if match and "updated" in line.lower():
                try:
                    date_str = match.group(0)
                    file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    file_age_hours = (now - file_date).total_seconds() / 3600
                except:
                    pass
                break

        # Determine status
        issues = []
        if missing_sections:
            issues.append(f"Missing sections: {missing_sections}")
        if file_age_hours and file_age_hours > max_age_hours:
            issues.append(f"File is {file_age_hours:.0f}h old (max {max_age_hours}h)")

        elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000

        if issues:
            return SessionCheckResult(
                name="session_hygiene", status="warn",
                message="; ".join(issues),
                severity="warning",
                timestamp=now.isoformat(),
                duration_ms=elapsed,
                details={"path": session_state_path, "found_sections": found_sections, "missing_sections": missing_sections, "age_hours": file_age_hours}
            )

        return SessionCheckResult(
            name="session_hygiene", status="pass",
            message="SESSION-STATE.md is current and complete",
            severity="info",
            timestamp=now.isoformat(),
            duration_ms=elapsed,
            details={"path": session_state_path, "found_sections": found_sections, "age_hours": file_age_hours}
        )

    except Exception as e:
        return SessionCheckResult(
            name="session_hygiene", status="fail",
            message=f"Session hygiene check failed: {str(e)}",
            severity="critical",
            timestamp=now.isoformat(),
            duration_ms=0,
            details={"error": str(e)}
        )
