# Deploy Contact Form API
$FunctionName = "contact-form-api"
$Region = "us-east-1"

Write-Host "Deploying $FunctionName..." -ForegroundColor Cyan

Set-Location contact_form_api
if (Test-Path function.zip) { Remove-Item function.zip }
Compress-Archive -Path index.py -DestinationPath function.zip

aws lambda update-function-code `
    --function-name $FunctionName `
    --zip-file fileb://function.zip `
    --region $Region

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployed successfully" -ForegroundColor Green
} else {
    Write-Host "Creating new function..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name $FunctionName `
        --runtime python3.12 `
        --role arn:aws:iam::371751795928:role/lambda-execution-role `
        --handler index.lambda_handler `
        --zip-file fileb://function.zip `
        --timeout 30 `
        --region $Region
}

Set-Location ..
Write-Host ""
Write-Host "API Endpoint: https://niexv1rw75.execute-api.us-east-1.amazonaws.com/contact" -ForegroundColor Cyan
