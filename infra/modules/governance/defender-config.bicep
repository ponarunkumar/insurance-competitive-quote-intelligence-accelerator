// Microsoft Defender for Cloud — threat protection for AI workloads
// Billing: Per-resource/per-user monthly billing
// Protects: agent endpoints, data stores, API surfaces from threats

@description('Enable Defender for App Service')
param enableAppService bool = true

@description('Enable Defender for SQL')
param enableSql bool = true

@description('Enable Defender for Storage')
param enableStorage bool = true

@description('Enable Defender for Key Vault')
param enableKeyVault bool = true

@description('Enable Defender for Containers')
param enableContainers bool = true

resource defenderAppService 'Microsoft.Security/pricings@2024-01-01' = if (enableAppService) {
  name: 'AppServices'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderSql 'Microsoft.Security/pricings@2024-01-01' = if (enableSql) {
  name: 'SqlServers'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderStorage 'Microsoft.Security/pricings@2024-01-01' = if (enableStorage) {
  name: 'StorageAccounts'
  properties: {
    pricingTier: 'Standard'
    subPlan: 'DefenderForStorageV2'
  }
}

resource defenderKeyVault 'Microsoft.Security/pricings@2024-01-01' = if (enableKeyVault) {
  name: 'KeyVaults'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderContainers 'Microsoft.Security/pricings@2024-01-01' = if (enableContainers) {
  name: 'Containers'
  properties: {
    pricingTier: 'Standard'
  }
}

output defenderEnabled bool = true
