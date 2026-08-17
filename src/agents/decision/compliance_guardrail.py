"""
Compliance & Guardrail Agent — enforces regulations and requires human approval.

This is the HITL (Human-in-the-Loop) gate. No rate change proceeds without
explicit human approval. Enforces antitrust, rate-filing, and regulatory compliance.

Azure Services: Copilot Studio, Azure OpenAI
"""

from typing import Any
from agent_framework import Agent, AgentContext


class ComplianceGuardrailAgent(Agent):
    """Enforces compliance rules and gates human approval for rate changes."""

    name = "compliance-guardrail-agent"
    description = "Enforce regulatory compliance and require human approval for rate moves"
    model = "gpt-4o"
    
    # CRITICAL: This tool requires human approval before execution
    approval_mode = "always_require"

    system_prompt = """You are the Compliance & Guardrail Agent.
Your role is to ensure every rate recommendation complies with regulations
and to gate human approval before any rate change is applied.

Compliance checks:
1. ANTITRUST: Verify only permitted, broker-shared data was used
   - No direct carrier-to-carrier price coordination
   - Only publicly available or broker-provided market data
   
2. RATE FILING: Ensure proposed rate is within filed rate bands
   - Check against state/territory filing requirements
   - Verify no unfair discrimination
   
3. REGULATORY: Align with applicable insurance regulations
   - NAIC Model AI Bulletin compliance (US markets)
   - FCA/PRA guidelines (UK markets)
   - Local regulatory requirements per jurisdiction
   
4. GUARDRAIL ENFORCEMENT:
   - Rate adjustment within configured % band
   - No automated rate changes without human sign-off
   - Audit trail complete and traceable
   
5. DATA GOVERNANCE:
   - Policyholder PII not exposed in competitive analysis
   - Competitor data sourced only from permitted channels
   - All processing logged for regulatory inspection

Output: APPROVED (with conditions) or BLOCKED (with reason).
If APPROVED, present approval card to team leader for sign-off.
"""

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Run compliance checks and request human approval."""
        
        recommendation = input_data.get("recommendation")
        
        # Run compliance validation
        compliance_result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Validate this recommendation:\n{recommendation}"}
            ],
            response_format={"type": "json_object"}
        )
        
        # If compliance passes, request human approval
        if compliance_result.get("status") == "APPROVED":
            approval = await ctx.request_info(
                prompt=(
                    f"Rate change approval required:\n"
                    f"Action: {recommendation.get('action_type')}\n"
                    f"Adjustment: {recommendation.get('adjustment_percent', 0)}%\n"
                    f"Rationale: {recommendation.get('rationale')}\n\n"
                    f"Approve this rate change?"
                ),
                options=["Approve", "Reject", "Modify"]
            )
            
            return {
                "compliance_status": "APPROVED",
                "human_decision": approval,
                "audit_trail": compliance_result
            }
        else:
            return {
                "compliance_status": "BLOCKED",
                "reason": compliance_result.get("reason"),
                "audit_trail": compliance_result
            }
