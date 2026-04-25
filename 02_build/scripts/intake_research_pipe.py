"""
Research Pipe Stage 1: Intake
Accept question, extract metadata (question, goal, domain, constraints).
"""

import uuid
from datetime import datetime


def stage_intake(question: str, goal: str = None, 
                domain: str = None, constraints: list = None) -> dict:
    """
    Stage 1: Accept question, extract metadata.
    
    Args:
        question: The research question
        goal: What the researcher will do with the answer
        domain: Academic discipline(s)
        constraints: List of constraints (peer-reviewed, recent, etc.)
    
    Returns:
        intake_output: dict with metadata
    """
    intake_id = str(uuid.uuid4())
    
    intake_output = {
        "intake_id": intake_id,
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "goal": goal or "Understand the domain and available methodologies",
        "domain": domain or "general",
        "constraints": constraints or ["peer-reviewed preferred", "foundational + current"],
        "intent_classification": "science-seeking",
        "loaded_language_flags": []
    }
    
    return intake_output
