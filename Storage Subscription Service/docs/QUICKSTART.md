# Quick Start Guide

Get CloudVault up and running in 15 minutes.

## Prerequisites

- AWS Account
- AWS CLI configured
- Python 3.12
- PowerShell 7+

## Step 1: Clone/Download Project

Download the "Storage Subscription Service" folder to your local machine.

## Step 2: Deploy Infrastructure (5 minutes)

Open PowerShell and navigate to the scripts folder:

```powershell
cd "Storage Subscription Service\scripts"
.\create-infrastructure.ps1
```

**Save the output!** You'll need:
- S3 Bucket name
- API Gateway URL

Example output:
```
S3 Bucket: storage-subscription-bucket-12345
API URL: https://abc123.execute-api.us-east-1.amazonaws.com/prod
```

## Step 3: Configure Stripe (5 minutes)

### Create Stripe Account
1. Go to https://stripe.com and sign up
2. Complete account setup

### Get API Keys
1. Go to Developers → API keys
2. Copy "Publishable key" (starts with `pk_test_`)
3. Copy "Secret key" (starts with `sk_test_`)

### Create Products
1. Go to Products → Add Product
2. Create three products:
   - **Basic**: $5/month recurring
   - **Pro**: $15/month recurring  
   - **Business**: $50/month recurring
3. Copy each Price ID (starts with `price_`)

### Update Lambda
```powershell
aws lambda update-function-configuration `
    --function-name subscription_api `
    --environment Variables="{
        JWT_SECRET=my-super-secret-key-12345,
        S3_BUCKET=storage-subscription-bucket-12345,
        STRIPE_SECRET_KEY=sk_test_YOUR_KEY
    }"
```

### Update subscription_api code
Edit `lambda/subscription_api/index.py` line 15-19:
```python
TIER_CONFIG = {
    'basic': {'priceId': 'price_YOUR_BASIC_ID'},
    'pro': {'priceId': 'price_YOUR_PRO_ID'},
    'business': {'priceId': 'price_YOUR_BUSINESS_ID'}
}
```

Redeploy:
```powershell
.\deploy-all.ps1
```

## Step 4: Configure Frontend (2 minutes)

Edit `frontend/config.js`:

```javascript
const API_URL = 'https://abc123.execute-api.us-east-1.amazonaws.com/prod';
const STRIPE_PUBLIC_KEY = 'pk_test_YOUR_KEY';
const ADMIN_EMAILS = ['your-email@example.com'];
```

## Step 5: Deploy Frontend (3 minutes)

```powershell
.\deploy-frontend.ps1
```

Enter a unique bucket name when prompted (e.g., `cloudvault-frontend-12345`)

**Save the website URL!**

Example: `http://cloudvault-frontend-12345.s3-website-us-east-1.amazonaws.com`

## Step 6: Test Application

### Test User Flow
1. Open website URL in browser
2. Click "Sign Up Free"
3. Create account with your email
4. Upload a test file
5. Download the file
6. Delete the file

### Test Subscription
1. Go to "Upgrade"
2. Click "Upgrade to Basic"
3. Use test card: `4242 4242 4242 4242`
4. Complete checkout
5. Verify storage increased to 10GB

### Test Admin Dashboard
1. Login with admin email
2. Go to `/admin.html`
3. View statistics
4. See user list

## Troubleshooting

### "Access Denied" Error
```powershell
# Check AWS credentials
aws sts get-caller-identity
```

### "Function Not Found" Error
```powershell
# List Lambda functions
aws lambda list-functions --query 'Functions[*].FunctionName'
```

### CORS Error in Browser
- Wait 1-2 minutes for API Gateway to propagate
- Clear browser cache
- Check config.js has correct API URL

### Stripe Checkout Not Working
- Verify Stripe public key in config.js
- Check Stripe secret key in Lambda
- Verify Price IDs are correct

## Next Steps

### Customize Branding
1. Edit `frontend/styles.css` for colors
2. Replace logo in navigation
3. Update company name throughout

### Add Custom Domain
1. Register domain in Route 53
2. Create CloudFront distribution
3. Add SSL certificate
4. Update DNS records

### Enable Monitoring
```powershell
# View Lambda logs
aws logs tail /aws/lambda/auth_api --follow

# View API Gateway logs
aws logs tail /aws/apigateway/storage-subscription-api --follow
```

### Production Checklist
- [ ] Change JWT_SECRET to random value
- [ ] Switch to Stripe live keys
- [ ] Add custom domain with HTTPS
- [ ] Enable CloudWatch alarms
- [ ] Set up backup strategy
- [ ] Configure rate limiting
- [ ] Add email notifications

## Cost Estimate

### Development/Testing
- **Free Tier**: $0/month (first 12 months)
- **After Free Tier**: ~$2-5/month

### Production (100 users)
- Lambda: ~$5/month
- DynamoDB: ~$5/month
- S3: ~$10/month
- API Gateway: ~$5/month
- **Total**: ~$25/month

Revenue from 100 users:
- 70 free, 20 basic, 8 pro, 2 business
- Revenue: (20 × $5) + (8 × $15) + (2 × $50) = $320/month
- **Profit**: ~$295/month

## Support

### Documentation
- [README.md](README.md) - Full documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment
- [API.md](API.md) - API reference

### Common Issues
- Check CloudWatch Logs for errors
- Verify environment variables
- Test API with test-api.ps1
- Review AWS service quotas

### Get Help
- AWS Documentation: https://docs.aws.amazon.com
- Stripe Documentation: https://stripe.com/docs
- GitHub Issues: [Your Repo]

## Success!

You now have a fully functional cloud storage subscription service!

**What you built:**
- Serverless backend with 4 Lambda functions
- Professional frontend with 8 pages
- Stripe payment integration
- Admin dashboard with analytics
- Scalable AWS infrastructure

**What you can do:**
- Accept paying customers
- Store and manage files
- Track revenue and users
- Scale to thousands of users

**Next steps:**
- Market your service
- Add more features
- Customize branding
- Launch to production

Congratulations! 🎉
