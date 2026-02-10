# Quick Start Guide - Email Subscription System

## 🚀 Get Started in 30 Minutes

This system collects email subscriptions from your election map and tracks opens/clicks.

## What You Need

- ✅ AWS Account
- ✅ contact@christianconservativestoday.com (working)
- ✅ 30 minutes

## 5-Step Setup

### 1. Verify Email (5 min)
```
AWS SES Console → Verified identities → Create identity
→ Email address → contact@christianconservativestoday.com
→ Check email → Click verification link
```

### 2. Request Production Access (submit now, approved in 24h)
```
SES Console → Account dashboard → Request production access
→ Fill form (see setup_instructions.md for details)
→ Submit → Wait for approval email
```

### 3. Create DynamoDB Tables (5 min)
```
DynamoDB Console → Create table

Table 1:
  Name: email-subscribers
  Partition key: email (String)

Table 2:
  Name: email-events
  Partition key: event_id (String)
  Sort key: timestamp (Number)
```

### 4. Deploy Lambda Function (10 min)
```
Lambda Console → Create function
  Name: email-subscription-handler
  Runtime: Python 3.12
  
→ Paste code from lambda_function.py
→ Deploy
→ Configuration → Permissions → Add policies:
  - AmazonDynamoDBFullAccess
  - AmazonSESFullAccess
```

### 5. Create API Gateway (10 min)
```
API Gateway Console → Create API → HTTP API
  Name: email-subscription-api
  Integration: Lambda (select your function)
  
→ Add routes:
  POST /subscribe
  GET /track/open/{tracking_id}
  GET /track/click/{tracking_id}
  OPTIONS /{proxy+}
  
→ Copy Invoke URL
```

### 6. Update Frontend
```
1. Open election-map.html
2. Replace subscribeEmail() function with code from frontend_code.js
3. Update API_ENDPOINT with your API Gateway URL
4. Upload to server
```

## Test It

1. Visit your election map
2. Subscribe with your email
3. Check inbox for welcome email
4. Click link in email
5. Check DynamoDB for tracking data

## View Analytics

```bash
python analytics_queries.py
```

## Send Newsletter

```bash
python send_newsletter.py --subject "Election Update" --campaign "jan-2025" --test
```

## Files You Need

- **lambda_function.py** - Copy to Lambda
- **frontend_code.js** - Copy to election-map.html
- **analytics_queries.py** - Run to view stats
- **send_newsletter.py** - Run to send emails
- **setup_instructions.md** - Detailed guide

## Cost

- 10,000 emails/month = **$1.00**
- Everything else = **$0** (free tier)

## Help

See **setup_instructions.md** for detailed steps and troubleshooting.

---

**Ready? Start with Step 1!** ⬆️
