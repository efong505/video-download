# Week 1 Summary: Infrastructure Setup

## What We're Building

Week 1 sets up the foundation for the Shopping System:
- **4 SQS Queues** for async processing
- **4 Dead Letter Queues** for failed messages
- **4 DynamoDB Tables** for data storage

This infrastructure follows enterprise-grade architecture patterns and prepares for Weeks 2-9.

---

## Why This Architecture?

### SQS Queues (Message Queues)
**Problem:** Direct Lambda invocations can fail and lose data  
**Solution:** SQS queues with automatic retries

**Benefits:**
- ✅ Automatic retries (3 attempts)
- ✅ No data loss
- ✅ Better error tracking
- ✅ Decoupled services
- ✅ Handles traffic spikes

**Example:**
```
Order Created → order-processing-queue → order_processor Lambda
                     ↓ (if fails 3x)
              order-processing-dlq (alert admin)
```

---

### DynamoDB Tables (NoSQL Database)
**Problem:** Need fast, scalable data storage  
**Solution:** DynamoDB with indexes for efficient queries

**Tables:**
1. **Products** - Product catalog with categories, pricing, inventory
2. **Orders** - Order history with payment and shipping info
3. **Cart** - Shopping carts (expires after 30 days)
4. **Reviews** - Customer reviews and ratings

**Benefits:**
- ✅ Serverless (no server management)
- ✅ Auto-scaling
- ✅ Fast queries with indexes
- ✅ Pay-per-use pricing

---

## What Gets Created

### SQS Queues (8 total)

**Main Queues:**
1. `order-processing-queue` - Process new orders
2. `payment-processing-queue` - Handle payments
3. `email-notification-queue` - Send emails
4. `inventory-update-queue` - Update stock levels

**Dead Letter Queues (DLQs):**
1. `order-processing-dlq` - Failed orders
2. `payment-processing-dlq` - Failed payments
3. `email-notification-dlq` - Failed emails
4. `inventory-update-dlq` - Failed inventory updates

**Configuration:**
- Retry: 3 attempts before DLQ
- Timeout: 1-5 minutes depending on queue
- Retention: 4 days

---

### DynamoDB Tables (4 total)

**1. Products Table**
```
Primary Key: product_id
Indexes:
  - category-created_at-index (browse by category)
  - status-sales_count-index (best sellers)
  - featured-created_at-index (featured products)
```

**2. Orders Table**
```
Primary Key: order_id
Sort Key: user_id
Indexes:
  - user_id-order_date-index (user order history)
  - order_status-order_date-index (admin order management)
  - payment_status-order_date-index (payment tracking)
```

**3. Cart Table**
```
Primary Key: user_id (or session_id for guests)
TTL: expires_at (30 days)
```

**4. Reviews Table**
```
Primary Key: review_id
Sort Key: product_id
Indexes:
  - product_id-created_at-index (product reviews)
  - user_id-created_at-index (user reviews)
```

---

## Time Estimate

| Task | Time | Difficulty |
|------|------|------------|
| Create SQS queues | 2 min | Easy |
| Create DynamoDB tables | 3 min | Easy |
| Test infrastructure | 30 sec | Easy |
| **Total** | **~6 min** | **Easy** |

---

## Cost Estimate

### Week 1 (Development)
- **SQS:** $0 (free tier: 1M requests/month)
- **DynamoDB:** $0 (free tier: 25 GB storage)
- **Total:** $0/month

### Production (Low Traffic)
- **SQS:** ~$0.50/month (100K messages)
- **DynamoDB:** ~$1/month (1M reads, 100K writes)
- **Total:** ~$1.50/month

### Production (High Traffic)
- **SQS:** ~$2/month (1M messages)
- **DynamoDB:** ~$3/month (10M reads, 1M writes)
- **Total:** ~$5/month

**Note:** Still within AWS free tier for first 12 months!

---

## Success Criteria

Week 1 is successful when:

- [x] All 8 SQS queues created
- [x] All 4 DynamoDB tables active
- [x] Test script passes (100% success rate)
- [x] Can send/receive test message
- [x] No errors in AWS Console
- [x] Monitor script shows healthy queues

---

## What's Next?

### Week 2: APIs + ElastiCache (Deferred)
- Create Lambda functions (shop_api, cart_api, order_api, payment_api)
- Set up ElastiCache Redis (when traffic justifies)
- Implement caching layer

**Deferred until:** 10,000 DynamoDB reads/day

### Week 3: Payment + Fault Tolerance
- Integrate PayPal and Stripe
- Add circuit breakers
- Implement rate limiting

### Week 4: Frontend + API Cache
- Build shopping pages (shop.html, product.html, cart.html)
- Enable API Gateway caching

---

## Rollback Plan

If something goes wrong:

```powershell
# Delete all SQS queues
$queues = @("order-processing-queue", "order-processing-dlq", "payment-processing-queue", "payment-processing-dlq", "email-notification-queue", "email-notification-dlq", "inventory-update-queue", "inventory-update-dlq")
foreach ($q in $queues) {
    $url = aws sqs get-queue-url --queue-name $q --query 'QueueUrl' --output text
    aws sqs delete-queue --queue-url $url
}

# Delete all DynamoDB tables
$tables = @("Products", "Orders", "Cart", "Reviews")
foreach ($t in $tables) {
    aws dynamodb delete-table --table-name $t
}
```

**Time to rollback:** ~2 minutes  
**Data loss:** None (no data added yet)

---

## Monitoring

### Real-Time Monitoring
```powershell
.\scripts\monitor-shopping-queues.ps1
```

Shows:
- Queue depths (visible messages)
- In-flight messages (being processed)
- DLQ message counts (failures)
- Updates every 5 seconds

### AWS Console
- **SQS:** https://console.aws.amazon.com/sqs/
- **DynamoDB:** https://console.aws.amazon.com/dynamodb/

---

## Key Learnings

### Why SQS?
- **Reliability:** Automatic retries prevent data loss
- **Scalability:** Handles traffic spikes automatically
- **Decoupling:** Services don't depend on each other
- **Visibility:** Easy to see what's processing

### Why DynamoDB?
- **Serverless:** No server management
- **Fast:** Single-digit millisecond latency
- **Scalable:** Auto-scales with traffic
- **Cost-effective:** Pay only for what you use

### Why This Order?
1. **Infrastructure first** - Foundation must be solid
2. **Test early** - Catch issues before building on top
3. **Monitor always** - Know what's happening in real-time

---

## Common Questions

**Q: Why 4 separate queues instead of 1?**  
A: Separation of concerns. Each queue has different timeout and retry requirements. Orders need 5 minutes, emails need 1 minute.

**Q: Why Dead Letter Queues?**  
A: To capture failed messages for debugging. Without DLQs, failed messages disappear after max retries.

**Q: Why DynamoDB instead of RDS?**  
A: Serverless, auto-scaling, and better for key-value lookups. No server to manage.

**Q: Why defer ElastiCache?**  
A: Costs $15/month. Only worth it at high traffic (10K+ reads/day). Start simple, add when needed.

**Q: Can I skip Week 1?**  
A: No. This is the foundation. Everything else builds on this infrastructure.

---

## Resources

**Documentation:**
- [QUICK_START.md](QUICK_START.md) - Get started in 10 minutes
- [SHOPPING_SYSTEM_PLAN.md](SHOPPING_SYSTEM_PLAN.md) - Complete plan
- [ARCHITECTURE_REQUIREMENTS.md](ARCHITECTURE_REQUIREMENTS.md) - Architecture patterns
- [scripts/README.md](scripts/README.md) - Script documentation

**AWS Documentation:**
- [SQS Developer Guide](https://docs.aws.amazon.com/sqs/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)

---

## Ready to Start?

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts
.\1-create-sqs-queues.ps1
.\2-create-dynamodb-tables.ps1
.\3-test-infrastructure.ps1
```

**Total time: ~6 minutes**  
**Difficulty: Easy**  
**Cost: $0 (free tier)**

Let's do this! 🚀
