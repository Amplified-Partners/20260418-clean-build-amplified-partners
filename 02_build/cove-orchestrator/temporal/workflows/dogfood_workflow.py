import asyncio
from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow

# Import activity dynamically to avoid module issues
with workflow.unsafe.imports_passed_through():
    from temporal.activities.dogfood_activities import consult_perplexity, consult_antigravity, consult_claude

@dataclass
class CouncilResult:
    perplexity: str
    antigravity: str
    claude: str

@workflow.defn(name="CouncilWorkflow")
class CouncilWorkflow:
    @workflow.run
    async def run(self, prompt: str, perplexity_key: str, antigravity_key: str, claude_key: str) -> CouncilResult:
        workflow.logger.info(f"Consulting the Tri-Council with prompt: {prompt}")
        
        # Run all three activities in parallel!
        # We set a generous 60s timeout for the LLMs
        futures = [
            workflow.execute_activity(
                consult_perplexity,
                args=[prompt, perplexity_key],
                start_to_close_timeout=timedelta(seconds=60),
            ),
            workflow.execute_activity(
                consult_antigravity,
                args=[prompt, antigravity_key],
                start_to_close_timeout=timedelta(seconds=60),
            ),
            workflow.execute_activity(
                consult_claude,
                args=[prompt, claude_key],
                start_to_close_timeout=timedelta(seconds=60),
            )
        ]
        
        # Wait for all three to finish simultaneously
        results = await asyncio.gather(*futures)
        
        return CouncilResult(
            perplexity=results[0],
            antigravity=results[1],
            claude=results[2]
        )
