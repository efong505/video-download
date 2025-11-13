Write-Host "Deploying products_api Lambda..." -ForegroundColor Cyan

cd ..\products_api

# Create deployment package
Write-Host "Creating deployment package..."
Compress-Archive -Path index.py -DestinationPath function.zip -Force

# Check if function exists
$functionExists = aws lambda get-function --function-name products-api --region us-east-1 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating new Lambda function..."
    aws lambda create-function `
        --function-name products-api `
        --runtime python3.12 `
        --role arn:aws:iam::371751795928:role/lambda-dynamodb-role `
        --handler index.lambda_handler `
        --timeout 30 `
        --memory-size 512 `
        --region us-east-1 `
        --zip-file fileb://function.zip
} else {
    Write-Host "Updating existing Lambda function..."
    aws lambda update-function-code `
        --function-name products-api `
        --zip-file fileb://function.zip `
        --region us-east-1
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Lambda deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Lambda deployment failed!" -ForegroundColor Red
    Remove-Item function.zip
    cd ..\scripts
    exit 1
}

# Test
Write-Host "`nTesting Lambda..."
$payload = '{"httpMethod":"GET","queryStringParameters":{"action":"list","limit":"5"}}'
aws lambda invoke `
    --function-name products-api `
    --payload $payload `
    --region us-east-1 `
    response.json

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Lambda test successful!" -ForegroundColor Green
    Write-Host "`nResponse:"
    Get-Content response.json
    Remove-Item response.json
} else {
    Write-Host "❌ Lambda test failed!" -ForegroundColor Red
}

Remove-Item function.zip
cd ..\scripts
