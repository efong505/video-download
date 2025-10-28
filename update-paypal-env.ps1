# Update PayPal Lambda Environment Variables
# This script updates the PayPal billing API Lambda function with live credentials

param(
    [Parameter(Mandatory=$true)]
    [string]$ClientId,
    
    [Parameter(Mandatory=$true)]
    [string]$ClientSecret,
    
    [Parameter(Mandatory=$false)]
    [string]$BaseUrl = "https://api-m.paypal.com"
)

Write-Host "Updating PayPal Lambda environment variables..." -ForegroundColor Cyan

# Update Lambda function configuration
$envVars = @{
    PAYPAL_CLIENT_ID = $ClientId
    PAYPAL_CLIENT_SECRET = $ClientSecret
    PAYPAL_BASE_URL = $BaseUrl
}

$envJson = $envVars | ConvertTo-Json -Compress

try {
    aws lambda update-function-configuration `
        --function-name paypal_billing_api `
        --environment "Variables={PAYPAL_CLIENT_ID=$ClientId,PAYPAL_CLIENT_SECRET=$ClientSecret,PAYPAL_BASE_URL=$BaseUrl}"
    
    Write-Host "✓ Environment variables updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration:" -ForegroundColor Yellow
    Write-Host "  Client ID: $($ClientId.Substring(0, 10))..." -ForegroundColor White
    Write-Host "  Base URL: $BaseUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Testing connection..." -ForegroundColor Cyan
    
    # Get API Gateway URL
    $apiUrl = "https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod/paypal?action=test"
    Write-Host "Test manually at: $apiUrl" -ForegroundColor Yellow
    
} catch {
    Write-Host "✗ Error updating environment variables: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the connection using the test endpoint" -ForegroundColor White
Write-Host "2. Create a test subscription" -ForegroundColor White
Write-Host "3. Verify webhook configuration in PayPal dashboard" -ForegroundColor White
