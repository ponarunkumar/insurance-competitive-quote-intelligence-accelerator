// RBAC Role Assignments — least-privilege access for each agent identity
// Implements zero-trust: each agent only accesses what it needs

@description('Orchestrator principal ID')
param orchestratorPrincipalId string

@description('Intake agent principal ID')
param intakePrincipalId string

@description('Price collection agent principal ID')
param priceCollectionPrincipalId string

@description('Analysis agent principal ID')
param analysisPrincipalId string

@description('Decision agent principal ID')
param decisionPrincipalId string

@description('Speech agent principal ID')
param speechPrincipalId string

@description('Compliance agent principal ID')
param compliancePrincipalId string

@description('Azure OpenAI resource ID')
param openAIResourceId string

@description('AI Search resource ID')
param aiSearchResourceId string

@description('Azure SQL Server resource ID')
param sqlServerId string

@description('Key Vault resource ID')
param keyVaultId string

@description('Storage account resource ID')
param storageAccountId string

// Built-in role definition IDs
var cognitiveServicesOpenAIUser = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
var searchIndexDataReader = '1407120a-92aa-4202-b7e9-c0e197c71c8f'
var keyVaultSecretsUser = '4633458b-17de-408a-b874-0445c86b69e6'
var storageBlobDataReader = '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
var storageBlobDataContributor = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'

// Orchestrator — OpenAI access for reasoning
resource orchestratorOpenAI 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAIResourceId, orchestratorPrincipalId, cognitiveServicesOpenAIUser)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesOpenAIUser)
    principalId: orchestratorPrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Intake — Document reading from storage
resource intakeStorage 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccountId, intakePrincipalId, storageBlobDataReader)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataReader)
    principalId: intakePrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Analysis — AI Search reading for RAG
resource analysisSearch 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiSearchResourceId, analysisPrincipalId, searchIndexDataReader)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', searchIndexDataReader)
    principalId: analysisPrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Decision — Key Vault for rate-update credentials (gated by HITL)
resource decisionKeyVault 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVaultId, decisionPrincipalId, keyVaultSecretsUser)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', keyVaultSecretsUser)
    principalId: decisionPrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Speech — Storage access for recordings and transcriptions
resource speechStorage 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccountId, speechPrincipalId, storageBlobDataContributor)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataContributor)
    principalId: speechPrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Compliance — read-only across all resources (Reader role at RG level)
resource complianceReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, compliancePrincipalId, 'acdd72a7-3385-48ef-bd42-f606fba81ae7')
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'acdd72a7-3385-48ef-bd42-f606fba81ae7')
    principalId: compliancePrincipalId
    principalType: 'ServicePrincipal'
  }
}
