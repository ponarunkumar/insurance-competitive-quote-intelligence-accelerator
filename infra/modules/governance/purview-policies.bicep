// Microsoft Purview — data governance and lineage tracking
// Billing: Per-asset billing for data catalog and governance
// Ensures: policyholder data protection, competitive data compliance, audit trails

@description('Name of the Purview account')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

resource purviewAccount 'Microsoft.Purview/accounts@2024-04-01-preview' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    managedResourceGroupName: '${name}-managed-rg'
  }
}

output id string = purviewAccount.id
output name string = purviewAccount.name
output principalId string = purviewAccount.identity.principalId
output catalogEndpoint string = 'https://${name}.purview.azure.com'
