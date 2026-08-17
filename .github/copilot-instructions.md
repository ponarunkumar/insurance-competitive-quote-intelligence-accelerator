# Copilot Instructions

This repository is the **Insurance Competitive Quote Intelligence Accelerator** — a multi-agent AI system for insurance contact centers built on Microsoft Azure.

## Repository Context

- **Framework**: Microsoft Agent Framework (Python 3.12)
- **Infrastructure**: Azure Bicep (modular, 3-stage deployment)
- **Agents**: 14 specialist agents orchestrated by a central Orchestrator
- **Schemas**: Pydantic models define all inter-agent contracts (`src/models/schemas.py`)
- **Deployment**: Azure Developer CLI (`azd up`) or Deploy to Azure button

## Architecture Patterns

This system uses 5 orchestration patterns:

1. **Handoff** — Orchestrator routes by input modality (text/voice/document)
2. **Sequential** — Pipeline: Intake → Normalize → Compare → Recommend → Comply → Explain
3. **Concurrent** — Fan-out to N competitor APIs simultaneously
4. **Magentic (capped)** — Open-ended RAG research with round limits
5. **HITL Gate** — Human approval required before rate recommendations proceed

## Code Conventions

- All agents inherit from `agent_framework.Agent`
- Each agent defines: `name`, `model`, `system_prompt`, and `async def run(self, context)`
- Inter-agent data contracts use Pydantic models from `src/models/schemas.py`
- Tools are standalone modules in `src/tools/` registered in `agent.yaml`
- Infrastructure uses Azure Bicep with conditional deployment flags
- Python code follows PEP 8 with type hints on all function signatures
- Use `async/await` for all agent methods and tool calls
- Docstrings use triple-quote format with a one-line summary

## File Structure

```
src/
├── agents/           # 14 specialist agents (one class per file)
│   ├── orchestrator.py
│   ├── intake/       # Submission + Voice intake
│   ├── market_intelligence/  # Price collection + Normalization
│   ├── analysis/     # Coverage, Pricing, Risk
│   ├── decision/     # Recommendation + Compliance (HITL)
│   ├── communication/  # Advisor explanation + Voice response
│   └── coaching/     # Call analytics + Advisor coaching
├── tools/            # Azure service integrations
│   ├── speech/       # STT, TTS, translation, diarization
│   ├── documents/    # Document Intelligence (OCR, parsing)
│   ├── data/         # SQL, Cosmos, AI Search, Fabric
│   ├── market/       # Competitor API via APIM
│   └── contact_center/  # ACS call recording
├── workflows/        # Pipeline definitions (3 workflows)
└── models/           # Pydantic schemas (data contracts)

infra/
├── main.bicep        # Master template (3-stage conditional)
├── main.json         # Compiled ARM (for Deploy to Azure button)
└── modules/          # Bicep modules by Azure service category

tests/                # pytest test suite
docs/                 # Architecture, Agents reference, Getting Started
```

## How to Add a New Agent

1. Create a new file in the appropriate `src/agents/<category>/` directory
2. Define a class inheriting from `Agent` with `name`, `model`, `system_prompt`, and `run()` method
3. Define input/output schemas in `src/models/schemas.py` if needed
4. Register the agent in `agent.yaml` under the `agents:` section
5. Add to the appropriate workflow in `src/workflows/`
6. Add unit tests in `tests/unit/agents/`

## How to Add a New Tool

1. Create a module in `src/tools/<category>/`
2. Implement the tool function with proper type hints and error handling
3. Register in `agent.yaml` under the `tools:` section
4. Reference from the agent that uses it

## Key Schemas

The following Pydantic models in `src/models/schemas.py` are the core data contracts:

- `SubmissionRecord` — Structured risk profile (output of Intake)
- `NormalizedQuote` — Standardized competitor quote
- `ComparisonMatrix` — Side-by-side coverage analysis
- `PricingVariance` — Market position and adequacy verdict
- `RiskAssessment` — Appetite match and exposure score
- `Recommendation` — Rate action with guardrail enforcement
- `ComplianceResult` — Regulatory validation result
- `QuoteIntelligenceResult` — Complete pipeline output

## Infrastructure Rules

- All Azure resources are defined in Bicep modules under `infra/modules/`
- The master `infra/main.bicep` uses conditional deployment (`if` statements)
- Three deployment stages: Core AI (default) → Data (optional) → Integration (optional)
- After modifying `main.bicep`, recompile: `az bicep build --file infra/main.bicep --outfile infra/main.json`
- Use managed identity for all service-to-service auth (no secrets in code)

## Testing Approach

- Unit tests: pytest with mocked Azure services
- Contract tests: Validate Pydantic schema compliance between agents
- Integration tests: Real Azure endpoints (requires deployed infrastructure)
- Use `pytest-asyncio` for async agent testing
- Mock OpenAI responses for deterministic unit tests

## Important Notes

- The Compliance Guardrail agent has `approval_mode: always_require` — never remove this
- Pricing Variance calculations must validate denominator ≠ 0
- Recommendation adjustments must stay within `guardrail_band_used` percentage
- Voice flows require Azure AI Speech resource to be deployed (Stage 1)
- Competitor API calls go through APIM (Stage 3) — mock locally for development
