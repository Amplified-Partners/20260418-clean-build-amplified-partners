import json
from temporalio import activity
from typing import Dict, Any, List

@activity.defn
async def fetch_ai_news() -> List[Dict[str, Any]]:
    """
    Pulls raw AI developments from the last 24 hours.
    In production, this hooks into the Perplexity extraction pipe or SearXNG.
    """
    activity.logger.info("🦇 Night Watchman: Fetching daily AI developments...")
    # Simulated data pull for the R&D pipeline
    return [
        {"title": "New Flux Model for Fast Video", "type": "tool"},
        {"title": "OpenAI releases 1M context window", "type": "news"},
        {"title": "New terminal agent 'Aider' update", "type": "tool"}
    ]

@activity.defn
async def apply_rubric(developments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Applies the Amplified Rubric: [Friction, Complexity, Cost, Benefit].
    Filters out the bullshit.
    """
    activity.logger.info("🦇 Night Watchman: Applying Friction/Complexity/Cost/Benefit rubric...")
    
    passed_items = []
    failed_items = []
    
    for item in developments:
        # In production, this makes a call to LiteLLM with the rubric system prompt.
        # For now, we simulate the logic: "tool" passes, "news" fails.
        if item.get("type") == "tool":
            passed_items.append(item)
        else:
            failed_items.append(item)
            
    return {
        "passed": passed_items,
        "failed": failed_items
    }

@activity.defn
async def route_to_autonomous_testing(passed_items: List[Dict[str, Any]]) -> str:
    """
    Parks the tools that passed the rubric into the Autonomous R&D pipe.
    Explicitly keeps Ewan out of the loop so he isn't distracted.
    """
    activity.logger.info(f"🦇 Night Watchman: Routing {len(passed_items)} items to Autonomous R&D.")
    # Here we would trigger the Testing Reactor (TR-001) workflows
    return f"Parked {len(passed_items)} tools for autonomous testing."

@activity.defn
async def generate_morning_brief(passed_items: List[Dict[str, Any]], failed_items: List[Dict[str, Any]]) -> str:
    """
    Generates the morning brief for Ewan's philosophical stream.
    Highlights what passed, and explicitly calls out the bullshit in the failed items.
    """
    activity.logger.info("🦇 Night Watchman: Drafting the Morning Brief for Ewan...")
    
    brief = f"Morning Ewan.\n\n"
    brief += f"We scanned the landscape. {len(passed_items)} items passed the rubric and have been parked for autonomous testing.\n"
    brief += f"We threw out {len(failed_items)} items as pure hype/bullshit.\n\n"
    brief += "Let's discuss."
    
    return brief
