# Foundry Tools Quick Start — Self-Service Enablement Kit

> **Audience:** AI Engineers, Solution Architects, ISV Partners
> **Time:** ~45 minutes total
> **Prerequisite:** Complete [Getting Started](GETTING_STARTED.md) — infrastructure deployed + agents registered

This guide walks you through wiring three Microsoft Foundry built-in tools into your
Quote Intelligence agents. Each tool adds a concrete capability that transforms
agents from prompt-only to data-grounded, production-ready AI.

| Tool | Agent | What It Adds | Setup Time |
|------|-------|-------------|-----------|
| [CodeInterpreterTool](#tool-1-codeinterpretertool) | Pricing Variance | Deterministic Python math (no LLM arithmetic) | 5 min |
| [BingGroundingTool](#tool-2-binggroundingtool) | Price Collection | Real-time web search for market data | 15 min |
| [FileSearchTool](#tool-3-filesearchtool) | Risk Assessment | RAG over underwriting manuals & appetite guides | 20 min |

---

## Prerequisites Checklist

Before starting, confirm you have:

- [ ] Azure AI Foundry project deployed and accessible at [ai.azure.com](https://ai.azure.com)
- [ ] 14 agents registered (`python src/register_agents.py` completed successfully)
- [ ] `.env` file configured with `FOUNDRY_PROJECT_ENDPOINT`
- [ ] Azure CLI authenticated (`az login`)
- [ ] Python 3.12+ with project dependencies installed (`pip install -e ".[dev]"`)
- [ ] Contributor or Owner role on the Azure resource group

---

## Tool 1: CodeInterpreterTool

**Agent:** `pricing-variance-agent`
**Purpose:** Execute Python code for deterministic financial calculations
**Setup:** Zero portal configuration required — this is the fastest win

### Why It Matters

Without CodeInterpreter, the Pricing Variance agent relies on the LLM to do arithmetic.
LLMs frequently hallucinate numbers. With CodeInterpreter, the agent writes and executes
real Python code to calculate:

- Market median premium
- Carrier vs. median variance (%)
- Position rank
- Rate adequacy verdict (GREEN / AMBER / RED)

### Step 1: Update the Agent Code

Edit `src/agents/analysis/pricing_variance.py` and add the tool import:

```python
from azure.ai.projects.tools import CodeInterpreterTool
```

Update the `create_pricing_variance_agent` function:

```python
def create_pricing_variance_agent(project_client: AIProjectClient) -> Any:
    """Register with CodeInterpreter for deterministic math."""
    code_tool = CodeInterpreterTool()

    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=[code_tool],
        ),
    )
```

### Step 2: Update register_agents.py

In `src/register_agents.py`, update the pricing-variance-agent entry to include tools:

```python
from azure.ai.projects.tools import CodeInterpreterTool

# In the registration loop, for pricing-variance-agent:
tools = [CodeInterpreterTool()] if agent_def["name"] == "pricing-variance-agent" else []

agent = project_client.agents.create_version(
    agent_name=agent_def["name"],
    definition=PromptAgentDefinition(
        model=agent_def["model"],
        instructions=agent_def["instructions"],
        tools=tools,
    ),
)
```

### Step 3: Re-register and Verify

```bash
# Re-register the agent with the new tool
python src/register_agents.py
```

### Step 4: Test in Foundry Playground

1. Open [ai.azure.com](https://ai.azure.com) → Your Project → Agents
2. Click **pricing-variance-agent** → Open in Playground
3. Paste this test prompt:

```
Calculate the pricing variance for these competitor quotes:
- Carrier Alpha: $45,000 annual premium
- Carrier Beta: $52,000 annual premium
- Carrier Gamma: $48,500 annual premium
- Our rate: $50,000 annual premium

Compute: market median, our variance %, position rank, and adequacy verdict
(GREEN = ±5%, AMBER = 5-15%, RED = >15%)
```

4. **Expected:** The agent writes Python code, executes it, and returns exact numbers
5. **Look for:** The "Code Interpreter" indicator in the response showing executed code

### ✅ Success Criteria

- [ ] Agent response includes executed Python code block
- [ ] Calculated variance is mathematically correct (not approximate)
- [ ] Verdict (GREEN/AMBER/RED) matches the actual percentage

---

## Tool 2: BingGroundingTool

**Agent:** `competitor-price-collection-agent`
**Purpose:** Search the web for real-time competitor market intelligence
**Setup:** Requires creating a Bing Search resource in Azure Portal

### Why It Matters

The Price Collection agent currently receives competitor data only from the input payload.
With Bing Grounding, it can search the web for publicly available market intelligence:
rate filings, industry reports, broker surveys, and news about competitor pricing trends.

### Step 1: Create Bing Search Resource (Azure Portal)

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **"Grounding with Bing Search"**
4. Click **Create**
5. Fill in:
   - **Resource group:** Same as your Foundry project (e.g., `rg-ins-qi-dev`)
   - **Name:** `bing-grounding-ins-qi` (or your preferred name)
   - **Pricing tier:** Select based on your needs (S1 for demo)
6. Click **Review + Create** → **Create**
7. Wait for deployment to complete

### Step 2: Connect to Foundry Project

1. Go to [ai.azure.com](https://ai.azure.com) → Your Project
2. Click **Management Center** (gear icon in sidebar)
3. Click **Connected Resources** → **+ New Connection**
4. Select **Grounding with Bing Search**
5. Choose the Bing resource you just created
6. Click **Add Connection**
7. **Copy the Connection ID** that appears (format: a GUID or path string)

### Step 3: Add to Environment

Add the connection ID to your `.env` file:

```bash
# Bing Grounding (for Price Collection agent)
BING_CONNECTION_ID=<paste-your-connection-id-here>
```

### Step 4: Update the Agent Code

Edit `src/agents/market_intelligence/price_collection.py`:

```python
import os
from azure.ai.projects.tools import BingGroundingTool

# In create_price_collection_agent():
def create_price_collection_agent(project_client: AIProjectClient) -> Any:
    """Register with Bing Grounding for real-time market search."""
    tools = []
    bing_connection = os.environ.get("BING_CONNECTION_ID")
    if bing_connection:
        tools.append(BingGroundingTool(connection_id=bing_connection))

    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=tools,
        ),
    )
```

### Step 5: Re-register and Verify

```bash
python src/register_agents.py
```

### Step 6: Test in Foundry Playground

1. Open [ai.azure.com](https://ai.azure.com) → Your Project → Agents
2. Click **competitor-price-collection-agent** → Open in Playground
3. Paste this test prompt:

```
Search for current commercial general liability (CGL) insurance market
pricing trends in the United States for technology companies with
$5M-$10M revenue. Find recent rate filing data, broker survey results,
or industry reports about competitive pricing.
```

4. **Expected:** Agent searches the web and returns results with source citations
5. **Look for:** Inline citations with URLs to actual web sources

### ✅ Success Criteria

- [ ] Agent response includes web citations (URLs)
- [ ] Results reference real, current market data sources
- [ ] "Bing Search" indicator appears in the response

---

## Tool 3: FileSearchTool

**Agent:** `risk-assessment-agent`
**Purpose:** Ground risk assessments in uploaded underwriting manuals and appetite guides
**Setup:** Requires creating a vector store and uploading documents

### Why It Matters

The Risk Assessment agent uses the Magentic (capped iteration) pattern to search for
evidence before making an assessment. Without FileSearch, it relies solely on the LLM's
training data. With FileSearch, it grounds assessments in your actual carrier documents:

- Underwriting manuals (coverage rules, exclusions, pricing guidelines)
- Appetite guides (target markets, acceptable risk profiles, referral triggers)
- Rate filing documentation

### Step 1: Prepare Sample Documents

For the demo, create 2-3 sample PDF documents. You can use these templates:

**Document 1: `CGL_Appetite_Guide.pdf`**
```
COMMERCIAL GENERAL LIABILITY — APPETITE GUIDE

Target Market:
- Technology companies, $1M-$50M revenue
- Professional services, $500K-$25M revenue
- Light manufacturing, $2M-$20M revenue

Acceptable Risk Profile:
- Loss ratio < 60% over 3 years
- No more than 2 claims in prior 5 years
- Clean OSHA record

Referral Triggers:
- Revenue > $50M → Senior Underwriter review
- New venture (< 2 years in business)
- Prior coverage cancellation or non-renewal
```

**Document 2: `Underwriting_Manual_CGL.pdf`**
```
CGL UNDERWRITING MANUAL — RATE GUIDELINES

Base Rate Calculation:
- Revenue band: per-$1000 of revenue
- Industry hazard grade: 1 (low) to 10 (high)
- Territory factor: 0.8 (rural) to 1.5 (urban/high-litigation)

Pricing Adjustments:
- Preferred risk (loss ratio < 40%): -10% to -15%
- Standard risk (loss ratio 40-60%): base rate
- Substandard risk (loss ratio > 60%): +15% to +25%

Maximum Guardrail Band: ±10% from calculated rate
```

Save these as PDF files in your `data/` directory or locally.

### Step 2: Create Vector Store (Foundry Portal)

1. Go to [ai.azure.com](https://ai.azure.com) → Your Project
2. Navigate to **Agents** → **risk-assessment-agent**
3. Click **Tools** → **+ Add Tool** → **File Search**
4. Click **Create new vector store**
5. Name it: `underwriting-knowledge-base`
6. Click **Create**

### Step 3: Upload Documents

1. With the vector store selected, click **Upload documents**
2. Drag and drop your PDF files (appetite guide + underwriting manual)
3. Wait for ingestion to complete (status shows "Ready")
4. **Copy the Vector Store ID** (visible in the vector store panel)

### Step 4: Add to Environment

```bash
# File Search (for Risk Assessment agent)
FILE_SEARCH_VECTOR_STORE_ID=<paste-your-vector-store-id-here>
```

### Step 5: Update the Agent Code

Edit `src/agents/analysis/risk_assessment.py`:

```python
import os
from azure.ai.projects.tools import FileSearchTool

# In create_risk_assessment_agent():
def create_risk_assessment_agent(project_client: AIProjectClient) -> Any:
    """Register with FileSearch for document-grounded assessment."""
    tools = []
    vector_store_id = os.environ.get("FILE_SEARCH_VECTOR_STORE_ID")
    if vector_store_id:
        tools.append(FileSearchTool(vector_store_ids=[vector_store_id]))

    return project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=tools,
        ),
    )
```

### Step 6: Re-register and Verify

```bash
python src/register_agents.py
```

### Step 7: Test in Foundry Playground

1. Open [ai.azure.com](https://ai.azure.com) → Your Project → Agents
2. Click **risk-assessment-agent** → Open in Playground
3. Paste this test prompt:

```
Assess this risk for appetite match and exposure:

Company: Nexus Digital Solutions
Industry: Technology / SaaS
Revenue: $8.2M
Employees: 47
Location: Austin, TX
Product: Commercial General Liability
Prior Claims: 1 claim in 5 years ($12,000 settled)
Loss Ratio: 35% (3-year average)
Years in Business: 6

Check the appetite guide and underwriting manual for this risk.
```

4. **Expected:** Agent searches uploaded documents and grounds its assessment
5. **Look for:** References to specific sections from your uploaded manuals

### ✅ Success Criteria

- [ ] Agent response references content from uploaded documents
- [ ] Appetite match decision cites specific criteria from the appetite guide
- [ ] Pricing recommendation references the underwriting manual rate guidelines
- [ ] File Search indicator shows which documents were searched

---

## Update .env.sample

After completing the tool setup, update `.env.sample` to include the new variables:

```bash
# ── Foundry Built-in Tools ──────────────────────────────────────────────────
# CodeInterpreterTool: No configuration needed (built-in)

# BingGroundingTool (for competitor-price-collection-agent):
# Get from: ai.azure.com → Project → Management Center → Connected Resources
BING_CONNECTION_ID=

# FileSearchTool (for risk-assessment-agent):
# Get from: ai.azure.com → Project → Agents → risk-assessment-agent → File Search → Vector Store
FILE_SEARCH_VECTOR_STORE_ID=
```

---

## Verify All Three Tools

Run this quick validation after all tools are configured:

```bash
# 1. Re-register all agents with tools
python src/register_agents.py

# 2. Run the demo pipeline
python src/main.py --demo

# 3. Check the output for tool usage indicators:
#    - Pricing Variance step: should show code execution
#    - Price Collection step: should show web citations
#    - Risk Assessment step: should show document references
```

### Full Verification in Foundry Portal

1. Go to [ai.azure.com](https://ai.azure.com) → Your Project → **Agents**
2. For each agent, verify the tool is listed in its configuration:

| Agent | Tool | Indicator |
|-------|------|-----------|
| pricing-variance-agent | Code Interpreter | ✅ Python icon |
| competitor-price-collection-agent | Bing Search | ✅ Web icon |
| risk-assessment-agent | File Search | ✅ Document icon |

---

## Troubleshooting

### "Connection not found" error for Bing Grounding
- **Cause:** `BING_CONNECTION_ID` doesn't match any connection in your project
- **Fix:** Go to ai.azure.com → Management Center → Connected Resources → verify the connection exists and copy the exact ID

### "Vector store not found" error for File Search
- **Cause:** `FILE_SEARCH_VECTOR_STORE_ID` is incorrect or the vector store was created in a different project
- **Fix:** Verify the vector store exists in the same project where your agents are registered

### "Permission denied" when creating Bing resource
- **Cause:** Your Azure subscription may not have the Bing Search provider registered
- **Fix:** Run `az provider register --namespace Microsoft.Bing` and wait for registration

### CodeInterpreter not executing code
- **Cause:** The agent may answer from knowledge instead of writing code
- **Fix:** Add explicit instructions: "Use the Code Interpreter tool to compute all numerical calculations. Do not estimate."

### File Search returns no results
- **Cause:** Document ingestion may still be processing
- **Fix:** Check vector store status in the Foundry portal — wait for "Ready" status on all files

### Tools not appearing after re-registration
- **Cause:** Agent version caching
- **Fix:** Delete the existing agent version in the portal, then re-run `python src/register_agents.py`

---

## What's Next

Now that your agents have real tools, continue with:

1. **[Demo Scenarios](DEMO_SCENARIOS.md)** — Run the full 6-scenario demo with live tools
2. **Custom Documents** — Upload your organization's actual underwriting manuals for a realistic demo
3. **Production Readiness** — Add authentication, RBAC, and monitoring for production deployment

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│              FOUNDRY TOOLS — QUICK REFERENCE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CodeInterpreterTool()                                           │
│    → No setup needed                                             │
│    → Agent writes & runs Python for deterministic math           │
│                                                                  │
│  BingGroundingTool(connection_id="...")                           │
│    → Portal: Create Bing resource → Connect to project           │
│    → Agent searches web with inline citations                    │
│                                                                  │
│  FileSearchTool(vector_store_ids=["..."])                        │
│    → Portal: Create vector store → Upload documents              │
│    → Agent grounds responses in your documents (RAG)             │
│                                                                  │
│  All tools: pass via PromptAgentDefinition(tools=[...])          │
│  SDK: from azure.ai.projects.tools import <ToolClass>            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Last updated: August 2026 | SDK: azure-ai-projects >= 2.3.0 | Agent Framework >= 0.3.0*
