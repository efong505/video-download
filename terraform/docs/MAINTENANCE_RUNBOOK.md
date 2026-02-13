# Terraform Maintenance Runbook

## Overview

This runbook provides step-by-step procedures for common Terraform maintenance tasks for the Christian Conservative Platform infrastructure.

**Last Updated**: February 11, 2026  
**Terraform Version**: 1.0+  
**AWS Provider Version**: ~> 5.0

---

## Table of Contents

1. [Daily Operations](#daily-operations)
2. [Adding New Resources](#adding-new-resources)
3. [Updating Existing Resources](#updating-existing-resources)
4. [Disaster Recovery](#disaster-recovery)
5. [Troubleshooting](#troubleshooting)
6. [Emergency Procedures](#emergency-procedures)

---

## Daily Operations

### Check Infrastructure Drift

**Frequency**: Daily  
**Duration**: 2 minutes

```bash
cd terraform/environments/prod
terraform plan
```

**Expected Output**: "No changes. Your infrastructure matches the configuration."

**If Drift Detected**:
1. Review changes carefully
2. Determine if manual change was intentional
3. Either update Terraform or revert manual change
4. Document reason for drift

### Monitor CloudWatch Alarms

**Frequency**: Daily  
**Duration**: 5 minutes

1. Check email for alarm notifications
2. Review AWS CloudWatch console
3. Investigate any triggered alarms
4. Document incidents

### Review Lambda Logs

**Frequency**: Daily  
**Duration**: 10 minutes

```bash
# View recent errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/video-downloader \
  --filter-pattern "ERROR" \
  --start-time $(date -d '1 hour ago' +%s)000
```

---

## Adding New Resources

### Add New Lambda Function

**Duration**: 15 minutes

1. **Create function code**:
```bash
mkdir Downloader/new_function
cd Downloader/new_function
touch index.py
```

2. **Add to Terraform**:
```hcl
# In terraform/environments/prod/main.tf
module "lambda_new_function" {
  source = "../../modules/lambda"

  function_name = "new-function"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"

  environment_variables = {}
}
```

3. **Add CloudWatch log group**:
```hcl
# In terraform/environments/prod/cloudwatch.tf
module "log_group_new_function" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name = "/aws/lambda/new-function"
  retention_days = 14
}
```

4. **Add CloudWatch alarm**:
```hcl
# In terraform/environments/prod/cloudwatch.tf
module "alarm_new_function_errors" {
  source = "../../modules/cloudwatch-alarm"

  alarm_name          = "Lambda-NewFunction-Errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 3
  alarm_description   = "New function error rate"
  alarm_actions       = [module.sns_critical_alerts.topic_arn]
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = "new-function"
  }
}
```

5. **Apply changes**:
```bash
terraform plan
terraform apply
```

6. **Deploy function code**:
```bash
cd Downloader/new_function
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name new-function \
  --zip-file fileb://function.zip
```

### Add New DynamoDB Table

**Duration**: 10 minutes

1. **Add to Terraform**:
```hcl
# In terraform/environments/prod/main.tf
module "dynamodb_new_table" {
  source = "../../modules/dynamodb"

  table_name   = "new-table"
  hash_key     = "id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "id", type = "S" }
  ]
}
```

2. **Apply changes**:
```bash
terraform plan
terraform apply
```

### Add API Gateway Endpoint

**Duration**: 10 minutes

1. **Add to Terraform**:
```hcl
# In terraform/environments/prod/main.tf
module "api_new_endpoint" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "new-endpoint"
  http_method          = "ANY"
  lambda_function_name = module.lambda_new_function.function_name
  lambda_function_arn  = module.lambda_new_function.function_arn
  enable_cors          = true
}
```

2. **Apply changes**:
```bash
terraform plan
terraform apply
```

3. **Test endpoint**:
```bash
curl https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/new-endpoint
```

---

## Updating Existing Resources

### Update Lambda Function Configuration

**Duration**: 5 minutes

1. **Edit Terraform**:
```hcl
module "lambda_function" {
  memory_size = 256  # Changed from 128
  timeout     = 60   # Changed from 30
}
```

2. **Apply changes**:
```bash
terraform plan
terraform apply
```

### Update Lambda Function Code

**Duration**: 3 minutes

```bash
cd Downloader/function_name
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name function-name \
  --zip-file fileb://function.zip
```

**Note**: Terraform ignores code changes (ignore_changes on filename).

### Update CloudWatch Alarm Threshold

**Duration**: 5 minutes

1. **Edit Terraform**:
```hcl
module "alarm_function_errors" {
  threshold = 5  # Changed from 3
}
```

2. **Apply changes**:
```bash
terraform plan
terraform apply
```

### Update DynamoDB Table (Add GSI)

**Duration**: 10 minutes

1. **Edit Terraform**:
```hcl
module "dynamodb_table" {
  global_secondary_indexes = [
    {
      name            = "email-index"
      hash_key        = "email"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}
```

2. **Apply changes**:
```bash
terraform plan
terraform apply
```

**Warning**: GSI creation can take several minutes.

---

## Disaster Recovery

### Full Infrastructure Recreation

**Duration**: 20 minutes  
**Use Case**: Complete AWS account loss or corruption

1. **Ensure Terraform state is backed up**:
```bash
aws s3 ls s3://techcross-terraform-state/prod/
```

2. **Recreate infrastructure**:
```bash
cd terraform/environments/prod
terraform init
terraform plan
terraform apply
```

3. **Deploy Lambda function code**:
```bash
# Use CI/CD pipeline or manual deployment
git push origin main
```

4. **Verify all services**:
```bash
# Test API Gateway
curl https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth

# Test CloudFront
curl https://videos.mytestimony.click

# Check Lambda functions
aws lambda list-functions
```

### Restore Single Lambda Function

**Duration**: 5 minutes

1. **Check Terraform state**:
```bash
terraform state show module.lambda_function.aws_lambda_function.this
```

2. **Recreate if missing**:
```bash
terraform apply -target=module.lambda_function
```

3. **Deploy code**:
```bash
cd Downloader/function_name
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name function-name \
  --zip-file fileb://function.zip
```

### Restore DynamoDB Table

**Duration**: 10 minutes + data restore time

1. **Recreate table structure**:
```bash
terraform apply -target=module.dynamodb_table
```

2. **Restore data from backup**:
```bash
# If Point-in-Time Recovery enabled
aws dynamodb restore-table-to-point-in-time \
  --source-table-name table-name \
  --target-table-name table-name-restored \
  --restore-date-time 2026-02-11T00:00:00Z
```

---

## Troubleshooting

### Terraform State Lock

**Symptom**: "Error acquiring the state lock"

**Solution**:
```bash
# Check lock status
aws dynamodb get-item \
  --table-name terraform-state-lock \
  --key '{"LockID":{"S":"techcross-terraform-state/prod/terraform.tfstate-md5"}}'

# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>
```

### Terraform Plan Shows Unexpected Changes

**Symptom**: Terraform wants to modify resources you didn't change

**Solution**:
1. Check for manual AWS Console changes
2. Review Terraform state
3. Use `terraform refresh` to sync state
4. If needed, import resource again

### Lambda Function Not Updating

**Symptom**: Code changes not reflected in Lambda

**Solution**:
```bash
# Check function version
aws lambda get-function --function-name function-name

# Force update
aws lambda update-function-code \
  --function-name function-name \
  --zip-file fileb://function.zip \
  --publish
```

### API Gateway 403 Errors

**Symptom**: API returns 403 Forbidden

**Solution**:
1. Check Lambda permissions
2. Verify API Gateway deployment
3. Check CORS configuration
4. Review CloudWatch logs

```bash
# Redeploy API Gateway
terraform apply -target=module.unified_api
```

### CloudWatch Alarm Not Triggering

**Symptom**: Alarm doesn't fire when it should

**Solution**:
1. Check alarm configuration
2. Verify SNS topic subscription
3. Test alarm manually

```bash
# Set alarm to ALARM state
aws cloudwatch set-alarm-state \
  --alarm-name Lambda-Function-Errors \
  --state-value ALARM \
  --state-reason "Testing alarm"
```

---

## Emergency Procedures

### Emergency: All Lambda Functions Down

**Duration**: 10 minutes

1. **Check AWS Service Health**:
   - Visit https://health.aws.amazon.com/health/status

2. **Check IAM Role**:
```bash
aws iam get-role --role-name lambda-execution-role
```

3. **Recreate IAM Role if needed**:
```bash
terraform apply -target=module.lambda_execution_role
```

4. **Recreate all Lambda functions**:
```bash
terraform apply
```

5. **Deploy all function code**:
```bash
git push origin main  # Triggers CI/CD
```

### Emergency: DynamoDB Table Deleted

**Duration**: 15 minutes + restore time

1. **DO NOT PANIC** - Point-in-Time Recovery is enabled

2. **Check if table exists**:
```bash
aws dynamodb describe-table --table-name table-name
```

3. **Restore from PITR**:
```bash
aws dynamodb restore-table-to-point-in-time \
  --source-table-name table-name \
  --target-table-name table-name \
  --use-latest-restorable-time
```

4. **Wait for restore** (can take 10-30 minutes)

5. **Verify data**:
```bash
aws dynamodb scan --table-name table-name --limit 10
```

### Emergency: Terraform State Corrupted

**Duration**: 20 minutes

1. **Check S3 versioning**:
```bash
aws s3api list-object-versions \
  --bucket techcross-terraform-state \
  --prefix prod/terraform.tfstate
```

2. **Restore previous version**:
```bash
aws s3api get-object \
  --bucket techcross-terraform-state \
  --key prod/terraform.tfstate \
  --version-id <VERSION_ID> \
  terraform.tfstate.backup
```

3. **Replace current state**:
```bash
aws s3 cp terraform.tfstate.backup \
  s3://techcross-terraform-state/prod/terraform.tfstate
```

4. **Verify state**:
```bash
terraform plan
```

### Emergency: API Gateway Down

**Duration**: 5 minutes

1. **Check API Gateway status**:
```bash
aws apigateway get-rest-api --rest-api-id diz6ceeb22
```

2. **Recreate API Gateway**:
```bash
terraform apply -target=module.unified_api
```

3. **Recreate all integrations**:
```bash
terraform apply
```

4. **Test endpoints**:
```bash
curl https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth
```

---

## Maintenance Schedule

### Daily
- [ ] Check infrastructure drift
- [ ] Monitor CloudWatch alarms
- [ ] Review Lambda error logs

### Weekly
- [ ] Review CloudWatch costs
- [ ] Check for AWS service updates
- [ ] Review security advisories

### Monthly
- [ ] Update Lambda runtimes if needed
- [ ] Review and optimize Lambda memory
- [ ] Audit IAM permissions
- [ ] Review DynamoDB table sizes
- [ ] Check S3 storage costs

### Quarterly
- [ ] Update Terraform provider versions
- [ ] Review and update documentation
- [ ] Conduct disaster recovery drill
- [ ] Review and optimize costs

### Annually
- [ ] Major version updates
- [ ] Security audit
- [ ] Architecture review
- [ ] Backup strategy review

---

## Contact Information

**Primary Contact**: Ed  
**Email**: hawaiianintucson@gmail.com  
**AWS Account**: 371751795928  
**Region**: us-east-1

**Escalation**:
1. Check AWS Service Health Dashboard
2. Review CloudWatch logs
3. Check Terraform state
4. Contact AWS Support if needed

---

## Additional Resources

- [Terraform Documentation](./TERRAFORM_DOCUMENTATION.md)
- [PROJECT_OUTLINE.md](./PROJECT_OUTLINE.md)
- [All Implementation Guides](./README.md)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Last Updated**: February 11, 2026  
**Version**: 1.0  
**Status**: Production Ready
