"""
Submission Intake Agent — parses and structures incoming risk submissions.

Handles text, document, and structured data inputs.
Uses Azure Document Intelligence for PDF/image processing.

Azure Services: Azure AI Foundry, Azure Document Intelligence
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "submission-intake-agent"
MODEL = os.environ.get("FOUNDRY_SECONDARY_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """You are the Submission Intake Agent for an insurance contact center.
Your role is to extract and structure risk information from incoming submissions.

You handle multiple input formats:
- Free text (advisor typing or pasting risk details)
- Parsed document content (from Document Intelligence)
- Structured form data (from web forms or APIs)
- Transcribed voice input (from Speech-to-Text)

Extract the following fields into a standardized submission record:
- Product type (CGL, Property, Professional Liability, etc.)
- Insured name and details
- Business description and SIC/NAICS code
- Annual revenue/turnover
- Number of employees
- Location(s) and territory
- Requested limits and deductibles
- Prior insurance history
- Loss history summary
- Special conditions or endorsements requested

Output a structured JSON submission record conforming to the SubmissionRecord schema.
Always flag missing required fields for follow-up.
"""


def create_submission_intake_agent(project_client: AIProjectClient) -> Any:
    """Register the submission intake agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_submission_intake(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
    conversation_id: str | None = None,
) -> dict[str, Any]:
    """Process submission and return structured risk record."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    input_type = input_data.get("type", "text")
    content = input_data.get("content", str(input_data))

    prompt = f"Extract a structured submission from this {input_type} input:\n{content}"

    response = openai.responses.create(input=prompt)

    return {
        "submission": response.output_text,
        "input_type": input_type,
    }
