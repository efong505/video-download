# Week 9: Create CloudWatch Dashboard + Alarms for Shopping System

$profile = "ekewaka"
$region = "us-east-1"
$accountId = "371751795928"

Write-Host "`n=== Week 9: Creating Monitoring ===" -ForegroundColor Cyan

# --- Step 1: CloudWatch Dashboard ---
Write-Host "`n[1/2] Creating CloudWatch Dashboard..." -ForegroundColor Yellow

$dashboard = @{
    widgets = @(
        @{
            type = "text"
            x = 0; y = 0; width = 24; height = 1
            properties = @{ markdown = "# Shopping System Dashboard" }
        },
        @{
            type = "metric"
            x = 0; y = 1; width = 12; height = 6
            properties = @{
                title = "Lambda Invocations"
                metrics = @(
                    @("AWS/Lambda", "Invocations", "FunctionName", "products-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Invocations", "FunctionName", "orders-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Invocations", "FunctionName", "reviews-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Invocations", "FunctionName", "tracking-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Invocations", "FunctionName", "marketing-api", @{stat="Sum"; period=300})
                )
                region = $region
                period = 300
                view = "timeSeries"
            }
        },
        @{
            type = "metric"
            x = 12; y = 1; width = 12; height = 6
            properties = @{
                title = "Lambda Errors"
                metrics = @(
                    @("AWS/Lambda", "Errors", "FunctionName", "products-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Errors", "FunctionName", "orders-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Errors", "FunctionName", "reviews-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Errors", "FunctionName", "tracking-api", @{stat="Sum"; period=300}),
                    @("AWS/Lambda", "Errors", "FunctionName", "marketing-api", @{stat="Sum"; period=300})
                )
                region = $region
                period = 300
                view = "timeSeries"
            }
        },
        @{
            type = "metric"
            x = 0; y = 7; width = 12; height = 6
            properties = @{
                title = "Lambda Duration (avg ms)"
                metrics = @(
                    @("AWS/Lambda", "Duration", "FunctionName", "products-api", @{stat="Average"; period=300}),
                    @("AWS/Lambda", "Duration", "FunctionName", "orders-api", @{stat="Average"; period=300}),
                    @("AWS/Lambda", "Duration", "FunctionName", "tracking-api", @{stat="Average"; period=300}),
                    @("AWS/Lambda", "Duration", "FunctionName", "marketing-api", @{stat="Average"; period=300})
                )
                region = $region
                period = 300
                view = "timeSeries"
            }
        },
        @{
            type = "metric"
            x = 12; y = 7; width = 12; height = 6
            properties = @{
                title = "DLQ Messages (should be 0)"
                metrics = @(
                    @("AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "order-processing-queue-dlq", @{stat="Maximum"; period=300}),
                    @("AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "payment-processing-queue-dlq", @{stat="Maximum"; period=300}),
                    @("AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "email-notification-queue-dlq", @{stat="Maximum"; period=300}),
                    @("AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", "inventory-update-queue-dlq", @{stat="Maximum"; period=300})
                )
                region = $region
                period = 300
                view = "singleValue"
            }
        },
        @{
            type = "metric"
            x = 0; y = 13; width = 24; height = 6
            properties = @{
                title = "API Gateway (5xx Errors)"
                metrics = @(
                    @("AWS/ApiGateway", "5XXError", "ApiName", "shopping-api", @{stat="Sum"; period=300})
                )
                region = $region
                period = 300
                view = "timeSeries"
            }
        }
    )
} | ConvertTo-Json -Depth 10 -Compress

$dashFile = "$env:TEMP\shopping-dashboard.json"
$dashboard | Out-File -FilePath $dashFile -Encoding utf8

aws cloudwatch put-dashboard `
    --dashboard-name "Shopping-System" `
    --dashboard-body "file://$dashFile" `
    --region $region --profile $profile --no-cli-pager | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Dashboard created: Shopping-System" -ForegroundColor Green
    Write-Host "  View: https://console.aws.amazon.com/cloudwatch/home?region=$region#dashboards:name=Shopping-System" -ForegroundColor Gray
} else {
    Write-Host "  Dashboard creation failed" -ForegroundColor Red
}

# --- Step 2: CloudWatch Alarms ---
Write-Host "`n[2/2] Creating CloudWatch Alarms..." -ForegroundColor Yellow

# Alarm: DLQ has messages (Critical)
$dlqs = @("order-processing-queue-dlq", "payment-processing-queue-dlq", "email-notification-queue-dlq", "inventory-update-queue-dlq")
foreach ($dlq in $dlqs) {
    aws cloudwatch put-metric-alarm `
        --alarm-name "Shopping-DLQ-$dlq" `
        --alarm-description "CRITICAL: Messages in $dlq - failed processing" `
        --namespace "AWS/SQS" `
        --metric-name "ApproximateNumberOfMessagesVisible" `
        --dimensions "Name=QueueName,Value=$dlq" `
        --statistic Maximum `
        --period 300 `
        --threshold 1 `
        --comparison-operator GreaterThanOrEqualToThreshold `
        --evaluation-periods 1 `
        --treat-missing-data notBreaching `
        --region $region --profile $profile --no-cli-pager 2>$null
    Write-Host "  Alarm: Shopping-DLQ-$dlq" -ForegroundColor Green
}

# Alarm: Lambda errors > 5 in 5 minutes
$lambdas = @("products-api", "orders-api", "reviews-api", "tracking-api", "marketing-api")
foreach ($fn in $lambdas) {
    aws cloudwatch put-metric-alarm `
        --alarm-name "Shopping-Errors-$fn" `
        --alarm-description "WARNING: $fn has >5 errors in 5 minutes" `
        --namespace "AWS/Lambda" `
        --metric-name "Errors" `
        --dimensions "Name=FunctionName,Value=$fn" `
        --statistic Sum `
        --period 300 `
        --threshold 5 `
        --comparison-operator GreaterThanThreshold `
        --evaluation-periods 1 `
        --treat-missing-data notBreaching `
        --region $region --profile $profile --no-cli-pager 2>$null
    Write-Host "  Alarm: Shopping-Errors-$fn" -ForegroundColor Green
}

# Alarm: Lambda duration > 10s (warning)
foreach ($fn in $lambdas) {
    aws cloudwatch put-metric-alarm `
        --alarm-name "Shopping-Latency-$fn" `
        --alarm-description "WARNING: $fn avg duration >10s" `
        --namespace "AWS/Lambda" `
        --metric-name "Duration" `
        --dimensions "Name=FunctionName,Value=$fn" `
        --statistic Average `
        --period 300 `
        --threshold 10000 `
        --comparison-operator GreaterThanThreshold `
        --evaluation-periods 2 `
        --treat-missing-data notBreaching `
        --region $region --profile $profile --no-cli-pager 2>$null
    Write-Host "  Alarm: Shopping-Latency-$fn" -ForegroundColor Green
}

Write-Host "`n=== Monitoring Setup Complete ===" -ForegroundColor Green
$totalAlarms = $dlqs.Count + ($lambdas.Count * 2)
Write-Host "  Dashboard: Shopping-System"
Write-Host "  Alarms: $totalAlarms total (4 DLQ + 5 error + 5 latency)"
Write-Host "  View alarms: https://console.aws.amazon.com/cloudwatch/home?region=$region#alarmsV2:"
