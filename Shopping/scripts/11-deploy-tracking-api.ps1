# Week 7: Deploy Tracking API Lambda + API Gateway resource
# Adds /tracking resource to existing shopping-api gateway

$profile = "ekewaka"
$region = "us-east-1"
$accountId = "371751795928"
$apiId = "ydq9xzya5d"  # existing shopping-api gateway
$functionName = "tracking-api"
$roleName = "tracking-api-role"

Write-Host "`n=== Week 7: Deploying Tracking API ===" -ForegroundColor Cyan

# --- Step 1: Create IAM Role ---
Write-Host "`n[1/5] Creating IAM role..." -ForegroundColor Yellow

$trustPolicy = @'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
'@

$trustFile = "$env:TEMP\tracking-trust.json"
$trustPolicy | Out-File -FilePath $trustFile -Encoding utf8

try {
    aws iam create-role --role-name $roleName --assume-role-policy-document "file://$trustFile" --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Role created" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "  Role already exists - continuing" -ForegroundColor Yellow
}

# Attach policies
aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" --profile $profile 2>$null
aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess" --profile $profile 2>$null
Write-Host "  Policies attached" -ForegroundColor Green

# --- Step 2: Package Lambda ---
Write-Host "`n[2/5] Packaging Lambda..." -ForegroundColor Yellow

$zipFile = "$env:TEMP\tracking-api.zip"
if (Test-Path $zipFile) { Remove-Item $zipFile }

$sourceDir = Join-Path $PSScriptRoot "..\tracking_api"
Compress-Archive -Path "$sourceDir\*" -DestinationPath $zipFile -Force
Write-Host "  Package created: $zipFile" -ForegroundColor Green

# --- Step 3: Create/Update Lambda ---
Write-Host "`n[3/5] Deploying Lambda function..." -ForegroundColor Yellow

$roleArn = "arn:aws:iam::${accountId}:role/${roleName}"

# Check if function exists
$exists = aws lambda get-function --function-name $functionName --region $region --profile $profile 2>$null
if ($LASTEXITCODE -eq 0) {
    # Update existing
    aws lambda update-function-code --function-name $functionName --zip-file "fileb://$zipFile" --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Lambda updated" -ForegroundColor Green
} else {
    # Create new
    aws lambda create-function `
        --function-name $functionName `
        --runtime python3.12 `
        --handler index.lambda_handler `
        --role $roleArn `
        --zip-file "fileb://$zipFile" `
        --timeout 15 `
        --memory-size 256 `
        --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Lambda created" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# --- Step 4: Add /tracking resource to API Gateway ---
Write-Host "`n[4/5] Adding /tracking to API Gateway..." -ForegroundColor Yellow

# Get root resource
$resources = aws apigateway get-resources --rest-api-id $apiId --region $region --profile $profile | ConvertFrom-Json
$rootId = ($resources.items | Where-Object { $_.path -eq "/" }).id

# Check if /tracking already exists
$trackingResource = $resources.items | Where-Object { $_.path -eq "/tracking" }

if ($trackingResource) {
    $trackingId = $trackingResource.id
    Write-Host "  /tracking resource already exists ($trackingId)" -ForegroundColor Yellow
} else {
    $result = aws apigateway create-resource --rest-api-id $apiId --parent-id $rootId --path-part "tracking" --region $region --profile $profile | ConvertFrom-Json
    $trackingId = $result.id
    Write-Host "  /tracking resource created ($trackingId)" -ForegroundColor Green
}

$lambdaArn = "arn:aws:lambda:${region}:${accountId}:function:${functionName}"
$integrationUri = "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/${lambdaArn}/invocations"

# Create methods: GET, POST, DELETE, OPTIONS
foreach ($method in @("GET", "POST", "DELETE")) {
    Write-Host "  Creating $method method..." -ForegroundColor Gray
    aws apigateway put-method --rest-api-id $apiId --resource-id $trackingId --http-method $method --authorization-type NONE --region $region --profile $profile --no-cli-pager 2>$null
    aws apigateway put-integration --rest-api-id $apiId --resource-id $trackingId --http-method $method --type AWS_PROXY --integration-http-method POST --uri $integrationUri --region $region --profile $profile --no-cli-pager 2>$null
}

# OPTIONS for CORS
Write-Host "  Creating OPTIONS method (CORS)..." -ForegroundColor Gray
aws apigateway put-method --rest-api-id $apiId --resource-id $trackingId --http-method OPTIONS --authorization-type NONE --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-integration --rest-api-id $apiId --resource-id $trackingId --http-method OPTIONS --type MOCK --request-templates '{"application/json":"{\"statusCode\":200}"}' --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-method-response --rest-api-id $apiId --resource-id $trackingId --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false" --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-integration-response --rest-api-id $apiId --resource-id $trackingId --http-method OPTIONS --status-code 200 --response-parameters "{`"method.response.header.Access-Control-Allow-Headers`":`"'Content-Type,Authorization'`",`"method.response.header.Access-Control-Allow-Methods`":`"'GET,POST,DELETE,OPTIONS'`",`"method.response.header.Access-Control-Allow-Origin`":`"'*'`"}" --region $region --profile $profile --no-cli-pager 2>$null

# Lambda permission for API Gateway
Write-Host "  Adding Lambda permission..." -ForegroundColor Gray
aws lambda add-permission --function-name $functionName --statement-id "apigateway-tracking" --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${region}:${accountId}:${apiId}/*/*/tracking" --region $region --profile $profile --no-cli-pager 2>$null

# --- Step 5: Deploy API ---
Write-Host "`n[5/5] Deploying API Gateway..." -ForegroundColor Yellow
aws apigateway create-deployment --rest-api-id $apiId --stage-name prod --region $region --profile $profile --no-cli-pager | Out-Null
Write-Host "  API deployed to prod" -ForegroundColor Green

$endpoint = "https://${apiId}.execute-api.${region}.amazonaws.com/prod/tracking"
Write-Host "`n=== Tracking API deployed successfully! ===" -ForegroundColor Green
Write-Host "Endpoint: $endpoint"
Write-Host "`nTest:"
Write-Host "  Track view:  curl -X POST `"$endpoint`?action=track-view`" -d '{`"product_id`":`"test`",`"product_name`":`"Test`"}'"
Write-Host "  Popular:     curl `"$endpoint`?action=popular`""
Write-Host "  Watchlist:   curl `"$endpoint`?action=watchlist&user_id=guest`""
