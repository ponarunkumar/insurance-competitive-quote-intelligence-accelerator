"""
Insurance Competitive Quote Intelligence — Orchestrator Agent

The central coordinator that routes requests to specialist agents using
the Microsoft Agent Framework with Foundry Hosted Agents.

Azure Services: Azure AI Foundry, Azure OpenAI (via Foundry SDK)
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential


# Agent configuration
AGENT_NAME = "quote-intelligence-orchestrator"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Quote Intelligence Orchestrator for an insurance contact center.
Your role is to coordinate specialist agents to deliver competitive quote analysis.

You manage a pipeline of specialist agents:
1. Submission Intake — parse and structure the incoming risk
2. Competitor Price-Collection — gather market prices (concurrent fan-out)
3. Quote Normalization — standardize all quotes to a common schema
4. Coverage Comparison — build side-by-side analysis matrix
5. Pricing Variance — calculate gap vs. carrier rate and market position
6. Risk Assessment — score appetite match and exposure
7. Recommendation — propose rate action within guardrails
8. Compliance & Guardrail — enforce regulations, require human approval
9. Advisor Explanation — generate plain-language talk-track

For voice-initiated requests, also coordinate:
- Voice Intake Agent (Speech-to-Text transcription)
- Voice Response Agent (Text-to-Speech output)

Always ensure:
- Human-in-the-loop approval before any rate change
- Full traceability of every decision
- Only permitted, broker-shared competitor data is processed
- Rate adjustments stay within configured percentage bands
"""


def create_orchestrator_agent(project_client: AIProjectClient) -> Any:
    """Register the orchestrator agent in the Foundry project."""
    agent = project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )
    return agent


async def run_orchestrator(project_client: AIProjectClient, input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Execute the quote intelligence pipeline.

    Uses Foundry Responses API to orchestrate the conversation with the agent.
    """
    modality = input_data.get("modality", "text")

    # Get OpenAI client bound to this agent
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    # Create a conversation for multi-turn orchestration
    conversation = openai.conversations.create()

    # Build the orchestration prompt based on modality
    if modality == "voice":
        prompt = (
            f"Process this voice-initiated quote request. "
            f"First transcribe via Voice Intake, then run the full pipeline.\n"
            f"Input: {input_data}"
        )
    elif modality == "document":
        prompt = (
            f"Process this document-based submission. "
            f"Parse via Document Intelligence, then run the full pipeline.\n"
            f"Input: {input_data}"
        )
    else:
        prompt = (
            f"Process this text-based quote request through the full pipeline.\n"
            f"Input: {input_data}"
        )

    # Execute via Responses API
    response = openai.responses.create(
        conversation=conversation.id,
        input=prompt,
    )

    return {
        "result": response.output_text,
        "conversation_id": conversation.id,
        "modality": modality,
    }
