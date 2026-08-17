// Azure AI Content Understanding — multimodal content processing
// Billing: Per-transaction billing for image, video, and mixed-document analysis
// Processes: scanned quote images, video walkthroughs of properties, mixed-format submissions

@description('Name of the Content Understanding account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU')
param sku string = 'S0'

resource contentUnderstanding 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'ContentUnderstanding'
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

output id string = contentUnderstanding.id
output name string = contentUnderstanding.name
output endpoint string = contentUnderstanding.properties.endpoint
output principalId string = contentUnderstanding.identity.principalId
