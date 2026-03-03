# Construct alarm ARNs from names
locals {
  alarm_arns = [
    for name in var.alarm_names :
    "arn:aws:cloudwatch:${var.region}:${var.account_id}:alarm:${name}"
  ]
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = var.dashboard_name

  dashboard_body = jsonencode({
    widgets = [
      # Alarm Status Widget
      {
        type = "alarm"
        properties = {
          title  = "🚨 Alarm Status (${length(var.alarm_names)} Alarms)"
          alarms = local.alarm_arns
        }
        x      = 0
        y      = 0
        width  = 24
        height = 6
      },
      
      # API Gateway Metrics
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApiGateway", "Count"],
            ["AWS/ApiGateway", "4XXError"],
            ["AWS/ApiGateway", "5XXError"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "📊 API Gateway Metrics"
          period  = 300
        }
        x      = 0
        y      = 6
        width  = 12
        height = 6
      },
      
      # Lambda Errors
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Errors", {"stat":"Sum"}]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "⚠️ Lambda Errors (All Functions)"
          period  = 300
        }
        x      = 12
        y      = 6
        width  = 12
        height = 6
      },
      
      # Lambda Duration
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", {"stat":"Average"}]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "⏱️ Lambda Duration (Average)"
          period  = 300
        }
        x      = 0
        y      = 12
        width  = 12
        height = 6
      },
      
      # Lambda Invocations
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", {"stat":"Sum"}]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "🔄 Total Lambda Invocations"
          period  = 300
        }
        x      = 12
        y      = 12
        width  = 12
        height = 6
      },
      
      # Lambda Throttles
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Throttles", {"stat":"Sum"}]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "🚫 Lambda Throttles"
          period  = 300
        }
        x      = 0
        y      = 18
        width  = 12
        height = 6
      },
      
      # Lambda Concurrent Executions
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "ConcurrentExecutions", {"stat":"Maximum"}]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.region
          title   = "🔀 Lambda Concurrent Executions"
          period  = 300
        }
        x      = 12
        y      = 18
        width  = 12
        height = 6
      }
    ]
  })
}
