// Managed storage account for the Azure AI Foundry hub and project workspace
// Required by Azure ML workspaces to persist project state, data, and metadata

@description('Name of the storage account for Azure AI Foundry')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    publicNetworkAccess: 'Enabled'
  }
}

output id string = storageAccount.id
output name string = storageAccount.name
