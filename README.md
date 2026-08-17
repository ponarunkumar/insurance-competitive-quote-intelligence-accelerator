# Insurance Competitive Quote Intelligence Accelerator

> **Multi-agent AI system for competitive quote intelligence in insurance contact centers**  
> Built on Microsoft Azure AI Foundry, Microsoft Agent Framework, and the full Azure AI & Apps stack.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/)

---

## 📖 Overview

### The Problem

Insurance contact center advisors spend **1–2 hours per quote** manually comparing competitor pricing across multiple carrier portals and spreadsheets. This manual process results in:

- **Slow quote turnaround** — customers wait while advisors toggle between systems
- **Incomplete market visibility** — advisors check 2–3 competitors at most
- **Inconsistent pricing decisions** — no standardized methodology for rate adequacy
- **Lost business** — conversion rates suffer when pricing isn't competitive or advisors can't articulate value
- **Compliance risk** — undocumented rate decisions with no audit trail

### The Solution

This accelerator deploys a **governed, multi-agent AI system** that reduces competitive quote comparison from hours to minutes, analyzing 10+ coverage dimensions across 5+ competitors simultaneously — with full auditability and human approval on every rate change.

### Who Is This For?

| Audience | What you'll find here |
|----------|----------------------|
| **Contact Center Leaders & Business Stakeholders** | A production-ready AI system that improves advisor productivity, conversion rates, and pricing accuracy — with governance and human oversight built in |
| **Developers & Platform Engineers** | A complete, deployable template: infrastructure-as-code, agent stubs with API contracts, sample data, and `azd up` for one-command provisioning |
| **AI Engineers & Solution Architects** | Multi-agent orchestration patterns (Sequential, Concurrent, Handoff, Magentic), agent design principles, tool/grounding architecture, and HITL governance patterns |

### Solution Play Alignment

This accelerator aligns with the **FY27 Innovate with AI & Apps** solution play:

| Pillar | How This Accelerator Delivers |
|--------|-------------------------------|
| **Amplify Your Intelligence** | Multi-agent AI transforms advisor decision-making from manual research to AI-augmented insight |
| **Azure AI Services** | 24 Azure services provisioned — every agent interaction leverages AI compute and storage |
| **Microsoft Cloud Platform** | Copilot Studio + M365 E5 + Entra P2 + Fabric — full Microsoft platform |
| **AI & Apps Modernization** | Legacy spreadsheet/portal workflows replaced with governed, observable AI agents |
| **Responsible AI** | Human-in-the-loop, Purview governance, antitrust guardrails, full audit trail |

---

## 🎯 What This Accelerator Does

Enables insurance carriers to deploy an AI-powered **competitive quote intelligence** system that:

1. **Ingests** risk submissions via text, voice, or document (multimodal)
2. **Collects** competitor pricing from market sources in parallel
3. **Normalizes** diverse quote formats into a unified comparison schema
4. **Compares** coverage across 10+ dimensions side-by-side
5. **Assesses** rate adequacy and competitive market position
6. **Recommends** rate actions within governed guardrail bands
7. **Requires** human approval before any rate change (HITL)
8. **Explains** recommendations in advisor-friendly language (text or voice)

### Quantified Business Value

| Metric | Before | After | Source |
|--------|--------|-------|--------|
| Quote comparison time | 1–2 hours | 5–10 minutes | Industry benchmark |
| Coverage dimensions analyzed | 3–5 | 10+ | Architecture design |
| Competitor sources checked | 2–3 | 5–10 (configurable) | Concurrent agent pattern |
| Hit/conversion ratio improvement | Baseline | +10–15% | Industry benchmark |
| Advisor admin time reclaimed | ~40% of day | Redirected to selling | McKinsey underwriting study |
| Rate decision audit trail | Manual/none | 100% automated | HITL + OpenTelemetry |

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│  EXPERIENCE: Copilot Studio in Teams / Web / Voice      │
└────────────────────────┬────────────────────────────────┘
                         │ A2A
┌────────────────────────▼────────────────────────────────┐
│  ORCHESTRATOR: Microsoft Agent Framework                │
│  (Sequential + Concurrent + Handoff patterns)           │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  14 SPECIALIST AGENTS                                   │
│  Intake │ Voice │ Price Collection │ Normalization │    │
│  Coverage │ Pricing │ Risk │ Recommendation │           │
│  Compliance (HITL) │ Explanation │ Voice Response │     │
│  Call Analytics │ Advisor Coaching                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  24 AZURE SERVICES                                      │
│  OpenAI │ AI Search │ Speech (STT/TTS/Translation) │   │
│  Doc Intelligence │ Content Understanding │ Language │  │
│  ACS │ SQL │ Cosmos │ Fabric │ APIM │ Monitor │        │
│  Entra │ Purview │ Defender │ Key Vault                 │
└─────────────────────────────────────────────────────────┘
```

### Agent Pipeline Flow

```
User Request (text / voice / document)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR — routes based on modality and intent                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ① Submission Intake ──────────► Structured risk record             │
│         │                                                           │
│  ② Competitor Price Collection ─► [CONCURRENT: N sources]           │
│         │                           ├─ Carrier A ─┐                 │
│         │                           ├─ Carrier B ─┤                 │
│         │                           ├─ Carrier C ─┼─► Aggregated    │
│         │                           ├─ Carrier D ─┤    quotes       │
│         │                           └─ Carrier E ─┘                 │
│         │                                                           │
│  ③ Quote Normalization ─────────► Common schema                     │
│         │                                                           │
│  ④ Coverage Comparison ─────────► Side-by-side matrix               │
│         │                                                           │
│  ⑤ Pricing Variance ───────────► Market position + adequacy         │
│         │                                                           │
│  ⑥ Risk Assessment ────────────► Appetite match + exposure score    │
│         │                                                           │
│  ⑦ Recommendation ─────────────► Proposed rate action               │
│         │                                                           │
│  ⑧ Compliance & Guardrail ─────► [HITL GATE: Human approves]       │
│         │                              ▲                            │
│         │                              │ Team leader clicks         │
│         │                              │ "Approve" in Teams         │
│         ▼                                                           │
│  ⑨ Advisor Explanation ─────────► Plain-language talk-track         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
Result delivered (text in Teams, voice via TTS, or both)
```

### Orchestration Patterns (for AI Engineers)

| Pipeline Segment | Pattern | Why This Pattern |
|---|---|---|
| Request triage (text vs voice vs doc) | **Handoff** | Single active agent; clean routing |
| Intake → Normalize → Compare → Recommend | **Sequential** | Fixed ordered pipeline; each step depends on prior |
| Collect prices from N competitors | **Concurrent** | Independent lookups; aggregated; fastest market coverage |
| Open-ended source discovery | **Magentic (capped)** | Plan-and-replan with round limits; handles unknown sources |
| Rate change approval | **HITL Gate** | `approval_mode="always_require"` — non-negotiable for compliance |

### Design Principles (for AI Engineers)

1. **One agent, one job** — each agent has a narrow, testable responsibility
2. **Tool scope follows agent role** — agents only access data they need (enforced via Entra RBAC)
3. **Prompts are configuration, not code** — system prompts are editable markdown files
4. **Schemas are contracts** — Pydantic models define what flows between agents
5. **Human approves, AI recommends** — no autonomous rate changes
6. **Observable by default** — OpenTelemetry traces every step, visible in Azure Monitor
7. **Model selection follows complexity** — GPT-4o for reasoning, GPT-4o-mini for extraction/generation

---

## 🚀 Quick Start

### Prerequisites

- Azure subscription with **Owner** or **Contributor + User Access Administrator** access
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) v1.10+
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) v2.60+ (logged in via `az login`)
- Python 3.12+
- Docker (for local testing of the container image)

### Deploy (One Command)

```bash
# Clone the repository
git clone https://github.com/your-org/insurance-competitive-quote-intelligence-accelerator.git
cd insurance-competitive-quote-intelligence-accelerator

# Copy environment template and configure
cp .env.sample .env
# Edit .env with your Azure subscription details, region, and credentials

# Provision all 24 Azure services and deploy the agent
azd up
```

### What `azd up` Provisions

| Category | Services Deployed |
|----------|-------------------|
| **AI Foundry** | Hub, Project, Agent Service, Hosted Agent runtime |
| **Models** | Azure OpenAI (GPT-4o @ 80K TPM, GPT-4o-mini @ 120K TPM) |
| **Search & RAG** | Azure AI Search (Standard S1, Semantic Ranking enabled) |
| **Speech** | Azure AI Speech (STT, TTS, Translation, Diarization, Custom Speech, Voice Live) |
| **Document** | Azure Document Intelligence (S0), Content Understanding |
| **Language** | Azure AI Language (Sentiment, PII, Summarization) |
| **Communication** | Azure Communication Services (Voice, Call Recording) |
| **Data** | Azure SQL (GP_S_Gen5_2), Cosmos DB (Serverless), Fabric (F2) |
| **Integration** | API Management (Standard v2 — AI Gateway) |
| **Observability** | Log Analytics, Application Insights |
| **Security** | Key Vault, Entra Agent Identities (7 managed identities), RBAC |
| **Governance** | Microsoft Purview, Defender for Cloud |

### Verify Deployment

```bash
# Check agent endpoint is responding
azd env get-value AGENT_ENDPOINT
curl -s $(azd env get-value AGENT_ENDPOINT)/health

# View agent traces
az monitor app-insights query --app $(azd env get-value APP_INSIGHTS_NAME) \
  --analytics-query "traces | where timestamp > ago(5m) | take 10"
```

---

## 📂 Project Structure

```
insurance-competitive-quote-intelligence-accelerator/
│
├── infra/                          Infrastructure-as-Code (Bicep)
│   ├── main.bicep                  Master orchestration (provisions all 24 services)
│   ├── main.parameters.json        Environment-specific parameters
│   └── modules/
│       ├── core/                   Key Vault, Log Analytics, App Insights
│       ├── ai-foundry/             Hub, Project, Agent Service, Model Deployments
│       ├── ai-services/            AI Search, Doc Intelligence, Content Understanding, Language
│       ├── speech/                 STT, TTS, Translation, Diarization, Custom Speech, Voice Live
│       ├── communication/          Azure Communication Services, Call Automation
│       ├── data/                   Azure SQL, Cosmos DB, Fabric Lakehouse
│       ├── integration/            API Management (AI Gateway) + APIM policies
│       └── governance/             Entra Identities, RBAC, Purview, Defender
│
├── src/
│   ├── agents/                     14 specialist agent implementations
│   │   ├── orchestrator.py         Central coordinator (routes & delegates)
│   │   ├── intake/                 Submission + Voice intake agents
│   │   ├── market_intelligence/    Price collection + Normalization agents
│   │   ├── analysis/               Coverage, Pricing Variance, Risk Assessment agents
│   │   ├── decision/               Recommendation + Compliance (HITL) agents
│   │   ├── communication/          Advisor Explanation + Voice Response agents
│   │   └── coaching/               Call Analytics + Advisor Coaching agents
│   ├── tools/                      Azure service integrations
│   │   ├── speech/                 STT, TTS, Translation, Diarization, Summarization
│   │   ├── documents/              Quote Parser, Content Understanding
│   │   ├── data/                   Azure SQL, AI Search, Fabric
│   │   ├── market/                 Competitor API (via APIM)
│   │   └── contact_center/         Call Recording, Dispositions
│   ├── workflows/                  3 pipeline definitions
│   │   ├── quote_intelligence.py   Primary: text/doc → analysis → recommendation
│   │   ├── voice_quote_intelligence.py  Voice-first: call → STT → analysis → TTS
│   │   └── coaching_report.py      Secondary: call analytics → coaching insights
│   └── models/                     Pydantic schemas (API contracts between agents)
│       ├── schemas.py              Core: Submission, Quote, Comparison, Recommendation
│       ├── speech_models.py        Transcription, TTS, Translation models
│       └── contact_center_models.py  Call analytics, coaching, performance models
│
├── data/                           Sample data for demos and testing
│   ├── sample_submission.json      Example CGL risk (£2M builder)
│   ├── sample_quotes/              5 competitor quote examples
│   └── seed_sql.sql                Database schema + seed data
│
├── tests/                          Test suites
│   ├── unit/                       Agent logic tests (mocked tools)
│   ├── integration/                Tool integration tests (real Azure services)
│   └── e2e/                        Full pipeline tests
│
├── docs/                           Detailed documentation
│
├── azure.yaml                      Azure Developer CLI manifest
├── agent.yaml                      Foundry Hosted Agent manifest (14 agents, 3 workflows)
├── pyproject.toml                  Python dependencies and tooling config
├── Dockerfile                      Container image for deployment
├── .env.sample                     Environment variable template
└── README.md                       ← You are here
```

---

## 👩‍💻 Developer Guide

### For Developers: How to Extend This Accelerator

#### Adding a New Agent

1. Create a new Python file in the appropriate `src/agents/` subdirectory
2. Inherit from `Agent` base class
3. Define: `name`, `description`, `model`, `system_prompt`, `tools`
4. Implement the `run()` method
5. Register in `agent.yaml`
6. Wire into the appropriate workflow in `src/workflows/`

```python
# Example: Adding a "Renewal Pricing Agent"
from agent_framework import Agent, AgentContext

class RenewalPricingAgent(Agent):
    name = "renewal-pricing-agent"
    model = "gpt-4o"
    system_prompt = """..."""
    tools = ["operational_datastore", "ai_search"]

    async def run(self, ctx: AgentContext, input_data: dict) -> dict:
        # Your logic here
        return {"renewal_recommendation": result}
```

#### Adding a New Competitor Source

1. Add a backend in `infra/modules/integration/apim-policies/competitor-api-routing.xml`
2. Create or reuse the MCP tool in `src/tools/market/competitor_api.py`
3. Add the carrier to the `competitors` list in your `.env`
4. No redeployment of other agents needed — the Concurrent pattern auto-discovers sources

#### Adding a New Product Type

1. Add to the `ProductType` enum in `src/models/schemas.py`
2. Add appetite/manual documents to your AI Search index
3. Update system prompts if product-specific logic is needed
4. The pipeline handles it automatically — no structural changes required

### Running Locally

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/unit/ -v

# Run the agent locally (mock mode)
python -m agent_framework serve --config agent.yaml --mock-tools

# Run with real Azure services (requires .env configured)
python -m agent_framework serve --config agent.yaml
```

---

## ☁️ Microsoft Cloud Services

Every service provisioned supports the solution:

| Priority | Services | Billing Model |
|----------|----------|---------------|
| **Core (new ACR)** | Azure OpenAI, Foundry Agent Service, AI Search, Copilot Studio, Fabric | Token + session + unit + message + CU billing |
| **Expand existing** | Azure SQL, Entra ID P2, M365 E5 | Tier-up + seat expansion |
| **Land new** | Document Intelligence, AI Speech, Content Understanding, ACS, Purview, Monitor | Per-transaction + per-hour + per-asset |
| **Strategic** | Frontier Tuning, Defender for Cloud | Training hours + per-resource protection |

### Estimated Monthly Azure Consumption (Production Scale)

> Based on a contact center with ~400 quote requests/day, 4 team leaders, 20 advisors

| Service | Usage Driver | Est. Monthly |
|---------|-------------|-------------|
| Azure OpenAI | ~12 agents × 400 calls × ~2K tokens avg | Significant token volume |
| Foundry Agent Service | 400 sessions/day × 30 days | Per-session billing |
| Azure AI Search | Always-on Standard S1 + semantic queries | Fixed + per-query |
| Azure AI Speech | ~100 voice calls/day × avg 5 min | Per-audio-hour |
| Document Intelligence | ~50 documents/day × avg 3 pages | Per-page |
| API Management | ~2000 competitor API calls/day | Per-call |
| Azure SQL | GP_S_Gen5_2 (serverless auto-scale) | vCore-seconds |
| Fabric | F2 capacity for analytics | Fixed CU/month |

*Exact figures depend on deployment scale. Template supports scale-to-zero when idle.*

---

## 🔧 Customization

This accelerator is designed to be adapted for any insurance carrier:

1. **Edit system prompts** in `src/prompts/` for your product lines and terminology
2. **Configure competitors** in `.env` and APIM backend settings
3. **Adjust guardrail bands** via `GUARDRAIL_BAND_PERCENT` environment variable
4. **Add product types** by extending the `ProductType` enum in `src/models/schemas.py`
5. **Train Custom Speech** with your industry terminology for improved transcription accuracy
6. **Customize APIM policies** for your specific rate limiting and caching needs

---

## 📋 Entry Points (Multimodal)

| Modality | Entry | Azure Services |
|----------|-------|----------------|
| **Text** | Teams chat / Web | Copilot Studio → Orchestrator |
| **Voice** | Live call | ACS → Speech STT → Orchestrator → Speech TTS |
| **Document** | PDF/Image upload | Doc Intelligence → Orchestrator |
| **Email** | Attachment | AI Language → Doc Intelligence → Orchestrator |

---

## 🔒 Governance & Compliance

- **Human-in-the-Loop**: Every rate change requires team leader approval
- **Antitrust**: Only broker-shared, permitted market data processed
- **Audit Trail**: Full OpenTelemetry tracing of every agent decision
- **Data Protection**: PII handled per GDPR/FCA guidelines via Purview
- **Zero Trust**: Each agent has its own Entra identity with least-privilege RBAC

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Getting Started](docs/GETTING_STARTED.md)
- [API Contracts](docs/API_CONTRACTS.md)
- [Speech Setup Guide](docs/SPEECH_SETUP.md)
- [Multimodal Guide](docs/MULTIMODAL_GUIDE.md)
- [Contact Center Integration](docs/CONTACT_CENTER_INTEGRATION.md)
- [Customization Guide](docs/CUSTOMIZATION.md)
- [Azure Services Map](docs/AZURE_SERVICES_MAP.md)

---

## 🤝 Contributing

This accelerator is designed for the insurance industry. Contributions welcome for:
- Additional product type support (Property, Marine, Specialty)
- New competitor API integrations (US, EU, APAC markets)
- Regulatory compliance modules for additional jurisdictions (NAIC, FCA, APRA, BaFin)
- Language and locale support (prompts, speech models)
- Performance optimizations and caching strategies
- UI/UX patterns for Copilot Studio front-end

### Development Standards

- Python 3.12+ with type hints
- Pydantic v2 for all data models
- `ruff` for linting (configured in `pyproject.toml`)
- `pytest` with async support for testing
- Bicep with Azure Verified Modules (AVM) patterns
- Conventional Commits for git history

---

## ❓ FAQ

**Q: Can this work with carriers outside the UK?**  
A: Yes. Change `AZURE_LOCATION`, speech language settings, and currency in `.env`. The architecture is region and locale-agnostic.

**Q: Do I need all 24 Azure services for a POC?**  
A: No. Start with the core pipeline (OpenAI + AI Search + Agent Service + SQL) and add speech/document/governance services incrementally. Comment out modules in `main.bicep` to reduce scope.

**Q: What models are supported?**  
A: Any model in the Azure OpenAI catalog. The template defaults to GPT-4o (reasoning) and GPT-4o-mini (extraction/generation). Swap via `model-deployments.bicep`.

**Q: How do I connect real competitor rating APIs?**  
A: Add backend endpoints in the APIM competitor API routing policy (`infra/modules/integration/apim-policies/competitor-api-routing.xml`). The agent's MCP tool routes through APIM automatically.

**Q: Is this safe for production use with real policyholder data?**  
A: The template includes enterprise governance (Entra RBAC, Purview, Defender, PII detection via AI Language, encrypted storage). However, you must complete your own security review, penetration testing, and regulatory approval before production deployment with real data.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with Microsoft Azure AI Foundry, Microsoft Agent Framework, and the full Azure AI & Apps stack.*
