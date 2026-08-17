"""
Risk Assessment Agent — appetite match and exposure scoring.

Evaluates whether the risk fits carrier appetite and scores exposure level.
Grounded on underwriting manuals and appetite guides via Azure AI Search.

Azure Services: Azure AI Foundry, Azure AI Search
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "risk-assessment-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Risk Assessment Agent.
Your role is to evaluate whether a submission fits carrier appetite and score the exposure.

Assess:
1. Appetite match (In-Appetite / Borderline / Decline)
   - Industry/SIC code vs. appetite guide
   - Size (revenue, employees) vs. target market
   - Territory match
   - Loss history vs. acceptable thresholds
   
2. Exposure scoring (1-10 scale)
   - Hazard grade of the industry
   - Claims frequency expectations
   - Severity potential
   - Aggregation risk
   
3. Pricing implications
   - Should rate be loaded or discounted based on risk quality?
   - Specific exclusions or conditions recommended?
   - Referral triggers (if any criteria breached)

Ground your assessment in the carrier's underwriting manuals and appetite guides.
Flag any referral triggers that require senior underwriter review.
"""


def create_risk_assessment_agent(project_client: AIProjectClient) -> Any:
    """Register the risk assessment agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_risk_assessment(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Assess risk appetite and exposure."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    submission = input_data.get("submission", {})

    prompt = (
        f"Assess this risk for appetite match and exposure scoring:\n"
        f"Submission: {submission}"
    )

    response = openai.responses.create(input=prompt)

    return {"risk_assessment": response.output_text}
