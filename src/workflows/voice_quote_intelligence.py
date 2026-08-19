"""
Voice Quote Intelligence Workflow — voice-initiated pipeline.

Extends the base pipeline with voice intake and voice response bookends.
Uses the Microsoft Agent Framework SequentialBuilder for orchestration.

Orchestration Pattern: Sequential (with voice bookends)
Azure Services: Azure AI Foundry, Azure AI Speech, Azure Communication Services
"""

import json
from typing import Any

from agent_framework import Agent
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient

from src.agents.intake.voice_intake import AGENT_NAME as VOICE_INTAKE_AGENT
from src.agents.intake.submission_intake import AGENT_NAME as INTAKE_AGENT
from src.agents.market_intelligence.price_collection import AGENT_NAME as PRICE_AGENT
from src.agents.market_intelligence.normalization import AGENT_NAME as NORMALIZE_AGENT
from src.agents.analysis.coverage_comparison import AGENT_NAME as COMPARISON_AGENT
from src.agents.analysis.pricing_variance import AGENT_NAME as VARIANCE_AGENT
from src.agents.analysis.risk_assessment import AGENT_NAME as RISK_AGENT
from src.agents.decision.recommendation import AGENT_NAME as RECOMMENDATION_AGENT
from src.agents.decision.compliance_guardrail import AGENT_NAME as COMPLIANCE_AGENT
from src.agents.communication.advisor_explanation import AGENT_NAME as EXPLANATION_AGENT
from src.agents.communication.voice_response import AGENT_NAME as VOICE_RESPONSE_AGENT


# Voice pipeline: voice bookends around the core pipeline
VOICE_PIPELINE_AGENTS = [
    VOICE_INTAKE_AGENT,
    INTAKE_AGENT,
    PRICE_AGENT,
    NORMALIZE_AGENT,
    COMPARISON_AGENT,
    VARIANCE_AGENT,
    RISK_AGENT,
    RECOMMENDATION_AGENT,
    COMPLIANCE_AGENT,
    EXPLANATION_AGENT,
    VOICE_RESPONSE_AGENT,
]


def build_voice_sequential_pipeline(project_client: AIProjectClient) -> Any:
    """
    Build the voice Sequential orchestration using Agent Framework.

    Same as text pipeline but bookended with Voice Intake (STT) and
    Voice Response (TTS) agents.
    """
    agents = []
    for agent_name in VOICE_PIPELINE_AGENTS:
        agent = Agent(
            name=agent_name,
            instructions=(
                f"You are the '{agent_name}' step in the voice quote intelligence pipeline. "
                f"Process the input from the previous step and produce structured output."
            ),
            client=project_client.get_openai_client(agent_name=agent_name),
        )
        agents.append(agent)

    workflow = SequentialBuilder(participants=agents).build()
    return workflow


async def run_voice_quote_intelligence_pipeline(
    project_client: AIProjectClient,
    input_data: dict,
) -> dict:
    """
    Execute the voice-initiated competitive quote intelligence workflow.

    Pattern: Sequential pipeline with voice bookends.
    Entry: Live voice call via Azure Communication Services.

    Flow:
    1. Voice Intake (STT + Diarization + Translation)
    2-9. [Core pipeline: same as text flow]
    10. Advisor Explanation (plain-language talk-track)
    11. Voice Response (TTS delivery to advisor)
    """
    workflow = build_voice_sequential_pipeline(project_client)

    pipeline_input = json.dumps(input_data, indent=2)
    result = await workflow(pipeline_input)

    return {
        "pipeline_output": result,
        "pipeline_complete": True,
        "modality": "voice",
        "orchestration_pattern": "sequential",
        "agents_invoked": VOICE_PIPELINE_AGENTS,
    }
