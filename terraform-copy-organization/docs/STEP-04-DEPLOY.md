# STEP 04: Deploy Infrastructure

**Goal**: Create main.tf and deploy infrastructure to child account

**Time**: 30-40 minutes (first time), 10-15 minutes (practice runs)

---

## Overview

You'll:
1. Create the Lambda function code
2. Create main.tf with all infrastructure resources
3. Review the Terraform plan
4. Deploy to child account
5. Verify resources were created

---

## Step 4.1: Create Lambda Function Code

**First, create the Lambda function that will be deployed.**

```powershell
# Navigate to lambda-code directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\lambda-code

# Create sample-function directory
mkdir sample-function
cd sample-function

# Create index.py
@'
import json
import boto3
import os
from datetime import datetime

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Get environment variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
S3_BUCKET = os.environ.get('S3_BUCKET')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'tutorial')

def lambda_handler(event, context):
    """
    Sample Lambda function that demonstrates:
    - DynamoDB operations
    - S3 operations
    - SNS notifications
    - API Gateway integration
    """
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        action = body.get('action', 'test')
        
        # Generate unique ID
        timestamp = int(datetime.now().timestamp())
        item_id = f"item-{timestamp}"
        
        # Perform action based on request
        if action == 'write_dynamodb':
            result = write_to_dynamodb(item_id, timestamp, body)
        elif action == 'write_s3':
            result = write_to_s3(item_id, body)
        elif action == 'send_notification':
            result = send_sns_notification(body)
        else:
            result = test_function()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Success',
                'action': action,
                'result': result,
                'environment': ENVIRONMENT,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Error',
                'error': str(e)
            })
        }

def test_function():
    """Test function to verify Lambda is working"""
    return {
        'status': 'Lambda function is working',
        'dynamodb_table': DYNAMODB_TABLE,
        's3_bucket': S3_BUCKET,
        'sns_topic': SNS_TOPIC_ARN
    }

def write_to_dynamodb(item_id, timestamp, data):
    """Write item to DynamoDB table"""
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    item = {
        'id': item_id,
        'timestamp': timestamp,
        'status': 'active',
        'data': json.dumps(data),
        'created_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=item)
    
    return {
        'dynamodb_write': 'success',
        'item_id': item_id
    }

def write_to_s3(item_id, data):
    """Write object to S3 bucket"""
    key = f"test-data/{item_id}.json"
    
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType='application/json'
    )
    
    return {
        's3_write': 'success',
        'bucket': S3_BUCKET,
        'key': key
    }

def send_sns_notification(data):
    """Send SNS notification"""
    message = data.get('message', 'Test notification from Lambda')
    
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='Tutorial Lambda Notification',
        Message=message
    )
    
    return {
        'sns_publish': 'success',
        'message_id': response['MessageId']
    }
'@ | Out-File -FilePath index.py -Encoding utf8

Write-Host "✅ Created index.py"
```

---

## Step 4.2: Package Lambda Function

```powershell
# Create ZIP file for Lambda deployment
Compress-Archive -Path index.py -DestinationPath sample-function.zip -Force

Write-Host "✅ Created sample-function.zip"

# Verify ZIP was created
if (Test-Path sample-function.zip) {
    Write-Host "✅ Lambda package ready: sample-function.zip"
    Write-Host "   Size: $((Get-Item sample-function.zip).Length) bytes"
} else {
    Write-Host "❌ Failed to create ZIP file"
}
```

---

## Step 4.3: Create main.tf (Part 1 - IAM and S3)

```powershell
# Navigate to terraform directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform

# Create main.tf with IAM and S3 resources
@'
# Main Infrastructure Configuration
# This file creates a simplified copy of production infrastructure in child account

# ============================================================================
# IAM ROLE FOR LAMBDA
# ============================================================================

# Lambda execution role
resource "aws_iam_role" "lambda_execution" {
  provider = aws.child
  name     = "lambda-execution-role-tutorial"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Name = "lambda-execution-role-tutorial"
  }
}

# Attach AWS managed policies
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_sns" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

# ============================================================================
# S3 BUCKET
# ============================================================================

# S3 bucket (similar to my-video-downloads-bucket in production)
resource "aws_s3_bucket" "main" {
  provider = aws.child
  bucket   = var.s3_bucket_name

  tags = {
    Name        = var.s3_bucket_name
    Description = "Tutorial S3 bucket - copy of production pattern"
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "main" {
  provider = aws.child
  bucket   = aws_s3_bucket.main.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  provider = aws.child
  bucket   = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CORS configuration
resource "aws_s3_bucket_cors_configuration" "main" {
  provider = aws.child
  bucket   = aws_s3_bucket.main.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# Block public access (security best practice)
resource "aws_s3_bucket_public_access_block" "main" {
  provider = aws.child
  bucket   = aws_s3_bucket.main.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
'@ | Out-File -FilePath main.tf -Encoding utf8

Write-Host "✅ Created main.tf (Part 1: IAM and S3)"
```

---

## Step 4.4: Add DynamoDB and Lambda to main.tf

```powershell
# Append DynamoDB and Lambda resources
@'

# ============================================================================
# DYNAMODB TABLE
# ============================================================================

# DynamoDB table (similar to production tables)
resource "aws_dynamodb_table" "main" {
  provider       = aws.child
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  range_key      = "timestamp"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "status"
    type = "S"
  }

  # Global Secondary Index
  global_secondary_index {
    name            = "status-index"
    hash_key        = "status"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  # Enable point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name        = var.dynamodb_table_name
    Description = "Tutorial DynamoDB table - copy of production pattern"
  }
}

# ============================================================================
# LAMBDA FUNCTION
# ============================================================================

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda" {
  provider          = aws.child
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7

  tags = {
    Name = "${var.lambda_function_name}-logs"
  }
}

# Lambda function
resource "aws_lambda_function" "main" {
  provider         = aws.child
  filename         = "../lambda-code/sample-function/sample-function.zip"
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_execution.arn
  handler          = "index.lambda_handler"
  source_code_hash = filebase64sha256("../lambda-code/sample-function/sample-function.zip")
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.main.name
      S3_BUCKET      = aws_s3_bucket.main.id
      SNS_TOPIC_ARN  = aws_sns_topic.alerts.arn
      ENVIRONMENT    = var.environment
    }
  }

  tags = {
    Name        = var.lambda_function_name
    Description = "Tutorial Lambda function - copy of production pattern"
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_basic
  ]
}
'@ | Out-File -FilePath main.tf -Append -Encoding utf8

Write-Host "✅ Added DynamoDB and Lambda to main.tf"
```

---

## Step 4.5: Add API Gateway to main.tf

```powershell
# Append API Gateway resources
@'

# ============================================================================
# API GATEWAY
# ============================================================================

# REST API
resource "aws_api_gateway_rest_api" "main" {
  provider    = aws.child
  name        = var.api_gateway_name
  description = "Tutorial API Gateway - copy of production pattern"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = var.api_gateway_name
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "sample" {
  provider    = aws.child
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "sample"
}

# API Gateway Method
resource "aws_api_gateway_method" "sample_post" {
  provider      = aws.child
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.sample.id
  http_method   = "POST"
  authorization = "NONE"
}

# Lambda Integration
resource "aws_api_gateway_integration" "lambda" {
  provider                = aws.child
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.sample.id
  http_method             = aws_api_gateway_method.sample_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.main.invoke_arn
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  provider      = aws.child
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "main" {
  provider    = aws.child
  rest_api_id = aws_api_gateway_rest_api.main.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.sample.id,
      aws_api_gateway_method.sample_post.id,
      aws_api_gateway_integration.lambda.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.lambda
  ]
}

# API Gateway Stage
resource "aws_api_gateway_stage" "main" {
  provider      = aws.child
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.environment

  tags = {
    Name = "${var.api_gateway_name}-${var.environment}"
  }
}
'@ | Out-File -FilePath main.tf -Append -Encoding utf8

Write-Host "✅ Added API Gateway to main.tf"
```

---

## Step 4.6: Add SNS and CloudWatch to main.tf

```powershell
# Append SNS and CloudWatch resources
@'

# ============================================================================
# SNS TOPIC
# ============================================================================

# SNS Topic for alerts
resource "aws_sns_topic" "alerts" {
  provider = aws.child
  name     = var.sns_topic_name

  tags = {
    Name        = var.sns_topic_name
    Description = "Tutorial SNS topic - copy of production pattern"
  }
}

# ============================================================================
# CLOUDWATCH ALARM
# ============================================================================

# CloudWatch Alarm for Lambda errors
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  provider            = aws.child
  alarm_name          = "${var.lambda_function_name}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Alert when Lambda function has more than 5 errors"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]

  tags = {
    Name = "${var.lambda_function_name}-error-alarm"
  }
}
'@ | Out-File -FilePath main.tf -Append -Encoding utf8

Write-Host "✅ Added SNS and CloudWatch to main.tf"
Write-Host "✅ main.tf is complete!"
```

---

## Step 4.7: Validate Configuration

```powershell
# Validate Terraform configuration
terraform validate

# Expected output:
# Success! The configuration is valid.
```

**If error**: Check syntax in main.tf

---

## Step 4.8: Review Terraform Plan

**This shows what Terraform will create WITHOUT actually creating it.**

```powershell
# Generate execution plan
terraform plan

# Review the output carefully
# You should see approximately 20+ resources to be created:
# - 1 IAM role
# - 4 IAM role policy attachments
# - 1 S3 bucket
# - 4 S3 bucket configurations
# - 1 DynamoDB table
# - 1 CloudWatch log group
# - 1 Lambda function
# - 1 API Gateway REST API
# - 1 API Gateway resource
# - 1 API Gateway method
# - 1 API Gateway integration
# - 1 Lambda permission
# - 1 API Gateway deployment
# - 1 API Gateway stage
# - 1 SNS topic
# - 1 CloudWatch alarm
```

**Review checklist**:
- [ ] All resources show `provider = aws.child`
- [ ] No resources being destroyed (should be all new)
- [ ] Resource names match your variables
- [ ] No errors in the plan

---

## Step 4.9: Deploy Infrastructure

**This actually creates the resources in your child account.**

```powershell
# Apply the Terraform configuration
terraform apply

# Terraform will show the plan again and ask for confirmation
# Type: yes

# Expected output:
# Apply complete! Resources: 20+ added, 0 changed, 0 destroyed.
#
# Outputs:
# api_gateway_endpoint = "https://xxxxx.execute-api.us-east-1.amazonaws.com/tutorial"
# child_account_id = "123456789012"
# dynamodb_table_name = "sample-table-tutorial"
# ...
```

**Deployment time**: 2-3 minutes

---

## Step 4.10: Save Outputs

```powershell
# Save outputs to file for reference
terraform output -json | Out-File -FilePath deployment-outputs.json -Encoding utf8

Write-Host "✅ Outputs saved to deployment-outputs.json"

# Display key outputs
Write-Host "`n=== Deployment Summary ===" -ForegroundColor Green
terraform output deployment_summary
```

---

## Step 4.11: Verification Checklist

After deployment, verify:

- [ ] `terraform apply` completed successfully
- [ ] No errors in output
- [ ] All resources created (20+ resources)
- [ ] Outputs displayed correctly
- [ ] deployment-outputs.json created

---

## Understanding What Was Created

### In Child Account

**IAM**:
- 1 Lambda execution role
- 4 policy attachments

**S3**:
- 1 bucket with versioning, encryption, CORS
- Public access blocked

**DynamoDB**:
- 1 table with GSI
- Point-in-time recovery enabled

**Lambda**:
- 1 function (Python 3.12)
- CloudWatch log group
- Environment variables configured

**API Gateway**:
- 1 REST API
- 1 resource (/sample)
- 1 method (POST)
- Lambda integration
- 1 stage (tutorial)

**SNS**:
- 1 topic for alerts

**CloudWatch**:
- 1 alarm for Lambda errors

---

## Troubleshooting

### Error: "Error assuming role"

**Cause**: Can't access child account

**Fix**: Verify cross-account role from Step 1:
```powershell
aws sts assume-role `
    --role-arn "arn:aws:iam::CHILD_ID:role/TerraformCrossAccountRole" `
    --role-session-name "test" `
    --external-id "terraform-copy-tutorial"
```

### Error: "Bucket name already exists"

**Cause**: S3 bucket names must be globally unique

**Fix**: Edit terraform.tfvars and change s3_bucket_name to something unique

### Error: "Lambda function code not found"

**Cause**: ZIP file doesn't exist or path is wrong

**Fix**: Verify ZIP exists:
```powershell
Test-Path ..\lambda-code\sample-function\sample-function.zip
```

### Error: "Invalid provider configuration"

**Cause**: terraform.tfvars not updated with child account ID

**Fix**: Edit terraform.tfvars and replace REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID

---

## Quick Reference

**Commands Used**:
- `terraform validate` - Check syntax
- `terraform plan` - Preview changes
- `terraform apply` - Deploy infrastructure
- `terraform output` - Show outputs

**Resources Created**: 20+
**Deployment Time**: 2-3 minutes
**Cost**: ~$0.02 per day

---

## Next Step

✅ **Infrastructure deployed!**

→ Continue to `STEP-05-VERIFY.md` to test the deployed infrastructure.

---

## Practice Tips

**For subsequent practice runs**:
1. Lambda code already exists - skip creation
2. main.tf already exists - just review
3. Run `terraform plan` to preview
4. Run `terraform apply` to deploy
5. Takes ~5 minutes total
