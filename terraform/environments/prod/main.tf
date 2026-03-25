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
    bucket       = "techcross-terraform-state"
    key          = "prod/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
    profile      = "ekewaka"
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "ekewaka"

  default_tags {
    tags = {
      Environment = "production"
      ManagedBy   = "Terraform"
      Project     = "ChristianConservativePlatform"
    }
  }
}

# ============================================
# Route53 & ACM Certificates
# ============================================

# Get Route53 hosted zone
data "aws_route53_zone" "main" {
  name         = "christianconservativestoday.com."
  private_zone = false
}

# Production API certificate
module "acm_api_prod" {
  source = "../../modules/acm-certificate"

  domain_name    = "api.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "production"
    Purpose     = "API Gateway Custom Domain"
  }
}

# Staging API certificate
module "acm_api_staging" {
  source = "../../modules/acm-certificate"

  domain_name    = "api-staging.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "staging"
    Purpose     = "API Gateway Custom Domain"
  }
}

# ============================================
# API Gateway Endpoints
# ============================================

module "api_events" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "events"
  http_method          = "ANY"
  lambda_function_name = module.lambda_events_api.function_name
  lambda_function_arn  = module.lambda_events_api.function_arn
  enable_cors          = true
}

# ============================================
# API Gateway Custom Domains
# ============================================

# Production API custom domain
module "api_domain_prod" {
  source = "../../modules/api-gateway-domain-name"

  domain_name      = "api.christianconservativestoday.com"
  certificate_arn  = module.acm_api_prod.certificate_arn
  api_id           = module.unified_api.api_id
  stage_name       = "prod"
  base_path        = ""
  hosted_zone_id   = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "production"
    Purpose     = "API Custom Domain"
  }

  depends_on = [module.unified_api]
}

# Staging API custom domain
module "api_domain_staging" {
  source = "../../modules/api-gateway-domain-name"

  domain_name      = "api-staging.christianconservativestoday.com"
  certificate_arn  = module.acm_api_staging.certificate_arn
  api_id           = module.unified_api.api_id
  stage_name       = "staging"
  base_path        = ""
  hosted_zone_id   = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "staging"
    Purpose     = "API Custom Domain"
  }

  depends_on = [module.unified_api]
}

# ============================================
# S3 Buckets
# ============================================
module "s3_videos" {
  source = "../../modules/s3"
  
  bucket_name = "my-video-downloads-bucket"
  versioning_enabled = true
  environment = "prod"
  
}

# CloudFront Origin Access Control
module "cloudfront_oac" {
  source = "../../modules/cloudfront-oac"

  name        = "my-video-downloads-bucket.s3.us-east-1.amazonaws.com"
  description = "Origin Access Control for video downloads bucket"
}

# CloudFront Distribution
module "cloudfront_distribution" {
  source = "../../modules/cloudfront"

  bucket_name                  = "my-video-downloads-bucket"
  bucket_regional_domain_name  = module.s3_videos.bucket_regional_domain_name
  origin_access_control_id     = module.cloudfront_oac.id
  aliases                      = ["videos.mytestimony.click", "christianconservativestoday.com"]
  acm_certificate_arn          = "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4"
  comment                      = "Christian Conservative Platform CDN"
  default_root_object          = "index.html"
  price_class                  = "PriceClass_100"
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



# ============================================
# Lambda Layers
# ============================================

# yt-dlp Layer
module "layer_yt_dlp" {
  source = "../../modules/lambda-layer"

  layer_name          = "yt-dlp-layer-v2"
  description         = "yt-dlp binary for Lambda"
  compatible_runtimes = ["python3.11"]
}

# FFmpeg Layer
module "layer_ffmpeg" {
  source = "../../modules/lambda-layer"

  layer_name          = "ffmpeg-layer"
  description         = "FFmpeg binaries for video conversion"
  compatible_runtimes = ["python3.11"]
}

# Requests Layer
module "layer_requests" {
  source = "../../modules/lambda-layer"

  layer_name          = "requests-layer"
  compatible_runtimes = ["python3.9", "python3.10", "python3.11", "python3.12"]
}

# ============================================
# Lambda Functions
# ============================================
module "lambda_admin_api" {
  source = "../../modules/lambda"

  function_name = "admin-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_comments_handler" {
  source = "../../modules/lambda"

  function_name = "comments-handler"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

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
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_mountains_api" {
  source = "../../modules/lambda"

  function_name = "mountains-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_newsletter_api" {
  source = "../../modules/lambda"

  function_name = "newsletter_api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_digest_generator" {
  source = "../../modules/lambda"

  function_name = "digest_generator"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_scheduled_publisher" {
  source = "../../modules/lambda"

  function_name = "scheduled-publisher"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_feature_flags_api" {
  source = "../../modules/lambda"

  function_name = "feature-flags-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_auto_cache_monitor" {
  source = "../../modules/lambda"

  function_name = "auto-cache-monitor"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_playlists_api" {
  source = "../../modules/lambda"

  function_name = "playlists-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_contact_form_api" {
  source = "../../modules/lambda"

  function_name = "contact-form-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_email_subscription_handler" {
  source = "../../modules/lambda"

  function_name = "email-subscription-handler"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/service-role/email-subscription-handler-role-s3uqsrwg"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_email_drip_processor" {
  source = "../../modules/lambda"

  function_name = "email-drip-processor"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_manual_email_sender" {
  source = "../../modules/lambda"

  function_name = "manual-email-sender"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_ses_event_processor" {
  source = "../../modules/lambda"

  function_name = "ses-event-processor"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_article_meta_tags_edge" {
  source = "../../modules/lambda"

  function_name = "article-meta-tags-edge"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 5
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_user_email_api" {
  source = "../../modules/lambda"

  function_name = "user-email-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_forum_api" {
  source = "../../modules/lambda"

  function_name = "forum-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_business_api" {
  source = "../../modules/lambda"

  function_name = "business-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_book_delivery_api" {
  source = "../../modules/lambda"

  function_name = "book-delivery-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_boycott_api" {
  source = "../../modules/lambda"

  function_name = "boycott-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_tracking_api" {
  source = "../../modules/lambda"

  function_name = "tracking-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 15
  role_arn      = "arn:aws:iam::371751795928:role/tracking-api-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
module "lambda_email_sender" {
  source = "../../modules/lambda"

  function_name = "email-sender"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_news_scraper" {
  source = "../../modules/lambda"

  function_name = "NewsScraperLambda"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 512
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/NewsScraperLambdaRole"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_testimony_auth" {
  source = "../../modules/lambda"

  function_name = "testimony-auth"
  runtime       = "nodejs22.x"
  handler       = "auth.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_testimony_crud" {
  source = "../../modules/lambda"

  function_name = "testimony-crud"
  runtime       = "nodejs22.x"
  handler       = "testimony.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_testimony_admin" {
  source = "../../modules/lambda"

  function_name = "testimony-admin"
  runtime       = "nodejs22.x"
  handler       = "admin.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_testimony_email_sharing" {
  source = "../../modules/lambda"

  function_name = "testimony-email-sharing"
  runtime       = "nodejs22.x"
  handler       = "email-sharing.handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

module "lambda_testimony_email_ses" {
  source = "../../modules/lambda"

  function_name = "testimony-email-ses"
  runtime       = "nodejs22.x"
  handler       = "email-ses.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}

# Add this to main.tf after the other Lambda functions

# PayPal IPN Handler Lambda
module "lambda_paypal_ipn_handler" {
  source = "../../modules/lambda"

  function_name = "paypal-ipn-handler"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

# PayPal IPN endpoint
module "api_paypal_ipn" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "paypal-ipn"
  http_method          = "POST"
  lambda_function_name = module.lambda_paypal_ipn_handler.function_name
  lambda_function_arn  = module.lambda_paypal_ipn_handler.function_arn
  enable_cors          = false  # PayPal doesn't need CORS
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

# Staging stage
resource "aws_api_gateway_stage" "staging" {
  deployment_id = module.unified_api.deployment_id
  rest_api_id   = module.unified_api.api_id
  stage_name    = "staging"
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
  lambda_function_name = module.lambda_comments_handler.function_name
  lambda_function_arn  = module.lambda_comments_handler.function_arn
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
  range_key    = "timestamp"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" },
    { name = "timestamp", type = "N" }
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

# Mountain pledges table
module "dynamodb_mountain_pledges" {
  source = "../../modules/dynamodb"

  table_name = "mountain-pledges"
  hash_key = "user_id"
  range_key = "mountain"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" }
  ]
}

# Mountain Badges
module "dynamodb_mountain_badges" {
  source = "../../modules/dynamodb"

  table_name   = "mountain-badges"
  hash_key     = "badge_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "badge_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "user-index"
      hash_key        = "user_id"
      range_key       = "mountain"
      projection_type = "ALL"
    }
  ]
}

# Mountain Contributions
module "dynamodb_mountain_contributions" {
  source = "../../modules/dynamodb"

  table_name   = "mountain-contributions"
  hash_key     = "contribution_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "contribution_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" },
    { name = "contribution_date", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "user-index"
      hash_key        = "user_id"
      range_key       = "contribution_date"
      projection_type = "ALL"
    },
    {
      name            = "mountain-index"
      hash_key        = "mountain"
      range_key       = "contribution_date"
      projection_type = "ALL"
    }
  ]
}

# admin-users
module "dynamodb_admin_users" {
  source = "../../modules/dynamodb"

  table_name   = "admin-users"
  hash_key     = "username"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "username", type = "S" }
  ]
}

# Content Comments
module "dynamodb_content_comments" {
  source = "../../modules/dynamodb"

  table_name   = "content-comments"
  hash_key     = "content_id"
  range_key    = "comment_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "content_id", type = "S" },
    { name = "comment_id", type = "S" },
    { name = "created_at", type = "N" }
  ]

  global_secondary_indexes = [
    {
      name            = "CreatedAtIndex"
      hash_key        = "content_id"
      range_key       = "created_at"
      projection_type = "ALL"
    }
  ]
}

# Feature-flags
module "dynamodb_feature_flags" {
  source = "../../modules/dynamodb"

  table_name   = "feature-flags"
  hash_key     = "feature_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "feature_id", type = "S" }
  ]
}

# Pending-changes
module "dynamodb_pending_changes" {
  source = "../../modules/dynamodb"

  table_name   = "pending-changes"
  hash_key     = "change_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "change_id", type = "S" }
  ]
}

# User-flags
module "dynamodb_user_flags" {
  source = "../../modules/dynamodb"

  table_name   = "user-flags"
  hash_key     = "flagId"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "flagId", type = "S" },
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

# email-campaign-stats
module "dynamodb_email_campaign_stats" {
  source = "../../modules/dynamodb"

  table_name   = "email-campaign-stats"
  hash_key     = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "campaign_id", type = "S" }
  ]
}

# email-subscriber-stats
module "dynamodb_email_subscriber_stats" {
  source = "../../modules/dynamodb"

  table_name   = "email-subscriber-stats"
  hash_key     = "subscriber_email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "subscriber_email", type = "S" }
  ]
}

# email_subscribers(underscore variant)
module "dynamodb_email_subscribers_v2" {
  source = "../../modules/dynamodb"

  table_name   = "email_subscribers"
  hash_key     = "email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "email", type = "S" }
  ]
}

# newsletter_anaylytics
module "dynamodb_newsletter_analytics" {
  source = "../../modules/dynamodb"

  table_name   = "newsletter_analytics"
  hash_key     = "tracking_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "tracking_id", type = "S" }
  ]
}

# user-eamil-campaigns
module "dynamodb_user_email_campaigns" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-campaigns"
  hash_key     = "user_id"
  range_key    = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "campaign_id", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    }
  ]
}

# user-email-drip-enrollments
module "dynamodb_user_email_drip_enrollments" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-drip-enrollments"
  hash_key     = "user_id"
  range_key    = "enrollment_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "enrollment_id", type = "S" },
    { name = "status", type = "S" },
    { name = "subscriber_email", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    },
    {
      name            = "email-index"
      hash_key        = "user_id"
      range_key       = "subscriber_email"
      projection_type = "ALL"
    }
  ]
}

# user-email-event
module "dynamodb_user_email_events" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-events"
  hash_key     = "user_id"
  range_key    = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "event_id", type = "S" },
    { name = "campaign_id", type = "S" },
    { name = "subscriber_email", type = "S" },
    { name = "timestamp", type = "N" }
  ]

  global_secondary_indexes = [
    {
      name            = "campaign-index"
      hash_key        = "campaign_id"
      range_key       = "timestamp"
      projection_type = "ALL"
    },
    {
      name            = "email-index"
      hash_key        = "subscriber_email"
      range_key       = "timestamp"
      projection_type = "ALL"
    }
  ]
}

#forum-posts
module "dynamodb_forum_posts" {
  source = "../../modules/dynamodb"

  table_name   = "forum-posts"
  hash_key     = "post_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "post_id", type = "S" },
    { name = "mountain", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "mountain-index"
      hash_key        = "mountain"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}

# Business Directory
module "dynamodb_business_directory" {
  source = "../../modules/dynamodb"

  table_name   = "business-directory"
  hash_key     = "business_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "business_id", type = "S" },
    { name = "category", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "category-index"
      hash_key        = "category"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}

# boycott-tracker
module "dynamodb_boycott_tracker" {
  source = "../../modules/dynamodb"

  table_name     = "boycott-tracker"
  hash_key       = "boycott_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attributes = [
    { name = "boycott_id", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "status"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}

# user-email-subscribers
module "dynamodb_user_email_subscribers" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-subscribers"
  hash_key     = "user_id"
  range_key    = "subscriber_email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "subscriber_email", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    }
  ]
}



# ============================================
# Outputs
# ============================================

output "s3_bucket_name" {
  value = module.s3_videos.bucket_id
  description = "S3 bucket name for video storage"
}

output "s3_bucket_arn" {
  value = module.s3_videos.bucket_arn
  description = "ARN of the S3 bucket for video storage"
}

output "s3_bucket_domain" {
  value = module.s3_videos.bucket_regional_domain_name
  description = "s3 bucket regional domain name"
}

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

output "cloudfront_distribution_id" {
  value       = module.cloudfront_distribution.distribution_id
  description = "CloudFront distribution ID"
}

output "cloudfront_domain_name" {
  value       = module.cloudfront_distribution.distribution_domain_name
  description = "CloudFront distribution domain name"
}

output "website_urls" {
  value = {
    cloudfront = "https://${module.cloudfront_distribution.distribution_domain_name}"
    custom1    = "https://videos.mytestimony.click"
    custom2    = "https://christianconservativestoday.com"
  }
  description = "Website URLs"
}

# ============================================
# SQS
# ============================================

# Video-processing-queue
module "sqs_video_processing" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name             = "video-processing-queue"
  dlq_name               = "video-processing-dlq"
  visibility_timeout     = 900
  message_retention      = 345600
  max_receive_count      = 3
  dlq_message_retention  = 1209600
  dlq_visibility_timeout = 900
}

# thumbnail-generation queu
module "sqs_thumbnail_generation" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name             = "thumbnail-generation-queue"
  dlq_name               = "thumbnail-generation-dlq"
  visibility_timeout     = 300
  message_retention      = 86400
  max_receive_count      = 3
  dlq_message_retention  = 1209600
  dlq_visibility_timeout = 300
}
# sqs_email
module "sqs_email" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name             = "email-queue"
  dlq_name               = "email-dlq"
  visibility_timeout     = 60
  message_retention      = 172800
  max_receive_count      = 5
  dlq_message_retention  = 1209600
  dlq_visibility_timeout = 60
}

# SQS notification queue
module "sqs_email_notification" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "email-notification-queue"
  visibility_timeout = 60
  message_retention  = 345600
  max_receive_count  = 3
}

# Analytics queue
module "sqs_analytics" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name             = "analytics-queue"
  dlq_name               = "analytics-dlq"
  visibility_timeout     = 30
  message_retention      = 86400
  max_receive_count      = 2
  dlq_message_retention  = 1209600
}

# ============================================
# SNS Topics
# ============================================
# platform-critical-alerts
module "sns_platform_critical_alerts" {
  source = "../../modules/sns-topic"

  topic_name      = "platform-critical-alerts"
  email_addresses = ["hawaiianintucson@gmail.com"]

  tags = {
    Environment = "production"
    Purpose     = "Critical platform alerts"
  }
}

# Video download notifications
module "sns_video_download_notifications" {
  source = "../../modules/sns-topic"

  topic_name      = "video-download-notifications"
  email_addresses = ["hawaiianintucson@gmail.com"]

  tags = {
    Environment = "production"
    Purpose     = "Video download completion alerts"
  }
}

# SES Bounces
module "sns_ses_bounces" {
  source = "../../modules/sns-topic"

  topic_name      = "ses-bounces"
  email_addresses = ["hawaiianintucson@gmail.com"]

  tags = {
    Environment = "production"
    Purpose     = "SES bounce notifications"
  }
}

# SES email events
resource "aws_sns_topic" "ses_email_events" {
  name = "ses-email-events"

  tags = {
    Environment = "production"
    Purpose     = "SES event processing"
  }
}

resource "aws_sns_topic_subscription" "ses_email_events_lambda" {
  topic_arn = aws_sns_topic.ses_email_events.arn
  protocol  = "lambda"
  endpoint  = module.lambda_ses_event_processor.function_arn
}


# ============================================
# CloudWatch Dashboard
# ============================================

module "platform_dashboard" {
  source = "../../modules/cloudwatch-dashboard"

  dashboard_name  = "ChristianConservativePlatform-Monitoring"
  region          = "us-east-1"
  account_id      = "371751795928"
  api_gateway_id  = module.unified_api.api_id

  lambda_functions = [
    "admin-api",
    "auth-api",
    "articles-api",
    "news-api",
    "comments-handler",
    "contributors-api",
    "resources-api",
    "video-list-api",
    "video-tag-api",
    "url-analysis-api",
    "paypal-billing-api",
    "video-downloader",
    "thumbnail-generator",
    "s3-thumbnail-trigger",
    "video-download-router",
    "prayer_api",
    "events_api",
    "notifications_api",
    "paypal-ipn-handler"
  ]

  alarm_names = [
    "API-Gateway-5XX-Errors",
    "Lambda-Admin-Errors",
    "Lambda-Articles-Errors",
    "Lambda-Auth-ConcurrentExecutions",
    "Lambda-Auth-Duration",
    "Lambda-Auth-Errors",
    "Lambda-Comments-Errors",
    "Lambda-Contributors-Errors",
    "Lambda-Downloader-Duration",
    "Lambda-Downloader-Errors",
    "Lambda-Downloader-Throttles",
    "Lambda-Events-Errors",
    "Lambda-News-Errors",
    "Lambda-Notifications-Errors",
    "Lambda-PayPal-Duration",
    "Lambda-PayPal-Errors",
    "Lambda-PayPal-Throttles",
    "Lambda-Prayer-Errors",
    "Lambda-Resources-Errors",
    "Lambda-Router-Duration",
    "Lambda-Router-Errors",
    "Lambda-Router-Throttles",
    "Lambda-S3Trigger-Errors",
    "Lambda-Thumbnail-Errors",
    "Lambda-URLAnalysis-Errors",
    "Lambda-VideoList-Errors",
    "Lambda-VideoTag-Errors"
  ]
}

output "dashboard_url" {
  value       = module.platform_dashboard.dashboard_url
  description = "URL to view the CloudWatch dashboard"
}
