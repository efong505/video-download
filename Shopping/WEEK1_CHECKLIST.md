# Week 1 Checklist: Infrastructure Setup

**Estimated Time:** 10 minutes  
**Difficulty:** Easy  
**Cost:** $0 (free tier)

---

## Pre-Flight Check

Before starting, verify:

- [ ] AWS CLI installed and configured
- [ ] PowerShell 7+ installed
- [ ] AWS credentials working: `aws sts get-caller-identity`
- [ ] Region set to us-east-1: `aws configure get region`
- [ ] Internet connection stable

---

## Step 1: Navigate to Scripts Directory

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\Shopping\scripts
```

- [ ] Confirmed in correct directory
- [ ] Can see script files: `ls`

---

## Step 2: Create SQS Queues (~2 minutes)

```powershell
.\1-create-sqs-queues.ps1
```

**Watch for:**
- [ ] "Creating Dead Letter Queues..." message
- [ ] "Creating Main Queues..." message
- [ ] "✅ All SQS queues created successfully!" message
- [ ] No error messages

**If errors occur:**
- Check AWS credentials
- Verify region is us-east-1
- Check for existing queues in AWS Console

---

## Step 3: Create DynamoDB Tables (~3 minutes)

```powershell
.\2-create-dynamodb-tables.ps1
```

**Watch for:**
- [ ] "Creating Products table..." message
- [ ] "Creating Orders table..." message
- [ ] "Creating Cart table..." message
- [ ] "Creating Reviews table..." message
- [ ] "Waiting for tables to become active..." message
- [ ] "✅ All tables are now active!" message
- [ ] No error messages

**If errors occur:**
- Check for existing tables in AWS Console
- Verify sufficient IAM permissions
- Wait 1 minute and retry

---

## Step 4: Test Infrastructure (~30 seconds)

```powershell
.\3-test-infrastructure.ps1
```

**Watch for:**
- [ ] "Testing SQS Queues..." section
- [ ] 8 green checkmarks (✅) for queues
- [ ] "Testing DynamoDB Tables..." section
- [ ] 4 green checkmarks (✅) for tables
- [ ] "Testing SQS Message Send..." section
- [ ] "✅ Test message sent successfully"
- [ ] "✅ Test message received and deleted"
- [ ] "✅ ALL TESTS PASSED - Infrastructure is ready!"

**If any test fails:**
- Review error message
- Check AWS Console for resource status
- Re-run creation scripts if needed

---

## Step 5: Update Cache Monitor (~30 seconds)

```powershell
.\4-update-cache-monitor.ps1
```

**Watch for:**
- [ ] "Creating deployment package..." message
- [ ] "Updating Lambda function..." message
- [ ] "✅ Lambda updated successfully!" message
- [ ] "✅ Lambda test successful!" message
- [ ] "✅ Auto-cache-monitor now monitors Shopping tables!" message
- [ ] List of monitored tables displayed
- [ ] Thresholds displayed (2M reads, 500K requests)

**What this does:**
- Updates existing auto-cache-monitor Lambda
- Adds Shopping tables to monitoring list
- Tracks combined traffic across all tables
- Auto-enables caching when thresholds reached

**If errors occur:**
- Verify auto-cache-monitor Lambda exists
- Check Lambda execution permissions
- Verify you're in correct directory

---

## Step 6: Verify in AWS Console

### SQS Queues
- [ ] Go to: https://console.aws.amazon.com/sqs/
- [ ] Region: us-east-1 (top right)
- [ ] See 8 queues total
- [ ] All queues show "Available" status
- [ ] No messages in any DLQ

**Expected queues:**
- order-processing-queue
- order-processing-dlq
- payment-processing-queue
- payment-processing-dlq
- email-notification-queue
- email-notification-dlq
- inventory-update-queue
- inventory-update-dlq

### DynamoDB Tables
- [ ] Go to: https://console.aws.amazon.com/dynamodb/
- [ ] Region: us-east-1 (top right)
- [ ] See 4 tables total
- [ ] All tables show "Active" status
- [ ] Products table has 3 indexes
- [ ] Orders table has 3 indexes
- [ ] Cart table has TTL enabled
- [ ] Reviews table has 2 indexes

**Expected tables:**
- Products
- Orders
- Cart
- Reviews

---

## Step 7: Monitor Queues (Optional)

```powershell
.\monitor-shopping-queues.ps1
```

**Watch for:**
- [ ] Real-time queue status display
- [ ] All queues show 0 visible messages
- [ ] All queues show 0 in-flight messages
- [ ] All DLQs show 0 messages
- [ ] Green checkmarks (✅) for all DLQs
- [ ] Screen refreshes every 5 seconds

**Press Ctrl+C to exit**

---

## Step 8: Update Progress Tracker

```powershell
# Open in editor
code ..\IMPLEMENTATION_PROGRESS.md
```

- [ ] Mark Week 1 tasks as complete
- [ ] Update completion date
- [ ] Update overall progress percentage
- [ ] Save file

---

## Step 9: Document Completion

Record the following information:

**Completion Date:** _______________

**SQS Queue URLs:**
```powershell
# Run this to get URLs
aws sqs list-queues --region us-east-1
```
- [ ] Saved queue URLs for reference

**DynamoDB Table ARNs:**
```powershell
# Run this to get ARNs
aws dynamodb list-tables --region us-east-1
```
- [ ] Saved table names for reference

**Time Taken:** _______________ minutes

**Issues Encountered:** 
- [ ] None
- [ ] Minor (resolved)
- [ ] Major (document below)

**Notes:**
_______________________________________
_______________________________________
_______________________________________

---

## Success Criteria

Week 1 is complete when ALL of these are true:

- [x] All 8 SQS queues created
- [x] All 4 DynamoDB tables active
- [x] Test script passes 100%
- [x] No errors in AWS Console
- [x] Monitor script shows healthy queues
- [x] Progress tracker updated
- [x] Completion documented

---

## What's Next?

### Immediate Next Steps:
1. [ ] Review Week 1 Summary (WEEK1_SUMMARY.md)
2. [ ] Understand what was built and why
3. [ ] Familiarize yourself with AWS Console views

### Week 2 Preparation:
1. [ ] Review SHOPPING_SYSTEM_PLAN.md (Week 2 section)
2. [ ] Check if ElastiCache is needed (run monitor-cache-threshold.ps1)
3. [ ] If traffic is low, proceed to Week 3 (Lambda functions)

### Optional:
1. [ ] Read ARCHITECTURE_REQUIREMENTS.md
2. [ ] Review TRACKING_SYSTEM_SPECS.md
3. [ ] Explore AWS Console features

---

## Troubleshooting

### Script Won't Run
```powershell
# Check execution policy
Get-ExecutionPolicy

# If Restricted, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Queue Already Exists" Error
```powershell
# Delete existing queues
.\rollback-week1.ps1

# Wait 1 minute
Start-Sleep -Seconds 60

# Re-run creation
.\1-create-sqs-queues.ps1
```

### "Table Already Exists" Error
```powershell
# Delete existing tables
aws dynamodb delete-table --table-name Products
aws dynamodb delete-table --table-name Orders
aws dynamodb delete-table --table-name Cart
aws dynamodb delete-table --table-name Reviews

# Wait 1 minute
Start-Sleep -Seconds 60

# Re-run creation
.\2-create-dynamodb-tables.ps1
```

### "Access Denied" Error
```powershell
# Verify credentials
aws sts get-caller-identity

# Check IAM permissions
# Need: SQS full access, DynamoDB full access
```

---

## Rollback (If Needed)

To completely remove Week 1 infrastructure:

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

**Time to rollback:** ~2 minutes  
**Data loss:** None (no production data yet)

---

## Support

**Documentation:**
- QUICK_START.md - Quick start guide
- WEEK1_SUMMARY.md - What we built and why
- scripts/README.md - Script documentation
- SHOPPING_SYSTEM_PLAN.md - Complete plan

**AWS Console:**
- SQS: https://console.aws.amazon.com/sqs/
- DynamoDB: https://console.aws.amazon.com/dynamodb/
- CloudWatch: https://console.aws.amazon.com/cloudwatch/

**Questions?**
- Check AWS Console for error messages
- Review CloudWatch Logs
- Verify IAM permissions
- Check scripts/README.md troubleshooting section

---

## Completion Sign-Off

**I confirm that:**
- [ ] All scripts ran successfully
- [ ] All tests passed
- [ ] AWS Console shows all resources
- [ ] No errors or warnings
- [ ] Progress tracker updated
- [ ] Ready for Week 2

**Signature:** _______________  
**Date:** _______________

---

**Congratulations on completing Week 1! 🎉**

You've successfully set up enterprise-grade infrastructure for the Shopping System. This foundation will support all future development.

**Next:** Review WEEK1_SUMMARY.md to understand what you built and why.
