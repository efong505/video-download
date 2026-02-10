# Lambda@Edge Dynamic Meta Tags

## Purpose
Intercepts social media crawler requests (Facebook, Twitter, LinkedIn) and serves HTML with article-specific meta tags for better social sharing previews.

## Kill Switch
**IMPORTANT**: Lambda@Edge does NOT support environment variables. Use `toggle-lambda-edge.ps1` script to disable/enable by removing/adding CloudFront association.

## How It Works
1. Detects social media crawlers by user-agent
2. Extracts article ID from URL query string
3. Fetches article data from DynamoDB
4. Returns HTML with article-specific og:image, og:title, og:description
5. Regular users get normal JavaScript-rendered page

## Cost
- **Low traffic (50 shares/month)**: ~$0.0001 (free tier)
- **Medium traffic (1,000 shares/month)**: ~$0.002 (free tier)
- **High traffic (10,000 shares/month)**: ~$1-2/month

## Deployment
1. Must deploy to **us-east-1** region (Lambda@Edge requirement)
2. Run `deploy-lambda-edge.ps1`
3. Publish Lambda version in AWS Console
4. Associate with CloudFront distribution (Viewer Request trigger)

## To Disable/Enable
**Use Toggle Script (Recommended)**
```powershell
cd lambda-edge-meta-tags

# Disable Lambda@Edge
.\toggle-lambda-edge.ps1 -Action disable

# Re-enable Lambda@Edge
.\toggle-lambda-edge.ps1 -Action enable

# Check status
.\toggle-lambda-edge.ps1 -Action status
```
Propagation time: 15-30 minutes

**Manual Method**
- CloudFront > Distribution E3N00R2D2NE9C5 > Behaviors > Edit
- Remove/Add Lambda@Edge association
- Wait 15-30 minutes for propagation

## Monitoring Costs
```bash
# Check Lambda@Edge invocations
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

## Supported Crawlers
- Facebook (facebookexternalhit)
- Twitter (twitterbot)
- LinkedIn (linkedinbot)
- Slack (slackbot)
- WhatsApp (whatsapp)
