# Email Marketing System - Deployment Checklist

## ☐ Pre-Deployment

- [ ] AWS CLI installed and configured
- [ ] PowerShell 7+ installed
- [ ] AWS account has access to Lambda, DynamoDB, SES
- [ ] Know your AWS Account ID
- [ ] Have domain name ready (e.g., christianconservativestoday.com)

---

## ☐ Phase 1: Initial Setup (30 minutes)

### Step 1: Update Configuration Files
- [ ] Edit `create-lambda-functions.ps1` → Replace `YOUR-ACCOUNT-ID` (line 35)
- [ ] Edit `email_subscribers_api/index.py` → Update domain name (lines 127, 177, 234)
- [ ] Edit `email_campaigns_api/index.py` → Update domain name if needed
- [ ] Edit `email_sender/index.py` → Update domain name (line 60)

### Step 2: Create Lambda Functions
```powershell
cd "Email Marketing"
.\create-lambda-functions.ps1
```
- [ ] email_subscribers_api created
- [ ] email_campaigns_api created
- [ ] email_sender created
- [ ] email_tracking_api created

### Step 3: Create DynamoDB Tables
```powershell
.\setup-database.ps1
```
- [ ] EmailSubscribers table created
- [ ] EmailCampaigns table created
- [ ] EmailAnalytics table created

### Step 4: Deploy Lambda Code
```powershell
.\deploy-all.ps1
```
- [ ] email_subscribers_api deployed
- [ ] email_campaigns_api deployed
- [ ] email_sender deployed
- [ ] email_tracking_api deployed

### Step 5: Configure IAM Permissions
- [ ] Lambda execution role has DynamoDB permissions
- [ ] Lambda execution role has SES permissions
- [ ] Lambda execution role has Lambda invoke permissions

### Step 6: Set Environment Variables
```bash
aws lambda update-function-configuration \
  --function-name email_subscribers_api \
  --environment Variables={SES_FROM_EMAIL=newsletter@yourdomain.com,SES_FROM_NAME="Your Name",DOMAIN=yourdomain.com}
```
- [ ] email_subscribers_api environment variables set
- [ ] email_campaigns_api environment variables set
- [ ] email_sender environment variables set
- [ ] email_tracking_api environment variables set

### Step 7: Verify Email in SES (for testing)
```bash
aws ses verify-email-identity --email-address your-email@example.com
```
- [ ] Email verification sent
- [ ] Email verified (check inbox and click link)

### Step 8: Test the System
```bash
# Test subscriber API
aws lambda invoke --function-name email_subscribers_api --payload '{"body":"{\"action\":\"list\"}"}' response.json
cat response.json
```
- [ ] Subscriber API works
- [ ] Campaign API works
- [ ] Can add test subscriber
- [ ] Can create test campaign

---

## ☐ Phase 2: Frontend Deployment (10 minutes)

### Step 1: Update HTML Files
- [ ] `admin-email-subscribers.html` → Update API_URL (line 127)
- [ ] `admin-email-campaigns.html` → Update API_URL (line 127, 128)
- [ ] `email-subscribe.html` → Update API_URL (line 82)
- [ ] `email-confirm.html` → Update API_URL (line 42)
- [ ] `email-unsubscribe.html` → Update API_URL (line 32)

### Step 2: Push to S3
```powershell
cd ..
.\s3-push.ps1
```
- [ ] HTML files uploaded to S3
- [ ] Files accessible via CloudFront

### Step 3: Test Frontend
- [ ] Open admin-email-subscribers.html in browser
- [ ] Can view subscribers
- [ ] Can add subscriber
- [ ] Open admin-email-campaigns.html in browser
- [ ] Can create campaign
- [ ] Can send test email
- [ ] Open email-subscribe.html in browser
- [ ] Can subscribe
- [ ] Receive confirmation email

---

## ☐ Phase 3: Production Setup (24-48 hours)

### Step 1: Request SES Production Access
- [ ] Go to AWS Console → Amazon SES
- [ ] Click "Request production access"
- [ ] Fill out form with use case
- [ ] Submit request
- [ ] Wait for approval (24-48 hours)

### Step 2: Domain Verification
```bash
aws ses verify-domain-identity --domain yourdomain.com
```
- [ ] Add TXT record to DNS
- [ ] Domain verified in SES

### Step 3: DKIM Setup
```bash
aws ses set-identity-dkim-enabled --identity yourdomain.com --dkim-enabled
aws ses get-identity-dkim-attributes --identities yourdomain.com
```
- [ ] Add 3 CNAME records to DNS
- [ ] DKIM verified

### Step 4: SPF Record
- [ ] Add SPF TXT record: `v=spf1 include:amazonses.com ~all`

### Step 5: Bounce/Complaint Handling
```bash
aws sns create-topic --name email-bounces-complaints
aws sns subscribe --topic-arn [ARN] --protocol email --notification-endpoint your-email@example.com
```
- [ ] SNS topic created
- [ ] Email subscribed to topic
- [ ] SES configured to publish to SNS

---

## ☐ Phase 4: API Gateway (Optional)

### Step 1: Create REST API
```bash
aws apigateway create-rest-api --name "EmailMarketingAPI"
```
- [ ] API created
- [ ] Note API ID

### Step 2: Create Resources
- [ ] /email-subscribers resource
- [ ] /email-campaigns resource
- [ ] /email-tracking resource

### Step 3: Create Methods
- [ ] POST method for each resource
- [ ] Lambda proxy integration configured
- [ ] CORS enabled

### Step 4: Deploy API
- [ ] Create deployment stage (e.g., "prod")
- [ ] Note API Gateway URL
- [ ] Update HTML files with new URL

---

## ☐ Testing Checklist

### Subscriber Management
- [ ] Can subscribe via form
- [ ] Receive confirmation email
- [ ] Can confirm subscription
- [ ] Receive welcome email
- [ ] Can view subscribers in admin
- [ ] Can filter by status
- [ ] Can export CSV
- [ ] Can import CSV
- [ ] Can unsubscribe

### Campaign Management
- [ ] Can create campaign
- [ ] Can save draft
- [ ] Can edit campaign
- [ ] Can send test email
- [ ] Receive test email
- [ ] Can send to all subscribers
- [ ] Emails delivered
- [ ] Tracking pixel works
- [ ] Click tracking works
- [ ] Unsubscribe link works

### Analytics
- [ ] Open events logged
- [ ] Click events logged
- [ ] Can view campaign stats
- [ ] Open rate calculated correctly
- [ ] Click rate calculated correctly

---

## ☐ Integration with Existing Platform

### Add Signup Forms
- [ ] Add to website footer
- [ ] Add to article pages
- [ ] Add to video pages
- [ ] Add to election map

### Content Notifications
- [ ] New article → Send notification
- [ ] New video → Add to digest
- [ ] Election update → Send alert

### User Account Integration
- [ ] Link subscribers to user accounts
- [ ] Sync subscription status
- [ ] Preference center

---

## ☐ Monitoring & Maintenance

### CloudWatch Alarms
- [ ] High bounce rate alarm (>5%)
- [ ] High complaint rate alarm (>0.1%)
- [ ] Lambda error alarm
- [ ] DynamoDB throttle alarm

### Regular Tasks
- [ ] Monitor bounce rate weekly
- [ ] Monitor complaint rate weekly
- [ ] Review unsubscribe reasons monthly
- [ ] Clean inactive subscribers quarterly
- [ ] Review campaign performance monthly

---

## ☐ Documentation

- [ ] Team trained on admin interface
- [ ] Email templates documented
- [ ] Merge tags documented
- [ ] Segmentation strategy documented
- [ ] Content calendar created

---

## 🎉 Launch Checklist

- [ ] All tests passing
- [ ] SES production access approved
- [ ] Domain verified
- [ ] DKIM configured
- [ ] Monitoring set up
- [ ] Team trained
- [ ] First campaign ready
- [ ] Backup plan in place

---

## 📞 Support Resources

- **AWS SES Documentation**: https://docs.aws.amazon.com/ses/
- **CloudWatch Logs**: `/aws/lambda/email_*`
- **DynamoDB Console**: Check tables for data
- **SES Console**: Monitor sending statistics

---

## 🚨 Troubleshooting

### Email not sending
- [ ] Check SES sandbox status
- [ ] Verify recipient email
- [ ] Check Lambda logs
- [ ] Verify IAM permissions

### High bounce rate
- [ ] Implement double opt-in
- [ ] Validate email addresses
- [ ] Remove bounced emails

### Emails in spam
- [ ] Verify DKIM configured
- [ ] Add SPF record
- [ ] Warm up sending gradually
- [ ] Monitor complaint rate

---

**Last Updated**: [Date]  
**Deployed By**: [Name]  
**Status**: [ ] Not Started | [ ] In Progress | [ ] Complete
