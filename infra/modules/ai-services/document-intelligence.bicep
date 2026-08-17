// Azure Document Intelligence — structured extraction from insurance documents
// Billing: Per-page / per-transaction billing
// Processes: competitor quote PDFs, certificates of insurance, loss runs, proposal forms, schedules

@description('Name of the Document Intelligence account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU')
@allowed(['F0', 'S0'])
param sku string = 'S0'

resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'FormRecognizer'
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

output id string = documentIntelligence.id
output name string = documentIntelligence.name
output endpoint string = documentIntelligence.properties.endpoint
output principalId string = documentIntelligence.identity.principalId
