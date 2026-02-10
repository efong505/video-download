# Deploy Lambda@Edge for Dynamic Meta Tags
# Must be deployed to us-east-1 region

$FunctionName = "article-meta-tags-edge"
$Region = "us-east-1"

Write-Host "Deploying Lambda@Edge function: $FunctionName" -ForegroundColor Cyan

# Create deployment package
Set-Location lambda-edge-meta-tags
if (Test-Path function.zip) { Remove-Item function.zip }
Compress-Archive -Path index.py -DestinationPath function.zip
Set-Location ..

Write-Host "Deployment package created" -ForegroundColor Green

# Update or create Lambda function
try {
    aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file fileb://lambda-edge-meta-tags/function.zip `
        --region $Region
    Write-Host "Lambda function updated" -ForegroundColor Green
} catch {
    Write-Host "Function doesn't exist, creating..." -ForegroundColor Yellow
    
    # Create IAM role first
    $RoleName = "lambda-edge-meta-tags-role"
    
    aws lambda create-function `
        --function-name $FunctionName `
        --runtime python3.12 `
        --role arn:aws:iam::YOUR_ACCOUNT_ID:role/$RoleName `
        --handler index.lambda_handler `
        --zip-file fileb://lambda-edge-meta-tags/function.zip `
        --timeout 5 `
        --memory-size 128 `
        --region $Region `
        --environment "Variables={ENABLE_DYNAMIC_META=true}"
    
    Write-Host "Lambda function created" -ForegroundColor Green
}

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Go to AWS Console > Lambda > $FunctionName" -ForegroundColor White
Write-Host "2. Publish a new version (Actions > Publish new version)" -ForegroundColor White
Write-Host "3. Go to CloudFront > Your Distribution > Behaviors" -ForegroundColor White
Write-Host "4. Edit behavior for *.html files" -ForegroundColor White
Write-Host "5. Add Lambda@Edge association: Viewer Request > Select your function version" -ForegroundColor White
Write-Host "`nTo disable dynamic meta tags:" -ForegroundColor Yellow
Write-Host "Set environment variable ENABLE_DYNAMIC_META=false in Lambda Console" -ForegroundColor White
