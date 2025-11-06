# Shopping System - Deployment Scripts

## Week 1: Infrastructure Setup (SQS + DynamoDB)

### Step 1: Create SQS Queues
```powershell
.\1-create-sqs-queues.ps1
```

**Creates:**
- 4 main queues (order, payment, email, inventory)
- 4 dead letter queues (DLQs)
- Configures retry logic (3 attempts before DLQ)
- Sets appropriate timeouts

**Time:** ~2 minutes

---

### Step 2: Create DynamoDB Tables
```powershell
.\2-create-dynamodb-tables.ps1
```

**Creates:**
- Products table (with 3 GSIs)
- Orders table (with 3 GSIs)
- Cart table (with TTL enabled)
- Reviews table (with 2 GSIs)

**Time:** ~3 minutes (includes waiting for tables to become active)

---

### Step 3: Test Infrastructure
```powershell
.\3-test-infrastructure.ps1
```

**Tests:**
- All SQS queues exist
- All DynamoDB tables are active
- Can send/receive messages
- Infrastructure is ready

**Time:** ~30 seconds

---

### Step 4: Update Cache Monitor
```powershell
.\4-update-cache-monitor.ps1
```

**Updates:**
- Adds Shopping tables to auto-cache-monitor Lambda
- Monitors combined traffic (main platform + Shopping)
- Auto-enables ElastiCache at 2M reads/day
- Auto-enables API Gateway cache at 500K requests/day

**Time:** ~30 seconds

---

### Step 5: Monitor Queues (Optional)
```powershell
.\monitor-shopping-queues.ps1
```

**Monitors:**
- Queue depths (visible messages)
- In-flight messages
- DLQ message counts
- Real-time updates every 5 seconds

**Usage:** Run in separate terminal, press Ctrl+C to exit

---

## Week 2: ElastiCache Setup (Deferred)

ElastiCache setup is deferred until traffic reaches:
- 10,000 DynamoDB reads/day
- OR when response times exceed 500ms

**Monitoring:**
```powershell
# Check if caching is justified
cd ..\..\Architecture-Improvements\scripts
.\monitor-cache-threshold.ps1
```

---

## Week 3: Lambda Functions

Scripts for Lambda deployment will be added in Week 3.

---

## Troubleshooting

### SQS Queue Creation Fails
```powershell
# Check AWS credentials
aws sts get-caller-identity

# Verify region
aws configure get region

# Delete and recreate
aws sqs delete-queue --queue-url <queue-url>
.\1-create-sqs-queues.ps1
```

### DynamoDB Table Creation Fails
```powershell
# Check if table already exists
aws dynamodb list-tables

# Delete existing table
aws dynamodb delete-table --table-name Products

# Recreate
.\2-create-dynamodb-tables.ps1
```

### Test Script Fails
```powershell
# Check queue URLs
aws sqs list-queues

# Check table status
aws dynamodb describe-table --table-name Products

# Verify permissions
aws iam get-user
```

---

## Cost Tracking

### Week 1 Costs
- SQS: $0 (free tier covers 1M requests/month)
- DynamoDB: $0 (free tier covers 25 GB storage)
- **Total: $0/month** (within free tier)

### Projected Costs (Production)
- SQS: ~$2/month
- DynamoDB: ~$3/month (with caching)
- **Total: ~$5/month** (before ElastiCache)

---

## Next Steps

After completing Week 1:

1. ✅ Verify all infrastructure in AWS Console
2. ✅ Run monitor script to confirm queues are working
3. ⏭️ Week 2: Set up ElastiCache (when traffic justifies)
4. ⏭️ Week 3: Implement Lambda functions
5. ⏭️ Week 4: Build frontend pages

---

## Rollback

If you need to remove everything:

```powershell
# Delete SQS queues
$queues = @("order-processing-queue", "order-processing-dlq", "payment-processing-queue", "payment-processing-dlq", "email-notification-queue", "email-notification-dlq", "inventory-update-queue", "inventory-update-dlq")
foreach ($q in $queues) {
    $url = aws sqs get-queue-url --queue-name $q --query 'QueueUrl' --output text
    aws sqs delete-queue --queue-url $url
}

# Delete DynamoDB tables
$tables = @("Products", "Orders", "Cart", "Reviews")
foreach ($t in $tables) {
    aws dynamodb delete-table --table-name $t
}
```

---

## Support

For issues or questions:
1. Check AWS Console for error messages
2. Review CloudWatch Logs
3. Verify IAM permissions
4. Check this README for troubleshooting steps
