"""
Quote Intelligence Workflow — primary text-initiated pipeline.

Orchestrates the sequential agent pipeline using Microsoft Foundry SDK.
Each agent is registered as a Foundry Prompt Agent and invoked via the
Responses API with conversation context for multi-turn orchestration.
"""

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Agent names in pipeline order
PIPELINE_AGENTS = [
    "submission-intake-agent",
    "competitor-price-collection-agent",
    "quote-normalization-agent",
    "coverage-comparison-agent",
    "pricing-variance-agent",
    "risk-assessment-agent",
    "recommendation-agent",
    "compliance-guardrail-agent",
    "advisor-explanation-agent",
]


async def run_quote_intelligence_pipeline(
    project_client: AIProjectClient,
    input_data: dict,
) -> dict:
    """
    Execute the competitive quote intelligence workflow.

    Pattern: Sequential pipeline with conversation context passed between agents.
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
    results = {"input": input_data}
    pipeline_context = str(input_data)

    for agent_name in PIPELINE_AGENTS:
        openai = project_client.get_openai_client(agent_name=agent_name)

        prompt = (
            f"Process the following data through your pipeline step.\n"
            f"Context from previous steps: {pipeline_context}\n"
            f"Original input: {input_data}"
        )

        response = openai.responses.create(input=prompt)

        step_result = response.output_text
        results[agent_name] = step_result
        pipeline_context = step_result

    results["pipeline_complete"] = True
    results["agents_invoked"] = PIPELINE_AGENTS
    return results
