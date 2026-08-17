// Entra Agent Identities — managed identities for each specialist agent
// Billing: Entra ID P2 per-user/month for PIM, Conditional Access on agent identities
// Each agent gets a least-privilege identity scoped to its data and tools

@description('Base name prefix for agent identities')
param namePrefix string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

// Orchestrator identity — has delegation rights to invoke specialist agents
resource orchestratorIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-orchestrator'
  location: location
  tags: tags
}

// Intake agent identity — read access to submissions and documents
resource intakeIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-intake'
  location: location
  tags: tags
}

// Price collection agent identity — access to competitor APIs via APIM
resource priceCollectionIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-price-collection'
  location: location
  tags: tags
}

// Analysis agents identity — read access to quotes and rating data
resource analysisIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-analysis'
  location: location
  tags: tags
}

// Decision agent identity — write access to rate recommendations (requires HITL approval)
resource decisionIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-decision'
  location: location
  tags: tags
}

// Speech agent identity — access to Speech services and call recordings
resource speechIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-speech'
  location: location
  tags: tags
}

// Compliance agent identity — read-only, audit access to all resources
resource complianceIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${namePrefix}-compliance'
  location: location
  tags: tags
}

output orchestratorId string = orchestratorIdentity.id
output orchestratorPrincipalId string = orchestratorIdentity.properties.principalId
output intakeId string = intakeIdentity.id
output intakePrincipalId string = intakeIdentity.properties.principalId
output priceCollectionId string = priceCollectionIdentity.id
output priceCollectionPrincipalId string = priceCollectionIdentity.properties.principalId
output analysisId string = analysisIdentity.id
output analysisPrincipalId string = analysisIdentity.properties.principalId
output decisionId string = decisionIdentity.id
output decisionPrincipalId string = decisionIdentity.properties.principalId
output speechId string = speechIdentity.id
output speechPrincipalId string = speechIdentity.properties.principalId
output complianceId string = complianceIdentity.id
output compliancePrincipalId string = complianceIdentity.properties.principalId
