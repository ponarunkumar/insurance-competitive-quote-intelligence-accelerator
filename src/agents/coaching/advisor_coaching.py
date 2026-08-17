"""
Advisor Coaching Agent — generates performance insights for team leaders.

Aggregates call analytics, sales metrics, and quality scores to produce
coaching reports for contact center team leaders.

Azure Services: Azure AI Foundry, Azure SQL, Microsoft Fabric
"""

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "advisor-coaching-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Advisor Coaching Agent.
Your role is to generate performance insights and coaching recommendations for team leaders.

When asked for a coaching report, provide:
1. Performance summary (for individual or team)
   - Policies written (count and premium)
   - Conversion/hit ratio
   - Average handle time
   - Quality scores (from call analytics)
   - Customer sentiment trend
   
2. Strengths identified
   - Top-performing areas
   - Positive customer feedback themes
   
3. Development areas
   - Recurring quality issues
   - Missed opportunities pattern
   - Knowledge gaps
   
4. Specific coaching recommendations
   - Actionable, specific suggestions
   - Reference specific call examples (anonymized)
   - Training resources to recommend
   
5. Comparison to team benchmarks
   - Where advisor sits vs. team average
   - Trend direction (improving/declining/stable)

Tone: supportive and constructive, focused on development not criticism.
"""


def create_coaching_agent(project_client: AIProjectClient) -> Any:
    """Register the advisor coaching agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def run_coaching_report(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Generate coaching report."""
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)

    advisor_id = input_data.get("advisor_id", "unknown")
    period = input_data.get("period", "this_week")

    prompt = (
        f"Generate a coaching report for advisor {advisor_id}, period: {period}.\n"
        f"Analytics data: {input_data.get('call_analytics', {})}"
    )

    response = openai.responses.create(input=prompt)

    return {
        "coaching_report": response.output_text,
        "advisor_id": advisor_id,
        "period": period,
    }
