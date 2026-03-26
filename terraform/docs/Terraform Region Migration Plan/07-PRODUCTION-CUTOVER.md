# Phase 7: Production Cutover

## Objective

Execute the actual migration of the Christian Conservative Platform from `us-east-1` to the target region. This is the real deal — production traffic will be redirected to the new region.

## Risk Level: MEDIUM

Production data and live traffic are involved. However, the rollback plan is straightforward (DNS revert), and the old region remains intact until explicitly decommissioned.

## Estimated Time: 2-4 hours for cutover + 48 hours monitoring before decommission

## Prerequisites

- **ALL previous phases complete and tested:**
  - Phase 1: Config parameterized ✅
  - Phase 2: CloudFront ACM multi-provider ✅
  - Phase 3: Lambda deployment pipeline tested ✅
  - Phase 4: Data migration strategy tested ✅
  - Phase 5: SES production access granted in target region ✅
  - Phase 6: Dry run successful, all issues resolved ✅
- Git working tree clean, all changes committed
- Maintenance window communicated to users (if applicable)
- Team members available for monitoring

---

## Pre-Migration Checklist (1 Week Before)

### Data Replication

- [ ] DynamoDB Global Tables enabled on ALL Tier 1 tables
- [ ] All replicas showing `ACTIVE` status
- [ ] Item counts match between regions (approximate is fine)
- [ ] Verify replication lag is acceptable (typically < 1 second)

```bash
# Verify all Tier 1 replicas
python scripts/migrate-data.py --target-region us-west-2 --phase verify-replication
```

### SES Readiness

- [ ] Domain verified in target region
- [ ] DKIM status: SUCCESS
- [ ] Production access: GRANTED
- [ ] Test email sent successfully from target region
- [ ] Suppression list migrated

### DNS Preparation

- [ ] Lower Route53 TTL on API records to 60 seconds (speeds up cutover)

```bash
# Check current TTL
aws route53 list-resource-record-sets \
  --hosted-zone-id Z0541028204EB3LCQMNQD \
  --profile ekewaka \
  --query "ResourceRecordSets[?Name=='api.christianconservativestoday.com.'].TTL"

# If TTL is high (e.g., 300), lower it to 60 at least 24 hours before cutover
# This ensures the old TTL has expired by migration time
```

### Backup

- [ ] Terraform state backed up:
  ```bash
  cd terraform/environments/prod
  terraform state pull > backup-pre-migration-$(date +%Y%m%d).tfstate
  ```
- [ ] Git tagged:
  ```bash
  git tag pre-region-migration
  git push origin pre-region-migration
  ```

---

## Migration Day — Hour-by-Hour Runbook

### T-60 min: Final Preparations

```bash
# 1. Pull latest state
cd terraform/environments/prod
terraform state pull > backup-final.tfstate

# 2. Verify Global Tables replication is current
python scripts/migrate-data.py --target-region us-west-2 --phase verify-replication

# 3. Verify SES is ready
aws sesv2 get-account --profile ekewaka --region us-west-2 \
  --query "{ProductionAccess:ProductionAccessEnabled,SendingEnabled:SendingEnabled}"

# 4. Verify Lambda deployment script is ready
python scripts/deploy-lambdas.py --region us-west-2 --profile ekewaka --dry-run
```

### T-30 min: Enable Maintenance Mode (Optional)

If you want zero user confusion during cutover:

```bash
# Option 1: CloudFront custom error page
# Upload a maintenance.html to S3 and configure CloudFront to serve it

# Option 2: API Gateway returns maintenance response
# Deploy a simple Lambda that returns {"status": "maintenance", "message": "..."}
# Point all API routes to it temporarily
```

**Alternative: Skip maintenance mode.** The cutover is fast enough (< 5 minutes of DNS propagation) that most users won't notice. Some requests during propagation may hit the old region (which still works).

### T-0: Begin Cutover

#### Step 1: Migrate Tier 2 Data (5-15 min)

Tier 1 is already synced via Global Tables. Migrate Tier 2 now:

```bash
python scripts/migrate-data.py --target-region us-west-2 --phase migrate-tier2
```

#### Step 2: Deploy Infrastructure to New Region (10-15 min)

Update the prod environment to target the new region:

**Option A: Update variables (if using terraform.tfvars)**
```hcl
# terraform/environments/prod/terraform.tfvars
aws_region = "us-west-2"
```

**Option B: Create new environment directory**

If you prefer to keep the old config intact:
```bash
# Copy prod to new directory
mkdir terraform/environments/prod-west
copy terraform/environments/prod/*.tf terraform/environments/prod-west/
# Update backend key and region variable
```

```bash
# Plan first — review carefully
terraform plan -out=migration.tfplan

# Apply
terraform apply migration.tfplan
```

**What happens:**
- Terraform creates ALL resources fresh in `us-west-2`
- The old `us-east-1` resources are NOT affected (different state file if using Option B, or Terraform sees them as new resources if using Option A with a new state key)

**Important:** If using Option A (same state file), Terraform will try to DESTROY us-east-1 resources and CREATE us-west-2 resources. This is dangerous. **Use Option B (separate state file) for safety.**

#### Step 3: Deploy Lambda Code (10-20 min)

```bash
# Deploy all function code
python scripts/deploy-lambdas.py --region us-west-2 --profile ekewaka

# Verify all functions are active
python scripts/deploy-lambdas.py --region us-west-2 --profile ekewaka --verify-only
```

#### Step 4: Deploy Lambda Layers (5 min)

```bash
python scripts/deploy-layers.py us-west-2 ekewaka
```

#### Step 5: Smoke Test New Region (10 min)

```bash
# Get the new API Gateway URL
terraform output api_gateway_url
# Example: https://xyz789.execute-api.us-west-2.amazonaws.com/prod

# Test critical endpoints
set API=https://xyz789.execute-api.us-west-2.amazonaws.com/prod
curl %API%/articles
curl %API%/auth
curl %API%/news
curl %API%/prayer
curl %API%/events
curl %API%/comments

# Test email
aws lambda invoke --function-name manual-email-sender \
  --payload '{"action":"test","email":"hawaiianintucson@gmail.com"}' \
  --profile ekewaka --region us-west-2 response.json
cat response.json
```

**If any endpoint fails: STOP. Fix the issue before proceeding to DNS cutover.**

#### Step 6: DNS Cutover (2 min)

This is the point of no return (though easily reversible).

```bash
# Update API Gateway custom domain to point to new region
# The Terraform apply in Step 2 should have created the custom domain mapping
# Verify:
aws apigateway get-domain-name \
  --domain-name api.christianconservativestoday.com \
  --profile ekewaka --region us-west-2

# If Route53 records need manual update:
# The ALIAS record for api.christianconservativestoday.com should point to
# the new API Gateway's regional domain name
```

If Terraform manages Route53 records (which it should after Phase 1), the `terraform apply` in Step 2 already updated them.

**Verify DNS is resolving to new region:**
```bash
nslookup api.christianconservativestoday.com
# Should show the new API Gateway endpoint
```

#### Step 7: Disable Maintenance Mode

If you enabled maintenance mode, disable it now.

#### Step 8: Verify Live Traffic (15 min)

```bash
# Test via the custom domain (not the API Gateway URL)
curl https://api.christianconservativestoday.com/articles
curl https://api.christianconservativestoday.com/auth
curl https://api.christianconservativestoday.com/news

# Check CloudWatch in new region for incoming requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value=ministry-platform-api \
  --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Sum \
  --profile ekewaka --region us-west-2
```

---

## Post-Cutover Monitoring (48 Hours)

### Hour 1-4: Active Monitoring

Watch for:
- API Gateway 5XX errors in CloudWatch
- Lambda errors/throttles
- SQS DLQ messages (indicates processing failures)
- SES bounce rate
- User reports of issues

```bash
# Quick health check script — run every 15 minutes
echo "=== API Gateway ===" && \
curl -s -o /dev/null -w "%%{http_code}" https://api.christianconservativestoday.com/articles && \
echo "" && \
echo "=== Lambda Errors ===" && \
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda --metric-name Errors \
  --start-time $(date -u -d '15 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 900 --statistics Sum \
  --profile ekewaka --region us-west-2 \
  --query "Datapoints[0].Sum" && \
echo "" && \
echo "=== DLQ Messages ===" && \
for q in analytics-dlq email-dlq video-processing-dlq thumbnail-generation-dlq; do \
  echo -n "$q: " && \
  aws sqs get-queue-attributes \
    --queue-url https://sqs.us-west-2.amazonaws.com/371751795928/$q \
    --attribute-names ApproximateNumberOfMessages \
    --profile ekewaka --region us-west-2 \
    --query "Attributes.ApproximateNumberOfMessages" --output text; \
done
```

### Hour 4-48: Passive Monitoring

- Check CloudWatch dashboard periodically
- Monitor email delivery rates
- Watch for user-reported issues
- Keep old region running as fallback

---

## Rollback Plan

### If Issues Found BEFORE DNS Cutover (Step 6)

**Action:** Simply don't cut over. The old region is untouched and still serving traffic.

```bash
# Fix the issue in the new region
# Re-test
# Try cutover again when ready
```

### If Issues Found AFTER DNS Cutover

**Action:** Revert DNS to point back to the old region.

```bash
# Option 1: If Terraform manages Route53
# Revert the region variable and apply
# terraform.tfvars: aws_region = "us-east-1"
terraform apply

# Option 2: Manual Route53 update (faster)
# Change the ALIAS record for api.christianconservativestoday.com
# back to the us-east-1 API Gateway endpoint
```

**DNS propagation time:** With TTL set to 60 seconds (from pre-migration prep), most clients will see the change within 1-2 minutes.

### If Data Issues Found

If data was written to the new region during the brief cutover window and you need to roll back:

1. Global Tables are still syncing — data written to us-west-2 will replicate back to us-east-1
2. If Global Tables were already disabled, you may need to manually migrate the delta

---

## Decommission Old Region (After 48 Hours)

Only proceed when you're confident the new region is stable.

### Step 1: Disable Global Tables Replication

```bash
# For each table with Global Tables enabled:
aws dynamodb update-table \
  --table-name articles \
  --replica-updates "Delete={RegionName=us-east-1}" \
  --profile ekewaka --region us-west-2
```

### Step 2: Delete Old Region Resources

**Option A: If using separate state files**
```bash
cd terraform/environments/prod  # Old us-east-1 environment
terraform destroy
```

**Option B: Manual cleanup**
```bash
# Delete Lambda functions
aws lambda list-functions --profile ekewaka --region us-east-1 \
  --query "Functions[].FunctionName" --output text | \
  xargs -n1 aws lambda delete-function --function-name --profile ekewaka --region us-east-1

# Delete DynamoDB tables (CAREFUL — verify Global Tables replication is disabled first!)
# Delete SQS queues
# Delete SNS topics
# Delete API Gateway
# etc.
```

**Recommendation:** Use Option A (Terraform destroy). It's safer and more complete.

### Step 3: Clean Up

- [ ] Delete old state file from S3 (or archive it)
- [ ] Remove old environment directory from git
- [ ] Update documentation to reflect new region
- [ ] Update memory bank / project notes
- [ ] Update any CI/CD pipelines that reference the old region

---

## Complete Migration Timeline

```
Week Before:
├── Day -7: Enable Global Tables on Tier 1 tables
├── Day -7: Lower DNS TTL to 60 seconds
├── Day -3: Verify all replicas ACTIVE
├── Day -2: Final dry run in test environment
└── Day -1: Communicate maintenance window

Migration Day:
├── T-60 min: Final verifications
├── T-30 min: Enable maintenance mode (optional)
├── T-0:     Begin cutover
│   ├── Migrate Tier 2 data (15 min)
│   ├── Deploy infrastructure (15 min)
│   ├── Deploy Lambda code (20 min)
│   ├── Smoke test (10 min)
│   ├── DNS cutover (2 min)
│   └── Verify live traffic (15 min)
├── T+1 hr:  Active monitoring
└── T+4 hr:  Passive monitoring begins

Post-Migration:
├── Day +1: Continue monitoring
├── Day +2: Confidence check — all metrics normal?
├── Day +3: Disable Global Tables replication
├── Day +3: Destroy old region resources
└── Day +7: Final cleanup and documentation
```

---

## Emergency Contacts and Escalation

| Scenario | Action | Time to Resolve |
|----------|--------|-----------------|
| API returning 5XX | Check Lambda logs in new region | 5-15 min |
| Emails not sending | Verify SES config, check Lambda logs | 10-30 min |
| Data missing | Check Global Tables replication status | 5-10 min |
| Complete outage | Revert DNS to old region | 1-2 min |
| State file corrupted | Restore from S3 versioned backup | 5 min |

---

## Checklist

### Pre-Cutover
- [ ] All 6 previous phases complete and tested
- [ ] Global Tables replication active on all Tier 1 tables
- [ ] SES production access confirmed in target region
- [ ] DNS TTL lowered to 60 seconds (24+ hours ago)
- [ ] State file backed up
- [ ] Git tagged `pre-region-migration`
- [ ] Team notified of maintenance window

### During Cutover
- [ ] Tier 2 data migrated
- [ ] Terraform apply succeeded in new region
- [ ] Lambda layers deployed
- [ ] Lambda function code deployed (all 48)
- [ ] All API endpoints smoke-tested
- [ ] DNS cutover executed
- [ ] Live traffic verified in new region
- [ ] Maintenance mode disabled

### Post-Cutover
- [ ] 4 hours of active monitoring — no critical issues
- [ ] 48 hours of passive monitoring — metrics normal
- [ ] Global Tables replication disabled
- [ ] Old region resources destroyed
- [ ] Old state file archived/deleted
- [ ] Documentation updated
- [ ] Git tagged `post-region-migration`
- [ ] Memory bank updated with new region info
