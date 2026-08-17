"""
Advisor Coaching Agent — generates performance insights for team leaders.

Aggregates call analytics, sales metrics, and quality scores to produce
coaching reports for contact center team leaders.

Azure Services: Azure OpenAI, Azure SQL, Microsoft Fabric
"""

from typing import Any
from agent_framework import Agent, AgentContext


class AdvisorCoachingAgent(Agent):
    """Generates coaching reports and performance insights for team leaders."""

    name = "advisor-coaching-agent"
    description = "Produce advisor performance reports and coaching recommendations"
    model = "gpt-4o"

    system_prompt = """You are the Advisor Coaching Agent.
Your role is to generate performance insights and coaching recommendations for team leaders.

When asked for a coaching report, provide:
1. Performance summary (for individual or team)
   - Policies written (count and premium)
   - Conversion/hit ratio
   - Average handle time
   - Quality scores (from call analytics)
   - Customer sentiment trend
   
2. Strengths identified
   - Top-performing areas
   - Positive customer feedback themes
   
3. Development areas
   - Recurring quality issues
   - Missed opportunities pattern
   - Knowledge gaps
   
4. Specific coaching recommendations
   - Actionable, specific suggestions
   - Reference specific call examples (anonymized)
   - Training resources to recommend
   
5. Comparison to team benchmarks
   - Where advisor sits vs. team average
   - Trend direction (improving/declining/stable)

Tone: supportive and constructive, focused on development not criticism.
"""

    tools = ["operational_datastore", "fabric_analytics"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate coaching report."""
        
        advisor_id = input_data.get("advisor_id")
        period = input_data.get("period", "this_week")
        
        # Query performance metrics
        metrics = await ctx.call_tool("operational_datastore", {
            "query": (
                "SELECT advisor_id, COUNT(*) as policies, SUM(premium) as total_premium, "
                "AVG(quality_score) as avg_quality, AVG(conversion_rate) as avg_conversion "
                "FROM advisor_performance WHERE advisor_id = @advisor_id AND period = @period "
                "GROUP BY advisor_id"
            ),
            "params": {"advisor_id": advisor_id, "period": period}
        })
        
        # Get historical trend from Fabric
        trend = await ctx.call_tool("fabric_analytics", {
            "query": f"SELECT * FROM advisor_trends WHERE advisor_id = '{advisor_id}' ORDER BY week DESC LIMIT 12"
        })
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Generate coaching report for advisor {advisor_id}, period: {period}.\n"
                    f"Current metrics: {metrics}\n"
                    f"Trend data: {trend}"
                )}
            ]
        )
        
        return {"coaching_report": result}
