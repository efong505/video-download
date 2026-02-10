# Deploy Prayer API Lambda Function

Write-Host "Deploying Prayer API Lambda..." -ForegroundColor Cyan

# Navigate to prayer_api directory
Set-Location -Path "prayer_api"

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "function.zip") { Remove-Item "function.zip" }
Compress-Archive -Path "index.py" -DestinationPath "function.zip"

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Yellow
aws lambda update-function-code `
    --function-name prayer_api `
    --zip-file fileb://function.zip

# Wait for update to complete
Write-Host "Waiting for update to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Update function configuration
Write-Host "Updating function configuration..." -ForegroundColor Yellow
aws lambda update-function-configuration `
    --function-name prayer_api `
    --timeout 30 `
    --memory-size 512

Write-Host "Prayer API deployed successfully!" -ForegroundColor Green

# Return to parent directory
Set-Location -Path ".."
