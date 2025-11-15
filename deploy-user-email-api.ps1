# Deploy user-email-api Lambda function
Write-Host "Deploying user-email-api Lambda function..." -ForegroundColor Cyan

Set-Location -Path "user_email_api"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -t .

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path * -DestinationPath function.zip -Force

# Update Lambda function
Write-Host "Updating Lambda function code..." -ForegroundColor Yellow
aws lambda update-function-code `
    --function-name user-email-api `
    --zip-file fileb://function.zip `
    --region us-east-1

Start-Sleep -Seconds 5

# Clean up
Remove-Item function.zip

Set-Location -Path ".."

Write-Host "✅ user-email-api deployment complete!" -ForegroundColor Green
