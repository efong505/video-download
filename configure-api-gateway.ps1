# Configure API Gateway for Book Delivery
$ApiId = "k2zbtkeh67"
$Region = "us-east-1"
$AccountId = "371751795928"

Write-Host "Getting API Gateway resources..." -ForegroundColor Cyan

# Get root resource ID
$resources = aws apigateway get-resources --rest-api-id $ApiId --region $Region | ConvertFrom-Json
$rootResource = $resources.items | Where-Object { $_.path -eq "/" }
$ResourceId = $rootResource.id

Write-Host "Root Resource ID: $ResourceId" -ForegroundColor Green

# Add GET method
Write-Host "Adding GET method..." -ForegroundColor Cyan
aws apigateway put-method `
    --rest-api-id $ApiId `
    --resource-id $ResourceId `
    --http-method GET `
    --authorization-type NONE `
    --region $Region

# Integrate with Lambda
Write-Host "Integrating with Lambda..." -ForegroundColor Cyan
aws apigateway put-integration `
    --rest-api-id $ApiId `
    --resource-id $ResourceId `
    --http-method GET `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${Region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${Region}:${AccountId}:function:book-delivery-api/invocations" `
    --region $Region

# Add Lambda permission
Write-Host "Adding Lambda permission..." -ForegroundColor Cyan
aws lambda add-permission `
    --function-name book-delivery-api `
    --statement-id apigateway-get-access `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:${Region}:${AccountId}:${ApiId}/*/*" `
    --region $Region

# Deploy API
Write-Host "Deploying API..." -ForegroundColor Cyan
aws apigateway create-deployment `
    --rest-api-id $ApiId `
    --stage-name prod `
    --region $Region

Write-Host ""
Write-Host "API Gateway configured successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Test endpoint:" -ForegroundColor Yellow
Write-Host "https://k2zbtkeh67.execute-api.us-east-1.amazonaws.com/prod?action=generate_link&email=test@example.com&txn_id=TEST123" -ForegroundColor Cyan
