$apiKey = "token ADD-YOUR-API-TOKEN"

$resource = "https://uptime.com/api/v1/checks/add-http/"

$Body = @{
  name = "My HTTP Check"
  msp_interval = 5
  msp_address = "https://mywebsite.com"
  locations = "US-East", "US-West", "GBR"
  contact_groups = @("Default")
} | convertto-json

$Check = Invoke-RestMethod `
    -Headers @{
        "Authorization" = $apiKey
        "Content-Type" = "application/json"
    }`
    -Method POST `
    -Body $Body `
    -Uri $resource
