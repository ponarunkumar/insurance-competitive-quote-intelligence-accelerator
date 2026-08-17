"""
Advisor Explanation Agent — generates plain-language talk-track.

Produces advisor-ready guidance that explains the competitive analysis
and recommendation in language suitable for customer conversations.

Azure Services: Azure OpenAI
"""

from typing import Any
from agent_framework import Agent, AgentContext


class AdvisorExplanationAgent(Agent):
    """Generates plain-language advisor talk-track from analysis results."""

    name = "advisor-explanation-agent"
    description = "Create advisor-ready explanation of quote analysis and recommendation"
    model = "gpt-4o-mini"  # Cost-optimized for text generation

    system_prompt = """You are the Advisor Explanation Agent.
Your role is to translate complex competitive analysis into advisor-friendly guidance.

Generate:
1. A 2-3 sentence summary of market position
2. Key talking points for the customer conversation
3. Objection handling — if customer mentions a competitor's lower price
4. Value proposition — why the carrier's coverage justifies the premium
5. Next steps — what the advisor should do/say

Tone and style:
- Professional but conversational
- Avoid jargon — use plain language
- Focus on customer value, not internal metrics
- Be factual — never misrepresent coverage
- Confident but not pushy

Do NOT include:
- Internal rate adequacy scores
- Competitor names (use "the market" or "alternative providers")
- Exact competitor premiums (use relative terms: "broadly in line", "slightly above")
- Any information that could be construed as price-fixing
"""

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate advisor talk-track."""
        
        comparison_matrix = input_data.get("comparison_matrix")
        recommendation = input_data.get("recommendation")
        product_type = input_data.get("product_type")
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Generate advisor talk-track for {product_type}.\n"
                    f"Market comparison: {comparison_matrix}\n"
                    f"Recommendation: {recommendation}"
                )}
            ]
        )
        
        return {"advisor_explanation": result}
