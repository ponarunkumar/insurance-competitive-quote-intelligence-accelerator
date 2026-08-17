"""
Foundry Project Client — shared initialization for all agents.

Provides a singleton-style project client using the Microsoft Foundry SDK
(azure-ai-projects) with Entra ID authentication via DefaultAzureCredential.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def get_project_client() -> AIProjectClient:
    """
    Create and return an authenticated AIProjectClient.

    Requires FOUNDRY_PROJECT_ENDPOINT environment variable set to:
        https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
    """
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    return AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )


def get_openai_client(agent_name: str | None = None):
    """
    Get an OpenAI-compatible client from the Foundry project.

    If agent_name is provided, the client is pre-bound to that agent.
    Use for Responses API calls, conversations, and evaluations.
    """
    project = get_project_client()
    if agent_name:
        return project.get_openai_client(agent_name=agent_name)
    return project.get_openai_client()
