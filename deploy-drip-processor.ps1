# Deploy email-drip-processor Lambda
# Run: .\deploy-drip-processor.ps1

Write-Host "Deploying email-drip-processor Lambda..." -ForegroundColor Green

# Check if Lambda exists
$functionExists = aws lambda get-function --function-name email-drip-processor --region us-east-1 --profile ekewaka 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Updating existing Lambda..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name email-drip-processor `
        --zip-file fileb://email-drip-processor/email-drip-processor.zip `
        --region us-east-1 `
        --profile ekewaka
} else {
    Write-Host "Creating new Lambda..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name email-drip-processor `
        --runtime python3.12 `
        --role arn:aws:iam::371751795928:role/lambda-execution-role `
        --handler lambda_function.lambda_handler `
        --zip-file fileb://email-drip-processor/email-drip-processor.zip `
        --timeout 300 `
        --memory-size 256 `
        --region us-east-1 `
        --profile ekewaka
}

Write-Host "`n[SUCCESS] Lambda deployed!" -ForegroundColor Green
