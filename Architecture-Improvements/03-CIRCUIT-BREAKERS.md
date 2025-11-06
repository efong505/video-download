# Week 3: Circuit Breakers & Fault Tolerance

## Overview

Implement circuit breaker pattern to prevent cascading failures when external services (bible-api.com, PayPal, etc.) are slow or unavailable.

**Time Required:** 4-6 hours
**Cost Impact:** $0
**Risk Level:** Low (code-level changes only)

---

## Circuit Breaker Pattern

### States
1. **CLOSED** - Normal operation, requests pass through
2. **OPEN** - Service is down, requests fail fast
3. **HALF_OPEN** - Testing if service recovered

### Flow
```
CLOSED → (5 failures) → OPEN → (60s timeout) → HALF_OPEN → (success) → CLOSED
                                              → (failure) → OPEN
```

---

## Implementation

### circuit_breaker.py (Reusable Module)

```python
import time
import functools
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print(f"Circuit breaker HALF_OPEN: Testing {func.__name__}")
            else:
                raise Exception(f"Circuit breaker OPEN: {func.__name__} unavailable")
        
        try:
            result = func(*args, **kwargs)
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                print(f"Circuit breaker CLOSED: {func.__name__} recovered")
            
            return result
            
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"Circuit breaker OPEN: {func.__name__} failed {self.failure_count} times")
            
            raise e
    
    def reset(self):
        """Manually reset circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

def circuit_breaker(failure_threshold=5, timeout=60, expected_exception=Exception):
    """Decorator for circuit breaker pattern"""
    def decorator(func):
        breaker = CircuitBreaker(failure_threshold, timeout, expected_exception)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        wrapper.circuit_breaker = breaker
        return wrapper
    
    return decorator
```

---

## Use Cases

### 1. Bible API Integration

```python
import requests
from circuit_breaker import circuit_breaker

@circuit_breaker(failure_threshold=3, timeout=30, expected_exception=requests.RequestException)
def fetch_bible_verse(reference):
    """Fetch Bible verse with circuit breaker"""
    response = requests.get(
        f'https://bible-api.com/{reference}',
        timeout=5
    )
    response.raise_for_status()
    return response.json()

def get_bible_verse_safe(reference):
    """Safe wrapper with fallback"""
    try:
        return fetch_bible_verse(reference)
    except Exception as e:
        print(f"Bible API unavailable: {e}")
        # Return cached or default response
        return {
            'reference': reference,
            'text': '[Bible verse temporarily unavailable]',
            'translation': 'KJV'
        }
```

### 2. PayPal API Integration

```python
from circuit_breaker import circuit_breaker
import requests

@circuit_breaker(failure_threshold=5, timeout=60)
def call_paypal_api(endpoint, data):
    """PayPal API with circuit breaker"""
    response = requests.post(
        f'https://api.paypal.com/{endpoint}',
        json=data,
        headers={'Authorization': f'Bearer {get_paypal_token()}'},
        timeout=10
    )
    response.raise_for_status()
    return response.json()

def process_subscription_safe(user_email, plan_id):
    """Safe subscription processing"""
    try:
        return call_paypal_api('v1/billing/subscriptions', {
            'plan_id': plan_id,
            'subscriber': {'email_address': user_email}
        })
    except Exception as e:
        print(f"PayPal API unavailable: {e}")
        # Queue for retry or notify admin
        send_admin_alert(f"PayPal API down: {e}")
        return {'status': 'pending', 'retry': True}
```

### 3. External Video Platforms

```python
from circuit_breaker import circuit_breaker
import yt_dlp

@circuit_breaker(failure_threshold=3, timeout=120)
def download_video(url):
    """Download video with circuit breaker"""
    ydl_opts = {
        'format': 'best',
        'socket_timeout': 30
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info

def download_video_safe(url):
    """Safe video download with fallback"""
    try:
        return download_video(url)
    except Exception as e:
        print(f"Video download failed: {e}")
        # Try alternative method or queue for retry
        return {'status': 'failed', 'error': str(e), 'retry_later': True}
```

---

## Advanced: Distributed Circuit Breaker

For multi-Lambda coordination, use DynamoDB to share circuit state:

```python
import boto3
import time
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
circuit_table = dynamodb.Table('circuit-breakers')

class DistributedCircuitBreaker:
    def __init__(self, service_name, failure_threshold=5, timeout=60):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
    
    def get_state(self):
        """Get circuit state from DynamoDB"""
        try:
            response = circuit_table.get_item(Key={'service_name': self.service_name})
            if 'Item' in response:
                item = response['Item']
                
                # Check if circuit should transition from OPEN to HALF_OPEN
                if item['state'] == 'OPEN':
                    if time.time() - float(item['last_failure_time']) > self.timeout:
                        self.update_state('HALF_OPEN')
                        return 'HALF_OPEN'
                
                return item['state']
            
            return 'CLOSED'
        except Exception as e:
            print(f"Error getting circuit state: {e}")
            return 'CLOSED'  # Fail open
    
    def update_state(self, new_state, increment_failures=False):
        """Update circuit state in DynamoDB"""
        try:
            if increment_failures:
                circuit_table.update_item(
                    Key={'service_name': self.service_name},
                    UpdateExpression='SET #state = :state, failure_count = if_not_exists(failure_count, :zero) + :one, last_failure_time = :time',
                    ExpressionAttributeNames={'#state': 'state'},
                    ExpressionAttributeValues={
                        ':state': new_state,
                        ':zero': 0,
                        ':one': 1,
                        ':time': Decimal(str(time.time()))
                    }
                )
            else:
                circuit_table.put_item(Item={
                    'service_name': self.service_name,
                    'state': new_state,
                    'failure_count': 0,
                    'last_failure_time': Decimal(str(time.time()))
                })
        except Exception as e:
            print(f"Error updating circuit state: {e}")
    
    def call(self, func, *args, **kwargs):
        """Execute function with distributed circuit breaker"""
        state = self.get_state()
        
        if state == 'OPEN':
            raise Exception(f"Circuit breaker OPEN: {self.service_name} unavailable")
        
        try:
            result = func(*args, **kwargs)
            
            if state == 'HALF_OPEN':
                self.update_state('CLOSED')
            
            return result
            
        except Exception as e:
            self.update_state('OPEN', increment_failures=True)
            raise e
```

---

## Monitoring

### CloudWatch Metrics

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def record_circuit_breaker_metric(service_name, state):
    """Record circuit breaker state changes"""
    cloudwatch.put_metric_data(
        Namespace='CCT/CircuitBreakers',
        MetricData=[
            {
                'MetricName': 'CircuitBreakerState',
                'Value': 1 if state == 'OPEN' else 0,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'ServiceName', 'Value': service_name}
                ]
            }
        ]
    )
```

### CloudWatch Alarms

```bash
# Alert when circuit breaker opens
aws cloudwatch put-metric-alarm \
    --alarm-name bible-api-circuit-open \
    --alarm-description "Alert when Bible API circuit breaker opens" \
    --metric-name CircuitBreakerState \
    --namespace CCT/CircuitBreakers \
    --statistic Sum \
    --period 60 \
    --evaluation-periods 1 \
    --threshold 1 \
    --comparison-operator GreaterThanOrEqualToThreshold \
    --dimensions Name=ServiceName,Value=bible-api
```

---

## Testing

### Test Circuit Breaker Behavior

```python
# test_circuit_breaker.py
import time
from circuit_breaker import circuit_breaker

call_count = 0

@circuit_breaker(failure_threshold=3, timeout=5)
def flaky_service():
    global call_count
    call_count += 1
    
    if call_count <= 3:
        raise Exception("Service unavailable")
    
    return "Success"

# Test 1: Circuit opens after 3 failures
for i in range(5):
    try:
        result = flaky_service()
        print(f"Call {i+1}: {result}")
    except Exception as e:
        print(f"Call {i+1}: {e}")

# Test 2: Circuit stays open
time.sleep(2)
try:
    flaky_service()
except Exception as e:
    print(f"Circuit still open: {e}")

# Test 3: Circuit transitions to HALF_OPEN after timeout
time.sleep(6)
try:
    result = flaky_service()
    print(f"Circuit recovered: {result}")
except Exception as e:
    print(f"Still failing: {e}")
```

---

## Deployment

### Update Lambda Functions

```bash
# Package circuit breaker module
zip -r circuit-breaker-layer.zip circuit_breaker.py

# Create Lambda layer
aws lambda publish-layer-version \
    --layer-name circuit-breaker-layer \
    --description "Circuit breaker pattern implementation" \
    --zip-file fileb://circuit-breaker-layer.zip \
    --compatible-runtimes python3.12

# Attach to Lambda functions
LAYER_ARN=$(aws lambda list-layer-versions \
    --layer-name circuit-breaker-layer \
    --query 'LayerVersions[0].LayerVersionArn' \
    --output text)

aws lambda update-function-configuration \
    --function-name articles-api \
    --layers $LAYER_ARN
```

---

## Success Criteria

✅ Circuit breaker module implemented
✅ Applied to all external API calls
✅ CloudWatch metrics recording state changes
✅ Alarms configured for circuit opens
✅ Graceful degradation when services unavailable
✅ No cascading failures during outages

**Next:** Week 3 - Rate Limiting Implementation
