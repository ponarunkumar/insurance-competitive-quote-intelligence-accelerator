// Azure AI Search — RAG grounding for underwriting manuals, appetite guides, and policy documents
// Billing: Per-unit monthly charge (Standard S1) + per-query semantic ranking charges
// Always-on service — indexes must stay provisioned for agent grounding

@description('Name of the AI Search service')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU tier')
@allowed(['basic', 'standard', 'standard2', 'standard3'])
param sku string = 'standard'

@description('Number of replicas for high availability')
param replicaCount int = 1

@description('Number of partitions for storage/throughput')
param partitionCount int = 1

@description('Enable semantic ranker for improved relevance')
param semanticSearch string = 'standard'

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: sku
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    replicaCount: replicaCount
    partitionCount: partitionCount
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    semanticSearch: semanticSearch
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
  }
}

output id string = search.id
output name string = search.name
output endpoint string = 'https://${search.name}.search.windows.net'
output principalId string = search.identity.principalId
