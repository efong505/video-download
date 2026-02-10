# Production Environment - Main Configuration

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "techcross-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      Environment = "production"
      ManagedBy   = "Terraform"
      Project     = "ChristianConservativePlatform"
    }
  }
}

# S3 Buckets
module "s3_videos" {
  source = "../../modules/s3"
  
  bucket_name = "my-video-downloads-bucket"
  environment = "prod"
}

# Lambda Functions
module "lambda_admin_api" {
  source = "../../modules/lambda"
  
  function_name = "admin-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_auth_api" {
  source = "../../modules/lambda"
  
  function_name = "auth-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_articles_api" {
  source = "../../modules/lambda"
  
  function_name = "articles-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_news_api" {
  source = "../../modules/lambda"
  
  function_name = "news-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_comments_api" {
  source = "../../modules/lambda"
  
  function_name = "comments-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {} 
}

module "lambda_contributors_api" {
  source = "../../modules/lambda"
  
  function_name = "contributors-api"
  runtime       = "python3.11"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {} 
}

module "lambda_resources_api" {
  source = "../../modules/lambda"

  function_name = "resources-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {} 
}