// Azure Communication Services — voice channel for contact center integration
// Billing: Per-minute (voice), per-SMS, per-recording-minute billing
// Provides: PSTN connectivity, call recording, real-time media streaming to Speech SDK

@description('Name of the Communication Services resource')
param name string

@description('Azure region (ACS is global, data location determines residency)')
param location string = 'global'

@description('Tags')
param tags object = {}

@description('Data location for compliance')
@allowed(['United States', 'Europe', 'UK', 'Australia', 'Japan', 'France', 'Germany'])
param dataLocation string = 'Europe'

resource communicationServices 'Microsoft.Communication/communicationServices@2023-06-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    dataLocation: dataLocation
  }
}

output id string = communicationServices.id
output name string = communicationServices.name
output hostName string = communicationServices.properties.hostName
output dataLocation string = communicationServices.properties.dataLocation
