# Shopping System - Deployment Scripts

All scripts use `--profile ekewaka` (account 371751795928, us-east-1).

---

## Scripts Overview

### Infrastructure (Week 1)

**1-create-sqs-queues.ps1**
- Creates 4 main queues + 4 DLQs (8 total)
- Configures 3-retry policy before DLQ
- Queues: order-processing, payment-processing, email-notification, inventory-update

**2-create-dynamodb-tables.ps1**
- Creates Products (3 GSIs), Orders (3 GSIs), Cart (TTL), Reviews (2 GSIs)
- Uses GSI definition files: `products-gsi.json`, `orders-gsi.json`, `reviews-gsi.json`

**3-test-infrastructure.ps1**
- Verifies all 8 SQS queues exist
- Verifies all 4 DynamoDB tables are ACTIVE
- Sends/receives test SQS message

**4-update-cache-monitor.ps1**
- Adds Shopping tables to auto-cache-monitor Lambda
- Auto-enables ElastiCache at 2M reads/day

**monitor-shopping-queues.ps1**
- Real-time queue depth + DLQ monitoring
- Refreshes every 5 seconds, Ctrl+C to exit

### APIs (Weeks 2-4)

**5-deploy-products-api.ps1**
- Deploys `products-api` Lambda (Python 3.12, 128MB)
- Creates /products resource on API Gateway `ydq9xzya5d`

**6-create-api-gateway.ps1**
- Creates API Gateway resources and methods
- Configures CORS for all endpoints

**7-deploy-shopping-frontend.ps1**
- Uploads all Shopping HTML pages to S3 `my-video-downloads-bucket/Shopping/`

**8-deploy-orders-api.ps1**
- Deploys `orders-api` Lambda with JWT dependency
- Creates /orders resource on API Gateway

**9-deploy-reviews-api.ps1**
- Deploys `reviews-api` Lambda
- Creates /reviews resource on API Gateway

**9-deploy-paypal-ipn.ps1**
- Deploys PayPal IPN handler Lambda (payment webhook)

**add-sample-products.py**
- Python script to seed 5 sample products into Products table
- Run with: `$env:AWS_PROFILE="ekewaka"; python add-sample-products.py`

### Tracking (Week 7)

**10-create-tracking-tables.ps1**
- Creates ProductViews table (3 GSIs + 90-day TTL)
- Creates WatchList table
- Uses `productviews-gsi.json`

**11-deploy-tracking-api.ps1**
- Deploys `tracking-api` Lambda (Python 3.12, 256MB)
- Creates /tracking resource on API Gateway
- Uses `tracking-trust-policy.json` for IAM role

### Marketing (Week 8)

**12-create-marketing-tables.ps1**
- Creates MarketingQueue table (2 GSIs + 30-day TTL)
- Creates EmailPreferences table
- Uses `marketingqueue-gsi.json`

**13-deploy-marketing-api.ps1**
- Deploys `marketing-api` Lambda (Python 3.12, 512MB, 5min timeout)
- Creates /marketing resource on API Gateway
- Creates CloudWatch Events rule `marketing-daily-scan` (10 AM EST daily)

### Testing & Monitoring (Week 9)

**14-smoke-test.ps1**
- Tests all 13 API endpoints across 5 resources
- Products: list, search, get
- Reviews: list
- Orders: list, create
- Tracking: popular, recommendations, watchlist, track-view, track-cart-add
- Marketing: stats, preferences, run-scans

**15-create-monitoring.ps1**
- Creates CloudWatch Dashboard `Shopping-System` (6 widgets)
- Creates 14 alarms: 4 DLQ + 5 error rate + 5 latency
- Uses `shopping-dashboard.json`

**16-e2e-test.ps1**
- End-to-end test: browse product → track view → track cart add → place order → verify order
- Tests the full customer journey

---

## Support Files

| File | Used By |
|------|---------|
| `products-gsi.json` | Script 2 |
| `orders-gsi.json` | Script 2 |
| `reviews-gsi.json` | Script 2 |
| `productviews-gsi.json` | Script 10 |
| `marketingqueue-gsi.json` | Script 12 |
| `shopping-dashboard.json` | Script 15 |
| `tracking-trust-policy.json` | Script 11 |

---

## Rollback

```powershell
# Delete SQS queues
$queues = @("order-processing-queue", "order-processing-queue-dlq", "payment-processing-queue", "payment-processing-queue-dlq", "email-notification-queue", "email-notification-queue-dlq", "inventory-update-queue", "inventory-update-queue-dlq")
foreach ($q in $queues) {
    $url = aws sqs get-queue-url --queue-name $q --query 'QueueUrl' --output text --profile ekewaka
    aws sqs delete-queue --queue-url $url --profile ekewaka
}

# Delete DynamoDB tables
$tables = @("Products", "Orders", "Cart", "Reviews", "ProductViews", "WatchList", "MarketingQueue", "EmailPreferences")
foreach ($t in $tables) {
    aws dynamodb delete-table --table-name $t --profile ekewaka
}
```
