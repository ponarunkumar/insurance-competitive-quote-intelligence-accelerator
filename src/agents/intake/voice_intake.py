"""
Voice Intake Agent — handles voice-first entry point via Azure AI Speech.

Transcribes live calls, identifies speakers, and extracts structured risk data
from natural conversation. Integrates with Azure Communication Services for
call channel and Azure AI Speech for real-time STT with diarization.

Azure Services: Azure AI Foundry, Azure AI Speech, Azure Communication Services
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "voice-intake-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Voice Intake Agent for an insurance contact center.
Your role is to process real-time call transcriptions and extract structured risk data.

You work with:
- Real-time Speech-to-Text transcription (streaming)
- Speaker diarization (distinguish advisor vs. customer)
- Language detection and translation (multi-language support)
- Custom Speech model (insurance terminology accuracy)

From the transcribed conversation, extract:
- The insurance product being discussed
- Key risk details mentioned by the customer
- Coverage requirements stated or implied
- Any competitor quotes mentioned verbally
- Customer sentiment and urgency indicators

Output a structured submission record that feeds into the quote intelligence pipeline.
Flag any ambiguous or missing information that the advisor should clarify.
"""


def create_voice_intake_agent(project_client: AIProjectClient) -> Any:
    """Register the voice intake agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_voice_intake(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Process voice input and return structured submission."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    transcription_text = input_data.get("transcription", "")
    language = input_data.get("language", "en-GB")

    prompt = (
        f"Structure this call transcript (language: {language}) into a "
        f"submission record:\n{transcription_text}"
    )

    response = openai.responses.create(input=prompt)

    return {
        "submission": response.output_text,
        "transcription": transcription_text,
        "language": language,
    }
