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

module "lambda_video_list_api" {
  source = "../../modules/lambda"

  function_name = "video-list-api"
  runtime       = "python3.11"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_video_tag_api" {
  source = "../../modules/lambda"

  function_name = "video-tag-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_url_analysis_api" {
  source = "../../modules/lambda"

  function_name = "url-analysis-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  layers        = ["arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1"]
  
  environment_variables = {}
}

module "lambda_paypal_billing_api" {
  source = "../../modules/lambda"

  function_name = "paypal-billing-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_video_downloader" {
  source = "../../modules/lambda"

  function_name = "video-downloader"
  runtime       = "python3.11"
  handler       = "index.lambda_handler"
  memory_size   = 2048
  timeout       = 900
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  layers        = [
        "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer-v2:1",
        "arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1"
  ]

  environment_variables = {}
}

module "lambda_thumbnail_generator" {
  source = "../../modules/lambda"

  function_name = "thumbnail-generator"
  runtime       = "python3.11"
  handler       = "index.lambda_handler"
  memory_size   = 1024
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  layers        = ["arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1"]

  environment_variables = {}
}

module "lambda_s3_thumbnail_trigger" {
  source = "../../modules/lambda"

  function_name = "s3-thumbnail-trigger"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 1024
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_video_download_router" {
  source = "../../modules/lambda"

  function_name = "video-download-router"
  runtime       = "python3.11"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_prayer_api" {
  source = "../../modules/lambda"

  function_name = "prayer_api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_events_api" {
  source = "../../modules/lambda"

  function_name = "events_api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

module "lambda_notifications_api" {
  source = "../../modules/lambda"

  function_name = "notifications_api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  
  environment_variables = {}
}

