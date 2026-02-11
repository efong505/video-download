# API Gateway - Detailed Implementation Guide

## Overview
Step-by-step guide for consolidating 12 separate API Gateways into 1 unified REST API with 14 Lambda integrations.

---

## Step 1: Analyze Existing API Gateways

### Commands to List All APIs

```bash
# List all REST APIs
aws apigateway get-rest-apis --query 'items[*].[id,name,createdDate]' --output table

# List all HTTP APIs
aws apigatewayv2 get-apis --query 'Items[*].[ApiId,Name,CreatedDate]' --output table
```

### Data Collected

**Total APIs Found**: 25 (22 REST + 3 HTTP)

**Christian Conservative Platform APIs** (12 total):
```
1. admin-api (REST) - r8x3k9m2l5
2. articles-api (REST) - a4b7c2d9e1
3. auth-api (REST) - f3g6h1j4k8
4. comments-api (REST) - m2n5p8q1r4
5. contributors-api (REST) - s7t0u3v6w9 (duplicate 1)
6. contributors-api (REST) - x2y5z8a1b4 (duplicate 2)
7. contributors-api (REST) - c7d0e3f6g9 (duplicate 3)
8. news-api (REST) - h4i7j0k3l6
9. resources-api (REST) - m9n2o5p8q1
10. video-tag-api (REST) - r4s7t0u3v6
11. video-downloader-api (REST) - w1x4y7z0a3 (duplicate 1)
12. video-downloader-api (REST) - b6c9d2e5f8 (duplicate 2)
```

**Decision**: Consolidate into 1 unified REST API

---

## Step 2: Design Unified API Structure

### Endpoint Mapping

| Old API | Old Endpoint | New Endpoint | Lambda Function |
|---------|-------------|--------------|-----------------|
| auth-api | / | /auth | auth_api |
| admin-api | / | /admin | admin_api |
| articles-api | / | /articles | articles_api |
| news-api | / | /news | news_api |
| comments-api | / | /comments | comments_api |
| contributors-api | / | /contributors | contributors_api |
| resources-api | / | /resources | resources_api |
| video-list-api | / | /videos | video_list_api |
| video-tag-api | / | /tags | tag_api |
| video-downloader-api | / | /download | router |
| paypal-billing-api | / | /paypal | paypal_billing_api |
| url-analysis-api | / | /analyze | url_analysis_api |
| prayer-api | / | /prayer | prayer_api |
| notifications-api | / | /notifications | notifications_api |

### New API Structure
```
ministry-platform-api (diz6ceeb22)
├── /auth          → auth_api Lambda
├── /admin         → admin_api Lambda
├── /articles      → articles_api Lambda
├── /news          → news_api Lambda
├── /comments      → comments_api Lambda
├── /contributors  → contributors_api Lambda
├── /resources     → resources_api Lambda
├── /videos        → video_list_api Lambda
├── /tags          → tag_api Lambda
├── /download      → router Lambda
├── /paypal        → paypal_billing_api Lambda
├── /analyze       → url_analysis_api Lambda
├── /prayer        → prayer_api Lambda
└── /notifications → notifications_api Lambda
```

---

## Step 3: Gather Lambda Function Information

### Commands to List Lambda Functions

```bash
# List all Lambda functions
aws lambda list-functions --query 'Functions[*].[FunctionName,FunctionArn,Runtime,Handler]' --output table

# Get specific function details
aws lambda get-function --function-name router --query 'Configuration.[FunctionName,FunctionArn,Role,Runtime,Handler,MemorySize,Timeout]'
```

### Data Collected

**Lambda Functions** (18 total):
```
router - arn:aws:lambda:us-east-1:371751795928:function:router
admin_api - arn:aws:lambda:us-east-1:371751795928:function:admin_api
articles_api - arn:aws:lambda:us-east-1:371751795928:function:articles_api
auth_api - arn:aws:lambda:us-east-1:371751795928:function:auth_api
comments_api - arn:aws:lambda:us-east-1:371751795928:function:comments_api
contributors_api - arn:aws:lambda:us-east-1:371751795928:function:contributors_api
news_api - arn:aws:lambda:us-east-1:371751795928:function:news_api
resources_api - arn:aws:lambda:us-east-1:371751795928:function:resources_api
tag_api - arn:aws:lambda:us-east-1:371751795928:function:tag_api
thumbnail_generator - arn:aws:lambda:us-east-1:371751795928:function:thumbnail_generator
s3_thumbnail_trigger - arn:aws:lambda:us-east-1:371751795928:function:s3_thumbnail_trigger
url_analysis_api - arn:aws:lambda:us-east-1:371751795928:function:url_analysis_api
article_analysis_api - arn:aws:lambda:us-east-1:371751795928:function:article_analysis_api
video_list_api - arn:aws:lambda:us-east-1:371751795928:function:video_list_api
paypal_billing_api - arn:aws:lambda:us-east-1:371751795928:function:paypal_billing_api
prayer_api - arn:aws:lambda:us-east-1:371751795928:function:prayer_api
notifications_api - arn:aws:lambda:us-east-1:371751795928:function:notifications_api
downloader - arn:aws:lambda:us-east-1:371751795928:function:downloader
```

---

## Step 4: Create API Gateway Module

### Directory Setup
```bash
mkdir -p terraform/modules/api-gateway
cd terraform/modules/api-gateway
```

### Create main.tf

**File**: `terraform/modules/api-gateway/main.tf`

```hcl
# REST API
resource "aws_api_gateway_rest_api" "this" {
  name        = var.api_name
  description = var.description

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = var.tags
}

# Deployment
resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id

  triggers = {
    redeployment = timestamp()
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_rest_api.this
  ]
}

# Stage
resource "aws_api_gateway_stage" "this" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = var.stage_name

  tags = var.tags
}

# CORS Gateway Responses
resource "aws_api_gateway_gateway_response" "cors_4xx" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  response_type = "DEFAULT_4XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,PUT,DELETE,OPTIONS'"
  }
}

resource "aws_api_gateway_gateway_response" "cors_5xx" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  response_type = "DEFAULT_5XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,PUT,DELETE,OPTIONS'"
  }
}
```

**Data Source**: 
- API Gateway best practices documentation
- Existing API configurations from AWS CLI
- CORS requirements from frontend code

### Create variables.tf

**File**: `terraform/modules/api-gateway/variables.tf`

```hcl
variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "description" {
  description = "Description of the API Gateway"
  type        = string
  default     = ""
}

variable "stage_name" {
  description = "Name of the deployment stage"
  type        = string
  default     = "prod"
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

### Create outputs.tf

**File**: `terraform/modules/api-gateway/outputs.tf`

```hcl
output "api_id" {
  description = "The ID of the REST API"
  value       = aws_api_gateway_rest_api.this.id
}

output "root_resource_id" {
  description = "The resource ID of the REST API root"
  value       = aws_api_gateway_rest_api.this.root_resource_id
}

output "invoke_url" {
  description = "The URL to invoke the API"
  value       = aws_api_gateway_stage.this.invoke_url
}

output "execution_arn" {
  description = "The execution ARN of the REST API"
  value       = aws_api_gateway_rest_api.this.execution_arn
}
```

---

## Step 5: Create Lambda Integration Module

### Directory Setup
```bash
mkdir -p terraform/modules/api-gateway-lambda-integration
cd terraform/modules/api-gateway-lambda-integration
```

### Create main.tf

**File**: `terraform/modules/api-gateway-lambda-integration/main.tf`

```hcl
# API Gateway Resource
resource "aws_api_gateway_resource" "this" {
  rest_api_id = var.api_id
  parent_id   = var.parent_id
  path_part   = var.path_part
}

# API Gateway Method (POST, GET, etc.)
resource "aws_api_gateway_method" "this" {
  rest_api_id   = var.api_id
  resource_id   = aws_api_gateway_resource.this.id
  http_method   = var.http_method
  authorization = var.authorization
}

# Lambda Integration
resource "aws_api_gateway_integration" "this" {
  rest_api_id             = var.api_id
  resource_id             = aws_api_gateway_resource.this.id
  http_method             = aws_api_gateway_method.this.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

# Lambda Permission
resource "aws_lambda_permission" "this" {
  statement_id  = "AllowAPIGatewayInvoke-${var.path_part}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# CORS OPTIONS Method
resource "aws_api_gateway_method" "options" {
  rest_api_id   = var.api_id
  resource_id   = aws_api_gateway_resource.this.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# CORS OPTIONS Integration (MOCK)
resource "aws_api_gateway_integration" "options" {
  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# CORS OPTIONS Method Response
resource "aws_api_gateway_method_response" "options" {
  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

# CORS OPTIONS Integration Response
resource "aws_api_gateway_integration_response" "options" {
  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options.http_method
  status_code = aws_api_gateway_method_response.options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,PUT,DELETE,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.options
  ]
}
```

**Data Source**:
- AWS API Gateway Lambda proxy integration documentation
- CORS preflight requirements (OPTIONS method)
- Existing API configurations

### Create variables.tf

**File**: `terraform/modules/api-gateway-lambda-integration/variables.tf`

```hcl
variable "api_id" {
  description = "The ID of the REST API"
  type        = string
}

variable "parent_id" {
  description = "The ID of the parent resource"
  type        = string
}

variable "path_part" {
  description = "The path part for this resource"
  type        = string
}

variable "http_method" {
  description = "The HTTP method"
  type        = string
  default     = "ANY"
}

variable "authorization" {
  description = "The type of authorization"
  type        = string
  default     = "NONE"
}

variable "lambda_invoke_arn" {
  description = "The ARN to invoke the Lambda function"
  type        = string
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "api_execution_arn" {
  description = "The execution ARN of the REST API"
  type        = string
}
```

### Create outputs.tf

**File**: `terraform/modules/api-gateway-lambda-integration/outputs.tf`

```hcl
output "resource_id" {
  description = "The ID of the API Gateway resource"
  value       = aws_api_gateway_resource.this.id
}

output "resource_path" {
  description = "The full path of the API Gateway resource"
  value       = aws_api_gateway_resource.this.path
}
```

---

## Step 6: Use Modules in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# Unified API Gateway
module "unified_api" {
  source = "../../modules/api-gateway"

  api_name    = "ministry-platform-api"
  description = "Unified API for Christian Conservative Platform"
  stage_name  = "prod"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Auth API Integration
module "api_integration_auth" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id              = module.unified_api.api_id
  parent_id           = module.unified_api.root_resource_id
  path_part           = "auth"
  http_method         = "ANY"
  lambda_invoke_arn   = module.lambda_auth_api.invoke_arn
  lambda_function_name = module.lambda_auth_api.function_name
  api_execution_arn   = module.unified_api.execution_arn
}

# Admin API Integration
module "api_integration_admin" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id              = module.unified_api.api_id
  parent_id           = module.unified_api.root_resource_id
  path_part           = "admin"
  http_method         = "ANY"
  lambda_invoke_arn   = module.lambda_admin_api.invoke_arn
  lambda_function_name = module.lambda_admin_api.function_name
  api_execution_arn   = module.unified_api.execution_arn
}

# ... (repeat for all 14 endpoints)
```

**Data Source**: Lambda function names and ARNs from Step 3

---

## Step 7: Deploy Unified API

### Initialize and Plan
```bash
cd terraform/environments/prod
terraform init
terraform plan
```

**Expected Output**:
```
Plan: 60 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + api_gateway_url = (known after apply)
  + api_endpoints   = {
      + admin         = (known after apply)
      + articles      = (known after apply)
      + auth          = (known after apply)
      ...
    }
```

### Apply Configuration
```bash
terraform apply
```

**Output**:
```
Apply complete! Resources: 60 added, 0 changed, 0 destroyed.

Outputs:

api_gateway_url = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"
api_endpoints = {
  "admin" = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/admin"
  "articles" = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/articles"
  "auth" = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth"
  ...
}
```

---

## Step 8: Test API Endpoints

### Test Auth Endpoint
```bash
curl -X POST https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Test CORS Preflight
```bash
curl -X OPTIONS https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

**Expected Response Headers**:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
Access-Control-Allow-Headers: Content-Type,Authorization
```

### Verify All Endpoints
```bash
# Test each endpoint
for endpoint in auth admin articles news comments contributors resources videos tags download paypal analyze prayer notifications; do
  echo "Testing /$endpoint..."
  curl -X OPTIONS "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/$endpoint" -I
done
```

---

## Step 9: Troubleshoot CORS Issue

### Problem Discovered
After deployment, CORS preflight requests returned 403 errors.

### Investigation Commands
```bash
# Check if OPTIONS method exists
aws apigateway get-resources --rest-api-id diz6ceeb22 --query 'items[?path==`/admin`]'

# Get resource ID
RESOURCE_ID=sru3e4

# Check OPTIONS method
aws apigateway get-method --rest-api-id diz6ceeb22 --resource-id $RESOURCE_ID --http-method OPTIONS

# Check integration
aws apigateway get-integration --rest-api-id diz6ceeb22 --resource-id $RESOURCE_ID --http-method OPTIONS

# Check integration response
aws apigateway get-integration-response --rest-api-id diz6ceeb22 --resource-id $RESOURCE_ID --http-method OPTIONS --status-code 200
```

### Root Cause
OPTIONS methods were created but API Gateway deployment wasn't triggered, so they weren't active.

### Solution
```bash
# Manual deployment (one-time fix)
aws apigateway create-deployment --rest-api-id diz6ceeb22 --stage-name prod
```

**Output**:
```json
{
    "id": "ksnta7",
    "createdDate": "2026-02-10T15:30:00Z"
}
```

### Permanent Fix
Updated `terraform/modules/api-gateway/main.tf`:

```hcl
# Changed deployment trigger from:
triggers = {
  redeployment = sha1(jsonencode(aws_api_gateway_rest_api.this.body))
}

# To:
triggers = {
  redeployment = timestamp()
}
```

**Reason**: `body` attribute is null for REST APIs without OpenAPI specs. `timestamp()` forces deployment on every apply.

---

## Step 10: Update Frontend URLs

### Find All API URL References
```bash
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

# Search for old API URLs
grep -r "execute-api" *.html *.js
```

### Replace Old URLs
```javascript
// Old (12 different APIs)
const AUTH_API = "https://f3g6h1j4k8.execute-api.us-east-1.amazonaws.com/prod";
const ADMIN_API = "https://r8x3k9m2l5.execute-api.us-east-1.amazonaws.com/prod";
// ... 10 more

// New (1 unified API)
const API_BASE = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod";
const AUTH_API = `${API_BASE}/auth`;
const ADMIN_API = `${API_BASE}/admin`;
// ... etc
```

### Test Frontend
1. Open admin dashboard
2. Test login (auth endpoint)
3. Test CRUD operations (admin endpoint)
4. Verify CORS works (no console errors)

---

## Key Learnings

### API Gateway Deployment
- **Deployment is separate from configuration**: Creating resources doesn't activate them
- **Deployment trigger is critical**: Use `timestamp()` for automatic deployments
- **Stage is required**: Deployment alone isn't enough, must have stage

### CORS Configuration
- **Two levels of CORS**: Gateway responses (4xx/5xx) and OPTIONS methods (preflight)
- **OPTIONS must be MOCK**: Can't use Lambda for preflight (adds latency)
- **Headers must match**: Frontend request headers must match allowed headers

### Lambda Proxy Integration
- **Always use POST**: Even for GET requests, integration method is POST
- **AWS_PROXY type**: Passes entire request to Lambda, Lambda returns full response
- **Permissions required**: API Gateway needs explicit permission to invoke Lambda

---

## Troubleshooting

### Issue: 403 Forbidden on OPTIONS requests
**Cause**: API Gateway deployment not triggered  
**Solution**: Run `aws apigateway create-deployment` or fix deployment trigger

### Issue: CORS headers missing
**Cause**: OPTIONS method not configured or integration response missing  
**Solution**: Verify OPTIONS method, integration, and integration response exist

### Issue: Lambda not invoked
**Cause**: Missing Lambda permission  
**Solution**: Add `aws_lambda_permission` resource with API Gateway principal

### Issue: 502 Bad Gateway
**Cause**: Lambda returning invalid response format  
**Solution**: Ensure Lambda returns `{statusCode, headers, body}` structure

---

## Related Files
- [API Gateway Module](../../modules/api-gateway/main.tf)
- [Lambda Integration Module](../../modules/api-gateway-lambda-integration/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
