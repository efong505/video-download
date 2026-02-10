# Quick Start Guide - Architecture Improvements

## 🚀 Get Started in 30 Minutes

This guide will walk you through implementing the highest-impact improvements first.

---

## Prerequisites

✅ AWS CLI installed and configured
✅ Admin access to AWS account
✅ PowerShell 7+ (Windows) or Bash (Linux/Mac)
✅ 30 minutes of focused time

---

## Week 1: SQS Queues (Highest Priority)

### Why Start Here?
- **Effort:** Low (2-3 hours)
- **Impact:** High (fault tolerance, retry logic)
- **Risk:** Very Low (additive, non-breaking)
- **Cost:** $5/month

### Step 1: Run Deployment Script

**Windows (PowerShell):**
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\Architecture-Improvements

# Dry run first (see what would happen)
.\scripts\week1-deploy.ps1 -DryRun

# Actual deployment
.\scripts\week1-deploy.ps1
```

**Linux/Mac (Bash):**
```bash
cd ~/Programming/AWS/Downloader/Architecture-Improvements

# Dry run first
chmod +x scripts/week1-deploy.sh
./scripts/week1-deploy.sh --dry-run

# Actual deployment
./scripts/week1-deploy.sh
```

### Step 2: Update IAM Role

1. Open AWS Console → IAM → Roles
2. Find your Lambda execution role (e.g., `lambda-execution-role`)
3. Click "Add permissions" → "Create inline policy"
4. Click "JSON" tab
5. Paste contents of `sqs-policy.json` (created by script)
6. Name it `SQSAccessPolicy`
7. Click "Create policy"

### Step 3: Update Lambda Environment Variables

1. AWS Console → Lambda → Functions → router
2. Configuration → Environment variables → Edit
3. Add these variables (URLs from script output):
   ```
   VIDEO_QUEUE_URL = https://sqs.us-east-1.amazonaws.com/.../video-processing-queue
   THUMBNAIL_QUEUE_URL = https://sqs.us-east-1.amazonaws.com/.../thumbnail-generation-queue
   EMAIL_QUEUE_URL = https://sqs.us-east-1.amazonaws.com/.../email-queue
   ANALYTICS_QUEUE_URL = https://sqs.us-east-1.amazonaws.com/.../analytics-queue
   ```
4. Click "Save"

### Step 4: Update Lambda Code

See detailed code examples in `01-SQS-IMPLEMENTATION.md`

**Quick summary:**
- Change from direct Lambda invoke to SQS send_message
- Update downloader Lambda to process SQS events
- Configure Lambda triggers for queues

### Step 5: Test

```powershell
# Send test message
aws sqs send-message `
    --queue-url YOUR_VIDEO_QUEUE_URL `
    --message-body '{"job_id":"test-123","video_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Check if processed
aws sqs get-queue-attributes `
    --queue-url YOUR_VIDEO_QUEUE_URL `
    --attribute-names ApproximateNumberOfMessages
```

**Expected:** Message count goes to 0 (processed successfully)

---

## Week 2: API Gateway Caching (Quick Win)

### Why This Next?
- **Effort:** Very Low (1-2 hours)
- **Impact:** Very High (40x faster responses)
- **Risk:** Very Low (AWS managed, easy rollback)
- **Cost:** $25/month (saves $80/month)

### Step 1: Enable Caching (AWS Console)

1. API Gateway → Your API → Stages → prod
2. Click "Settings" tab
3. **Cache Settings:**
   - ✅ Enable API cache
   - Cache capacity: 0.5 GB
   - Cache TTL: 300 seconds (5 minutes)
4. Click "Save Changes"

### Step 2: Configure Routes

1. Go to "Routes" tab
2. For each GET route (articles, videos, resources):
   - Select route
   - ✅ Enable route cache
   - TTL: 300 seconds
   - Click "Save"

### Step 3: Test

```bash
# First request (cache miss)
time curl https://api.christianconservativestoday.com/articles
# Expected: 1-2 seconds

# Second request (cache hit)
time curl https://api.christianconservativestoday.com/articles
# Expected: 50-100ms (20x faster!)
```

### Step 4: Monitor

1. CloudWatch → Metrics → API Gateway
2. Watch `CacheHitCount` and `CacheMissCount`
3. Target: >80% hit rate after 24 hours

---

## Week 3: Circuit Breakers (Reliability)

### Why This Next?
- **Effort:** Low (4-6 hours)
- **Impact:** Medium (prevents cascading failures)
- **Risk:** Very Low (code-level only)
- **Cost:** $0

### Step 1: Add Circuit Breaker Module

Copy `circuit_breaker.py` from `03-CIRCUIT-BREAKERS.md` to your Lambda functions.

### Step 2: Wrap External API Calls

```python
from circuit_breaker import circuit_breaker

@circuit_breaker(failure_threshold=3, timeout=30)
def fetch_bible_verse(reference):
    response = requests.get(f'https://bible-api.com/{reference}', timeout=5)
    return response.json()
```

### Step 3: Deploy

```powershell
# Create Lambda layer
zip -r circuit-breaker-layer.zip circuit_breaker.py

aws lambda publish-layer-version `
    --layer-name circuit-breaker-layer `
    --zip-file fileb://circuit-breaker-layer.zip `
    --compatible-runtimes python3.12

# Attach to functions
aws lambda update-function-configuration `
    --function-name articles-api `
    --layers YOUR_LAYER_ARN
```

---

## Week 4: ElastiCache (Performance Boost)

### Why Save This for Later?
- **Effort:** High (12-16 hours)
- **Impact:** Very High (80% cost reduction)
- **Risk:** Medium (requires VPC setup)
- **Cost:** $15/month (saves $100/month)

### When to Implement
- After Week 1-3 are stable
- When you have a full day to dedicate
- When you're comfortable with VPC concepts

See `02-ELASTICACHE-IMPLEMENTATION.md` for full guide.

---

## Monitoring Your Progress

### Week 1 Success Metrics
- ✅ All 8 queues created (4 main + 4 DLQ)
- ✅ No messages stuck in DLQ
- ✅ Lambda functions processing from queues
- ✅ Failed jobs automatically retry

### Week 2 Success Metrics
- ✅ API Gateway cache enabled
- ✅ Cache hit rate >80%
- ✅ Response times <100ms for cached content
- ✅ Lambda invocations reduced by 80%

### Week 3 Success Metrics
- ✅ Circuit breakers on all external APIs
- ✅ No cascading failures during outages
- ✅ Graceful degradation when services down

---

## Troubleshooting

### SQS Messages Not Processing
1. Check Lambda trigger is enabled
2. Verify IAM permissions
3. Check Lambda logs for errors
4. Verify queue URL in environment variables

### Cache Not Working
1. Verify cache is enabled on stage
2. Check route-level cache settings
3. Look for `X-Cache` header in response
4. Ensure no `Cache-Control: no-cache` headers

### Circuit Breaker Not Opening
1. Verify failure threshold is correct
2. Check exception type matches
3. Add logging to see state transitions
4. Test with intentional failures

---

## Cost Tracking

### Before Improvements
- Lambda: $200/month
- DynamoDB: $150/month
- S3: $50/month
- **Total: $400/month**

### After Week 1-3
- Lambda: $180/month (-10%)
- DynamoDB: $150/month (no change yet)
- SQS: $5/month (new)
- API Gateway Cache: $25/month (new)
- **Total: $360/month (10% savings)**

### After Week 4 (ElastiCache)
- Lambda: $120/month (-40%)
- DynamoDB: $50/month (-67%)
- ElastiCache: $15/month (new)
- SQS: $5/month
- API Gateway Cache: $25/month
- **Total: $215/month (46% savings)**

---

## Next Steps

1. ✅ Complete Week 1 (SQS Queues)
2. ✅ Complete Week 2 (API Gateway Caching)
3. ✅ Complete Week 3 (Circuit Breakers)
4. ⏭️ Monitor for 1 week
5. ⏭️ Review metrics and cost savings
6. ⏭️ Proceed to Week 4 (ElastiCache) when ready

---

## Getting Help

### Documentation
- `00-MASTER-PLAN.md` - Overall strategy
- `01-SQS-IMPLEMENTATION.md` - Detailed SQS guide
- `02-ELASTICACHE-IMPLEMENTATION.md` - Caching guide
- `03-CIRCUIT-BREAKERS.md` - Fault tolerance
- `04-RATE-LIMITING.md` - API protection
- `05-API-GATEWAY-CACHING.md` - Response caching

### AWS Resources
- [SQS Documentation](https://docs.aws.amazon.com/sqs/)
- [API Gateway Caching](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html)
- [ElastiCache Documentation](https://docs.aws.amazon.com/elasticache/)

### Support
- AWS Support (if you have a support plan)
- AWS Forums
- Stack Overflow (tag: aws-lambda, amazon-sqs, etc.)

---

## Success! 🎉

After completing Week 1-3, you'll have:
- ✅ Fault-tolerant architecture with automatic retries
- ✅ 20-40x faster response times for cached content
- ✅ Protection against external service failures
- ✅ 10-20% cost reduction
- ✅ Foundation for future improvements

**Your platform is now more reliable, faster, and cheaper to run!**
