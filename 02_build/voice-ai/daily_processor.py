"""
Daily Processor for Voice Transcripts
======================================
Reads day's transcripts, extracts signal from noise.

Outputs:
- Tasks identified
- Ideas captured
- Decisions made
- Sentiment patterns
- Themes and connections

Built: December 6th, 2025
"""

import os
from datetime import datetime
from pathlib import Path

import anthropic


class DailyProcessor:
    """
    Process daily voice transcripts and extract structured insights.
    
    Uses Claude Haiku for cost efficiency - this is classification/extraction work.
    """
    
    def __init__(
        self,
        anthropic_api_key: str,
        transcripts_dir: str = "transcripts/raw",
        insights_dir: str = "insights/daily"
    ):
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.transcripts_dir = Path(transcripts_dir)
        self.insights_dir = Path(insights_dir)
        self.insights_dir.mkdir(parents=True, exist_ok=True)
    
    def get_today_transcript(self) -> str | None:
        """
        Get today's transcript file content.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        transcript_file = self.transcripts_dir / f"{date_str}.md"
        
        if not transcript_file.exists():
            return None
        
        return transcript_file.read_text()
    
    def get_transcript_for_date(self, date_str: str) -> str | None:
        """
        Get transcript for a specific date (YYYY-MM-DD format).
        """
        transcript_file = self.transcripts_dir / f"{date_str}.md"
        
        if not transcript_file.exists():
            return None
        
        return transcript_file.read_text()
    
    def extract_insights(self, transcript: str) -> dict:
        """
        Extract structured insights from transcript.
        
        Uses Claude Haiku for speed and cost efficiency.
        """
        extraction_prompt = """Analyze this voice conversation transcript and extract:

1. TASKS - Anything that needs to be done. Include:
   - The task itself
   - Any deadline mentioned
   - Priority if indicated
   - Status (new, in progress, completed, blocked)

2. IDEAS - Concepts, possibilities, things to explore. Include:
   - The idea
   - Why it came up
   - Any connections to other ideas

3. DECISIONS - Choices made or confirmed. Include:
   - What was decided
   - The reasoning if given
   - Any conditions or caveats

4. SENTIMENT - Emotional tone patterns. Note:
   - Overall energy level (high/medium/low)
   - Any frustration points
   - Any excitement spikes
   - Mood shifts during conversation

5. THEMES - Recurring topics or threads. Note:
   - Main themes discussed
   - Connections between topics
   - Unresolved threads

6. FOLLOW-UPS - Things to surface tomorrow. Include:
   - Questions left unanswered
   - Things to check on
   - Promises made

Be concise. No waffle. Just the signal.

TRANSCRIPT:
{transcript}

OUTPUT FORMAT:
Use markdown with clear sections. No fluff."""

        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",  # Fast and cheap for extraction
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": extraction_prompt.format(transcript=transcript)
            }]
        )
        
        return {
            "raw_extraction": response.content[0].text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
    
    def generate_daily_brief(self, extraction: str, previous_context: str = None) -> str:
        """
        Generate a conversational daily brief from extractions.
        
        This is what gets read back to user tomorrow morning.
        """
        brief_prompt = """Based on these extracted insights from yesterday's voice conversations, 
write a brief spoken summary for tomorrow morning.

Tone: Direct, no waffle. Like a trusted colleague giving you the rundown.

Structure:
1. Open with the most important thing (one sentence)
2. Tasks that need attention today
3. Any decisions that are waiting
4. Anything worth noting about patterns/mood
5. One thing to think about

Keep it under 200 words. This will be spoken aloud.

EXTRACTED INSIGHTS:
{extraction}

{previous_context_section}

Write the brief now:"""

        previous_section = ""
        if previous_context:
            previous_section = f"\nPREVIOUS CONTEXT (for continuity):\n{previous_context}\n"
        
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": brief_prompt.format(
                    extraction=extraction,
                    previous_context_section=previous_section
                )
            }]
        )
        
        return response.content[0].text
    
    def save_daily_insights(self, extraction: str, brief: str, date_str: str = None):
        """
        Save processed insights to markdown file.
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        output_file = self.insights_dir / f"{date_str}.md"
        
        content = f"""# Daily Insights - {date_str}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Morning Brief

{brief}

---

## Full Extraction

{extraction}
"""
        
        output_file.write_text(content)
        return output_file
    
    def process_today(self) -> Path | None:
        """
        Process today's transcript and generate insights.
        """
        transcript = self.get_today_transcript()
        
        if not transcript:
            print("No transcript found for today.")
            return None
        
        print("Extracting insights...")
        extraction_result = self.extract_insights(transcript)
        
        print("Generating brief...")
        brief = self.generate_daily_brief(extraction_result["raw_extraction"])
        
        print("Saving...")
        output_file = self.save_daily_insights(
            extraction_result["raw_extraction"],
            brief
        )
        
        print(f"✅ Saved to: {output_file}")
        print(f"   Tokens used: {extraction_result['input_tokens']} in, {extraction_result['output_tokens']} out")
        
        return output_file
    
    def get_latest_insights(self) -> str | None:
        """
        Get the most recent insights file content.
        For loading context into next conversation.
        """
        insight_files = sorted(self.insights_dir.glob("*.md"), reverse=True)
        
        if not insight_files:
            return None
        
        return insight_files[0].read_text()


def main():
    """
    Run daily processing.
    
    Expects environment variable:
    - ANTHROPIC_API_KEY
    """
    processor = DailyProcessor(
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    processor.process_today()


if __name__ == "__main__":
    main()
