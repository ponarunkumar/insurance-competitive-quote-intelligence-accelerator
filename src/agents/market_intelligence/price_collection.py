"""
Competitor Price-Collection Agent — concurrent fan-out to market sources.

Retrieves competitor quotes for an identical risk from multiple carrier rating APIs.
Uses MCP tools via APIM AI Gateway for managed, rate-limited access.

Azure Services: Azure OpenAI, API Management, Azure AI Search
"""

from typing import Any
from agent_framework import Agent, AgentContext


class CompetitorPriceCollectionAgent(Agent):
    """Collects competitor prices for identical risk profiles."""

    name = "competitor-price-collection-agent"
    description = "Retrieve competitor carrier quotes for the same risk via market APIs"
    model = "gpt-4o-mini"

    system_prompt = """You are the Competitor Price-Collection Agent.
Your role is to retrieve market pricing for an identical insurance risk from multiple carriers.

For each competitor source:
1. Format the risk data according to that carrier's API schema
2. Submit the quote request via the APIM-managed competitor API
3. Capture: premium, limits, deductibles, commission, key terms
4. Handle timeouts and failures gracefully (mark source as unavailable)

Important compliance rules:
- Only use permitted, broker-shared market data
- Never access proprietary carrier systems without authorization
- Log every external API call for audit trail
- Respect rate limits enforced by APIM AI Gateway

Output a list of raw competitor quotes in their original formats.
"""

    tools = ["competitor_api", "market_data", "ai_search"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Collect prices from configured competitor sources."""
        
        submission = input_data.get("submission")
        competitors = input_data.get("competitors", [
            "carrier-a", "carrier-b", "carrier-c", "carrier-d", "carrier-e"
        ])
        
        quotes = []
        for carrier in competitors:
            try:
                quote = await ctx.call_tool("competitor_api", {
                    "carrier": carrier,
                    "risk_data": submission,
                    "product_type": submission.get("product_type")
                })
                quotes.append({"carrier": carrier, "status": "success", "quote": quote})
            except Exception as e:
                quotes.append({"carrier": carrier, "status": "failed", "error": str(e)})
        
        return {
            "competitor_quotes": quotes,
            "sources_queried": len(competitors),
            "sources_successful": len([q for q in quotes if q["status"] == "success"])
        }
