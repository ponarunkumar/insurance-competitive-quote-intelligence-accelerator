"""
Insurance Competitive Quote Intelligence — Orchestrator Agent

Uses the Microsoft Agent Framework HandoffBuilder for zero-latency code-level
routing based on input modality. No LLM call needed for triage — the orchestrator
dispatches to the correct pipeline (text, voice, coaching) via deterministic logic.

Orchestration Pattern: Handoff (agent-framework-orchestrations)
Azure Services: Azure AI Foundry, Azure OpenAI (via Foundry SDK)
"""

import json
import os
from typing import Any

from agent_framework import Agent
from agent_framework.orchestrations import HandoffBuilder
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential


# Agent configuration
AGENT_NAME = "quote-intelligence-orchestrator"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

SYSTEM_INSTRUCTIONS = """You are the Quote Intelligence Orchestrator for an insurance contact center.
Your role is to coordinate specialist agents to deliver competitive quote analysis.

You manage a pipeline of specialist agents:
1. Submission Intake — parse and structure the incoming risk
2. Competitor Price-Collection — gather market prices (concurrent fan-out)
3. Quote Normalization — standardize all quotes to a common schema
4. Coverage Comparison — build side-by-side analysis matrix
5. Pricing Variance — calculate gap vs. carrier rate and market position
6. Risk Assessment — score appetite match and exposure
7. Recommendation — propose rate action within guardrails
8. Compliance & Guardrail — enforce regulations, require human approval
9. Advisor Explanation — generate plain-language talk-track

For voice-initiated requests, also coordinate:
- Voice Intake Agent (Speech-to-Text transcription)
- Voice Response Agent (Text-to-Speech output)

Always ensure:
- Human-in-the-loop approval before any rate change
- Full traceability of every decision
- Only permitted, broker-shared competitor data is processed
- Rate adjustments stay within configured percentage bands
"""


def create_orchestrator_agent(project_client: AIProjectClient) -> Any:
    """Register the orchestrator agent in the Foundry project."""
    agent = project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )
    return agent


def detect_modality(input_data: dict[str, Any]) -> str:
    """
    Determine input modality for zero-latency routing.

    Returns: "voice", "coaching", or "text" (default).
    No LLM call needed — this is pure code-level dispatch.
    """
    # Explicit modality field
    modality = input_data.get("modality", "").lower()
    if modality in ("voice", "call", "audio"):
        return "voice"

    # Coaching report request detection
    request_type = input_data.get("request_type", "").lower()
    if request_type in ("coaching", "coaching_report", "performance_review"):
        return "coaching"
    if "coaching" in input_data.get("query", "").lower():
        return "coaching"

    # Voice indicators
    if any(key in input_data for key in ("call_id", "audio_url", "transcript_url")):
        return "voice"

    return "text"


def build_handoff_orchestrator(project_client: AIProjectClient) -> Any:
    """
    Build the Handoff orchestration using Agent Framework.

    The orchestrator uses code-level routing (detect_modality) to dispatch
    to the appropriate pipeline — no LLM call needed for triage.
    """
    # Define the three pipeline entry points as agents
    text_pipeline = Agent(
        name="text-quote-pipeline",
        instructions=(
            "Execute the full text-based quote intelligence pipeline: "
            "Intake → Price Collection → Normalization → Comparison → "
            "Variance → Risk → Recommendation → Compliance (HITL) → Explanation."
        ),
        client=project_client.get_openai_client(agent_name=AGENT_NAME),
    )

    voice_pipeline = Agent(
        name="voice-quote-pipeline",
        instructions=(
            "Execute the voice-initiated pipeline: "
            "Voice Intake (STT) → full text pipeline → Voice Response (TTS)."
        ),
        client=project_client.get_openai_client(agent_name=AGENT_NAME),
    )

    coaching_pipeline = Agent(
        name="coaching-report-pipeline",
        instructions=(
            "Execute the coaching report pipeline: "
            "Call Analytics → Advisor Coaching."
        ),
        client=project_client.get_openai_client(agent_name=AGENT_NAME),
    )

    # Build Handoff — triage decides which pipeline to invoke
    triage = Agent(
        name="triage",
        instructions="Route to the correct pipeline based on input modality.",
        client=project_client.get_openai_client(agent_name=AGENT_NAME),
    )

    workflow = (
        HandoffBuilder()
        .participants([triage, text_pipeline, voice_pipeline, coaching_pipeline])
        .with_start_agent(triage)
        .build()
    )
    return workflow


async def run_orchestrator(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute the orchestrator with code-level Handoff routing.

    Zero-latency triage: detect_modality() determines the pipeline
    without an LLM call, then dispatches to the appropriate workflow.
    """
    from src.workflows.quote_intelligence import run_quote_intelligence_pipeline
    from src.workflows.voice_quote_intelligence import run_voice_quote_intelligence_pipeline
    from src.workflows.coaching_report import run_coaching_report_pipeline

    # Zero-latency code-level routing (no LLM call for triage)
    modality = detect_modality(input_data)

    if modality == "voice":
        result = await run_voice_quote_intelligence_pipeline(project_client, input_data)
    elif modality == "coaching":
        result = await run_coaching_report_pipeline(project_client, input_data)
    else:
        result = await run_quote_intelligence_pipeline(project_client, input_data)

    return {
        "orchestration_pattern": "handoff",
        "modality_detected": modality,
        "routing": "code-level (zero-latency, no LLM triage call)",
        **result,
    }
