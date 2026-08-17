// ACS Call Automation — programmable voice for IVR, routing, and recording triggers
// Billing: Per-call billing + recording storage
// Enables: automated call routing, mid-call agent injection, call recording for compliance

@description('Name of the Communication Services resource (parent)')
param communicationServiceName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Callback endpoint for call events')
param callbackEndpoint string = ''

@description('Speech service resource ID for cognitive speech in calls')
param speechServiceId string = ''

@description('Enable call recording')
param enableRecording bool = true

resource communicationService 'Microsoft.Communication/communicationServices@2023-06-01-preview' existing = {
  name: communicationServiceName
}

// Storage for call recordings
resource recordingStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = if (enableRecording) {
  name: '${replace(communicationServiceName, '-', '')}rec'
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = if (enableRecording) {
  parent: recordingStorage
  name: 'default'
}

resource recordingsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = if (enableRecording) {
  parent: blobService
  name: 'call-recordings'
  properties: {
    publicAccess: 'None'
  }
}

output communicationServiceHostName string = communicationService.properties.hostName
output recordingStorageId string = enableRecording ? recordingStorage.id : ''
output recordingEnabled bool = enableRecording
