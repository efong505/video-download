# Shopping System - Quick Start Guide

## Prerequisites

✅ AWS CLI configured with credentials  
✅ PowerShell 7+ installed  
✅ Access to AWS Console  
✅ Region set to us-east-1  

---

## Week 1: Get Started in 10 Minutes

### Step 1: Navigate to Scripts Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts
```

### Step 2: Create SQS Queues (~2 minutes)
```powershell
.\1-create-sqs-queues.ps1
```

**What this does:**
- Creates 4 main queues (order, payment, email, inventory)
- Creates 4 dead letter queues (DLQs)
- Configures retry logic (3 attempts)
- Sets appropriate timeouts

**Expected output:**
```
Creating SQS Queues for Shopping System...
Creating Dead Letter Queues...
Creating order-processing-dlq...
Creating payment-processing-dlq...
...
✅ All SQS queues created successfully!
```

---

### Step 3: Create DynamoDB Tables (~3 minutes)
```powershell
.\2-create-dynamodb-tables.ps1
```

**What this does:**
- Creates Products table (with 3 indexes)
- Creates Orders table (with 3 indexes)
- Creates Cart table (with TTL)
- Creates Reviews table (with 2 indexes)
- Waits for tables to become active

**Expected output:**
```
Creating DynamoDB Tables for Shopping System...
Creating Products table...
Creating Orders table...
...
✅ All tables are now active!
```

---

### Step 4: Test Infrastructure (~30 seconds)
```powershell
.\3-test-infrastructure.ps1
```

**What this does:**
- Verifies all 8 SQS queues exist
- Verifies all 4 DynamoDB tables are active
- Sends test message to queue
- Receives and deletes test message

**Expected output:**
```
Testing Shopping System Infrastructure...
Testing SQS Queues...
  ✅ order-processing-queue exists
  ✅ order-processing-dlq exists
  ...
Testing DynamoDB Tables...
  ✅ Products is ACTIVE
  ✅ Orders is ACTIVE
  ...
✅ ALL TESTS PASSED - Infrastructure is ready!
```

---

### Step 5: Update Cache Monitor (~30 seconds)
```powershell
.\4-update-cache-monitor.ps1
```

**What this does:**
- Updates auto-cache-monitor Lambda to include Shopping tables
- Monitors combined traffic (main platform + Shopping)
- Auto-enables ElastiCache when traffic reaches 2M reads/day
- Auto-enables API Gateway cache at 500K requests/day

**Expected output:**
```
Updating auto-cache-monitor Lambda with Shopping tables...
Creating deployment package...
Updating Lambda function...
✅ Lambda updated successfully!
✅ Auto-cache-monitor now monitors Shopping tables!
```

**Key benefit:** Zero manual monitoring - caching auto-enables when traffic justifies cost.

---

### Step 6: Monitor Queues (Optional)
```powershell
.\monitor-shopping-queues.ps1
```

**What this does:**
- Shows real-time queue depths
- Shows in-flight messages
- Alerts if DLQ has messages
- Refreshes every 5 seconds

**Press Ctrl+C to exit**

---

## Verify in AWS Console

### SQS Queues
1. Go to: https://console.aws.amazon.com/sqs/
2. Region: us-east-1
3. You should see 8 queues:
   - order-processing-queue
   - order-processing-dlq
   - payment-processing-queue
   - payment-processing-dlq
   - email-notification-queue
   - email-notification-dlq
   - inventory-update-queue
   - inventory-update-dlq

### DynamoDB Tables
1. Go to: https://console.aws.amazon.com/dynamodb/
2. Region: us-east-1
3. You should see 4 tables:
   - Products
   - Orders
   - Cart
   - Reviews

---

## What's Next?

### Week 2: ElastiCache (Deferred)
ElastiCache setup is deferred until traffic reaches:
- 10,000 DynamoDB reads/day
- OR response times exceed 500ms

**Check if caching is needed:**
```powershell
cd ..\..\Architecture-Improvements\scripts
.\monitor-cache-threshold.ps1
```

### Week 3: Lambda Functions
Implement Lambda functions with:
- SQS integration
- Circuit breakers
- Rate limiting

### Week 4: Frontend Pages
Build shopping pages:
- Product catalog
- Shopping cart
- Checkout

---

## Troubleshooting

### "Queue already exists" Error
```powershell
# Delete existing queues
$queues = @("order-processing-queue", "order-processing-dlq", "payment-processing-queue", "payment-processing-dlq", "email-notification-queue", "email-notification-dlq", "inventory-update-queue", "inventory-update-dlq")
foreach ($q in $queues) {
    $url = aws sqs get-queue-url --queue-name $q --query 'QueueUrl' --output text
    aws sqs delete-queue --queue-url $url
}

# Re-run creation script
.\1-create-sqs-queues.ps1
```

### "Table already exists" Error
```powershell
# Delete existing tables
$tables = @("Products", "Orders", "Cart", "Reviews")
foreach ($t in $tables) {
    aws dynamodb delete-table --table-name $t
}

# Wait 1 minute for deletion
Start-Sleep -Seconds 60

# Re-run creation script
.\2-create-dynamodb-tables.ps1
```

### "Access Denied" Error
```powershell
# Check AWS credentials
aws sts get-caller-identity

# Verify region
aws configure get region

# Should return: us-east-1
```

---

## Cost Tracking

### Week 1 Costs
- **SQS:** $0 (free tier: 1M requests/month)
- **DynamoDB:** $0 (free tier: 25 GB storage)
- **Total:** $0/month

### Projected Production Costs
- **SQS:** ~$2/month
- **DynamoDB:** ~$3/month (with caching)
- **ElastiCache:** ~$15/month (when needed)
- **API Gateway Cache:** ~$10/month (when needed)
- **Total:** ~$5-30/month depending on traffic

---

## Success Checklist

Week 1 is complete when:
- [x] All 8 SQS queues created
- [x] All 4 DynamoDB tables active
- [x] Test script passes all checks
- [x] No errors in AWS Console
- [x] Monitor script shows healthy queues

---

## Support

**Documentation:**
- SHOPPING_SYSTEM_PLAN.md - Complete implementation plan
- ARCHITECTURE_REQUIREMENTS.md - Mandatory architecture patterns
- TRACKING_SYSTEM_SPECS.md - Technical specifications
- IMPLEMENTATION_PROGRESS.md - Progress tracker

**Scripts:**
- scripts/README.md - Detailed script documentation
- scripts/1-create-sqs-queues.ps1 - SQS setup
- scripts/2-create-dynamodb-tables.ps1 - DynamoDB setup
- scripts/3-test-infrastructure.ps1 - Testing
- scripts/monitor-shopping-queues.ps1 - Monitoring

**Questions?**
- Check AWS Console for error messages
- Review CloudWatch Logs
- Verify IAM permissions
- Check scripts/README.md for troubleshooting

---

## Ready to Start?

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts
.\1-create-sqs-queues.ps1
```

**Let's build this! 🚀**
