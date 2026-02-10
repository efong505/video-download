# Deploy articles-api Lambda function
Write-Host "Deploying articles-api Lambda function..." -ForegroundColor Cyan

# Navigate to articles_api directory
Set-Location -Path "articles_api"

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path index.py -DestinationPath function.zip -Force

# Update Lambda function
Write-Host "Updating Lambda function code..." -ForegroundColor Yellow
aws lambda update-function-code --function-name articles-api --zip-file fileb://function.zip

# Clean up
Remove-Item function.zip

# Return to parent directory
Set-Location -Path ".."

Write-Host "Deployment complete!" -ForegroundColor Green
