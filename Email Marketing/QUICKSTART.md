# Email Marketing System - Quick Start Guide

## 🚀 Get Started in 30 Minutes

### Step 1: Create Lambda Functions (5 minutes)

```powershell
cd "Email Marketing"

# Edit create-lambda-functions.ps1 and replace YOUR-ACCOUNT-ID with your AWS account ID
# Then run:
.\create-lambda-functions.ps1
```

This creates 4 Lambda functions:
- `email_subscribers_api` - Manage subscribers
- `email_campaigns_api` - Manage campaigns
- `email_sender` - Send emails
- `email_tracking_api` - Track opens/clicks

---

### Step 2: Create DynamoDB Tables (2 minutes)

```powershell
.\setup-database.ps1
```

This creates 3 tables:
- `EmailSubscribers` - Subscriber data
- `EmailCampaigns` - Campaign data
- `EmailAnalytics` - Tracking events

---

### Step 3: Deploy Lambda Code (3 minutes)

```powershell
.\deploy-all.ps1
```

This deploys all Lambda function code.

---

### Step 4: Set Up AWS SES (10 minutes)

#### Verify Your Email (for testing)
```bash
aws ses verify-email-identity --email-address your-email@example.com
```

Check your email and click the verification link.

#### Test Email Sending
```bash
aws ses send-email \
  --from your-email@example.com \
  --destination ToAddresses=your-email@example.com \
  --message Subject={Data="Test"},Body={Text={Data="Test email"}}
```

If this works, you're ready to test!

#### Request Production Access (for real use)
1. Go to AWS Console → Amazon SES
2. Click "Request production access"
3. Fill out the form (approval takes 24-48 hours)

---

### Step 5: Test the System (10 minutes)

#### Test 1: Add a Subscriber
```bash
aws lambda invoke \
  --function-name email_subscribers_api \
  --payload '{"body":"{\"action\":\"subscribe\",\"email\":\"test@example.com\",\"first_name\":\"Test\"}"}' \
  response.json

cat response.json
```

#### Test 2: List Subscribers
```bash
aws lambda invoke \
  --function-name email_subscribers_api \
  --payload '{"body":"{\"action\":\"list\",\"status\":\"active\"}"}' \
  response.json

cat response.json
```

#### Test 3: Create a Campaign
```bash
aws lambda invoke \
  --function-name email_campaigns_api \
  --payload '{"body":"{\"action\":\"create\",\"title\":\"Test Campaign\",\"subject\":\"Hello!\",\"content_html\":\"<p>This is a test</p>\"}"}' \
  response.json

cat response.json
```

---

## 🎯 What's Next?

### Option A: Use Without API Gateway (Direct Lambda Invocation)
You can use the system right now by invoking Lambda functions directly from your frontend using AWS SDK.

**Example:**
```javascript
const lambda = new AWS.Lambda();
const params = {
    FunctionName: 'email_subscribers_api',
    Payload: JSON.stringify({
        body: JSON.stringify({
            action: 'subscribe',
            email: 'user@example.com'
        })
    })
};
lambda.invoke(params, (err, data) => {
    console.log(data);
});
```

### Option B: Set Up API Gateway (Recommended for Production)
Follow SETUP.md Step 4 to create REST API endpoints.

---

## 📝 Update Frontend Files

Replace `YOUR-API-GATEWAY-URL` in these files:
- `admin-email-subscribers.html`
- `admin-email-campaigns.html`
- `email-subscribe.html`
- `email-confirm.html`
- `email-unsubscribe.html`

If using direct Lambda invocation, modify the JavaScript to use AWS SDK instead of fetch().

---

## 🔧 Configuration

### Add Environment Variables to Lambda Functions

```bash
# For all functions
aws lambda update-function-configuration \
  --function-name email_subscribers_api \
  --environment Variables={SES_FROM_EMAIL=newsletter@yourdomain.com,SES_FROM_NAME="Your Name",DOMAIN=yourdomain.com}

# Repeat for other functions
```

---

## 📊 Monitor Your System

### View Logs
```powershell
# Real-time logs
aws logs tail /aws/lambda/email_subscribers_api --follow

# Or use your existing script
..\live-logs.ps1 -FunctionName email_subscribers_api
```

### Check DynamoDB Tables
```bash
# List subscribers
aws dynamodb scan --table-name EmailSubscribers --max-items 10

# List campaigns
aws dynamodb scan --table-name EmailCampaigns --max-items 10
```

---

## 🎉 You're Ready!

Your email marketing system is now functional. You can:

✅ Add subscribers (manually or via API)  
✅ Create email campaigns  
✅ Send emails (to verified addresses while in SES sandbox)  
✅ Track opens and clicks  

### Next Steps:
1. **Request SES production access** to send to any email
2. **Set up API Gateway** for cleaner API endpoints
3. **Add signup forms** to your website
4. **Create email templates** for consistent branding
5. **Set up automations** (welcome emails, drip campaigns)

---

## 🆘 Troubleshooting

### "Email not verified" error
- You're still in SES sandbox mode
- Only verified emails can receive emails
- Request production access or verify recipient emails

### Lambda timeout
- Increase timeout: `aws lambda update-function-configuration --function-name email_sender --timeout 300`

### Can't find tables
- Run `aws dynamodb list-tables` to verify tables exist
- Check region: `aws configure get region`

### Permission errors
- Lambda needs IAM permissions for DynamoDB and SES
- Check Lambda execution role has correct policies

---

## 💰 Cost Estimate

**For 1,000 subscribers, 4 emails/month:**
- SES: $0.40/month
- Lambda: $0.05/month
- DynamoDB: $0.10/month
- **Total: ~$0.55/month**

Compare to Mailchimp: $13-20/month for 500 subscribers

---

## 📚 Full Documentation

- **SETUP.md** - Complete setup guide with all phases
- **README.md** - System overview and features
- **Lambda function code** - In each function folder

---

## 🤝 Support

If you run into issues:
1. Check CloudWatch logs for errors
2. Verify IAM permissions
3. Confirm SES is configured
4. Test with AWS CLI first before using frontend
