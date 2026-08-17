"""
Quote Intelligence Workflow — primary text-initiated pipeline.

Defines the Sequential + Concurrent orchestration using Microsoft Agent Framework WorkflowBuilder.
"""

from agent_framework import WorkflowBuilder


def build_quote_intelligence_workflow() -> WorkflowBuilder:
    """
    Build the competitive quote intelligence workflow.
    
    Pattern: Sequential pipeline with concurrent fan-out for price collection.
    Entry: Text or document submission.
    
    Flow:
    1. Submission Intake (Sequential)
    2. Competitor Price Collection (Concurrent fan-out to N sources)
    3. Quote Normalization (Sequential)
    4. Coverage Comparison (Sequential)
    5. Pricing Variance (Sequential)
    6. Risk Assessment (Sequential)
    7. Recommendation (Sequential)
    8. Compliance & Guardrail — HITL gate (Sequential, approval_mode=always_require)
    9. Advisor Explanation (Sequential)
    """
    
    workflow = WorkflowBuilder(name="quote-intelligence-pipeline")
    
    # Step 1: Intake
    workflow.add_step(
        name="submission_intake",
        agent="submission-intake-agent",
        description="Parse and structure the incoming risk submission"
    )
    
    # Step 2: Concurrent competitor price collection
    workflow.add_concurrent_step(
        name="price_collection",
        agent="competitor-price-collection-agent",
        fan_out_key="competitors",
        max_concurrent=10,
        timeout_seconds=30,
        description="Fan-out to N competitor sources in parallel"
    )
    
    # Step 3: Normalization
    workflow.add_step(
        name="normalization",
        agent="quote-normalization-agent",
        description="Standardize all quotes to common schema"
    )
    
    # Step 4: Coverage Comparison
    workflow.add_step(
        name="coverage_comparison",
        agent="coverage-comparison-agent",
        description="Build side-by-side comparison matrix"
    )
    
    # Step 5: Pricing Variance
    workflow.add_step(
        name="pricing_variance",
        agent="pricing-variance-agent",
        description="Calculate market position and rate adequacy"
    )
    
    # Step 6: Risk Assessment
    workflow.add_step(
        name="risk_assessment",
        agent="risk-assessment-agent",
        description="Score appetite match and exposure level"
    )
    
    # Step 7: Recommendation
    workflow.add_step(
        name="recommendation",
        agent="recommendation-agent",
        description="Propose rate action within guardrails"
    )
    
    # Step 8: Compliance Gate (HITL)
    workflow.add_step(
        name="compliance_gate",
        agent="compliance-guardrail-agent",
        approval_mode="always_require",
        description="Enforce regulations and require human approval"
    )
    
    # Step 9: Advisor Explanation
    workflow.add_step(
        name="advisor_explanation",
        agent="advisor-explanation-agent",
        description="Generate plain-language talk-track for advisor"
    )
    
    return workflow
