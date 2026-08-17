// Text-to-Speech configuration for advisor readback and voice responses
// Billing: Per-1M characters billing (Neural TTS)
// Used by: Voice Response Agent (read back recommendations), Advisor Explanation Agent (audio summaries)
//
// Capabilities enabled:
// - Neural TTS with natural-sounding voices
// - Custom Neural Voice (optional — for branded carrier voice)
// - SSML support for emphasis, pauses, and pronunciation of insurance terms
// - Real-time streaming for low-latency voice responses

@description('Name of the Speech service (parent)')
param speechServiceName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Default voice for TTS output')
param defaultVoice string = 'en-GB-SoniaNeural'

@description('Additional voices available')
param additionalVoices array = [
  'en-GB-RyanNeural'
  'en-US-JennyNeural'
  'en-US-GuyNeural'
]

@description('Enable Custom Neural Voice training')
param enableCustomVoice bool = false

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: speechServiceName
}

// Storage for Custom Neural Voice training data (if enabled)
resource voiceTrainingStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = if (enableCustomVoice) {
  name: '${replace(speechServiceName, '-', '')}tts'
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

output speechServiceEndpoint string = speechService.properties.endpoint
output defaultVoice string = defaultVoice
output availableVoices array = union([defaultVoice], additionalVoices)
output customVoiceEnabled bool = enableCustomVoice
