# Week 8: Deploy Marketing Automation API + CloudWatch daily trigger

$profile = "ekewaka"
$region = "us-east-1"
$accountId = "371751795928"
$apiId = "ydq9xzya5d"
$functionName = "marketing-api"
$roleName = "marketing-api-role"

Write-Host "`n=== Week 8: Deploying Marketing Automation ===" -ForegroundColor Cyan

# --- Step 1: Create IAM Role ---
Write-Host "`n[1/6] Creating IAM role..." -ForegroundColor Yellow

$trustFile = Join-Path $PSScriptRoot "tracking-trust-policy.json"  # reuse same trust policy

$roleExists = aws iam get-role --role-name $roleName --profile $profile 2>$null
if ($LASTEXITCODE -ne 0) {
    aws iam create-role --role-name $roleName --assume-role-policy-document "file://$trustFile" --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Role created" -ForegroundColor Green
    Start-Sleep -Seconds 5
} else {
    Write-Host "  Role already exists" -ForegroundColor Yellow
}

aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" --profile $profile 2>$null
aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess" --profile $profile 2>$null
aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/AmazonSESFullAccess" --profile $profile 2>$null
Write-Host "  Policies attached (DynamoDB + SES + CloudWatch)" -ForegroundColor Green

# --- Step 2: Package Lambda ---
Write-Host "`n[2/6] Packaging Lambda..." -ForegroundColor Yellow
$zipFile = "$env:TEMP\marketing-api.zip"
if (Test-Path $zipFile) { Remove-Item $zipFile }
$sourceDir = Join-Path $PSScriptRoot "..\marketing_api"
Compress-Archive -Path "$sourceDir\*" -DestinationPath $zipFile -Force
Write-Host "  Package created" -ForegroundColor Green

# --- Step 3: Create/Update Lambda ---
Write-Host "`n[3/6] Deploying Lambda..." -ForegroundColor Yellow
$roleArn = "arn:aws:iam::${accountId}:role/${roleName}"

$exists = aws lambda get-function --function-name $functionName --region $region --profile $profile 2>$null
if ($LASTEXITCODE -eq 0) {
    aws lambda update-function-code --function-name $functionName --zip-file "fileb://$zipFile" --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Lambda updated" -ForegroundColor Green
} else {
    aws lambda create-function `
        --function-name $functionName `
        --runtime python3.12 `
        --handler index.lambda_handler `
        --role $roleArn `
        --zip-file "fileb://$zipFile" `
        --timeout 300 `
        --memory-size 512 `
        --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  Lambda created" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# --- Step 4: Add /marketing to API Gateway ---
Write-Host "`n[4/6] Adding /marketing to API Gateway..." -ForegroundColor Yellow

$resources = aws apigateway get-resources --rest-api-id $apiId --region $region --profile $profile | ConvertFrom-Json
$rootId = ($resources.items | Where-Object { $_.path -eq "/" }).id
$marketingResource = $resources.items | Where-Object { $_.path -eq "/marketing" }

if ($marketingResource) {
    $marketingId = $marketingResource.id
    Write-Host "  /marketing already exists ($marketingId)" -ForegroundColor Yellow
} else {
    $result = aws apigateway create-resource --rest-api-id $apiId --parent-id $rootId --path-part "marketing" --region $region --profile $profile | ConvertFrom-Json
    $marketingId = $result.id
    Write-Host "  /marketing created ($marketingId)" -ForegroundColor Green
}

$lambdaArn = "arn:aws:lambda:${region}:${accountId}:function:${functionName}"
$integrationUri = "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/${lambdaArn}/invocations"

foreach ($method in @("GET", "POST")) {
    Write-Host "  Creating $method method..." -ForegroundColor Gray
    aws apigateway put-method --rest-api-id $apiId --resource-id $marketingId --http-method $method --authorization-type NONE --region $region --profile $profile --no-cli-pager 2>$null
    aws apigateway put-integration --rest-api-id $apiId --resource-id $marketingId --http-method $method --type AWS_PROXY --integration-http-method POST --uri $integrationUri --region $region --profile $profile --no-cli-pager 2>$null
}

# OPTIONS for CORS
Write-Host "  Creating OPTIONS (CORS)..." -ForegroundColor Gray
aws apigateway put-method --rest-api-id $apiId --resource-id $marketingId --http-method OPTIONS --authorization-type NONE --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-integration --rest-api-id $apiId --resource-id $marketingId --http-method OPTIONS --type MOCK --request-templates "{`"application/json`": `"{\\`"statusCode\\`": 200}`"}" --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-method-response --rest-api-id $apiId --resource-id $marketingId --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false" --region $region --profile $profile --no-cli-pager 2>$null
aws apigateway put-integration-response --rest-api-id $apiId --resource-id $marketingId --http-method OPTIONS --status-code 200 --response-parameters "{`"method.response.header.Access-Control-Allow-Headers`":`"'Content-Type,Authorization'`",`"method.response.header.Access-Control-Allow-Methods`":`"'GET,POST,OPTIONS'`",`"method.response.header.Access-Control-Allow-Origin`":`"'*'`"}" --region $region --profile $profile --no-cli-pager 2>$null

# Lambda permission for API Gateway
aws lambda add-permission --function-name $functionName --statement-id "apigateway-marketing" --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${region}:${accountId}:${apiId}/*/*/marketing" --region $region --profile $profile --no-cli-pager 2>$null

# --- Step 5: Create CloudWatch Events daily trigger ---
Write-Host "`n[5/6] Creating daily CloudWatch Events trigger (10 AM EST)..." -ForegroundColor Yellow

aws events put-rule `
    --name "marketing-daily-scan" `
    --schedule-expression "cron(0 15 * * ? *)" `
    --state ENABLED `
    --description "Run marketing automation scans daily at 10 AM EST (15:00 UTC)" `
    --region $region --profile $profile --no-cli-pager | Out-Null

# Permission for CloudWatch to invoke Lambda
aws lambda add-permission --function-name $functionName --statement-id "cloudwatch-daily-trigger" --action lambda:InvokeFunction --principal events.amazonaws.com --source-arn "arn:aws:events:${region}:${accountId}:rule/marketing-daily-scan" --region $region --profile $profile --no-cli-pager 2>$null

# Add Lambda as target
aws events put-targets `
    --rule "marketing-daily-scan" `
    --targets "Id=marketing-api-target,Arn=arn:aws:lambda:${region}:${accountId}:function:${functionName}" `
    --region $region --profile $profile --no-cli-pager | Out-Null

Write-Host "  Daily trigger created (10 AM EST / 3 PM UTC)" -ForegroundColor Green

# --- Step 6: Deploy API ---
Write-Host "`n[6/6] Deploying API Gateway..." -ForegroundColor Yellow
aws apigateway create-deployment --rest-api-id $apiId --stage-name prod --region $region --profile $profile --no-cli-pager | Out-Null
Write-Host "  API deployed to prod" -ForegroundColor Green

$endpoint = "https://${apiId}.execute-api.${region}.amazonaws.com/prod/marketing"
Write-Host "`n=== Marketing API deployed! ===" -ForegroundColor Green
Write-Host "Endpoint: $endpoint"
Write-Host "Daily scan: 10 AM EST via CloudWatch Events"
Write-Host "`nTest:"
Write-Host "  Stats:       curl `"$endpoint`?action=stats`""
Write-Host "  Preferences: curl `"$endpoint`?action=preferences-get&user_id=test`""
Write-Host "  Manual scan: curl -X POST `"$endpoint`?action=run-scans`""
