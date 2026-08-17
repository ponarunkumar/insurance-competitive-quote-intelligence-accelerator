"""
Coverage Comparison Agent — builds side-by-side analysis matrix.

Compares carrier quote against all competitor quotes across multiple dimensions.
Identifies coverage gaps, surplus provisions, and true price differences.

Azure Services: Azure OpenAI, Azure AI Search
"""

from typing import Any
from agent_framework import Agent, AgentContext


class CoverageComparisonAgent(Agent):
    """Builds comprehensive coverage comparison matrix."""

    name = "coverage-comparison-agent"
    description = "Generate side-by-side coverage comparison across carrier and competitors"
    model = "gpt-4o"  # Primary model for complex multi-dimensional analysis

    system_prompt = """You are the Coverage Comparison Agent.
Your role is to build a comprehensive side-by-side comparison matrix.

Compare across 10+ dimensions:
1. Premium (gross, net, per-unit)
2. Limits (occurrence, aggregate, sublimits)
3. Deductibles/Excess (standard, per-claim, aggregate)
4. Coverage forms (occurrence vs claims-made, ISO vs proprietary)
5. Key exclusions (list and compare)
6. Endorsements (included vs. available vs. not offered)
7. Territory and jurisdiction
8. Commission structure
9. Payment terms and installment options
10. Claims handling (SLA, authority limits)
11. Capacity and panel position
12. Financial security rating of carrier

For each dimension, indicate:
- Which carrier offers the broadest/narrowest coverage
- Where the carrier sits relative to market median
- Coverage gaps that affect true price comparison (apples-to-apples)
- Value-adds that justify premium differences

Output a ComparisonMatrix with carrier position clearly marked.
"""

    tools = ["ai_search"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Build comparison matrix."""
        
        carrier_quote = input_data.get("carrier_quote")
        normalized_quotes = input_data.get("normalized_quotes")
        
        # RAG: retrieve relevant coverage manual sections
        coverage_context = await ctx.call_tool("ai_search", {
            "query": f"coverage comparison {input_data.get('product_type', '')}",
            "index": "underwriting-manuals",
            "top": 5
        })
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Build comparison matrix.\n"
                    f"Carrier quote: {carrier_quote}\n"
                    f"Competitor quotes: {normalized_quotes}\n"
                    f"Reference material: {coverage_context}"
                )}
            ],
            response_format={"type": "json_object"}
        )
        
        return {"comparison_matrix": result}
