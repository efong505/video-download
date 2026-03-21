# Create API Gateway for Feature Flags API
Write-Host "Creating API Gateway for Feature Flags..." -ForegroundColor Cyan

$Profile = "ekewaka"
$Region = "us-east-1"
$FunctionName = "feature-flags-api"
$FunctionArn = "arn:aws:lambda:us-east-1:371751795928:function:feature-flags-api"

# Create HTTP API
Write-Host "Creating HTTP API..." -ForegroundColor Yellow
$apiResult = aws apigatewayv2 create-api `
    --name "feature-flags-api" `
    --protocol-type HTTP `
    --profile $Profile `
    --region $Region | ConvertFrom-Json

$ApiId = $apiResult.ApiId
$ApiEndpoint = $apiResult.ApiEndpoint

Write-Host "[SUCCESS] API Created: $ApiId" -ForegroundColor Green
Write-Host "API Endpoint: $ApiEndpoint" -ForegroundColor Cyan

# Create integration
Write-Host "Creating Lambda integration..." -ForegroundColor Yellow
$integrationResult = aws apigatewayv2 create-integration `
    --api-id $ApiId `
    --integration-type AWS_PROXY `
    --integration-uri $FunctionArn `
    --payload-format-version "2.0" `
    --profile $Profile `
    --region $Region | ConvertFrom-Json

$IntegrationId = $integrationResult.IntegrationId
Write-Host "[SUCCESS] Integration Created: $IntegrationId" -ForegroundColor Green

# Create routes
Write-Host "Creating routes..." -ForegroundColor Yellow

# GET route
aws apigatewayv2 create-route `
    --api-id $ApiId `
    --route-key "GET /feature-flags" `
    --target "integrations/$IntegrationId" `
    --profile $Profile `
    --region $Region | Out-Null

# POST route
aws apigatewayv2 create-route `
    --api-id $ApiId `
    --route-key "POST /feature-flags" `
    --target "integrations/$IntegrationId" `
    --profile $Profile `
    --region $Region | Out-Null

# PUT route
aws apigatewayv2 create-route `
    --api-id $ApiId `
    --route-key "PUT /feature-flags" `
    --target "integrations/$IntegrationId" `
    --profile $Profile `
    --region $Region | Out-Null

# DELETE route
aws apigatewayv2 create-route `
    --api-id $ApiId `
    --route-key "DELETE /feature-flags" `
    --target "integrations/$IntegrationId" `
    --profile $Profile `
    --region $Region | Out-Null

# OPTIONS route for CORS
aws apigatewayv2 create-route `
    --api-id $ApiId `
    --route-key "OPTIONS /feature-flags" `
    --target "integrations/$IntegrationId" `
    --profile $Profile `
    --region $Region | Out-Null

Write-Host "[SUCCESS] Routes created" -ForegroundColor Green

# Create stage
Write-Host "Creating prod stage..." -ForegroundColor Yellow
aws apigatewayv2 create-stage `
    --api-id $ApiId `
    --stage-name "prod" `
    --auto-deploy `
    --profile $Profile `
    --region $Region | Out-Null

Write-Host "[SUCCESS] Stage created" -ForegroundColor Green

# Grant Lambda permission
Write-Host "Granting Lambda invoke permission..." -ForegroundColor Yellow
aws lambda add-permission `
    --function-name $FunctionName `
    --statement-id apigateway-invoke `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:$Region:371751795928:$ApiId/*/*/feature-flags" `
    --profile $Profile `
    --region $Region | Out-Null

Write-Host "[SUCCESS] Permission granted" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "API Gateway Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "API Endpoint URL:" -ForegroundColor Cyan
Write-Host "$ApiEndpoint/prod/feature-flags" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update feature-flags.js with this URL:"
Write-Host "   API_URL: '$ApiEndpoint/prod/feature-flags'"
Write-Host ""
Write-Host "2. Update admin-feature-flags.html with this URL:"
Write-Host "   const FEATURE_FLAGS_API = '$ApiEndpoint/prod/feature-flags';"
Write-Host ""
Write-Host "3. Test the API:"
Write-Host "   curl $ApiEndpoint/prod/feature-flags?action=list"
Write-Host ""
