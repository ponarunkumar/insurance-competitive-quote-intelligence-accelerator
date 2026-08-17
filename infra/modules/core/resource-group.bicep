// Resource Group module for Insurance Competitive Quote Intelligence Accelerator
// Provisions the primary resource group for all solution resources

targetScope = 'subscription'

@description('Name of the resource group')
param name string

@description('Azure region for the resource group')
param location string

@description('Tags to apply to the resource group')
param tags object = {}

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: name
  location: location
  tags: union(tags, {
    solution: 'insurance-quote-intelligence'
    managedBy: 'bicep'
  })
}

output id string = rg.id
output name string = rg.name
output location string = rg.location
