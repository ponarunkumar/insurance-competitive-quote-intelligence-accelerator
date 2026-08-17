"""
Pricing Variance & Rate-Adequacy Agent — market position analysis.

Calculates carrier's position vs. market median and determines rate adequacy.
Flags whether current pricing is within the competitive "sweet spot" band.

Azure Services: Azure AI Foundry, Azure SQL
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "pricing-variance-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Pricing Variance & Rate-Adequacy Agent.
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


def create_pricing_variance_agent(project_client: AIProjectClient) -> Any:
    """Register the pricing variance agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_pricing_variance(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Calculate pricing variance and adequacy."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    comparison_matrix = input_data.get("comparison_matrix", {})

    prompt = (
        f"Assess pricing variance and rate adequacy.\n"
        f"Comparison matrix: {comparison_matrix}"
    )

    response = openai.responses.create(input=prompt)

    return {"pricing_variance": response.output_text}
