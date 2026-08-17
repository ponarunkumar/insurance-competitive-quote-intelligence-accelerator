// Azure AI Foundry Hub — the workspace for all AI agents, models, and connections
// Billing: Consumption-based billing for agent executions and model inference

@description('Name of the AI Foundry hub')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Key Vault resource ID for secrets')
param keyVaultId string

@description('Application Insights resource ID')
param appInsightsId string

@description('Storage account resource ID for agent state')
param storageAccountId string

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Insurance Quote Intelligence Hub'
    description: 'AI Foundry hub for competitive quote intelligence multi-agent system'
    keyVault: keyVaultId
    applicationInsights: appInsightsId
    storageAccount: storageAccountId
    publicNetworkAccess: 'Enabled'
  }
}

output id string = aiHub.id
output name string = aiHub.name
output principalId string = aiHub.identity.principalId
