// Foundry Hosted Agent — production runtime with session isolation and Entra Agent Identity
// Billing: Consumption billing per agent session; automatic scale-to-zero when idle
// Each agent gets its own Entra identity for RBAC-scoped access to data and tools

@description('Name of the hosted agent')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('AI Foundry Project resource ID')
param projectId string

@description('Container Registry for agent container image')
param containerRegistryId string

@description('Agent container image')
param containerImage string = ''

@description('Environment variables for the agent')
param environmentVariables object = {}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: '${replace(name, '-', '')}cr'
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    environmentId: containerAppEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        transport: 'http'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: 'system'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'agent'
          // Placeholder until `azd deploy` builds and pushes the real orchestrator image
          image: !empty(containerImage) ? containerImage : 'mcr.microsoft.com/k8se/quickstart:latest'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [for key in items(environmentVariables): {
            name: key.key
            value: key.value
          }]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
        rules: [
          {
            name: 'http-rule'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
        ]
      }
    }
  }
}

resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${name}-env'
  location: location
  tags: tags
  properties: {
    zoneRedundant: false
  }
}

output id string = containerApp.id
output name string = containerApp.name
output fqdn string = containerApp.properties.configuration.ingress.fqdn
output principalId string = containerApp.identity.principalId
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
