# Week 3: Rate Limiting Implementation

## Overview

Implement rate limiting to:
- Prevent API abuse
- Protect against DDoS attacks
- Control costs (prevent runaway Lambda invocations)
- Ensure fair usage across users

**Time Required:** 4-6 hours
**Cost Impact:** $0
**Risk Level:** Low

---

## Rate Limiting Strategies

### 1. API Gateway Level (Recommended)
- Built-in AWS feature
- No code changes required
- Per-API key or per-IP
- Cost: Included in API Gateway pricing

### 2. Application Level
- More flexible (per-user, per-action)
- Custom logic
- Uses DynamoDB for tracking
- Cost: Minimal DynamoDB writes

### 3. CloudFront Level
- Geographic restrictions
- IP-based blocking
- WAF integration
- Cost: WAF charges apply

---

## Implementation: API Gateway Rate Limiting

### Step 1: Create Usage Plan (AWS Console)

1. Go to API Gateway → Your API → Usage Plans
2. Click "Create"
3. **Usage Plan Details:**
   - Name: cct-free-tier
   - Description: Free tier rate limits
4. **Throttle:**
   - Rate: 10 requests/second
   - Burst: 20 requests
5. **Quota:**
   - 10,000 requests per day
   - 300,000 requests per month
6. Click "Create"

### Step 2: Create API Keys

1. API Gateway → API Keys → Create API Key
2. **Details:**
   - Name: user-{email}
   - Auto Generate: Yes
3. Click "Save"
4. **Associate with Usage Plan:**
   - Click "Add to Usage Plan"
   - Select: cct-free-tier
   - Click "Add"

### Step 3: Require API Key on Routes

1. API Gateway → Your API → Routes
2. Select route (e.g., POST /videos)
3. **Route Settings:**
   - API Key Required: Yes
4. Click "Save"
5. **Deploy API** for changes to take effect

---

## Implementation: Application-Level Rate Limiting

### rate_limiter.py (Reusable Module)

```python
import boto3
import time
from decimal import Decimal
from functools import wraps

dynamodb = boto3.resource('dynamodb')
rate_limit_table = dynamodb.Table('rate-limits')

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_allowed(self, user_id, action):
        """Check if request is allowed"""
        now = Decimal(str(time.time()))
        window_start = now - Decimal(str(self.window_seconds))
        
        # Get recent requests
        try:
            response = rate_limit_table.query(
                KeyConditionExpression='user_id = :uid AND #ts > :start',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':uid': user_id,
                    ':start': window_start
                }
            )
            
            request_count = len(response['Items'])
            
            if request_count >= self.max_requests:
                return False, f"Rate limit exceeded. Max {self.max_requests} requests per {self.window_seconds}s"
            
            # Record this request
            rate_limit_table.put_item(Item={
                'user_id': user_id,
                'timestamp': now,
                'action': action,
                'ttl': int(now + Decimal(str(self.window_seconds * 2)))  # Auto-delete old records
            })
            
            remaining = self.max_requests - request_count - 1
            return True, f"{remaining} requests remaining"
            
        except Exception as e:
            print(f"Rate limit check error: {e}")
            # Fail open (allow request if rate limit check fails)
            return True, "Rate limit check unavailable"

def rate_limit(max_requests=10, window_seconds=60):
    """Decorator for rate limiting"""
    def decorator(func):
        limiter = RateLimiter(max_requests, window_seconds)
        
        @wraps(func)
        def wrapper(event, context):
            # Extract user ID from JWT token
            user_id = get_user_from_token(event)
            action = event.get('rawPath') or event.get('path')
            
            allowed, message = limiter.is_allowed(user_id, action)
            
            if not allowed:
                return {
                    'statusCode': 429,
                    'headers': {
                        'Retry-After': str(window_seconds),
                        'X-RateLimit-Limit': str(max_requests),
                        'X-RateLimit-Remaining': '0'
                    },
                    'body': json.dumps({'error': message})
                }
            
            # Call original function
            response = func(event, context)
            
            # Add rate limit headers
            if 'headers' not in response:
                response['headers'] = {}
            
            response['headers']['X-RateLimit-Limit'] = str(max_requests)
            response['headers']['X-RateLimit-Remaining'] = message.split()[0]
            
            return response
        
        return wrapper
    return decorator

def get_user_from_token(event):
    """Extract user ID from JWT token"""
    import jwt
    import os
    
    token = event.get('headers', {}).get('authorization', '').replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        return payload['email']
    except:
        # Anonymous user - use IP address
        return event.get('requestContext', {}).get('http', {}).get('sourceIp', 'unknown')
```

---

## Tiered Rate Limits

### Different Limits by Subscription Tier

```python
RATE_LIMITS = {
    'free': {
        'video_download': (5, 3600),      # 5 per hour
        'article_create': (10, 86400),    # 10 per day
        'api_calls': (100, 60)            # 100 per minute
    },
    'premium': {
        'video_download': (50, 3600),     # 50 per hour
        'article_create': (100, 86400),   # 100 per day
        'api_calls': (1000, 60)           # 1000 per minute
    },
    'pro': {
        'video_download': (200, 3600),    # 200 per hour
        'article_create': (500, 86400),   # 500 per day
        'api_calls': (5000, 60)           # 5000 per minute
    },
    'enterprise': {
        'video_download': (999999, 3600), # Unlimited
        'article_create': (999999, 86400),
        'api_calls': (999999, 60)
    }
}

def get_rate_limit(user_email, action):
    """Get rate limit based on user's subscription tier"""
    user = get_user(user_email)
    tier = user.get('subscription_tier', 'free')
    
    limits = RATE_LIMITS.get(tier, RATE_LIMITS['free'])
    max_requests, window = limits.get(action, (10, 60))
    
    return RateLimiter(max_requests, window)
```

---

## Usage in Lambda Functions

### Example: Video Download with Rate Limiting

```python
from rate_limiter import rate_limit, get_rate_limit

@rate_limit(max_requests=5, window_seconds=3600)
def lambda_handler(event, context):
    """Video download with rate limiting"""
    
    # Extract user
    user_email = get_user_from_token(event)
    
    # Check tier-specific rate limit
    limiter = get_rate_limit(user_email, 'video_download')
    allowed, message = limiter.is_allowed(user_email, 'video_download')
    
    if not allowed:
        return {
            'statusCode': 429,
            'body': json.dumps({
                'error': message,
                'upgrade_url': 'https://christianconservativestoday.com/pricing'
            })
        }
    
    # Process video download
    # ...
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'success'})
    }
```

---

## DynamoDB Table Setup

### Create rate-limits Table

```bash
# AWS CLI
aws dynamodb create-table \
    --table-name rate-limits \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
        AttributeName=timestamp,AttributeType=N \
    --key-schema \
        AttributeName=user_id,KeyType=HASH \
        AttributeName=timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --time-to-live-specification \
        Enabled=true,AttributeName=ttl
```

### AWS Console Method:
1. DynamoDB → Tables → Create table
2. **Table details:**
   - Table name: rate-limits
   - Partition key: user_id (String)
   - Sort key: timestamp (Number)
3. **Settings:**
   - Capacity mode: On-demand
4. Click "Create table"
5. **Enable TTL:**
   - Table → Additional settings → Time to Live
   - TTL attribute: ttl
   - Enable TTL

---

## IP-Based Rate Limiting (CloudFront + WAF)

### Step 1: Create WAF Web ACL

```bash
# Create IP set for blocked IPs
aws wafv2 create-ip-set \
    --name blocked-ips \
    --scope CLOUDFRONT \
    --ip-address-version IPV4 \
    --addresses 192.0.2.0/24

# Create rate-based rule
aws wafv2 create-web-acl \
    --name cct-rate-limit \
    --scope CLOUDFRONT \
    --default-action Allow={} \
    --rules file://rate-limit-rule.json
```

### rate-limit-rule.json

```json
[
    {
        "Name": "RateLimitRule",
        "Priority": 1,
        "Statement": {
            "RateBasedStatement": {
                "Limit": 2000,
                "AggregateKeyType": "IP"
            }
        },
        "Action": {
            "Block": {}
        },
        "VisibilityConfig": {
            "SampledRequestsEnabled": true,
            "CloudWatchMetricsEnabled": true,
            "MetricName": "RateLimitRule"
        }
    }
]
```

### Step 2: Associate with CloudFront

```bash
# Get CloudFront distribution ID
DIST_ID=$(aws cloudfront list-distributions \
    --query "DistributionList.Items[?Aliases.Items[0]=='christianconservativestoday.com'].Id" \
    --output text)

# Get WAF ACL ARN
ACL_ARN=$(aws wafv2 list-web-acls \
    --scope CLOUDFRONT \
    --query "WebACLs[?Name=='cct-rate-limit'].ARN" \
    --output text)

# Associate WAF with CloudFront
aws cloudfront update-distribution \
    --id $DIST_ID \
    --web-acl-id $ACL_ARN
```

---

## Monitoring

### CloudWatch Metrics

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def record_rate_limit_event(user_id, action, allowed):
    """Record rate limit events"""
    cloudwatch.put_metric_data(
        Namespace='CCT/RateLimiting',
        MetricData=[
            {
                'MetricName': 'RateLimitExceeded' if not allowed else 'RequestAllowed',
                'Value': 1,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'Action', 'Value': action},
                    {'Name': 'UserId', 'Value': user_id}
                ]
            }
        ]
    )
```

### CloudWatch Alarms

```bash
# Alert on high rate limit violations
aws cloudwatch put-metric-alarm \
    --alarm-name high-rate-limit-violations \
    --alarm-description "Alert when rate limits frequently exceeded" \
    --metric-name RateLimitExceeded \
    --namespace CCT/RateLimiting \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 100 \
    --comparison-operator GreaterThanThreshold
```

---

## Testing

### Test Rate Limiter

```python
# test_rate_limiter.py
from rate_limiter import RateLimiter
import time

limiter = RateLimiter(max_requests=5, window_seconds=10)

# Test 1: Allow first 5 requests
for i in range(5):
    allowed, msg = limiter.is_allowed('test-user', 'test-action')
    print(f"Request {i+1}: {allowed} - {msg}")

# Test 2: Block 6th request
allowed, msg = limiter.is_allowed('test-user', 'test-action')
print(f"Request 6: {allowed} - {msg}")

# Test 3: Allow after window expires
time.sleep(11)
allowed, msg = limiter.is_allowed('test-user', 'test-action')
print(f"Request 7 (after window): {allowed} - {msg}")
```

### Load Test

```bash
# Use Apache Bench to test rate limiting
ab -n 100 -c 10 \
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    https://api.christianconservativestoday.com/articles

# Expected: First 10 succeed, rest get 429 status
```

---

## User-Friendly Error Messages

```python
def rate_limit_error_response(tier, action, retry_after):
    """Generate helpful error message"""
    
    messages = {
        'free': {
            'video_download': "You've reached your free tier limit of 5 video downloads per hour. Upgrade to Premium for 50 downloads/hour!",
            'article_create': "Free tier allows 10 articles per day. Upgrade to Premium for unlimited articles!"
        },
        'premium': {
            'video_download': "You've reached your Premium limit of 50 downloads per hour. Upgrade to Pro for 200 downloads/hour!"
        }
    }
    
    message = messages.get(tier, {}).get(action, f"Rate limit exceeded. Try again in {retry_after} seconds.")
    
    return {
        'statusCode': 429,
        'headers': {
            'Retry-After': str(retry_after),
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'error': 'Rate limit exceeded',
            'message': message,
            'retry_after': retry_after,
            'upgrade_url': 'https://christianconservativestoday.com/pricing',
            'current_tier': tier
        })
    }
```

---

## Deployment

### Create Lambda Layer

```bash
# Package rate limiter
zip -r rate-limiter-layer.zip rate_limiter.py

# Upload to Lambda
aws lambda publish-layer-version \
    --layer-name rate-limiter-layer \
    --description "Rate limiting implementation" \
    --zip-file fileb://rate-limiter-layer.zip \
    --compatible-runtimes python3.12

# Attach to functions
LAYER_ARN=$(aws lambda list-layer-versions \
    --layer-name rate-limiter-layer \
    --query 'LayerVersions[0].LayerVersionArn' \
    --output text)

aws lambda update-function-configuration \
    --function-name router \
    --layers $LAYER_ARN
```

---

## Success Criteria

✅ Rate limiting implemented at API Gateway level
✅ Application-level rate limiting for fine-grained control
✅ Tiered limits based on subscription
✅ DynamoDB table with TTL for automatic cleanup
✅ CloudWatch metrics tracking violations
✅ User-friendly error messages with upgrade prompts
✅ Load testing confirms limits enforced

**Next:** Week 4 - API Gateway Caching
