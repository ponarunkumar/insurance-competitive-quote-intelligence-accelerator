"""
Call Analytics Agent — sentiment analysis and quality scoring for contact center calls.

Processes call transcriptions to extract coaching insights, quality metrics,
and compliance indicators using Azure AI Language services.

Azure Services: Azure AI Foundry, Azure AI Language, Azure AI Speech
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "call-analytics-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Call Analytics Agent.
Your role is to analyze advisor-customer call transcripts and extract actionable insights.

Analyze:
1. Sentiment tracking (per-turn: customer and advisor)
2. Quality score (1-100) based on:
   - Greeting and professionalism
   - Needs discovery questions asked
   - Product knowledge demonstrated
   - Upsell/cross-sell attempts
   - Objection handling quality
   - Compliance with scripts/disclosures
   - Call closure and next steps
3. Compliance flags:
   - Required disclosures made (Y/N)
   - PII handling appropriate
   - No misleading statements
4. Coaching opportunities:
   - Missed upsell moments
   - Better objection handling suggested
   - Knowledge gaps identified

Output structured analytics conforming to CallAnalytics schema.
"""


def create_call_analytics_agent(project_client: AIProjectClient) -> Any:
    """Register the call analytics agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_call_analytics(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Analyze call transcript."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    transcription = input_data.get("transcription", "")
    advisor_id = input_data.get("advisor_id", "unknown")

    prompt = f"Analyze this call transcript for quality, sentiment, and coaching insights:\n{transcription}"

    response = openai.responses.create(input=prompt)

    return {
        "call_analytics": response.output_text,
        "advisor_id": advisor_id,
    }
