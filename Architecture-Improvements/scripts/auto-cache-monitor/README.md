# Auto Cache Monitor - Zero-Cost Automatic Caching

## Overview

Automatically monitors traffic and enables caching when thresholds are reached - **completely free**.

## How It Works

1. **EventBridge** triggers Lambda daily at 2 AM UTC (free - 1M events/month)
2. **Lambda** checks CloudWatch metrics (free - 1M requests/month, this uses ~30/month)
3. **Auto-enables** ElastiCache or API Gateway cache when thresholds reached
4. **CloudWatch Logs** record all actions (free - 5GB/month)

## Cost Breakdown

- EventBridge: $0 (30 events/month << 1M free tier)
- Lambda: $0 (30 invocations/month << 1M free tier)
- CloudWatch Logs: $0 (<1MB/month << 5GB free tier)
- **Total: $0/month**

## Thresholds

- **ElastiCache:** Auto-enables at 10,000 DynamoDB reads/day
- **API Gateway Cache:** Auto-enables at 100,000 API requests/day

## Deployment

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Architecture-Improvements\scripts
.\deploy-auto-cache-monitor.ps1
```

## Testing

```powershell
# Test Lambda manually
aws lambda invoke --function-name auto-cache-monitor response.json --region us-east-1
cat response.json

# View logs
aws logs tail /aws/lambda/auto-cache-monitor --follow --region us-east-1
```

## What Happens When Threshold Reached

1. Lambda detects traffic >= threshold
2. Checks if caching already enabled
3. If not enabled:
   - **ElastiCache:** Creates cache.t3.micro Redis cluster
   - **API Gateway:** Enables 0.5GB cache on all stages
4. Logs action to CloudWatch
5. Next day: Verifies cache is working

## Manual Override

You can still use the manual script:

```powershell
# Check current traffic
.\monitor-cache-threshold.ps1

# Manually enable if needed
.\enable-elasticache.ps1
.\enable-api-cache.ps1
```

## Monitoring

```powershell
# Check EventBridge rule
aws events describe-rule --name auto-cache-monitor-daily --region us-east-1

# Check Lambda function
aws lambda get-function --function-name auto-cache-monitor --region us-east-1

# View recent logs
aws logs tail /aws/lambda/auto-cache-monitor --since 1d --region us-east-1
```

## Disable Auto-Monitoring

```powershell
# Disable EventBridge rule (keeps Lambda)
aws events disable-rule --name auto-cache-monitor-daily --region us-east-1

# Delete everything
aws events remove-targets --rule auto-cache-monitor-daily --ids 1 --region us-east-1
aws events delete-rule --name auto-cache-monitor-daily --region us-east-1
aws lambda delete-function --function-name auto-cache-monitor --region us-east-1
```

## Benefits

✅ **Zero Cost:** Uses free tier only
✅ **Automatic:** No manual intervention needed
✅ **Safe:** Only enables when traffic justifies cost
✅ **Transparent:** All actions logged to CloudWatch
✅ **Reversible:** Can disable anytime

## Example Output

```json
{
  "statusCode": 200,
  "body": {
    "reads": 12500,
    "requests": 85000,
    "actions": [
      "ElastiCache enabled (12500 reads/day)"
    ]
  }
}
```

## Next Steps

After deployment:
1. Wait for daily run (2 AM UTC)
2. Check logs next morning
3. When threshold reached, caching auto-enables
4. Monitor cost savings in AWS Cost Explorer
