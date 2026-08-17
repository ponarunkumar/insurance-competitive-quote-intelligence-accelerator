"""
Submission Intake Agent — parses and structures incoming risk submissions.

Handles text, document, and structured data inputs.
Uses Azure Document Intelligence for PDF/image processing.
"""

from typing import Any
from agent_framework import Agent, AgentContext


class SubmissionIntakeAgent(Agent):
    """Parses incoming submissions into a structured risk record."""

    name = "submission-intake-agent"
    description = "Parse and structure insurance risk submissions from any input format"
    model = "gpt-4o-mini"  # Cost-optimized for structured extraction

    system_prompt = """You are the Submission Intake Agent for an insurance contact center.
Your role is to extract and structure risk information from incoming submissions.

You handle multiple input formats:
- Free text (advisor typing or pasting risk details)
- Parsed document content (from Document Intelligence)
- Structured form data (from web forms or APIs)
- Transcribed voice input (from Speech-to-Text)

Extract the following fields into a standardized submission record:
- Product type (CGL, Property, Professional Liability, etc.)
- Insured name and details
- Business description and SIC/NAICS code
- Annual revenue/turnover
- Number of employees
- Location(s) and territory
- Requested limits and deductibles
- Prior insurance history
- Loss history summary
- Special conditions or endorsements requested

Output a structured JSON submission record conforming to the SubmissionRecord schema.
Always flag missing required fields for follow-up.
"""

    tools = ["quote_parser", "certificate_parser", "loss_run_parser", "content_understanding"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process the submission and return a structured risk record."""
        
        input_type = input_data.get("type", "text")
        
        if input_type == "document":
            # Use Document Intelligence to extract structured data
            parsed = await ctx.call_tool("quote_parser", {
                "document_url": input_data["document_url"]
            })
            input_data["parsed_content"] = parsed
        
        elif input_type == "image":
            # Use Content Understanding for multimodal input
            parsed = await ctx.call_tool("content_understanding", {
                "content_url": input_data["content_url"],
                "content_type": input_data.get("content_type", "image")
            })
            input_data["parsed_content"] = parsed
        
        # Use LLM to structure the extraction
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Extract a structured submission from: {input_data}"}
            ]
        )
        
        return result
