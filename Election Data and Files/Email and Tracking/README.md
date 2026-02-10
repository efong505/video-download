# Email Subscription & Tracking System

Complete AWS SES implementation with open/click tracking for the Christian Conservatives Today Election Map.

## 📋 What This System Does

1. **Collects email subscriptions** from election-map.html
2. **Stores subscribers** in DynamoDB
3. **Sends welcome emails** via AWS SES using contact@christianconservativestoday.com
4. **Tracks email opens** using invisible 1x1 pixel
5. **Tracks link clicks** using redirect URLs
6. **Provides analytics** on engagement (open rate, click rate)

## 🏗️ Architecture

```
User subscribes on website
    ↓
API Gateway → Lambda Function
    ↓
DynamoDB (stores email)
    ↓
AWS SES (sends confirmation email with tracking)
    ↓
User opens email → Tracking pixel loads → Lambda logs "open"
User clicks link → Tracking URL redirects → Lambda logs "click"
```

## 📁 Files in This Folder

1. **README.md** (this file) - Complete setup guide
2. **lambda_function.py** - Main Lambda function code
3. **analytics_queries.py** - Scripts to view email statistics
4. **send_newsletter.py** - Script to send emails to all subscribers
5. **setup_instructions.md** - Step-by-step AWS setup
6. **frontend_code.js** - JavaScript for election-map.html

## 🚀 Quick Start (30 Minutes)

### Step 1: Verify Email Domain (5 min)
1. Go to AWS SES Console: https://console.aws.amazon.com/ses/
2. Click **Verified identities** → **Create identity**
3. Choose **Email address**
4. Enter: `contact@christianconservativestoday.com`
5. Click verification link in email

### Step 2: Request Production Access (24 hours)
1. In SES Console → **Account dashboard**
2. Click **Request production access**
3. Fill form:
   - Use case: Transactional emails
   - Website: https://christianconservativestoday.com
   - Volume: 1,000/month initially
4. Wait for approval (usually < 24 hours)

### Step 3: Create DynamoDB Tables (5 min)

**Table 1: email-subscribers**
```bash
Table name: email-subscribers
Partition key: email (String)
Settings: Default
```

**Table 2: email-events**
```bash
Table name: email-events
Partition key: event_id (String)
Sort key: timestamp (Number)
Settings: Default
```

### Step 4: Create Lambda Function (10 min)
1. Go to AWS Lambda Console
2. Click **Create function**
3. Name: `email-subscription-handler`
4. Runtime: **Python 3.12**
5. Click **Create function**
6. Copy code from `lambda_function.py` and paste
7. Click **Deploy**
8. Go to **Configuration** → **Permissions** → Click role name
9. Add policies:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSESFullAccess`

### Step 5: Create API Gateway (5 min)
1. Go to API Gateway Console
2. Click **Create API** → **HTTP API**
3. Add integration → **Lambda** → Select your function
4. API name: `email-subscription-api`
5. Click **Next** → **Next** → **Create**
6. Copy the **Invoke URL** (e.g., `https://abc123.execute-api.us-east-1.amazonaws.com`)

### Step 6: Update election-map.html (5 min)
1. Open `election-map.html`
2. Find the `subscribeEmail()` function
3. Replace with code from `frontend_code.js`
4. Update `API_ENDPOINT` with your API Gateway URL
5. Upload to your server

### Step 7: Test (5 min)
1. Visit election-map.html
2. Enter your email and subscribe
3. Check email inbox for welcome message
4. Click link in email
5. Check DynamoDB tables for data

## 📊 Viewing Analytics

Run `analytics_queries.py` to see:
- Total subscribers
- Open rates
- Click rates
- Most engaged subscribers
- Campaign performance

```bash
python analytics_queries.py
```

## 📧 Sending Newsletters

Use `send_newsletter.py` to send emails to all subscribers:

```python
python send_newsletter.py --subject "Election Update" --campaign "jan-2025-update"
```

## 💰 Cost Breakdown

- **DynamoDB**: ~$0 (free tier covers this)
- **Lambda**: ~$0 (free tier covers 1M requests/month)
- **SES**: $0.10 per 1,000 emails
- **API Gateway**: ~$0 (free tier covers 1M requests/month)

**Example**: 10,000 emails/month = **$1.00/month**

## 📈 What Gets Tracked

### Per Email Campaign:
- Total sent
- Total opens (including repeat opens)
- Unique opens (distinct subscribers)
- Total clicks
- Unique clicks
- Open rate %
- Click rate %

### Per Subscriber:
- Total emails received
- Total opens
- Total clicks
- Last activity date
- Engagement score

## 🔒 Privacy & Compliance

- ✅ Unsubscribe link in every email
- ✅ CAN-SPAM compliant
- ✅ GDPR ready (stores minimal data)
- ✅ Secure tracking (base64 encoded IDs)

## 🛠️ Troubleshooting

### Email not sending?
- Check SES is out of sandbox mode
- Verify email address in SES
- Check Lambda CloudWatch logs

### Tracking not working?
- Verify API Gateway routes are configured
- Check Lambda has DynamoDB permissions
- Test tracking URLs manually

### High bounce rate?
- Use double opt-in
- Clean email list regularly
- Monitor SES reputation dashboard

## 📚 Additional Resources

- **AWS SES Documentation**: https://docs.aws.amazon.com/ses/
- **DynamoDB Guide**: https://docs.aws.amazon.com/dynamodb/
- **Lambda Tutorial**: https://docs.aws.amazon.com/lambda/

## 🆘 Support

For issues or questions:
- Check `setup_instructions.md` for detailed steps
- Review Lambda CloudWatch logs
- Email: contact@christianconservativestoday.com

## 🎯 Next Steps After Setup

1. ✅ Test with your own email
2. ✅ Send test newsletter
3. ✅ Monitor analytics for 1 week
4. ✅ Create email templates for different campaigns
5. ✅ Set up automated welcome series
6. ✅ Build analytics dashboard (optional)

---

**Last Updated**: January 2025
**Version**: 1.0
**Status**: Production Ready
