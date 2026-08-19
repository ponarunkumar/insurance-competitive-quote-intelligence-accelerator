// Azure AI Foundry — unified account (kind: AIServices) + project sub-resource
// This is the current (non-legacy) Foundry pattern: a single Cognitive Services
// account with allowProjectManagement enabled, hosting one or more projects.
// Produces the endpoint format required by azure-ai-projects >= 2.3.0:
//   https://<account-name>.services.ai.azure.com/api/projects/<project-name>

@description('Name of the Foundry account (Cognitive Services multi-service resource)')
param accountName string

@description('Name of the Foundry project (sub-resource of the account)')
param projectName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Friendly display name for the project')
param projectDisplayName string = 'Quote Intelligence Agents'

@description('Description for the project')
param projectDescription string = 'Multi-agent project for competitive quote intelligence in insurance contact centers'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: accountName
    allowProjectManagement: true
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: projectName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: projectDisplayName
    description: projectDescription
  }
}

output accountId string = account.id
output accountName string = account.name
output accountPrincipalId string = account.identity.principalId
output accountEndpoint string = account.properties.endpoint
output projectId string = project.id
output projectName string = project.name
output projectPrincipalId string = project.identity.principalId
output projectEndpoint string = '${account.properties.endpoint}api/projects/${project.name}'
