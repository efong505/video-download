# Configure API Gateway for Contact Form
$ApiId = "k2zbtkeh67"
$Region = "us-east-1"
$AccountId = "371751795928"

Write-Host "Getting root resource..." -ForegroundColor Cyan
$resources = aws apigateway get-resources --rest-api-id $ApiId --region $Region | ConvertFrom-Json
$rootResource = $resources.items | Where-Object { $_.path -eq "/" }
$RootId = $rootResource.id
Write-Host "Root ID: $RootId" -ForegroundColor Green

Write-Host "Creating /contact resource..." -ForegroundColor Cyan
try {
    $contactResource = aws apigateway create-resource `
        --rest-api-id $ApiId `
        --parent-id $RootId `
        --path-part contact `
        --region $Region 2>&1 | ConvertFrom-Json
    $ContactId = $contactResource.id
} catch {
    Write-Host "Resource may already exist, getting it..." -ForegroundColor Yellow
    $contactResource = $resources.items | Where-Object { $_.path -eq "/contact" }
    $ContactId = $contactResource.id
}
Write-Host "Contact ID: $ContactId" -ForegroundColor Green

Write-Host "Adding POST method..." -ForegroundColor Cyan
aws apigateway put-method `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method POST `
    --authorization-type NONE `
    --region $Region

Write-Host "Integrating with Lambda..." -ForegroundColor Cyan
aws apigateway put-integration `
    --rest-api-id $ApiId `
    --resource-id $ContactId `
    --http-method POST `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${Region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${Region}:${AccountId}:function:contact-form-api/invocations" `
    --region $Region

Write-Host "Adding Lambda permission..." -ForegroundColor Cyan
aws lambda add-permission `
    --function-name contact-form-api `
    --statement-id apigateway-contact-access `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:${Region}:${AccountId}:${ApiId}/*/*" `
    --region $Region 2>$null

Write-Host "Deploying API..." -ForegroundColor Cyan
aws apigateway create-deployment `
    --rest-api-id $ApiId `
    --stage-name prod `
    --region $Region

Write-Host ""
Write-Host "Contact form API configured!" -ForegroundColor Green
Write-Host "Endpoint: https://k2zbtkeh67.execute-api.us-east-1.amazonaws.com/prod/contact" -ForegroundColor Cyan
