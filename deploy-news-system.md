# News Management System Deployment Guide

## Step 1: Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name news-table \
    --attribute-definitions \
        AttributeName=news_id,AttributeType=S \
    --key-schema \
        AttributeName=news_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

## Step 2: Create Lambda Function

```bash
# Create deployment package
cd news_api
zip -r ../news-api-deployment.zip .
cd ..

# Create Lambda function
aws lambda create-function \
    --function-name news-api \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
    --handler index.lambda_handler \
    --zip-file fileb://news-api-deployment.zip \
    --timeout 30 \
    --memory-size 256 \
    --region us-east-1
```

## Step 3: Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api \
    --name news-api \
    --description "News Management API" \
    --region us-east-1

# Note the API ID from the response, then create resource
aws apigateway create-resource \
    --rest-api-id YOUR_API_ID \
    --parent-id ROOT_RESOURCE_ID \
    --path-part news \
    --region us-east-1

# Create methods (GET, POST, PUT, DELETE, OPTIONS)
aws apigateway put-method \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method GET \
    --authorization-type NONE \
    --region us-east-1

aws apigateway put-method \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method POST \
    --authorization-type NONE \
    --region us-east-1

aws apigateway put-method \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method PUT \
    --authorization-type NONE \
    --region us-east-1

aws apigateway put-method \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method DELETE \
    --authorization-type NONE \
    --region us-east-1

aws apigateway put-method \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method OPTIONS \
    --authorization-type NONE \
    --region us-east-1

# Create integrations for each method
aws apigateway put-integration \
    --rest-api-id YOUR_API_ID \
    --resource-id RESOURCE_ID \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:news-api/invocations \
    --region us-east-1

# Repeat for POST, PUT, DELETE, OPTIONS methods

# Deploy API
aws apigateway create-deployment \
    --rest-api-id YOUR_API_ID \
    --stage-name prod \
    --region us-east-1
```

## Step 4: Grant Lambda Permissions

```bash
aws lambda add-permission \
    --function-name news-api \
    --statement-id allow-api-gateway \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:us-east-1:YOUR_ACCOUNT_ID:YOUR_API_ID/*/*" \
    --region us-east-1
```

## Step 5: Update Frontend Files

Update the NEWS_API variable in the following files with your actual API Gateway URL:
- `create-news.html`
- `news.html` 
- `news-article.html`

Replace `https://your-api-gateway-url/prod/news` with your actual endpoint.

## Step 6: Upload Frontend Files to S3

```bash
aws s3 cp create-news.html s3://your-bucket-name/
aws s3 cp news.html s3://your-bucket-name/
aws s3 cp news-article.html s3://your-bucket-name/
```

## Step 7: Update Navigation Links

Add news navigation links to existing pages:
- `index.html`
- `videos.html`
- `articles.html`
- `admin.html`

Add this to navigation sections:
```html
<a href="news.html" class="nav-btn"><i class="fas fa-broadcast-tower"></i> News</a>
```

## Step 8: Test the System

1. Access `news.html` to view news listing
2. Login as admin and access `create-news.html` to create news
3. Test breaking news functionality
4. Verify news article viewing works
5. Test admin edit/delete functionality

## Environment Variables for Lambda

Set these environment variables in your Lambda function:
- `JWT_SECRET`: Your JWT secret key (same as auth API)

## Required IAM Permissions

Your Lambda execution role needs:
- `dynamodb:GetItem`
- `dynamodb:PutItem`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`
- `dynamodb:Scan`
- `dynamodb:Query`

## Database Schema

The news-table will store:
- `news_id` (String, Primary Key)
- `title` (String)
- `content` (String)
- `summary` (String)
- `category` (String)
- `tags` (List)
- `author` (String)
- `author_name` (String)
- `visibility` (String: public/private)
- `is_breaking` (Boolean)
- `external_url` (String)
- `featured_image` (String)
- `scheduled_publish` (String)
- `status` (String: published/draft/scheduled)
- `created_at` (String)
- `updated_at` (String)
- `view_count` (Number)