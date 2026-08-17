"""
Compliance & Guardrail Agent — enforces regulations and requires human approval.

This is the HITL (Human-in-the-Loop) gate. No rate change proceeds without
explicit human approval. Enforces antitrust, rate-filing, and regulatory compliance.

Azure Services: Azure AI Foundry, Microsoft Purview
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "compliance-guardrail-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

# CRITICAL: This agent requires human approval before execution
APPROVAL_MODE = "always_require"

SYSTEM_INSTRUCTIONS = """You are the Compliance & Guardrail Agent.
Your role is to ensure every rate recommendation complies with regulations
and to gate human approval before any rate change is applied.

Compliance checks:
1. ANTITRUST: Verify only permitted, broker-shared data was used
   - No direct carrier-to-carrier price coordination
   - Only publicly available or broker-provided market data
   
2. RATE FILING: Ensure proposed rate is within filed rate bands
   - Check against state/territory filing requirements
   - Verify no unfair discrimination
   
3. REGULATORY: Align with applicable insurance regulations
   - NAIC Model AI Bulletin compliance (US markets)
   - FCA/PRA guidelines (UK markets)
   - Local regulatory requirements per jurisdiction
   
4. GUARDRAIL ENFORCEMENT:
   - Rate adjustment within configured % band
   - No automated rate changes without human sign-off
   - Audit trail complete and traceable
   
5. DATA GOVERNANCE:
   - Policyholder PII not exposed in competitive analysis
   - Competitor data sourced only from permitted channels
   - All processing logged for regulatory inspection

Output: APPROVED (with conditions) or BLOCKED (with reason).
If APPROVED, present approval card to team leader for sign-off.
"""


def create_compliance_agent(project_client: AIProjectClient) -> Any:
    """Register the compliance guardrail agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_compliance_check(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Run compliance checks and request human approval."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    recommendation = input_data.get("recommendation", {})

    prompt = (
        f"Validate this recommendation for compliance.\n"
        f"Recommendation: {recommendation}\n"
        f"Check: antitrust, rate filing, regulatory, guardrail enforcement, data governance.\n"
        f"Output APPROVED or BLOCKED with detailed reasoning."
    )

    response = openai.responses.create(input=prompt)

    return {
        "compliance_result": response.output_text,
        "approval_mode": APPROVAL_MODE,
        "requires_human_approval": True,
    }
