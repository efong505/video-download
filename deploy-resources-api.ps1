# Deploy resources-api Lambda function
Write-Host "Deploying resources-api Lambda function..." -ForegroundColor Cyan

# Navigate to resources_api directory
Set-Location -Path "resources_api"

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path index.py -DestinationPath function.zip -Force

# Update Lambda function
Write-Host "Updating Lambda function code..." -ForegroundColor Yellow
aws lambda update-function-code `
    --function-name resources-api `
    --zip-file fileb://function.zip `
    --region us-east-1

# Wait for update to complete
Write-Host "Waiting for function update to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Clean up
Remove-Item function.zip

# Return to root directory
Set-Location -Path ".."

Write-Host "✅ resources-api deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Testing the function..." -ForegroundColor Cyan
aws lambda invoke `
    --function-name resources-api `
    --payload '{"queryStringParameters":{"action":"list"}}' `
    --region us-east-1 `
    response.json

Write-Host ""
Write-Host "Response:" -ForegroundColor Yellow
Get-Content response.json
Remove-Item response.json

Write-Host ""
Write-Host "Deployment complete! Multiple categories feature is now live." -ForegroundColor Green
