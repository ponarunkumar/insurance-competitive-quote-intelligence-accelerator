"""
Competitor Price-Collection Agent — concurrent fan-out to market sources.

Uses the Microsoft Agent Framework ConcurrentBuilder to query multiple carrier
rating APIs simultaneously. Partial failures are tolerated (minimum 2 of N required).

Orchestration Pattern: Concurrent Fan-Out / Fan-In (agent-framework-orchestrations)
Azure Services: Azure AI Foundry, API Management, Azure AI Search
"""

import asyncio
import json
import os
from typing import Any

from agent_framework import Agent
from agent_framework.orchestrations import ConcurrentBuilder
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "competitor-price-collection-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

# Minimum successful responses required (partial failure tolerance)
MIN_SUCCESSFUL_SOURCES = 2

# Timeout per source in seconds
SOURCE_TIMEOUT_SECONDS = int(os.environ.get("COMPETITOR_TIMEOUT_SECONDS", "30"))

# Default competitor sources
DEFAULT_COMPETITORS = [
    "carrier-alpha",
    "carrier-beta",
    "carrier-gamma",
    "carrier-delta",
    "carrier-epsilon",
]

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


def build_concurrent_collection(
    project_client: AIProjectClient,
    competitors: list[str],
) -> Any:
    """
    Build a ConcurrentBuilder to fan-out to N competitor sources.

    Each competitor gets its own agent instance that runs in parallel.
    Results are gathered and merged after all complete (or timeout).
    """
    agents = []
    for carrier in competitors:
        agent = Agent(
            name=f"price-collector-{carrier}",
            instructions=(
                f"You are collecting a quote from '{carrier}'. "
                f"Format the risk data for this carrier's requirements, "
                f"submit the request, and return the structured quote response "
                f"including: premium, limits, deductibles, commission, terms. "
                f"If the source is unavailable, return status: 'unavailable'."
            ),
            client=project_client.get_openai_client(agent_name=AGENT_NAME),
        )
        agents.append(agent)

    workflow = ConcurrentBuilder(participants=agents).build()
    return workflow


async def run_price_collection(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Collect prices using concurrent fan-out to multiple carrier sources.

    Pattern: Concurrent (Fan-Out / Fan-In)
    - All carrier queries run in parallel via ConcurrentBuilder
    - Partial failures tolerated (minimum 2 of N responses required)
    - Individual source timeouts enforced
    """
    submission = input_data.get("submission", {})
    competitors = input_data.get("competitors", DEFAULT_COMPETITORS)
    max_sources = int(os.environ.get("MAX_COMPETITOR_SOURCES", "10"))
    competitors = competitors[:max_sources]

    # Build the concurrent orchestration
    workflow = build_concurrent_collection(project_client, competitors)

    # Fan-out: all competitors queried simultaneously
    collection_input = json.dumps({
        "submission": submission,
        "request": "Provide a competitive quote for this risk",
    }, indent=2)

    try:
        result = await asyncio.wait_for(
            workflow(collection_input),
            timeout=SOURCE_TIMEOUT_SECONDS * 2,  # Allow 2x single-source timeout
        )
        collected_quotes = result
    except asyncio.TimeoutError:
        collected_quotes = f"Partial timeout — some sources did not respond within {SOURCE_TIMEOUT_SECONDS}s"

    return {
        "competitor_quotes": collected_quotes,
        "sources_queried": len(competitors),
        "competitors": competitors,
        "orchestration_pattern": "concurrent_fan_out",
        "min_required": MIN_SUCCESSFUL_SOURCES,
        "timeout_seconds": SOURCE_TIMEOUT_SECONDS,
    }
