# Email Marketing System - Complete Setup Guide

## Prerequisites
- AWS CLI configured with credentials
- PowerShell 7+
- Python 3.12
- Access to domain DNS records

## Phase 1: Foundation Setup (4-5 hours)

### Step 1: AWS SES Setup (30 minutes)

#### 1.1 Verify Domain
```bash
# Replace with your domain
aws ses verify-domain-identity --domain christianconservativestoday.com
```

**Output**: You'll receive verification token. Add this TXT record to your DNS:
- Name: `_amazonses.christianconservativestoday.com`
- Type: `TXT`
- Value: `[verification-token-from-output]`

#### 1.2 Verify Email Address (for testing)
```bash
# Verify your email for testing
aws ses verify-email-identity --email-address your-email@example.com
```
Check your email and click verification link.

#### 1.3 Check Verification Status
```bash
# Check domain verification
aws ses get-identity-verification-attributes --identities christianconservativestoday.com

# Check email verification
aws ses get-identity-verification-attributes --identities your-email@example.com
```

#### 1.4 Request Production Access
1. Go to AWS Console → Amazon SES → Account Dashboard
2. Click "Request production access"
3. Fill out form:
   - **Mail Type**: Transactional
   - **Website URL**: https://christianconservativestoday.com
   - **Use Case**: Newsletter and content notifications for Christian ministry platform
   - **Bounce/Complaint Handling**: We will monitor bounce and complaint rates
   - **Compliance**: We follow CAN-SPAM Act with unsubscribe links
4. Submit (approval takes 24-48 hours)

#### 1.5 Configure DKIM (Email Authentication)
```bash
# Enable DKIM signing
aws ses set-identity-dkim-enabled --identity christianconservativestoday.com --dkim-enabled

# Get DKIM tokens
aws ses get-identity-dkim-attributes --identities christianconservativestoday.com
```

Add 3 CNAME records to DNS (from output):
- Name: `[token1]._domainkey.christianconservativestoday.com`
- Type: `CNAME`
- Value: `[token1].dkim.amazonses.com`

Repeat for token2 and token3.

#### 1.6 Set Up SNS for Bounce/Complaint Notifications
```bash
# Create SNS topic
aws sns create-topic --name email-bounces-complaints

# Subscribe your email to topic
aws sns subscribe --topic-arn arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:email-bounces-complaints --protocol email --notification-endpoint your-email@example.com

# Configure SES to publish to SNS
aws ses set-identity-notification-topic --identity christianconservativestoday.com --notification-type Bounce --sns-topic arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:email-bounces-complaints

aws ses set-identity-notification-topic --identity christianconservativestoday.com --notification-type Complaint --sns-topic arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:email-bounces-complaints
```

---

### Step 2: Create DynamoDB Tables (15 minutes)

Run the database setup script:
```powershell
.\Email Marketing\setup-database.ps1
```

Or manually create tables:

#### 2.1 Subscribers Table
```bash
aws dynamodb create-table \
  --table-name EmailSubscribers \
  --attribute-definitions \
    AttributeName=email,AttributeType=S \
    AttributeName=status,AttributeType=S \
  --key-schema \
    AttributeName=email,KeyType=HASH \
  --global-secondary-indexes \
    IndexName=StatusIndex,KeySchema=[{AttributeName=status,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5} \
  --billing-mode PAY_PER_REQUEST
```

#### 2.2 Campaigns Table
```bash
aws dynamodb create-table \
  --table-name EmailCampaigns \
  --attribute-definitions \
    AttributeName=campaign_id,AttributeType=S \
    AttributeName=status,AttributeType=S \
  --key-schema \
    AttributeName=campaign_id,KeyType=HASH \
  --global-secondary-indexes \
    IndexName=StatusIndex,KeySchema=[{AttributeName=status,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5} \
  --billing-mode PAY_PER_REQUEST
```

#### 2.3 Analytics Table
```bash
aws dynamodb create-table \
  --table-name EmailAnalytics \
  --attribute-definitions \
    AttributeName=event_id,AttributeType=S \
    AttributeName=campaign_id,AttributeType=S \
  --key-schema \
    AttributeName=event_id,KeyType=HASH \
  --global-secondary-indexes \
    IndexName=CampaignIndex,KeySchema=[{AttributeName=campaign_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5} \
  --billing-mode PAY_PER_REQUEST
```

#### 2.4 Verify Tables Created
```bash
aws dynamodb list-tables
```

---

### Step 3: Deploy Lambda Functions (1-2 hours)

#### 3.1 Deploy Subscriber API
```powershell
cd "Email Marketing\email_subscribers_api"
.\deploy.ps1
```

#### 3.2 Deploy Campaigns API
```powershell
cd "..\email_campaigns_api"
.\deploy.ps1
```

#### 3.3 Deploy Tracking API
```powershell
cd "..\email_tracking_api"
.\deploy.ps1
```

#### 3.4 Deploy Email Sender
```powershell
cd "..\email_sender"
.\deploy.ps1
```

#### 3.5 Deploy Automation API
```powershell
cd "..\email_automation_api"
.\deploy.ps1
```

#### 3.6 Deploy All at Once
```powershell
cd "Email Marketing"
.\deploy-all.ps1
```

#### 3.7 Verify Deployments
```bash
aws lambda list-functions --query "Functions[?starts_with(FunctionName, 'email_')].FunctionName"
```

---

### Step 4: Create API Gateway Endpoints (30 minutes)

#### 4.1 Create REST API
```bash
aws apigateway create-rest-api --name "EmailMarketingAPI" --description "Email marketing system API"
```

Note the `api-id` from output.

#### 4.2 Get Root Resource ID
```bash
aws apigateway get-resources --rest-api-id YOUR-API-ID
```

#### 4.3 Create Resources and Methods
Run the API setup script:
```powershell
.\Email Marketing\setup-api-gateway.ps1 -ApiId YOUR-API-ID
```

Or follow manual steps in `API_GATEWAY_SETUP.md`

---

### Step 5: Deploy Frontend (30 minutes)

#### 5.1 Update API Endpoints
Edit these files and replace `YOUR-API-GATEWAY-URL`:
- `admin-email-subscribers.html`
- `admin-email-campaigns.html`
- `email-subscribe.html`

#### 5.2 Push to S3
```powershell
.\s3-push.ps1
```

Or manually:
```bash
aws s3 cp "Email Marketing/admin-email-subscribers.html" s3://techcross-videos/
aws s3 cp "Email Marketing/admin-email-campaigns.html" s3://techcross-videos/
aws s3 cp "Email Marketing/email-subscribe.html" s3://techcross-videos/
```

---

### Step 6: Test End-to-End (30 minutes)

#### 6.1 Test Subscription
1. Open `https://yourdomain.com/email-subscribe.html`
2. Enter email address
3. Check email for confirmation link
4. Click confirmation link
5. Verify subscriber in DynamoDB

#### 6.2 Test Campaign Creation
1. Open `https://yourdomain.com/admin-email-campaigns.html`
2. Create test campaign
3. Send to yourself
4. Check email received

#### 6.3 Test Tracking
1. Open email from test campaign
2. Click link in email
3. Check EmailAnalytics table for open/click events

#### 6.4 Test Unsubscribe
1. Click unsubscribe link in email
2. Verify status changed to "unsubscribed" in DynamoDB

---

## Phase 2: Campaign Builder (Weeks 3-4)

### Features to Implement
- [ ] Visual email editor (Quill.js integration)
- [ ] Email templates library
- [ ] Merge tag support ({{first_name}}, etc.)
- [ ] Preview functionality (desktop/mobile)
- [ ] Test email sending
- [ ] Campaign scheduling

### Files to Create
- `admin-email-templates.html` - Template management
- `email-template-editor.html` - Visual template builder
- `email_templates_api/index.py` - Template CRUD operations

---

## Phase 3: Sending & Tracking (Weeks 5-6)

### Features to Implement
- [ ] Batch email sending (throttled)
- [ ] Open tracking (1x1 pixel)
- [ ] Click tracking (redirect URLs)
- [ ] Analytics dashboard
- [ ] Bounce/complaint handling
- [ ] Unsubscribe management

### Files to Create
- `admin-email-analytics.html` - Analytics dashboard
- `email-tracking-pixel.html` - Tracking pixel endpoint
- `email-link-redirect.html` - Click tracking redirect

---

## Phase 4: Automation (Weeks 7-8)

### Features to Implement
- [ ] Welcome email automation
- [ ] Drip campaign builder
- [ ] Trigger system (EventBridge)
- [ ] Workflow editor
- [ ] Automation analytics

### Files to Create
- `admin-email-automations.html` - Automation builder
- `email-workflow-editor.html` - Visual workflow builder

---

## Phase 5: Advanced Features (Weeks 9-10)

### Features to Implement
- [ ] A/B testing
- [ ] Segmentation builder
- [ ] CSV import/export
- [ ] Re-engagement campaigns
- [ ] Advanced analytics

---

## Configuration

### Environment Variables
Add to each Lambda function:
```
SES_FROM_EMAIL=newsletter@christianconservativestoday.com
SES_FROM_NAME=Christian Conservatives Today
SES_REPLY_TO=contact@christianconservativestoday.com
DOMAIN=christianconservativestoday.com
TRACKING_DOMAIN=track.christianconservativestoday.com
```

### IAM Permissions
Each Lambda needs:
- DynamoDB: Read/Write to EmailSubscribers, EmailCampaigns, EmailAnalytics
- SES: SendEmail, SendRawEmail
- SNS: Publish (for notifications)

---

## Monitoring

### CloudWatch Alarms
```bash
# High bounce rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name email-high-bounce-rate \
  --alarm-description "Alert when bounce rate exceeds 5%" \
  --metric-name BounceRate \
  --namespace EmailMarketing \
  --statistic Average \
  --period 3600 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold

# High complaint rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name email-high-complaint-rate \
  --alarm-description "Alert when complaint rate exceeds 0.1%" \
  --metric-name ComplaintRate \
  --namespace EmailMarketing \
  --statistic Average \
  --period 3600 \
  --threshold 0.1 \
  --comparison-operator GreaterThanThreshold
```

### View Logs
```powershell
# Real-time logs for subscriber API
.\live-logs.ps1 -FunctionName email_subscribers_api

# Real-time logs for sender
.\live-logs.ps1 -FunctionName email_sender
```

---

## Troubleshooting

### SES Still in Sandbox
**Problem**: Can only send to verified emails
**Solution**: Request production access (Step 1.4), wait 24-48 hours

### Emails Going to Spam
**Problem**: Emails landing in spam folder
**Solution**: 
1. Verify DKIM configured (Step 1.5)
2. Add SPF record: `v=spf1 include:amazonses.com ~all`
3. Warm up sending (start with small volumes)

### High Bounce Rate
**Problem**: Bounce rate above 5%
**Solution**:
1. Implement double opt-in
2. Remove bounced emails from list
3. Validate email addresses before adding

### Lambda Timeout
**Problem**: email_sender timing out
**Solution**: Increase timeout to 5 minutes, reduce batch size

---

## Cost Estimates

### Monthly Costs (1,000 subscribers, 4 emails/month)
- **SES**: $0.40 (4,000 emails × $0.10/1000)
- **Lambda**: $0.05 (minimal invocations)
- **DynamoDB**: $0.10 (on-demand pricing)
- **API Gateway**: $0.05 (minimal requests)
- **Total**: ~$0.60/month

### Monthly Costs (10,000 subscribers, 4 emails/month)
- **SES**: $4.00 (40,000 emails × $0.10/1000)
- **Lambda**: $0.20
- **DynamoDB**: $0.50
- **API Gateway**: $0.10
- **Total**: ~$4.80/month

---

## Next Steps After Phase 1

1. **Collect Subscribers**: Add signup forms to all pages
2. **Create First Campaign**: Send welcome email to existing users
3. **Monitor Metrics**: Track open rates, click rates, bounces
4. **Build Templates**: Create reusable email templates
5. **Set Up Automations**: Welcome series, content notifications
6. **Integrate with Content**: Auto-send when new article published

---

## Support Resources

### AWS Documentation
- [SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [SES Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)

### Email Marketing Best Practices
- Keep subject lines under 50 characters
- Use preview text effectively
- Mobile-first design
- Clear call-to-action
- Test before sending

### Legal Compliance
- **CAN-SPAM Act**: Include physical address, unsubscribe link
- **GDPR**: Get explicit consent for EU subscribers
- **CCPA**: Allow California residents to opt-out
