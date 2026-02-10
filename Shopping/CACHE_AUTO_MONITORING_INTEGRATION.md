# Shopping System - Cache Auto-Monitoring Integration

**Created:** November 6, 2025  
**Purpose:** Integrate Shopping system with platform-wide auto-cache-monitor

---

## Current Situation

The main platform has deployed `auto-cache-monitor` Lambda that:
- Runs daily at 2 AM UTC
- Monitors DynamoDB traffic across all tables
- Auto-enables ElastiCache at 2M reads/day
- Auto-enables API Gateway cache at 500K requests/day
- Cost: $0 (Lambda free tier)

**Currently monitors:** Videos, Articles, News, Races, Candidates tables

---

## Required Changes

### 1. Update auto-cache-monitor Lambda

**File:** `Architecture-Improvements/scripts/auto-cache-monitor/index.py`

**Current code:**
```python
tables = ['Videos', 'Articles', 'News', 'Races', 'Candidates']
```

**Update to:**
```python
# Main platform tables
main_tables = ['Videos', 'Articles', 'News', 'Races', 'Candidates']

# Shopping system tables
shopping_tables = ['Products', 'Orders', 'Cart', 'Reviews']

all_tables = main_tables + shopping_tables
total_reads = 0

for table in all_tables:
    # existing monitoring code...
```

### 2. Redeploy Lambda

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Architecture-Improvements\scripts
cd auto-cache-monitor
Compress-Archive -Path index.py -DestinationPath function.zip -Force
cd ..
aws lambda update-function-code --function-name auto-cache-monitor --zip-file fileb://auto-cache-monitor/function.zip --region us-east-1
```

### 3. Test Updated Lambda

```powershell
aws lambda invoke --function-name auto-cache-monitor response.json --region us-east-1
cat response.json
```

Expected output:
```json
{"statusCode": 200, "body": "{\"reads\": 0, \"requests\": 0, \"actions\": []}"}
```

---

## How It Works for Shopping

### Scenario 1: Low Traffic (Current State)
- Shopping tables: 0 reads/day
- Main platform: 500 reads/day
- **Total: 500 reads/day** (way below 2M threshold)
- Action: Nothing - logs "below threshold"
- Cost: $0

### Scenario 2: Shopping Gets Popular
- Shopping tables: 1.5M reads/day (Products, Cart heavily used)
- Main platform: 600K reads/day
- **Total: 2.1M reads/day** (exceeds 2M threshold)
- Action: Auto-enables ElastiCache for ALL tables
- Cost: +$15/month (but saves $50/month on DynamoDB)

### Scenario 3: Only Shopping is Busy
- Shopping tables: 2.5M reads/day
- Main platform: 100K reads/day
- **Total: 2.6M reads/day** (exceeds threshold)
- Action: Auto-enables ElastiCache
- Shopping benefits from caching immediately

---

## Benefits for Shopping System

✅ **Zero manual monitoring** - Automatic threshold detection  
✅ **Shared infrastructure** - One Lambda monitors everything  
✅ **Cost optimization** - Only enables caching when justified  
✅ **Unified monitoring** - All tables tracked together  
✅ **No code changes needed** - Shopping Lambdas work with or without cache

---

## Shopping Lambda Code Pattern

When ElastiCache is enabled, Shopping Lambdas should check cache first:

```python
import boto3
import json

dynamodb = boto3.resource('dynamodb')
elasticache = None  # Will be set if cache exists

def get_product(product_id):
    # Try cache first (if enabled)
    if elasticache:
        try:
            cached = elasticache.get(f'product:{product_id}')
            if cached:
                return json.loads(cached)
        except:
            pass  # Cache miss or not available
    
    # Fallback to DynamoDB
    table = dynamodb.Table('Products')
    response = table.get_item(Key={'product_id': product_id})
    
    # Cache for next time (if cache enabled)
    if elasticache and 'Item' in response:
        elasticache.setex(
            f'product:{product_id}',
            3600,  # 1 hour TTL
            json.dumps(response['Item'])
        )
    
    return response.get('Item')
```

**Key point:** Code works with or without cache. When auto-cache-monitor enables ElastiCache, Shopping Lambdas automatically start using it.

---

## Thresholds Explained

### Why 2M reads/day for ElastiCache?

**Break-even calculation:**
- ElastiCache cost: $15/month
- DynamoDB cost: $0.25 per million reads
- With 80% cache hit rate, need 60M reads/month to save $15
- 60M reads/month = 2M reads/day

**Below 2M reads/day:** Caching costs more than it saves  
**Above 2M reads/day:** Caching saves money

### Why 500K requests/day for API Gateway cache?

**Break-even calculation:**
- API Gateway cache: $25/month (0.5GB)
- Lambda cost: $0.20 per million requests
- With 80% cache hit rate, need 15M requests/month to save $25
- 15M requests/month = 500K requests/day

---

## Shopping-Specific Monitoring

The auto-cache-monitor tracks **combined traffic** across all tables. For Shopping-specific metrics:

```powershell
# Check Shopping table traffic only
aws cloudwatch get-metric-statistics \
    --namespace AWS/DynamoDB \
    --metric-name ConsumedReadCapacityUnits \
    --dimensions Name=TableName,Value=Products \
    --start-time 2025-11-05T00:00:00Z \
    --end-time 2025-11-06T00:00:00Z \
    --period 86400 \
    --statistics Sum
```

---

## Action Items for Shopping Implementation

### Week 1: Database Setup
- [ ] Create Shopping tables (Products, Orders, Cart, Reviews)
- [ ] Update auto-cache-monitor to include Shopping tables
- [ ] Redeploy auto-cache-monitor Lambda
- [ ] Test monitoring with sample data

### Week 2: ElastiCache Preparation
- [ ] Add cache-check logic to Shopping Lambdas
- [ ] Test Lambdas work WITHOUT cache (fallback to DynamoDB)
- [ ] Document cache keys and TTLs
- [ ] Wait for auto-cache-monitor to enable cache (when traffic justifies)

### Week 3: Verify Auto-Caching
- [ ] Monitor daily auto-cache-monitor logs
- [ ] Verify Shopping tables included in traffic counts
- [ ] Test cache hit rates when enabled
- [ ] Confirm cost savings

---

## Cost Impact

### Current (No Shopping System)
- Main platform: ~500 reads/day
- Auto-cache-monitor: $0/month
- ElastiCache: Not enabled (below threshold)
- **Total: $0/month**

### With Shopping (Low Traffic)
- Main platform: 500 reads/day
- Shopping: 10K reads/day
- **Total: 10.5K reads/day** (still below 2M threshold)
- ElastiCache: Not enabled
- **Total: $0/month**

### With Shopping (High Traffic)
- Main platform: 500K reads/day
- Shopping: 1.5M reads/day
- **Total: 2M reads/day** (at threshold)
- ElastiCache: Auto-enabled
- **Total: +$15/month** (but saves $50/month on DynamoDB)

---

## Summary

**No action needed now** - Just update the Lambda code to include Shopping tables when you create them. The auto-monitoring will:

1. Track Shopping tables automatically
2. Enable caching when combined traffic justifies it
3. Shopping Lambdas benefit immediately
4. Zero manual intervention required

**The system is already built and deployed** - just needs Shopping table names added to the monitoring list.

---

## Questions?

Ask in the main architecture implementation chat session.
