# Deploy email_subscribers_api Lambda function

Write-Host "Deploying email_subscribers_api..." -ForegroundColor Cyan

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "function.zip") { Remove-Item "function.zip" }
Compress-Archive -Path "index.py" -DestinationPath "function.zip"

# Update Lambda function
Write-Host "Updating Lambda function..." -ForegroundColor Yellow
aws lambda update-function-code `
    --function-name email_subscribers_api `
    --zip-file fileb://function.zip

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
    exit 1
}

# Wait for update to complete
Write-Host "Waiting for update to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test the function
Write-Host "Testing function..." -ForegroundColor Yellow
$testPayload = @{
    body = @{
        action = "list"
        status = "active"
        limit = 10
    } | ConvertTo-Json
} | ConvertTo-Json

$testPayload | Out-File -FilePath "test-payload.json" -Encoding utf8
aws lambda invoke --function-name email_subscribers_api --payload file://test-payload.json response.json

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Test successful!" -ForegroundColor Green
    Get-Content response.json
} else {
    Write-Host "✗ Test failed!" -ForegroundColor Red
}

# Cleanup
Remove-Item "test-payload.json" -ErrorAction SilentlyContinue
Remove-Item "response.json" -ErrorAction SilentlyContinue

Write-Host "`nDeployment complete!" -ForegroundColor Cyan
