"""
Pricing Variance & Rate-Adequacy Agent — market position analysis.

Calculates carrier's position vs. market median and determines rate adequacy.
Flags whether current pricing is within the competitive "sweet spot" band.

Azure Services: Azure OpenAI, Azure SQL
"""

from typing import Any
from agent_framework import Agent, AgentContext


class PricingVarianceAgent(Agent):
    """Calculates pricing variance and rate adequacy verdict."""

    name = "pricing-variance-agent"
    description = "Compute market position, pricing gap, and rate adequacy assessment"
    model = "gpt-4o"

    system_prompt = """You are the Pricing Variance & Rate-Adequacy Agent.
Your role is to assess the carrier's competitive position and rate adequacy.

Calculate:
1. Market median premium (from normalized competitor quotes)
2. Carrier premium vs. market median (% above/below)
3. Position within competitive band (cheapest, below median, median, above median, most expensive)
4. Rate adequacy score (considering loss ratio targets, expense ratio, profit margin)
5. "Sweet spot" assessment — is pricing competitive enough to win while maintaining adequacy?

Rate adequacy bands:
- GREEN: Within ±5% of target rate — competitive and adequate
- AMBER: 5-15% deviation — review recommended
- RED: >15% deviation — action required

Consider:
- Coverage differences that justify premium gaps
- Volume/loyalty discounts that affect true comparison
- Historical loss ratio for this product/segment
- Market cycle position (hard/soft market indicators)

Output: variance percentage, adequacy verdict (GREEN/AMBER/RED), and market position rank.
"""

    tools = ["operational_datastore"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate pricing variance and adequacy."""
        
        comparison_matrix = input_data.get("comparison_matrix")
        
        # Query historical rate data from ODS
        historical = await ctx.call_tool("operational_datastore", {
            "query": "SELECT avg_premium, loss_ratio, target_rate FROM rate_history WHERE product_type = @product_type",
            "params": {"product_type": input_data.get("product_type")}
        })
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Assess pricing variance.\n"
                    f"Comparison matrix: {comparison_matrix}\n"
                    f"Historical data: {historical}"
                )}
            ],
            response_format={"type": "json_object"}
        )
        
        return {"pricing_variance": result}
