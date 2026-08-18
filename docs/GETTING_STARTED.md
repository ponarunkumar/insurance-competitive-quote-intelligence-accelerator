# Getting Started Guide

> **Insurance Competitive Quote Intelligence Accelerator**  
> Step-by-step deployment guide for all audiences

---

## Table of Contents

- [Choose Your Deployment Path](#choose-your-deployment-path)
- [Option 1: Deploy to Azure (Portal — One Click)](#option-1-deploy-to-azure-portal--one-click)
- [Option 2: Azure Developer CLI (Command Line)](#option-2-azure-developer-cli-command-line)
- [Post-Deployment: Register Agents](#post-deployment-register-agents)
- [Post-Deployment Setup](#post-deployment-setup)
- [Verify Your Deployment](#verify-your-deployment)
- [Next Steps by Role](#next-steps-by-role)
- [Demo Scenarios](#demo-scenarios)
- [Troubleshooting](#troubleshooting)
- [Cost Management](#cost-management)

---

## Choose Your Deployment Path

| Approach | Best For | Time | Prerequisites |
|----------|----------|------|---------------|
| **Option 1: Deploy to Azure Button** | Azure Admins, quick demos, POC setup | 20–30 min | Azure subscription + browser |
| **Option 2: Azure Developer CLI (`azd up`)** | Developers, CI/CD, repeatable deployments | 15–25 min | Azure CLI + azd + Python 3.12 |

---

## Option 1: Deploy to Azure (Portal — One Click)

### Step 1: Click the Deploy Button

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fponarunkumar%2Finsurance-competitive-quote-intelligence-accelerator%2Fmain%2Finfra%2Fmain.json)

This opens the Azure Portal **Custom Deployment** page with the template pre-loaded.

---

### Step 2: Fill in the Basics Tab

You'll see a form with the following fields:

| Field | What to Enter | Example | Notes |
|-------|--------------|---------|-------|
| **Subscription** | Your Azure subscription | `Contoso-Production` | Must have Owner or Contributor + User Access Admin role |
| **Region** | Deployment region | `Sweden Central` | See [supported regions](#supported-regions) below |
| **Environment Name** | Short identifier used in all resource names | `dev` | Lowercase, no spaces. Creates resources like `rg-ins-qi-dev` |
| **SQL Admin Login** | Azure SQL admin username | `sqladmin` | Cannot be `admin`, `sa`, or other reserved words |
| **SQL Admin Password** | Strong password | `••••••••••••` | Min 12 chars: uppercase + lowercase + number + symbol |
| **APIM Publisher Email** | Email for API Management portal | `admin@yourcompany.com` | Must be a valid email address |
| **APIM Publisher Name** | Organization name | `Acme Insurance` | Appears on the developer portal |
| **Fabric Admin Members** | Entra Object IDs (JSON array) | `[]` | Optional — add later if needed |

---

### Step 3: Review + Create

1. Click **"Review + create"** at the bottom
2. Azure validates the template (1–2 minutes):
   - ✅ Region availability for all 24 services
   - ✅ Resource naming rules (no conflicts)
   - ✅ Quota sufficiency (OpenAI TPM, Search units, etc.)
   - ✅ Your RBAC permissions
3. If you see **"Validation passed"** ✅ → click **"Create"**
4. If validation fails → see [Troubleshooting](#troubleshooting)

---

### Step 4: Wait for Deployment (15–25 minutes)

The deployment progress page shows each resource being created:

```
Phase 1 (~2 min):   Resource Group, Key Vault, Log Analytics, App Insights
Phase 2 (~5 min):   Azure SQL, Cosmos DB, Speech Service, Communication Services
Phase 3 (~5 min):   AI Foundry Hub, OpenAI, AI Search, Doc Intelligence,
                    Content Understanding, AI Language, Fabric
Phase 4 (~3 min):   AI Foundry Project, GPT-4o + GPT-4o-mini deployments
Phase 5 (~3 min):   Container App + Registry, Speech configurations
Phase 6 (~15 min):  API Management (Standard v2) ← SLOWEST RESOURCE
Phase 7 (~2 min):   Managed Identities, RBAC, Purview, Defender
```

> ⚠️ **Do not cancel the deployment.** APIM Standard v2 takes 15–20 minutes — this is normal.

---

### Step 5: Deployment Complete ✅

When you see **"Your deployment is complete"**:

1. Click **"Outputs"** in the left sidebar to view and copy key endpoints:

| Output | Value | Used For |
|--------|-------|----------|
| `resourceGroupName` | `rg-ins-qi-dev` | All subsequent Azure management |
| `openAIEndpoint` | `https://oai-ins-qi-dev.openai.azure.com/` | Agent LLM configuration |
| `aiSearchEndpoint` | `https://srch-ins-qi-dev.search.windows.net` | RAG index creation |
| `speechEndpoint` | `https://speech-ins-qi-dev.cognitiveservices.azure.com/` | Speech SDK setup |
| `sqlServerFqdn` | `sql-ins-qi-dev.database.windows.net` | Database connection |
| `cosmosEndpoint` | `https://cosmos-ins-qi-dev.documents.azure.com:443/` | Agent state store |
| `apimGatewayUrl` | `https://apim-ins-qi-dev.azure-api.net` | Competitor API gateway |
| `appInsightsConnectionString` | `InstrumentationKey=...` | Telemetry & tracing |

2. Click **"Go to resource group"** to see all deployed resources

> 💡 **Tip:** Save these output values — you'll need them for the `.env` file when running agents locally.

---

### Supported Regions

| Region | All 24 Services | Recommendation |
|--------|-----------------|----------------|
| **Sweden Central** | ✅ Full support | Best for UK/EU data residency |
| **East US 2** | ✅ Full support | Best for US workloads |
| **West US 3** | ✅ Full support | Alternative US region |
| **Australia East** | ⚠️ Check Fabric | APAC workloads |
| **UK South** | ⚠️ Check OpenAI models | May need Sweden Central for GPT-4o |
| **West Europe** | ⚠️ Check Voice Live | Check GA status per service |

> **Check availability:** Run `az cognitiveservices model list --location <region> --query "[?model.name=='gpt-4o']"` to verify GPT-4o availability in your target region.

---

## Option 2: Azure Developer CLI (Command Line)

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Azure CLI | 2.60+ | [Install](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| Azure Developer CLI (azd) | 1.10+ | [Install](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) |
| Python | 3.12+ | [Install](https://python.org/downloads) |
| Docker | 24+ | [Install](https://docs.docker.com/get-docker/) (for container deployment) |
| Git | 2.40+ | [Install](https://git-scm.com/) |

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/ponarunkumar/insurance-competitive-quote-intelligence-accelerator.git
cd insurance-competitive-quote-intelligence-accelerator

# Copy the environment template
cp .env.sample .env

# Edit .env with your values
# At minimum, set:
#   AZURE_LOCATION=swedencentral
#   SQL_ADMIN_LOGIN=sqladmin
#   SQL_ADMIN_PASSWORD=YourStr0ngP@ssw0rd!
#   APIM_PUBLISHER_EMAIL=admin@yourcompany.com
```

### Step 2: Authenticate

```bash
# Login to Azure
az login

# Login to Azure Developer CLI
azd auth login

# Verify your subscription
az account show --query "{name: name, id: id}" -o table
```

### Step 3: Initialize and Deploy

```bash
# Initialize azd environment (creates .azure/ folder)
azd init --environment dev

# Provision all 24 Azure services + deploy the agent
azd up
```

You'll be prompted for:
- Azure subscription (select from list)
- Azure location (type: `swedencentral`)
- Parameter values (SQL password, email, etc.)

### Step 4: Monitor Deployment

```bash
# Watch deployment progress
azd provision --output json

# Or check in Azure Portal:
# Portal → Resource Groups → rg-ins-qi-dev → Deployments
```

### Step 5: Verify Endpoints

```bash
# Get all deployment outputs
azd env get-values

# Test agent health endpoint
curl -s $(azd env get-value AGENT_ENDPOINT)/health

# View recent traces
az monitor app-insights query \
  --app $(azd env get-value APP_INSIGHTS_NAME) \
  --analytics-query "traces | take 5"
```

---

## Post-Deployment: Register Agents

After Azure resources are deployed, register all 14 agents in your Foundry project:

### Step 1: Set Your Foundry Endpoint

Find your project endpoint in the Azure portal under your AI Foundry resource, or in the deployment outputs.

```bash
# Add to your .env file
FOUNDRY_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

### Step 2: Run the Registration Script

```bash
# Install dependencies (if not already done)
pip install "azure-ai-projects>=2.3.0" azure-identity python-dotenv

# Authenticate with Azure
az login

# Register all 14 agents
python src/register_agents.py
```

You should see:

```
Connecting to Foundry project: https://...
Registering 14 agents...
============================================================
  [ 1/14] ✅ quote-intelligence-orchestrator (model: gpt-4o)
  [ 2/14] ✅ submission-intake-agent (model: gpt-4o-mini)
  [ 3/14] ✅ voice-intake-agent (model: gpt-4o-mini)
  ...
  [14/14] ✅ advisor-coaching-agent (model: gpt-4o)
============================================================
Agent registration complete.
```

### Step 3: Verify in Foundry Portal

1. Open [ai.azure.com](https://ai.azure.com)
2. Navigate to your Project → **Build** → **Agents**
3. Confirm all 14 agents are listed
4. Click on `quote-intelligence-orchestrator` → **Open in Playground**
5. Paste the sample submission from `data/sample_request.json` and verify a response

---

## Post-Deployment Setup

After either deployment option completes, these steps finish the configuration:

### For Azure Admins

| # | Task | Time | Instructions |
|---|------|------|-------------|
| 1 | **Verify resource health** | 2 min | Portal → Resource Group → check all resources show "Running" / "Active" |
| 2 | **Resume Fabric capacity** (if paused) | 1 min | Portal → Fabric Capacities → Resume |
| 3 | **Review Defender recommendations** | 5 min | Portal → Defender for Cloud → Recommendations |
| 4 | **Configure network rules** (production) | 15 min | Add VNet integration, private endpoints as needed |

### For Developers

| # | Task | Time | Instructions |
|---|------|------|-------------|
| 1 | **Seed Azure SQL** | 5 min | Connect to SQL Server with admin creds → execute `data/seed_sql.sql` |
| 2 | **Create AI Search indexes** | 15 min | Portal → AI Search → Import Data → create indexes: `underwriting-manuals`, `appetite-guides` |
| 3 | **Build & push agent container** | 10 min | See [Deploy Agent Container](#deploy-agent-container) below |
| 4 | **Configure APIM backends** | 10 min | Portal → APIM → APIs → add competitor endpoint URLs |
| 5 | **Test with sample data** | 5 min | POST `data/sample_submission.json` to agent endpoint |

### For AI Engineers

| # | Task | Time | Instructions |
|---|------|------|-------------|
| 1 | **Upload Custom Speech phrase list** | 10 min | Portal → Speech → Custom Speech → upload insurance terminology |
| 2 | **Create AI Search semantic config** | 10 min | Add semantic configuration to each index for improved RAG |
| 3 | **Configure agent prompts** | 15 min | Edit `src/prompts/*.md` for your specific product lines |
| 4 | **Set up evaluation** | 20 min | Configure Agent Framework evaluation in `tests/e2e/` |
| 5 | **Connect Copilot Studio** | 15 min | Copilot Studio → New Agent → A2A connection to Container App |

---

### Deploy Agent Container

```bash
# Get Container Registry login server from deployment outputs
ACR_SERVER=$(azd env get-value CONTAINER_REGISTRY_LOGIN_SERVER)

# Login to Container Registry
az acr login --name $(echo $ACR_SERVER | cut -d. -f1)

# Build the agent image
docker build -t $ACR_SERVER/quote-intelligence-agent:latest .

# Push to Azure Container Registry
docker push $ACR_SERVER/quote-intelligence-agent:latest

# Update the Container App to use the new image
az containerapp update \
  --name ins-qi-dev-agent \
  --resource-group rg-ins-qi-dev \
  --image $ACR_SERVER/quote-intelligence-agent:latest
```

---

## Verify Your Deployment

### Quick Health Check

```bash
# 1. Check all resources deployed
az resource list --resource-group rg-ins-qi-dev --output table | wc -l
# Expected: 20+ resources

# 2. Test OpenAI connectivity
az cognitiveservices account show \
  --name oai-ins-qi-dev \
  --resource-group rg-ins-qi-dev \
  --query "properties.provisioningState" -o tsv
# Expected: Succeeded

# 3. Test AI Search
curl -s "https://srch-ins-qi-dev.search.windows.net/indexes?api-version=2024-07-01" \
  -H "api-key: $(az search admin-key show --service-name srch-ins-qi-dev -g rg-ins-qi-dev --query primaryKey -o tsv)"
# Expected: JSON response with indexes array

# 4. Test SQL connectivity
az sql db show --server sql-ins-qi-dev --name InsuranceQuoteIntelligence \
  --resource-group rg-ins-qi-dev --query "status" -o tsv
# Expected: Online
```

### Run the Demo

```bash
# Submit a sample quote request to the agent
curl -X POST "$(azd env get-value AGENT_ENDPOINT)/api/quote-intelligence" \
  -H "Content-Type: application/json" \
  -d @data/sample_submission.json

# Expected: JSON response with comparison matrix, pricing variance, and recommendation
```

---

## Next Steps by Role

### Azure Admin
- [ ] Set up Azure Budget alerts ($500, $1000 thresholds)
- [ ] Configure diagnostic settings to forward logs to SIEM
- [ ] Review and apply Azure Policy for compliance
- [ ] Set up backup for Azure SQL (auto-enabled, verify retention)

### Developer
- [ ] Implement real competitor API integrations (replace stubs in `src/tools/market/`)
- [ ] Connect real document sources to Document Intelligence pipeline
- [ ] Write unit tests for each agent (`tests/unit/`)
- [ ] Set up CI/CD pipeline with GitHub Actions

### AI Engineer
- [ ] Fine-tune system prompts based on real quote data
- [ ] Train Custom Speech model with insurance call recordings
- [ ] Build evaluation dataset for agent quality scoring
- [ ] Configure guardrail band percentages per product line
- [ ] Set up A/B testing for model selection (GPT-4o vs fine-tuned)

### Contact Center Leader
- [ ] Identify 2–4 advisors for pilot group
- [ ] Define success metrics (conversion rate, handle time, quality score)
- [ ] Schedule 90-day proof-of-value review
- [ ] Prepare coaching report format for team leaders

---

## Demo Scenarios

For detailed, step-by-step demo guides with talk tracks, sample data, and fallback plans, see **[DEMO_SCENARIOS.md](DEMO_SCENARIOS.md)**.

### Available Scenarios

| # | Scenario | Duration | Best For |
|---|----------|----------|----------|
| 1 | **Fork & Deploy** | 3-5 min | Any audience — one-click deployment |
| 2 | **Meet the Agents** | 3-5 min | Technical — 14-agent architecture tour |
| 3 | **Ask for a Quote** | 3-5 min | Any audience — live business value demo |
| 4 | **See the Pipeline** | 5-7 min | AI Engineers — step-by-step agent execution |
| 5 | **Customize with Copilot** | 5-7 min | Developers — add agents via GitHub Copilot |
| 6 | **Open in Codespaces** | 2-3 min | Developers — zero-setup onboarding |

### Quick Demo Commands

```bash
# Register agents in Foundry project
python src/register_agents.py

# Run pipeline with sample data (Scenario 4)
python src/main.py --demo

# Interactive chat with orchestrator
python src/main.py
```

### Sample Data

- **Input**: `data/sample_request.json` — CGL submission for a tech company with 3 competitor quotes
- **Output**: `data/sample_response.json` — Complete pipeline result with recommendation and talk-track

---

## Troubleshooting

### Common Deployment Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `QuotaExceeded` (Azure OpenAI) | Region token-per-minute limit reached | Request quota increase: Portal → OpenAI → Quotas → Request increase |
| `ResourceProviderNotRegistered` | First-time use of a service | `az provider register --namespace Microsoft.CognitiveServices` (repeat per provider) |
| `InvalidTemplateDeployment` | Naming conflict (resource already exists) | Change `environmentName` to a unique value |
| `RoleAssignmentExists` | Re-running deployment | Safe to ignore — RBAC assignments are idempotent |
| APIM deployment timeout | Normal — takes 15–20 min | Wait and retry; do not cancel other resources |
| Fabric "Paused" state | Auto-pause on creation in some regions | Portal → Fabric → Resume capacity |
| Speech model unavailable | Region doesn't support requested model | Use East US, West Europe, or Southeast Asia for Speech |
| `SkuNotAvailable` | SKU not available in selected region | Try a different region or SKU tier |

### Resource Provider Registration

If you see `ResourceProviderNotRegistered`, run these commands:

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider register --namespace Microsoft.Search
az provider register --namespace Microsoft.Communication
az provider register --namespace Microsoft.Fabric
az provider register --namespace Microsoft.MachineLearningServices
az provider register --namespace Microsoft.Purview
az provider register --namespace Microsoft.DocumentDB
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.ApiManagement

# Wait for registration (1–5 minutes per provider)
az provider show --namespace Microsoft.CognitiveServices --query "registrationState" -o tsv
```

---

## Cost Management

### Estimated Monthly Costs

| Profile | Description | Est. Cost |
|---------|-------------|-----------|
| **POC / Demo** | Minimal SKUs, scale-to-zero, 50 queries/day | ~$100–200/month |
| **Pilot** | Standard SKUs, 4 advisors, 400 queries/day | ~$750–1,200/month |
| **Production** | High-availability, 20+ advisors, 2000+ queries/day | ~$3,000–5,000/month |

### Cost Optimization Tips

| Tip | Savings | How |
|-----|---------|-----|
| Use AI Search **Basic** tier for POC | ~$200/month | Change `sku` in `ai-search.bicep` to `basic` |
| Use APIM **Consumption** tier for POC | ~$175/month | Change `sku` in `apim.bicep` to `Consumption` |
| **Pause Fabric** when not in use | ~$260/month | Portal → Fabric → Pause (or set schedule) |
| Use Azure SQL **Serverless** (default) | Auto-pauses | Already configured — no action needed |
| Use Cosmos DB **Serverless** (default) | Pay only for queries | Already configured — no action needed |
| Set **budget alerts** | Prevention | Portal → Cost Management → Budgets → Create |

### Set Up Budget Alert

```bash
az consumption budget create \
  --budget-name "QuoteIntelligence-Monthly" \
  --amount 1000 \
  --resource-group rg-ins-qi-dev \
  --time-grain Monthly \
  --start-date $(date +%Y-%m-01) \
  --end-date 2027-12-31 \
  --notifications "[{\"enabled\":true,\"operator\":\"GreaterThan\",\"threshold\":80,\"contactEmails\":[\"admin@yourcompany.com\"]}]"
```

---

## Cleanup

To remove all deployed resources:

```bash
# Option 1: Using azd
azd down --force --purge

# Option 2: Using Azure CLI
az group delete --name rg-ins-qi-dev --yes --no-wait
```

> ⚠️ This permanently deletes all resources and data. Ensure backups are taken first.

---

*For architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md). For API contracts between agents, see [API_CONTRACTS.md](API_CONTRACTS.md).*
