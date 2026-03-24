# Deploy Mountains API Lambda Function
# Run this script to deploy the 7 Mountains API to AWS

Write-Host "🏔️  Deploying 7 Mountains API Lambda Function..." -ForegroundColor Cyan

# Set variables
$FunctionName = "mountains-api"
$Region = "us-east-1"
$Profile = "ekewaka"
$ZipFile = "function.zip"

# Navigate to mountains_api directory
Set-Location -Path "mountains_api"

# Check if PyJWT is installed
if (-not (Test-Path "jwt")) {
    Write-Host "📦 Installing PyJWT dependency..." -ForegroundColor Yellow
    pip install PyJWT -t .
}

# Create deployment package
Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow
if (Test-Path $ZipFile) {
    Remove-Item $ZipFile
}

Compress-Archive -Path index.py,jwt,PyJWT-*.dist-info -DestinationPath $ZipFile -Force

# Check if Lambda function exists
Write-Host "🔍 Checking if Lambda function exists..." -ForegroundColor Yellow
$functionExists = $false
try {
    aws lambda get-function --function-name $FunctionName --region $Region --profile $Profile 2>$null
    $functionExists = $true
    Write-Host "✅ Function exists, updating code..." -ForegroundColor Green
} catch {
    Write-Host "📝 Function doesn't exist, creating new..." -ForegroundColor Yellow
}

if ($functionExists) {
    # Update existing function
    aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file fileb://$ZipFile `
        --region $Region `
        --profile $Profile
    
    Write-Host "✅ Lambda function code updated!" -ForegroundColor Green
} else {
    # Create new function
    Write-Host "Creating new Lambda function..." -ForegroundColor Yellow
    Write-Host "⚠️  You'll need to:" -ForegroundColor Yellow
    Write-Host "   1. Create the function in AWS Console first" -ForegroundColor Yellow
    Write-Host "   2. Set Runtime: Python 3.12" -ForegroundColor Yellow
    Write-Host "   3. Set Handler: index.lambda_handler" -ForegroundColor Yellow
    Write-Host "   4. Attach role: lambda-execution-role" -ForegroundColor Yellow
    Write-Host "   5. Add permissions: DynamoDB Full Access" -ForegroundColor Yellow
    Write-Host "   6. Then run this script again to upload code" -ForegroundColor Yellow
}

# Return to parent directory
Set-Location -Path ".."

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create API Gateway endpoint" -ForegroundColor White
Write-Host "2. Link API Gateway to mountains-api Lambda" -ForegroundColor White
Write-Host "3. Test endpoints with Postman or curl" -ForegroundColor White
Write-Host "4. Update frontend to call new API" -ForegroundColor White
