"""
Coaching Report Workflow — team leader analytics pipeline.

Secondary workflow demonstrating the same Foundry project serving multiple use cases.

Azure Services: Azure AI Foundry, Azure AI Language, Microsoft Fabric
"""

from azure.ai.projects import AIProjectClient

# Agent names for coaching pipeline
COACHING_PIPELINE_AGENTS = [
    "call-analytics-agent",
    "advisor-coaching-agent",
]


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
    results = {"input": input_data}
    pipeline_context = str(input_data)

    for agent_name in COACHING_PIPELINE_AGENTS:
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
    results["agents_invoked"] = COACHING_PIPELINE_AGENTS
    return results
