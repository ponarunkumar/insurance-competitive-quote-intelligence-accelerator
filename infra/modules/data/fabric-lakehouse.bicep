// Microsoft Fabric Lakehouse — analytics and historical quote data
// Billing: Capacity Units (CU) per month (F2+ SKU)
// Provides: historical quote analytics, market trend analysis, pricing model training data

@description('Name of the Fabric capacity')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Fabric SKU')
@allowed(['F2', 'F4', 'F8', 'F16', 'F32', 'F64'])
param sku string = 'F2'

@description('Admin members (Entra object IDs)')
param adminMembers array = []

resource fabricCapacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: sku
    tier: 'Fabric'
  }
  properties: {
    administration: {
      members: adminMembers
    }
  }
}

output id string = fabricCapacity.id
output name string = fabricCapacity.name
output state string = fabricCapacity.properties.state
