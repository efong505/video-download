# Deploy Lambda Function to AWS

$functionName = "email-subscription-handler"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying Lambda Function" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "lambda_deployment.zip") {
    Remove-Item "lambda_deployment.zip"
}

Compress-Archive -Path "lambda_function.py" -DestinationPath "lambda_deployment.zip"

# Deploy to AWS
Write-Host "Uploading to AWS Lambda..." -ForegroundColor Yellow
aws lambda update-function-code --function-name $functionName --zip-file fileb://lambda_deployment.zip

Write-Host ""
Write-Host "Waiting for update to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Verify deployment
Write-Host "Verifying deployment..." -ForegroundColor Yellow
$result = aws lambda get-function --function-name $functionName --query "Configuration.LastModified" --output text

if ($result) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Lambda function updated successfully!" -ForegroundColor Green
    Write-Host "Last modified: $result" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "New features available:" -ForegroundColor Cyan
    Write-Host "  - Unsubscribe endpoint (/unsubscribe)" -ForegroundColor White
    Write-Host "  - Enhanced error handling" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Warning: Could not verify deployment" -ForegroundColor Yellow
    Write-Host ""
}

# Cleanup
Remove-Item "lambda_deployment.zip" -ErrorAction SilentlyContinue

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host ""
