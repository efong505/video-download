# Email Drip System - Testing & Operations Guide

## System Status: ✅ FULLY OPERATIONAL

The complete 7-email drip campaign automation is now live and working.

## What Was Fixed

1. **Enrollment Structure**: Changed from `campaign_id` to `sequence_name` + `filter_tags`
2. **Campaign Lookup**: Drip processor now queries by `user_id` and filters by tags
3. **Field Names**: Standardized `current_sequence_number` across both Lambdas
4. **Deployment**: Fixed PowerShell zip creation and Lambda deployment process

## Testing Scripts

### 1. Test New Signup
```bash
python -c "import requests, json; from datetime import datetime; email = f'test-{datetime.now().strftime(\"%Y%m%d%H%M%S\")}@example.com'; r = requests.post('https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe', json={'email': email, 'name': 'Test User', 'list_type': 'book'}); print(f'Email: {email}'); print(json.dumps(r.json(), indent=2))"
```

### 2. Check Enrollments
```bash
# Check specific email
python check_drip_enrollments.py test@example.com

# Check all active enrollments
python check_drip_enrollments.py
```

### 3. Backdate Enrollment (for testing)
```bash
# Edit backdate_enrollment.py to set the email
python backdate_enrollment.py
```

### 4. Manually Trigger Drip Processor
```bash
aws lambda invoke --function-name email-drip-processor --payload "{}" response.json --profile ekewaka --region us-east-1 && type response.json
```

### 5. Check Logs
```bash
# Tail logs in real-time
aws logs tail /aws/lambda/email-drip-processor --follow --profile ekewaka --region us-east-1

# Get recent logs
aws logs tail /aws/lambda/email-drip-processor --since 5m --profile ekewaka --region us-east-1

# Filter specific time range
aws logs filter-log-events --log-group-name /aws/lambda/email-drip-processor --start-time 1742675200000 --profile ekewaka --region us-east-1 --query "events[-20:].message" --output text
```

## How It Works

### Enrollment Flow
1. User signs up on book landing page
2. `email-subscription-handler` Lambda:
   - Saves to `book-subscribers` table
   - Sends welcome email with 4 PDFs
   - Bridges to `user-email-subscribers` table with tags `['book', 'survival-kit']`
   - **Auto-enrolls** in drip sequence:
     ```python
     {
       'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
       'enrollment_id': 'email@example.com#book-welcome-sequence',
       'subscriber_email': 'email@example.com',
       'sequence_name': 'book-welcome-sequence',
       'filter_tags': ['book', 'survival-kit'],
       'enrolled_at': '2026-03-19T20:48:49.803938',
       'current_sequence_number': 0,
       'status': 'active'
     }
     ```

### Daily Processing (9am EST)
1. EventBridge triggers `email-drip-processor` Lambda
2. Processor scans all active enrollments
3. For each enrollment:
   - Queries campaigns by `user_id`
   - Filters campaigns by matching `filter_tags`
   - Sorts by `sequence_number`
   - Finds next email (current_sequence + 1)
   - Calculates due date: `enrolled_at + delay_days` (or `last_sent_at + delay_days`)
   - If due, sends to SQS queue
   - Updates `current_sequence_number` and `last_sent_at`
4. When sequence complete (no more emails), marks enrollment as `completed`

### Email Schedule
- **Day 0**: Welcome email with PDFs (immediate, not part of drip)
- **Day 1**: First drip email (delay_days: 1)
- **Day 3**: Second email (delay_days: 2 from Day 1)
- **Day 5**: Third email (delay_days: 2 from Day 3)
- **Day 7**: Fourth email (delay_days: 2 from Day 5)
- **Day 10**: Fifth email (delay_days: 3 from Day 7)
- **Day 14**: Sixth email (delay_days: 4 from Day 10)

## Monitoring

### Check System Health
```bash
# Check EventBridge rule
aws events describe-rule --name email-drip-processor-daily --profile ekewaka --region us-east-1

# Check Lambda last modified
aws lambda get-function --function-name email-drip-processor --profile ekewaka --region us-east-1 --query "Configuration.LastModified"

# Count active enrollments
aws dynamodb scan --table-name user-email-drip-enrollments --filter-expression "#status = :status" --expression-attribute-names "{\"#status\":\"status\"}" --expression-attribute-values "{\":status\":{\"S\":\"active\"}}" --select COUNT --profile ekewaka --region us-east-1
```

### Check SQS Queue
```bash
# Get queue attributes
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue --attribute-names All --profile ekewaka --region us-east-1
```

## Manual Operations

### Enroll Existing Subscribers
```bash
python enroll_existing_subscribers.py
```
This script:
- Queries all subscribers under Ed's user_id
- Filters for those with 'book' or 'survival-kit' tags
- Enrolls them in the drip sequence
- Skips if already enrolled

### Pause/Resume Enrollment
```bash
# Pause
aws dynamodb update-item --table-name user-email-drip-enrollments --key "{\"user_id\":{\"S\":\"effa3242-cf64-4021-b2b0-c8a5a9dfd6d2\"},\"enrollment_id\":{\"S\":\"email@example.com#book-welcome-sequence\"}}" --update-expression "SET #status = :status" --expression-attribute-names "{\"#status\":\"status\"}" --expression-attribute-values "{\":status\":{\"S\":\"paused\"}}" --profile ekewaka --region us-east-1

# Resume
aws dynamodb update-item --table-name user-email-drip-enrollments --key "{\"user_id\":{\"S\":\"effa3242-cf64-4021-b2b0-c8a5a9dfd6d2\"},\"enrollment_id\":{\"S\":\"email@example.com#book-welcome-sequence\"}}" --update-expression "SET #status = :status" --expression-attribute-names "{\"#status\":\"status\"}" --expression-attribute-values "{\":status\":{\"S\":\"active\"}}" --profile ekewaka --region us-east-1
```

### Delete Enrollment
```bash
aws dynamodb delete-item --table-name user-email-drip-enrollments --key "{\"user_id\":{\"S\":\"effa3242-cf64-4021-b2b0-c8a5a9dfd6d2\"},\"enrollment_id\":{\"S\":\"email@example.com#book-welcome-sequence\"}}" --profile ekewaka --region us-east-1
```

## Deployment

### Update Drip Processor
```bash
cd email-drip-processor
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath package.zip -Force"
aws lambda update-function-code --function-name email-drip-processor --zip-file fileb://package.zip --profile ekewaka --region us-east-1
```

### Update Subscription Handler
```bash
cd email-subscription-handler
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath package.zip -Force"
aws lambda update-function-code --function-name email-subscription-handler --zip-file fileb://package.zip --profile ekewaka --region us-east-1
```

### Update S3 Files
```bash
.\s3-push.ps1 the-necessary-evil-book.html
```

## Troubleshooting

### No Emails Being Sent
1. Check enrollments exist: `python check_drip_enrollments.py`
2. Check campaigns exist: `aws dynamodb scan --table-name user-email-campaigns --filter-expression "attribute_exists(sequence_number)" --profile ekewaka --region us-east-1`
3. Check logs: `aws logs tail /aws/lambda/email-drip-processor --since 10m --profile ekewaka --region us-east-1`
4. Manually trigger: `aws lambda invoke --function-name email-drip-processor --payload "{}" response.json --profile ekewaka --region us-east-1`

### Emails Not Due Yet
- Day 1 email sends 1 day AFTER enrollment
- Use `backdate_enrollment.py` to test immediately

### Subscriber Not Active
- Check subscriber status: `aws dynamodb get-item --table-name user-email-subscribers --key "{\"user_id\":{\"S\":\"effa3242-cf64-4021-b2b0-c8a5a9dfd6d2\"},\"subscriber_email\":{\"S\":\"email@example.com\"}}" --profile ekewaka --region us-east-1`
- Enrollment will be paused if subscriber is not active

## AWS Resources

- **Account**: 371751795928 (ekewaka profile)
- **Region**: us-east-1
- **Lambdas**: 
  - `email-subscription-handler` (handles signups, sends welcome email, enrolls in drip)
  - `email-drip-processor` (processes enrollments daily)
  - `email-sender` (processes SQS queue, sends actual emails)
- **DynamoDB Tables**:
  - `book-subscribers` (simple list)
  - `user-email-subscribers` (multi-tenant with tags)
  - `user-email-campaigns` (7 drip campaigns with sequence_number, delay_days)
  - `user-email-drip-enrollments` (enrollment tracking)
- **SQS**: `email-sending-queue`
- **EventBridge**: `email-drip-processor-daily` (cron: `0 14 * * ? *` = 9am EST)
- **S3**: `my-video-downloads-bucket/book-pdfs/`

## Next Steps

1. **Monitor first real drip sends** tomorrow at 9am EST
2. **Track email engagement** (opens, clicks) via existing tracking system
3. **Analyze conversion rates** from drip sequence to book purchases
4. **A/B test** subject lines and content
5. **Add unsubscribe** functionality to drip emails
6. **Build admin dashboard** to view enrollment status and metrics
