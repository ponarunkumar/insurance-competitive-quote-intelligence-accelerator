// Speaker Diarization configuration for contact center call processing
// Billing: Included in Speech-to-Text per-audio-hour billing (value-add feature)
// Used by: Call Analytics Agent — distinguishes advisor vs. customer in transcripts
//
// Capabilities:
// - Real-time diarization during live calls
// - Batch diarization for recorded calls
// - Speaker identification (match against enrolled advisor voiceprints)
// - Speaker count estimation for conference calls

@description('Name of the Speech service (parent)')
param speechServiceName string

@description('Maximum number of speakers to identify')
param maxSpeakers int = 4

@description('Enable speaker identification (voiceprint enrollment)')
param enableSpeakerIdentification bool = true

@description('Enable speaker verification')
param enableSpeakerVerification bool = false

resource speechService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: speechServiceName
}

output speechServiceEndpoint string = speechService.properties.endpoint
output maxSpeakers int = maxSpeakers
output speakerIdentificationEnabled bool = enableSpeakerIdentification
output speakerVerificationEnabled bool = enableSpeakerVerification
