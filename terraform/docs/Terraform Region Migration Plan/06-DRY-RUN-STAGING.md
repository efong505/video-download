# Phase 6: Dry Run — Deploy to Staging Region

## Objective

Deploy the entire platform to a non-production region (e.g., `us-west-2`) as a full end-to-end test. This validates that the parameterized Terraform config, Lambda deployment pipeline, and data migration all work correctly — without touching production.

## Risk Level: ZERO

This is a completely isolated deployment. It creates new resources in a new region with a separate Terraform state file. Production in `us-east-1` is untouched.

## Estimated Time: 4-6 hours

## Prerequisites

- Phase 1 complete (parameterized config)
- Phase 2 complete (CloudFront ACM multi-provider)
- Phase 3 complete (Lambda deployment pipeline)
- Phase 5 complete (SES verified in target region, production access granted)
- All changes committed to git

---

## Step 1: Create the Staging Environment

Create a new Terraform environment directory:

```
terraform/
├── environments/
│   ├── prod/              ← Current production (us-east-1)
│   │   ├── main.tf
│   │   └── variables.tf
│   └── us-west-2-test/    ← NEW: Staging test environment
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
```

### 1a. Copy main.tf

```bash
# From the terraform/environments directory:
mkdir us-west-2-test
copy prod\main.tf us-west-2-test\main.tf
copy prod\variables.tf us-west-2-test\variables.tf
```

### 1b. Create terraform.tfvars

Create `us-west-2-test/terraform.tfvars`:

```hcl
aws_region   = "us-west-2"
environment  = "staging-test"
```

### 1c. Update Backend Config

In `us-west-2-test/main.tf`, change the backend key so it uses a separate state file:

```hcl
backend "s3" {
  bucket       = "techcross-terraform-state"
  key          = "us-west-2-test/terraform.tfstate"    # Different key!
  region       = "us-east-1"                           # State stays in us-east-1
  encrypt      = true
  use_lockfile = true
  profile      = "ekewaka"
}
```

### 1d. Adjust Resource Names to Avoid Conflicts

Some resources have globally unique names. Update these in the test environment:

```hcl
# S3 bucket — must be globally unique
module "s3_videos" {
  source         = "../../modules/s3"
  bucket_name    = "my-video-downloads-bucket-west-test"  # Different name
  ...
}

# SNS email subscriptions — you probably don't want test alerts
# Comment out or use a test email address
module "sns_platform_critical_alerts" {
  ...
  email_addresses = ["hawaiianintucson@gmail.com"]  # Will get duplicate subscription emails
}

# API Gateway custom domains — skip for testing (or use test subdomains)
# Comment out api_domain_prod and api_domain_staging modules
# Comment out acm_api_prod and acm_api_staging modules
```

### 1e. Skip CloudFront for Testing

CloudFront distributions take 15-30 minutes to deploy and aren't needed for API testing. Comment out:
- `module "cloudfront_oac"`
- `module "cloudfront_distribution"`
- CloudFront-related outputs

You can test CloudFront separately later.

---

## Step 2: Initialize and Plan

```bash
cd terraform/environments/us-west-2-test

# Initialize with new backend
terraform init

# Plan — should show ALL resources as "will be created"
terraform plan -out=test-plan.tfplan
```

### Expected Plan Output

Everything should be `+ create`:
- ~48 Lambda functions
- ~54 DynamoDB tables
- 1 API Gateway + 17 integrations
- 5 SQS queues + 5 DLQs
- 4 SNS topics
- 1 S3 bucket
- 1 IAM role
- 3 Lambda layers
- 1 CloudWatch dashboard

**No destroys. No changes. Only creates.**

Review the plan carefully:
- All Lambda functions should reference the correct IAM role ARNs
- All DynamoDB tables should have correct schemas
- API Gateway integrations should reference the correct Lambda functions
- SQS queues should have correct visibility timeouts and retention periods

---

## Step 3: Apply

```bash
terraform apply test-plan.tfplan
```

This will take 5-15 minutes. Watch for errors.

### Common Issues and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `BucketAlreadyExists` | S3 bucket name taken | Use a different bucket name |
| `ResourceInUseException` | DynamoDB table exists | Someone created it manually; import or rename |
| `InvalidParameterValueException` on Lambda | Layer ARN doesn't exist in new region | Deploy layers first (Step 4) |
| `Certificate not found` | ACM cert doesn't exist in new region | Skip CloudFront or create cert first |

### If Lambda Layer ARNs Fail

If you parameterized layer ARNs (Phase 1, Step 5) using module references, Terraform creates the layers first. But the layers will be empty shells — you need to publish the actual layer code:

```bash
# Deploy layers to new region BEFORE applying (or after, then update functions)
python scripts/deploy-layers.py us-west-2 ekewaka
```

---

## Step 4: Deploy Lambda Code

After Terraform creates the Lambda function shells, deploy the actual code:

```bash
# Deploy all Lambda function code to the test region
python scripts/deploy-lambdas.py --region us-west-2 --profile ekewaka

# Verify all functions are active
python scripts/deploy-lambdas.py --region us-west-2 --profile ekewaka --verify-only
```

---

## Step 5: Migrate Test Data

You don't need full production data for testing. Options:

### Option A: Use a subset of production data

```bash
# Migrate just a few key tables with small datasets
python scripts/migrate-table.py --table articles --target-region us-west-2
python scripts/migrate-table.py --table users --target-region us-west-2
python scripts/migrate-table.py --table admin-users --target-region us-west-2
```

### Option B: Create test data

```bash
# Insert test records directly
aws dynamodb put-item --table-name articles \
  --item '{"article_id":{"S":"test-001"},"title":{"S":"Test Article"},"content":{"S":"Migration test content"}}' \
  --profile ekewaka --region us-west-2

aws dynamodb put-item --table-name users \
  --item '{"user_id":{"S":"test-user-001"},"email":{"S":"test@example.com"}}' \
  --profile ekewaka --region us-west-2
```

---

## Step 6: Test Everything

### 6a. Get the API Gateway URL

```bash
terraform output api_gateway_url
# Example: https://abc123def4.execute-api.us-west-2.amazonaws.com/prod
```

### 6b. Test Each Endpoint

```bash
# Set the base URL
set API=https://abc123def4.execute-api.us-west-2.amazonaws.com/prod

# Articles
curl %API%/articles

# Auth
curl -X POST %API%/auth -d "{\"action\":\"test\"}"

# News
curl %API%/news

# Comments
curl %API%/comments

# Prayer
curl %API%/prayer

# Events
curl %API%/events

# Notifications
curl %API%/notifications

# Admin
curl %API%/admin

# Contributors
curl %API%/contributors

# Resources
curl %API%/resources

# Videos
curl %API%/videos

# Tags
curl %API%/tags

# Fact-checks
curl %API%/fact-checks

# Forum (if applicable)
curl %API%/forum

# Business directory (if applicable)
curl %API%/businesses
```

### 6c. Test Email Flow

```bash
# Test email subscription
curl -X POST %API%/subscribe -d "{\"email\":\"test@example.com\",\"source\":\"migration-test\"}"

# If SES is in production mode, test actual email sending
# Trigger a test email via the manual-email-sender Lambda
aws lambda invoke --function-name manual-email-sender \
  --payload '{"action":"test","email":"hawaiianintucson@gmail.com"}' \
  --profile ekewaka --region us-west-2 \
  response.json
```

### 6d. Test SQS Processing

```bash
# Send a test message to a queue
aws sqs send-message \
  --queue-url https://sqs.us-west-2.amazonaws.com/371751795928/analytics-queue \
  --message-body '{"test":"migration-verification"}' \
  --profile ekewaka --region us-west-2

# Check if the message was processed (check DLQ for failures)
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-west-2.amazonaws.com/371751795928/analytics-dlq \
  --attribute-names ApproximateNumberOfMessages \
  --profile ekewaka --region us-west-2
```

### 6e. Test SNS Notifications

```bash
# Publish a test message to the critical alerts topic
aws sns publish \
  --topic-arn arn:aws:sns:us-west-2:371751795928:platform-critical-alerts \
  --message "Migration test alert from us-west-2" \
  --profile ekewaka --region us-west-2

# Check your email for the notification
```

### 6f. Test CloudWatch Dashboard

```bash
terraform output dashboard_url
# Open in browser — verify metrics are being collected
```

---

## Step 7: Document Results

Create a test results log:

```markdown
# Dry Run Test Results — us-west-2

## Date: [DATE]

### Infrastructure Deployment
- [ ] Terraform apply succeeded: YES/NO
- [ ] Total resources created: ___
- [ ] Errors during apply: ___

### Lambda Functions
- [ ] All 48 functions created: YES/NO
- [ ] Code deployed to all functions: YES/NO
- [ ] Functions responding: YES/NO
- [ ] Failed functions: [list]

### API Gateway
- [ ] All endpoints responding: YES/NO
- [ ] Failed endpoints: [list]
- [ ] Response times acceptable: YES/NO

### DynamoDB
- [ ] All tables created: YES/NO
- [ ] Test data accessible: YES/NO
- [ ] GSIs working: YES/NO

### Email (SES)
- [ ] Test email sent: YES/NO
- [ ] Email received: YES/NO
- [ ] Tracking pixel loaded: YES/NO
- [ ] Click tracking worked: YES/NO

### SQS
- [ ] Messages processed: YES/NO
- [ ] DLQ empty (no failures): YES/NO

### SNS
- [ ] Alert received: YES/NO

### Issues Found
1. [Issue description + fix]
2. [Issue description + fix]
```

---

## Step 8: Tear Down

After testing is complete, destroy the test environment:

```bash
cd terraform/environments/us-west-2-test

# Destroy all resources
terraform destroy

# Verify nothing remains
aws dynamodb list-tables --profile ekewaka --region us-west-2
aws lambda list-functions --profile ekewaka --region us-west-2
```

### Clean Up State

```bash
# The state file in S3 can be left (it's empty after destroy)
# Or delete it:
aws s3 rm s3://techcross-terraform-state/us-west-2-test/terraform.tfstate --profile ekewaka
```

### Clean Up Test Data

If you migrated production data for testing:
- The `terraform destroy` already deleted the DynamoDB tables (and their data)
- Delete the test S3 bucket if created:
  ```bash
  aws s3 rb s3://my-video-downloads-bucket-west-test --force --profile ekewaka
  ```

---

## What Success Looks Like

After this phase, you should have confidence that:

1. **Terraform config is region-portable** — `terraform apply` in a new region creates everything correctly
2. **Lambda deployment pipeline works** — All 48 functions get their code deployed
3. **API Gateway routes work** — All endpoints respond correctly
4. **Data migration works** — Tables can be populated and queried
5. **Email sending works** — SES sends, tracks, and handles bounces
6. **No hardcoded region references remain** — Everything adapts to the target region

If any of these fail, fix the issue and re-test before proceeding to Phase 7 (production cutover).

---

## Checklist

- [ ] Test environment directory created (`us-west-2-test/`)
- [ ] Backend config uses separate state key
- [ ] Resource name conflicts resolved (S3 bucket, etc.)
- [ ] `terraform init` succeeded
- [ ] `terraform plan` shows only creates (no changes/destroys)
- [ ] `terraform apply` succeeded
- [ ] Lambda layers deployed to new region
- [ ] Lambda function code deployed to all 48 functions
- [ ] All API Gateway endpoints tested and responding
- [ ] DynamoDB tables created with correct schemas
- [ ] Test data migrated or created
- [ ] Email sending tested (if SES production access granted)
- [ ] SQS message processing verified
- [ ] SNS notifications received
- [ ] Test results documented
- [ ] `terraform destroy` completed — all resources removed
- [ ] Test environment cleaned up
- [ ] Issues found are documented and fixes planned
- [ ] Git commit: "Phase 6: Dry run test results and fixes"
