// Azure SQL Database — Operational Data Store for quotes, rates, and policy data
// Billing: vCore/DTU monthly billing
// The single source of truth: consolidates carrier rating data, competitor quotes, and policy records

@description('Name of the SQL Server')
param serverName string

@description('Name of the database')
param databaseName string = 'InsuranceQuoteIntelligence'

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('SQL admin username')
@secure()
param adminLogin string

@description('SQL admin password')
@secure()
param adminPassword string

@description('Database SKU')
@allowed(['Basic', 'S0', 'S1', 'S2', 'S3', 'GP_Gen5_2', 'GP_Gen5_4', 'GP_S_Gen5_2'])
param databaseSku string = 'GP_S_Gen5_2'

@description('Enable Microsoft Entra authentication')
param enableEntraAuth bool = true

resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: serverName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    administratorLogin: adminLogin
    administratorLoginPassword: adminPassword
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
}

// Allow Azure services to access
resource firewallRule 'Microsoft.Sql/servers/firewallRules@2023-08-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource database 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sqlServer
  name: databaseName
  location: location
  tags: tags
  sku: {
    name: databaseSku
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: 34359738368 // 32GB
    zoneRedundant: false
    readScale: 'Disabled'
  }
}

output serverId string = sqlServer.id
output serverName string = sqlServer.name
output serverFqdn string = sqlServer.properties.fullyQualifiedDomainName
output databaseId string = database.id
output databaseName string = database.name
