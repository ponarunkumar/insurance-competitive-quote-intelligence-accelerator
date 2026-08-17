"""
Contact center data models for coaching and analytics.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CallAnalytics(BaseModel):
    """Analytics output for a single call."""
    call_id: str
    advisor_id: str
    quality_score: float = Field(ge=0, le=100)
    sentiment: dict[str, str] = Field(description="Per-speaker sentiment")
    compliance_flags: list[str] = Field(default_factory=list)
    coaching_opportunities: list[str] = Field(default_factory=list)
    upsell_attempts: int = 0
    upsell_successes: int = 0
    handle_time_seconds: float = 0
    first_contact_resolution: bool = True


class AdvisorPerformance(BaseModel):
    """Aggregated advisor performance metrics."""
    advisor_id: str
    period: str
    policies_written: int = 0
    total_premium: float = 0
    conversion_rate: float = 0
    avg_quality_score: float = 0
    avg_handle_time_seconds: float = 0
    customer_sentiment_avg: float = 0
    calls_handled: int = 0


class CoachingReport(BaseModel):
    """Coaching report for a team leader."""
    advisor_id: str
    period: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    performance_summary: str
    strengths: list[str]
    development_areas: list[str]
    coaching_recommendations: list[str]
    team_benchmark_comparison: dict[str, str]
    trend_direction: str = Field(description="improving | stable | declining")


class TeamDashboard(BaseModel):
    """Team-level dashboard metrics."""
    team_id: str
    period: str
    total_policies: int = 0
    total_premium: float = 0
    avg_conversion_rate: float = 0
    avg_quality_score: float = 0
    containment_rate: float = Field(default=0, description="% handled without escalation")
    first_contact_resolution_rate: float = 0
    top_performer: Optional[str] = None
    needs_coaching: list[str] = Field(default_factory=list)
