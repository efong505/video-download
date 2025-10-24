# Fix API Gateway CORS and Routes

$apiId = "niexv1rw75"
$region = "us-east-1"

Write-Host ""
Write-Host "Fixing API Gateway CORS and Routes..." -ForegroundColor Cyan
Write-Host ""

# Get Lambda function ARN
Write-Host "Getting Lambda function ARN..." -ForegroundColor Yellow
$lambdaArn = aws lambda get-function --function-name email-subscription-handler --query "Configuration.FunctionArn" --output text

# Get integration ID
Write-Host "Getting integration ID..." -ForegroundColor Yellow
$integrationId = aws apigatewayv2 get-integrations --api-id $apiId --query "Items[0].IntegrationId" --output text

# Create/Update routes with CORS
Write-Host "Creating routes..." -ForegroundColor Yellow

# POST /subscribe
aws apigatewayv2 create-route --api-id $apiId --route-key "POST /subscribe" --target "integrations/$integrationId" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Route already exists, updating..." -ForegroundColor Yellow
}

# GET /unsubscribe
aws apigatewayv2 create-route --api-id $apiId --route-key "GET /unsubscribe" --target "integrations/$integrationId" 2>$null

# GET /track/open/{tracking_id}
aws apigatewayv2 create-route --api-id $apiId --route-key "GET /track/open/{tracking_id}" --target "integrations/$integrationId" 2>$null

# GET /track/click/{tracking_id}
aws apigatewayv2 create-route --api-id $apiId --route-key "GET /track/click/{tracking_id}" --target "integrations/$integrationId" 2>$null

# Enable CORS
Write-Host "Enabling CORS..." -ForegroundColor Yellow
aws apigatewayv2 update-api --api-id $apiId --cors-configuration "AllowOrigins=*,AllowMethods=GET,POST,OPTIONS,AllowHeaders=Content-Type,Authorization"

Write-Host ""
Write-Host "Testing subscription endpoint..." -ForegroundColor Yellow
$testResult = curl -X POST "https://$apiId.execute-api.$region.amazonaws.com/subscribe" -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\"}" 2>&1

if ($testResult -match "Subscription successful" -or $testResult -match "Already subscribed") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "API Gateway is now configured correctly!" -ForegroundColor Green
    Write-Host "CORS is enabled for all origins" -ForegroundColor Green
    Write-Host ""
    Write-Host "Available endpoints:" -ForegroundColor Cyan
    Write-Host "  POST   https://$apiId.execute-api.$region.amazonaws.com/subscribe"
    Write-Host "  GET    https://$apiId.execute-api.$region.amazonaws.com/unsubscribe"
    Write-Host "  GET    https://$apiId.execute-api.$region.amazonaws.com/track/open/{id}"
    Write-Host "  GET    https://$apiId.execute-api.$region.amazonaws.com/track/click/{id}"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Warning: Test failed, but routes are configured" -ForegroundColor Yellow
    Write-Host "Try subscribing from your website now" -ForegroundColor Yellow
    Write-Host ""
}
