# Create AWS Infrastructure for Storage Subscription Service
Write-Host "Creating AWS Infrastructure..." -ForegroundColor Green

$BUCKET_NAME = "storage-subscription-bucket-$(Get-Random -Maximum 99999)"
$REGION = "us-east-1"

# Create S3 Bucket
Write-Host "`nCreating S3 Bucket: $BUCKET_NAME" -ForegroundColor Cyan
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Enable CORS on S3 Bucket
Write-Host "Configuring CORS..." -ForegroundColor Yellow
$corsConfig = @"
{
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": []
        }
    ]
}
"@
$corsConfig | Out-File -FilePath "cors.json" -Encoding utf8
aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration file://cors.json
Remove-Item "cors.json"

# Create DynamoDB Tables
Write-Host "`nCreating DynamoDB Tables..." -ForegroundColor Cyan

# StorageUsers Table
Write-Host "Creating StorageUsers table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name StorageUsers `
    --attribute-definitions AttributeName=email,AttributeType=S `
    --key-schema AttributeName=email,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --region $REGION

# StorageFiles Table
Write-Host "Creating StorageFiles table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name StorageFiles `
    --attribute-definitions AttributeName=fileId,AttributeType=S `
    --key-schema AttributeName=fileId,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --region $REGION

# Wait for tables to be created
Write-Host "`nWaiting for tables to be active..." -ForegroundColor Yellow
aws dynamodb wait table-exists --table-name StorageUsers --region $REGION
aws dynamodb wait table-exists --table-name StorageFiles --region $REGION

# Create IAM Role for Lambda
Write-Host "`nCreating IAM Role for Lambda..." -ForegroundColor Cyan
$trustPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
"@
$trustPolicy | Out-File -FilePath "trust-policy.json" -Encoding utf8
aws iam create-role --role-name StorageSubscriptionLambdaRole --assume-role-policy-document file://trust-policy.json
Remove-Item "trust-policy.json"

# Attach policies to role
Write-Host "Attaching policies to role..." -ForegroundColor Yellow
aws iam attach-role-policy --role-name StorageSubscriptionLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name StorageSubscriptionLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
aws iam attach-role-policy --role-name StorageSubscriptionLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

Write-Host "`nWaiting for IAM role to propagate..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Get AWS Account ID
$ACCOUNT_ID = aws sts get-caller-identity --query Account --output text

# Create Lambda Functions
Write-Host "`nCreating Lambda Functions..." -ForegroundColor Cyan

$lambdas = @("auth_api", "storage_api", "subscription_api", "admin_api")

foreach ($lambda in $lambdas) {
    Write-Host "Creating $lambda..." -ForegroundColor Yellow
    
    Set-Location "..\lambda\$lambda"
    
    # Install dependencies
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt -t .
    }
    
    # Create deployment package
    if (Test-Path "function.zip") {
        Remove-Item "function.zip"
    }
    Compress-Archive -Path * -DestinationPath function.zip
    
    # Create Lambda function
    aws lambda create-function `
        --function-name $lambda `
        --runtime python3.12 `
        --role arn:aws:iam::${ACCOUNT_ID}:role/StorageSubscriptionLambdaRole `
        --handler index.lambda_handler `
        --zip-file fileb://function.zip `
        --timeout 30 `
        --memory-size 512 `
        --environment Variables="{JWT_SECRET=your-secret-key-change-this,S3_BUCKET=$BUCKET_NAME,ADMIN_EMAILS=admin@yourdomain.com}" `
        --region $REGION
    
    Remove-Item "function.zip"
    
    Set-Location "..\..\scripts"
}

# Create API Gateway
Write-Host "`nCreating API Gateway..." -ForegroundColor Cyan
$apiId = aws apigatewayv2 create-api `
    --name storage-subscription-api `
    --protocol-type HTTP `
    --cors-configuration AllowOrigins="*",AllowMethods="*",AllowHeaders="*" `
    --region $REGION `
    --query ApiId `
    --output text

Write-Host "API Gateway ID: $apiId" -ForegroundColor Green

# Create integrations and routes
$lambdas = @{
    "auth_api" = @("/auth")
    "storage_api" = @("/storage")
    "subscription_api" = @("/subscription")
    "admin_api" = @("/admin/users", "/admin/stats")
}

foreach ($lambda in $lambdas.Keys) {
    Write-Host "Creating integration for $lambda..." -ForegroundColor Yellow
    
    $integrationId = aws apigatewayv2 create-integration `
        --api-id $apiId `
        --integration-type AWS_PROXY `
        --integration-uri arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:$lambda `
        --payload-format-version 2.0 `
        --region $REGION `
        --query IntegrationId `
        --output text
    
    foreach ($route in $lambdas[$lambda]) {
        Write-Host "Creating route: $route" -ForegroundColor Yellow
        aws apigatewayv2 create-route `
            --api-id $apiId `
            --route-key "ANY $route" `
            --target integrations/$integrationId `
            --region $REGION
    }
    
    # Grant API Gateway permission to invoke Lambda
    aws lambda add-permission `
        --function-name $lambda `
        --statement-id apigateway-invoke `
        --action lambda:InvokeFunction `
        --principal apigateway.amazonaws.com `
        --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${apiId}/*" `
        --region $REGION
}

# Create default stage
Write-Host "Creating API stage..." -ForegroundColor Yellow
aws apigatewayv2 create-stage `
    --api-id $apiId `
    --stage-name prod `
    --auto-deploy `
    --region $REGION

$API_URL = "https://${apiId}.execute-api.${REGION}.amazonaws.com/prod"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Infrastructure Created Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "S3 Bucket: $BUCKET_NAME" -ForegroundColor Cyan
Write-Host "API URL: $API_URL" -ForegroundColor Cyan
Write-Host "`nUpdate frontend/config.js with:" -ForegroundColor Yellow
Write-Host "const API_URL = '$API_URL';" -ForegroundColor White
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Update config.js with API URL" -ForegroundColor White
Write-Host "2. Set up Stripe account and add keys" -ForegroundColor White
Write-Host "3. Deploy frontend to S3: .\deploy-frontend.ps1" -ForegroundColor White
