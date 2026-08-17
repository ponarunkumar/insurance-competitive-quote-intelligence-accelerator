// Azure Cosmos DB — agent conversation state and session history
// Billing: Per-RU (serverless) or provisioned throughput billing
// Stores: agent conversation threads, HITL approval records, orchestration state

@description('Name of the Cosmos DB account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Capacity mode')
@allowed(['Serverless', 'Provisioned'])
param capacityMode string = 'Serverless'

resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: name
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: capacityMode == 'Serverless' ? [{ name: 'EnableServerless' }] : []
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    publicNetworkAccess: 'Enabled'
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmosAccount
  name: 'quote-intelligence'
  properties: {
    resource: {
      id: 'quote-intelligence'
    }
  }
}

resource sessionsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'agent-sessions'
  properties: {
    resource: {
      id: 'agent-sessions'
      partitionKey: {
        paths: ['/sessionId']
        kind: 'Hash'
      }
      defaultTtl: 2592000 // 30 days
    }
  }
}

resource approvalsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'hitl-approvals'
  properties: {
    resource: {
      id: 'hitl-approvals'
      partitionKey: {
        paths: ['/quoteId']
        kind: 'Hash'
      }
    }
  }
}

output id string = cosmosAccount.id
output name string = cosmosAccount.name
output endpoint string = cosmosAccount.properties.documentEndpoint
output databaseName string = database.name
output principalId string = cosmosAccount.identity.principalId
