# Deploy Scheduled Publisher Lambda
Write-Host "Deploying Scheduled Publisher Lambda..." -ForegroundColor Cyan

# Navigate to scheduled-publisher directory
Set-Location scheduled-publisher

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path "lambda.zip") {
    Remove-Item "lambda.zip"
}
Compress-Archive -Path lambda_function.py -DestinationPath lambda.zip

# Check if Lambda function exists
Write-Host "Checking if Lambda function exists..." -ForegroundColor Yellow
$functionExists = $false
try {
    aws lambda get-function --function-name scheduled-publisher --profile ekewaka --region us-east-1 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $functionExists = $true
    }
} catch {}

if ($functionExists) {
    # Update existing function
    Write-Host "Updating existing Lambda function..." -ForegroundColor Yellow
    aws lambda update-function-code --function-name scheduled-publisher --zip-file fileb://lambda.zip --region us-east-1 --profile ekewaka
} else {
    # Create new function
    Write-Host "Creating new Lambda function..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name scheduled-publisher `
        --runtime python3.12 `
        --role arn:aws:iam::371751795928:role/lambda-execution-role `
        --handler lambda_function.lambda_handler `
        --zip-file fileb://lambda.zip `
        --timeout 60 `
        --memory-size 256 `
        --region us-east-1 `
        --profile ekewaka
    
    # Create EventBridge rule to run every 5 minutes
    Write-Host "Creating EventBridge schedule..." -ForegroundColor Yellow
    aws events put-rule `
        --name scheduled-publisher-trigger `
        --schedule-expression "rate(5 minutes)" `
        --state ENABLED `
        --region us-east-1 `
        --profile ekewaka
    
    # Add permission for EventBridge to invoke Lambda
    aws lambda add-permission `
        --function-name scheduled-publisher `
        --statement-id scheduled-publisher-event `
        --action lambda:InvokeFunction `
        --principal events.amazonaws.com `
        --source-arn arn:aws:events:us-east-1:371751795928:rule/scheduled-publisher-trigger `
        --region us-east-1 `
        --profile ekewaka
    
    # Add Lambda as target for EventBridge rule
    aws events put-targets `
        --rule scheduled-publisher-trigger `
        --targets '[{"Id":"1","Arn":"arn:aws:lambda:us-east-1:371751795928:function:scheduled-publisher"}]' `
        --region us-east-1 `
        --profile ekewaka
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Scheduled Publisher deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Return to root directory
Set-Location ..

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "The scheduler will check for scheduled content every 5 minutes." -ForegroundColor Cyan
