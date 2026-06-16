Write-Host "Deploying email system fixes..." -ForegroundColor Cyan

# Fix 1: Deploy drip processor with Decimal timestamp fix
Write-Host "`n1. Deploying email-drip-processor..." -ForegroundColor Yellow
Set-Location "C:\Users\Ed\Documents\Programming\AWS\Downloader\email-drip-processor"

if (Test-Path "lambda.zip") { Remove-Item "lambda.zip" }
Compress-Archive -Path "lambda_function.py" -DestinationPath "lambda.zip"

aws lambda update-function-code `
    --function-name email-drip-processor `
    --zip-file fileb://lambda.zip `
    --profile ekewaka `
    --region us-east-1

Write-Host "✅ Drip processor deployed" -ForegroundColor Green

# Fix 2: Deploy email-sender (already has correct sender address)
Write-Host "`n2. Deploying email-sender..." -ForegroundColor Yellow
Set-Location "C:\Users\Ed\Documents\Programming\AWS\Downloader\email_sender"

if (Test-Path "lambda.zip") { Remove-Item "lambda.zip" }
Compress-Archive -Path "index.py" -DestinationPath "lambda.zip"

aws lambda update-function-code `
    --function-name email-sender `
    --zip-file fileb://lambda.zip `
    --profile ekewaka `
    --region us-east-1

Write-Host "✅ Email sender deployed" -ForegroundColor Green

Write-Host "`n✅ All fixes deployed!" -ForegroundColor Cyan
Write-Host "`nFixed issues:" -ForegroundColor White
Write-Host "  1. Drip processor Decimal timestamp bug (sabkab720@gmail.com will now receive emails)" -ForegroundColor White
Write-Host "  2. Email sender address (contact@christianconservativestoday.com)" -ForegroundColor White
