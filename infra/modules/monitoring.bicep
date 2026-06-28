// Monitoring module: App Insights + Log Analytics
// For local, simulate; in real connects to Foundry.

param location string
param environment string

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-pantheon-${environment}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output instrumentationKey string = appInsights.properties.InstrumentationKey
