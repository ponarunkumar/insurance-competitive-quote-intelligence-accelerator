// Azure AI Language — text analytics for call transcripts and submissions
// Billing: Per-1K text records billing
// Provides: sentiment analysis, PII detection, conversation summarization, entity recognition
// Used by: Call Analytics Agent, Compliance Agent (PII redaction), Coaching Agent

@description('Name of the Language service account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SKU')
@allowed(['F0', 'S'])
param sku string = 'S'

resource languageService 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'TextAnalytics'
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

output id string = languageService.id
output name string = languageService.name
output endpoint string = languageService.properties.endpoint
output principalId string = languageService.identity.principalId
