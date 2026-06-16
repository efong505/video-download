# Deploy All Lambda Functions
Write-Host "Deploying Storage Subscription Service Lambda Functions..." -ForegroundColor Green

$lambdas = @("auth_api", "storage_api", "subscription_api", "admin_api")

foreach ($lambda in $lambdas) {
    Write-Host "`nDeploying $lambda..." -ForegroundColor Cyan
    
    # Navigate to lambda directory
    Set-Location "..\lambda\$lambda"
    
    # Install dependencies if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt -t .
    }
    
    # Create deployment package
    Write-Host "Creating deployment package..." -ForegroundColor Yellow
    if (Test-Path "function.zip") {
        Remove-Item "function.zip"
    }
    Compress-Archive -Path * -DestinationPath function.zip
    
    # Update Lambda function
    Write-Host "Updating Lambda function..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name $lambda `
        --zip-file fileb://function.zip
    
    # Clean up
    Remove-Item "function.zip"
    
    Write-Host "$lambda deployed successfully!" -ForegroundColor Green
}

Set-Location "..\..\scripts"
Write-Host "`nAll Lambda functions deployed successfully!" -ForegroundColor Green
