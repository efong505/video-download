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
