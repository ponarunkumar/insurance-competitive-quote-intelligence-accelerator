// Azure AI Speech Service — unified account for STT, TTS, Translation, and Diarization
// Billing: Per-audio-hour (STT/Translation), Per-1M characters (TTS), Per-endpoint-hour (Custom Speech)
// This is the foundation account; individual capabilities are configured via child resources

@description('Name of the Speech service account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU')
@allowed(['F0', 'S0'])
param sku string = 'S0'

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'SpeechServices'
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

output id string = speechService.id
output name string = speechService.name
output endpoint string = speechService.properties.endpoint
output region string = speechService.location
output principalId string = speechService.identity.principalId
