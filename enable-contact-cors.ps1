# Enable CORS for Contact Endpoint
$ApiId = "k2zbtkeh67"
$Region = "us-east-1"
$ContactId = "xe9zph"

Write-Host "Adding OPTIONS method..." -ForegroundColor Cyan
aws apigateway put-method `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method OPTIONS `
    --authorization-type NONE `
    --region $Region

Write-Host "Adding mock integration..." -ForegroundColor Cyan
aws apigateway put-integration `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method OPTIONS `
    --type MOCK `
    --request-templates '{"application/json": "{\"statusCode\": 200}"}' `
    --region $Region

Write-Host "Adding method response..." -ForegroundColor Cyan
aws apigateway put-method-response `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method OPTIONS `
    --status-code 200 `
    --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false" `
    --region $Region

Write-Host "Adding integration response..." -ForegroundColor Cyan
aws apigateway put-integration-response `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method OPTIONS `
    --status-code 200 `
    --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":\"'"'"'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"'"'\",\"method.response.header.Access-Control-Allow-Methods\":\"'"'"'POST,OPTIONS'"'"'\",\"method.response.header.Access-Control-Allow-Origin\":\"'"'"'*'"'"'\"}' `
    --region $Region

Write-Host "Deploying API..." -ForegroundColor Cyan
aws apigateway create-deployment `
    --rest-api-id $ApiId `
    --stage-name prod `
    --region $Region

Write-Host ""
Write-Host "CORS enabled!" -ForegroundColor Green
