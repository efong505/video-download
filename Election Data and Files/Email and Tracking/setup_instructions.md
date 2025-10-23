# Complete Setup Instructions

Follow these steps in order to deploy the email subscription system with tracking.

## Prerequisites

- AWS Account with admin access
- Domain: christianconservativestoday.com
- Email: contact@christianconservativestoday.com (working)
- Basic familiarity with AWS Console

## Estimated Time: 30-45 minutes

---

## Step 1: Verify Email in AWS SES (5 minutes)

### 1.1 Go to SES Console
- Open: https://console.aws.amazon.com/ses/
- Make sure you're in **us-east-1** region (top right)

### 1.2 Verify Email Address
1. Click **Verified identities** in left menu
2. Click **Create identity** button
3. Select **Email address**
4. Enter: `contact@christianconservativestoday.com`
5. Click **Create identity**
6. Check your email inbox
7. Click the verification link from AWS

### 1.3 Verify Status
- Wait 1-2 minutes
- Refresh the page
- Status should show **Verified** ✓

---

## Step 2: Request Production Access (Submit now, approved in 24 hours)

### 2.1 Why This is Needed
By default, SES is in "sandbox mode" - you can only send to verified emails. Production access lets you send to anyone.

### 2.2 Request Access
1. In SES Console, click **Account dashboard** (left menu)
2. Look for "Sending statistics" section
3. Click **Request production access** button
4. Fill out the form:

**Mail type**: Transactional
**Website URL**: https://christianconservativestoday.com
**Use case description**:
```
We operate a Christian conservative election information website. We collect 
email subscriptions from visitors who want to receive:
- Election updates and voter guides
- Pro-life, pro-family candidate information
- Church mobilization resources

All subscribers explicitly opt-in via our website form. We include unsubscribe 
links in every email. Expected volume: 1,000 emails/month initially, growing 
to 10,000/month.
```

**How you handle bounces/complaints**:
```
We monitor SES bounce and complaint notifications. We automatically remove 
bounced emails from our list. We honor all unsubscribe requests immediately.
```

**Compliance**: Check the box confirming you comply with AWS policies

5. Click **Submit request**

### 2.3 Wait for Approval
- Usually approved within 24 hours
- You'll receive email notification
- Continue with other steps while waiting

---

## Step 3: Create DynamoDB Tables (5 minutes)

### 3.1 Create Subscribers Table
1. Go to DynamoDB Console: https://console.aws.amazon.com/dynamodb/
2. Click **Create table**
3. Settings:
   - **Table name**: `email-subscribers`
   - **Partition key**: `email` (String)
   - Leave other settings as default
4. Click **Create table**
5. Wait for status to show **Active** (30 seconds)

### 3.2 Create Events Table
1. Click **Create table** again
2. Settings:
   - **Table name**: `email-events`
   - **Partition key**: `event_id` (String)
   - **Sort key**: `timestamp` (Number)
   - Leave other settings as default
3. Click **Create table**
4. Wait for status to show **Active**

### 3.3 Verify Tables
- You should see both tables listed
- Both should show **Active** status

---

## Step 4: Create Lambda Function (10 minutes)

### 4.1 Create Function
1. Go to Lambda Console: https://console.aws.amazon.com/lambda/
2. Click **Create function**
3. Choose **Author from scratch**
4. Settings:
   - **Function name**: `email-subscription-handler`
   - **Runtime**: Python 3.12
   - **Architecture**: x86_64
   - Leave other settings as default
5. Click **Create function**

### 4.2 Add Function Code
1. In the function page, scroll to **Code source** section
2. Delete the default code in `lambda_function.py`
3. Open the file `lambda_function.py` from this folder
4. Copy ALL the code
5. Paste into Lambda editor
6. Click **Deploy** button (top right)
7. Wait for "Successfully deployed" message

### 4.3 Add Permissions
1. Click **Configuration** tab
2. Click **Permissions** in left menu
3. Click the **Role name** link (opens in new tab)
4. In IAM console, click **Add permissions** → **Attach policies**
5. Search for and select:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSESFullAccess`
6. Click **Add permissions**
7. Close the IAM tab

### 4.4 Increase Timeout
1. Back in Lambda, click **Configuration** tab
2. Click **General configuration**
3. Click **Edit**
4. Change **Timeout** to `30` seconds
5. Click **Save**

---

## Step 5: Create API Gateway (10 minutes)

### 5.1 Create HTTP API
1. Go to API Gateway Console: https://console.aws.amazon.com/apigateway/
2. Click **Create API**
3. Find **HTTP API** and click **Build**
4. Click **Add integration**
5. Select **Lambda**
6. Choose your region: **us-east-1**
7. Select your Lambda function: `email-subscription-handler`
8. **API name**: `email-subscription-api`
9. Click **Next**

### 5.2 Configure Routes
1. On "Configure routes" page, you'll see a default route
2. Click **Next** (we'll add more routes later)

### 5.3 Configure Stages
1. **Stage name**: `$default` (already filled)
2. **Auto-deploy**: Enabled (checked)
3. Click **Next**

### 5.4 Review and Create
1. Review settings
2. Click **Create**
3. Wait for creation to complete

### 5.5 Add Additional Routes
1. In your API, click **Routes** in left menu
2. Click **Create** button
3. Add these routes one by one:

**Route 1:**
- Method: `POST`
- Path: `/subscribe`
- Integration: Select your Lambda function
- Click **Create**

**Route 2:**
- Method: `GET`
- Path: `/track/open/{tracking_id}`
- Integration: Select your Lambda function
- Click **Create**

**Route 3:**
- Method: `GET`
- Path: `/track/click/{tracking_id}`
- Integration: Select your Lambda function
- Click **Create**

**Route 4:**
- Method: `OPTIONS`
- Path: `/{proxy+}`
- Integration: Select your Lambda function
- Click **Create**

### 5.6 Get Your API URL
1. Click **Stages** in left menu
2. Click **$default**
3. Copy the **Invoke URL** (looks like: `https://abc123xyz.execute-api.us-east-1.amazonaws.com`)
4. **SAVE THIS URL** - you'll need it for the frontend

---

## Step 6: Update Frontend Code (5 minutes)

### 6.1 Update election-map.html
1. Open `election-map.html` in your code editor
2. Find the `subscribeEmail()` function (around line 700)
3. Replace the entire function with code from `frontend_code.js`
4. Find this line:
   ```javascript
   const EMAIL_API_ENDPOINT = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com';
   ```
5. Replace `YOUR-API-ID` with your actual API Gateway URL from Step 5.6
6. Save the file

### 6.2 Upload to Server
1. Upload the updated `election-map.html` to your web server
2. Make sure it's accessible at: https://christianconservativestoday.com/election-map.html

---

## Step 7: Test the System (5 minutes)

### 7.1 Test Subscription
1. Visit: https://christianconservativestoday.com/election-map.html
2. Scroll to email subscription section
3. Enter your email address
4. Click **Subscribe**
5. You should see success message

### 7.2 Check Email
1. Check your email inbox (and spam folder)
2. You should receive welcome email within 1 minute
3. Email should have:
   - Subject: "🗳️ Welcome to Christian Conservatives Today!"
   - Professional formatting
   - "View Interactive Election Map" button

### 7.3 Test Open Tracking
1. Open the welcome email
2. Wait 5 seconds
3. Go to DynamoDB Console
4. Open `email-events` table
5. Click **Explore table items**
6. You should see an event with `event_type: opened`

### 7.4 Test Click Tracking
1. In the welcome email, click "View Interactive Election Map" button
2. You should be redirected to the election map
3. Go back to DynamoDB `email-events` table
4. Refresh the items
5. You should see a new event with `event_type: clicked`

### 7.5 Check Subscriber Record
1. Go to DynamoDB Console
2. Open `email-subscribers` table
3. Click **Explore table items**
4. Find your email
5. You should see:
   - `status: active`
   - `total_opens: 1` (or more)
   - `total_clicks: 1` (or more)

---

## Step 8: View Analytics (Optional)

### 8.1 Install AWS CLI (if not already installed)
```bash
pip install boto3
```

### 8.2 Configure AWS Credentials
```bash
aws configure
```
Enter your AWS Access Key ID and Secret Access Key

### 8.3 Run Analytics Script
```bash
cd "Election Data and Files/Email and Tracking"
python analytics_queries.py
```

You should see:
- Total subscribers
- Campaign performance
- Open/click rates
- Most engaged subscribers

---

## Troubleshooting

### Email Not Sending
**Problem**: Subscription works but no email received

**Solutions**:
1. Check spam folder
2. Verify SES email is verified (Step 1)
3. Check Lambda CloudWatch logs:
   - Go to Lambda function
   - Click **Monitor** tab
   - Click **View CloudWatch logs**
   - Look for errors
4. Verify SES is out of sandbox mode (Step 2)

### API Gateway Error
**Problem**: "Failed to subscribe" error on website

**Solutions**:
1. Check API Gateway URL is correct in frontend code
2. Verify Lambda function has DynamoDB permissions
3. Check browser console for errors (F12)
4. Test API directly:
   ```bash
   curl -X POST https://YOUR-API-URL/subscribe \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com"}'
   ```

### Tracking Not Working
**Problem**: Opens/clicks not recorded in DynamoDB

**Solutions**:
1. Verify API Gateway routes are configured (Step 5.5)
2. Check Lambda has permissions for DynamoDB
3. Test tracking URLs directly in browser
4. Check CloudWatch logs for errors

### SES Sandbox Mode
**Problem**: Can only send to verified emails

**Solution**:
- Wait for production access approval (Step 2)
- Usually takes < 24 hours
- Check email for approval notification

---

## Next Steps After Setup

1. ✅ Test with multiple email addresses
2. ✅ Send a test newsletter using `send_newsletter.py`
3. ✅ Monitor analytics daily for first week
4. ✅ Create email templates for different campaigns
5. ✅ Set up weekly/monthly newsletter schedule
6. ✅ Build custom analytics dashboard (optional)

---

## Cost Monitoring

### Expected Costs:
- **DynamoDB**: $0 (free tier)
- **Lambda**: $0 (free tier)
- **API Gateway**: $0 (free tier)
- **SES**: $0.10 per 1,000 emails

### Example:
- 1,000 subscribers
- 4 emails/month
- Total: 4,000 emails/month = **$0.40/month**

### Monitor Costs:
1. Go to AWS Billing Console
2. Check "Cost Explorer"
3. Filter by service (SES, Lambda, DynamoDB)

---

## Support

If you encounter issues:
1. Check CloudWatch logs in Lambda
2. Review this guide's troubleshooting section
3. Check AWS service health dashboard
4. Email: contact@christianconservativestoday.com

---

**Setup Complete!** 🎉

Your email subscription system with tracking is now live and ready to collect subscribers.
