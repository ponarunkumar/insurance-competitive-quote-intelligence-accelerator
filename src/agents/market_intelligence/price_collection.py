"""
Competitor Price-Collection Agent — concurrent fan-out to market sources.

Retrieves competitor quotes for an identical risk from multiple carrier rating APIs.
Uses MCP tools via APIM AI Gateway for managed, rate-limited access.

Azure Services: Azure AI Foundry, API Management, Azure AI Search
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "competitor-price-collection-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Competitor Price-Collection Agent.
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


def create_price_collection_agent(project_client: AIProjectClient) -> Any:
    """Register the price collection agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_price_collection(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Collect prices from configured competitor sources."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    submission = input_data.get("submission", {})
    competitors = input_data.get("competitors", [
        "carrier-a", "carrier-b", "carrier-c", "carrier-d", "carrier-e"
    ])

    prompt = (
        f"Collect competitor quotes for this risk from {len(competitors)} sources.\n"
        f"Competitors: {competitors}\n"
        f"Submission data: {submission}\n"
        f"Return structured quotes for each carrier."
    )

    response = openai.responses.create(input=prompt)

    return {
        "competitor_quotes": response.output_text,
        "sources_queried": len(competitors),
    }
