// Main Bicep — Insurance Competitive Quote Intelligence Accelerator
// Orchestrates all Azure resources for a multimodal contact center AI solution
// Run: azd up (provisions all 24 Azure cloud services)
//
// Microsoft Cloud Services Provisioned:
// - Azure AI Foundry (Agent Service, Hosted Agents)
// - Azure OpenAI Service (GPT-4o, GPT-4o-mini)
// - Azure AI Search (Standard, Semantic Ranking)
// - Azure AI Speech (STT, TTS, Translation, Custom Speech, Voice Live)
// - Azure Document Intelligence
// - Azure AI Content Understanding
// - Azure AI Language (Sentiment, PII, Summarization)
// - Azure Communication Services (Voice, Recording)
// - Azure SQL Database
// - Azure Cosmos DB
// - Microsoft Fabric (Lakehouse)
// - Azure API Management (AI Gateway)
// - Azure Monitor + Application Insights
// - Azure Key Vault
// - Microsoft Entra ID (Agent Identities, RBAC)
// - Microsoft Purview (Data Governance)
// - Microsoft Defender for Cloud
// - Copilot Studio (license — configured separately)
// - Microsoft 365 E5 (license — configured separately)

targetScope = 'subscription'

// ============================================================================
// PARAMETERS
// ============================================================================

@description('Environment name (e.g., dev, staging, prod)')
param environmentName string

@description('Azure region for all resources')
param location string

@description('Base name for all resources')
param resourceBaseName string = 'ins-qi-${environmentName}'

@description('Tags applied to all resources')
param tags object = {
  solution: 'insurance-quote-intelligence'
  environment: environmentName
  managedBy: 'bicep-azd'
}

// ============================================================================
// DEPLOYMENT STAGES (Modular — deploy incrementally)
// ============================================================================
// Stage 1: Core AI (default: true) — AI Foundry, OpenAI, Speech, Search, Monitor
// Stage 2: Data Layer (default: false) — Azure SQL, Cosmos DB, Fabric
// Stage 3: Integration (default: false) — APIM, Communication Services, Governance
// ============================================================================

@description('Stage 1: Deploy Core AI services (AI Foundry, OpenAI, Speech, Search, Monitor)')
param deployCoreAI bool = true

@description('Optional: deploy the Container Apps hosted-agent runtime (registry, environment, container app). Requires a built agent image via `azd deploy`; leave off until the image exists so it does not block core AI provisioning.')
param deployHostedAgent bool = false

@description('Optional service: Deploy Azure AI Content Understanding. This is not available in all regions and can block provisioning in some subscriptions/locations.')
param deployContentUnderstanding bool = false

@description('Stage 2: Deploy Data Layer (Azure SQL, Cosmos DB, Fabric)')
param deployDataLayer bool = false

@description('Stage 3: Deploy Integration & Governance (APIM, ACS, Purview, Defender)')
param deployIntegration bool = false

// Data parameters (required only if deployDataLayer = true)
@description('SQL admin username (required if deployDataLayer is true)')
param sqlAdminLogin string = ''

@description('SQL admin password (required if deployDataLayer is true)')
@secure()
param sqlAdminPassword string = ''

// Integration parameters (required only if deployIntegration = true)
@description('Publisher email for API Management (required if deployIntegration is true)')
param apimPublisherEmail string = ''

@description('Publisher name for API Management')
param apimPublisherName string = 'Insurance Quote Intelligence'

// Fabric parameters (optional)
@description('Fabric admin member object IDs')
param fabricAdminMembers array = []

// ============================================================================
// RESOURCE GROUP
// ============================================================================

module resourceGroup 'modules/core/resource-group.bicep' = {
  name: 'rg-deployment'
  params: {
    name: 'rg-${resourceBaseName}'
    location: location
    tags: tags
  }
}

// ============================================================================
// STAGE 1: CORE AI (deployCoreAI = true by default)
// Includes: Resource Group, Key Vault, Monitor, AI Foundry, OpenAI, Speech,
//           AI Search, Document Intelligence, Content Understanding, AI Language
// ============================================================================

// --- Core Infrastructure (always deployed with Stage 1) ---

module keyVault 'modules/core/key-vault.bicep' = if (deployCoreAI) {
  name: 'kv-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'kv-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module logAnalytics 'modules/core/log-analytics.bicep' = if (deployCoreAI) {
  name: 'law-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'law-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module appInsights 'modules/core/app-insights.bicep' = if (deployCoreAI) {
  name: 'ai-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'ai-${resourceBaseName}'
    location: location
    tags: tags
    logAnalyticsWorkspaceId: deployCoreAI ? logAnalytics.outputs.id : ''
  }
  dependsOn: [resourceGroup]
}

// --- AI Foundry (Agent Runtime & Hosting) ---

module aiStorage 'modules/ai-foundry/managed-storage.bicep' = if (deployCoreAI) {
  name: 'ai-storage-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'sa${replace(resourceBaseName, '-', '')}ml'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module foundryProject 'modules/ai-foundry/foundry-project.bicep' = if (deployCoreAI) {
  name: 'foundry-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    accountName: 'aif-${resourceBaseName}'
    projectName: '${resourceBaseName}-project'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module hostedAgent 'modules/ai-foundry/hosted-agent.bicep' = if (deployCoreAI && deployHostedAgent) {
  name: 'agent-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: '${resourceBaseName}-agent'
    location: location
    tags: tags
    projectId: deployCoreAI ? foundryProject.outputs.projectId : ''
    containerRegistryId: ''
    environmentVariables: deployCoreAI ? {
      FOUNDRY_PROJECT_ENDPOINT: foundryProject.outputs.projectEndpoint
      FOUNDRY_MODEL_NAME: 'gpt-4o'
      AZURE_LOCATION: location
      APPLICATIONINSIGHTS_CONNECTION_STRING: appInsights.outputs.connectionString
    } : {}
  }
  dependsOn: [resourceGroup, foundryProject, appInsights]
}

// Grant the hosted agent's managed identity access to call the Foundry project
module hostedAgentFoundryAccess 'modules/ai-foundry/foundry-rbac.bicep' = if (deployCoreAI && deployHostedAgent) {
  name: 'foundry-rbac-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    accountId: deployCoreAI ? foundryProject.outputs.accountId : ''
    principalId: (deployCoreAI && deployHostedAgent) ? hostedAgent.outputs.principalId : ''
  }
}

module modelDeployments 'modules/ai-foundry/model-deployments.bicep' = if (deployCoreAI) {
  name: 'models-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'oai-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

// --- AI Services ---

module aiSearch 'modules/ai-services/ai-search.bicep' = if (deployCoreAI) {
  name: 'search-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'srch-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module documentIntelligence 'modules/ai-services/document-intelligence.bicep' = if (deployCoreAI) {
  name: 'docint-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'di-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module contentUnderstanding 'modules/ai-services/content-understanding.bicep' = if (deployCoreAI && deployContentUnderstanding) {
  name: 'cu-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'cu-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module aiLanguage 'modules/ai-services/ai-language.bicep' = if (deployCoreAI) {
  name: 'lang-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'lang-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

// --- Speech Services ---

module speechService 'modules/speech/speech-service.bicep' = if (deployCoreAI) {
  name: 'speech-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module speechSTT 'modules/speech/speech-stt.bicep' = if (deployCoreAI) {
  name: 'stt-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module speechTTS 'modules/speech/speech-tts.bicep' = if (deployCoreAI) {
  name: 'tts-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module speechTranslation 'modules/speech/speech-translation.bicep' = if (deployCoreAI) {
  name: 'translation-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
  }
  dependsOn: [speechService]
}

module customSpeech 'modules/speech/custom-speech.bicep' = if (deployCoreAI) {
  name: 'customspeech-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module voiceLive 'modules/speech/voice-live.bicep' = if (deployCoreAI) {
  name: 'voicelive-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'vl-${resourceBaseName}'
    location: location
    tags: tags
    speechServiceId: deployCoreAI ? speechService.outputs.id : ''
    openAIResourceId: deployCoreAI ? modelDeployments.outputs.id : ''
  }
  dependsOn: [speechService, modelDeployments]
}

// ============================================================================
// STAGE 2: DATA LAYER (deployDataLayer = true to enable)
// Includes: Azure SQL, Cosmos DB, Microsoft Fabric
// ============================================================================

module azureSql 'modules/data/azure-sql.bicep' = if (deployDataLayer) {
  name: 'sql-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    serverName: 'sql-${resourceBaseName}'
    location: location
    tags: tags
    adminLogin: sqlAdminLogin
    adminPassword: sqlAdminPassword
  }
  dependsOn: [resourceGroup]
}

module cosmosDb 'modules/data/cosmos-db.bicep' = if (deployDataLayer) {
  name: 'cosmos-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'cosmos-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module fabric 'modules/data/fabric-lakehouse.bicep' = if (deployDataLayer) {
  name: 'fabric-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'fabric${replace(resourceBaseName, '-', '')}'
    location: location
    tags: tags
    adminMembers: fabricAdminMembers
  }
  dependsOn: [resourceGroup]
}

// ============================================================================
// STAGE 3: INTEGRATION & GOVERNANCE (deployIntegration = true to enable)
// Includes: APIM, Communication Services, Entra Identities, RBAC, Purview, Defender
// ============================================================================

module communicationServices 'modules/communication/communication-services.bicep' = if (deployIntegration) {
  name: 'acs-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'acs-${resourceBaseName}'
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module callAutomation 'modules/communication/call-automation.bicep' = if (deployIntegration) {
  name: 'callaut-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    communicationServiceName: 'acs-${resourceBaseName}'
    location: location
    tags: tags
    speechServiceId: ''
  }
  dependsOn: [communicationServices]
}

module apim 'modules/integration/apim.bicep' = if (deployIntegration) {
  name: 'apim-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'apim-${resourceBaseName}'
    location: location
    tags: tags
    publisherEmail: apimPublisherEmail
    publisherName: apimPublisherName
  }
  dependsOn: [resourceGroup]
}

module agentIdentities 'modules/governance/entra-agent-identities.bicep' = if (deployIntegration) {
  name: 'identities-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    namePrefix: 'id-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module rbacAssignments 'modules/governance/rbac-assignments.bicep' = if (deployIntegration && deployCoreAI) {
  name: 'rbac-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    orchestratorPrincipalId: deployIntegration ? agentIdentities.outputs.orchestratorPrincipalId : ''
    intakePrincipalId: deployIntegration ? agentIdentities.outputs.intakePrincipalId : ''
    priceCollectionPrincipalId: deployIntegration ? agentIdentities.outputs.priceCollectionPrincipalId : ''
    analysisPrincipalId: deployIntegration ? agentIdentities.outputs.analysisPrincipalId : ''
    decisionPrincipalId: deployIntegration ? agentIdentities.outputs.decisionPrincipalId : ''
    speechPrincipalId: deployIntegration ? agentIdentities.outputs.speechPrincipalId : ''
    compliancePrincipalId: deployIntegration ? agentIdentities.outputs.compliancePrincipalId : ''
    openAIResourceId: deployCoreAI ? modelDeployments.outputs.id : ''
    aiSearchResourceId: deployCoreAI ? aiSearch.outputs.id : ''
    sqlServerId: deployDataLayer ? azureSql.outputs.serverId : ''
    keyVaultId: deployCoreAI ? keyVault.outputs.id : ''
    storageAccountId: deployCoreAI ? aiStorage.outputs.id : ''
  }
  dependsOn: [agentIdentities, aiStorage]
}

module purview 'modules/governance/purview-policies.bicep' = if (deployIntegration) {
  name: 'purview-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'pv-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module defender 'modules/governance/defender-config.bicep' = if (deployIntegration) {
  name: 'defender-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {}
  dependsOn: [resourceGroup]
}

// ============================================================================
// OUTPUTS
// ============================================================================

// Stage 1 outputs (Core AI)
output resourceGroupName string = 'rg-${resourceBaseName}'
output FOUNDRY_PROJECT_ENDPOINT string = deployCoreAI ? foundryProject.outputs.projectEndpoint : 'Not deployed — enable deployCoreAI'
output aiFoundryAccountEndpoint string = deployCoreAI ? foundryProject.outputs.accountEndpoint : 'Not deployed'
output openAIEndpoint string = deployCoreAI ? modelDeployments.outputs.endpoint : 'Not deployed'
output aiSearchEndpoint string = deployCoreAI ? aiSearch.outputs.endpoint : 'Not deployed'
output speechEndpoint string = deployCoreAI ? speechService.outputs.endpoint : 'Not deployed'
output appInsightsConnectionString string = deployCoreAI ? appInsights.outputs.connectionString : 'Not deployed'

// Stage 2 outputs (Data Layer)
output sqlServerFqdn string = deployDataLayer ? azureSql.outputs.serverFqdn : 'Not deployed — enable deployDataLayer'
output cosmosEndpoint string = deployDataLayer ? cosmosDb.outputs.endpoint : 'Not deployed'

// Stage 3 outputs (Integration)
output apimGatewayUrl string = deployIntegration ? apim.outputs.gatewayUrl : 'Not deployed — enable deployIntegration'
