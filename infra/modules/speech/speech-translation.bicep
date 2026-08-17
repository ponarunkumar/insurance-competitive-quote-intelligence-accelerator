// Speech Translation for multi-language contact center support
// Billing: Per-audio-hour billing for real-time translation
// Used by: Voice Intake Agent (translate non-English callers), Advisor Explanation Agent (multi-language output)
//
// Capabilities:
// - Real-time speech-to-speech translation
// - Speech-to-text translation (transcribe + translate simultaneously)
// - Support for 70+ languages
// - Insurance terminology preservation across translations

@description('Name of the Speech service (parent)')
param speechServiceName string

@description('Source languages for translation')
param sourceLanguages array = ['en-GB', 'en-US', 'fr-FR', 'de-DE', 'es-ES', 'it-IT', 'pt-PT', 'nl-NL']

@description('Target languages for translation output')
param targetLanguages array = ['en-GB', 'fr-FR', 'de-DE', 'es-ES']

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: speechServiceName
}

output speechServiceEndpoint string = speechService.properties.endpoint
output sourceLanguages array = sourceLanguages
output targetLanguages array = targetLanguages
output translationEnabled bool = true
