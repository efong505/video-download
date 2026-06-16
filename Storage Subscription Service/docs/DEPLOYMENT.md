# Deployment Guide

Complete step-by-step guide to deploy CloudVault Storage Subscription Service.

## Prerequisites

### Required Software
1. **AWS CLI** - Install from https://aws.amazon.com/cli/
2. **Python 3.12** - Install from https://www.python.org/
3. **PowerShell 7+** - Install from https://github.com/PowerShell/PowerShell
4. **pip** - Python package manager (included with Python)

### AWS Account Setup
1. Create an AWS account at https://aws.amazon.com
2. Create an IAM user with administrator access
3. Configure AWS CLI:
   ```bash
   aws configure
   ```
   Enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region: us-east-1
   - Default output format: json

### Stripe Account Setup
1. Create account at https://stripe.com
2. Get API keys from Dashboard → Developers → API keys
3. Create products:
   - Go to Products → Add Product
   - Create three products: Basic, Pro, Business
   - Set recurring prices: $5, $15, $50
   - Note the Price IDs (e.g., price_1234...)

## Step 1: Create AWS Infrastructure

### Run Infrastructure Script

```powershell
cd "Storage Subscription Service\scripts"
.\create-infrastructure.ps1
```

This script will:
1. Create S3 bucket for file storage
2. Configure CORS on S3 bucket
3. Create DynamoDB tables (StorageUsers, StorageFiles)
4. Create IAM role for Lambda functions
5. Create and deploy Lambda functions
6. Create API Gateway with routes
7. Configure Lambda permissions

**Expected Output:**
```
Infrastructure Created Successfully!
========================================
S3 Bucket: storage-subscription-bucket-12345
API URL: https://abc123.execute-api.us-east-1.amazonaws.com/prod
```

**Save these values!** You'll need them for configuration.

### Verify Infrastructure

Check that resources were created:

```powershell
# Check S3 bucket
aws s3 ls | Select-String "storage-subscription"

# Check DynamoDB tables
aws dynamodb list-tables

# Check Lambda functions
aws lambda list-functions --query 'Functions[*].FunctionName'

# Check API Gateway
aws apigatewayv2 get-apis
```

## Step 2: Configure Stripe Integration

### Update Lambda Environment Variables

```powershell
# Set Stripe keys for subscription_api
aws lambda update-function-configuration `
    --function-name subscription_api `
    --environment Variables="{
        JWT_SECRET=your-secret-key-change-this,
        S3_BUCKET=your-bucket-name,
        STRIPE_SECRET_KEY=sk_test_YOUR_KEY,
        STRIPE_WEBHOOK_SECRET=whsec_YOUR_KEY
    }"
```

### Create Stripe Webhook

1. Go to Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Enter URL: `https://YOUR_API_URL/prod/subscription`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
5. Copy webhook signing secret
6. Update Lambda environment variable (see above)

### Update Stripe Price IDs

Edit `lambda/subscription_api/index.py`:

```python
TIER_CONFIG = {
    'basic': {'quota': 10737418240, 'price': 5, 'name': 'Basic', 'priceId': 'price_YOUR_BASIC_ID'},
    'pro': {'quota': 107374182400, 'price': 15, 'name': 'Pro', 'priceId': 'price_YOUR_PRO_ID'},
    'business': {'quota': 1099511627776, 'price': 50, 'name': 'Business', 'priceId': 'price_YOUR_BUSINESS_ID'}
}
```

Redeploy subscription_api:
```powershell
.\deploy-all.ps1
```

## Step 3: Configure Frontend

### Update config.js

Edit `frontend/config.js`:

```javascript
// Replace with your API Gateway URL from Step 1
const API_URL = 'https://abc123.execute-api.us-east-1.amazonaws.com/prod';

// Replace with your Stripe publishable key
const STRIPE_PUBLIC_KEY = 'pk_test_YOUR_KEY';

// Replace with your admin email
const ADMIN_EMAILS = ['admin@yourdomain.com'];
```

### Update Lambda Admin Email

```powershell
aws lambda update-function-configuration `
    --function-name admin_api `
    --environment Variables="{
        JWT_SECRET=your-secret-key-change-this,
        ADMIN_EMAILS=admin@yourdomain.com
    }"
```

## Step 4: Deploy Frontend

### Create Frontend Bucket

```powershell
.\deploy-frontend.ps1
```

When prompted, enter a unique bucket name (e.g., `cloudvault-frontend-12345`)

**Expected Output:**
```
Frontend Deployed Successfully!
========================================
Website URL: http://cloudvault-frontend-12345.s3-website-us-east-1.amazonaws.com
```

### Optional: Configure Custom Domain

#### Using CloudFront (Recommended)

1. Create CloudFront distribution:
   ```powershell
   aws cloudfront create-distribution `
       --origin-domain-name your-bucket.s3.amazonaws.com `
       --default-root-object index.html
   ```

2. Get distribution domain name
3. Create CNAME record in your DNS pointing to CloudFront

#### Using Route 53

1. Create hosted zone for your domain
2. Create A record pointing to S3 website endpoint
3. Update bucket name to match domain

## Step 5: Test the Application

### Test Authentication

1. Open website URL in browser
2. Click "Sign Up Free"
3. Create account with email and password
4. Verify redirect to dashboard

### Test File Upload

1. Go to "My Files"
2. Drag and drop a file or click to upload
3. Verify file appears in list
4. Test download and delete

### Test Subscription

1. Go to "Upgrade"
2. Click "Upgrade to Basic"
3. Complete Stripe checkout (use test card: 4242 4242 4242 4242)
4. Verify storage quota increased

### Test Admin Dashboard

1. Login with admin email
2. Go to `/admin.html`
3. Verify statistics display
4. Test user management

## Step 6: Production Checklist

### Security

- [ ] Change JWT_SECRET to strong random value
- [ ] Use Stripe live keys (not test keys)
- [ ] Enable CloudFront for HTTPS
- [ ] Configure WAF rules for API Gateway
- [ ] Enable CloudTrail for audit logging
- [ ] Set up AWS Backup for DynamoDB
- [ ] Implement rate limiting on API Gateway
- [ ] Add password strength requirements
- [ ] Upgrade password hashing to bcrypt

### Monitoring

- [ ] Set up CloudWatch alarms for errors
- [ ] Configure SNS notifications
- [ ] Enable X-Ray tracing on Lambda
- [ ] Set up CloudWatch dashboards
- [ ] Configure log retention policies

### Performance

- [ ] Enable Lambda reserved concurrency
- [ ] Configure DynamoDB auto-scaling
- [ ] Set up S3 lifecycle policies
- [ ] Enable CloudFront caching
- [ ] Optimize Lambda memory allocation

### Backup

- [ ] Enable DynamoDB point-in-time recovery
- [ ] Configure S3 versioning
- [ ] Set up cross-region replication
- [ ] Document disaster recovery plan

## Troubleshooting

### Lambda Function Errors

**Problem**: Lambda returns 500 error

**Solution**:
```powershell
# Check CloudWatch logs
aws logs tail /aws/lambda/auth_api --follow

# Test Lambda directly
aws lambda invoke --function-name auth_api --payload '{"body":"{}"}' response.json
```

### CORS Errors

**Problem**: Browser shows CORS error

**Solution**:
1. Verify API Gateway CORS configuration
2. Check Lambda response headers include CORS headers
3. Update S3 bucket CORS configuration

### Stripe Webhook Failures

**Problem**: Subscription not updating after payment

**Solution**:
1. Check Stripe webhook logs
2. Verify webhook secret in Lambda
3. Test webhook endpoint manually
4. Check CloudWatch logs for subscription_api

### File Upload Failures

**Problem**: Files not uploading

**Solution**:
1. Check file size (Lambda has 6MB payload limit)
2. Verify S3 bucket permissions
3. Check storage quota not exceeded
4. Review CloudWatch logs for storage_api

### Authentication Issues

**Problem**: Login fails or token invalid

**Solution**:
1. Verify JWT_SECRET matches across all Lambdas
2. Check token expiration (30 days default)
3. Clear browser localStorage
4. Verify DynamoDB table has user record

## Updating the Application

### Update Lambda Functions

```powershell
# Update all functions
.\deploy-all.ps1

# Update specific function
cd ..\lambda\auth_api
pip install -r requirements.txt -t .
Compress-Archive -Path * -DestinationPath function.zip -Force
aws lambda update-function-code --function-name auth_api --zip-file fileb://function.zip
```

### Update Frontend

```powershell
.\deploy-frontend.ps1
```

### Update Environment Variables

```powershell
aws lambda update-function-configuration `
    --function-name FUNCTION_NAME `
    --environment Variables="{KEY=VALUE}"
```

## Cost Optimization

### Monitor Costs

```powershell
# Get cost estimate
aws ce get-cost-and-usage `
    --time-period Start=2024-01-01,End=2024-01-31 `
    --granularity MONTHLY `
    --metrics BlendedCost
```

### Reduce Costs

1. **S3**: Enable Intelligent-Tiering
2. **Lambda**: Optimize memory and timeout
3. **DynamoDB**: Use on-demand billing for low traffic
4. **API Gateway**: Use HTTP API instead of REST API
5. **CloudWatch**: Set log retention to 7 days

## Scaling Considerations

### For 1,000+ Users

1. Enable DynamoDB auto-scaling
2. Use Lambda reserved concurrency
3. Implement API Gateway caching
4. Add CloudFront in front of API Gateway
5. Consider Aurora Serverless for relational data

### For 10,000+ Users

1. Implement multi-region deployment
2. Use DynamoDB Global Tables
3. Add ElastiCache for session management
4. Implement SQS for async processing
5. Use Step Functions for workflows

## Support

For deployment issues:
- Check CloudWatch Logs
- Review AWS documentation
- Contact AWS Support
- Open GitHub issue

## Next Steps

After successful deployment:
1. Customize branding and colors
2. Add custom domain
3. Configure email notifications
4. Implement analytics tracking
5. Add more features from roadmap
