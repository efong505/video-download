locals {
  alarm_arns = [
    for name in var.alarm_names :
    "arn:aws:cloudwatch:${var.region}:${var.account_id}:alarm:${name}"
  ]

  lambda_error_metrics = [
    for fn in var.lambda_functions :
    ["AWS/Lambda", "Errors", "FunctionName", fn]
  ]

  lambda_duration_metrics = [
    for fn in var.lambda_functions :
    ["AWS/Lambda", "Duration", "FunctionName", fn]
  ]

  lambda_invocation_metrics = [
    for fn in var.lambda_functions :
    ["AWS/Lambda", "Invocations", "FunctionName", fn]
  ]

  sqs_depth_metrics = [
    for q in var.sqs_queue_names :
    ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", q]
  ]

  sqs_dlq_metrics = [
    for q in var.sqs_queue_names :
    ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "${q}-dlq"]
  ]

  dynamo_read_metrics = [
    for t in var.dynamodb_table_names :
    ["AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", t]
  ]

  dynamo_write_metrics = [
    for t in var.dynamodb_table_names :
    ["AWS/DynamoDB", "ConsumedWriteCapacityUnits", "TableName", t]
  ]

  dynamo_read_throttle_metrics = [
    for t in var.dynamodb_table_names :
    ["AWS/DynamoDB", "ReadThrottleEvents", "TableName", t]
  ]

  dynamo_write_throttle_metrics = [
    for t in var.dynamodb_table_names :
    ["AWS/DynamoDB", "WriteThrottleEvents", "TableName", t]
  ]
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = var.dashboard_name

  dashboard_body = jsonencode({
    widgets = [
      # Row 1: Alarm Status
      {
        type = "alarm"
        properties = {
          title  = "Alarm Status (${length(var.alarm_names)} Alarms)"
          alarms = local.alarm_arns
        }
        x      = 0
        y      = 0
        width  = 24
        height = 4
      },

      # Row 2: API Gateway
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApiGateway", "Count", "ApiName", "unified-api"],
            ["AWS/ApiGateway", "4XXError", "ApiName", "unified-api"],
            ["AWS/ApiGateway", "5XXError", "ApiName", "unified-api"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Sum"
          title   = "API Gateway - Requests & Errors"
          period  = 300
        }
        x      = 0
        y      = 4
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApiGateway", "Latency", "ApiName", "unified-api"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Average"
          title   = "API Gateway - Latency (avg)"
          period  = 300
        }
        x      = 12
        y      = 4
        width  = 12
        height = 6
      },

      # Row 3: Lambda Per-Function Errors & Duration
      {
        type = "metric"
        properties = {
          metrics = local.lambda_error_metrics
          view    = "timeSeries"
          stacked = true
          region  = var.region
          stat    = "Sum"
          title   = "Lambda Errors - Per Function"
          period  = 300
        }
        x      = 0
        y      = 10
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = local.lambda_duration_metrics
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Average"
          title   = "Lambda Duration - Per Function (avg)"
          period  = 300
        }
        x      = 12
        y      = 10
        width  = 12
        height = 6
      },

      # Row 4: Lambda Invocations & Concurrency
      {
        type = "metric"
        properties = {
          metrics = local.lambda_invocation_metrics
          view    = "timeSeries"
          stacked = true
          region  = var.region
          stat    = "Sum"
          title   = "Lambda Invocations - Per Function"
          period  = 300
        }
        x      = 0
        y      = 16
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "ConcurrentExecutions"],
            ["AWS/Lambda", "Throttles"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Maximum"
          title   = "Concurrency & Throttles"
          period  = 300
        }
        x      = 12
        y      = 16
        width  = 12
        height = 6
      },

      # Row 5: DynamoDB
      {
        type = "metric"
        properties = {
          metrics = local.dynamo_read_metrics
          view    = "timeSeries"
          stacked = true
          region  = var.region
          stat    = "Sum"
          title   = "DynamoDB - Read Capacity Consumed"
          period  = 300
        }
        x      = 0
        y      = 22
        width  = 8
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = local.dynamo_write_metrics
          view    = "timeSeries"
          stacked = true
          region  = var.region
          stat    = "Sum"
          title   = "DynamoDB - Write Capacity Consumed"
          period  = 300
        }
        x      = 8
        y      = 22
        width  = 8
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = concat(local.dynamo_read_throttle_metrics, local.dynamo_write_throttle_metrics)
          view    = "timeSeries"
          stacked = true
          region  = var.region
          stat    = "Sum"
          title   = "DynamoDB - Throttle Events"
          period  = 300
        }
        x      = 16
        y      = 22
        width  = 8
        height = 6
      },

      # Row 6: SQS Queues
      {
        type = "metric"
        properties = {
          metrics = local.sqs_depth_metrics
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Maximum"
          title   = "SQS - Queue Depth"
          period  = 60
        }
        x      = 0
        y      = 28
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = local.sqs_dlq_metrics
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Maximum"
          title   = "SQS - Dead Letter Queue Depth"
          period  = 60
        }
        x      = 12
        y      = 28
        width  = 12
        height = 6
      },

      # Row 7: SES Email
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/SES", "Send"],
            ["AWS/SES", "Delivery"],
            ["AWS/SES", "Bounce"],
            ["AWS/SES", "Complaint"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Sum"
          title   = "SES - Email Delivery"
          period  = 300
        }
        x      = 0
        y      = 34
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/SES", "Reputation.BounceRate"],
            ["AWS/SES", "Reputation.ComplaintRate"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          stat    = "Average"
          title   = "SES - Reputation (bounce < 5%, complaint < 0.1%)"
          period  = 300
          yAxis = {
            left = { min = 0, max = 10 }
          }
        }
        x      = 12
        y      = 34
        width  = 12
        height = 6
      },

      # Row 8: CloudFront
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/CloudFront", "Requests", "DistributionId", var.cloudfront_distribution_id, "Region", "Global"],
            ["AWS/CloudFront", "BytesDownloaded", "DistributionId", var.cloudfront_distribution_id, "Region", "Global"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "us-east-1"
          stat    = "Sum"
          title   = "CloudFront - Requests & Bytes"
          period  = 300
        }
        x      = 0
        y      = 40
        width  = 12
        height = 6
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/CloudFront", "4xxErrorRate", "DistributionId", var.cloudfront_distribution_id, "Region", "Global"],
            ["AWS/CloudFront", "5xxErrorRate", "DistributionId", var.cloudfront_distribution_id, "Region", "Global"],
            ["AWS/CloudFront", "CacheHitRate", "DistributionId", var.cloudfront_distribution_id, "Region", "Global"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "us-east-1"
          stat    = "Average"
          title   = "CloudFront - Cache Hit & Error Rates"
          period  = 300
        }
        x      = 12
        y      = 40
        width  = 12
        height = 6
      }
    ]
  })
}
