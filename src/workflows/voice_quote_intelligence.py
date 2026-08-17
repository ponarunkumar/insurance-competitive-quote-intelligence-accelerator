"""
Voice Quote Intelligence Workflow — voice-initiated pipeline.

Extends the base pipeline with voice intake and voice response steps.
Uses Azure AI Speech for STT/TTS and Azure Communication Services for call channel.

Azure Services: Azure AI Foundry, Azure AI Speech, Azure Communication Services
"""

from azure.ai.projects import AIProjectClient

# Agent names in pipeline order (voice bookends around the core pipeline)
VOICE_PIPELINE_AGENTS = [
    "voice-intake-agent",
    "submission-intake-agent",
    "competitor-price-collection-agent",
    "quote-normalization-agent",
    "coverage-comparison-agent",
    "pricing-variance-agent",
    "risk-assessment-agent",
    "recommendation-agent",
    "compliance-guardrail-agent",
    "advisor-explanation-agent",
    "voice-response-agent",
]


async def run_voice_quote_intelligence_pipeline(
    project_client: AIProjectClient,
    input_data: dict,
) -> dict:
    """
    Execute the voice-initiated competitive quote intelligence workflow.

    Pattern: Sequential pipeline with voice bookends.
    Entry: Live voice call via Azure Communication Services.

    Flow:
    1. Voice Intake (STT + Diarization + Translation)
    2-9. [Core pipeline: same as text flow]
    10. Voice Response (TTS delivery to advisor)
    """
    results = {"input": input_data, "modality": "voice"}
    pipeline_context = str(input_data)

    for agent_name in VOICE_PIPELINE_AGENTS:
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
    results["agents_invoked"] = VOICE_PIPELINE_AGENTS
    return results
