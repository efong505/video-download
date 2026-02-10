# Deploy articles-api Lambda with dependencies
Write-Host "Deploying articles-api with requests library..." -ForegroundColor Cyan

Set-Location -Path "articles_api"

# Create deployment package with all dependencies
Write-Host "Creating deployment package with dependencies..." -ForegroundColor Yellow
Compress-Archive -Path index.py,requests,urllib3,certifi,charset_normalizer,idna,bin -DestinationPath deployment.zip -Force

# Update Lambda function
Write-Host "Updating Lambda function code..." -ForegroundColor Yellow
aws lambda update-function-code --function-name articles-api --zip-file fileb://deployment.zip

Set-Location -Path ".."
Write-Host "Deployment complete! Scripture lookup should now work." -ForegroundColor Green
