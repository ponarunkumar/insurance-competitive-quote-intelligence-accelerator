"""
Coaching Report Workflow — team leader analytics pipeline.

Secondary workflow demonstrating the same orchestrator serving multiple use cases.
"""

from agent_framework import WorkflowBuilder


def build_coaching_report_workflow() -> WorkflowBuilder:
    """
    Build the team leader coaching report workflow.
    
    Pattern: Sequential (simple 2-step pipeline).
    Entry: Team leader asks "Give me a coaching report on [advisor/team]"
    
    Flow:
    1. Call Analytics — process recent call transcripts
    2. Advisor Coaching — generate performance report with recommendations
    """
    
    workflow = WorkflowBuilder(name="coaching-report-pipeline")
    
    workflow.add_step(
        name="call_analytics",
        agent="call-analytics-agent",
        description="Analyze recent call transcripts for quality and sentiment"
    )
    
    workflow.add_step(
        name="coaching_report",
        agent="advisor-coaching-agent",
        description="Generate coaching report with actionable recommendations"
    )
    
    return workflow
