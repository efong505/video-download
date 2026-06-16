# AWS Region
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

# Production Account ID
variable "production_account_id" {
  description = "Production AWS account ID"
  type        = string
  default     = "371751795928"
}

# Child Account ID
variable "child_account_id" {
  description = "Child AWS account ID (ed@ekewaka)"
  type        = string
  # No default - must be provided
}

# Cross-Account Role ARN
variable "child_account_role_arn" {
  description = "ARN of the cross-account role in child account"
  type        = string
  # Will be constructed from child_account_id
}

# External ID for AssumeRole
variable "external_id" {
  description = "External ID for cross-account role assumption"
  type        = string
  default     = "terraform-copy-tutorial"
  sensitive   = true
}

# Project Name
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "infra-copy-tutorial"
}

# Environment
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "tutorial"
}

# S3 Bucket Name
variable "s3_bucket_name" {
  description = "Name for S3 bucket (must be globally unique)"
  type        = string
  # Will be constructed with account ID for uniqueness
}

# Lambda Function Name
variable "lambda_function_name" {
  description = "Name for Lambda function"
  type        = string
  default     = "sample-function-tutorial"
}

# DynamoDB Table Name
variable "dynamodb_table_name" {
  description = "Name for DynamoDB table"
  type        = string
  default     = "sample-table-tutorial"
}

# SNS Topic Name
variable "sns_topic_name" {
  description = "Name for SNS topic"
  type        = string
  default     = "tutorial-alerts"
}

# API Gateway Name
variable "api_gateway_name" {
  description = "Name for API Gateway"
  type        = string
  default     = "sample-api-tutorial"
}
