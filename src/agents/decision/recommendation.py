"""
Recommendation Agent — proposes rate action within guardrails.

Synthesizes pricing variance + risk assessment into an actionable recommendation.
All rate moves are capped within configured percentage bands.

Azure Services: Azure AI Foundry
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "recommendation-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Recommendation Agent.
Your role is to propose a rate action based on market intelligence and risk assessment.

Your recommendation must:
1. Stay within the configured guardrail band (max adjustment %)
2. Be justified by market data (not just matching competitors)
3. Consider risk quality (load for poor risks, discount for preferred)
4. Account for coverage differences in the comparison
5. Include a confidence score (High/Medium/Low)

Recommendation types:
- HOLD: Current rate is competitive and adequate — no change needed
- REDUCE: Rate is above market — propose specific % reduction
- INCREASE: Rate is below adequate — propose specific % increase (rare in competitive context)
- ADJUST_COVERAGE: Rate is fine but coverage needs modification to compete
- DECLINE: Risk does not fit appetite — recommend non-renewal or decline

For each recommendation, provide:
- Action type (HOLD/REDUCE/INCREASE/ADJUST_COVERAGE/DECLINE)
- Percentage adjustment (if applicable)
- Rationale (3-5 bullet points)
- Confidence level
- Conditions or caveats
- Expected impact on conversion probability

CRITICAL: The guardrail band is a HARD LIMIT. Never propose adjustments exceeding it.
"""


def create_recommendation_agent(project_client: AIProjectClient) -> Any:
    """Register the recommendation agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_recommendation(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Generate rate recommendation."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    pricing_variance = input_data.get("pricing_variance", {})
    risk_assessment = input_data.get("risk_assessment", {})
    guardrail_band = input_data.get("guardrail_band_percent", 10)

    prompt = (
        f"Generate recommendation.\n"
        f"Pricing variance: {pricing_variance}\n"
        f"Risk assessment: {risk_assessment}\n"
        f"Guardrail band: ±{guardrail_band}%\n"
        f"HARD LIMIT: Do not exceed {guardrail_band}% adjustment."
    )

    response = openai.responses.create(input=prompt)

    return {"recommendation": response.output_text}
