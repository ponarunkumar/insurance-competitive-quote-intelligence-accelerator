# Demo Scenarios

> A complete, modular demo guide for the Insurance Competitive Quote Intelligence Accelerator.
> Pick and combine scenarios based on your audience.

---

## Who Is This For?

This guide is for anyone demonstrating the accelerator:

- **Microsoft field sellers** — customer-facing demos and workshops
- **Partner solution architects** — SI/ISV technical validation sessions
- **Customer AI leads** — internal proof-of-concept walkthroughs
- **Developer advocates** — conference talks and live coding sessions

---

## Scenario Picker

Choose scenarios based on your audience and available time:

| Audience | Recommended Scenarios | Duration |
|----------|----------------------|----------|
| **CIO / Business Leader** | 1 → 3 | 8 min |
| **IT Director / Architect** | 1 → 2 → 4 | 12 min |
| **Developer / AI Engineer** | 6 → 2 → 4 → 5 | 18 min |
| **Partner / SI** | 1 → 3 → 5 | 12 min |
| **Full Demo Day** | 1 → 2 → 3 → 4 → 5 → 6 | 25 min |

### Scenario Flow

```
                    ┌──────────────────┐
                    │ 1. Fork & Deploy │ ← Start here (always)
                    └────────┬─────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
       ┌──────────────┐ ┌──────────┐ ┌───────────────┐
       │ 2. Meet the  │ │ 6. Open  │ │ 3. Ask for a  │
       │    Agents    │ │ Codespace│ │    Quote      │
       └──────┬───────┘ └────┬─────┘ └───────┬───────┘
              │              │               │
              ▼              ▼               │
       ┌──────────────┐ ┌───────────────┐    │
       │ 4. See the   │ │ 5. Customize  │    │
       │   Pipeline   │ │ with Copilot  │    │
       └──────────────┘ └───────────────┘    │
                                             ▼
                                        (End for
                                         business)
```

---

## Prerequisites & Preparation

### 24 Hours Before Demo

- [ ] Deploy Azure resources (Stage 1: Core AI) — takes ~15 min
- [ ] Run `python src/register_agents.py` — registers all 14 agents
- [ ] Verify: Open [ai.azure.com](https://ai.azure.com) → Project → Agents → confirm 14 agents listed
- [ ] Test: Paste sample submission in Foundry Playground → verify response

### 1 Hour Before Demo

- [ ] Open browser tabs: GitHub repo, Azure portal, Foundry portal (ai.azure.com)
- [ ] Open terminal with repo cloned and `.env` configured
- [ ] Clear browser history / close personal tabs
- [ ] Test internet connectivity

### 15 Minutes Before Demo

- [ ] Verify Foundry Playground responds to a test query
- [ ] Have `data/sample_request.json` open and ready to copy
- [ ] Have fallback recording ready (if live demo fails)
- [ ] Mute notifications on all devices

---

## Scenario 1: Fork & Deploy

> **Duration**: 3-5 min | **Audience**: Any | **Difficulty**: Easy

### What This Proves

*"This entire multi-agent AI system deploys to YOUR Azure tenant in 15 minutes with zero code."*

### Setup

- Browser open to the GitHub repo
- Azure portal logged in (separate tab)

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Open the GitHub repo in browser | README with architecture overview |
| 2 | Scroll to "Quick Start" section | Deploy to Azure button visible |
| 3 | Click **"Deploy to Azure"** button | Azure portal opens with Custom Deployment form |
| 4 | Select Subscription and Resource Group | Standard Azure deployment form |
| 5 | Leave deployment stage as "Core AI" (default) | Only required field is Location |
| 6 | Click **Review + Create** → **Create** | Deployment starts (show the progress) |

### Talk Track

> *"Let me show you how fast you can get started. This repository contains a complete multi-agent AI system for insurance contact centers — 14 specialist agents, 24 Azure services, all the infrastructure as code.*
>
> *I'm going to click Deploy to Azure — one click — and it starts provisioning everything in your tenant. Azure AI Foundry for hosting the agents, Azure OpenAI for reasoning, AI Search for grounding on your underwriting manuals, Speech services for voice interactions, and all the security and observability you need.*
>
> *Notice I haven't entered any credentials or API keys. Stage 1 deploys with zero secrets — it uses managed identity for everything. For a production deployment, you'd add the Data Layer and Integration Layer in stages 2 and 3.*
>
> *While this deploys — about 15 minutes — let me show you what you get..."*

### Key Message

**One click. Zero secrets. 15 minutes to a working AI agent platform.**

### Fallback

If Azure portal is slow or deployment fails:
- Show the ARM template structure in `infra/main.json`
- Walk through the 3-stage modular deployment diagram in `docs/ARCHITECTURE.md`
- Say: *"The deployment is the same infrastructure-as-code you'd use in production — Bicep templates, conditional modules, managed identity throughout."*

---

## Scenario 2: Meet the Agents

> **Duration**: 3-5 min | **Audience**: Technical | **Difficulty**: Easy

### What This Proves

*"14 specialist agents, each with a defined role, working together through 5 orchestration patterns — this isn't a chatbot, it's a production AI system."*

### Setup

- Foundry portal open at [ai.azure.com](https://ai.azure.com) → Your Project → Build → Agents
- Agents already registered (run `python src/register_agents.py` beforehand)

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Open Foundry portal → Project → Agents | List of 14 registered agents |
| 2 | Click on **quote-intelligence-orchestrator** | Agent details: model, instructions |
| 3 | Scroll through the system instructions | Detailed pipeline coordination logic |
| 4 | Go back, click on **compliance-guardrail-agent** | Shows HITL approval requirement |
| 5 | Show `docs/ARCHITECTURE.md` in browser (GitHub) | Mermaid diagram of full architecture |

### Talk Track

> *"Let me introduce you to the team. We have 14 specialist agents — each one is an expert in a specific part of the insurance quote workflow.*
>
> *Here's the Orchestrator — it's the conductor. When a request comes in, it determines whether it's text, voice, or a document, and routes it to the right intake agent. From there, it coordinates a sequential pipeline: intake, price collection, normalization, comparison, risk assessment, recommendation.*
>
> *Now look at this one — the Compliance Guardrail Agent. This is critical for insurance. It has `approval_mode: always_require`. That means NO rate recommendation ever reaches the advisor without a human team leader approving it first. This is how you build AI that regulators trust.*
>
> *And here's the architecture — 5 orchestration patterns: sequential pipeline, concurrent fan-out for competitor pricing, handoff routing by modality, capped research for risk assessment, and human-in-the-loop for compliance. This isn't a single chatbot — it's a multi-agent system designed for production."*

### Key Message

**14 agents. 5 orchestration patterns. Human-in-the-loop governance. Production-grade.**

### Fallback

If Foundry portal is unavailable:
- Open `docs/AGENTS.md` on GitHub — shows the full agent catalog table
- Open `src/agents/orchestrator.py` — show the system instructions and pipeline logic
- Walk through `agent.yaml` — shows all 14 agents and their models

---

## Scenario 3: Ask for a Quote

> **Duration**: 3-5 min | **Audience**: Any | **Difficulty**: Easy

### What This Proves

*"In under 10 seconds, an advisor gets a complete competitive analysis — market position, rate adequacy, recommendation, and a talk-track for the customer call."*

### Setup

- Foundry Playground open with `quote-intelligence-orchestrator` selected
- `data/sample_request.json` open for copy-paste

### Sample Submission (Copy-Paste This)

```
Analyze this submission for competitive quote intelligence:

Company: Nexus Digital Solutions Ltd
Industry: Technology consulting (SIC 7371)
Annual Revenue: $48,000,000
Employees: 475
Location: Austin, TX (primary), Denver, CO (satellite)
Product: Commercial General Liability (CGL)
Requested Limit: $2,000,000 per occurrence / $4,000,000 aggregate
Requested Deductible: $10,000
Current Carrier: Atlantic Mutual
Current Premium: $42,500/year
Years with Current Carrier: 3
Loss History: 1 claim in 3 years ($18,000, slip-and-fall, closed)

Competing quotes received from broker:
- Pacific Shield Insurance: $38,200 (per-occurrence $2M, aggregate $4M, $5K deductible)
- Continental Risk Partners: $41,800 (per-occurrence $2M, aggregate $4M, $10K deductible)
- Summit Specialty Group: $44,100 (per-occurrence $2M, aggregate $5M, $10K deductible, includes cyber sublimit)

Advisor needs: competitive position assessment, rate recommendation, and customer talk-track.
```

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Open Foundry Playground | Chat interface ready |
| 2 | Select `quote-intelligence-orchestrator` agent | Agent loaded |
| 3 | Paste the sample submission above | Input appears in chat |
| 4 | Press Enter / Send | Agent processes (~5-10 seconds) |
| 5 | Read through the response together | Structured analysis with recommendation |

### Talk Track

> *"Now let's see this in action. I'm going to play the role of an insurance advisor. A broker has just sent me a submission for a technology company — $48M revenue, 475 employees, they want CGL coverage. They've also shared competing quotes from three other carriers.*
>
> *I paste this into the system — in production, this could come from an email, a phone call via speech-to-text, or a document upload. Watch what happens...*
>
> [Wait for response]
>
> *In seconds, the orchestrator has coordinated multiple agents: the intake agent structured the submission, the price collection agent analyzed the competitor quotes, the comparison agent built a side-by-side matrix, the variance agent calculated our market position, and the recommendation agent proposed an action — all within guardrail bands.*
>
> *And look at the end — there's an advisor talk-track. This is what the advisor reads to the customer on the phone. Plain language, no jargon, focused on value. This is the kind of intelligence that wins renewals."*

### Key Message

**Seconds, not hours. Complete competitive intelligence at the advisor's fingertips.**

### What to Highlight in the Response

- **Market position**: Where the carrier sits vs. competitors
- **Rate adequacy verdict**: GREEN / AMBER / RED
- **Recommendation**: HOLD / REDUCE / INCREASE with percentage
- **Advisor talk-track**: Customer-ready language
- **Compliance note**: "Pending human approval" — shows the HITL gate

### Fallback

If Foundry Playground doesn't respond:
- Open `data/sample_response.json` and walk through the pre-generated output
- Say: *"Here's what the system produces — let me walk you through each section"*

---

## Scenario 4: See the Pipeline

> **Duration**: 5-7 min | **Audience**: Technical / AI Engineers | **Difficulty**: Medium

### What This Proves

*"You can see exactly which agents fire, in what order, with full observability — every decision is traceable and auditable."*

### Setup

- Terminal open in the repo directory (local or Codespaces)
- `.env` configured with `FOUNDRY_PROJECT_ENDPOINT`
- Agents registered

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Open terminal in repo root | Command prompt ready |
| 2 | Run: `python src/main.py --demo` | Pipeline starts executing |
| 3 | Watch the step-by-step output | Each agent invocation logged with timing |
| 4 | Point out the concurrent fan-out step | Price collection hits N sources simultaneously |
| 5 | Point out the HITL gate | Pipeline pauses at compliance, shows approval prompt |
| 6 | Open Azure Monitor / App Insights | OpenTelemetry traces showing full pipeline span |

### Talk Track

> *"For the technical audience — let me show you what happens under the hood. I'm going to run the pipeline locally and you'll see every agent fire in sequence.*
>
> *Step 1: Submission Intake — the system parses the raw text into a structured record. You can see it identified the product type, revenue, limits, and flagged the loss history.*
>
> *Step 2: Price Collection — watch this — it fans out to multiple competitor sources concurrently. In production, these would be APIM-managed API calls with rate limiting and audit logging.*
>
> *Steps 3 through 6 are sequential: normalize the quotes, build the comparison matrix, calculate variance, assess risk appetite. Each agent gets the output from the previous step as context.*
>
> *Step 7: Recommendation — and here it proposes a rate action. Notice it stays within the guardrail band — the system won't propose an adjustment larger than ±10% without explicit configuration.*
>
> *Step 8: This is where it stops — the Compliance Guardrail agent. It says APPROVED, but it won't release the recommendation until a human team leader signs off. In production, this would surface as an approval card in Teams or Copilot Studio.*
>
> *And all of this is traced — every agent call, every token, every decision — in Azure Monitor via OpenTelemetry. Full audit trail for regulators."*

### Key Message

**Every step visible. Every decision traceable. Full regulatory audit trail.**

### Fallback

If `main.py` fails to connect:
- Walk through `src/workflows/quote_intelligence.py` — show the pipeline agent list
- Open `src/agents/orchestrator.py` — show the orchestration logic
- Show `docs/ARCHITECTURE.md` pipeline diagram

---

## Scenario 5: Customize with Copilot

> **Duration**: 5-7 min | **Audience**: Developers / Partners | **Difficulty**: Medium

### What This Proves

*"Your team can extend this system without starting from scratch. GitHub Copilot understands the architecture and can build new agents, add data sources, and adapt for your lines of business."*

### Setup

- GitHub repo open in browser
- Copilot Coding Agent enabled on the repo

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Open the repo's Issues tab | Issue templates visible |
| 2 | Click **"New Issue"** → Select **"Add a New Agent"** | Structured form appears |
| 3 | Fill in: Name: `fraud-detection-agent`, Category: `analysis`, Model: `gpt-4o` | Form guides the requirements |
| 4 | Add description: *"Analyze submission patterns to detect potential fraud indicators. Flag suspicious claims history, revenue inconsistencies, and known fraud rings."* | Clear acceptance criteria |
| 5 | Click **Submit** | Issue created |
| 6 | Assign the issue to `@copilot` | Copilot Coding Agent picks it up |
| 7 | (After ~2 min) Show the PR that Copilot creates | New agent file, agent.yaml update, tests |

### Talk Track

> *"Now here's where it gets exciting for your development team. Let's say your underwriting team says: 'We need a fraud detection agent in the pipeline.' Traditionally, that's weeks of development. Watch this.*
>
> *I open a new issue using the built-in template — 'Add a New Agent.' I fill in the name, category, model, and what the agent should do. Then I assign it to @copilot — GitHub Copilot Coding Agent.*
>
> *Copilot reads our repo instructions — it understands the Foundry SDK pattern, the Pydantic schemas, the agent registration process. In about 2 minutes, it creates a pull request with:*
> - *A new agent file following our exact SDK pattern*
> - *Updated agent.yaml with the registration*
> - *Unit tests for the new agent*
>
> *Your developer reviews the PR, merges it, and the CI/CD pipeline validates and deploys automatically. A new specialist agent, from idea to production, in minutes.*
>
> *This is the power of combining Azure AI Foundry with GitHub Copilot — the platform writes its own extensions."*

### Key Message

**From idea to working agent in minutes. Your AI platform extends itself.**

### Fallback

If Copilot is slow or unavailable:
- Show `.github/copilot-instructions.md` — explain how Copilot understands the repo
- Show `.github/ISSUE_TEMPLATE/add-agent.yml` — the structured template
- Show an existing agent file — explain the pattern Copilot would follow
- Say: *"Copilot would create a file exactly like this one, following the same SDK pattern"*

---

## Scenario 6: Open in Codespaces

> **Duration**: 2-3 min | **Audience**: Developers | **Difficulty**: Easy

### What This Proves

*"Zero setup. Click one button and you have a fully configured development environment with Python, Azure CLI, Bicep, Copilot — everything ready in 60 seconds."*

### Setup

- GitHub repo open in browser
- GitHub account with Codespaces access

### Step-by-Step

| Step | Action | What Audience Sees |
|------|--------|--------------------|
| 1 | Click the green **"Code"** button on GitHub | Dropdown with Codespaces tab |
| 2 | Click **"Create codespace on main"** | VS Code opens in browser |
| 3 | Wait ~60 seconds for post-create script | Terminal shows setup progress |
| 4 | Show the installed extensions | Python, Bicep, Copilot, Azure Tools |
| 5 | Open `README.md` (auto-opens) | Full documentation visible |
| 6 | Open terminal → run `python --version` and `az bicep version` | Everything pre-installed |

### Talk Track

> *"For developers — how long does it usually take to set up a Python AI project with Azure CLI, Bicep, and all the right extensions? An hour? Half a day?*
>
> *Watch this. I click 'Create Codespace' — one button. In 60 seconds, I have a fully configured VS Code environment in my browser. Python 3.12, Azure CLI with Bicep, azd, Ruff linter, GitHub Copilot — all pre-installed. The README opens automatically so I know exactly where to start.*
>
> *Your developers fork this repo, open a Codespace, and they're writing code in 60 seconds. No local setup, no dependency conflicts, no 'works on my machine' problems.*
>
> *And because GitHub Copilot is pre-configured with our repo's instructions, it already understands the agent architecture. It suggests code that follows our patterns from the first keystroke."*

### Key Message

**60 seconds from click to coding. Zero friction developer onboarding.**

### Fallback

If Codespaces is slow to start:
- Show `.devcontainer/devcontainer.json` — walk through the config
- Show `.devcontainer/post-create.sh` — explain what gets installed
- Say: *"This same config works with VS Code Dev Containers locally, Docker Desktop, or any devcontainer-compatible IDE"*

---

## Sample Data Reference

### Sample Submission (Scenario 3)

Save as `data/sample_request.json` — copy-paste ready for demos:

```json
{
  "modality": "text",
  "submission": {
    "insured_name": "Nexus Digital Solutions Ltd",
    "business_description": "Technology consulting and software development",
    "sic_code": "7371",
    "annual_revenue": 48000000,
    "currency": "USD",
    "employee_count": 475,
    "locations": ["Austin, TX", "Denver, CO"],
    "territory": "US",
    "product_type": "commercial_general_liability",
    "requested_limit": 2000000,
    "requested_deductible": 10000,
    "prior_carrier": "Atlantic Mutual",
    "years_with_prior": 3,
    "loss_history_summary": "1 claim in 3 years: $18,000 slip-and-fall, closed"
  },
  "carrier_quote": {
    "carrier": "Our Carrier",
    "annual_premium_gross": 42500,
    "per_occurrence_limit": 2000000,
    "aggregate_limit": 4000000,
    "deductible": 10000
  },
  "competitor_quotes": [
    {
      "carrier": "Pacific Shield Insurance",
      "annual_premium_gross": 38200,
      "per_occurrence_limit": 2000000,
      "aggregate_limit": 4000000,
      "deductible": 5000,
      "key_exclusions": ["cyber", "professional liability"],
      "endorsements_included": []
    },
    {
      "carrier": "Continental Risk Partners",
      "annual_premium_gross": 41800,
      "per_occurrence_limit": 2000000,
      "aggregate_limit": 4000000,
      "deductible": 10000,
      "key_exclusions": ["cyber"],
      "endorsements_included": ["additional insured blanket"]
    },
    {
      "carrier": "Summit Specialty Group",
      "annual_premium_gross": 44100,
      "per_occurrence_limit": 2000000,
      "aggregate_limit": 5000000,
      "deductible": 10000,
      "key_exclusions": [],
      "endorsements_included": ["cyber sublimit $500K", "additional insured blanket"]
    }
  ]
}
```

### Expected Pipeline Output Summary (Scenario 3 & 4)

```json
{
  "pipeline_result": {
    "market_position": {
      "carrier_premium": 42500,
      "market_median": 41800,
      "variance_percent": 1.67,
      "position_rank": 3,
      "total_competitors": 3,
      "adequacy_verdict": "GREEN"
    },
    "recommendation": {
      "action_type": "HOLD",
      "adjustment_percent": 0,
      "confidence": "High",
      "rationale": [
        "Current premium is within 1.7% of market median — competitive position is strong",
        "Loss history is favorable (1 minor claim in 3 years)",
        "Coverage terms are comparable to mid-market offerings",
        "Pacific Shield's lower price reflects reduced deductible ($5K vs $10K) — not a true apples-to-apples comparison",
        "Summit's higher price includes cyber sublimit — a value-add our policy doesn't offer"
      ],
      "conditions": [
        "Consider adding cyber sublimit endorsement to match Summit's offering",
        "Verify Pacific Shield's lower deductible impact on net premium comparison"
      ],
      "guardrail_band_used": 10
    },
    "compliance": {
      "status": "APPROVED",
      "requires_human_approval": true,
      "antitrust_check": true,
      "rate_filing_check": true,
      "regulatory_check": true
    },
    "advisor_talk_track": "Your current premium of $42,500 is very competitive — it's broadly in line with the market. One alternative provider is offering a slightly lower price, but that comes with a lower deductible which changes the risk profile. Another provider is slightly higher but includes additional cyber coverage. My recommendation is to hold the current rate and discuss adding a cyber endorsement, which would give you the strongest overall package at a fair price. Shall I walk through the coverage differences in more detail?"
  }
}
```

---

## Demo Preparation Checklist

### For Any Demo

```
□ Azure subscription with sufficient quota (Core AI stage)
□ GitHub account with repo access
□ Foundry project endpoint noted
□ Agents registered (python src/register_agents.py)
□ Test query successful in Foundry Playground
□ Sample data files open and ready
□ Fallback recording ready (3-min screen capture)
□ Browser tabs pre-opened:
  - GitHub repo (README visible)
  - Azure portal (resource group visible)
  - Foundry portal (agents listed)
  - Foundry Playground (orchestrator selected)
```

### For Developer Demos (Add These)

```
□ Codespaces tested (creates in <60s)
□ Terminal with .env configured
□ python src/main.py --demo tested successfully
□ GitHub Copilot Coding Agent enabled on repo
□ Sample issue template tested
```

---

## Objection Handling & FAQ

### "How much does this cost to run?"

> *"Stage 1 (Core AI) runs approximately $X-Y/day during development. The primary cost drivers are Azure OpenAI tokens (pay-per-use) and Azure AI Search (basic tier, ~$75/month). In production, costs scale with usage — a contact center processing 500 quotes/day would see approximately $Z/month. All resources can be paused or scaled down when not in use."*

### "Can this work with our existing policy admin system?"

> *"Absolutely. The `src/tools/` directory is where you connect to external systems. We've designed tool modules for Guidewire, Duck Creek, and other common platforms. You add a tool, register it in agent.yaml, and the agents can use it. The APIM integration layer manages all external API calls with rate limiting and audit logging."*

### "Is the competitor data real?"

> *"The sample data is synthetic — designed to demonstrate the system's analytical capabilities. In production, competitor data comes from broker-shared market intelligence, industry benchmarking services, and public filing data — all routed through Azure API Management for compliance and audit."*

### "What about data privacy and compliance?"

> *"Three layers of protection: First, all data stays in your Azure tenant — nothing leaves your environment. Second, the Compliance Guardrail Agent enforces antitrust rules, rate filing compliance, and PII protection on every pipeline run. Third, every decision is traced via OpenTelemetry to Azure Monitor, creating a complete audit trail for regulators. And the HITL gate means no automated rate change ever reaches a customer without human approval."*

### "How long to customize for our lines of business?"

> *"The template is built for Commercial P&C, but adapting it is straightforward. For a new product line, you update the ProductType enum, adjust the agent system prompts, and add your underwriting data to AI Search. With GitHub Copilot Coding Agent, the mechanics take hours, not weeks. The real time investment is in defining your business rules and loading your data."*

### "Why Microsoft vs. building on AWS or Google?"

> *"Three reasons: First, Azure AI Foundry provides managed agent hosting with built-in governance, evaluation, and red-teaming — you don't build that yourself. Second, the Foundry SDK gives you one project endpoint for all AI services — models, tools, search, speech, document intelligence — instead of stitching together 10 different SDKs. Third, the GitHub integration means your developers get Copilot-assisted development, Codespaces for onboarding, and automated CI/CD — all in one Microsoft ecosystem. It's end-to-end, not best-of-breed."*

### "What if the Foundry SDK changes?"

> *"The SDK is GA (azure-ai-projects 2.x). The agent pattern — create agent, create conversation, send responses — is stable. The template pins to a minimum version (>=2.3.0) and our CI pipeline validates on every PR. If the SDK evolves, the template evolves with it."*

---

## Appendix: Azure Service Cost Estimates

### Stage 1: Core AI (Demo / Development)

| Service | SKU | Estimated Monthly Cost |
|---------|-----|----------------------|
| Azure AI Foundry | Free tier (included with project) | $0 |
| Azure OpenAI (GPT-4o) | Pay-per-token | ~$30-100 (demo usage) |
| Azure OpenAI (GPT-4o-mini) | Pay-per-token | ~$5-20 (demo usage) |
| Azure AI Search | Basic | ~$75 |
| Azure AI Speech | Free tier (5hrs/month) | $0 |
| Azure AI Document Intelligence | Free tier (500 pages/month) | $0 |
| Azure Key Vault | Standard | ~$1 |
| Azure Monitor + App Insights | Pay-per-GB | ~$5-10 |
| Azure Storage | LRS, minimal | ~$1 |
| **Stage 1 Total** | | **~$120-210/month** |

### Stage 2: Data Layer (Add When Needed)

| Service | SKU | Estimated Monthly Cost |
|---------|-----|----------------------|
| Azure SQL Database | Basic (5 DTU) | ~$5 |
| Azure Cosmos DB | Serverless | ~$1-10 (usage-based) |
| Microsoft Fabric | F2 (paused when not in use) | ~$0-50 |
| **Stage 2 Total** | | **~$6-65/month** |

### Stage 3: Integration & Governance (Add for Production)

| Service | SKU | Estimated Monthly Cost |
|---------|-----|----------------------|
| Azure API Management | Standard v2 | ~$175 |
| Azure Communication Services | Pay-per-use | ~$1-20 |
| Microsoft Purview | Free tier (1GB) | $0 |
| Azure Event Grid | Pay-per-event | ~$1 |
| **Stage 3 Total** | | **~$177-196/month** |

> **Demo budget**: Stage 1 only = ~$120-210/month. Scale up stages as needed.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ INSURANCE QUOTE INTELLIGENCE ACCELERATOR — DEMO CHEAT SHEET│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ DEPLOY:    Click "Deploy to Azure" → Stage 1 → 15 min      │
│ REGISTER:  python src/register_agents.py                    │
│ TEST:      Foundry Playground → paste sample submission     │
│ RUN:       python src/main.py --demo                        │
│ CUSTOMIZE: Create issue → assign @copilot → review PR      │
│ DEVELOP:   "Create Codespace" → ready in 60s               │
│                                                             │
│ AGENTS:    14 specialist agents                             │
│ SERVICES:  24 Azure services                                │
│ PATTERNS:  Sequential, Concurrent, Handoff, Magentic, HITL  │
│ SDK:       azure-ai-projects >= 2.3.0 (Foundry SDK)        │
│ COST:      ~$120-210/month (Stage 1 only)                   │
│                                                             │
│ REPO:      github.com/ponarunkumar/insurance-competitive-   │
│            quote-intelligence-accelerator                   │
│                                                             │
│ HELP:      docs/GETTING_STARTED.md                          │
│ ARCH:      docs/ARCHITECTURE.md                             │
│ AGENTS:    docs/AGENTS.md                                   │
└─────────────────────────────────────────────────────────────┘
```
