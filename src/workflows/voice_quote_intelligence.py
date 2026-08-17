"""
Voice Quote Intelligence Workflow — voice-initiated pipeline.

Extends the base pipeline with voice intake and voice response steps.
Uses Azure AI Speech for STT/TTS and Azure Communication Services for call channel.
"""

from agent_framework import WorkflowBuilder


def build_voice_quote_intelligence_workflow() -> WorkflowBuilder:
    """
    Build the voice-initiated competitive quote intelligence workflow.
    
    Pattern: Sequential pipeline with voice bookends.
    Entry: Live voice call via Azure Communication Services.
    
    Flow:
    1. Voice Intake (STT + Diarization + Translation)
    2. [Base pipeline: steps 2-9 from quote_intelligence]
    3. Voice Response (TTS delivery to advisor)
    """
    
    workflow = WorkflowBuilder(name="voice-quote-intelligence-pipeline")
    
    # Step 0: Voice Intake (STT, diarization, translation)
    workflow.add_step(
        name="voice_intake",
        agent="voice-intake-agent",
        description="Transcribe and structure voice input from live call"
    )
    
    # Steps 1-9: Same as text pipeline
    workflow.add_step(name="submission_intake", agent="submission-intake-agent")
    workflow.add_concurrent_step(
        name="price_collection",
        agent="competitor-price-collection-agent",
        fan_out_key="competitors",
        max_concurrent=10,
        timeout_seconds=30
    )
    workflow.add_step(name="normalization", agent="quote-normalization-agent")
    workflow.add_step(name="coverage_comparison", agent="coverage-comparison-agent")
    workflow.add_step(name="pricing_variance", agent="pricing-variance-agent")
    workflow.add_step(name="risk_assessment", agent="risk-assessment-agent")
    workflow.add_step(name="recommendation", agent="recommendation-agent")
    workflow.add_step(
        name="compliance_gate",
        agent="compliance-guardrail-agent",
        approval_mode="always_require"
    )
    workflow.add_step(name="advisor_explanation", agent="advisor-explanation-agent")
    
    # Step 10: Voice Response (TTS)
    workflow.add_step(
        name="voice_response",
        agent="voice-response-agent",
        description="Deliver recommendation via speech to advisor"
    )
    
    return workflow
