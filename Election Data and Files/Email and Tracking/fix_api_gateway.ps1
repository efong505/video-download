# API Gateway Diagnostic and Fix Script
# Run this to check and fix your API Gateway configuration

$apiId = "niexv1rw75"
$region = "us-east-1"
$functionName = "email-subscription-handler"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API Gateway Diagnostic Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if API exists
Write-Host "[1/6] Checking API Gateway..." -ForegroundColor Yellow
try {
    $api = Get-AG2Api -ApiId $apiId -Region $region
    Write-Host "✓ API found: $($api.Name)" -ForegroundColor Green
} catch {
    Write-Host "✗ API not found!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit
}

# Step 2: Check Lambda function
Write-Host "[2/6] Checking Lambda function..." -ForegroundColor Yellow
try {
    $lambda = Get-LMFunction -FunctionName $functionName -Region $region
    Write-Host "✓ Lambda function found" -ForegroundColor Green
    $lambdaArn = $lambda.FunctionArn
    Write-Host "  ARN: $lambdaArn" -ForegroundColor Gray
} catch {
    Write-Host "✗ Lambda function not found!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit
}

# Step 3: Check existing routes
Write-Host "[3/6] Checking existing routes..." -ForegroundColor Yellow
$routes = Get-AG2RouteList -ApiId $apiId -Region $region

if ($routes.Count -eq 0) {
    Write-Host "✗ No routes found!" -ForegroundColor Red
} else {
    Write-Host "✓ Found $($routes.Count) route(s):" -ForegroundColor Green
    foreach ($route in $routes) {
        Write-Host "  - $($route.RouteKey)" -ForegroundColor Gray
    }
}

# Check if POST /subscribe exists
$subscribeRoute = $routes | Where-Object { $_.RouteKey -eq "POST /subscribe" }

# Step 4: Check integrations
Write-Host "[4/6] Checking integrations..." -ForegroundColor Yellow
$integrations = Get-AG2IntegrationList -ApiId $apiId -Region $region

if ($integrations.Count -eq 0) {
    Write-Host "✗ No integrations found! Creating one..." -ForegroundColor Yellow
    
    # Create integration
    $integration = New-AG2Integration `
        -ApiId $apiId `
        -IntegrationType AWS_PROXY `
        -IntegrationUri $lambdaArn `
        -PayloadFormatVersion "2.0" `
        -Region $region
    
    $integrationId = $integration.IntegrationId
    Write-Host "✓ Integration created: $integrationId" -ForegroundColor Green
} else {
    $integrationId = $integrations[0].IntegrationId
    Write-Host "✓ Integration found: $integrationId" -ForegroundColor Green
}

# Step 5: Create/Fix routes
Write-Host "[5/6] Setting up routes..." -ForegroundColor Yellow

$routesToCreate = @(
    "POST /subscribe",
    "GET /track/open/{tracking_id}",
    "GET /track/click/{tracking_id}",
    "OPTIONS /{proxy+}"
)

foreach ($routeKey in $routesToCreate) {
    $existingRoute = $routes | Where-Object { $_.RouteKey -eq $routeKey }
    
    if ($existingRoute) {
        Write-Host "  ✓ Route exists: $routeKey" -ForegroundColor Gray
    } else {
        try {
            New-AG2Route `
                -ApiId $apiId `
                -RouteKey $routeKey `
                -Target "integrations/$integrationId" `
                -Region $region | Out-Null
            Write-Host "  ✓ Created route: $routeKey" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Failed to create route: $routeKey" -ForegroundColor Red
            Write-Host "    Error: $_" -ForegroundColor Red
        }
    }
}

# Step 6: Grant Lambda permissions
Write-Host "[6/6] Checking Lambda permissions..." -ForegroundColor Yellow

$accountId = $lambdaArn.Split(':')[4]
$sourceArn = "arn:aws:execute-api:${region}:${accountId}:${apiId}/*/*"

try {
    # Try to add permission (will fail if already exists, which is fine)
    Add-LMPermission `
        -FunctionName $functionName `
        -StatementId "apigateway-invoke-$(Get-Random -Maximum 99999)" `
        -Action "lambda:InvokeFunction" `
        -Principal "apigateway.amazonaws.com" `
        -SourceArn $sourceArn `
        -Region $region `
        -ErrorAction SilentlyContinue | Out-Null
    Write-Host "✓ Lambda permissions configured" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -like "*already exists*") {
        Write-Host "✓ Lambda permissions already exist" -ForegroundColor Green
    } else {
        Write-Host "⚠ Warning: Could not verify permissions" -ForegroundColor Yellow
        Write-Host "  This might be okay if permissions already exist" -ForegroundColor Gray
    }
}

# Final test
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing API..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$testUrl = "https://${apiId}.execute-api.${region}.amazonaws.com/subscribe"
Write-Host "Test URL: $testUrl" -ForegroundColor Gray

try {
    $testBody = @{email = "test@example.com"} | ConvertTo-Json
    $response = Invoke-RestMethod `
        -Uri $testUrl `
        -Method POST `
        -Body $testBody `
        -ContentType "application/json" `
        -ErrorAction Stop
    
    Write-Host ""
    Write-Host "✓ SUCCESS! API is working!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "✗ API test failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Check Lambda CloudWatch logs for errors" -ForegroundColor Gray
    Write-Host "2. Verify DynamoDB tables exist (email-subscribers, email-events)" -ForegroundColor Gray
    Write-Host "3. Verify SES email is verified" -ForegroundColor Gray
    Write-Host "4. Check Lambda has DynamoDB and SES permissions" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Diagnostic Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
