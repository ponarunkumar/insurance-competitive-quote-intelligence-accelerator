// Foundry Voice Live — real-time voice agent interface
// Billing: Per-minute consumption billing for live voice interactions
// Enables: callers to interact with the quote intelligence system via natural voice
//
// This is the voice-first entry point for the contact center:
// - Caller describes their risk verbally
// - Voice Live handles turn-taking, interruption, and natural conversation
// - Integrates with the Quote Intelligence Orchestrator via A2A
// - Supports barge-in, hold music, and transfer to human advisor

@description('Name of the Voice Live resource')
param name string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags')
param tags object = {}

@description('Speech service resource ID for STT/TTS backend')
param speechServiceId string

@description('OpenAI resource ID for reasoning')
param openAIResourceId string

@description('Agent endpoint URL for orchestrator integration')
param agentEndpointUrl string = ''

// Note: Foundry Voice Live is deployed as part of the AI Foundry Agent Service
// Configuration connects the voice channel to the orchestrator agent
// The Bicep below provisions the supporting Communication Services resource

resource voiceLiveConfig 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

output id string = voiceLiveConfig.id
output name string = voiceLiveConfig.name
output endpoint string = voiceLiveConfig.properties.endpoint
output principalId string = voiceLiveConfig.identity.principalId
