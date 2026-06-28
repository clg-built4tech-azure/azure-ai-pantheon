// Foundry project stub
// In real, deploys models etc. For local sim.

param location string
param environment string

output foundryEndpoint string = 'https://sim-foundry-${environment}.services.ai.azure.com'
