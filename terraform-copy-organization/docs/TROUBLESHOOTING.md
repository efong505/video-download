# Troubleshooting Guide

Common issues and solutions for the Terraform Multi-Account Infrastructure Copy Tutorial.

---

## Table of Contents

1. [Account Setup Issues](#account-setup-issues)
2. [Terraform Configuration Issues](#terraform-configuration-issues)
3. [Deployment Issues](#deployment-issues)
4. [Verification Issues](#verification-issues)
5. [Cleanup Issues](#cleanup-issues)
6. [General AWS Issues](#general-aws-issues)

---

## Account Setup Issues

### Error: "Organizations is not enabled"

**Symptom**:
```
An error occurred (AWSOrganizationsNotInUseException) when calling the DescribeOrganization operation
```

**Cause**: AWS Organizations not set up in production account

**Solution**:
```powershell
aws organizations create-organization --feature-set ALL
```

---

### Error: "Access Denied" when creating organization

**Symptom**:
```
An error occurred (AccessDeniedException) when calling the CreateOrganization operation
```

**Cause**: IAM user doesn't have Organizations permissions

**Solution**:
1. Log into AWS Console as root user
2. Create organization from Console
3. Or attach OrganizationsFullAccess policy to IAM user

---

### Error: "Cannot assume role"

**Symptom**:
```
An error occurred (AccessDenied) when calling the AssumeRole operation
```

**Cause**: Trust policy doesn't allow production account, or external ID mismatch

**Solution**:
```powershell
# Verify trust policy in child account role
aws iam get-role --role-name TerraformCrossAccountRole --profile child-account

# Trust policy should include:
# "Principal": { "AWS": "arn:aws:iam::371751795928:root" }
# "Condition": { "StringEquals": { "sts:ExternalId": "terraform-copy-tutorial" } }
```

---

### Error: "Role already exists"

**Symptom**:
```
An error occurred (EntityAlreadyExists) when calling the CreateRole operation
```

**Cause**: Role already created from previous tutorial run

**Solution**: This is fine! Skip role creation and continue to next step.

---

## Terraform Configuration Issues

### Error: "No valid credential sources found"

**Symptom**:
```
Error: No valid credential sources found for AWS Provider
```

**Cause**: AWS credentials not configured

**Solution**:
```powershell
# Configure AWS CLI
aws configure

# Verify credentials
aws sts get-caller-identity
```

---

### Error: "Invalid provider configuration"

**Symptom**:
```
Error: Invalid provider configuration
```

**Cause**: Syntax error in providers.tf or missing variables

**Solution**:
```powershell
# Validate configuration
terraform validate

# Check for specific errors in output
# Common issues:
# - Missing closing braces
# - Incorrect variable references
# - Typos in provider block
```

---

### Error: "Variable not defined"

**Symptom**:
```
Error: Reference to undeclared input variable
```

**Cause**: Variable used but not defined in variables.tf

**Solution**:
```powershell
# Ensure variable is defined in variables.tf
# Example:
# variable "child_account_id" {
#   description = "Child AWS account ID"
#   type        = string
# }
```

---

### Error: "terraform.tfvars contains REPLACE_WITH..."

**Symptom**: Terraform plan fails with invalid account ID

**Cause**: terraform.tfvars not updated with actual child account ID

**Solution**:
```powershell
# Edit terraform.tfvars
notepad terraform.tfvars

# Replace all instances of:
# REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID
# with your actual child account ID
```

---

## Deployment Issues

### Error: "Error assuming role" during apply

**Symptom**:
```
Error: error configuring Terraform AWS Provider: error validating provider credentials
```

**Cause**: Can't assume cross-account role

**Solution**:
```powershell
# Test assume role manually
aws sts assume-role `
    --role-arn "arn:aws:iam::CHILD_ID:role/TerraformCrossAccountRole" `
    --role-session-name "test" `
    --external-id "terraform-copy-tutorial"

# If this fails, check:
# 1. Role exists in child account
# 2. Trust policy is correct
# 3. External ID matches
# 4. Production account ID is correct in trust policy
```

---

### Error: "Bucket name already exists"

**Symptom**:
```
Error: error creating S3 Bucket: BucketAlreadyExists
```

**Cause**: S3 bucket names must be globally unique across ALL AWS accounts

**Solution**:
```powershell
# Edit terraform.tfvars
# Change s3_bucket_name to something unique
s3_bucket_name = "infra-copy-tutorial-CHILD_ACCOUNT_ID-v2"
```

---

### Error: "Lambda function code not found"

**Symptom**:
```
Error: error creating Lambda Function: InvalidParameterValueException
```

**Cause**: ZIP file doesn't exist or path is incorrect

**Solution**:
```powershell
# Verify ZIP exists
Test-Path ..\lambda-code\sample-function\sample-function.zip

# If False, create it:
cd ..\lambda-code\sample-function
Compress-Archive -Path index.py -DestinationPath sample-function.zip -Force
cd ..\..\terraform
```

---

### Error: "IAM role not ready"

**Symptom**:
```
Error: error creating Lambda Function: InvalidParameterValueException: The role defined for the function cannot be assumed by Lambda
```

**Cause**: IAM role just created, not yet propagated

**Solution**:
```powershell
# Wait 10-15 seconds and try again
Start-Sleep -Seconds 15
terraform apply
```

---

### Error: "API Gateway deployment failed"

**Symptom**:
```
Error: error creating API Gateway Deployment: BadRequestException
```

**Cause**: Integration not properly configured

**Solution**:
```powershell
# Check that Lambda integration exists
terraform state list | Select-String "api_gateway_integration"

# If missing, check main.tf for syntax errors in integration block
```

---

## Verification Issues

### Error: "403 Forbidden" when testing API

**Symptom**: API Gateway returns 403 error

**Cause**: Lambda permission not granted to API Gateway

**Solution**:
```powershell
# Verify Lambda permission exists
terraform state list | Select-String "lambda_permission"

# If missing, check main.tf for aws_lambda_permission resource
```

---

### Error: "500 Internal Server Error" from API

**Symptom**: API Gateway returns 500 error

**Cause**: Lambda function error

**Solution**:
```powershell
# Check CloudWatch logs
$FUNCTION_NAME = terraform output -raw lambda_function_name
$LOG_GROUP = "/aws/lambda/$FUNCTION_NAME"

aws logs tail $LOG_GROUP --follow --profile child-account

# Look for error messages in logs
```

---

### Error: "Access Denied" when Lambda writes to DynamoDB

**Symptom**: Lambda function fails with AccessDeniedException

**Cause**: IAM role doesn't have DynamoDB permissions

**Solution**:
```powershell
# Verify IAM policy attachments
terraform state list | Select-String "iam_role_policy_attachment"

# Should see 4 attachments including lambda_dynamodb
# If missing, check main.tf for policy attachment resources
```

---

### Error: "Table not found" in Lambda

**Symptom**: Lambda logs show ResourceNotFoundException for DynamoDB

**Cause**: Environment variable not set correctly

**Solution**:
```powershell
# Check Lambda environment variables
aws lambda get-function-configuration `
    --function-name sample-function-tutorial `
    --profile child-account `
    --query 'Environment.Variables'

# Should show DYNAMODB_TABLE, S3_BUCKET, SNS_TOPIC_ARN
```

---

## Cleanup Issues

### Error: "Bucket not empty" during destroy

**Symptom**:
```
Error: error deleting S3 Bucket: BucketNotEmpty
```

**Cause**: S3 bucket contains objects

**Solution**:
```powershell
# Empty bucket first
$BUCKET_NAME = terraform output -raw s3_bucket_name
aws s3 rm s3://$BUCKET_NAME --recursive --profile child-account

# Then destroy
terraform destroy
```

---

### Error: "Resource still in use"

**Symptom**:
```
Error: error deleting resource: ResourceInUseException
```

**Cause**: Resource has dependencies that haven't been deleted yet

**Solution**:
```powershell
# Wait 1-2 minutes for AWS to process deletions
Start-Sleep -Seconds 120

# Try destroy again
terraform destroy
```

---

### Error: "DynamoDB table is being deleted"

**Symptom**:
```
Error: error deleting DynamoDB Table: ResourceInUseException: Table is being deleted
```

**Cause**: Table deletion already in progress

**Solution**:
```powershell
# Wait for deletion to complete
Start-Sleep -Seconds 60

# Refresh state and try again
terraform refresh
terraform destroy
```

---

### Error: Some resources not destroyed

**Symptom**: `terraform destroy` completes but resources still exist in AWS

**Cause**: Terraform lost track of resources (state drift)

**Solution**:
```powershell
# Refresh state
terraform refresh

# Try destroy again
terraform destroy

# If still failing, delete manually via Console or CLI
# Then remove from state:
terraform state rm aws_resource_type.resource_name
```

---

## General AWS Issues

### Error: "Rate exceeded"

**Symptom**:
```
Error: error creating resource: Throttling: Rate exceeded
```

**Cause**: Too many API calls to AWS

**Solution**:
```powershell
# Wait a few minutes
Start-Sleep -Seconds 300

# Try again
terraform apply
```

---

### Error: "Region not supported"

**Symptom**:
```
Error: error creating resource: InvalidParameterValueException: Region not supported
```

**Cause**: Service not available in specified region

**Solution**:
```powershell
# Verify region in terraform.tfvars
# Tutorial uses us-east-1 which supports all services
aws_region = "us-east-1"
```

---

### Error: "Service quota exceeded"

**Symptom**:
```
Error: error creating resource: LimitExceededException
```

**Cause**: AWS service limit reached

**Solution**:
1. Check AWS Service Quotas in Console
2. Request limit increase if needed
3. Or delete unused resources to free up quota

---

## Getting Help

### Enable Terraform Debug Logging

```powershell
# Set debug level
$env:TF_LOG = "DEBUG"

# Run Terraform command
terraform apply

# Disable debug logging
$env:TF_LOG = ""
```

### Check Terraform State

```powershell
# List all resources
terraform state list

# Show specific resource
terraform state show aws_lambda_function.main

# Verify state matches reality
terraform refresh
```

### Verify AWS Resources Manually

```powershell
# List Lambda functions
aws lambda list-functions --profile child-account

# List S3 buckets
aws s3 ls --profile child-account

# List DynamoDB tables
aws dynamodb list-tables --profile child-account

# List API Gateways
aws apigateway get-rest-apis --profile child-account
```

---

## Common Mistakes

### 1. Forgetting to update terraform.tfvars

**Mistake**: Leaving REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID in terraform.tfvars

**Fix**: Always edit terraform.tfvars before first apply

### 2. Using wrong AWS profile

**Mistake**: Testing with production account instead of child account

**Fix**: Always use `--profile child-account` when verifying resources

### 3. Not waiting for IAM propagation

**Mistake**: Applying immediately after creating IAM role

**Fix**: Wait 10-15 seconds after IAM role creation

### 4. Forgetting to create Lambda ZIP

**Mistake**: Running terraform apply without creating sample-function.zip

**Fix**: Always create ZIP before terraform apply

### 5. Not cleaning up between practice runs

**Mistake**: Running terraform apply without destroying previous resources

**Fix**: Always run terraform destroy before next practice run

---

## Prevention Tips

### Before Each Practice Run

```powershell
# 1. Verify credentials
aws sts get-caller-identity

# 2. Verify terraform.tfvars is configured
Get-Content terraform\terraform.tfvars | Select-String "REPLACE_WITH"
# Should return nothing

# 3. Verify Lambda ZIP exists
Test-Path lambda-code\sample-function\sample-function.zip
# Should return True

# 4. Verify no resources exist
terraform state list
# Should return nothing (or run terraform destroy first)

# 5. Validate configuration
cd terraform
terraform validate
# Should return "Success!"
```

---

## Still Having Issues?

1. **Review step-by-step guides** in `docs/` directory
2. **Check Terraform documentation**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
3. **Check AWS documentation** for specific services
4. **Enable debug logging** to see detailed error messages
5. **Verify all prerequisites** are met
6. **Start fresh** with `terraform destroy` and try again

---

## Quick Diagnostic Script

```powershell
# Run this to diagnose common issues
Write-Host "=== Terraform Tutorial Diagnostics ===" -ForegroundColor Green

# Check AWS credentials
Write-Host "`n1. Checking AWS credentials..." -ForegroundColor Yellow
try {
    aws sts get-caller-identity
    Write-Host "✅ AWS credentials OK" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS credentials not configured" -ForegroundColor Red
}

# Check Terraform
Write-Host "`n2. Checking Terraform..." -ForegroundColor Yellow
try {
    terraform version
    Write-Host "✅ Terraform installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform not installed" -ForegroundColor Red
}

# Check terraform.tfvars
Write-Host "`n3. Checking terraform.tfvars..." -ForegroundColor Yellow
$placeholders = Get-Content terraform\terraform.tfvars | Select-String "REPLACE_WITH"
if ($placeholders) {
    Write-Host "❌ terraform.tfvars contains placeholders" -ForegroundColor Red
    Write-Host "   Update: $placeholders"
} else {
    Write-Host "✅ terraform.tfvars configured" -ForegroundColor Green
}

# Check Lambda ZIP
Write-Host "`n4. Checking Lambda ZIP..." -ForegroundColor Yellow
if (Test-Path lambda-code\sample-function\sample-function.zip) {
    Write-Host "✅ Lambda ZIP exists" -ForegroundColor Green
} else {
    Write-Host "❌ Lambda ZIP not found" -ForegroundColor Red
}

# Check Terraform state
Write-Host "`n5. Checking Terraform state..." -ForegroundColor Yellow
cd terraform
$resources = terraform state list
if ($resources) {
    Write-Host "⚠️  Resources exist in state:" -ForegroundColor Yellow
    $resources
    Write-Host "   Run 'terraform destroy' before next practice run"
} else {
    Write-Host "✅ No resources in state (ready for fresh deploy)" -ForegroundColor Green
}

Write-Host "`n=== Diagnostics Complete ===" -ForegroundColor Green
```

Save this as `diagnose.ps1` and run before each practice session!
