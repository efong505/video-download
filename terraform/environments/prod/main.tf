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

# IAM Role for Lambda Functions
module "lambda_execution_role" {
  source = "../../modules/iam-role"

  role_name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "edgelambda.amazonaws.com"
          ]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
    "arn:aws:iam::aws:policy/AmazonSESFullAccess",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonSNSFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
    "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
  ]

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
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
  layers = [
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
# DynamoDB Tables
# ============================================

# Articles table
module "dynamodb_articles" {
  source = "../../modules/dynamodb"

  table_name   = "articles"
  hash_key     = "article_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "article_id", type = "S" }
  ]
}

# Users table
module "dynamodb_users" {
  source = "../../modules/dynamodb"

  table_name   = "users"
  hash_key     = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "email", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "email-index"
      hash_key        = "email"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}

# News table
module "dynamodb_news" {
  source = "../../modules/dynamodb"

  table_name   = "news-table"
  hash_key     = "news_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "news_id", type = "S" }
  ]
}

# Comments table
module "dynamodb_comments" {
  source = "../../modules/dynamodb"

  table_name   = "comments"
  hash_key     = "comment_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "comment_id", type = "S" }
  ]
}

# Video metadata table
module "dynamodb_video_metadata" {
  source = "../../modules/dynamodb"

  table_name   = "video-metadata"
  hash_key     = "video_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "video_id", type = "S" }
  ]
}

# Resources table
module "dynamodb_resources" {
  source = "../../modules/dynamodb"

  table_name   = "resources-table"
  hash_key     = "resource_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "resource_id", type = "S" }
  ]
}

# Contributors table
module "dynamodb_contributors" {
  source = "../../modules/dynamodb"

  table_name   = "contributors"
  hash_key     = "contributor_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "contributor_id", type = "S" }
  ]
}

# Rate limits table
module "dynamodb_rate_limits" {
  source = "../../modules/dynamodb"

  table_name    = "rate-limits"
  hash_key      = "rate_key"
  billing_mode  = "PAY_PER_REQUEST"
  ttl_enabled   = true
  ttl_attribute = "ttl"

  attributes = [
    { name = "rate_key", type = "S" }
  ]
}

# Book subscribers table
module "dynamodb_book_subscribers" {
  source = "../../modules/dynamodb"

  table_name   = "book-subscribers"
  hash_key     = "email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "email", type = "S" }
  ]
}

# Book purchases table
module "dynamodb_book_purchases" {
  source = "../../modules/dynamodb"

  table_name   = "book_purchases"
  hash_key     = "transaction_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "transaction_id", type = "S" }
  ]
}

# Notifications table
module "dynamodb_notifications" {
  source = "../../modules/dynamodb"

  table_name   = "notifications"
  hash_key     = "notification_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "notification_id", type = "S" }
  ]
}

# Events table
module "dynamodb_events" {
  source = "../../modules/dynamodb"

  table_name   = "events"
  hash_key     = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" }
  ]
}

# Prayer requests table
module "dynamodb_prayer_requests" {
  source = "../../modules/dynamodb"

  table_name   = "prayer-requests"
  hash_key     = "request_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "request_id", type = "S" }
  ]
}

# Video analytics table
module "dynamodb_video_analytics" {
  source = "../../modules/dynamodb"

  table_name   = "video-analytics"
  hash_key     = "video_id"
  range_key    = "timestamp"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "video_id", type = "S" },
    { name = "timestamp", type = "N" }
  ]
}

# Video playlists table
module "dynamodb_video_playlists" {
  source = "../../modules/dynamodb"

  table_name   = "video-playlists"
  hash_key     = "playlist_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "playlist_id", type = "S" }
  ]
}

# Download jobs table
module "dynamodb_download_jobs" {
  source = "../../modules/dynamodb"

  table_name   = "download-jobs"
  hash_key     = "job_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "job_id", type = "S" }
  ]
}

# Testimonies table
module "dynamodb_testimonies" {
  source = "../../modules/dynamodb"

  table_name   = "testimonies"
  hash_key     = "testimonyId"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "testimonyId", type = "S" },
    { name = "userEmail", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "UserEmailIndex"
      hash_key        = "userEmail"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}

# Testimony users table
module "dynamodb_testimony_users" {
  source = "../../modules/dynamodb"

  table_name   = "testimony-users"
  hash_key     = "email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "email", type = "S" }
  ]
}

# Candidates table
module "dynamodb_candidates" {
  source = "../../modules/dynamodb"

  table_name   = "candidates"
  hash_key     = "candidate_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "candidate_id", type = "S" }
  ]
}

# Races table
module "dynamodb_races" {
  source = "../../modules/dynamodb"

  table_name   = "races"
  hash_key     = "race_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "race_id", type = "S" }
  ]
}

# State summaries table
module "dynamodb_state_summaries" {
  source = "../../modules/dynamodb"

  table_name   = "state-summaries"
  hash_key     = "state"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "state", type = "S" }
  ]
}

# Election events table
module "dynamodb_election_events" {
  source = "../../modules/dynamodb"

  table_name   = "election-events"
  hash_key     = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" }
  ]
}

# Email subscribers table
module "dynamodb_email_subscribers" {
  source = "../../modules/dynamodb"

  table_name   = "email-subscribers"
  hash_key     = "email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "email", type = "S" }
  ]
}

# Email events table
module "dynamodb_email_events" {
  source = "../../modules/dynamodb"

  table_name   = "email-events"
  hash_key     = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" }
  ]
}

# Newsletters table
module "dynamodb_newsletters" {
  source = "../../modules/dynamodb"

  table_name   = "newsletters"
  hash_key     = "newsletter_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "newsletter_id", type = "S" }
  ]
}

# Newsletter campaigns table
module "dynamodb_newsletter_campaigns" {
  source = "../../modules/dynamodb"

  table_name   = "newsletter_campaigns"
  hash_key     = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "campaign_id", type = "S" }
  ]
}

# Newsletter templates table
module "dynamodb_newsletter_templates" {
  source = "../../modules/dynamodb"

  table_name   = "newsletter_templates"
  hash_key     = "template_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "template_id", type = "S" }
  ]
}

# Newsletter analytics table
module "dynamodb_newsletter_analytics" {
  source = "../../modules/dynamodb"

  table_name   = "newsletter_analytics"
  hash_key     = "analytics_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "analytics_id", type = "S" }
  ]
}

# User email subscribers table
module "dynamodb_user_email_subscribers" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-subscribers"
  hash_key     = "subscriber_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "subscriber_id", type = "S" }
  ]
}

# User email campaigns table
module "dynamodb_user_email_campaigns" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-campaigns"
  hash_key     = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "campaign_id", type = "S" }
  ]
}

# User email events table
module "dynamodb_user_email_events" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-events"
  hash_key     = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" }
  ]
}

# Pending changes table
module "dynamodb_pending_changes" {
  source = "../../modules/dynamodb"

  table_name   = "pending-changes"
  hash_key     = "change_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "change_id", type = "S" }
  ]
}

# User flags table
module "dynamodb_user_flags" {
  source = "../../modules/dynamodb"

  table_name   = "user-flags"
  hash_key     = "flag_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "flag_id", type = "S" }
  ]
}

# Admin users table
module "dynamodb_admin_users" {
  source = "../../modules/dynamodb"

  table_name   = "admin-users"
  hash_key     = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" }
  ]
}

# Templates table
module "dynamodb_templates" {
  source = "../../modules/dynamodb"

  table_name   = "Templates"
  hash_key     = "template_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "template_id", type = "S" }
  ]
}

# Cards table
module "dynamodb_cards" {
  source = "../../modules/dynamodb"

  table_name   = "Cards"
  hash_key     = "card_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "card_id", type = "S" }
  ]
}

# Cart table
module "dynamodb_cart" {
  source = "../../modules/dynamodb"

  table_name   = "Cart"
  hash_key     = "cart_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "cart_id", type = "S" }
  ]
}

# Orders table
module "dynamodb_orders" {
  source = "../../modules/dynamodb"

  table_name   = "Orders"
  hash_key     = "order_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "order_id", type = "S" }
  ]
}

# Products table
module "dynamodb_products" {
  source = "../../modules/dynamodb"

  table_name   = "Products"
  hash_key     = "product_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "product_id", type = "S" }
  ]
}

# Reviews table
module "dynamodb_reviews" {
  source = "../../modules/dynamodb"

  table_name   = "Reviews"
  hash_key     = "review_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "review_id", type = "S" }
  ]
}

# Storage files table
module "dynamodb_storage_files" {
  source = "../../modules/dynamodb"

  table_name   = "StorageFiles"
  hash_key     = "file_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "file_id", type = "S" }
  ]
}

# Storage users table
module "dynamodb_storage_users" {
  source = "../../modules/dynamodb"

  table_name   = "StorageUsers"
  hash_key     = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" }
  ]
}

# Users legacy table
module "dynamodb_users_legacy" {
  source = "../../modules/dynamodb"

  table_name   = "Users"
  hash_key     = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" }
  ]
}

# Website configs table
module "dynamodb_website_configs" {
  source = "../../modules/dynamodb"

  table_name   = "WebsiteConfigs"
  hash_key     = "config_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "config_id", type = "S" }
  ]
}

# News articles legacy table
module "dynamodb_news_articles" {
  source = "../../modules/dynamodb"

  table_name   = "NewsArticles"
  hash_key     = "article_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "article_id", type = "S" }
  ]
}

# Demo table
module "dynamodb_demo_table" {
  source = "../../modules/dynamodb"

  table_name   = "DemoTable"
  hash_key     = "id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "id", type = "S" }
  ]
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
