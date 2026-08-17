"""
Recommendation Agent — proposes rate action within guardrails.

Synthesizes pricing variance + risk assessment into an actionable recommendation.
All rate moves are capped within configured percentage bands.

Azure Services: Azure OpenAI
"""

from typing import Any
from agent_framework import Agent, AgentContext


class RecommendationAgent(Agent):
    """Proposes rate action based on market analysis and risk assessment."""

    name = "recommendation-agent"
    description = "Propose competitive rate action within configured guardrail bands"
    model = "gpt-4o"

    system_prompt = """You are the Recommendation Agent.
Your role is to propose a rate action based on market intelligence and risk assessment.

Your recommendation must:
1. Stay within the configured guardrail band (max adjustment %)
2. Be justified by market data (not just matching competitors)
3. Consider risk quality (load for poor risks, discount for preferred)
4. Account for coverage differences in the comparison
5. Include a confidence score (High/Medium/Low)

Recommendation types:
- HOLD: Current rate is competitive and adequate — no change needed
- REDUCE: Rate is above market — propose specific % reduction
- INCREASE: Rate is below adequate — propose specific % increase (rare in competitive context)
- ADJUST_COVERAGE: Rate is fine but coverage needs modification to compete
- DECLINE: Risk does not fit appetite — recommend non-renewal or decline

For each recommendation, provide:
- Action type (HOLD/REDUCE/INCREASE/ADJUST_COVERAGE/DECLINE)
- Percentage adjustment (if applicable)
- Rationale (3-5 bullet points)
- Confidence level
- Conditions or caveats
- Expected impact on conversion probability

CRITICAL: The guardrail band is a HARD LIMIT. Never propose adjustments exceeding it.
"""

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate rate recommendation."""
        
        pricing_variance = input_data.get("pricing_variance")
        risk_assessment = input_data.get("risk_assessment")
        guardrail_band = input_data.get("guardrail_band_percent", 10)  # Default ±10%
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Generate recommendation.\n"
                    f"Pricing variance: {pricing_variance}\n"
                    f"Risk assessment: {risk_assessment}\n"
                    f"Guardrail band: ±{guardrail_band}%\n"
                    f"HARD LIMIT: Do not exceed {guardrail_band}% adjustment."
                )}
            ],
            response_format={"type": "json_object"}
        )
        
        return {"recommendation": result}
