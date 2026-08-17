"""
Risk Assessment Agent — appetite match and exposure scoring.

Evaluates whether the risk fits carrier appetite and scores exposure level.
Grounded on underwriting manuals and appetite guides via Azure AI Search.

Azure Services: Azure OpenAI, Azure AI Search
"""

from typing import Any
from agent_framework import Agent, AgentContext


class RiskAssessmentAgent(Agent):
    """Scores risk appetite match and exposure level."""

    name = "risk-assessment-agent"
    description = "Evaluate risk against carrier appetite and score exposure"
    model = "gpt-4o"

    system_prompt = """You are the Risk Assessment Agent.
Your role is to evaluate whether a submission fits carrier appetite and score the exposure.

Assess:
1. Appetite match (In-Appetite / Borderline / Decline)
   - Industry/SIC code vs. appetite guide
   - Size (revenue, employees) vs. target market
   - Territory match
   - Loss history vs. acceptable thresholds
   
2. Exposure scoring (1-10 scale)
   - Hazard grade of the industry
   - Claims frequency expectations
   - Severity potential
   - Aggregation risk
   
3. Pricing implications
   - Should rate be loaded or discounted based on risk quality?
   - Specific exclusions or conditions recommended?
   - Referral triggers (if any criteria breached)

Ground your assessment in the carrier's underwriting manuals and appetite guides.
Flag any referral triggers that require senior underwriter review.
"""

    tools = ["ai_search", "operational_datastore"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Assess risk appetite and exposure."""
        
        submission = input_data.get("submission")
        
        # RAG: retrieve appetite guides
        appetite_docs = await ctx.call_tool("ai_search", {
            "query": f"appetite guide {submission.get('product_type', '')} {submission.get('industry', '')}",
            "index": "appetite-guides",
            "top": 5
        })
        
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"Assess this risk:\n{submission}\n"
                    f"Appetite reference:\n{appetite_docs}"
                )}
            ],
            response_format={"type": "json_object"}
        )
        
        return {"risk_assessment": result}
