"""
Pydantic schemas for the Insurance Competitive Quote Intelligence system.

Defines the data contracts between agents — input/output schemas for each step.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class ProductType(str, Enum):
    CGL = "commercial_general_liability"
    PROPERTY = "commercial_property"
    PROFESSIONAL_LIABILITY = "professional_liability"
    DIRECTORS_OFFICERS = "directors_and_officers"
    WORKERS_COMP = "workers_compensation"
    BOP = "business_owners_policy"
    COMMERCIAL_AUTO = "commercial_auto"
    UMBRELLA = "umbrella_excess"
    CYBER = "cyber_liability"
    EPLI = "employment_practices"


class RateAction(str, Enum):
    HOLD = "HOLD"
    REDUCE = "REDUCE"
    INCREASE = "INCREASE"
    ADJUST_COVERAGE = "ADJUST_COVERAGE"
    DECLINE = "DECLINE"


class ComplianceStatus(str, Enum):
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"
    PENDING_REVIEW = "PENDING_REVIEW"


class AdequacyVerdict(str, Enum):
    GREEN = "GREEN"   # Within ±5% — competitive and adequate
    AMBER = "AMBER"   # 5-15% deviation — review recommended
    RED = "RED"       # >15% deviation — action required


class AppetiteMatch(str, Enum):
    IN_APPETITE = "IN_APPETITE"
    BORDERLINE = "BORDERLINE"
    DECLINE = "DECLINE"


# ============================================================================
# SUBMISSION & INTAKE
# ============================================================================

class SubmissionRecord(BaseModel):
    """Structured risk submission — output of Intake Agent."""
    id: str = Field(description="Unique submission identifier")
    product_type: ProductType
    insured_name: str
    business_description: str
    sic_code: Optional[str] = None
    annual_revenue: float = Field(description="Annual revenue/turnover in local currency")
    currency: str = "GBP"
    employee_count: Optional[int] = None
    locations: list[str] = Field(default_factory=list)
    territory: str = "UK"
    requested_limit: float
    requested_deductible: float
    prior_carrier: Optional[str] = None
    years_with_prior: Optional[int] = None
    loss_history_summary: Optional[str] = None
    special_conditions: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list, description="Fields needing follow-up")
    submission_timestamp: datetime = Field(default_factory=datetime.utcnow)
    modality: str = Field(default="text", description="text | voice | document")


# ============================================================================
# QUOTES & COMPARISON
# ============================================================================

class NormalizedQuote(BaseModel):
    """Standardized quote — output of Normalization Agent."""
    carrier: str
    annual_premium_gross: float
    annual_premium_net: float
    commission_percent: float
    per_occurrence_limit: float
    aggregate_limit: float
    deductible: float
    coverage_form: str
    key_exclusions: list[str] = Field(default_factory=list)
    endorsements_included: list[str] = Field(default_factory=list)
    payment_terms: Optional[str] = None
    policy_period_months: int = 12
    territory: str = ""
    financial_rating: Optional[str] = None
    quote_valid_until: Optional[datetime] = None


class ComparisonDimension(BaseModel):
    """Single dimension of the comparison matrix."""
    dimension: str
    carrier_value: str
    competitor_values: dict[str, str]
    carrier_position: str = Field(description="best | above_median | median | below_median | worst")
    notes: Optional[str] = None


class ComparisonMatrix(BaseModel):
    """Full comparison matrix — output of Coverage Comparison Agent."""
    product_type: ProductType
    carrier_quote: NormalizedQuote
    competitor_quotes: list[NormalizedQuote]
    dimensions: list[ComparisonDimension]
    apples_to_apples_adjustments: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# ANALYSIS & DECISION
# ============================================================================

class PricingVariance(BaseModel):
    """Pricing variance result — output of Pricing Variance Agent."""
    carrier_premium: float
    market_median: float
    variance_percent: float = Field(description="Positive = above market, negative = below")
    market_position_rank: int = Field(description="1 = cheapest, N = most expensive")
    total_competitors: int
    adequacy_verdict: AdequacyVerdict
    sweet_spot_assessment: str
    historical_loss_ratio: Optional[float] = None
    target_loss_ratio: Optional[float] = None


class RiskAssessment(BaseModel):
    """Risk assessment — output of Risk Assessment Agent."""
    appetite_match: AppetiteMatch
    exposure_score: float = Field(ge=1, le=10, description="1=low, 10=extreme")
    hazard_grade: str
    referral_triggers: list[str] = Field(default_factory=list)
    recommended_conditions: list[str] = Field(default_factory=list)
    pricing_load_percent: float = Field(default=0, description="Additional loading for risk quality")


class Recommendation(BaseModel):
    """Rate recommendation — output of Recommendation Agent."""
    action_type: RateAction
    adjustment_percent: float = Field(default=0)
    rationale: list[str] = Field(min_length=1)
    confidence: str = Field(description="High | Medium | Low")
    conditions: list[str] = Field(default_factory=list)
    expected_conversion_impact: Optional[str] = None
    guardrail_band_used: float


class ComplianceResult(BaseModel):
    """Compliance check result — output of Compliance Agent."""
    status: ComplianceStatus
    human_decision: Optional[str] = None
    antitrust_check: bool = True
    rate_filing_check: bool = True
    regulatory_check: bool = True
    data_governance_check: bool = True
    block_reason: Optional[str] = None
    audit_id: str = ""


# ============================================================================
# FULL PIPELINE OUTPUT
# ============================================================================

class QuoteIntelligenceResult(BaseModel):
    """Complete pipeline output — returned to the advisor/team leader."""
    submission: SubmissionRecord
    comparison_matrix: ComparisonMatrix
    pricing_variance: PricingVariance
    risk_assessment: RiskAssessment
    recommendation: Recommendation
    compliance: ComplianceResult
    advisor_explanation: str
    pipeline_duration_seconds: float
    agents_invoked: list[str]
