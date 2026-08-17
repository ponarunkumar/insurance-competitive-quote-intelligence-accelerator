"""
Advisor Explanation Agent — generates plain-language talk-track.

Produces advisor-ready guidance that explains the competitive analysis
and recommendation in language suitable for customer conversations.

Azure Services: Azure AI Foundry
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "advisor-explanation-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Advisor Explanation Agent.
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


def create_explanation_agent(project_client: AIProjectClient) -> Any:
    """Register the advisor explanation agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_advisor_explanation(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Generate advisor talk-track."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    comparison_matrix = input_data.get("comparison_matrix", {})
    recommendation = input_data.get("recommendation", {})
    product_type = input_data.get("product_type", "")

    prompt = (
        f"Generate advisor talk-track for {product_type}.\n"
        f"Market comparison: {comparison_matrix}\n"
        f"Recommendation: {recommendation}"
    )

    response = openai.responses.create(input=prompt)

    return {"advisor_explanation": response.output_text}
