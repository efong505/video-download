# Deploy news_api Lambda function
Write-Host "Deploying news_api Lambda function..." -ForegroundColor Cyan

# Navigate to news_api directory
Set-Location -Path "news_api"

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path "index.py" -DestinationPath "news-api.zip" -Force

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Yellow
aws lambda update-function-code --function-name news-api --zip-file fileb://news-api.zip

# Clean up
Remove-Item "news-api.zip"

# Return to parent directory
Set-Location -Path ".."

Write-Host "news_api deployment complete!" -ForegroundColor Green
