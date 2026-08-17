"""
Call Analytics Agent — sentiment analysis and quality scoring for contact center calls.

Processes call transcriptions to extract coaching insights, quality metrics,
and compliance indicators using Azure AI Language services.

Azure Services: Azure AI Language, Azure AI Speech
"""

from typing import Any
from agent_framework import Agent, AgentContext


class CallAnalyticsAgent(Agent):
    """Analyzes call transcripts for quality, sentiment, and coaching insights."""

    name = "call-analytics-agent"
    description = "Extract quality metrics, sentiment, and coaching data from call transcripts"
    model = "gpt-4o-mini"

    system_prompt = """You are the Call Analytics Agent.
Your role is to analyze advisor-customer call transcripts and extract actionable insights.

Analyze:
1. Sentiment tracking (per-turn: customer and advisor)
2. Quality score (1-100) based on:
   - Greeting and professionalism
   - Needs discovery questions asked
   - Product knowledge demonstrated
   - Upsell/cross-sell attempts
   - Objection handling quality
   - Compliance with scripts/disclosures
   - Call closure and next steps
3. Compliance flags:
   - Required disclosures made (Y/N)
   - PII handling appropriate
   - No misleading statements
4. Coaching opportunities:
   - Missed upsell moments
   - Better objection handling suggested
   - Knowledge gaps identified

Output structured analytics conforming to CallAnalytics schema.
"""

    tools = ["call_summarization", "operational_datastore"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze call transcript."""
        
        transcription = input_data.get("transcription")
        advisor_id = input_data.get("advisor_id")
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyze this call:\n{transcription}"}
            ],
            response_format={"type": "json_object"}
        )
        
        # Store analytics in ODS
        await ctx.call_tool("operational_datastore", {
            "query": "INSERT INTO call_analytics (advisor_id, call_date, quality_score, sentiment_avg, insights) VALUES (@advisor_id, GETDATE(), @score, @sentiment, @insights)",
            "params": {
                "advisor_id": advisor_id,
                "score": result.get("quality_score"),
                "sentiment": result.get("avg_sentiment"),
                "insights": str(result.get("coaching_opportunities"))
            }
        })
        
        return {"call_analytics": result}
