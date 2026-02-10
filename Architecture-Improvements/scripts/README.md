# Safe SQS Deployment Scripts

These scripts enable **zero-risk** SQS implementation with gradual rollout and easy rollback.

## Quick Start

```powershell
# 1. Create queues (no Lambda changes)
.\safe-sqs-deploy.ps1

# 2. Test queues work
.\test-sqs-integration.ps1

# 3. Enable SQS for one Lambda at a time
.\gradual-rollout.ps1 -Phase 1  # Thumbnail generator (safest)
# Wait 24 hours, monitor...

.\gradual-rollout.ps1 -Phase 2  # Video downloader
# Wait 24 hours, monitor...

.\gradual-rollout.ps1 -Phase 3  # Digest generator
# Wait 24 hours, monitor...

.\gradual-rollout.ps1 -Phase 4  # Analytics

# 4. Check status anytime
.\gradual-rollout.ps1 -Phase status

# 5. Rollback if needed
.\rollback-sqs.ps1 -Function thumbnail-generator  # Rollback one
.\rollback-sqs.ps1 -Function all                  # Rollback all
.\rollback-sqs.ps1 -Function all -DeleteQueues    # Rollback + delete queues
```

---

## Scripts Overview

### 0. monitor-cache-threshold.ps1
**Purpose:** Automated monitoring to determine when caching becomes cost-effective  
**Risk:** Zero - read-only monitoring  
**Time:** 2 minutes  
**Frequency:** Run weekly or set up Task Scheduler

**Example:**
```powershell
# Check current traffic and get recommendations
.\monitor-cache-threshold.ps1
```

**What it does:**
- Checks last 24 hours of DynamoDB reads and API requests
- Calculates projected monthly costs with and without caching
- Alerts when traffic reaches 80% of threshold (warning)
- Recommends enabling caching when traffic reaches threshold:
  - ElastiCache: 10,000 DynamoDB reads/day
  - API Gateway Cache: 100,000 API requests/day
- Saves daily report for tracking trends
- Shows projected savings when caching is enabled

**Thresholds:**
- **ElastiCache:** Enable at 10K DynamoDB reads/day (saves money at this traffic level)
- **API Gateway Cache:** Enable at 100K API requests/day (saves money at this traffic level)
- **Warning:** Alert at 80% of threshold (8K reads or 80K requests)

**Output:**
- Current traffic levels
- Projected monthly costs (with and without caching)
- Clear recommendations (ENABLE NOW or Keep disabled)
- Percentage of threshold reached
- Daily report saved to file

### 1. safe-sqs-deploy.ps1
**Purpose:** Create SQS queues without modifying Lambda functions  
**Risk:** Zero - only creates infrastructure  
**Time:** 2 minutes  

**Options:**
- `-DryRun` - See what would be created without creating anything

**Example:**
```powershell
# Dry run first
.\safe-sqs-deploy.ps1 -DryRun

# Create for real
.\safe-sqs-deploy.ps1
```

**What it does:**
- Creates 4 dead-letter queues (DLQs)
- Creates 4 main queues with DLQ configuration
- Verifies queues exist
- Does NOT modify any Lambda functions

---

### 2. test-sqs-integration.ps1
**Purpose:** Test that queues work correctly  
**Risk:** Zero - only sends test messages  
**Time:** 1 minute  

**Example:**
```powershell
.\test-sqs-integration.ps1
```

**What it does:**
- Verifies all queues exist
- Sends test message to video-processing-queue
- Verifies message was queued
- Cleans up test message
- Does NOT modify any Lambda functions

---

### 3. gradual-rollout.ps1
**Purpose:** Enable SQS one Lambda at a time  
**Risk:** Low - gradual with verification between phases  
**Time:** 5 minutes per phase (+ 24 hours monitoring)  

**Phases:**
1. **Phase 1:** Thumbnail generator (lowest risk)
2. **Phase 2:** Video downloader (medium risk)
3. **Phase 3:** Digest generator (low risk)
4. **Phase 4:** Analytics (very low risk)

**Example:**
```powershell
# Start with safest Lambda
.\gradual-rollout.ps1 -Phase 1

# Monitor for 24 hours, then proceed
.\gradual-rollout.ps1 -Phase 2

# Check status anytime
.\gradual-rollout.ps1 -Phase status
```

**What it does:**
- Creates Lambda event source mapping to SQS queue
- Enables automatic message processing
- Provides verification checklist
- Recommends 24-hour monitoring between phases

---

### 4. rollback-sqs.ps1
**Purpose:** Remove SQS integration and revert to direct invocation  
**Risk:** Zero - restores original behavior  
**Time:** 2 minutes  

**Options:**
- `-Function <name>` - Rollback specific Lambda
- `-Function all` - Rollback all Lambdas
- `-DeleteQueues` - Also delete SQS queues

**Examples:**
```powershell
# Rollback one Lambda
.\rollback-sqs.ps1 -Function thumbnail-generator

# Rollback all Lambdas (keep queues)
.\rollback-sqs.ps1 -Function all

# Rollback all + delete queues
.\rollback-sqs.ps1 -Function all -DeleteQueues
```

**What it does:**
- Removes Lambda event source mappings
- Lambdas revert to direct invocation
- Optionally deletes SQS queues
- Site works exactly as before SQS

---

## Deployment Timeline

### Week 1: Infrastructure Setup
- **Day 1:** Run `safe-sqs-deploy.ps1` (2 min)
- **Day 1:** Run `test-sqs-integration.ps1` (1 min)
- **Day 1:** Review queues in AWS Console (10 min)

### Week 2: Phase 1 Rollout
- **Day 8:** Run `gradual-rollout.ps1 -Phase 1` (5 min)
- **Days 8-9:** Monitor CloudWatch logs (24 hours)
- **Day 9:** Check DLQ for failed messages

### Week 3: Phase 2 Rollout
- **Day 15:** Run `gradual-rollout.ps1 -Phase 2` (5 min)
- **Days 15-16:** Monitor video downloads (24 hours)
- **Day 16:** Verify no timeouts

### Week 4: Phases 3 & 4
- **Day 22:** Run `gradual-rollout.ps1 -Phase 3` (5 min)
- **Day 23:** Run `gradual-rollout.ps1 -Phase 4` (5 min)
- **Days 23-30:** Monitor all functions

**Total Time:** 30 minutes active work + monitoring

---

## Monitoring Checklist

After each phase:

### Check Queue Status
```powershell
# Check thumbnail-generation-queue
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/thumbnail-generation-queue --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check video-processing-queue
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-queue --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check email-queue
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/email-queue --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check analytics-queue
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/analytics-queue --attribute-names ApproximateNumberOfMessages --region us-east-1
```

### Check Dead Letter Queues
```powershell
# Check thumbnail-generation-dlq
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/thumbnail-generation-dlq --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check video-processing-dlq
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-dlq --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check email-dlq
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/email-dlq --attribute-names ApproximateNumberOfMessages --region us-east-1

# Check analytics-dlq
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/analytics-dlq --attribute-names ApproximateNumberOfMessages --region us-east-1
```

### CloudWatch Logs
```powershell
# View recent Lambda logs (last 1 hour)
aws logs tail /aws/lambda/thumbnail-generator --since 1h --region us-east-1
aws logs tail /aws/lambda/downloader --since 1h --region us-east-1
aws logs tail /aws/lambda/digest-generator --since 1h --region us-east-1
aws logs tail /aws/lambda/article-analysis --since 1h --region us-east-1

# Or use live-logs.ps1 for real-time monitoring
.\live-logs.ps1
```

### Verify Functionality
- **Phase 1:** Upload video, check thumbnail generated
  ```powershell
  # Check recent thumbnail-generator logs
  aws logs tail /aws/lambda/thumbnail-generator --since 10m --region us-east-1
  ```
- **Phase 2:** Download video, verify it appears in gallery
  ```powershell
  # Check recent downloader logs
  aws logs tail /aws/lambda/downloader --since 10m --region us-east-1
  ```
- **Phase 3:** Generate newsletter, check email sent
  ```powershell
  # Check recent digest-generator logs
  aws logs tail /aws/lambda/digest-generator --since 10m --region us-east-1
  ```
- **Phase 4:** View article, check analytics recorded
  ```powershell
  # Check recent article-analysis logs
  aws logs tail /aws/lambda/article-analysis --since 10m --region us-east-1
  ```

---

## Rollback Scenarios

### Scenario 1: Phase 1 has issues
```powershell
# Rollback thumbnail generator only
.\rollback-sqs.ps1 -Function thumbnail-generator

# Site continues working normally
# Other Lambdas unaffected
```

### Scenario 2: Phase 2 breaks video downloads
```powershell
# Rollback video downloader only
.\rollback-sqs.ps1 -Function downloader

# Thumbnails still use SQS (Phase 1)
# Video downloads revert to direct invocation
```

### Scenario 3: Complete rollback needed
```powershell
# Rollback everything
.\rollback-sqs.ps1 -Function all

# All Lambdas revert to direct invocation
# Queues remain (no cost if unused)
```

### Scenario 4: Start over completely
```powershell
# Rollback and delete everything
.\rollback-sqs.ps1 -Function all -DeleteQueues

# System exactly as before SQS implementation
# Can re-run safe-sqs-deploy.ps1 to try again
```

---

## Success Criteria

After full rollout (all 4 phases):

✅ **Functionality:**
- All features work as before
- No user-facing errors
- Video downloads complete successfully
- Thumbnails generate automatically

✅ **Performance:**
- No Lambda timeouts
- Messages processed within visibility timeout
- DLQs remain empty (no failed messages)

✅ **Monitoring:**
- CloudWatch logs show successful processing
- SQS metrics show messages in/out
- No error spikes in CloudWatch

✅ **Cost:**
- SQS costs ~$5/month
- Lambda costs unchanged or lower (fewer retries)

---

## Troubleshooting

### Issue: Queues not found
**Solution:** Run `.\safe-sqs-deploy.ps1` first

### Issue: Lambda can't send to queue
**Solution:** Check IAM permissions - Lambda needs `sqs:SendMessage`

### Issue: Messages stuck in queue
**Solution:** Check Lambda has event source mapping and is enabled

### Issue: Messages going to DLQ
**Solution:** Check CloudWatch logs for Lambda errors

### Issue: Want to start over
**Solution:** Run `.\rollback-sqs.ps1 -Function all -DeleteQueues`

---

## Cost Breakdown

**SQS Costs (estimated):**
- First 1M requests/month: Free
- After 1M: $0.40 per million requests
- Typical usage: ~500K requests/month = $0
- High usage: ~2M requests/month = $0.40

**Lambda Costs:**
- Unchanged (same number of invocations)
- May decrease (fewer failed retries)

**Total Additional Cost:** ~$0-5/month

---

## Next Steps

After successful SQS rollout:

1. Monitor for 1 week
2. Verify DLQs remain empty
3. Check CloudWatch metrics
4. **Run cache threshold monitoring weekly:**
   ```powershell
   .\monitor-cache-threshold.ps1
   ```
5. Enable caching only when traffic justifies cost:
   - ElastiCache: When reaching 10K DynamoDB reads/day
   - API Gateway Cache: When reaching 100K API requests/day
6. Proceed to Circuit Breakers and Rate Limiting (zero cost)
7. Read `03-CIRCUIT-BREAKERS.md` and `04-RATE-LIMITING.md`

---

## Support

If you encounter issues:
1. Check CloudWatch logs: `.\live-logs.ps1`
2. Check DLQs for failed messages
3. Run rollback script
4. Review this README
5. Check AWS Console for queue/Lambda status
