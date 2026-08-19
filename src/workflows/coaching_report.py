"""
Coaching Report Workflow — team leader analytics pipeline.

Uses the Microsoft Agent Framework SequentialBuilder for a simple 2-step pipeline.
Demonstrates the same Foundry project serving multiple use cases.

Orchestration Pattern: Sequential (agent-framework-orchestrations)
Azure Services: Azure AI Foundry, Azure AI Language, Microsoft Fabric
"""

import json
from typing import Any

from agent_framework import Agent
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient

from src.agents.coaching.call_analytics import AGENT_NAME as ANALYTICS_AGENT
from src.agents.coaching.advisor_coaching import AGENT_NAME as COACHING_AGENT


# Coaching pipeline agents
COACHING_PIPELINE_AGENTS = [
    ANALYTICS_AGENT,
    COACHING_AGENT,
]


def build_coaching_pipeline(project_client: AIProjectClient) -> Any:
    """
    Build the coaching Sequential orchestration using Agent Framework.

    Two-step pipeline: Call Analytics → Advisor Coaching.
    """
    agents = []
    for agent_name in COACHING_PIPELINE_AGENTS:
        agent = Agent(
            name=agent_name,
            instructions=(
                f"You are the '{agent_name}' step in the coaching pipeline. "
                f"Analyze call data and generate coaching insights."
            ),
            client=project_client.get_openai_client(agent_name=agent_name),
        )
        agents.append(agent)

    workflow = SequentialBuilder(participants=agents).build()
    return workflow


async def run_coaching_report_pipeline(
    project_client: AIProjectClient,
    input_data: dict,
) -> dict:
    """
    Execute the team leader coaching report workflow.

    Pattern: Sequential (simple 2-step pipeline).
    Entry: Team leader asks "Give me a coaching report on [advisor/team]"

    Flow:
    1. Call Analytics — process recent call transcripts
    2. Advisor Coaching — generate performance report with recommendations
    """
    workflow = build_coaching_pipeline(project_client)

    pipeline_input = json.dumps(input_data, indent=2)
    result = await workflow(pipeline_input)

    return {
        "pipeline_output": result,
        "pipeline_complete": True,
        "orchestration_pattern": "sequential",
        "agents_invoked": COACHING_PIPELINE_AGENTS,
    }
