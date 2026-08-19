// Grants a principal (e.g. the hosted agent's managed identity) access to
// call the Azure AI Foundry project via the built-in "Azure AI Developer" role.

@description('Resource ID of the Foundry account (scope for the role assignment)')
param accountId string

@description('Principal ID to grant access to')
param principalId string

var azureAIDeveloperRole = '64702f94-c441-49e6-a78b-ef80e0188fee'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: last(split(accountId, '/'))
}

resource foundryAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(accountId, principalId, azureAIDeveloperRole)
  scope: account
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', azureAIDeveloperRole)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
