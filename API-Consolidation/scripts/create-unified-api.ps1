# create-unified-api.ps1
# Creates unified API Gateway with all service routes

param(
    [string]$ApiName = "unified-api",
    [string]$Region = "us-east-1"
)

Write-Host "🚀 Creating Unified API Gateway..." -ForegroundColor Cyan

# Step 1: Create REST API
Write-Host "`n📝 Step 1: Creating REST API..." -ForegroundColor Yellow
$apiResponse = aws apigateway create-rest-api `
    --name $ApiName `
    --description "Consolidated API for Christian Conservatives Today" `
    --endpoint-configuration types=REGIONAL `
    --region $Region | ConvertFrom-Json

$apiId = $apiResponse.id
Write-Host "✅ API Created: $apiId" -ForegroundColor Green

# Step 2: Get root resource ID
Write-Host "`n📝 Step 2: Getting root resource..." -ForegroundColor Yellow
$resourcesResponse = aws apigateway get-resources `
    --rest-api-id $apiId `
    --region $Region | ConvertFrom-Json

$rootId = $resourcesResponse.items[0].id
Write-Host "✅ Root ID: $rootId" -ForegroundColor Green

# Step 3: Create base path resources
Write-Host "`n📝 Step 3: Creating base path resources..." -ForegroundColor Yellow

$paths = @(
    "admin",
    "auth",
    "articles",
    "videos",
    "news",
    "resources",
    "contributors",
    "comments",
    "tags",
    "prayer",
    "events",
    "email",
    "ministry",
    "notifications",
    "url-analysis",
    "paypal",
    "download"
)

$resourceIds = @{}

foreach ($path in $paths) {
    Write-Host "  Creating /$path..." -NoNewline
    $resource = aws apigateway create-resource `
        --rest-api-id $apiId `
        --parent-id $rootId `
        --path-part $path `
        --region $Region | ConvertFrom-Json
    
    $resourceIds[$path] = $resource.id
    Write-Host " ✅" -ForegroundColor Green
}

# Step 4: Create proxy resources
Write-Host "`n📝 Step 4: Creating proxy resources..." -ForegroundColor Yellow

$proxyIds = @{}

foreach ($path in $paths) {
    Write-Host "  Creating /$path/{proxy+}..." -NoNewline
    $proxy = aws apigateway create-resource `
        --rest-api-id $apiId `
        --parent-id $resourceIds[$path] `
        --path-part "{proxy+}" `
        --region $Region | ConvertFrom-Json
    
    $proxyIds[$path] = $proxy.id
    Write-Host " ✅" -ForegroundColor Green
}

# Step 5: Map Lambda functions
Write-Host "`n📝 Step 5: Mapping Lambda functions..." -ForegroundColor Yellow

$accountId = (aws sts get-caller-identity --query Account --output text)

$lambdaMappings = @{
    "admin" = "admin_api"
    "auth" = "auth_api"
    "articles" = "articles_api"
    "videos" = "video_list_api"
    "news" = "news_api"
    "resources" = "resources_api"
    "contributors" = "contributors_api"
    "comments" = "comments_api"
    "tags" = "tag_api"
    "prayer" = "prayer_api"
    "events" = "events_api"
    "email" = "email_subscription_api"
    "ministry" = "ministry_tools_api"
    "notifications" = "notifications_api"
    "url-analysis" = "url_analysis_api"
    "paypal" = "paypal_billing_api"
    "download" = "downloader"
}

foreach ($path in $paths) {
    $lambdaName = $lambdaMappings[$path]
    $proxyId = $proxyIds[$path]
    
    Write-Host "  Mapping /$path to $lambdaName..." -NoNewline
    
    # Create ANY method
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method ANY `
        --authorization-type NONE `
        --region $Region | Out-Null
    
    # Create Lambda integration
    $lambdaUri = "arn:aws:apigateway:${Region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${Region}:${accountId}:function:${lambdaName}/invocations"
    
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method ANY `
        --type AWS_PROXY `
        --integration-http-method POST `
        --uri $lambdaUri `
        --region $Region | Out-Null
    
    # Grant API Gateway permission
    aws lambda add-permission `
        --function-name $lambdaName `
        --statement-id "apigateway-unified-$path" `
        --action lambda:InvokeFunction `
        --principal apigateway.amazonaws.com `
        --source-arn "arn:aws:execute-api:${Region}:${accountId}:${apiId}/*/*" `
        --region $Region 2>$null | Out-Null
    
    Write-Host " ✅" -ForegroundColor Green
}

# Step 6: Enable CORS
Write-Host "`n📝 Step 6: Enabling CORS..." -ForegroundColor Yellow

foreach ($path in $paths) {
    $proxyId = $proxyIds[$path]
    
    Write-Host "  Enabling CORS for /$path..." -NoNewline
    
    # Create OPTIONS method
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method OPTIONS `
        --authorization-type NONE `
        --region $Region | Out-Null
    
    # Create mock integration
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method OPTIONS `
        --type MOCK `
        --request-templates '{\"application/json\": \"{\\\"statusCode\\\": 200}\"}' `
        --region $Region | Out-Null
    
    # Create method response
    aws apigateway put-method-response `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method OPTIONS `
        --status-code 200 `
        --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\": true, \"method.response.header.Access-Control-Allow-Methods\": true, \"method.response.header.Access-Control-Allow-Origin\": true}' `
        --region $Region | Out-Null
    
    # Create integration response
    aws apigateway put-integration-response `
        --rest-api-id $apiId `
        --resource-id $proxyId `
        --http-method OPTIONS `
        --status-code 200 `
        --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\": \"\\\"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\\\"\", \"method.response.header.Access-Control-Allow-Methods\": \"\\\"GET,POST,PUT,DELETE,OPTIONS\\\"\", \"method.response.header.Access-Control-Allow-Origin\": \"\\\"*\\\"\"}' `
        --region $Region | Out-Null
    
    Write-Host " ✅" -ForegroundColor Green
}

# Step 7: Deploy API
Write-Host "`n📝 Step 7: Deploying API..." -ForegroundColor Yellow

aws apigateway create-deployment `
    --rest-api-id $apiId `
    --stage-name prod `
    --stage-description "Production stage" `
    --description "Initial deployment of unified API" `
    --region $Region | Out-Null

Write-Host "✅ API Deployed!" -ForegroundColor Green

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "🎉 UNIFIED API CREATED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "`nAPI ID: $apiId" -ForegroundColor Yellow
Write-Host "API URL: https://$apiId.execute-api.$Region.amazonaws.com/prod" -ForegroundColor Yellow
Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Request ACM certificate for api.christianconservativestoday.com"
Write-Host "2. Run: .\configure-custom-domain.ps1 -ApiId $apiId -CertificateArn YOUR_CERT_ARN"
Write-Host "3. Test all endpoints"
Write-Host "4. Update frontend to use new API URLs"
Write-Host "`n" + "="*60 -ForegroundColor Cyan

# Save API ID for next script
$apiId | Out-File -FilePath "api-id.txt" -NoNewline
Write-Host "`n💾 API ID saved to api-id.txt" -ForegroundColor Green
