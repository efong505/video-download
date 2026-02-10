# Week 1: SQS Message Queues Implementation

## Overview

Add Amazon SQS (Simple Queue Service) to decouple Lambda functions and enable:
- Automatic retry logic for failed operations
- Backpressure handling during traffic spikes
- Dead Letter Queues (DLQ) for failed messages
- Better observability and debugging

**Time Required:** 8-12 hours
**Cost Impact:** +$5/month
**Risk Level:** Low (additive, non-breaking)

---

## Architecture Changes

### Current Architecture (Tight Coupling)
```
User Request → router Lambda → downloader Lambda (direct invoke)
                             → thumbnail Lambda (direct invoke)
```

**Problems:**
- If downloader fails, request fails immediately
- No retry logic
- Synchronous blocking
- Hard to debug failures

### New Architecture (Loose Coupling)
```
User Request → router Lambda → SQS Queue → downloader Lambda
                                         → SQS Queue → thumbnail Lambda
                                         → DLQ (failed messages)
```

**Benefits:**
- Automatic retries (up to 3 times)
- Asynchronous processing
- Failed messages go to DLQ for investigation
- Better monitoring and alerting

---

## Queues to Create

### 1. video-processing-queue
**Purpose:** Video download and processing jobs
**Configuration:**
- Visibility Timeout: 900 seconds (15 minutes)
- Message Retention: 4 days
- Max Receives: 3 (retry 3 times before DLQ)
- DLQ: video-processing-dlq

### 2. thumbnail-generation-queue
**Purpose:** Thumbnail generation after video upload
**Configuration:**
- Visibility Timeout: 300 seconds (5 minutes)
- Message Retention: 1 day
- Max Receives: 3
- DLQ: thumbnail-generation-dlq

### 3. email-queue
**Purpose:** Email sending (newsletters, notifications)
**Configuration:**
- Visibility Timeout: 60 seconds
- Message Retention: 2 days
- Max Receives: 5 (emails can retry more)
- DLQ: email-dlq

### 4. analytics-queue
**Purpose:** Article views, video plays, user actions
**Configuration:**
- Visibility Timeout: 30 seconds
- Message Retention: 1 day
- Max Receives: 2
- DLQ: analytics-dlq

---

## Implementation Steps

### Step 1: Create SQS Queues (AWS Console)

#### 1.1 Navigate to SQS
1. Open AWS Console
2. Search for "SQS" in services
3. Click "Create queue"

#### 1.2 Create video-processing-dlq (Dead Letter Queue First)
1. **Type:** Standard Queue
2. **Name:** video-processing-dlq
3. **Configuration:**
   - Visibility timeout: 900 seconds
   - Message retention period: 14 days (max)
   - Delivery delay: 0 seconds
   - Maximum message size: 256 KB
   - Receive message wait time: 0 seconds
4. **Access policy:** Default (only queue owner)
5. Click "Create queue"
6. **Copy the Queue ARN** (you'll need this)

#### 1.3 Create video-processing-queue
1. **Type:** Standard Queue
2. **Name:** video-processing-queue
3. **Configuration:**
   - Visibility timeout: 900 seconds
   - Message retention period: 4 days
   - Delivery delay: 0 seconds
   - Maximum message size: 256 KB
   - Receive message wait time: 0 seconds (short polling)
4. **Dead-letter queue:**
   - ✅ Enable
   - Choose queue: video-processing-dlq
   - Maximum receives: 3
5. Click "Create queue"
6. **Copy the Queue URL** (you'll need this)

#### 1.4 Repeat for Other Queues
Create these queue pairs (DLQ first, then main queue):
- thumbnail-generation-dlq → thumbnail-generation-queue
- email-dlq → email-queue
- analytics-dlq → analytics-queue

---

### Step 2: Create SQS Queues (AWS CLI - Bash)

```bash
#!/bin/bash
# create-sqs-queues.sh

REGION="us-east-1"

echo "Creating Dead Letter Queues..."

# Create DLQs
aws sqs create-queue \
    --queue-name video-processing-dlq \
    --region $REGION \
    --attributes '{
        "MessageRetentionPeriod": "1209600",
        "VisibilityTimeout": "900"
    }'

aws sqs create-queue \
    --queue-name thumbnail-generation-dlq \
    --region $REGION \
    --attributes '{
        "MessageRetentionPeriod": "1209600",
        "VisibilityTimeout": "300"
    }'

aws sqs create-queue \
    --queue-name email-dlq \
    --region $REGION \
    --attributes '{
        "MessageRetentionPeriod": "1209600",
        "VisibilityTimeout": "60"
    }'

aws sqs create-queue \
    --queue-name analytics-dlq \
    --region $REGION \
    --attributes '{
        "MessageRetentionPeriod": "1209600",
        "VisibilityTimeout": "30"
    }'

echo "Getting DLQ ARNs..."

VIDEO_DLQ_ARN=$(aws sqs get-queue-attributes \
    --queue-url $(aws sqs get-queue-url --queue-name video-processing-dlq --query 'QueueUrl' --output text) \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

THUMBNAIL_DLQ_ARN=$(aws sqs get-queue-attributes \
    --queue-url $(aws sqs get-queue-url --queue-name thumbnail-generation-dlq --query 'QueueUrl' --output text) \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

EMAIL_DLQ_ARN=$(aws sqs get-queue-attributes \
    --queue-url $(aws sqs get-queue-url --queue-name email-dlq --query 'QueueUrl' --output text) \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

ANALYTICS_DLQ_ARN=$(aws sqs get-queue-attributes \
    --queue-url $(aws sqs get-queue-url --queue-name analytics-dlq --query 'QueueUrl' --output text) \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

echo "Creating Main Queues with DLQ configuration..."

# Create main queues with DLQ
aws sqs create-queue \
    --queue-name video-processing-queue \
    --region $REGION \
    --attributes "{
        \"MessageRetentionPeriod\": \"345600\",
        \"VisibilityTimeout\": \"900\",
        \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$VIDEO_DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"
    }"

aws sqs create-queue \
    --queue-name thumbnail-generation-queue \
    --region $REGION \
    --attributes "{
        \"MessageRetentionPeriod\": \"86400\",
        \"VisibilityTimeout\": \"300\",
        \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$THUMBNAIL_DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"
    }"

aws sqs create-queue \
    --queue-name email-queue \
    --region $REGION \
    --attributes "{
        \"MessageRetentionPeriod\": \"172800\",
        \"VisibilityTimeout\": \"60\",
        \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$EMAIL_DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"5\\\"}\"
    }"

aws sqs create-queue \
    --queue-name analytics-queue \
    --region $REGION \
    --attributes "{
        \"MessageRetentionPeriod\": \"86400\",
        \"VisibilityTimeout\": \"30\",
        \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$ANALYTICS_DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"2\\\"}\"
    }"

echo "✅ All queues created successfully!"
echo ""
echo "Queue URLs:"
aws sqs list-queues --region $REGION
```

---

### Step 3: Create SQS Queues (PowerShell)

```powershell
# create-sqs-queues.ps1

$Region = "us-east-1"

Write-Host "Creating Dead Letter Queues..." -ForegroundColor Cyan

# Create DLQs
aws sqs create-queue `
    --queue-name video-processing-dlq `
    --region $Region `
    --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"900\"}'

aws sqs create-queue `
    --queue-name thumbnail-generation-dlq `
    --region $Region `
    --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"300\"}'

aws sqs create-queue `
    --queue-name email-dlq `
    --region $Region `
    --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"60\"}'

aws sqs create-queue `
    --queue-name analytics-dlq `
    --region $Region `
    --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"30\"}'

Write-Host "Getting DLQ ARNs..." -ForegroundColor Cyan

$VideoDlqUrl = aws sqs get-queue-url --queue-name video-processing-dlq --query 'QueueUrl' --output text
$VideoDlqArn = aws sqs get-queue-attributes --queue-url $VideoDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text

$ThumbnailDlqUrl = aws sqs get-queue-url --queue-name thumbnail-generation-dlq --query 'QueueUrl' --output text
$ThumbnailDlqArn = aws sqs get-queue-attributes --queue-url $ThumbnailDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text

$EmailDlqUrl = aws sqs get-queue-url --queue-name email-dlq --query 'QueueUrl' --output text
$EmailDlqArn = aws sqs get-queue-attributes --queue-url $EmailDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text

$AnalyticsDlqUrl = aws sqs get-queue-url --queue-name analytics-dlq --query 'QueueUrl' --output text
$AnalyticsDlqArn = aws sqs get-queue-attributes --queue-url $AnalyticsDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text

Write-Host "Creating Main Queues with DLQ configuration..." -ForegroundColor Cyan

# Create main queues with DLQ
aws sqs create-queue `
    --queue-name video-processing-queue `
    --region $Region `
    --attributes "{`"MessageRetentionPeriod`":`"345600`",`"VisibilityTimeout`":`"900`",`"RedrivePolicy`":`"{\\`"deadLetterTargetArn\\`":\\`"$VideoDlqArn\\`",\\`"maxReceiveCount\\`":\\`"3\\`"}`"}"

aws sqs create-queue `
    --queue-name thumbnail-generation-queue `
    --region $Region `
    --attributes "{`"MessageRetentionPeriod`":`"86400`",`"VisibilityTimeout`":`"300`",`"RedrivePolicy`":`"{\\`"deadLetterTargetArn\\`":\\`"$ThumbnailDlqArn\\`",\\`"maxReceiveCount\\`":\\`"3\\`"}`"}"

aws sqs create-queue `
    --queue-name email-queue `
    --region $Region `
    --attributes "{`"MessageRetentionPeriod`":`"172800`",`"VisibilityTimeout`":`"60`",`"RedrivePolicy`":`"{\\`"deadLetterTargetArn\\`":\\`"$EmailDlqArn\\`",\\`"maxReceiveCount\\`":\\`"5\\`"}`"}"

aws sqs create-queue `
    --queue-name analytics-queue `
    --region $Region `
    --attributes "{`"MessageRetentionPeriod`":`"86400`",`"VisibilityTimeout`":`"30`",`"RedrivePolicy`":`"{\\`"deadLetterTargetArn\\`":\\`"$AnalyticsDlqArn\\`",\\`"maxReceiveCount\\`":\\`"2\\`"}`"}"

Write-Host "✅ All queues created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Queue URLs:" -ForegroundColor Cyan
aws sqs list-queues --region $Region
```

---

### Step 4: Update IAM Permissions

Add SQS permissions to Lambda execution role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
            ],
            "Resource": [
                "arn:aws:sqs:us-east-1:*:video-processing-queue",
                "arn:aws:sqs:us-east-1:*:thumbnail-generation-queue",
                "arn:aws:sqs:us-east-1:*:email-queue",
                "arn:aws:sqs:us-east-1:*:analytics-queue"
            ]
        }
    ]
}
```

**AWS Console Steps:**
1. Go to IAM → Roles
2. Find your Lambda execution role (e.g., `lambda-execution-role`)
3. Click "Add permissions" → "Create inline policy"
4. Choose JSON tab
5. Paste the policy above
6. Name it `SQSAccessPolicy`
7. Click "Create policy"

---

### Step 5: Update Lambda Functions

#### router/index.py (Send to Queue)

```python
import boto3
import json
import os

sqs = boto3.client('sqs')

# Get queue URLs from environment variables
VIDEO_QUEUE_URL = os.environ.get('VIDEO_QUEUE_URL')

def lambda_handler(event, context):
    # ... existing quota check code ...
    
    # Instead of direct Lambda invoke:
    # lambda_client.invoke(FunctionName='downloader', Payload=job_data)
    
    # Send to SQS queue:
    response = sqs.send_message(
        QueueUrl=VIDEO_QUEUE_URL,
        MessageBody=json.dumps({
            'job_id': job_id,
            'video_url': video_url,
            'user_email': user_email,
            'quality': quality,
            'timestamp': int(time.time())
        }),
        MessageAttributes={
            'JobType': {
                'StringValue': 'video_download',
                'DataType': 'String'
            },
            'Priority': {
                'StringValue': 'normal',
                'DataType': 'String'
            }
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Job queued successfully',
            'job_id': job_id,
            'queue_message_id': response['MessageId']
        })
    }
```

#### downloader/index.py (Process from Queue)

```python
import boto3
import json

def lambda_handler(event, context):
    """
    This Lambda is now triggered by SQS, not direct invocation.
    Event structure is different.
    """
    
    # Process each message from SQS
    for record in event['Records']:
        # Parse message body
        message_body = json.loads(record['body'])
        
        job_id = message_body['job_id']
        video_url = message_body['video_url']
        user_email = message_body['user_email']
        
        try:
            # ... existing video download code ...
            
            print(f"✅ Successfully processed job {job_id}")
            
            # SQS automatically deletes message on successful return
            
        except Exception as e:
            print(f"❌ Error processing job {job_id}: {str(e)}")
            
            # Raise exception to trigger retry
            # After 3 retries, message goes to DLQ
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processed all messages')
    }
```

---

### Step 6: Configure Lambda Triggers

#### AWS Console Method:
1. Go to Lambda → Functions → downloader
2. Click "Add trigger"
3. Select "SQS"
4. Choose queue: video-processing-queue
5. Batch size: 1 (process one video at a time)
6. Enable trigger: ✅
7. Click "Add"

#### AWS CLI Method (Bash):
```bash
# Get Lambda ARN
LAMBDA_ARN=$(aws lambda get-function --function-name downloader --query 'Configuration.FunctionArn' --output text)

# Get Queue ARN
QUEUE_ARN=$(aws sqs get-queue-attributes \
    --queue-url $(aws sqs get-queue-url --queue-name video-processing-queue --query 'QueueUrl' --output text) \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

# Create event source mapping
aws lambda create-event-source-mapping \
    --function-name downloader \
    --event-source-arn $QUEUE_ARN \
    --batch-size 1 \
    --enabled
```

#### PowerShell Method:
```powershell
# Get Lambda ARN
$LambdaArn = aws lambda get-function --function-name downloader --query 'Configuration.FunctionArn' --output text

# Get Queue ARN
$QueueUrl = aws sqs get-queue-url --queue-name video-processing-queue --query 'QueueUrl' --output text
$QueueArn = aws sqs get-queue-attributes --queue-url $QueueUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text

# Create event source mapping
aws lambda create-event-source-mapping `
    --function-name downloader `
    --event-source-arn $QueueArn `
    --batch-size 1 `
    --enabled
```

---

### Step 7: Add Environment Variables

Update Lambda environment variables to include queue URLs:

```powershell
# Update router Lambda
aws lambda update-function-configuration `
    --function-name router `
    --environment "Variables={
        VIDEO_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/video-processing-queue,
        THUMBNAIL_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/thumbnail-generation-queue,
        EMAIL_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/email-queue,
        ANALYTICS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/analytics-queue
    }"
```

---

## Testing

### Test 1: Send Test Message

```bash
# Send test message to queue
aws sqs send-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/video-processing-queue \
    --message-body '{
        "job_id": "test-123",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "user_email": "test@example.com",
        "quality": "720p"
    }'
```

### Test 2: Monitor Queue

```bash
# Check queue depth
aws sqs get-queue-attributes \
    --queue-url https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/video-processing-queue \
    --attribute-names ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible
```

### Test 3: Check DLQ

```bash
# Check if any messages failed
aws sqs get-queue-attributes \
    --queue-url https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/video-processing-dlq \
    --attribute-names ApproximateNumberOfMessages
```

---

## Monitoring

### CloudWatch Metrics to Watch

1. **NumberOfMessagesSent** - Messages added to queue
2. **NumberOfMessagesReceived** - Messages processed
3. **ApproximateAgeOfOldestMessage** - Queue backlog
4. **NumberOfMessagesDeleted** - Successful processing
5. **ApproximateNumberOfMessagesVisible** - Queue depth

### Create CloudWatch Alarm

```bash
# Alert if DLQ has messages (indicates failures)
aws cloudwatch put-metric-alarm \
    --alarm-name video-processing-dlq-alarm \
    --alarm-description "Alert when messages in DLQ" \
    --metric-name ApproximateNumberOfMessagesVisible \
    --namespace AWS/SQS \
    --statistic Average \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 1 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=QueueName,Value=video-processing-dlq
```

---

## Rollback Plan

If issues occur:

```powershell
# 1. Disable SQS trigger
aws lambda update-event-source-mapping \
    --uuid EVENT_SOURCE_MAPPING_UUID \
    --no-enabled

# 2. Drain queue (process remaining messages)
# Let existing messages complete

# 3. Revert Lambda code to previous version
aws lambda update-function-code \
    --function-name router \
    --s3-bucket your-deployment-bucket \
    --s3-key router-previous-version.zip

# 4. Delete queues (optional)
aws sqs delete-queue --queue-url QUEUE_URL
```

---

## Success Criteria

✅ All 8 queues created (4 main + 4 DLQ)
✅ Lambda functions updated to use SQS
✅ Event source mappings configured
✅ IAM permissions granted
✅ Test messages processed successfully
✅ CloudWatch alarms configured
✅ No messages in DLQ after testing

**Next:** Proceed to Week 2 - ElastiCache Implementation
