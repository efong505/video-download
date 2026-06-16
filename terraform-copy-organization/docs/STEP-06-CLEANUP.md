# STEP 06: Cleanup

**Goal**: Remove all resources and prepare for next practice run

**Time**: 5-10 minutes

---

## Overview

You'll:
1. Review what will be destroyed
2. Destroy all infrastructure
3. Verify cleanup
4. Prepare for next practice run

---

## Step 6.1: Review Current State

```powershell
# Navigate to terraform directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform

# List all managed resources
terraform state list

# Expected output: 20+ resources
```

---

## Step 6.2: Plan Destruction

**Preview what will be destroyed WITHOUT actually destroying:**

```powershell
# Generate destruction plan
terraform plan -destroy

# Review the output carefully
# You should see all resources marked for destruction
```

**Review checklist**:
- [ ] All resources will be destroyed
- [ ] No resources will be kept
- [ ] Resource count matches what was created

---

## Step 6.3: Destroy Infrastructure

**This removes all resources from child account:**

```powershell
# Destroy all resources
terraform destroy

# Terraform will show the plan and ask for confirmation
# Type: yes

# Expected output:
# Destroy complete! Resources: 20+ destroyed.
```

**Destruction time**: 2-3 minutes

---

## Step 6.4: Verify Cleanup

### Verify IAM Role Deleted

```powershell
# Try to get role (should fail)
aws iam get-role `
    --role-name lambda-execution-role-tutorial `
    --profile child-account

# Expected: Error - NoSuchEntity
```

### Verify S3 Bucket Deleted

```powershell
# Try to list bucket (should fail)
aws s3 ls s3://infra-copy-tutorial-* --profile child-account

# Expected: Error - NoSuchBucket
```

### Verify DynamoDB Table Deleted

```powershell
# Try to describe table (should fail)
aws dynamodb describe-table `
    --table-name sample-table-tutorial `
    --profile child-account

# Expected: Error - ResourceNotFoundException
```

### Verify Lambda Function Deleted

```powershell
# Try to get function (should fail)
aws lambda get-function `
    --function-name sample-function-tutorial `
    --profile child-account

# Expected: Error - ResourceNotFoundException
```

### Verify API Gateway Deleted

```powershell
# List APIs (tutorial API should not be present)
aws apigateway get-rest-apis --profile child-account

# Expected: Tutorial API not in list
```

---

## Step 6.5: Check for Orphaned Resources

**Sometimes resources don't get deleted properly. Check for orphans:**

```powershell
# Check CloudWatch log groups
aws logs describe-log-groups `
    --log-group-name-prefix "/aws/lambda/sample-function-tutorial" `
    --profile child-account

# If log group still exists, delete manually:
aws logs delete-log-group `
    --log-group-name "/aws/lambda/sample-function-tutorial" `
    --profile child-account

# Check SNS topics
aws sns list-topics --profile child-account | Select-String "tutorial-alerts"

# If topic still exists, delete manually:
# aws sns delete-topic --topic-arn <arn> --profile child-account

# Check CloudWatch alarms
aws cloudwatch describe-alarms `
    --alarm-name-prefix "sample-function-tutorial" `
    --profile child-account

# If alarm still exists, delete manually:
# aws cloudwatch delete-alarms --alarm-names "sample-function-tutorial-errors" --profile child-account
```

---

## Step 6.6: Clean Local Files

```powershell
# Remove Terraform state files (optional - keeps history)
# Remove-Item terraform.tfstate
# Remove-Item terraform.tfstate.backup

# Remove test response files
Remove-Item response.json -ErrorAction SilentlyContinue

# Remove deployment outputs
Remove-Item deployment-outputs.json -ErrorAction SilentlyContinue

Write-Host "✅ Local files cleaned"
```

---

## Step 6.7: Verification Checklist

After cleanup, verify:

- [ ] `terraform destroy` completed successfully
- [ ] All 20+ resources destroyed
- [ ] IAM role deleted
- [ ] S3 bucket deleted
- [ ] DynamoDB table deleted
- [ ] Lambda function deleted
- [ ] API Gateway deleted
- [ ] SNS topic deleted
- [ ] CloudWatch alarm deleted
- [ ] CloudWatch log group deleted (or manually removed)
- [ ] No orphaned resources remain

---

## Step 6.8: Cost Verification

**Verify no ongoing costs:**

```powershell
# Check AWS Cost Explorer (via Console)
# 1. Log into child account
# 2. Go to AWS Cost Management → Cost Explorer
# 3. Verify costs drop to $0 after cleanup

# Or use AWS CLI
aws ce get-cost-and-usage `
    --time-period Start=2025-01-01,End=2025-01-31 `
    --granularity DAILY `
    --metrics BlendedCost `
    --profile child-account
```

---

## Step 6.9: Prepare for Next Practice Run

**Reset for another practice run:**

```powershell
# Verify Terraform is ready
terraform validate

# Expected: Success! The configuration is valid.

# Verify Lambda code exists
Test-Path ..\lambda-code\sample-function\sample-function.zip

# Expected: True

# Verify terraform.tfvars is configured
Get-Content terraform.tfvars | Select-String "child_account_id"

# Expected: Should show your child account ID (not REPLACE_WITH...)
```

**Ready for next run!** Just execute:
```powershell
terraform apply
```

---

## Understanding Terraform Destroy

### What Gets Destroyed

**Terraform destroys resources in reverse dependency order:**

1. CloudWatch alarm (depends on Lambda)
2. API Gateway stage (depends on deployment)
3. API Gateway deployment (depends on integration)
4. API Gateway integration (depends on Lambda)
5. Lambda permission (depends on Lambda and API Gateway)
6. API Gateway method (depends on resource)
7. API Gateway resource (depends on API)
8. API Gateway REST API
9. Lambda function (depends on role)
10. CloudWatch log group
11. DynamoDB table
12. S3 bucket configurations (depends on bucket)
13. S3 bucket
14. IAM role policy attachments (depends on role)
15. IAM role
16. SNS topic

### What Doesn't Get Destroyed

**These persist after destroy:**
- Cross-account IAM role (TerraformCrossAccountRole) - created manually
- AWS Organizations structure
- Terraform state file (local)
- Lambda code ZIP file (local)
- Terraform configuration files (local)

---

## Troubleshooting

### Error: "Resource still in use"

**Cause**: Dependency not properly handled

**Fix**: Wait 1-2 minutes and run `terraform destroy` again

### Error: "Bucket not empty"

**Cause**: S3 bucket has objects

**Fix**: Empty bucket manually:
```powershell
aws s3 rm s3://BUCKET_NAME --recursive --profile child-account
terraform destroy
```

### Error: "DynamoDB table is being deleted"

**Cause**: Table deletion in progress

**Fix**: Wait 1-2 minutes and run `terraform destroy` again

### Some resources not destroyed

**Cause**: Terraform lost track of resources

**Fix**: Delete manually via AWS Console or CLI, then:
```powershell
terraform refresh
terraform destroy
```

---

## Quick Reference

**Commands Used**:
- `terraform state list` - List managed resources
- `terraform plan -destroy` - Preview destruction
- `terraform destroy` - Destroy all resources
- `terraform refresh` - Sync state with reality

**Destruction Time**: 2-3 minutes
**Resources Destroyed**: 20+
**Cost After Cleanup**: $0

---

## Practice Cycle Complete!

✅ **Cleanup complete!**

**You've completed one full practice cycle:**
1. ✅ Account setup
2. ✅ IAM configuration
3. ✅ Terraform configuration
4. ✅ Infrastructure deployment
5. ✅ Verification and testing
6. ✅ Cleanup and reset

**To practice again:**
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform
terraform apply
# ... test ...
terraform destroy
```

**Each practice run takes**: ~15-20 minutes

---

## Next Steps

### For More Practice
- Repeat the cycle multiple times
- Modify resources (add tags, change settings)
- Experiment with different configurations
- Practice rollback scenarios

### To Extend the Tutorial
- Add more Lambda functions
- Add more DynamoDB tables
- Add CloudFront distribution
- Add Route53 records
- Add more API Gateway endpoints

### To Apply to Production
- Review production infrastructure
- Identify resources to Terraform-ify
- Create Terraform modules
- Implement blue/green deployments
- Add CI/CD pipeline

---

## Congratulations!

You've successfully learned:
- ✅ Multi-account AWS architecture
- ✅ Cross-account IAM roles
- ✅ Terraform provider configuration
- ✅ Infrastructure as Code patterns
- ✅ Resource dependencies
- ✅ Deployment and verification
- ✅ Cleanup and reset

**Keep practicing to build muscle memory!**
