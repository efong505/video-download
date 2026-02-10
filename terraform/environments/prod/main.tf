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


# ============================================
# Unified API Gateway
# ============================================

module "unified_api" {
  source = "../../modules/api-gateway"
  
  api_name        = "ministry-platform-api"
  api_description = "Unified API for Christian Conservative Platform"
  stage_name      = "prod"
}

# Auth endpoint
module "api_auth" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "auth"
  http_method          = "ANY"
  lambda_function_name = module.lambda_auth_api.function_name
  lambda_function_arn  = module.lambda_auth_api.function_arn
  enable_cors          = true
}

# Articles endpoint
module "api_articles" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "articles"
  http_method          = "ANY"
  lambda_function_name = module.lambda_articles_api.function_name
  lambda_function_arn  = module.lambda_articles_api.function_arn
  enable_cors          = true
}

# News endpoint
module "api_news" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "news"
  http_method          = "ANY"
  lambda_function_name = module.lambda_news_api.function_name
  lambda_function_arn  = module.lambda_news_api.function_arn
  enable_cors          = true
}

# Admin endpoint
module "api_admin" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "admin"
  http_method          = "ANY"
  lambda_function_name = module.lambda_admin_api.function_name
  lambda_function_arn  = module.lambda_admin_api.function_arn
  enable_cors          = true
}

# Comments endpoint
module "api_comments" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "comments"
  http_method          = "ANY"
  lambda_function_name = module.lambda_comments_api.function_name
  lambda_function_arn  = module.lambda_comments_api.function_arn
  enable_cors          = true
}

# Contributors endpoint
module "api_contributors" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "contributors"
  http_method          = "ANY"
  lambda_function_name = module.lambda_contributors_api.function_name
  lambda_function_arn  = module.lambda_contributors_api.function_arn
  enable_cors          = true
}

# Resources endpoint
module "api_resources" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "resources"
  http_method          = "ANY"
  lambda_function_name = module.lambda_resources_api.function_name
  lambda_function_arn  = module.lambda_resources_api.function_arn
  enable_cors          = true
}

# Videos endpoint
module "api_videos" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "videos"
  http_method          = "ANY"
  lambda_function_name = module.lambda_video_list_api.function_name
  lambda_function_arn  = module.lambda_video_list_api.function_arn
  enable_cors          = true
}

# Tags endpoint
module "api_tags" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "tags"
  http_method          = "ANY"
  lambda_function_name = module.lambda_video_tag_api.function_name
  lambda_function_arn  = module.lambda_video_tag_api.function_arn
  enable_cors          = true
}

# Download endpoint
module "api_download" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "download"
  http_method          = "ANY"
  lambda_function_name = module.lambda_video_download_router.function_name
  lambda_function_arn  = module.lambda_video_download_router.function_arn
  enable_cors          = true
}

# PayPal endpoint
module "api_paypal" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "paypal"
  http_method          = "ANY"
  lambda_function_name = module.lambda_paypal_billing_api.function_name
  lambda_function_arn  = module.lambda_paypal_billing_api.function_arn
  enable_cors          = true
}

# Analyze endpoint
module "api_analyze" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "analyze"
  http_method          = "ANY"
  lambda_function_name = module.lambda_url_analysis_api.function_name
  lambda_function_arn  = module.lambda_url_analysis_api.function_arn
  enable_cors          = true
}

# Prayer endpoint
module "api_prayer" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "prayer"
  http_method          = "ANY"
  lambda_function_name = module.lambda_prayer_api.function_name
  lambda_function_arn  = module.lambda_prayer_api.function_arn
  enable_cors          = true
}

# Notifications endpoint
module "api_notifications" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "notifications"
  http_method          = "ANY"
  lambda_function_name = module.lambda_notifications_api.function_name
  lambda_function_arn  = module.lambda_notifications_api.function_arn
  enable_cors          = true
}

# ============================================
# Outputs
# ============================================

output "api_gateway_url" {
  value       = module.unified_api.invoke_url
  description = "Base URL for the unified API Gateway"
}

output "api_gateway_id" {
  value       = module.unified_api.api_id
  description = "API Gateway ID"
}

output "api_endpoints" {
  value = {
    auth          = "${module.unified_api.invoke_url}/auth"
    articles      = "${module.unified_api.invoke_url}/articles"
    news          = "${module.unified_api.invoke_url}/news"
    admin         = "${module.unified_api.invoke_url}/admin"
    comments      = "${module.unified_api.invoke_url}/comments"
    contributors  = "${module.unified_api.invoke_url}/contributors"
    resources     = "${module.unified_api.invoke_url}/resources"
    videos        = "${module.unified_api.invoke_url}/videos"
    tags          = "${module.unified_api.invoke_url}/tags"
    download      = "${module.unified_api.invoke_url}/download"
    paypal        = "${module.unified_api.invoke_url}/paypal"
    analyze       = "${module.unified_api.invoke_url}/analyze"
    prayer        = "${module.unified_api.invoke_url}/prayer"
    notifications = "${module.unified_api.invoke_url}/notifications"
  }
  description = "All API endpoint URLs"
}
