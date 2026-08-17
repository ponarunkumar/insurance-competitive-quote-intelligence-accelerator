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

// Data parameters
@description('SQL admin username')
@secure()
param sqlAdminLogin string

@description('SQL admin password')
@secure()
param sqlAdminPassword string

// APIM parameters
@description('Publisher email for API Management')
param apimPublisherEmail string

@description('Publisher name for API Management')
param apimPublisherName string = 'Insurance Quote Intelligence'

// Fabric parameters
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
// CORE INFRASTRUCTURE
// ============================================================================

module keyVault 'modules/core/key-vault.bicep' = {
  name: 'kv-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'kv-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module logAnalytics 'modules/core/log-analytics.bicep' = {
  name: 'law-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'law-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module appInsights 'modules/core/app-insights.bicep' = {
  name: 'ai-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'ai-${resourceBaseName}'
    location: location
    tags: tags
    logAnalyticsWorkspaceId: logAnalytics.outputs.id
  }
  dependsOn: [resourceGroup]
}

// ============================================================================
// AI FOUNDRY (Agent Runtime & Hosting)
// ============================================================================

module storageAccount 'modules/ai-foundry/hosted-agent.bicep' = {
  name: 'agent-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: '${resourceBaseName}-agent'
    location: location
    tags: tags
    projectId: aiProject.outputs.id
    containerRegistryId: ''
  }
  dependsOn: [resourceGroup]
}

module aiHub 'modules/ai-foundry/ai-foundry-hub.bicep' = {
  name: 'aihub-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'aih-${resourceBaseName}'
    location: location
    tags: tags
    keyVaultId: keyVault.outputs.id
    appInsightsId: appInsights.outputs.id
    storageAccountId: '' // TODO: Wire storage account for agent state
  }
  dependsOn: [resourceGroup]
}

module aiProject 'modules/ai-foundry/ai-foundry-project.bicep' = {
  name: 'aiproject-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'aip-${resourceBaseName}'
    location: location
    tags: tags
    hubId: aiHub.outputs.id
  }
}

module modelDeployments 'modules/ai-foundry/model-deployments.bicep' = {
  name: 'models-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'oai-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

// ============================================================================
// AI SERVICES
// ============================================================================

module aiSearch 'modules/ai-services/ai-search.bicep' = {
  name: 'search-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'srch-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module documentIntelligence 'modules/ai-services/document-intelligence.bicep' = {
  name: 'docint-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'di-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module contentUnderstanding 'modules/ai-services/content-understanding.bicep' = {
  name: 'cu-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'cu-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module aiLanguage 'modules/ai-services/ai-language.bicep' = {
  name: 'lang-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'lang-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

// ============================================================================
// SPEECH SERVICES (Full multimodal voice stack)
// ============================================================================

module speechService 'modules/speech/speech-service.bicep' = {
  name: 'speech-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module speechSTT 'modules/speech/speech-stt.bicep' = {
  name: 'stt-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module speechTTS 'modules/speech/speech-tts.bicep' = {
  name: 'tts-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module speechTranslation 'modules/speech/speech-translation.bicep' = {
  name: 'translation-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
  }
  dependsOn: [speechService]
}

module customSpeech 'modules/speech/custom-speech.bicep' = {
  name: 'customspeech-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    speechServiceName: 'speech-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [speechService]
}

module voiceLive 'modules/speech/voice-live.bicep' = {
  name: 'voicelive-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'vl-${resourceBaseName}'
    location: location
    tags: tags
    speechServiceId: speechService.outputs.id
    openAIResourceId: modelDeployments.outputs.id
  }
  dependsOn: [speechService, modelDeployments]
}

// ============================================================================
// COMMUNICATION SERVICES (Contact Center)
// ============================================================================

module communicationServices 'modules/communication/communication-services.bicep' = {
  name: 'acs-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'acs-${resourceBaseName}'
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module callAutomation 'modules/communication/call-automation.bicep' = {
  name: 'callaut-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    communicationServiceName: 'acs-${resourceBaseName}'
    location: location
    tags: tags
    speechServiceId: speechService.outputs.id
  }
  dependsOn: [communicationServices]
}

// ============================================================================
// DATA LAYER
// ============================================================================

module azureSql 'modules/data/azure-sql.bicep' = {
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

module cosmosDb 'modules/data/cosmos-db.bicep' = {
  name: 'cosmos-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'cosmos-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module fabric 'modules/data/fabric-lakehouse.bicep' = {
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
// INTEGRATION (API Management AI Gateway)
// ============================================================================

module apim 'modules/integration/apim.bicep' = {
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

// ============================================================================
// GOVERNANCE
// ============================================================================

module agentIdentities 'modules/governance/entra-agent-identities.bicep' = {
  name: 'identities-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    namePrefix: 'id-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module rbacAssignments 'modules/governance/rbac-assignments.bicep' = {
  name: 'rbac-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    orchestratorPrincipalId: agentIdentities.outputs.orchestratorPrincipalId
    intakePrincipalId: agentIdentities.outputs.intakePrincipalId
    priceCollectionPrincipalId: agentIdentities.outputs.priceCollectionPrincipalId
    analysisPrincipalId: agentIdentities.outputs.analysisPrincipalId
    decisionPrincipalId: agentIdentities.outputs.decisionPrincipalId
    speechPrincipalId: agentIdentities.outputs.speechPrincipalId
    compliancePrincipalId: agentIdentities.outputs.compliancePrincipalId
    openAIResourceId: modelDeployments.outputs.id
    aiSearchResourceId: aiSearch.outputs.id
    sqlServerId: azureSql.outputs.serverId
    keyVaultId: keyVault.outputs.id
    storageAccountId: '' // TODO: Wire primary storage account
  }
  dependsOn: [agentIdentities]
}

module purview 'modules/governance/purview-policies.bicep' = {
  name: 'purview-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {
    name: 'pv-${resourceBaseName}'
    location: location
    tags: tags
  }
  dependsOn: [resourceGroup]
}

module defender 'modules/governance/defender-config.bicep' = {
  name: 'defender-deployment'
  scope: az.resourceGroup('rg-${resourceBaseName}')
  params: {}
  dependsOn: [resourceGroup]
}

// ============================================================================
// OUTPUTS
// ============================================================================

output resourceGroupName string = 'rg-${resourceBaseName}'
output aiFoundryEndpoint string = aiHub.outputs.name
output openAIEndpoint string = modelDeployments.outputs.endpoint
output aiSearchEndpoint string = aiSearch.outputs.endpoint
output speechEndpoint string = speechService.outputs.endpoint
output sqlServerFqdn string = azureSql.outputs.serverFqdn
output cosmosEndpoint string = cosmosDb.outputs.endpoint
output apimGatewayUrl string = apim.outputs.gatewayUrl
output appInsightsConnectionString string = appInsights.outputs.connectionString
