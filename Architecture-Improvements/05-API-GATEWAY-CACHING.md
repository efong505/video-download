# Week 4: API Gateway Caching

## Overview

Enable API Gateway caching for instant performance boost:
- Response times: 2s → 50ms (40x faster)
- Lambda invocations: -90% (huge cost savings)
- Zero code changes required
- Managed by AWS

**Time Required:** 2-4 hours
**Cost Impact:** +$25/month (saves $80/month on Lambda)
**Risk Level:** Very Low (AWS managed feature)

---

## How API Gateway Caching Works

```
Request → API Gateway → Check Cache
                      ↓ (cache hit)
                      Return cached response (50ms)
                      ↓ (cache miss)
                      Lambda → DynamoDB → Response
                      ↓
                      Store in cache → Return response
```

**Cache Hit:** Response served from API Gateway (no Lambda invocation)
**Cache Miss:** Lambda invoked, response cached for next request

---

## What to Cache

### ✅ Cache These Endpoints
- **GET /articles** - Article listings (rarely change)
- **GET /articles/{id}** - Individual articles (static after publish)
- **GET /videos** - Video gallery (changes infrequently)
- **GET /resources** - Resource library (rarely updated)
- **GET /election-map** - Election data (updated weekly)
- **GET /news** - News articles (updated daily)

### ❌ Don't Cache These
- **POST /videos** - Video uploads (unique every time)
- **POST /auth/login** - Authentication (security risk)
- **GET /download-status** - Real-time status (stale data problem)
- **POST /comments** - User-generated content (must be fresh)
- **PUT /articles/{id}** - Updates (must reflect immediately)

---

## Step 1: Enable Caching (AWS Console)

### Navigate to API Gateway
1. Open AWS Console
2. Go to API Gateway
3. Select your API (e.g., "cct-api")
4. Click "Stages" in left sidebar
5. Select your stage (e.g., "prod")

### Enable Cache
1. Click "Settings" tab
2. **Cache Settings:**
   - ✅ Enable API cache
   - Cache capacity: 0.5 GB ($25/month)
   - Cache time-to-live (TTL): 300 seconds (5 minutes)
   - ✅ Encrypt cache data
   - ✅ Require authorization (prevents cache poisoning)
3. Click "Save Changes"

### Configure Per-Route Caching
1. Go to "Routes" tab
2. Select route (e.g., GET /articles)
3. **Cache Settings:**
   - ✅ Enable route cache
   - TTL override: 300 seconds
   - Cache key parameters: None (cache all requests the same)
4. Click "Save"

---

## Step 2: Enable Caching (AWS CLI)

### Bash Script

```bash
#!/bin/bash
# enable-api-cache.sh

API_ID="your-api-id"
STAGE_NAME="prod"

echo "Enabling API Gateway cache..."

# Enable cache on stage
aws apigatewayv2 update-stage \
    --api-id $API_ID \
    --stage-name $STAGE_NAME \
    --route-settings '{
        "GET /articles": {
            "DataTraceEnabled": true,
            "ThrottlingBurstLimit": 100,
            "ThrottlingRateLimit": 50,
            "CachingEnabled": true,
            "CacheTtlInSeconds": 300
        },
        "GET /articles/{id}": {
            "CachingEnabled": true,
            "CacheTtlInSeconds": 600
        },
        "GET /videos": {
            "CachingEnabled": true,
            "CacheTtlInSeconds": 300
        },
        "GET /resources": {
            "CachingEnabled": true,
            "CacheTtlInSeconds": 600
        },
        "GET /election-map": {
            "CachingEnabled": true,
            "CacheTtlInSeconds": 3600
        }
    }'

echo "✅ API Gateway cache enabled!"
```

### PowerShell Script

```powershell
# enable-api-cache.ps1

$ApiId = "your-api-id"
$StageName = "prod"

Write-Host "Enabling API Gateway cache..." -ForegroundColor Cyan

# Enable cache on stage
aws apigatewayv2 update-stage `
    --api-id $ApiId `
    --stage-name $StageName `
    --route-settings '{
        \"GET /articles\": {
            \"CachingEnabled\": true,
            \"CacheTtlInSeconds\": 300
        },
        \"GET /articles/{id}\": {
            \"CachingEnabled\": true,
            \"CacheTtlInSeconds\": 600
        },
        \"GET /videos\": {
            \"CachingEnabled\": true,
            \"CacheTtlInSeconds\": 300
        },
        \"GET /resources\": {
            \"CachingEnabled\": true,
            \"CacheTtlInSeconds\": 600
        },
        \"GET /election-map\": {
            \"CachingEnabled\": true,
            \"CacheTtlInSeconds\": 3600
        }
    }'

Write-Host "✅ API Gateway cache enabled!" -ForegroundColor Green
```

---

## Step 3: Cache Key Configuration

### Simple Caching (All Requests Cached the Same)
```
GET /articles → Cache Key: "GET-/articles"
```
All users get the same cached response.

### Parameterized Caching (Different Cache per Parameter)
```
GET /articles?category=sermons → Cache Key: "GET-/articles-sermons"
GET /articles?category=politics → Cache Key: "GET-/articles-politics"
```

### Configure Cache Keys (Console)
1. API Gateway → Stages → prod → Routes
2. Select route: GET /articles
3. **Cache key parameters:**
   - Add parameter: category
   - Add parameter: page
4. Click "Save"

### Configure Cache Keys (CLI)
```bash
aws apigatewayv2 update-route \
    --api-id $API_ID \
    --route-id $ROUTE_ID \
    --request-parameters '{
        "method.request.querystring.category": {
            "Required": false,
            "Caching": true
        },
        "method.request.querystring.page": {
            "Required": false,
            "Caching": true
        }
    }'
```

---

## Step 4: Cache Invalidation

### Manual Invalidation (Console)
1. API Gateway → Stages → prod
2. Click "Invalidate cache" button
3. Confirm

### Manual Invalidation (CLI)
```bash
# Invalidate entire cache
aws apigateway flush-stage-cache \
    --rest-api-id $API_ID \
    --stage-name prod
```

### Programmatic Invalidation (Lambda)

When content is updated, invalidate cache:

```python
import boto3

apigateway = boto3.client('apigateway')

def invalidate_cache(api_id, stage_name):
    """Invalidate API Gateway cache"""
    try:
        apigateway.flush_stage_cache(
            restApiId=api_id,
            stageName=stage_name
        )
        print(f"✅ Cache invalidated for {api_id}/{stage_name}")
        return True
    except Exception as e:
        print(f"❌ Cache invalidation failed: {e}")
        return False

# Use in Lambda functions that update content
def update_article(article_id, updates):
    # Update article in DynamoDB
    articles_table.update_item(...)
    
    # Invalidate cache
    invalidate_cache('your-api-id', 'prod')
    
    return {'success': True}
```

### Selective Invalidation (Custom Header)

Add custom header to bypass cache:

```python
# Lambda response
return {
    'statusCode': 200,
    'headers': {
        'Cache-Control': 'no-cache'  # Don't cache this response
    },
    'body': json.dumps(data)
}
```

---

## Step 5: Cache Headers

### Control Caching Behavior

```python
def lambda_handler(event, context):
    # Get article
    article = get_article(article_id)
    
    # Determine cache headers based on content
    if article['status'] == 'draft':
        # Don't cache drafts
        cache_control = 'no-cache, no-store, must-revalidate'
    elif article['status'] == 'published':
        # Cache published articles for 1 hour
        cache_control = 'public, max-age=3600'
    
    return {
        'statusCode': 200,
        'headers': {
            'Cache-Control': cache_control,
            'Content-Type': 'application/json'
        },
        'body': json.dumps(article)
    }
```

### Cache-Control Values

| Value | Meaning | Use Case |
|-------|---------|----------|
| `public, max-age=3600` | Cache for 1 hour, shareable | Published articles |
| `private, max-age=300` | Cache for 5 min, user-specific | User profiles |
| `no-cache` | Revalidate before using | Frequently updated |
| `no-store` | Never cache | Sensitive data |
| `must-revalidate` | Check freshness | Critical data |

---

## Monitoring

### CloudWatch Metrics

Key metrics to monitor:
- **CacheHitCount** - Requests served from cache
- **CacheMissCount** - Requests that invoked Lambda
- **Count** - Total requests
- **Latency** - Response time

### Calculate Cache Hit Rate

```bash
# Get cache metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/ApiGateway \
    --metric-name CacheHitCount \
    --dimensions Name=ApiName,Value=cct-api Name=Stage,Value=prod \
    --start-time 2025-01-01T00:00:00Z \
    --end-time 2025-01-02T00:00:00Z \
    --period 3600 \
    --statistics Sum

# Cache Hit Rate = CacheHitCount / (CacheHitCount + CacheMissCount)
# Target: >80%
```

### CloudWatch Dashboard

```json
{
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/ApiGateway", "CacheHitCount", {"stat": "Sum"}],
                    [".", "CacheMissCount", {"stat": "Sum"}]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "API Gateway Cache Performance"
            }
        }
    ]
}
```

---

## Testing

### Test 1: Verify Caching Enabled

```bash
# First request (cache miss)
curl -i https://api.christianconservativestoday.com/articles

# Look for headers:
# X-Cache: Miss from cloudfront
# X-Amz-Cf-Pop: IAD89-C1

# Second request (cache hit)
curl -i https://api.christianconservativestoday.com/articles

# Look for headers:
# X-Cache: Hit from cloudfront
```

### Test 2: Measure Performance

```bash
# Without cache (first request)
time curl https://api.christianconservativestoday.com/articles
# Expected: 1-2 seconds

# With cache (subsequent requests)
time curl https://api.christianconservativestoday.com/articles
# Expected: 50-100ms
```

### Test 3: Cache Invalidation

```bash
# Request 1 (cache miss)
curl https://api.christianconservativestoday.com/articles

# Request 2 (cache hit)
curl https://api.christianconservativestoday.com/articles

# Invalidate cache
aws apigateway flush-stage-cache --rest-api-id $API_ID --stage-name prod

# Request 3 (cache miss again)
curl https://api.christianconservativestoday.com/articles
```

---

## Cost Analysis

### Cache Pricing
- **0.5 GB cache:** $0.020/hour = $14.40/month
- **1.6 GB cache:** $0.038/hour = $27.36/month
- **6.1 GB cache:** $0.200/hour = $144/month

### Savings Calculation

**Before Caching:**
- 1M requests/month
- 100% invoke Lambda
- Lambda cost: $0.20 per 1M requests × 2s avg = $100/month

**After Caching (80% hit rate):**
- 800K requests from cache (no Lambda)
- 200K requests invoke Lambda
- Lambda cost: $0.20 per 1M requests × 200K = $20/month
- Cache cost: $15/month
- **Total: $35/month (65% savings)**

**ROI:** 2.8x return on investment

---

## Best Practices

### 1. Start Small
- Begin with 0.5 GB cache
- Monitor hit rate
- Upgrade if needed

### 2. Set Appropriate TTLs
- Static content: 1 hour (3600s)
- Semi-static: 5 minutes (300s)
- Dynamic: Don't cache

### 3. Use Cache Keys Wisely
- Only include parameters that affect response
- Avoid user-specific parameters (low hit rate)

### 4. Invalidate on Updates
- Flush cache when content changes
- Use selective invalidation if possible

### 5. Monitor Performance
- Track cache hit rate (target: >80%)
- Watch for cache thrashing (frequent misses)
- Adjust TTLs based on usage patterns

---

## Troubleshooting

### Problem: Low Cache Hit Rate (<50%)

**Causes:**
- Too many cache key parameters
- TTL too short
- Frequent content updates

**Solutions:**
- Reduce cache key parameters
- Increase TTL for stable content
- Implement smarter invalidation

### Problem: Stale Data

**Causes:**
- TTL too long
- Cache not invalidated on updates

**Solutions:**
- Reduce TTL
- Add cache invalidation to update functions
- Use Cache-Control headers

### Problem: High Costs

**Causes:**
- Cache size too large
- Low hit rate (wasting money)

**Solutions:**
- Downgrade cache size
- Optimize cache keys
- Review what's being cached

---

## Rollback Plan

```bash
# Disable caching (immediate)
aws apigatewayv2 update-stage \
    --api-id $API_ID \
    --stage-name prod \
    --route-settings '{
        "GET /articles": {
            "CachingEnabled": false
        }
    }'

# Or delete cache entirely
aws apigateway update-stage \
    --rest-api-id $API_ID \
    --stage-name prod \
    --patch-operations op=replace,path=/cacheClusterEnabled,value=false
```

---

## Success Criteria

✅ API Gateway caching enabled for read endpoints
✅ Cache hit rate >80% after 24 hours
✅ Response times <100ms for cached content
✅ Lambda invocations reduced by 80%
✅ Cache invalidation working on content updates
✅ CloudWatch dashboard monitoring cache performance
✅ Cost savings of $50-80/month achieved

**Next:** Month 2 - Lambda Refactoring (Optional)
