# Deploy email_sender Lambda function

Write-Host "Deploying email_sender..." -ForegroundColor Cyan

if (Test-Path "function.zip") { Remove-Item "function.zip" }
Compress-Archive -Path "index.py" -DestinationPath "function.zip"

aws lambda update-function-code `
    --function-name email_sender `
    --zip-file fileb://function.zip

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
}
