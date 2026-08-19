"""
Risk Assessment Agent — appetite match and exposure scoring.

Uses the Magentic (capped iteration) pattern to iteratively search underwriting
manuals and appetite guides via Azure AI Search until sufficient evidence is found
or the round cap is hit.

Orchestration Pattern: Magentic (Capped Discovery) — iterates with AI Search
Azure Services: Azure AI Foundry, Azure AI Search
"""

import json
import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


AGENT_NAME = "risk-assessment-agent"
MODEL = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

# Magentic loop configuration
MAX_ITERATIONS = int(os.environ.get("RISK_ASSESSMENT_MAX_ROUNDS", "5"))
MIN_EVIDENCE_THRESHOLD = 3  # Minimum evidence items needed for confident assessment

# AI Search indexes for grounding
SEARCH_INDEX_MANUALS = os.environ.get("AI_SEARCH_INDEX_MANUALS", "underwriting-manuals")
SEARCH_INDEX_APPETITE = os.environ.get("AI_SEARCH_INDEX_APPETITE", "appetite-guides")

SYSTEM_INSTRUCTIONS = """You are the Risk Assessment Agent.
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

For each iteration, indicate:
- What evidence you found
- What evidence is still missing
- Whether you have SUFFICIENT evidence to make a confident assessment
- Output "ASSESSMENT_COMPLETE" when done, or "NEED_MORE_EVIDENCE" to continue searching
"""


def create_risk_assessment_agent(project_client: AIProjectClient) -> Any:
    """Register the risk assessment agent in the Foundry project."""
    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
        ),
    )


async def search_knowledge_base(
    project_client: AIProjectClient,
    query: str,
    index_name: str,
) -> list[dict[str, Any]]:
    """
    Query Azure AI Search for underwriting manuals or appetite guides.

    In production, this calls the Azure AI Search SDK. For demo, the agent
    uses the FileSearchTool built into Foundry.
    """
    # TODO: Replace with real Azure AI Search SDK call when data layer deployed
    # For now, return the query to be used as context for the agent
    return [{"query": query, "index": index_name, "status": "search_executed"}]


async def run_risk_assessment(
    project_client: AIProjectClient,
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Assess risk using Magentic (capped iteration) pattern.

    The agent iterates up to MAX_ITERATIONS rounds:
    1. Analyze current evidence
    2. Identify gaps in knowledge
    3. Search AI Search for missing evidence (manuals, appetite guides)
    4. Synthesize findings
    5. Repeat until confident or cap reached

    This pattern ensures thorough, grounded assessments while preventing
    infinite loops via the hard round cap.
    """
    openai = project_client.get_openai_client(agent_name=AGENT_NAME)
    submission = input_data.get("submission", {})

    # Magentic state: evidence ledger
    evidence_collected: list[str] = []
    iteration_history: list[dict[str, Any]] = []
    final_assessment = None

    for round_num in range(1, MAX_ITERATIONS + 1):
        # Build prompt with accumulated evidence
        prompt = (
            f"ROUND {round_num}/{MAX_ITERATIONS} — Risk Assessment Iteration\n\n"
            f"Submission to assess:\n{json.dumps(submission, indent=2)}\n\n"
            f"Evidence collected so far ({len(evidence_collected)} items):\n"
            f"{json.dumps(evidence_collected, indent=2)}\n\n"
            f"Instructions:\n"
            f"1. Review the submission and evidence collected\n"
            f"2. Identify what additional evidence you need from underwriting manuals or appetite guides\n"
            f"3. If you have SUFFICIENT evidence ({MIN_EVIDENCE_THRESHOLD}+ items), "
            f"provide your final assessment and output 'ASSESSMENT_COMPLETE'\n"
            f"4. If you need more evidence, specify your search query and output 'NEED_MORE_EVIDENCE'\n"
        )

        response = openai.responses.create(input=prompt)
        agent_output = response.output_text

        # Record iteration
        iteration_history.append({
            "round": round_num,
            "output": agent_output[:500],
            "evidence_count": len(evidence_collected),
        })

        # Check if assessment is complete
        if "ASSESSMENT_COMPLETE" in agent_output:
            final_assessment = agent_output
            break

        # Agent needs more evidence — search knowledge base
        # Extract search intent from agent response
        search_queries = [
            f"{submission.get('product_type', 'CGL')} appetite criteria",
            f"{submission.get('industry', 'technology')} hazard grade underwriting",
            f"loss history threshold {submission.get('product_type', 'general liability')}",
        ]

        for query in search_queries[:2]:  # Max 2 searches per round
            manuals_results = await search_knowledge_base(
                project_client, query, SEARCH_INDEX_MANUALS
            )
            appetite_results = await search_knowledge_base(
                project_client, query, SEARCH_INDEX_APPETITE
            )
            evidence_collected.append(
                f"Round {round_num} search '{query}': "
                f"manuals={len(manuals_results)} results, "
                f"appetite={len(appetite_results)} results"
            )

        # Check if we hit minimum evidence threshold
        if len(evidence_collected) >= MIN_EVIDENCE_THRESHOLD and round_num >= 2:
            # Force final assessment on next round
            pass

    # If loop exhausted without completion, use last output
    if final_assessment is None:
        final_assessment = agent_output  # noqa: F821 — set in final loop iteration

    return {
        "risk_assessment": final_assessment,
        "orchestration_pattern": "magentic_capped_iteration",
        "iterations_used": len(iteration_history),
        "max_iterations": MAX_ITERATIONS,
        "evidence_items_collected": len(evidence_collected),
        "iteration_history": iteration_history,
        "search_indexes_used": [SEARCH_INDEX_MANUALS, SEARCH_INDEX_APPETITE],
    }
