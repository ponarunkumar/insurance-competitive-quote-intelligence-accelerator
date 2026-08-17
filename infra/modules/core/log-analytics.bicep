// Log Analytics Workspace for centralized agent telemetry, call analytics, and compliance auditing
// All agent traces, speech transcription logs, and document processing metrics flow here

@description('Name of the Log Analytics workspace')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Data retention in days')
param retentionInDays int = 90

@description('SKU for the workspace')
@allowed(['PerGB2018', 'CapacityReservation'])
param sku string = 'PerGB2018'

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      name: sku
    }
    retentionInDays: retentionInDays
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

output id string = workspace.id
output name string = workspace.name
output customerId string = workspace.properties.customerId
