# Deploy News API Lambda Function
Write-Host "Deploying News API Lambda Function..." -ForegroundColor Yellow

# Navigate to news_api directory
Set-Location news_api

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Cyan
if (Test-Path "news-deployment.zip") {
    Remove-Item "news-deployment.zip"
}
Compress-Archive -Path index.py,jwt,PyJWT-2.10.1.dist-info -DestinationPath news-deployment.zip -Force

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Cyan
aws lambda update-function-code --function-name news-api --zip-file fileb://news-deployment.zip

# Return to parent directory
Set-Location ..

Write-Host "✅ News API deployment complete!" -ForegroundColor Green
