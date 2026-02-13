# ============================================
# CloudWatch Log Groups
# ============================================

# High Priority (30 days retention)
module "log_group_router" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/video-download-router"
  retention_days = 30

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "high"
  }
}

module "log_group_downloader" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/video-downloader"
  retention_days = 30

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "high"
  }
}

module "log_group_auth_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/auth-api"
  retention_days = 30

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "high"
  }
}

module "log_group_paypal" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/paypal-billing-api"
  retention_days = 30

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "high"
  }
}

# Medium Priority (14 days retention)
module "log_group_admin_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/admin-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_articles_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/articles-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_news_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/news-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_contributors_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/contributors-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_resources_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/resources-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_video_list_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/video-list-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_video_tag_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/video-tag-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

module "log_group_url_analysis_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/url-analysis-api"
  retention_days = 14

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "medium"
  }
}

# Low Priority (7 days retention)
module "log_group_thumbnail_generator" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/thumbnail-generator"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}

module "log_group_s3_thumbnail_trigger" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/s3-thumbnail-trigger"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}

module "log_group_prayer_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/prayer_api"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}

module "log_group_events_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/events_api"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}

module "log_group_notifications_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/notifications_api"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}

module "log_group_comments_api" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/comments-api"
  retention_days = 7

  tags = {
    Environment  = "production"
    ManagedBy    = "Terraform"
    Project      = "ChristianConservativePlatform"
    CostCenter   = "monitoring"
    Criticality  = "low"
  }
}


# ============================================
# SNS Topic for Alarms
# ============================================

module "sns_critical_alerts" {
  source = "../../modules/sns-topic"

  topic_name = "platform-critical-alerts"
  email_addresses = [
    "hawaiianintucson@gmail.com"  # Replace with your actual email
  ]

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
  }
}

# ============================================================================
# CloudWatch Alarms
# ============================================================================

# API Gateway 5XX Errors
module "alarm_api_gateway_5xx" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "API-Gateway-5XX-Errors"
  alarm_description   = "Alert when API Gateway returns 5XX errors" 
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    ApiName = "unified-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality  = "high"
  }
}

# ============================================================================
# Lambda Error Alarms (18 functions)
# ============================================================================

# Router
module "alarm_router_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Router-Errors"
  alarm_description   = "Alert on router Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-download-router"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Downloader
module "alarm_downloader_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Downloader-Errors"
  alarm_description   = "Alert on downloader Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-downloader"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Auth API
module "alarm_auth_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Auth-Errors"
  alarm_description   = "Alert on auth Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "auth-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# PayPal
module "alarm_paypal_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-PayPal-Errors"
  alarm_description   = "Alert on PayPal Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "paypal-billing-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Admin API
module "alarm_admin_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Admin-Errors"
  alarm_description   = "Alert on admin Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "admin-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Articles API
module "alarm_articles_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Articles-Errors"
  alarm_description   = "Alert on articles Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "articles-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# News API
module "alarm_news_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-News-Errors"
  alarm_description   = "Alert on news Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "news-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Contributors API
module "alarm_contributors_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Contributors-Errors"
  alarm_description   = "Alert on contributors Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "contributors-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Resources API
module "alarm_resources_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Resources-Errors"
  alarm_description   = "Alert on resources Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "resources-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Video List API
module "alarm_video_list_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-VideoList-Errors"
  alarm_description   = "Alert on video list Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-list-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Video Tag API
module "alarm_video_tag_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-VideoTag-Errors"
  alarm_description   = "Alert on video tag Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-tag-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# URL Analysis API
module "alarm_url_analysis_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-URLAnalysis-Errors"
  alarm_description   = "Alert on URL analysis Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "url-analysis-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "medium"
  }
}

# Thumbnail Generator
module "alarm_thumbnail_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Thumbnail-Errors"
  alarm_description   = "Alert on thumbnail Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "thumbnail-generator"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# S3 Thumbnail Trigger
module "alarm_s3_trigger_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-S3Trigger-Errors"
  alarm_description   = "Alert on S3 trigger Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "s3-thumbnail-trigger"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# Prayer API
module "alarm_prayer_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Prayer-Errors"
  alarm_description   = "Alert on prayer Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "prayer_api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# Events API
module "alarm_events_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Events-Errors"
  alarm_description   = "Alert on events Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "events_api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# Notifications API
module "alarm_notifications_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Notifications-Errors"
  alarm_description   = "Alert on notifications Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "notifications_api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# Comments API
module "alarm_comments_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Comments-Errors"
  alarm_description   = "Alert on comments Lambda errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "comments-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "low"
  }
}

# ============================================================================
# Critical Lambda Function Alarms (Duration, Throttles, Concurrent Executions)
# ============================================================================

# Router - Duration
module "alarm_router_duration" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Router-Duration"
  alarm_description   = "Alert when router duration exceeds 80% of timeout"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 12000
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-download-router"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Router - Throttles
module "alarm_router_throttles" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Router-Throttles"
  alarm_description   = "Alert on router throttling"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-download-router"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Downloader - Duration
module "alarm_downloader_duration" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Downloader-Duration"
  alarm_description   = "Alert when downloader duration exceeds 80% of timeout"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 720000
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-downloader"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Downloader - Throttles
module "alarm_downloader_throttles" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Downloader-Throttles"
  alarm_description   = "Alert on downloader throttling"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "video-downloader"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Auth - Duration
module "alarm_auth_duration" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Auth-Duration"
  alarm_description   = "Alert when auth duration exceeds 80% of timeout"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 24000
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "auth-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# Auth - Concurrent Executions
module "alarm_auth_concurrent" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-Auth-ConcurrentExecutions"
  alarm_description   = "Alert on high concurrent executions for auth"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ConcurrentExecutions"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Maximum"
  threshold           = 50
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "auth-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# PayPal - Duration
module "alarm_paypal_duration" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-PayPal-Duration"
  alarm_description   = "Alert when PayPal duration exceeds 80% of timeout"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 24000
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "paypal-billing-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}

# PayPal - Throttles
module "alarm_paypal_throttles" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-PayPal-Throttles"
  alarm_description   = "Alert on PayPal throttling"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  alarm_actions = [module.sns_critical_alerts.topic_arn]

  dimensions = {
    FunctionName = "paypal-billing-api"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "ChristianConservativePlatform"
    CostCenter  = "monitoring"
    Criticality = "high"
  }
}
