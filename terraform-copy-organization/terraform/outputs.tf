# Account Information
output "production_account_id" {
  description = "Production AWS account ID"
  value       = var.production_account_id
}

output "child_account_id" {
  description = "Child AWS account ID"
  value       = var.child_account_id
}

# IAM Role
output "lambda_execution_role_arn" {
  description = "ARN of Lambda execution role"
  value       = aws_iam_role.lambda_execution.arn
}

# S3 Bucket
output "s3_bucket_name" {
  description = "Name of S3 bucket"
  value       = aws_s3_bucket.main.id
}

output "s3_bucket_arn" {
  description = "ARN of S3 bucket"
  value       = aws_s3_bucket.main.arn
}

# DynamoDB Table
output "dynamodb_table_name" {
  description = "Name of DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "dynamodb_table_arn" {
  description = "ARN of DynamoDB table"
  value       = aws_dynamodb_table.main.arn
}

# Lambda Function
output "lambda_function_name" {
  description = "Name of Lambda function"
  value       = aws_lambda_function.main.function_name
}

output "lambda_function_arn" {
  description = "ARN of Lambda function"
  value       = aws_lambda_function.main.arn
}

# API Gateway
output "api_gateway_id" {
  description = "ID of API Gateway"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_endpoint" {
  description = "Invoke URL of API Gateway"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}"
}

# SNS Topic
output "sns_topic_arn" {
  description = "ARN of SNS topic"
  value       = aws_sns_topic.alerts.arn
}

# CloudWatch Log Group
output "log_group_name" {
  description = "Name of CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda.name
}

# Summary
output "deployment_summary" {
  description = "Summary of deployed resources"
  value = {
    account     = var.child_account_id
    region      = var.aws_region
    environment = var.environment
    resources = {
      s3_bucket       = aws_s3_bucket.main.id
      dynamodb_table  = aws_dynamodb_table.main.name
      lambda_function = aws_lambda_function.main.function_name
      api_gateway     = aws_api_gateway_rest_api.main.name
      sns_topic       = aws_sns_topic.alerts.name
    }
  }
}
