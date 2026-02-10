# Fix API Gateway Responses
$ApiId = "k2zbtkeh67"
$Region = "us-east-1"
$ResourceId = "7rytxy6m1a"

Write-Host "Adding method response..." -ForegroundColor Cyan
aws apigateway put-method-response `
    --rest-api-id $ApiId `
    --resource-id $ResourceId `
    --http-method GET `
    --status-code 200 `
    --region $Region

Write-Host "Adding integration response..." -ForegroundColor Cyan
aws apigateway put-integration-response `
    --rest-api-id $ApiId `
    --resource-id $ResourceId `
    --http-method GET `
    --status-code 200 `
    --region $Region

Write-Host "Deploying API..." -ForegroundColor Cyan
aws apigateway create-deployment `
    --rest-api-id $ApiId `
    --stage-name prod `
    --region $Region

Write-Host ""
Write-Host "API Gateway fixed!" -ForegroundColor Green
