# Test PayPal Lambda Function

Write-Host "Testing PayPal Lambda Function..." -ForegroundColor Cyan
Write-Host ""

# Get API Gateway URL for paypal-billing-api
Write-Host "Getting API Gateway URL..." -ForegroundColor Yellow
$functionConfig = aws lambda get-function --function-name paypal-billing-api | ConvertFrom-Json

# Get the function URL or API Gateway endpoint
$apiUrl = $null

# Try to get function URL first
try {
    $functionUrl = aws lambda get-function-url-config --function-name paypal-billing-api 2>$null | ConvertFrom-Json
    if ($functionUrl.FunctionUrl) {
        $apiUrl = $functionUrl.FunctionUrl.TrimEnd('/') + "?action=test"
    }
} catch {
    # Function URL not configured
}

# If no function URL, need to use API Gateway
if (-not $apiUrl) {
    Write-Host "No Function URL found. Checking API Gateway..." -ForegroundColor Yellow
    
    # List API Gateways
    $apis = aws apigatewayv2 get-apis | ConvertFrom-Json
    
    foreach ($api in $apis.Items) {
        if ($api.Name -like "*paypal*" -or $api.Name -like "*billing*") {
            $apiUrl = "$($api.ApiEndpoint)/paypal?action=test"
            break
        }
    }
}

if (-not $apiUrl) {
    Write-Host "Could not find API Gateway URL automatically." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please invoke Lambda directly:" -ForegroundColor Yellow
    Write-Host 'aws lambda invoke --function-name paypal-billing-api --payload ''{"queryStringParameters":{"action":"test"}}'' response.json' -ForegroundColor White
    Write-Host 'type response.json' -ForegroundColor White
    exit
}

Write-Host "API URL: $apiUrl" -ForegroundColor Green
Write-Host ""

# Test the endpoint
Write-Host "Calling test endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Get
    
    Write-Host ""
    Write-Host "✓ Test successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 5 | Write-Host
    
    # Check environment
    if ($response.environment -eq "LIVE") {
        Write-Host ""
        Write-Host "✓ PayPal is configured for LIVE production mode" -ForegroundColor Green
    } elseif ($response.environment -eq "SANDBOX") {
        Write-Host ""
        Write-Host "⚠ PayPal is still in SANDBOX mode" -ForegroundColor Yellow
        Write-Host "Run: .\update-paypal-env.ps1 -ClientId YOUR_ID -ClientSecret YOUR_SECRET" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "⚠ PayPal credentials not configured" -ForegroundColor Yellow
        Write-Host "Run: .\update-paypal-env.ps1 -ClientId YOUR_ID -ClientSecret YOUR_SECRET" -ForegroundColor White
    }
    
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying direct Lambda invoke..." -ForegroundColor Yellow
    
    # Try direct invoke
    $payload = '{"queryStringParameters":{"action":"test"}}'
    aws lambda invoke --function-name paypal-billing-api --payload $payload response.json
    
    if (Test-Path "response.json") {
        Write-Host ""
        Write-Host "Lambda Response:" -ForegroundColor Cyan
        Get-Content "response.json" | ConvertFrom-Json | ConvertTo-Json -Depth 5 | Write-Host
        Remove-Item "response.json"
    }
}
