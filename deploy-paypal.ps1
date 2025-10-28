# Deploy PayPal Billing API Lambda Function

Write-Host "Deploying PayPal Billing API Lambda..." -ForegroundColor Cyan

# Navigate to function directory
Set-Location -Path "paypal_billing_api"

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "function.zip") {
    Remove-Item "function.zip"
}

# Zip the function
Compress-Archive -Path "index.py" -DestinationPath "function.zip"

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Yellow
aws lambda update-function-code `
    --function-name paypal_billing_api `
    --zip-file fileb://function.zip

# Wait for update to complete
Write-Host "Waiting for update to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Clean up
Remove-Item "function.zip"

# Return to root directory
Set-Location -Path ".."

Write-Host "✓ PayPal Billing API deployed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update environment variables with: .\update-paypal-env.ps1 -ClientId YOUR_ID -ClientSecret YOUR_SECRET" -ForegroundColor White
Write-Host "2. Test connection at: https://your-api-gateway-url/paypal?action=test" -ForegroundColor White
