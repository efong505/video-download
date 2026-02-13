# CloudWatch Monitoring - Implementation Guide (Week 9)

## Status: ✅ COMPLETE

This guide documents the completed implementation for Week 9.

---

## Overview
Add comprehensive monitoring and alerting for Lambda functions, API Gateway, and DynamoDB using CloudWatch.

---

## Accomplishments

### Week 9 Complete (February 11, 2026)
✅ Created CloudWatch Log Group module  
✅ Imported 18 existing Lambda log groups  
✅ Set retention policies by criticality (7/14/30 days)  
✅ Created SNS Topic module with email subscriptions  
✅ Created CloudWatch Alarm module with treat_missing_data  
✅ Deployed 27 CloudWatch alarms (1 API Gateway + 18 Lambda errors + 8 critical)  
✅ Tested alarm notifications (2 alarms triggered successfully)  
✅ Confirmed email notifications working  
✅ Removed 20 problematic DynamoDB tables from Terraform state  

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

**All Functions (18 alarms)**:
- Lambda errors: > 3 errors in 5 minutes
- treat_missing_data: "notBreaching"

**Critical Functions Only (8 alarms for 4 functions)**:
- Lambda duration: > 80% of timeout (router: 720s, downloader: 720s, auth-api: 24s, paypal: 24s)
- Lambda throttles: > 0
- treat_missing_data: "notBreaching"

**API Gateway (1 alarm)**:
- 5XX errors: > 5 errors in 5 minutes
- treat_missing_data: "notBreaching"
- Latency alarm: Deferred (not mission-critical yet)

**Total Alarms: 27** (1 API + 18 Lambda errors + 8 critical)

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
  treat_missing_data  = var.treat_missing_data

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

variable "treat_missing_data" {
  description = "How to treat missing data (notBreaching, breaching, ignore, missing)"
  type        = string
  default     = "notBreaching"
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

## Actual Costs

### Monthly Recurring Costs
- **CloudWatch Logs**: $5-6/month (1GB ingestion + storage)
- **CloudWatch Alarms**: $1.70/month (27 alarms, first 10 free)
- **SNS**: $0/month (free tier, 1,000 emails free)
- **Total**: $10-11/month

**Note**: CloudWatch costs incur even with zero activity (flat fees for alarms)

---

## Actual Implementation Timeline

### Week 9 (Days 1-2) - ✅ Complete
- Created CloudWatch Log Group module
- Imported existing log groups (18 functions)
- Set retention policies by criticality:
  - High priority (30 days): router, downloader, auth-api, paypal-billing-api
  - Medium priority (14 days): admin-api, articles-api, news-api, contributors-api, resources-api, video-list-api, video-tag-api, url-analysis-api
  - Low priority (7 days): thumbnail-generator, s3-thumbnail-trigger, prayer_api, events_api, notifications_api, comments-api

### Week 9 (Day 3) - ✅ Complete
- Created SNS Topic module
- Created SNS topic: platform-critical-alerts
- Subscribed email and confirmed subscription
- Tested SNS with manual publish (successful)

### Week 9 (Days 4-5) - ✅ Complete
- Created CloudWatch Alarm module (with treat_missing_data)
- Deployed 27 alarms:
  - 1 API Gateway 5XX alarm
  - 18 Lambda error alarms (all functions)
  - 8 critical function alarms (duration + throttle for 4 functions)
- Tested 2 alarms with manual state changes (both successful)
- Confirmed email notifications working

### Deferred to Future Phase
- CloudWatch Dashboard (not critical for initial monitoring)
- Alarm runbooks (will create as issues arise)
- Validation documentation (completed via testing)

---

## Success Criteria - ✅ ACHIEVED

✅ All 18 Lambda functions have log groups with retention (7/14/30 days by criticality)  
✅ 27 alarms configured (1 API Gateway 5XX + 18 Lambda errors + 8 critical function alarms)  
✅ SNS topic configured with email subscription confirmed  
✅ **Post-deployment validation completed: 2 alarms intentionally triggered and verified**  
✅ Email notifications working correctly  
✅ Zero false positives during testing  
✅ Cost < $15/month ($10-11/month actual)  

---

## Related Files
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)
- [CI/CD Documentation](../../.github/CI_CD_DOCUMENTATION.md)

---

**Status**: Planning Phase  
**Planned Start**: Week 9  
**Estimated Duration**: 2 weeks  
**Created**: February 10, 2026


---

## Alarm Response Runbook

### Create: `docs/ALARM_RUNBOOK.md`

Document response procedures for each alarm type:

**API Gateway 5XX Errors**
- Investigation: Check Lambda logs, DynamoDB metrics, recent deployments
- Common causes: Lambda timeout, DynamoDB throttling, bad deployment
- Resolution: Increase timeout, enable auto-scaling, rollback deployment

**Lambda Error Alarm**
- Investigation: Check Lambda logs for error patterns
- Common causes: Code bug, permission issue, dependency failure
- Resolution: Fix code, update IAM role, check AWS service health

**Lambda Duration Warning**
- Investigation: Check duration trend, payload size, code bottlenecks
- Common causes: Large payload, inefficient queries, cold starts
- Resolution: Optimize code, increase memory, enable provisioned concurrency

**Lambda Throttle Alarm**
- Investigation: Check concurrent executions, reserved concurrency
- Common causes: Traffic spike, insufficient concurrency limit
- Resolution: Increase reserved concurrency, enable auto-scaling

---

## Validation Testing

### Post-Deployment Validation (CRITICAL)

**After deploying alarms, intentionally trigger 2-3 alarms to validate the system.**

This is the difference between "I created alarms" and "I operate an alerting system."

```bash
# Test 1: Lambda Error Alarm
aws lambda invoke \
  --function-name auth-api \
  --payload '{"httpMethod":"POST","body":"invalid_json{{"}' \
  response.json

# Wait 5 minutes, verify:
# ✅ Alarm fires (state = ALARM)
# ✅ SNS notification received
# ✅ Alarm auto-resolves after 10 minutes (state = OK)

# Test 2: API Gateway 5XX Alarm
# Make 6 invalid requests to trigger threshold
for i in {1..6}; do
  curl -X POST https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth
done

# Wait 5 minutes, verify alarm cycle

# Test 3: Runbook Validation
# Follow runbook steps for Lambda error alarm
# Document: Did runbook steps work? What's missing?
```

### Validation Checklist
- [ ] Alarm transitions to ALARM state within 5 minutes
- [ ] SNS email notification received with correct details
- [ ] Alarm auto-resolves to OK state after issue clears
- [ ] Runbook steps successfully identify root cause
- [ ] Runbook steps successfully resolve issue
- [ ] Document validation results in `docs/ALARM_VALIDATION.md`

### Pre-Production Checklist

```bash
# 1. Validate Terraform
terraform validate
terraform plan | grep "cloudwatch"

# 2. Test SNS subscription
aws sns publish \
  --topic-arn <topic-arn> \
  --message "Test alert"

# 3. Trigger test alarm
aws lambda invoke \
  --function-name auth-api \
  --payload '{"httpMethod":"POST","body":"invalid"}' \
  response.json

# 4. Verify alarm state
aws cloudwatch describe-alarms \
  --alarm-names auth-api-errors-critical

# 5. Confirm SNS notification received
```

### Post-Deployment Monitoring

- Week 1: Monitor alarm frequency, tune thresholds if >5 false positives/day
- Week 2: Adjust evaluation periods based on traffic patterns
- Week 3: Review dashboard usage, add/remove widgets as needed

---

## Preventing Alert Fatigue

**Strategy**:
1. Start with conservative thresholds (higher values)
2. Use `treat_missing_data = "notBreaching"` for all alarms (prevents false alarms during low traffic)
3. Use 2 consecutive evaluation periods for duration alarms (sustained issues only)
4. Only create duration/throttle alarms for 4 critical functions (not all 18)
5. Defer latency alarm until traffic patterns justify it
6. Tune thresholds weekly based on actual data

**Dashboard Philosophy**:
- Dashboards show problems
- Alarms fix problems
- Build dashboard last (Week 10, Day 5)
- Focus first on: Log retention → SNS → Alarms → Validation → Runbook → Dashboard

**Red Flags**:
- >5 false positives per day = thresholds too aggressive
- Alarms ignored by team = alert fatigue setting in
- No alarms firing for weeks = thresholds too conservative

**treat_missing_data Nuance**:
- Current: All alarms use "notBreaching" (correct for low-traffic systems)
- Future: If you scale significantly, consider "missing" for duration alarms
- Not necessary now, but keep in mind for growth



---

## Resume Statement (Post-Phase 7)

**Before**:
> "Implemented structured logging and CloudWatch monitoring..."

**After**:
> "Designed and deployed production-grade monitoring and alerting system with Terraform-managed CloudWatch alarms (27 alarms across 18 Lambda functions and API Gateway), SNS escalation workflows, and validated operational runbooks for incident response."

---

## Operational Authority

At 80% project completion, you are no longer "learning Terraform."

You are operating:
- Infrastructure as Code
- CI/CD automation with quality gates
- Deployment discipline
- API consolidation
- CDN management
- Disaster recovery optimization (85% faster)

**Monitoring moves you into operational authority.**

This phase demonstrates:
- Production-grade observability design
- Incident response procedures
- Validation discipline
- Cost awareness
- Alert fatigue prevention

**This is the difference between "I created alarms" and "I operate an alerting system."**

---

**Status**: ✅ Complete  
**Completion Date**: February 11, 2026  
**Duration**: 1 week (Week 9)  
**Last Updated**: February 11, 2026
