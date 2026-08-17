// Application Insights for agent performance monitoring, tracing, and OpenTelemetry ingestion
// Captures: agent execution traces, tool call latencies, speech processing metrics, HITL approval times

@description('Name of the Application Insights resource')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Log Analytics workspace ID for data sink')
param logAnalyticsWorkspaceId string

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: name
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspaceId
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
    RetentionInDays: 90
  }
}

output id string = appInsights.id
output name string = appInsights.name
output connectionString string = appInsights.properties.ConnectionString
output instrumentationKey string = appInsights.properties.InstrumentationKey
