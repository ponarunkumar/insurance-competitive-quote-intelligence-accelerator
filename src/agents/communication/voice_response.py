"""
Voice Response Agent — converts text output to speech for advisor/customer.

Uses Azure AI Speech TTS to deliver recommendations and explanations
via voice when the interaction was voice-initiated.

Azure Services: Azure AI Foundry, Azure AI Speech Text-to-Speech
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "voice-response-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Voice Response Agent.
Your role is to prepare text for spoken delivery and invoke TTS.

Adapt text for voice:
- Shorten sentences for natural speech flow
- Spell out abbreviations (CGL → "commercial general liability")
- Add natural pauses via SSML markup where appropriate
- Use conversational transitions ("Now, regarding pricing...")
- Keep the response under 30 seconds of speech (~100 words)

Do NOT read out:
- Tables or matrices (summarize instead)
- Technical identifiers or reference numbers
- Internal scores or codes
"""


def create_voice_response_agent(project_client: AIProjectClient) -> Any:
    """Register the voice response agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_voice_response(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Convert explanation to speech-ready format."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    advisor_explanation = input_data.get("advisor_explanation", "")

    prompt = f"Prepare this for spoken delivery (max 100 words):\n{advisor_explanation}"

    response = openai.responses.create(input=prompt)

    return {
        "speech_text": response.output_text,
        "voice": input_data.get("voice", "en-GB-SoniaNeural"),
    }
