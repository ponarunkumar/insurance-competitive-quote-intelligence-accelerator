"""
Insurance Competitive Quote Intelligence — Orchestrator Agent

The central coordinator that routes requests to specialist agents using
Sequential, Concurrent, and Handoff patterns via Microsoft Agent Framework.

Azure Services: Azure OpenAI for agent reasoning across all interactions.
"""

from typing import Any
from agent_framework import Agent, WorkflowBuilder, AgentContext
from agent_framework.patterns import Sequential, Concurrent, Handoff


class QuoteIntelligenceOrchestrator(Agent):
    """
    Orchestrates the competitive quote intelligence pipeline.
    
    Patterns used:
    - Handoff: Triage incoming requests (text vs voice vs document)
    - Sequential: Intake → Normalize → Compare → Recommend → Comply → Explain
    - Concurrent: Fan-out to N competitor price-collection agents
    - Magentic (capped): Open-ended source discovery with round limits
    """

    name = "quote-intelligence-orchestrator"
    description = "Orchestrates competitive quote analysis across specialist agents"
    model = "gpt-4o"  # Primary model for complex reasoning

    system_prompt = """You are the Quote Intelligence Orchestrator for an insurance contact center.
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

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the quote intelligence pipeline."""
        
        # Determine entry modality
        modality = input_data.get("modality", "text")  # text | voice | document
        
        # Build the workflow based on modality
        workflow = WorkflowBuilder()
        
        # Step 1: Intake (modality-dependent)
        if modality == "voice":
            workflow.add_step("voice_intake", agent="voice-intake-agent")
        elif modality == "document":
            workflow.add_step("doc_intake", agent="submission-intake-agent",
                           tools=["quote_parser", "certificate_parser"])
        else:
            workflow.add_step("text_intake", agent="submission-intake-agent")
        
        # Step 2: Concurrent competitor price collection
        workflow.add_concurrent_step(
            "price_collection",
            agent="competitor-price-collection-agent",
            fan_out_key="competitors",  # Fan out to N carrier sources
            max_concurrent=10,
            timeout_seconds=30
        )
        
        # Step 3-6: Sequential analysis pipeline
        workflow.add_step("normalization", agent="quote-normalization-agent")
        workflow.add_step("coverage_comparison", agent="coverage-comparison-agent")
        workflow.add_step("pricing_variance", agent="pricing-variance-agent")
        workflow.add_step("risk_assessment", agent="risk-assessment-agent")
        
        # Step 7: Recommendation
        workflow.add_step("recommendation", agent="recommendation-agent")
        
        # Step 8: Compliance gate (HITL)
        workflow.add_step("compliance", agent="compliance-guardrail-agent",
                        approval_mode="always_require")
        
        # Step 9: Advisor explanation
        workflow.add_step("explanation", agent="advisor-explanation-agent")
        
        # Optional: Voice response if voice-initiated
        if modality == "voice":
            workflow.add_step("voice_response", agent="voice-response-agent")
        
        # Execute the workflow
        result = await workflow.execute(ctx, input_data)
        
        return result
