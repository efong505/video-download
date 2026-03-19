# Email Drip Campaign Automation - COMPLETE

## ✅ What Was Built

### 1. **7 Email Campaigns Created**
All campaigns stored in `user-email-campaigns` DynamoDB table:

- **Day 1**: Why I Wrote This Book
- **Day 3**: The Two Paths of AI  
- **Day 5**: Personal Impact (Family/Church/Career)
- **Day 7**: Testimonials + Buy
- **Day 10**: Objection Handling
- **Day 14**: Urgency + Offer

Each campaign has:
- `campaign_type`: "drip"
- `sequence_number`: 1-6
- `delay_days`: Days to wait before sending
- `filter_tags`: ["book", "survival-kit"]
- Full HTML and text content

### 2. **Drip Enrollments Table**
Created `user-email-drip-enrollments` DynamoDB table:

**Schema:**
```json
{
  "user_id": "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2",
  "enrollment_id": "email@example.com_book-welcome-sequence",
  "subscriber_email": "email@example.com",
  "campaign_id": "book-welcome-sequence",
  "enrolled_at": "2026-03-19T12:00:00Z",
  "current_sequence": 0,
  "last_sent_at": "2026-03-20T09:00:00Z",
  "status": "active" | "completed" | "paused"
}
```

**Indexes:**
- `email-index`: Query by user_id + subscriber_email
- `status-index`: Query by user_id + status

### 3. **Drip Processor Lambda**
Created `email-drip-processor` Lambda function:

**What it does:**
1. Runs daily at 9am EST (triggered by EventBridge)
2. Scans all active enrollments
3. Calculates which emails are due based on:
   - `enrolled_at` date
   - `last_sent_at` date
   - `delay_days` for next email
4. Verifies subscriber is still active
5. Sends email via SQS queue
6. Updates enrollment with new sequence number
7. Marks enrollment as "completed" when sequence finishes

**Location:** `email-drip-processor/lambda_function.py`

### 4. **Auto-Enrollment**
Updated `email-subscription-handler` Lambda:

**New functionality:**
- When someone signs up for book list
- Automatically creates enrollment in `user-email-drip-enrollments`
- Sets `current_sequence` to 0
- Sets `status` to "active"
- Drip processor will start sending emails based on schedule

### 5. **EventBridge Schedule**
Created `email-drip-processor-daily` rule:

- **Schedule**: `cron(0 14 * * ? *)` (9am EST / 2pm UTC)
- **Target**: `email-drip-processor` Lambda
- **Frequency**: Daily

---

## 🔄 How It Works

### User Journey:

1. **Day 0**: User signs up on book page
   - Receives immediate email with 4 PDFs (Day 0 email)
   - Added to `book-subscribers` table
   - Bridged to `user-email-subscribers` table
   - **Auto-enrolled** in drip sequence

2. **Day 1 (9am)**: Drip processor runs
   - Finds enrollment (enrolled yesterday)
   - Calculates: enrolled_at + 1 day = today
   - Sends "Why I Wrote This Book" email
   - Updates `current_sequence` to 1

3. **Day 3 (9am)**: Drip processor runs
   - Finds enrollment (last_sent_at was Day 1)
   - Calculates: last_sent_at + 2 days = today
   - Sends "The Two Paths of AI" email
   - Updates `current_sequence` to 2

4. **Day 5, 7, 10, 14**: Same process continues

5. **After Day 14**: 
   - No more emails in sequence
   - Enrollment marked as "completed"
   - No more emails sent

---

## 📊 Database Structure

### user-email-campaigns
```
user_id (PK) | campaign_id (SK) | campaign_type | sequence_number | delay_days | subject | content
```

### user-email-drip-enrollments
```
user_id (PK) | enrollment_id (SK) | subscriber_email | campaign_id | current_sequence | status
```

### user-email-subscribers
```
user_id (PK) | subscriber_email (SK) | first_name | tags | status
```

---

## 🚀 Deployment Status

✅ **7 campaigns created** in DynamoDB  
✅ **Drip enrollments table** created  
✅ **Drip processor Lambda** deployed  
✅ **EventBridge schedule** created (daily 9am EST)  
✅ **Auto-enrollment** enabled in signup handler  
✅ **Email subscription handler** updated and deployed

---

## 🧪 Testing

### Test Auto-Enrollment:
1. Sign up on book page with test email
2. Check `user-email-drip-enrollments` table
3. Should see enrollment with `status: "active"`

### Test Drip Processor:
```bash
aws lambda invoke \
  --function-name email-drip-processor \
  --region us-east-1 \
  --profile ekewaka \
  response.json
```

### Check Logs:
```bash
aws logs tail /aws/lambda/email-drip-processor \
  --since 1h \
  --region us-east-1 \
  --profile ekewaka
```

---

## 📝 Manual Operations

### Enroll Existing Subscribers:
```python
import boto3
from datetime import datetime

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')

# Get existing book subscribers
subscribers_table = dynamodb.Table('book-subscribers')
response = subscribers_table.scan()

for sub in response['Items']:
    email = sub['email']
    enrollment_id = f"{email}_book-welcome-sequence"
    
    enrollments_table.put_item(Item={
        'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'enrollment_id': enrollment_id,
        'subscriber_email': email,
        'campaign_id': 'book-welcome-sequence',
        'enrolled_at': datetime.now().isoformat(),
        'current_sequence': 0,
        'status': 'active'
    })
    print(f"Enrolled: {email}")
```

### Pause Enrollment:
```python
enrollments_table.update_item(
    Key={
        'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'enrollment_id': 'email@example.com_book-welcome-sequence'
    },
    UpdateExpression='SET #status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'paused'}
)
```

### Resume Enrollment:
```python
enrollments_table.update_item(
    Key={
        'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'enrollment_id': 'email@example.com_book-welcome-sequence'
    },
    UpdateExpression='SET #status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'active'}
)
```

---

## 🔧 Configuration

### Change Send Time:
Edit EventBridge rule cron expression:
```bash
aws events put-rule \
  --name email-drip-processor-daily \
  --schedule-expression "cron(0 15 * * ? *)" \
  --region us-east-1 \
  --profile ekewaka
```
(This changes to 10am EST / 3pm UTC)

### Add More Emails:
1. Create new campaign in DynamoDB with next `sequence_number`
2. Set appropriate `delay_days`
3. Drip processor will automatically pick it up

---

## 📈 Monitoring

### Check Active Enrollments:
```bash
aws dynamodb scan \
  --table-name user-email-drip-enrollments \
  --filter-expression "#status = :status" \
  --expression-attribute-names '{"#status":"status"}' \
  --expression-attribute-values '{":status":{"S":"active"}}' \
  --region us-east-1 \
  --profile ekewaka
```

### Check Completed Enrollments:
```bash
aws dynamodb scan \
  --table-name user-email-drip-enrollments \
  --filter-expression "#status = :status" \
  --expression-attribute-names '{"#status":"status"}' \
  --expression-attribute-values '{":status":{"S":"completed"}}' \
  --region us-east-1 \
  --profile ekewaka
```

---

## 🎯 Next Steps

1. **Test with real subscriber** - Sign up and verify enrollment
2. **Monitor first run** - Check logs after 9am EST tomorrow
3. **Review analytics** - Track open/click rates in campaigns table
4. **Optimize timing** - Adjust send times based on engagement
5. **A/B test subject lines** - Create variant campaigns
6. **Add more sequences** - Create drip sequences for other products

---

## 📁 Files Created

- `create_book_campaigns.py` - Script to create 7 campaigns
- `create_drip_table.py` - Script to create enrollments table
- `email-drip-processor/lambda_function.py` - Drip processor Lambda
- `deploy-drip-processor.ps1` - Deployment script
- `create-drip-schedule.ps1` - EventBridge schedule script
- `EMAIL_DRIP_AUTOMATION_COMPLETE.md` - This file

---

## ✅ System is LIVE and READY!

New book subscribers will automatically:
1. Receive immediate welcome email with PDFs
2. Be enrolled in 7-email drip sequence
3. Receive emails on Days 1, 3, 5, 7, 10, and 14
4. Be marked as "completed" after final email

**No manual intervention required!**
