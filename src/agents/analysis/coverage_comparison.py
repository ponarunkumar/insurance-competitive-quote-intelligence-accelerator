"""
Coverage Comparison Agent — builds side-by-side analysis matrix.

Compares carrier quote against all competitor quotes across multiple dimensions.
Identifies coverage gaps, surplus provisions, and true price differences.

Azure Services: Azure AI Foundry, Azure AI Search
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "coverage-comparison-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Coverage Comparison Agent.
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


def create_coverage_comparison_agent(project_client: AIProjectClient) -> Any:
    """Register the coverage comparison agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_coverage_comparison(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Build comparison matrix."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    carrier_quote = input_data.get("carrier_quote", {})
    normalized_quotes = input_data.get("normalized_quotes", [])

    prompt = (
        f"Build a comprehensive comparison matrix.\n"
        f"Carrier quote: {carrier_quote}\n"
        f"Competitor quotes: {normalized_quotes}"
    )

    response = openai.responses.create(input=prompt)

    return {"comparison_matrix": response.output_text}
