# Deploy Feature Flags API Lambda Function
Write-Host "Deploying Feature Flags API Lambda Function..." -ForegroundColor Cyan

# Configuration
$FunctionName = "feature-flags-api"
$Region = "us-east-1"
$Profile = "ekewaka"
$Runtime = "python3.12"
$Handler = "index.lambda_handler"
$Role = "arn:aws:iam::371751795928:role/testimony-lambda-role"
$Timeout = 30
$MemorySize = 256

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
$PackageDir = "feature_flags_api"
$ZipFile = "feature-flags-api.zip"

# Remove old zip if exists
if (Test-Path $ZipFile) {
    Remove-Item $ZipFile
}

# Install PyJWT if not already in package
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install PyJWT -t $PackageDir --upgrade --quiet

# Create zip file
Write-Host "Creating zip archive..." -ForegroundColor Yellow
Compress-Archive -Path "$PackageDir\*" -DestinationPath $ZipFile -Force

# Check if function exists
Write-Host "Checking if Lambda function exists..." -ForegroundColor Yellow
$FunctionExists = $false
$checkResult = aws lambda get-function --function-name $FunctionName --region $Region --profile $Profile 2>&1
if ($LASTEXITCODE -eq 0) {
    $FunctionExists = $true
    Write-Host "[SUCCESS] Function exists, updating..." -ForegroundColor Green
} else {
    Write-Host "[INFO] Function doesn't exist, creating..." -ForegroundColor Yellow
}

if ($FunctionExists) {
    # Update existing function
    Write-Host "Updating function code..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file "fileb://$ZipFile" `
        --region $Region `
        --profile $Profile
    
    Write-Host "Updating function configuration..." -ForegroundColor Yellow
    aws lambda update-function-configuration `
        --function-name $FunctionName `
        --runtime $Runtime `
        --handler $Handler `
        --timeout $Timeout `
        --memory-size $MemorySize `
        --region $Region `
        --profile $Profile
} else {
    # Create new function
    Write-Host "Creating new Lambda function..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name $FunctionName `
        --runtime $Runtime `
        --role $Role `
        --handler $Handler `
        --zip-file "fileb://$ZipFile" `
        --timeout $Timeout `
        --memory-size $MemorySize `
        --region $Region `
        --profile $Profile
}

Write-Host ""
Write-Host "[SUCCESS] Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create API Gateway HTTP API and connect to this Lambda function"
Write-Host "2. Update feature-flags.js with your API Gateway URL"
Write-Host "3. Update admin-feature-flags.html with your API Gateway URL"
Write-Host ""
Write-Host "Lambda Function ARN:" -ForegroundColor Yellow
aws lambda get-function --function-name $FunctionName --region $Region --profile $Profile --query 'Configuration.FunctionArn' --output text
Write-Host ""
Write-Host "[SUCCESS] Done!" -ForegroundColor Green
