"""
Quote Normalization Agent — standardizes competitor quotes to a common schema.

Maps disparate carrier quote formats into a unified comparison structure.
Handles variations in terminology, coverage definitions, and pricing models.

Azure Services: Azure AI Foundry, Azure OpenAI (via Foundry SDK)
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "quote-normalization-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Quote Normalization Agent.
Your role is to map competitor quotes from various formats into a standardized schema.

Normalize each quote to include:
- Annual premium (gross and net of commission)
- Policy limits (per-occurrence and aggregate)
- Deductible/excess amounts
- Coverage forms and editions
- Key exclusions and limitations
- Commission percentage
- Payment terms
- Policy period
- Endorsements included/available
- Territory and jurisdiction

Handle common variations:
- Convert monthly to annual premiums
- Standardize currency
- Map carrier-specific terms to industry-standard terminology
- Flag coverage differences that affect true price comparison
- Identify sublimits vs. full limits

Output standardized QuoteObject records conforming to the NormalizedQuote schema.
"""


def create_normalization_agent(project_client: AIProjectClient) -> Any:
    """Register the normalization agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_normalization(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Normalize all competitor quotes to common schema."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    raw_quotes = input_data.get("competitor_quotes", [])

    prompt = f"Normalize these competitor quotes to the NormalizedQuote schema:\n{raw_quotes}"

    response = openai.responses.create(input=prompt)

    return {"normalized_quotes": response.output_text}
