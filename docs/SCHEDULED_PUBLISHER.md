# Scheduled Publisher System

## Overview

The Scheduled Publisher is an automated Lambda function that runs on a schedule to publish articles and news items at their scheduled time. It checks every 5 minutes for content that should be published and automatically updates their status from "scheduled" to "published".

## Architecture

### Components

1. **Lambda Function**: `scheduled-publisher`
   - Runtime: Python 3.12
   - Memory: 256 MB
   - Timeout: 60 seconds
   - Region: us-east-1

2. **EventBridge Rule**: `scheduled-publisher-trigger`
   - Schedule: `rate(5 minutes)` (runs 288 times/day)
   - State: ENABLED
   - Triggers the Lambda function automatically

3. **DynamoDB Tables**:
   - `articles` - Stores article content with scheduled_publish timestamps
   - `news-table` - Stores news items with scheduled_publish timestamps
   - `email_subscribers` - Used to send notifications when content is published

### File Structure

```
Downloader/
├── scheduled-publisher/
│   ├── lambda_function.py          # Main Lambda code
│   └── lambda.zip                  # Deployment package
├── deploy-scheduled-publisher.ps1  # Deployment script
└── check-scheduled-article.ps1     # Utility script to check scheduled articles
```

## How It Works

1. **EventBridge Trigger**: Every 5 minutes, EventBridge invokes the Lambda function
2. **Scan Tables**: Lambda scans both `articles` and `news-table` for items with `status = 'scheduled'`
3. **Check Time**: For each scheduled item, compares `scheduled_publish` timestamp with current UTC time
4. **Publish**: If scheduled time has passed, updates status to "published" and sends notifications
5. **Notifications**: Invokes `notifications_api` Lambda to email all active subscribers

### Publishing Logic

```python
# Item is published if:
scheduled_time <= current_time (UTC)

# Example:
# Article scheduled for: 2026-03-23T14:10:00.000Z
# Current time:          2026-03-23T16:00:00.000Z
# Result: Article is published ✓
```

## Cost Analysis

### AWS Free Tier (First 12 Months)
- **Lambda Invocations**: 1 million requests/month (FREE)
  - Scheduled publisher uses: ~8,640/month
  - Remaining: 991,360 requests for other functions

- **Lambda Duration**: 400,000 GB-seconds/month (FREE)
  - Scheduled publisher uses: ~1,728 GB-seconds/month
  - Remaining: 398,272 GB-seconds

- **DynamoDB**: 25 GB storage + 25 read/write capacity units (FREE)
  - Scheduled publisher scans: ~260,000 read requests/month
  - Well within free tier limits

- **CloudWatch Logs**: 5 GB ingestion/month (FREE)
  - Scheduled publisher logs: <1 MB/month

### After Free Tier
- **Lambda**: $0.20 per 1M requests + $0.0000166667 per GB-second
  - Monthly cost: ~$0.002 (essentially free)

- **DynamoDB On-Demand**: $0.25 per million read requests
  - Monthly cost: ~$0.065

- **Total Monthly Cost**: ~$0.07/month (7 cents)

### Cost Optimization Options

**Change Schedule Frequency:**
```bash
# Every 15 minutes (96 times/day, ~2,880/month)
aws events put-rule --name scheduled-publisher-trigger --schedule-expression "rate(15 minutes)" --state ENABLED --region us-east-1 --profile ekewaka

# Every 30 minutes (48 times/day, ~1,440/month)
aws events put-rule --name scheduled-publisher-trigger --schedule-expression "rate(30 minutes)" --state ENABLED --region us-east-1 --profile ekewaka

# Every hour (24 times/day, ~720/month)
aws events put-rule --name scheduled-publisher-trigger --schedule-expression "rate(1 hour)" --state ENABLED --region us-east-1 --profile ekewaka

# Specific times (e.g., every 6 hours: midnight, 6am, noon, 6pm)
aws events put-rule --name scheduled-publisher-trigger --schedule-expression "cron(0 0,6,12,18 * * ? *)" --state ENABLED --region us-east-1 --profile ekewaka
```

## Deployment

### Initial Deployment

```powershell
# From Downloader directory
.\deploy-scheduled-publisher.ps1
```

This script:
1. Creates deployment package (lambda.zip)
2. Creates or updates Lambda function
3. Creates EventBridge rule (if new deployment)
4. Adds Lambda invoke permissions for EventBridge
5. Configures EventBridge to trigger Lambda

### Update Existing Deployment

```powershell
# Same command - script detects existing function
.\deploy-scheduled-publisher.ps1
```

## Management Commands

### Check Current Schedule

```bash
aws events describe-rule --name scheduled-publisher-trigger --profile ekewaka --region us-east-1
```

### Change Schedule

```bash
# Change to every 15 minutes
aws events put-rule --name scheduled-publisher-trigger --schedule-expression "rate(15 minutes)" --state ENABLED --region us-east-1 --profile ekewaka
```

### Disable Scheduler

```bash
aws events disable-rule --name scheduled-publisher-trigger --region us-east-1 --profile ekewaka
```

### Enable Scheduler

```bash
aws events enable-rule --name scheduled-publisher-trigger --region us-east-1 --profile ekewaka
```

### Manual Invocation (Testing)

```bash
aws lambda invoke --function-name scheduled-publisher --profile ekewaka --region us-east-1 response.json
type response.json
```

### View Logs

```bash
# Last 5 minutes
aws logs tail /aws/lambda/scheduled-publisher --profile ekewaka --region us-east-1 --since 5m

# Follow live logs
aws logs tail /aws/lambda/scheduled-publisher --profile ekewaka --region us-east-1 --follow
```

### Check Scheduled Articles

```powershell
# Use utility script
.\check-scheduled-article.ps1
```

Or manually:
```bash
aws dynamodb scan --table-name articles --filter-expression "#s = :status" --expression-attribute-names "{\"#s\":\"status\"}" --expression-attribute-values "{\":status\":{\"S\":\"scheduled\"}}" --profile ekewaka --region us-east-1
```

## Troubleshooting

### Common Issues

#### 1. Lambda Finding 0 Scheduled Articles

**Symptoms**: Logs show "Found 0 scheduled articles" but articles exist in DynamoDB

**Causes**:
- Missing DynamoDB permissions
- DynamoDB scan not paginating (only reading first page)
- Wrong region configuration

**Solutions**:
```bash
# Check IAM permissions
aws iam get-role-policy --role-name lambda-execution-role --policy-name scheduled-publisher-dynamodb --profile ekewaka --region us-east-1

# Verify Lambda region
aws lambda get-function --function-name scheduled-publisher --profile ekewaka --region us-east-1 --query "Configuration.Environment"
```

#### 2. Timezone Comparison Errors

**Symptoms**: Error "can't compare offset-naive and offset-aware datetimes"

**Cause**: scheduled_publish timestamp missing timezone info

**Solution**: Lambda code ensures all timestamps are timezone-aware:
```python
if scheduled_time.tzinfo is None:
    scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
```

#### 3. Articles Not Publishing

**Symptoms**: Articles remain "scheduled" past their publish time

**Checks**:
1. Verify EventBridge rule is enabled
2. Check Lambda logs for errors
3. Verify article scheduled_publish format: `2026-03-23T14:10:00.000Z`
4. Confirm Lambda has UpdateItem permissions

### Debug Mode

The Lambda includes detailed logging:
- Total articles scanned
- Status breakdown (scheduled, published, draft)
- Each scheduled article found with ID and scheduled time
- Publishing actions taken

## IAM Permissions Required

### Lambda Execution Role

The Lambda needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:371751795928:table/articles",
        "arn:aws:dynamodb:us-east-1:371751795928:table/news-table",
        "arn:aws:dynamodb:us-east-1:371751795928:table/email_subscribers"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:371751795928:function:notifications_api"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### EventBridge Permissions

EventBridge needs permission to invoke the Lambda:

```json
{
  "FunctionName": "scheduled-publisher",
  "StatementId": "scheduled-publisher-event",
  "Action": "lambda:InvokeFunction",
  "Principal": "events.amazonaws.com",
  "SourceArn": "arn:aws:events:us-east-1:371751795928:rule/scheduled-publisher-trigger"
}
```

## Bug Fixes Applied

### March 23, 2026

1. **DynamoDB Permissions Issue**
   - Added `scheduled-publisher-dynamodb` policy to Lambda role
   - Granted Scan and UpdateItem permissions for articles, news-table, email_subscribers

2. **Pagination Bug**
   - Lambda was only reading first page of DynamoDB scan (19 items instead of 76)
   - Added pagination loop to scan all items:
   ```python
   while True:
       response = articles_table.scan(**scan_kwargs)
       article_items.extend(response.get('Items', []))
       last_key = response.get('LastEvaluatedKey')
       if not last_key:
           break
       scan_kwargs['ExclusiveStartKey'] = last_key
   ```

3. **Timezone Comparison Bug**
   - Fixed "can't compare offset-naive and offset-aware datetimes" error
   - Ensured all datetime objects are timezone-aware (UTC)

4. **Region Configuration**
   - Explicitly set region to us-east-1 in boto3 clients:
   ```python
   dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
   ```

## Integration with Article System

### Creating Scheduled Articles

In `create-article.html` or `edit-article.html`:

1. Set status to "scheduled"
2. Set scheduled_publish timestamp: `2026-03-23T14:10:00.000Z`
3. Save article

The scheduled publisher will automatically publish it when the time arrives.

### Article Status Flow

```
draft → scheduled → published
  ↓         ↓
  └─────────┴──────→ published (manual)
```

## Monitoring

### Key Metrics to Watch

1. **Invocation Count**: Should be ~288/day (every 5 minutes)
2. **Error Rate**: Should be 0%
3. **Duration**: Should be <2 seconds
4. **Scheduled Articles Found**: Check logs for count
5. **Articles Published**: Check logs for successful publications

### CloudWatch Alarms (Optional)

```bash
# Create alarm for Lambda errors
aws cloudwatch put-metric-alarm \
  --alarm-name scheduled-publisher-errors \
  --alarm-description "Alert when scheduled publisher has errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=scheduled-publisher \
  --profile ekewaka --region us-east-1
```

## Future Enhancements

### Potential Improvements

1. **Batch Publishing**: Publish multiple articles in parallel
2. **Retry Logic**: Retry failed publications with exponential backoff
3. **Dead Letter Queue**: Capture failed publications for manual review
4. **Notification Preferences**: Allow users to opt-in/out of specific content types
5. **Preview Mode**: Send preview emails before publishing
6. **Scheduling UI**: Calendar view of scheduled content
7. **Time Zone Support**: Schedule in local time zones, not just UTC

## Related Documentation

- [NEWS_MANAGEMENT_SYSTEM.md](NEWS_MANAGEMENT_SYSTEM.md) - News article system
- [ARTICLE_ANALYTICS.md](ARTICLE_ANALYTICS.md) - Article analytics
- [Email Marketing/README.md](../Email%20Marketing/README.md) - Email marketing system
- [aws-commands-guide.md](aws-commands-guide.md) - AWS CLI reference

---

**Last Updated**: March 23, 2026  
**Version**: 1.0  
**Status**: Production Ready  
**Maintainer**: Christian Conservatives Today Platform
