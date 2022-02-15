$apiKey = "Token ADD-YOUR-API-TOKEN"

$resource = "https://uptime.com/api/v1/checks/123456/maintenance/"

$Body = @{
    state = "SUPPRESSED"
} | convertto-json

$Check = Invoke-RestMethod `
    -Headers @{
        "Authorization" = $apiKey
        "Content-Type" = "application/json"
    }`
    -Method PATCH `
    -Body $Body `
    -Uri $resource
