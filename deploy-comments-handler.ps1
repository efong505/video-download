# Deploy Comments Handler Lambda
Write-Host "Deploying Comments Handler Lambda..." -ForegroundColor Cyan

# Navigate to comments-handler directory
Set-Location comments-handler

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "lambda.zip") {
    Remove-Item "lambda.zip"
}
Compress-Archive -Path lambda_function.py -DestinationPath lambda.zip

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Yellow
aws lambda update-function-code --function-name comments-api --zip-file fileb://lambda.zip --region us-east-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Comments Handler deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Return to root directory
Set-Location ..

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Email notifications for comment replies are now active." -ForegroundColor Cyan
