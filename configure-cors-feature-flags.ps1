# Configure CORS for API Gateway
Write-Host "Configuring CORS for API Gateway..." -ForegroundColor Cyan

$Profile = "ekewaka"
$Region = "us-east-1"
$ApiId = "0h9mj9ul9j"

# Update API to enable CORS
Write-Host "Enabling CORS on API..." -ForegroundColor Yellow
aws apigatewayv2 update-api `
    --api-id $ApiId `
    --cors-configuration "AllowOrigins=*,AllowMethods=GET,POST,PUT,DELETE,OPTIONS,AllowHeaders=Content-Type,Authorization" `
    --profile $Profile `
    --region $Region

Write-Host "[SUCCESS] CORS configured!" -ForegroundColor Green
Write-Host ""
Write-Host "Testing API endpoint..." -ForegroundColor Yellow
Write-Host "URL: https://$ApiId.execute-api.$Region.amazonaws.com/prod/feature-flags?action=list"
