# Deploy email_tracking_api Lambda function

Write-Host "Deploying email_tracking_api..." -ForegroundColor Cyan

if (Test-Path "function.zip") { Remove-Item "function.zip" }
Compress-Archive -Path "index.py" -DestinationPath "function.zip"

aws lambda update-function-code `
    --function-name email_tracking_api `
    --zip-file fileb://function.zip

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
}
