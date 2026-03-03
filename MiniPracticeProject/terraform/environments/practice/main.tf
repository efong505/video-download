terraform {
  required_version = ">=1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MiniPracticeProject"
      Environment = "practice"
      ManagedBy   = "Terraform"
    }
  }
}

# S3 Bucket Module
module "s3_practice" {
  source = "../../modules/s3-practice"

  bucket_prefix = var.bucket_prefix
  environment   = "practice"
}

# DynamoDB Table Module
module "dynamodb_practice" {
  source = "../../modules/dynamodb-practice"

  table_name  = var.dynamodb_table_name
  hash_key    = "id"
  environment = "practice"
}

# Lambda Function Module
module "lambda_practice" {
  source = "../../modules/lambda-practice"

  function_name = var.lambda_function_name
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = var.lambda_role_arn
  environment   = "practice"
}

# Cloudwatch Log Group Module
module "cloudwatch_practice" {
  source = "../../modules/cloudwatch-practice"

  log_group_name = "/aws/lambda/${var.lambda_function_name}"
  retention_days = 7
  environment    = "practice"
}

# SNS Topic module
module "sns_practice" {
  source = "../../modules/sns-practice"

  topic_name  = var.sns_topic_name
  environment = "practice"
}