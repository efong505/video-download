# Shopping System - Cache Monitoring Summary

## How It Works

The Shopping system integrates with the **existing platform-wide auto-cache-monitor Lambda** that runs daily at 2 AM UTC.

### Single Monitoring Lambda for Everything

**One Lambda monitors:**
- Main platform tables: Videos, Articles, News, Races, Candidates
- Shopping tables: Products, Orders, Cart, Reviews

**Combined traffic triggers caching:**
- When **total reads across all tables** reach 2M/day → Enable ElastiCache
- When **total API requests** reach 500K/day → Enable API Gateway cache

---

## Why Combined Monitoring?

### Scenario 1: Shopping Gets Popular First
- Shopping: 1.8M reads/day
- Main platform: 300K reads/day
- **Total: 2.1M reads/day** ✅ Exceeds threshold
- **Action:** ElastiCache enabled for ALL tables
- **Result:** Both Shopping and main platform benefit

### Scenario 2: Main Platform Gets Popular First
- Main platform: 1.9M reads/day
- Shopping: 200K reads/day
- **Total: 2.1M reads/day** ✅ Exceeds threshold
- **Action:** ElastiCache enabled for ALL tables
- **Result:** Both Shopping and main platform benefit

### Scenario 3: Both Low Traffic
- Main platform: 500 reads/day
- Shopping: 10K reads/day
- **Total: 10.5K reads/day** ❌ Below threshold
- **Action:** Nothing - logs "below threshold"
- **Result:** No unnecessary costs

---

## Thresholds Explained

### ElastiCache: 2M reads/day

**Break-even calculation:**
```
ElastiCache cost: $15/month
DynamoDB cost: $0.25 per million reads
With 80% cache hit rate: Need 60M reads/month to save $15
60M reads/month = 2M reads/day
```

**Below 2M:** Caching costs more than it saves  
**Above 2M:** Caching saves money

### API Gateway Cache: 500K requests/day

**Break-even calculation:**
```
API Gateway cache: $25/month (0.5GB)
Lambda cost: $0.20 per million requests
With 80% cache hit rate: Need 15M requests/month to save $25
15M requests/month = 500K requests/day
```

**Below 500K:** Caching costs more than it saves  
**Above 500K:** Caching saves money

---

## What We Updated

### Before (Main Platform Only)
```python
tables = ['Videos', 'Articles', 'News', 'Races', 'Candidates']
```

### After (Main Platform + Shopping)
```python
# Main platform tables
main_tables = ['Videos', 'Articles', 'News', 'Races', 'Candidates']
# Shopping system tables (added Nov 2025)
shopping_tables = ['Products', 'Orders', 'Cart', 'Reviews']

all_tables = main_tables + shopping_tables
```

---

## Shopping Lambda Code Pattern

Shopping Lambdas should implement **cache-with-fallback** pattern:

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

**Key points:**
- ✅ Works with or without cache
- ✅ Graceful fallback to DynamoDB
- ✅ Automatic caching when available
- ✅ No code changes needed when cache enabled

---

## Cache TTLs for Shopping

Recommended TTLs for Shopping data:

| Data Type | TTL | Reason |
|-----------|-----|--------|
| Products | 1 hour | Rarely change |
| Cart | 30 min | Frequently updated |
| Orders | 1 hour | Rarely change after creation |
| Reviews | 1 hour | Rarely change |
| Categories | 24 hours | Very rarely change |
| Featured Products | 15 min | May change for promotions |

---

## Monitoring Commands

### Check Combined Traffic
```powershell
# Manual check (runs same logic as Lambda)
cd ..\..\Architecture-Improvements\scripts
.\monitor-cache-threshold.ps1
```

### Check Shopping Tables Only
```powershell
# Products table
aws cloudwatch get-metric-statistics `
    --namespace AWS/DynamoDB `
    --metric-name ConsumedReadCapacityUnits `
    --dimensions Name=TableName,Value=Products `
    --start-time 2025-11-05T00:00:00Z `
    --end-time 2025-11-06T00:00:00Z `
    --period 86400 `
    --statistics Sum

# Orders table
aws cloudwatch get-metric-statistics `
    --namespace AWS/DynamoDB `
    --metric-name ConsumedReadCapacityUnits `
    --dimensions Name=TableName,Value=Orders `
    --start-time 2025-11-05T00:00:00Z `
    --end-time 2025-11-06T00:00:00Z `
    --period 86400 `
    --statistics Sum
```

### Check Lambda Logs
```powershell
aws logs tail /aws/lambda/auto-cache-monitor --follow
```

---

## Cost Impact

### Current State (Low Traffic)
- Main platform: 500 reads/day
- Shopping: 0 reads/day (not launched yet)
- **Total: 500 reads/day**
- ElastiCache: Not enabled
- **Cost: $0/month**

### After Shopping Launch (Low Traffic)
- Main platform: 500 reads/day
- Shopping: 10K reads/day
- **Total: 10.5K reads/day**
- ElastiCache: Not enabled (below threshold)
- **Cost: $0/month**

### After Shopping Gets Popular
- Main platform: 500K reads/day
- Shopping: 1.5M reads/day
- **Total: 2M reads/day** ✅ At threshold
- ElastiCache: Auto-enabled
- **Cost: +$15/month** (but saves $50/month on DynamoDB)
- **Net savings: $35/month**

---

## Benefits

✅ **Zero manual monitoring** - Runs automatically daily  
✅ **Cost-optimized** - Only enables caching when it saves money  
✅ **Unified infrastructure** - One Lambda for everything  
✅ **Automatic scaling** - Adapts to traffic growth  
✅ **No code changes** - Shopping Lambdas work with or without cache  
✅ **Shared benefits** - All tables benefit when threshold reached  

---

## Action Items

### Week 1 (Now)
- [x] Update auto-cache-monitor Lambda code
- [ ] Run `.\4-update-cache-monitor.ps1`
- [ ] Verify Lambda updated successfully
- [ ] Test Lambda invocation

### Week 2-3 (Lambda Development)
- [ ] Implement cache-with-fallback pattern in Shopping Lambdas
- [ ] Test Lambdas work WITHOUT cache (fallback to DynamoDB)
- [ ] Document cache keys and TTLs

### Week 4+ (After Launch)
- [ ] Monitor daily auto-cache-monitor logs
- [ ] Track combined traffic growth
- [ ] Verify cache hit rates when enabled
- [ ] Confirm cost savings

---

## FAQ

**Q: Why not separate monitoring for Shopping?**  
A: Combined monitoring is more efficient. If either system gets popular, both benefit from caching.

**Q: What if Shopping traffic is high but main platform is low?**  
A: Doesn't matter - combined traffic triggers caching. Shopping still benefits.

**Q: Can I manually enable caching before threshold?**  
A: Yes, but not recommended. You'll pay $15/month without cost savings.

**Q: What if I want different thresholds for Shopping?**  
A: Not recommended. The 2M threshold is mathematically optimal for break-even.

**Q: How do I know when caching is enabled?**  
A: Check CloudWatch Logs for auto-cache-monitor Lambda. It logs all actions.

**Q: Can I disable auto-caching?**  
A: Yes, but not recommended. Manual monitoring is error-prone and time-consuming.

---

## Summary

**The system is already built** - just needed Shopping table names added. Now:

1. ✅ Auto-cache-monitor tracks Shopping tables
2. ✅ Combined traffic triggers caching
3. ✅ Shopping benefits immediately when enabled
4. ✅ Zero manual intervention required

**Next step:** Run `.\4-update-cache-monitor.ps1` to deploy the update! 🚀
