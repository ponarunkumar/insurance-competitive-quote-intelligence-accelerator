// Azure API Management — AI Gateway for competitor APIs, token management, and caching
// Billing: Monthly instance charge + per-call overage
// Role: Rate-limit competitor API calls, cache responses, route to multiple carriers, track token spend

@description('Name of the APIM instance')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Publisher email')
param publisherEmail string

@description('Publisher name')
param publisherName string

@description('SKU')
@allowed(['Consumption', 'Developer', 'Basic', 'Standard', 'Premium', 'StandardV2'])
param sku string = 'StandardV2'

@description('SKU capacity (units)')
param skuCapacity int = 1

resource apim 'Microsoft.ApiManagement/service@2023-09-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: sku
    capacity: sku == 'Consumption' ? 0 : skuCapacity
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
    publicNetworkAccess: 'Enabled'
  }
}

// API for competitor quote collection
resource competitorApi 'Microsoft.ApiManagement/service/apis@2023-09-01-preview' = {
  parent: apim
  name: 'competitor-quotes'
  properties: {
    displayName: 'Competitor Quote APIs'
    description: 'Gateway for competitor carrier rating APIs'
    path: 'competitors'
    protocols: ['https']
    subscriptionRequired: true
    apiType: 'http'
  }
}

// API for internal agent-to-agent communication
resource agentApi 'Microsoft.ApiManagement/service/apis@2023-09-01-preview' = {
  parent: apim
  name: 'agent-orchestration'
  properties: {
    displayName: 'Agent Orchestration API'
    description: 'Internal API for agent-to-agent communication and tool calls'
    path: 'agents'
    protocols: ['https']
    subscriptionRequired: true
    apiType: 'http'
  }
}

// Product grouping for rate limiting
resource competitorProduct 'Microsoft.ApiManagement/service/products@2023-09-01-preview' = {
  parent: apim
  name: 'competitor-intelligence'
  properties: {
    displayName: 'Competitor Intelligence'
    description: 'Product tier for competitor quote collection APIs'
    subscriptionRequired: true
    approvalRequired: false
    state: 'published'
  }
}

output id string = apim.id
output name string = apim.name
output gatewayUrl string = apim.properties.gatewayUrl
output principalId string = apim.identity.principalId
