// Speech-to-Text configuration for real-time and batch transcription
// Billing: Per-audio-hour billing (real-time and batch)
// Used by: Voice Intake Agent (live call transcription), Call Analytics Agent (batch processing)
//
// Capabilities enabled:
// - Real-time transcription (streaming) for live advisor calls
// - Batch transcription for historical call recordings
// - Continuous language identification for multi-language calls
// - Word-level timestamps for compliance and quality review

@description('Name of the Speech service (parent)')
param speechServiceName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Default language for recognition')
param defaultLanguage string = 'en-GB'

@description('Additional languages for auto-detection')
param additionalLanguages array = ['en-US', 'fr-FR', 'de-DE', 'es-ES']

@description('Enable real-time transcription')
param enableRealtime bool = true

@description('Enable batch transcription')
param enableBatch bool = true

// Speech-to-Text endpoint configuration
// Note: STT capabilities are part of the parent Speech Services account
// This module documents the configuration and outputs for consumer services

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: speechServiceName
}

// Storage account for batch transcription results
resource transcriptionStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = if (enableBatch) {
  name: '${replace(speechServiceName, '-', '')}stt'
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

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = if (enableBatch) {
  parent: transcriptionStorage
  name: 'default'
}

resource transcriptionContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = if (enableBatch) {
  parent: blobService
  name: 'transcriptions'
  properties: {
    publicAccess: 'None'
  }
}

output speechServiceEndpoint string = speechService.properties.endpoint
output defaultLanguage string = defaultLanguage
output supportedLanguages array = union([defaultLanguage], additionalLanguages)
output transcriptionStorageId string = enableBatch ? transcriptionStorage.id : ''
output realtimeEnabled bool = enableRealtime
output batchEnabled bool = enableBatch
