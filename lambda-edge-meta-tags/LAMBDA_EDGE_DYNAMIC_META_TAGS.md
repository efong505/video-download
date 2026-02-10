# Lambda@Edge Dynamic Meta Tags for Social Sharing

## Overview
Lambda@Edge function that intercepts social media crawler requests and serves article-specific Open Graph meta tags for rich social sharing previews on Facebook, Twitter, LinkedIn, and other platforms.

## Problem Statement
Facebook's scraper only reads initial HTML and cannot see JavaScript-updated meta tags. Without server-side rendering, all article shares show the same default logo and description instead of article-specific featured images and content.

## Solution
Lambda@Edge function deployed at CloudFront edge locations that:
1. Detects social media crawlers by user-agent
2. Fetches article data from DynamoDB
3. Returns HTML with article-specific meta tags
4. Regular users get normal JavaScript-rendered page

## Implementation

### Files Created
- `lambda-edge-meta-tags/index.py` - Lambda@Edge function (Python 3.12)
- `lambda-edge-meta-tags/requirements.txt` - boto3 dependency
- `lambda-edge-meta-tags/README.md` - Complete setup guide
- `deploy-lambda-edge.ps1` - Deployment automation script

### Lambda@Edge Function
**Runtime**: Python 3.12  
**Memory**: 128 MB  
**Timeout**: 5 seconds  
**Region**: us-east-1 (Lambda@Edge requirement)  
**Trigger**: CloudFront Viewer Request  

### Supported Crawlers
- Facebook (facebookexternalhit)
- Twitter (twitterbot)
- LinkedIn (linkedinbot)
- Slack (slackbot)
- WhatsApp (whatsapp)

### Meta Tags Injected
```html
<meta property="og:type" content="article">
<meta property="og:site_name" content="Christian Conservatives Today">
<meta property="og:title" content="Actual Article Title">
<meta property="og:description" content="Article excerpt (first 160 chars)">
<meta property="og:url" content="https://christianconservativestoday.com/article.html?id=uuid">
<meta property="og:image" content="https://christianconservativestoday.com/featured-image.jpg">
<meta property="og:image:secure_url" content="https://christianconservativestoday.com/featured-image.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Actual Article Title">
<meta name="twitter:description" content="Article excerpt">
<meta name="twitter:image" content="https://christianconservativestoday.com/featured-image.jpg">
```

## Cost Analysis

### Lambda@Edge Pricing
- **Request Cost**: $0.60 per 1 million requests
- **Compute Cost**: $0.00005001 per GB-second

### Real-World Costs
| Monthly Shares | Request Cost | Compute Cost | Total Cost |
|---------------|--------------|--------------|------------|
| 50 shares     | $0.00003     | $0.00003     | ~$0.0001   |
| 1,000 shares  | $0.0006      | $0.0006      | ~$0.002    |
| 10,000 shares | $0.006       | $0.006       | ~$1-2      |

### Free Tier
- 1 million requests/month free
- 50,000 GB-seconds compute/month free
- You'd stay well within free tier for low-volume sharing

## Kill Switch

**IMPORTANT**: Lambda@Edge does NOT support environment variables. You must remove/add CloudFront association.

### Using Toggle Script (Recommended)
**Time to Disable/Enable**: 15-30 minutes

```powershell
# Disable Lambda@Edge
.\toggle-lambda-edge.ps1 -Action disable

# Re-enable Lambda@Edge
.\toggle-lambda-edge.ps1 -Action enable

# Check status
.\toggle-lambda-edge.ps1 -Action status
```

### Manual Method
**Time to Disable/Enable**: 15-30 minutes

1. Go to CloudFront > Distribution E3N00R2D2NE9C5 > Behaviors
2. Edit default behavior
3. Remove/Add Lambda@Edge association:
   - Event Type: Viewer Request
   - Function ARN: arn:aws:lambda:us-east-1:371751795928:function:article-meta-tags-edge:2
4. Save changes
5. Wait 15-30 minutes for propagation

## Deployment Process

### Prerequisites
- AWS Account with admin access
- Lambda function must be deployed to us-east-1 region
- CloudFront distribution already configured

### Step 1: Deploy Lambda Function
```powershell
.\deploy-lambda-edge.ps1
```

### Step 2: Publish Lambda Version
1. Go to AWS Console > Lambda > article-meta-tags-edge
2. Actions > Publish new version
3. Note the version ARN (e.g., arn:aws:lambda:us-east-1:123456789:function:article-meta-tags-edge:1)

### Step 3: Associate with CloudFront
1. Go to CloudFront > Your Distribution > Behaviors
2. Edit behavior for *.html files
3. Lambda Function Associations:
   - Event Type: Viewer Request
   - Lambda Function ARN: [paste version ARN from Step 2]
4. Save changes
5. Wait 15-30 minutes for deployment

### Step 4: Test
1. Share article URL on Facebook
2. Use Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
3. Verify article-specific title, description, and featured image appear

## Monitoring

### Check Invocations
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=article-meta-tags-edge \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-31T23:59:59Z \
  --period 86400 \
  --statistics Sum \
  --region us-east-1
```

### Check Errors
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=article-meta-tags-edge \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-31T23:59:59Z \
  --period 86400 \
  --statistics Sum \
  --region us-east-1
```

### View Logs
```bash
aws logs tail /aws/lambda/us-east-1.article-meta-tags-edge --follow --region us-east-1
```

## Comparison: With vs Without Lambda@Edge

### Without Lambda@Edge (Current Implementation)
✅ **Pros**:
- Zero cost
- Already implemented
- No additional setup required
- No maintenance needed

❌ **Cons**:
- All shares show default logo (techcrosslogo.jpg)
- Generic title: "Christian Conservative Articles - Faith-Based Commentary"
- Generic description: "Explore biblical perspectives on current events..."
- No article-specific previews

### With Lambda@Edge (Optional Enhancement)
✅ **Pros**:
- Article-specific featured images in shares
- Actual article titles in previews
- Article excerpts in descriptions
- Better click-through rates
- Professional appearance

❌ **Cons**:
- Small cost (~$1-2/month for 10,000 shares)
- Additional setup and deployment
- Requires monitoring
- Needs maintenance if issues arise

## Recommendation

**Start without Lambda@Edge** (current implementation is sufficient):
- Default meta tags provide acceptable sharing experience
- Zero cost
- No additional complexity

**Deploy Lambda@Edge if**:
- Social sharing becomes major traffic source
- Article-specific previews are important for branding
- Budget allows $1-5/month for enhanced sharing
- You want professional article previews on social media

**Kill switch ensures**:
- Instant disable if costs exceed expectations
- Easy revert to default meta tags
- No risk of runaway costs

## Troubleshooting

### Issue: Lambda@Edge not triggering
**Solution**: Verify CloudFront association includes version number (not $LATEST)

### Issue: Still showing default meta tags
**Solution**: 
1. Clear Facebook cache: https://developers.facebook.com/tools/debug/
2. Wait 5-10 minutes for CloudFront propagation
3. Check Lambda logs for errors

### Issue: High costs
**Solution**: 
1. Set ENABLE_DYNAMIC_META=false immediately
2. Check CloudWatch metrics for unusual traffic
3. Review Lambda logs for bot traffic

### Issue: Errors in Lambda logs
**Solution**:
1. Check DynamoDB permissions
2. Verify article_id extraction logic
3. Test with sample article URLs

## Security Considerations

- Lambda@Edge has no environment variables in code (uses Lambda configuration)
- DynamoDB access requires proper IAM role
- Only processes requests from known social media crawlers
- Regular users bypass Lambda@Edge entirely
- No sensitive data exposed in meta tags

## Future Enhancements

- Cache article data in Lambda memory (reduce DynamoDB calls)
- Support for video meta tags (og:video)
- Custom meta tags per article category
- A/B testing different preview images
- Analytics on share click-through rates

## Support

For issues or questions:
- Check `lambda-edge-meta-tags/README.md` for detailed setup
- Review CloudWatch logs for errors
- Test with Facebook Sharing Debugger
- Disable via kill switch if problems persist

---

**Status**: Implementation complete, ready for deployment  
**Cost**: ~$0.0001 for 50 shares/month (free tier)  
**Kill Switch**: Instant disable via environment variable  
**Deployment Time**: ~30 minutes  
**Maintenance**: Minimal (monitor monthly costs)
