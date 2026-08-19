"""
Quote Intelligence Workflow — primary text-initiated pipeline.

Uses the Microsoft Agent Framework SequentialBuilder to orchestrate 9 specialist
agents in a linear pipeline. Each agent's output feeds the next as context.

Orchestration Pattern: Sequential (agent-framework-orchestrations)
Azure Services: Azure AI Foundry, Azure OpenAI (via Foundry SDK)
"""

import json
from typing import Any

from agent_framework import Agent
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient

from src.agents.intake.submission_intake import AGENT_NAME as INTAKE_AGENT
from src.agents.market_intelligence.price_collection import AGENT_NAME as PRICE_AGENT
from src.agents.market_intelligence.normalization import AGENT_NAME as NORMALIZE_AGENT
from src.agents.analysis.coverage_comparison import AGENT_NAME as COMPARISON_AGENT
from src.agents.analysis.pricing_variance import AGENT_NAME as VARIANCE_AGENT
from src.agents.analysis.risk_assessment import AGENT_NAME as RISK_AGENT
from src.agents.decision.recommendation import AGENT_NAME as RECOMMENDATION_AGENT
from src.agents.decision.compliance_guardrail import AGENT_NAME as COMPLIANCE_AGENT
from src.agents.communication.advisor_explanation import AGENT_NAME as EXPLANATION_AGENT


# Pipeline agent names in execution order
PIPELINE_AGENTS = [
    INTAKE_AGENT,
    PRICE_AGENT,
    NORMALIZE_AGENT,
    COMPARISON_AGENT,
    VARIANCE_AGENT,
    RISK_AGENT,
    RECOMMENDATION_AGENT,
    COMPLIANCE_AGENT,
    EXPLANATION_AGENT,
]


def build_sequential_pipeline(project_client: AIProjectClient) -> Any:
    """
    Build the Sequential orchestration using Agent Framework.

    Each agent is backed by a Foundry Prompt Agent and invoked via the
    Responses API. The SequentialBuilder chains them so each agent's
    output automatically becomes the next agent's input.
    """
    agents = []
    for agent_name in PIPELINE_AGENTS:
        agent = Agent(
            name=agent_name,
            instructions=(
                f"You are the '{agent_name}' step in the quote intelligence pipeline. "
                f"Process the input from the previous step and produce structured output "
                f"for the next step."
            ),
            client=project_client.get_openai_client(agent_name=agent_name),
        )
        agents.append(agent)

    workflow = SequentialBuilder(participants=agents).build()
    return workflow


async def run_quote_intelligence_pipeline(
    project_client: AIProjectClient,
    input_data: dict,
) -> dict:
    """
    Execute the competitive quote intelligence workflow.

    Pattern: Sequential — each agent processes and passes to the next.
    Entry: Text or document submission.

    Flow:
    1. Submission Intake (parse and structure)
    2. Competitor Price Collection (concurrent fan-out to N sources)
    3. Quote Normalization (standardize to common schema)
    4. Coverage Comparison (side-by-side matrix)
    5. Pricing Variance (market position and adequacy)
    6. Risk Assessment (appetite match and exposure)
    7. Recommendation (rate action within guardrails)
    8. Compliance & Guardrail — HITL gate (human approval required)
    9. Advisor Explanation (plain-language talk-track)
    """
    # Build the sequential orchestration
    workflow = build_sequential_pipeline(project_client)

    # Execute the full pipeline — SequentialBuilder handles context passing
    pipeline_input = json.dumps(input_data, indent=2)
    result = await workflow(pipeline_input)

    return {
        "pipeline_output": result,
        "pipeline_complete": True,
        "orchestration_pattern": "sequential",
        "agents_invoked": PIPELINE_AGENTS,
    }
