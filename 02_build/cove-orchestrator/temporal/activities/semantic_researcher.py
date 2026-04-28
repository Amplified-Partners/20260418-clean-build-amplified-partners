import json
from temporalio import activity
from typing import Dict, Any, List

@activity.defn
async def fetch_semantic_scholar_papers(query: str) -> List[Dict[str, str]]:
    """
    Ingestion: Hits the research pipe (Semantic Scholar / Perplexity) to pull
    peer-reviewed papers on influence, semantics, and communication density.
    """
    activity.logger.info(f"📚 Research Pipe: Searching scientific literature for '{query}'...")
    
    # Simulated response from the research API
    return [
        {
            "title": "Lexical Density and Persuasion in Asynchronous Communication",
            "source": "Journal of Applied Psychology",
            "findings": "High density of low-friction action verbs (e.g., 'solve', 'remove') correlates with a 40% higher trust index. Avoidance of absolute determiners (e.g., 'always', 'never') prevents reactance."
        },
        {
            "title": "The Impact of Acknowledged Limitations on Perceived Competence",
            "source": "Behavioral Science Review",
            "findings": "Explicitly stating a limitation or unknown variable before offering a solution increases the perceived validity of the solution by 62%."
        }
    ]

@activity.defn
async def build_semantic_guidelines(papers: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Expression: Distills the peer-reviewed papers into a Word Density Guideline.
    This gives the LLM the flexibility to react naturally, but bounds it with
    scientifically proven semantic density.
    """
    activity.logger.info("🧠 Research Pipe: Building the Semantic Guideline from peer-reviewed papers...")
    
    # In production, LiteLLM parses the papers and outputs this strict schema
    guideline = {
        "watchword": "Win-Win",
        "flexibility_mandate": "React naturally to the user. Do NOT use these as a rigid script.",
        "target_word_density": {
            "high_frequency": ["solve", "remove", "friction", "baseline", "assess"],
            "low_frequency_warnings": ["always", "guarantee", "never", "disrupt"]
        },
        "structural_rules": [
            "Acknowledge a limitation before offering the solution.",
            "Maintain conversational flexibility. Do not sound like a robot."
        ],
        "attribution": "These guidelines are derived from 'Lexical Density and Persuasion' (JAP) and 'Acknowledged Limitations' (BSR)."
    }
    
    return guideline
