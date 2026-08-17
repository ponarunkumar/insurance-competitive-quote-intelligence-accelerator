"""
Quote Normalization Agent — standardizes competitor quotes to a common schema.

Maps disparate carrier quote formats into a unified comparison structure.
Handles variations in terminology, coverage definitions, and pricing models.

Azure Services: Azure OpenAI for LLM-based normalization
"""

from typing import Any
from agent_framework import Agent, AgentContext


class QuoteNormalizationAgent(Agent):
    """Normalizes competitor quotes to a common schema for comparison."""

    name = "quote-normalization-agent"
    description = "Standardize diverse carrier quotes into a unified comparison format"
    model = "gpt-4o-mini"

    system_prompt = """You are the Quote Normalization Agent.
Your role is to map competitor quotes from various formats into a standardized schema.

Normalize each quote to include:
- Annual premium (gross and net of commission)
- Policy limits (per-occurrence and aggregate)
- Deductible/excess amounts
- Coverage forms and editions
- Key exclusions and limitations
- Commission percentage
- Payment terms
- Policy period
- Endorsements included/available
- Territory and jurisdiction

Handle common variations:
- Convert monthly to annual premiums
- Standardize currency
- Map carrier-specific terms to industry-standard terminology
- Flag coverage differences that affect true price comparison
- Identify sublimits vs. full limits

Output standardized QuoteObject records conforming to the NormalizedQuote schema.
"""

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Normalize all competitor quotes to common schema."""
        
        raw_quotes = input_data.get("competitor_quotes", [])
        
        normalized = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Normalize these quotes:\n{raw_quotes}"}
            ],
            response_format={"type": "json_object"}
        )
        
        return {"normalized_quotes": normalized}
