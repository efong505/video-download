# CloudWatch Monitoring - Implementation Guide (Week 9-10)

## Status: 🔜 NOT YET IMPLEMENTED

This guide outlines the planned implementation for Week 9-10.

---

## Overview
Add comprehensive monitoring and alerting for Lambda functions, API Gateway, and DynamoDB using CloudWatch.

---

## Goals

### Week 9: CloudWatch Log Groups & Metrics
- Create Log Groups for all 18 Lambda functions
- Set log retention policies (30 days)
- Create custom metrics for business logic
- Set up CloudWatch Dashboards

### Week 10: Alarms & Notifications
- Create CloudWatch Alarms for errors, throttles, duration
- Set up SNS topics for alert notifications
- Configure email/SMS notifications
- Implement alarm actions (auto-scaling, Lambda triggers)

---

## Step 1: Gather Current Monitoring State

### Commands to Inspect Existing Resources

```bash
# List all CloudWatch Log Groups
aws logs describe-log-groups --query 'logGroups[*].[logGroupName,retentionInDays]' --output table

# List CloudWatch Alarms
aws cloudwatch describe-alarms --query 'MetricAlarms[*].[AlarmName,StateValue,MetricName]' --output table

# List SNS Topics
aws sns list-topics

# Get Lambda function metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=router \
  --start-time 2026-02-01T00:00:00Z \
  --end-time 2026-02-10T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

### Expected Current State

**Log Groups**: Automatically created by Lambda (no retention policy)
```
/aws/lambda/router
/aws/lambda/admin_api
/aws/lambda/articles_api
... (18 total)
```

**Alarms**: None (manual monitoring only)

**SNS Topics**: 1 existing
```
arn:aws:sns:us-east-1:371751795928:video-download-notifications
```

---

## Step 2: Design Monitoring Strategy

### Metrics to Monitor

**Lambda Functions**:
- Errors (count)
- Duration (milliseconds)
- Throttles (count)
- Concurrent Executions (count)
- Invocations (count)

**API Gateway**:
- 4XXError (count)
- 5XXError (count)
- Latency (milliseconds)
- Count (requests)

**DynamoDB**:
- ConsumedReadCapacityUnits
- ConsumedWriteCapacityUnits
- UserErrors (count)
- SystemErrors (count)

### Alarm Thresholds

**Critical (Page immediately)**:
- Lambda error rate > 5%
- API Gateway 5XX error rate > 1%
- Lambda duration > 80% of timeout

**Warning (Email notification)**:
- Lambda error rate > 1%
- API Gateway 4XX error rate > 10%
- Lambda throttles > 0

**Info (Dashboard only)**:
- Lambda invocations
- API Gateway request count
- DynamoDB capacity usage

---

## Step 3: Create CloudWatch Log Group Module

### Module Structure

**File**: `terraform/modules/cloudwatch-log-group/main.tf`

```hcl
resource "aws_cloudwatch_log_group" "this" {
  name              = var.log_group_name
  retention_in_days = var.retention_days

  tags = var.tags
}
```

**File**: `terraform/modules/cloudwatch-log-group/variables.tf`

```hcl
variable "log_group_name" {
  description = "Name of the CloudWatch Log Group"
  type        = string
}

variable "retention_days" {
  description = "Log retention in days"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to the log group"
  type        = map(string)
  default     = {}
}
```

**File**: `terraform/modules/cloudwatch-log-group/outputs.tf`

```hcl
output "log_group_name" {
  description = "Name of the CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.this.name
}

output "log_group_arn" {
  description = "ARN of the CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.this.arn
}
```

---

## Step 4: Create CloudWatch Alarm Module

### Module Structure

**File**: `terraform/modules/cloudwatch-alarm/main.tf`

```hcl
resource "aws_cloudwatch_metric_alarm" "this" {
  alarm_name          = var.alarm_name
  comparison_operator = var.comparison_operator
  evaluation_periods  = var.evaluation_periods
  metric_name         = var.metric_name
  namespace           = var.namespace
  period              = var.period
  statistic           = var.statistic
  threshold           = var.threshold
  alarm_description   = var.alarm_description
  alarm_actions       = var.alarm_actions

  dimensions = var.dimensions

  tags = var.tags
}
```

**File**: `terraform/modules/cloudwatch-alarm/variables.tf`

```hcl
variable "alarm_name" {
  description = "Name of the alarm"
  type        = string
}

variable "comparison_operator" {
  description = "Comparison operator (GreaterThanThreshold, LessThanThreshold, etc.)"
  type        = string
}

variable "evaluation_periods" {
  description = "Number of periods to evaluate"
  type        = number
  default     = 2
}

variable "metric_name" {
  description = "Name of the metric"
  type        = string
}

variable "namespace" {
  description = "Namespace of the metric"
  type        = string
}

variable "period" {
  description = "Period in seconds"
  type        = number
  default     = 300
}

variable "statistic" {
  description = "Statistic to apply (Average, Sum, Maximum, etc.)"
  type        = string
  default     = "Average"
}

variable "threshold" {
  description = "Threshold value"
  type        = number
}

variable "alarm_description" {
  description = "Description of the alarm"
  type        = string
  default     = ""
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm triggers"
  type        = list(string)
  default     = []
}

variable "dimensions" {
  description = "Dimensions for the metric"
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags to apply to the alarm"
  type        = map(string)
  default     = {}
}
```

---

## Step 5: Create SNS Topic Module

### Module Structure

**File**: `terraform/modules/sns-topic/main.tf`

```hcl
resource "aws_sns_topic" "this" {
  name = var.topic_name

  tags = var.tags
}

resource "aws_sns_topic_subscription" "email" {
  for_each = toset(var.email_addresses)

  topic_arn = aws_sns_topic.this.arn
  protocol  = "email"
  endpoint  = each.value
}
```

**File**: `terraform/modules/sns-topic/variables.tf`

```hcl
variable "topic_name" {
  description = "Name of the SNS topic"
  type        = string
}

variable "email_addresses" {
  description = "List of email addresses to subscribe"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to the topic"
  type        = map(string)
  default     = {}
}
```

---

## Step 6: Use Modules in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# SNS Topic for Alarms
module "sns_alarms" {
  source = "../../modules/sns-topic"

  topic_name = "lambda-alarms"
  email_addresses = [
    "admin@example.com"
  ]

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Log Group for Router Lambda
module "log_group_router" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name  = "/aws/lambda/router"
  retention_days  = 30

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Alarm for Router Errors
module "alarm_router_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "router-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "Router Lambda error count exceeded 10 in 5 minutes"
  alarm_actions       = [module.sns_alarms.topic_arn]

  dimensions = {
    FunctionName = "router"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Repeat for all 18 Lambda functions...
```

---

## Step 7: Import Existing Resources

### Import Log Groups

```bash
# Import existing log groups (created automatically by Lambda)
terraform import module.log_group_router.aws_cloudwatch_log_group.this /aws/lambda/router
terraform import module.log_group_admin_api.aws_cloudwatch_log_group.this /aws/lambda/admin_api
# ... repeat for all 18 functions
```

### Create New Resources

```bash
# SNS topics and alarms don't exist yet, so just apply
terraform apply
```

---

## Step 8: Create CloudWatch Dashboard

### Dashboard Configuration

**File**: `terraform/environments/prod/cloudwatch-dashboard.tf`

```hcl
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "ministry-platform-overview"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", { stat = "Sum", label = "Total Invocations" }],
            [".", "Errors", { stat = "Sum", label = "Total Errors" }],
            [".", "Throttles", { stat = "Sum", label = "Total Throttles" }]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-1"
          title  = "Lambda Overview"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApiGateway", "Count", { stat = "Sum", label = "API Requests" }],
            [".", "4XXError", { stat = "Sum", label = "4XX Errors" }],
            [".", "5XXError", { stat = "Sum", label = "5XX Errors" }]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-1"
          title  = "API Gateway Overview"
        }
      }
    ]
  })
}
```

---

## Expected Benefits

### Operational Visibility
- **Before**: Manual log checking, no alerts
- **After**: Automated alerts, centralized dashboard

### Faster Incident Response
- **Before**: Discover issues when users report them
- **After**: Alerted immediately when errors occur

### Cost Optimization
- **Before**: No visibility into unused resources
- **After**: Identify low-usage functions for optimization

### Compliance
- **Before**: No log retention policy
- **After**: 30-day retention for audit trail

---

## Estimated Costs

### CloudWatch Logs
- **Ingestion**: $0.50 per GB
- **Storage**: $0.03 per GB/month
- **Estimated**: $5-10/month for 18 Lambda functions

### CloudWatch Alarms
- **Standard Metrics**: $0.10 per alarm/month
- **18 functions × 3 alarms**: $5.40/month

### SNS
- **Email notifications**: Free (first 1,000)
- **Estimated**: $0/month

**Total Estimated Cost**: $10-15/month

---

## Implementation Timeline

### Week 9 (Days 1-3)
- Create CloudWatch Log Group module
- Import existing log groups
- Set retention policies
- Create CloudWatch Dashboard

### Week 9 (Days 4-5)
- Create CloudWatch Alarm module
- Create SNS Topic module
- Test alarm notifications

### Week 10 (Days 1-3)
- Create alarms for all Lambda functions
- Create alarms for API Gateway
- Create alarms for DynamoDB

### Week 10 (Days 4-5)
- Test all alarms
- Document alarm response procedures
- Create runbooks for common issues

---

## Success Criteria

✅ All 18 Lambda functions have log groups with 30-day retention  
✅ Critical alarms configured for errors and throttles  
✅ SNS topic configured with email notifications  
✅ CloudWatch Dashboard shows key metrics  
✅ Test alarm triggers successfully  
✅ Documentation complete for alarm response  

---

## Related Files
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)
- [CI/CD Documentation](../../.github/CI_CD_DOCUMENTATION.md)

---

**Status**: Planning Phase  
**Planned Start**: Week 9  
**Estimated Duration**: 2 weeks  
**Created**: February 10, 2026
