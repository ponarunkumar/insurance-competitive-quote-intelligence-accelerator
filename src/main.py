"""
Insurance Competitive Quote Intelligence — Main Entry Point

Runs the quote intelligence pipeline locally or in demo mode.

Usage:
    python src/main.py                  # Interactive mode
    python src/main.py --demo           # Run with sample data
    python src/main.py --register       # Register agents only

Requires:
    - FOUNDRY_PROJECT_ENDPOINT environment variable
    - Azure CLI authenticated (az login)
    - Agents registered (run with --register first)
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Pipeline agent names in execution order
PIPELINE_AGENTS = [
    ("submission-intake-agent", "Submission Intake"),
    ("competitor-price-collection-agent", "Price Collection"),
    ("quote-normalization-agent", "Quote Normalization"),
    ("coverage-comparison-agent", "Coverage Comparison"),
    ("pricing-variance-agent", "Pricing Variance"),
    ("risk-assessment-agent", "Risk Assessment"),
    ("recommendation-agent", "Recommendation"),
    ("compliance-guardrail-agent", "Compliance Gate (HITL)"),
    ("advisor-explanation-agent", "Advisor Explanation"),
]


def print_banner():
    print()
    print("━" * 64)
    print("  Insurance Competitive Quote Intelligence Accelerator")
    print("  Powered by Microsoft Foundry SDK")
    print("━" * 64)
    print()


def load_sample_data() -> dict:
    """Load the sample request from data/sample_request.json."""
    sample_path = Path(__file__).parent.parent / "data" / "sample_request.json"
    if not sample_path.exists():
        print(f"ERROR: Sample data not found at {sample_path}")
        sys.exit(1)
    with open(sample_path) as f:
        return json.load(f)


async def run_pipeline(project_client: AIProjectClient, input_data: dict) -> dict:
    """Execute the quote intelligence pipeline step by step."""
    results = {}
    pipeline_context = json.dumps(input_data, indent=2)
    total_start = time.time()

    print("Pipeline Execution")
    print("=" * 64)

    for i, (agent_name, display_name) in enumerate(PIPELINE_AGENTS, 1):
        step_start = time.time()
        print(f"\n  Step {i}/{len(PIPELINE_AGENTS)}: {display_name}")
        print(f"  Agent: {agent_name}")
        print(f"  {'─' * 50}")

        try:
            openai = project_client.get_openai_client(agent_name=agent_name)

            prompt = (
                f"Process the following data through your pipeline step.\n\n"
                f"Context from previous steps:\n{pipeline_context}\n\n"
                f"Original submission:\n{json.dumps(input_data.get('submission', {}), indent=2)}"
            )

            response = openai.responses.create(input=prompt)

            step_result = response.output_text
            elapsed = time.time() - step_start

            results[agent_name] = step_result
            pipeline_context = step_result

            # Show abbreviated output
            preview = step_result[:200] + "..." if len(step_result) > 200 else step_result
            print(f"  ✅ Complete ({elapsed:.1f}s)")
            print(f"  Output: {preview}")

        except Exception as e:
            elapsed = time.time() - step_start
            print(f"  ❌ Failed ({elapsed:.1f}s): {e}")
            results[agent_name] = f"ERROR: {e}"

    total_elapsed = time.time() - total_start
    print()
    print("=" * 64)
    print(f"  Pipeline complete in {total_elapsed:.1f}s")
    print(f"  Agents invoked: {len(PIPELINE_AGENTS)}")
    print("=" * 64)

    return results


async def run_interactive(project_client: AIProjectClient):
    """Interactive mode — chat with the orchestrator."""
    print("Interactive Mode — Chat with the Orchestrator")
    print("Type 'quit' to exit, 'demo' to run sample pipeline")
    print("─" * 64)

    orchestrator_name = "quote-intelligence-orchestrator"

    try:
        openai = project_client.get_openai_client(agent_name=orchestrator_name)
        conversation = openai.conversations.create()
        print(f"  Conversation started: {conversation.id}")
        print()

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                break
            if user_input.lower() == "demo":
                sample_data = load_sample_data()
                await run_pipeline(project_client, sample_data)
                continue

            response = openai.responses.create(
                conversation=conversation.id,
                input=user_input,
            )
            print(f"\nOrchestrator: {response.output_text}\n")

    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Run 'python src/register_agents.py' first to register agents.")


def main():
    parser = argparse.ArgumentParser(
        description="Insurance Competitive Quote Intelligence Accelerator"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run pipeline with sample data (data/sample_request.json)"
    )
    parser.add_argument(
        "--register", action="store_true",
        help="Register all 14 agents in Foundry project"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Save pipeline output to a JSON file"
    )
    args = parser.parse_args()

    print_banner()

    # Check endpoint
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    if not endpoint:
        print("ERROR: FOUNDRY_PROJECT_ENDPOINT environment variable not set.")
        print("Set it to: https://<resource-name>.services.ai.azure.com/api/projects/<project-name>")
        sys.exit(1)

    print(f"Foundry endpoint: {endpoint}")
    print()

    # Handle --register
    if args.register:
        from register_agents import main as register_main
        register_main()
        return

    # Create project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    ):
        if args.demo:
            # Demo mode — run pipeline with sample data
            print("Mode: Demo (sample data)")
            print()
            sample_data = load_sample_data()
            print(f"Submission: {sample_data['submission']['insured_name']}")
            print(f"Product: {sample_data['submission']['product_type']}")
            print(f"Competitors: {len(sample_data['competitor_quotes'])}")
            print()

            results = asyncio.run(run_pipeline(project_client, sample_data))

            if args.output:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump(results, f, indent=2)
                print(f"\nResults saved to: {output_path}")
        else:
            # Interactive mode
            asyncio.run(run_interactive(project_client))


if __name__ == "__main__":
    main()
