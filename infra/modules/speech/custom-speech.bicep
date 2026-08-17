// Custom Speech model for insurance-specific terminology
// Billing: Per-endpoint-hour billing for deployed custom models
// Improves accuracy for: policy types, coverage terms, carrier names, underwriting jargon
//
// Custom training data includes:
// - Insurance product names (CGL, E&O, D&O, BOP, WC, etc.)
// - Carrier and MGA names
// - Underwriting terminology (aggregate limit, deductible, sublimit, occurrence)
// - Numeric accuracy for premium amounts and policy numbers

@description('Name of the Speech service (parent)')
param speechServiceName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Base model locale')
param locale string = 'en-GB'

@description('Enable custom model endpoint (incurs per-hour charge)')
param deployCustomEndpoint bool = false

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: speechServiceName
}

// Storage for custom speech training data (audio + transcripts)
resource trainingStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: '${replace(speechServiceName, '-', '')}csp'
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
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: trainingStorage
  name: 'default'
}

resource trainingDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'training-data'
  properties: {
    publicAccess: 'None'
  }
}

resource phraseListContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'phrase-lists'
  properties: {
    publicAccess: 'None'
  }
}

output speechServiceEndpoint string = speechService.properties.endpoint
output trainingStorageId string = trainingStorage.id
output locale string = locale
output customEndpointDeployed bool = deployCustomEndpoint
