// Azure OpenAI Model Deployments for agent reasoning
// Billing: Per-token billing (input + output) — primary Azure AI usage driver
// Every agent call across 12 specialist agents burns tokens

@description('Name of the Azure OpenAI account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU for the OpenAI account')
param sku string = 'S0'

@description('Primary model for agent reasoning')
param primaryModel string = 'gpt-4o'

@description('Primary model version')
param primaryModelVersion string = '2024-11-20'

@description('Primary model capacity (tokens per minute in thousands)')
param primaryModelCapacity int = 80

@description('Secondary model for lightweight tasks')
param secondaryModel string = 'gpt-4.1-mini'

@description('Secondary model version')
param secondaryModelVersion string = '2025-04-14'

@description('Secondary model capacity')
param secondaryModelCapacity int = 120

resource openai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: sku
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

// Primary model — used by Orchestrator, Recommendation, Risk Assessment agents
resource primaryDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openai
  name: primaryModel
  sku: {
    name: 'Standard'
    capacity: primaryModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: primaryModel
      version: primaryModelVersion
    }
  }
}

// Secondary model — used by Intake, Normalization, Explanation agents (cost optimization)
resource secondaryDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openai
  name: secondaryModel
  dependsOn: [primaryDeployment]
  sku: {
    name: 'Standard'
    capacity: secondaryModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: secondaryModel
      version: secondaryModelVersion
    }
  }
}

output id string = openai.id
output name string = openai.name
output endpoint string = openai.properties.endpoint
output primaryModelDeployment string = primaryDeployment.name
output secondaryModelDeployment string = secondaryDeployment.name
