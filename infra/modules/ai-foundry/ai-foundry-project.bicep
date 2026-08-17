// Azure AI Foundry Project with Agent Service enabled
// This is where agents are deployed, managed, and monitored
// Billing: Per-session, per-execution billing for every agent interaction

@description('Name of the AI Foundry project')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('AI Foundry Hub resource ID')
param hubId string

@description('Enable Agent Service')
param enableAgentService bool = true

resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'Project'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Quote Intelligence Agents'
    description: 'Multi-agent project for competitive quote intelligence in insurance contact centers'
    hubResourceId: hubId
    publicNetworkAccess: 'Enabled'
  }
}

// Agent Service configuration
resource agentService 'Microsoft.MachineLearningServices/workspaces/agents@2024-10-01' = if (enableAgentService) {
  parent: aiProject
  name: 'default'
  properties: {
    description: 'Agent service for insurance quote intelligence orchestration'
  }
}

output id string = aiProject.id
output name string = aiProject.name
output principalId string = aiProject.identity.principalId
