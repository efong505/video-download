# Shopping System - Quick Start Guide

## Prerequisites

✅ AWS CLI configured with `--profile ekewaka`
✅ PowerShell 7+ installed
✅ Region: us-east-1

---

## All Deployment Scripts

Navigate to the scripts directory:
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts
```

### Week 1: Infrastructure (SQS + DynamoDB)

| Script | What It Does | Time |
|--------|-------------|------|
| `1-create-sqs-queues.ps1` | Creates 4 main queues + 4 DLQs | ~2 min |
| `2-create-dynamodb-tables.ps1` | Creates Products, Orders, Cart, Reviews tables | ~3 min |
| `3-test-infrastructure.ps1` | Verifies all queues and tables exist | ~30 sec |
| `4-update-cache-monitor.ps1` | Adds Shopping tables to auto-cache-monitor | ~30 sec |
| `monitor-shopping-queues.ps1` | Real-time queue depth monitoring (Ctrl+C to exit) | Ongoing |

### Week 2: Product Catalog API

| Script | What It Does | Time |
|--------|-------------|------|
| `5-deploy-products-api.ps1` | Deploys products-api Lambda + /products API Gateway | ~2 min |
| `add-sample-products.py` | Adds 5 sample products to Products table | ~30 sec |

### Week 3-4: Orders, Reviews, Frontend

| Script | What It Does | Time |
|--------|-------------|------|
| `6-create-api-gateway.ps1` | Creates API Gateway resources and methods | ~2 min |
| `7-deploy-shopping-frontend.ps1` | Uploads HTML pages to S3 | ~1 min |
| `8-deploy-orders-api.ps1` | Deploys orders-api Lambda + /orders API Gateway | ~2 min |
| `9-deploy-reviews-api.ps1` | Deploys reviews-api Lambda + /reviews API Gateway | ~2 min |
| `9-deploy-paypal-ipn.ps1` | Deploys PayPal IPN handler Lambda | ~2 min |

### Week 7: Behavioral Tracking

| Script | What It Does | Time |
|--------|-------------|------|
| `10-create-tracking-tables.ps1` | Creates ProductViews (3 GSIs, TTL) + WatchList tables | ~3 min |
| `11-deploy-tracking-api.ps1` | Deploys tracking-api Lambda + /tracking API Gateway | ~2 min |

### Week 8: Marketing Automation

| Script | What It Does | Time |
|--------|-------------|------|
| `12-create-marketing-tables.ps1` | Creates MarketingQueue (2 GSIs, TTL) + EmailPreferences tables | ~3 min |
| `13-deploy-marketing-api.ps1` | Deploys marketing-api Lambda + /marketing API Gateway + CloudWatch Events rule | ~2 min |

### Week 9: Testing & Monitoring

| Script | What It Does | Time |
|--------|-------------|------|
| `14-smoke-test.ps1` | Tests all 13 API endpoints | ~1 min |
| `15-create-monitoring.ps1` | Creates CloudWatch dashboard + 14 alarms | ~2 min |
| `16-e2e-test.ps1` | End-to-end test: browse → track → cart → order → verify | ~1 min |

---

## Full Deployment (From Scratch)

Run all scripts in order:
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts

# Week 1: Infrastructure
.\1-create-sqs-queues.ps1
.\2-create-dynamodb-tables.ps1
.\3-test-infrastructure.ps1
.\4-update-cache-monitor.ps1

# Week 2-4: APIs + Frontend
.\5-deploy-products-api.ps1
.\6-create-api-gateway.ps1
.\8-deploy-orders-api.ps1
.\9-deploy-reviews-api.ps1
.\7-deploy-shopping-frontend.ps1

# Week 7-8: Tracking + Marketing
.\10-create-tracking-tables.ps1
.\11-deploy-tracking-api.ps1
.\12-create-marketing-tables.ps1
.\13-deploy-marketing-api.ps1

# Week 9: Verify
.\14-smoke-test.ps1
.\15-create-monitoring.ps1
.\16-e2e-test.ps1
```

---

## Verify in AWS Console

### DynamoDB Tables (8)
https://console.aws.amazon.com/dynamodb/ → us-east-1
- Products, Orders, Cart, Reviews
- ProductViews, WatchList, MarketingQueue, EmailPreferences

### SQS Queues (8)
https://console.aws.amazon.com/sqs/ → us-east-1
- order-processing-queue + DLQ
- payment-processing-queue + DLQ
- email-notification-queue + DLQ
- inventory-update-queue + DLQ

### API Gateway
https://console.aws.amazon.com/apigateway/ → `ydq9xzya5d`
- /products, /orders, /reviews, /tracking, /marketing

### CloudWatch
- Dashboard: `Shopping-System`
- Alarms: 14 (search "Shopping" or "DLQ")
- Events Rule: `marketing-daily-scan`

---

## Troubleshooting

### "Access Denied" Error
```powershell
aws sts get-caller-identity --profile ekewaka
aws configure get region --profile ekewaka
# Should return us-east-1
```

### "Table/Queue already exists" Error
Tables and queues are idempotent — safe to skip if they already exist.

### Smoke Test Failures
```powershell
# Re-run individual endpoint tests
.\14-smoke-test.ps1
# Check CloudWatch Logs for Lambda errors
```

---

## Support Files

| File | Purpose |
|------|---------|
| `products-gsi.json` | GSI definitions for Products table |
| `orders-gsi.json` | GSI definitions for Orders table |
| `reviews-gsi.json` | GSI definitions for Reviews table |
| `productviews-gsi.json` | GSI definitions for ProductViews table |
| `marketingqueue-gsi.json` | GSI definitions for MarketingQueue table |
| `shopping-dashboard.json` | CloudWatch dashboard body |
| `tracking-trust-policy.json` | IAM trust policy for Lambda roles |
