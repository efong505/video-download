# Deploy Book Delivery API Lambda Function
$FunctionName = "book-delivery-api"
$Region = "us-east-1"

Write-Host "Deploying $FunctionName..." -ForegroundColor Cyan

# Create deployment package
Set-Location book_delivery_api

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
if (Test-Path package) { Remove-Item -Recurse -Force package }
mkdir package
pip install -r requirements.txt -t package --quiet

# Create ZIP with dependencies
if (Test-Path function.zip) { Remove-Item function.zip }
Copy-Item index.py package/
Set-Location package
Compress-Archive -Path * -DestinationPath ../function.zip
Set-Location ..

# Update Lambda function
aws lambda update-function-code `
    --function-name $FunctionName `
    --zip-file fileb://function.zip `
    --region $Region

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployed successfully" -ForegroundColor Green
} else {
    Write-Host "Deployment failed" -ForegroundColor Red
}

# Cleanup
Remove-Item -Recurse -Force package
Set-Location ..
