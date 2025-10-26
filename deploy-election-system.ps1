# Deploy State Election Contributor System
# Run this script to deploy the complete election coverage system

Write-Host "=== State Election Contributor System Deployment ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create DynamoDB Tables
Write-Host "Step 1: Creating DynamoDB Tables..." -ForegroundColor Yellow

Write-Host "Creating contributors table..."
aws dynamodb create-table `
    --table-name contributors `
    --attribute-definitions AttributeName=contributor_id,AttributeType=S `
    --key-schema AttributeName=contributor_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST

Write-Host "Creating candidates table..."
aws dynamodb create-table `
    --table-name candidates `
    --attribute-definitions AttributeName=candidate_id,AttributeType=S `
    --key-schema AttributeName=candidate_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST

Write-Host "Creating election-events table..."
aws dynamodb create-table `
    --table-name election-events `
    --attribute-definitions AttributeName=event_id,AttributeType=S `
    --key-schema AttributeName=event_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST

Write-Host "DynamoDB tables created!" -ForegroundColor Green
Write-Host ""

# Step 2: Package and Deploy Lambda
Write-Host "Step 2: Packaging Lambda function..." -ForegroundColor Yellow

# Get AWS account ID
$accountId = aws sts get-caller-identity --query Account --output text
$region = aws configure get region
Write-Host "Account ID: $accountId" -ForegroundColor Cyan
Write-Host "Region: $region" -ForegroundColor Cyan

Set-Location contributors_api
Compress-Archive -Path index.py -DestinationPath function.zip -Force

Write-Host "Creating Lambda function..."
aws lambda create-function `
    --function-name contributors-api `
    --runtime python3.11 `
    --role arn:aws:iam::${accountId}:role/lambda-execution-role `
    --handler index.lambda_handler `
    --zip-file fileb://function.zip `
    --timeout 30 `
    --memory-size 256

Set-Location ..
Write-Host "Lambda function deployed!" -ForegroundColor Green
Write-Host ""

# Step 3: Create API Gateway
Write-Host "Step 3: Creating API Gateway..." -ForegroundColor Yellow

# Create REST API
$apiResult = aws apigateway create-rest-api --name "contributors-api" --description "State Election Contributors API" | ConvertFrom-Json
$apiId = $apiResult.id
Write-Host "API ID: $apiId" -ForegroundColor Cyan

# Get root resource ID
$resourcesResult = aws apigateway get-resources --rest-api-id $apiId | ConvertFrom-Json
$rootId = $resourcesResult.items[0].id

# Create /contributors resource
$contributorsResource = aws apigateway create-resource --rest-api-id $apiId --parent-id $rootId --path-part "contributors" | ConvertFrom-Json
$resourceId = $contributorsResource.id

# Get Lambda ARN
$lambdaArn = "arn:aws:lambda:${region}:${accountId}:function:contributors-api"

# Create methods
$methods = @('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')
foreach ($method in $methods) {
    Write-Host "Creating $method method..." -ForegroundColor Gray
    
    # Create method
    aws apigateway put-method --rest-api-id $apiId --resource-id $resourceId --http-method $method --authorization-type NONE | Out-Null
    
    if ($method -ne 'OPTIONS') {
        # Create integration
        aws apigateway put-integration --rest-api-id $apiId --resource-id $resourceId --http-method $method --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/${lambdaArn}/invocations" | Out-Null
    } else {
        # Mock integration for OPTIONS
        $mockTemplate = '{"application/json":"{\"statusCode\": 200}"}'
        aws apigateway put-integration --rest-api-id $apiId --resource-id $resourceId --http-method OPTIONS --type MOCK --request-templates $mockTemplate | Out-Null
        
        # OPTIONS response
        $methodParams = '{"method.response.header.Access-Control-Allow-Headers":false,"method.response.header.Access-Control-Allow-Methods":false,"method.response.header.Access-Control-Allow-Origin":false}'
        aws apigateway put-method-response --rest-api-id $apiId --resource-id $resourceId --http-method OPTIONS --status-code 200 --response-parameters $methodParams | Out-Null
        
        $integrationParams = '{"method.response.header.Access-Control-Allow-Headers":"''Content-Type,Authorization''","method.response.header.Access-Control-Allow-Methods":"''GET,POST,PUT,DELETE,OPTIONS''","method.response.header.Access-Control-Allow-Origin":"''*''"}'
        aws apigateway put-integration-response --rest-api-id $apiId --resource-id $resourceId --http-method OPTIONS --status-code 200 --response-parameters $integrationParams | Out-Null
    }
}

# Add Lambda permission
Write-Host "Adding Lambda permissions..." -ForegroundColor Gray
aws lambda add-permission --function-name contributors-api --statement-id apigateway-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${region}:${accountId}:${apiId}/*/*" 2>$null

# Deploy API
Write-Host "Deploying API to prod stage..." -ForegroundColor Gray
aws apigateway create-deployment --rest-api-id $apiId --stage-name prod | Out-Null

$apiUrl = "https://${apiId}.execute-api.${region}.amazonaws.com/prod/contributors"
Write-Host "API Gateway created!" -ForegroundColor Green
Write-Host "API URL: $apiUrl" -ForegroundColor Cyan
Write-Host ""

# Step 4: Update HTML files with API URL
Write-Host "Step 4: Updating HTML files with API URL..." -ForegroundColor Yellow

(Get-Content election-map.html) -replace 'YOUR_API_GATEWAY_URL', $apiUrl | Set-Content election-map.html
(Get-Content admin-contributors.html) -replace 'YOUR_API_GATEWAY_URL', $apiUrl | Set-Content admin-contributors.html

Write-Host "HTML files updated!" -ForegroundColor Green
Write-Host ""

# Step 5: Upload HTML files to S3
Write-Host "Step 5: Uploading HTML files to S3..." -ForegroundColor Yellow

aws s3 cp election-map.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
aws s3 cp admin-contributors.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"

Write-Host "HTML files uploaded!" -ForegroundColor Green
Write-Host ""

# Step 6: Add navigation links
Write-Host "Step 6: Adding navigation links to existing pages..." -ForegroundColor Yellow

$electionLink = '<a href="election-map.html" class="nav-link">🗺️ Election Map</a>'
$adminElectionLink = '<a href="admin-contributors.html" class="nav-link">🗺️ Contributors</a>'

# Add to videos.html
if (Test-Path "videos.html") {
    $content = Get-Content "videos.html" -Raw
    if ($content -notmatch 'election-map.html') {
        $content = $content -replace '(<a href="resources.html" class="nav-link">)', "$electionLink`n                    `$1"
        Set-Content "videos.html" $content -NoNewline
        aws s3 cp videos.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
        Write-Host "  Added to videos.html" -ForegroundColor Gray
    }
}

# Add to articles.html
if (Test-Path "articles.html") {
    $content = Get-Content "articles.html" -Raw
    if ($content -notmatch 'election-map.html') {
        $content = $content -replace '(<a href="resources.html" class="nav-link">)', "$electionLink`n                    `$1"
        Set-Content "articles.html" $content -NoNewline
        aws s3 cp articles.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
        Write-Host "  Added to articles.html" -ForegroundColor Gray
    }
}

# Add to news.html
if (Test-Path "news.html") {
    $content = Get-Content "news.html" -Raw
    if ($content -notmatch 'election-map.html') {
        $content = $content -replace '(<a href="resources.html" class="nav-link">)', "$electionLink`n                    `$1"
        Set-Content "news.html" $content -NoNewline
        aws s3 cp news.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
        Write-Host "  Added to news.html" -ForegroundColor Gray
    }
}

# Add to index.html
if (Test-Path "index.html") {
    $content = Get-Content "index.html" -Raw
    if ($content -notmatch 'election-map.html') {
        $content = $content -replace '(<a href="resources.html" class="nav-link">)', "$electionLink`n                    `$1"
        Set-Content "index.html" $content -NoNewline
        aws s3 cp index.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
        Write-Host "  Added to index.html" -ForegroundColor Gray
    }
}

# Add to admin.html
if (Test-Path "admin.html") {
    $content = Get-Content "admin.html" -Raw
    if ($content -notmatch 'admin-contributors.html') {
        $content = $content -replace '(<a href="profile\.html" class="nav-link">)', "$adminElectionLink`n                    `$1"
        Set-Content "admin.html" $content -NoNewline
        aws s3 cp admin.html s3://my-video-downloads-bucket/ --cache-control "max-age=300"
        Write-Host "  Added to admin.html" -ForegroundColor Gray
    }
}

Write-Host "Navigation links added!" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "=== DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "✅ DynamoDB Tables Created" -ForegroundColor White
Write-Host "✅ Lambda Function Deployed" -ForegroundColor White
Write-Host "✅ API Gateway Created & Configured" -ForegroundColor White
Write-Host "✅ HTML Files Updated & Uploaded" -ForegroundColor White
Write-Host "✅ Navigation Links Added" -ForegroundColor White
Write-Host ""
Write-Host "API URL: $apiUrl" -ForegroundColor Cyan
Write-Host "Public Page: https://christianconservativestoday.com/election-map.html" -ForegroundColor Cyan
Write-Host "Admin Page: https://christianconservativestoday.com/admin-contributors.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 State Election Contributor System is LIVE!" -ForegroundColor Green
