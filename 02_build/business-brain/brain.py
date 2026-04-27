"""
Business Brain - Core Intelligence Engine

Combines:
1. Founder interview data (their goals, constraints, pain points)
2. Business knowledge from Qdrant (frameworks, best practices)
3. Claude reasoning (synthesis, recommendations)

Output: Personalized Business Bible
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import anthropic

try:
    from qdrant_client import QdrantClient
    HAS_QDRANT = True
except ImportError:
    QdrantClient = None  # type: ignore
    HAS_QDRANT = False

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    SentenceTransformer = None  # type: ignore
    HAS_SENTENCE_TRANSFORMERS = False


@dataclass
class InterviewContext:
    """Structured interview data for Business Brain."""

    # Life goals
    desired_work_hours_per_week: Optional[float] = None
    desired_days_off_per_year: Optional[int] = None
    income_goal: Optional[float] = None

    # Current state
    current_work_hours_per_week: Optional[float] = None
    current_days_off_per_year: Optional[int] = None
    current_income: Optional[float] = None

    # Business context
    business_age_years: Optional[float] = None
    team_size: Optional[int] = None
    monthly_revenue: Optional[float] = None
    cash_in_bank: Optional[float] = None

    # Pain points & priorities
    biggest_pain_point: Optional[str] = None
    one_thing_to_fix: Optional[str] = None
    keeps_awake_at_night: Optional[str] = None

    # Qualitative insights
    role_preference: Optional[str] = None  # e.g., "loves customer contact"
    family_situation: Optional[str] = None
    energy_level: Optional[str] = None
    sustainability: Optional[str] = None

    # All extractions (raw)
    all_extractions: List[Dict[str, Any]] = None

    # Full conversation
    conversation_history: List[Dict[str, str]] = None


@dataclass
class KnowledgeChunk:
    """A chunk of business knowledge from Qdrant."""

    title: str
    section: str
    content: str
    score: float  # Relevance score
    source: str = "business-knowledge-foundation.md"


class BusinessBrain:
    """
    The Business Brain intelligence engine.

    Combines interview insights + business knowledge → personalized recommendations.
    """

    def __init__(
        self,
        anthropic_api_key: str,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        qdrant_api_key: str = "amplified-qdrant-2026",
        qdrant_collection: str = "business_knowledge",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        # Claude client
        self.claude = anthropic.Anthropic(api_key=anthropic_api_key)
        self.claude_model = "claude-sonnet-4-5-20250929"

        # Qdrant client
        self.qdrant = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
            api_key=qdrant_api_key,
            https=False,
            prefer_grpc=False
        )
        self.qdrant_collection = qdrant_collection

        # Embedding model (for semantic search)
        self.embedding_model = SentenceTransformer(embedding_model)

    def query_knowledge(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[KnowledgeChunk]:
        """
        Semantic search of business knowledge.

        Args:
            query: Natural language query
            limit: Max results
            score_threshold: Minimum relevance score (0-1)

        Returns:
            List of relevant knowledge chunks
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search Qdrant
        results = self.qdrant.query_points(
            collection_name=self.qdrant_collection,
            query=query_embedding,
            limit=limit
        )

        # Filter by score and convert to KnowledgeChunk
        chunks = []
        for hit in results.points:
            if hit.score >= score_threshold:
                chunks.append(KnowledgeChunk(
                    title=hit.payload['title'],
                    section=hit.payload['section'],
                    content=hit.payload['content'],
                    score=hit.score,
                    source=hit.payload.get('source', 'unknown')
                ))

        return chunks

    def query_multiple_topics(
        self,
        topics: List[str],
        chunks_per_topic: int = 3
    ) -> Dict[str, List[KnowledgeChunk]]:
        """
        Query multiple topics at once.

        Returns dict mapping topic → relevant chunks.
        """
        results = {}
        for topic in topics:
            results[topic] = self.query_knowledge(topic, limit=chunks_per_topic)

        return results

    def generate_business_bible(
        self,
        interview_context: InterviewContext,
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized Business Bible.

        Combines interview data + business knowledge → recommendations.

        Args:
            interview_context: Structured interview data
            topics: Optional specific topics to focus on (auto-detected if None)

        Returns:
            Business Bible with recommendations, frameworks, action plan
        """
        # Step 1: Identify topics from interview if not provided
        if topics is None:
            topics = self._identify_topics_from_interview(interview_context)

        # Step 2: Query business knowledge for each topic
        knowledge_by_topic = self.query_multiple_topics(topics, chunks_per_topic=3)

        # Step 3: Synthesize with Claude
        business_bible = self._synthesize_recommendations(
            interview_context,
            knowledge_by_topic
        )

        return business_bible

    def _identify_topics_from_interview(
        self,
        interview_context: InterviewContext
    ) -> List[str]:
        """
        Use Claude to identify key topics from interview data.
        """
        # Build interview summary
        summary = self._build_interview_summary(interview_context)

        # Ask Claude to identify topics
        prompt = f"""Based on this founder interview, identify 5-7 key business topics/frameworks that would be most helpful.

Interview Summary:
{summary}

Return topics as a JSON array of strings. Topics should be specific enough to search for (e.g., "pricing strategies", "delegation frameworks", "time management", "hiring process").

Return ONLY the JSON array, nothing else."""

        response = self.claude.messages.create(
            model=self.claude_model,
            max_tokens=1024,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Parse JSON
        import json
        try:
            topics = json.loads(content)
            return topics if isinstance(topics, list) else []
        except json.JSONDecodeError:
            # Fallback topics
            return [
                "time management",
                "delegation",
                "pricing strategies",
                "team management",
                "financial management"
            ]

    def _build_interview_summary(
        self,
        interview_context: InterviewContext
    ) -> str:
        """Build readable summary of interview data."""
        parts = ["# Founder Interview Summary\n"]

        # Life goals
        if any([
            interview_context.desired_work_hours_per_week,
            interview_context.desired_days_off_per_year,
            interview_context.income_goal
        ]):
            parts.append("## Life Goals")
            if interview_context.desired_work_hours_per_week:
                parts.append(f"- Desired work hours: {interview_context.desired_work_hours_per_week} hours/week")
            if interview_context.desired_days_off_per_year:
                parts.append(f"- Desired days off: {interview_context.desired_days_off_per_year} days/year")
            if interview_context.income_goal:
                parts.append(f"- Income goal: £{interview_context.income_goal:,.0f}/year")
            parts.append("")

        # Current state
        if any([
            interview_context.current_work_hours_per_week,
            interview_context.current_days_off_per_year,
            interview_context.current_income
        ]):
            parts.append("## Current State")
            if interview_context.current_work_hours_per_week:
                parts.append(f"- Current work hours: {interview_context.current_work_hours_per_week} hours/week")
            if interview_context.current_days_off_per_year:
                parts.append(f"- Current days off: {interview_context.current_days_off_per_year} days/year")
            if interview_context.current_income:
                parts.append(f"- Current income: £{interview_context.current_income:,.0f}/year")
            parts.append("")

        # Business context
        if any([
            interview_context.business_age_years,
            interview_context.team_size,
            interview_context.monthly_revenue
        ]):
            parts.append("## Business Context")
            if interview_context.business_age_years:
                parts.append(f"- Business age: {interview_context.business_age_years} years")
            if interview_context.team_size:
                parts.append(f"- Team size: {interview_context.team_size} people")
            if interview_context.monthly_revenue:
                parts.append(f"- Monthly revenue: £{interview_context.monthly_revenue:,.0f}")
            if interview_context.cash_in_bank:
                parts.append(f"- Cash in bank: £{interview_context.cash_in_bank:,.0f}")
            parts.append("")

        # Pain points
        if any([
            interview_context.biggest_pain_point,
            interview_context.one_thing_to_fix,
            interview_context.keeps_awake_at_night
        ]):
            parts.append("## Pain Points")
            if interview_context.biggest_pain_point:
                parts.append(f"- Biggest pain: {interview_context.biggest_pain_point}")
            if interview_context.one_thing_to_fix:
                parts.append(f"- One thing to fix: {interview_context.one_thing_to_fix}")
            if interview_context.keeps_awake_at_night:
                parts.append(f"- Keeps awake: {interview_context.keeps_awake_at_night}")
            parts.append("")

        # Qualitative
        if any([
            interview_context.role_preference,
            interview_context.family_situation,
            interview_context.energy_level,
            interview_context.sustainability
        ]):
            parts.append("## Qualitative Insights")
            if interview_context.role_preference:
                parts.append(f"- Role preference: {interview_context.role_preference}")
            if interview_context.family_situation:
                parts.append(f"- Family: {interview_context.family_situation}")
            if interview_context.energy_level:
                parts.append(f"- Energy: {interview_context.energy_level}")
            if interview_context.sustainability:
                parts.append(f"- Sustainability: {interview_context.sustainability}")

        return "\n".join(parts)

    def _synthesize_recommendations(
        self,
        interview_context: InterviewContext,
        knowledge_by_topic: Dict[str, List[KnowledgeChunk]]
    ) -> Dict[str, Any]:
        """
        Use Claude to synthesize interview + knowledge → recommendations.
        """
        # Build interview summary
        interview_summary = self._build_interview_summary(interview_context)

        # Build knowledge context
        knowledge_context = self._build_knowledge_context(knowledge_by_topic)

        # Synthesis prompt
        synthesis_prompt = f"""You are generating a personalized Business Bible for a small business founder.

You have two inputs:
1. Their interview data (goals, constraints, pain points)
2. Relevant business frameworks and best practices

Your task: Synthesize specific, actionable recommendations that honor THEIR goals while incorporating best practices.

{interview_summary}

---

# Relevant Business Knowledge

{knowledge_context}

---

# Instructions

Generate a Business Bible with these sections:

## 1. Executive Summary
- 3-5 bullet points: Where they are, where they want to be, biggest gaps

## 2. Life-First Recommendations
- Specific actions to move toward life goals (work hours, days off, income)
- Based on interview data + relevant frameworks
- Example: "E-Myth says work ON not IN business, BUT you love customer contact. Recommendation: Keep 30% customer-facing (your passion), systematize backend 70%."

## 3. Business Priorities (Rule of Three)
- Top 3 priorities for next 90 days
- Each with: What to do, Why (framework), How (specific steps), Expected outcome

## 4. Frameworks Applied
- List 3-5 frameworks most relevant to them
- For each: What it is, Why it matters for THEIR situation, How to apply it specifically
- ALWAYS cite sources (e.g., "Based on Michael Gerber's E-Myth Revisited")

## 5. Action Plan (90 Days)
- Week-by-week breakdown
- Concrete actions, not vague advice
- Owner: who does what

## 6. Key Metrics to Track
- 3-5 metrics aligned with their goals
- How to measure, target values, review frequency

## 7. Red Flags to Watch
- 2-3 warning signs things are off track
- What to do if they appear

---

CRITICAL RULES:
- Honor THEIR goals first (life goals > business best practices)
- Be specific, not generic ("Hire admin for £25K, handles scheduling/invoicing" not "Consider delegation")
- Always cite frameworks used (radical attribution)
- Rule of Three: never more than 3 priorities at once
- If framework conflicts with their goals, acknowledge and adapt

Generate the Business Bible in markdown format."""

        # Call Claude
        response = self.claude.messages.create(
            model=self.claude_model,
            max_tokens=16000,
            temperature=0.7,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        business_bible_content = response.content[0].text

        # Return structured response
        return {
            "business_bible": business_bible_content,
            "interview_summary": interview_summary,
            "topics_covered": list(knowledge_by_topic.keys()),
            "frameworks_used": self._extract_frameworks(knowledge_by_topic),
            "generated_at": self._get_timestamp(),
            "token_usage": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens
            }
        }

    def _build_knowledge_context(
        self,
        knowledge_by_topic: Dict[str, List[KnowledgeChunk]]
    ) -> str:
        """Format knowledge chunks for Claude."""
        parts = []

        for topic, chunks in knowledge_by_topic.items():
            if not chunks:
                continue

            parts.append(f"## Topic: {topic}\n")

            for i, chunk in enumerate(chunks, 1):
                parts.append(f"### [{i}] {chunk.title} (relevance: {chunk.score:.2f})\n")
                parts.append(chunk.content[:1500])  # Truncate very long chunks
                parts.append("\n---\n")

        return "\n".join(parts)

    def _extract_frameworks(
        self,
        knowledge_by_topic: Dict[str, List[KnowledgeChunk]]
    ) -> List[str]:
        """Extract list of frameworks referenced."""
        frameworks = set()

        for chunks in knowledge_by_topic.values():
            for chunk in chunks:
                # Extract framework names from titles/sections
                if " - " in chunk.title:
                    framework = chunk.title.split(" - ")[-1]
                    frameworks.add(framework)

        return sorted(list(frameworks))

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
