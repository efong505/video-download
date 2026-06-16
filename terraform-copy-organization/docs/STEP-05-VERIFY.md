# STEP 05: Verify Deployment

**Goal**: Test the deployed infrastructure to ensure everything works

**Time**: 15-20 minutes

---

## Overview

You'll verify:
1. Resources exist in child account
2. Lambda function works
3. API Gateway endpoint responds
4. DynamoDB operations work
5. S3 operations work
6. SNS notifications work

---

## Step 5.1: View Terraform Outputs

```powershell
# Navigate to terraform directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform

# Display all outputs
terraform output

# Display specific output
terraform output api_gateway_endpoint
terraform output lambda_function_name
terraform output s3_bucket_name
terraform output dynamodb_table_name
```

**Save these values - you'll need them for testing.**

---

## Step 5.2: Verify IAM Role

```powershell
# Get role details (requires child account access)
aws iam get-role `
    --role-name lambda-execution-role-tutorial `
    --profile child-account

# List attached policies
aws iam list-attached-role-policies `
    --role-name lambda-execution-role-tutorial `
    --profile child-account

# Expected: 4 policies attached
```

**If you don't have child-account profile configured**, you can verify in AWS Console:
1. Log into child account
2. Go to IAM → Roles
3. Find `lambda-execution-role-tutorial`
4. Verify 4 policies attached

---

## Step 5.3: Verify S3 Bucket

```powershell
# Get bucket name from Terraform
$BUCKET_NAME = terraform output -raw s3_bucket_name

# List bucket (should be empty initially)
aws s3 ls s3://$BUCKET_NAME/ --profile child-account

# Get bucket versioning status
aws s3api get-bucket-versioning --bucket $BUCKET_NAME --profile child-account

# Expected output:
# {
#     "Status": "Enabled"
# }

# Get bucket encryption
aws s3api get-bucket-encryption --bucket $BUCKET_NAME --profile child-account

# Expected: AES256 encryption enabled
```

---

## Step 5.4: Verify DynamoDB Table

```powershell
# Get table name from Terraform
$TABLE_NAME = terraform output -raw dynamodb_table_name

# Describe table
aws dynamodb describe-table --table-name $TABLE_NAME --profile child-account

# Check table status
aws dynamodb describe-table `
    --table-name $TABLE_NAME `
    --profile child-account `
    --query 'Table.TableStatus'

# Expected output: "ACTIVE"

# List items (should be empty initially)
aws dynamodb scan --table-name $TABLE_NAME --profile child-account
```

---

## Step 5.5: Verify Lambda Function

```powershell
# Get function name from Terraform
$FUNCTION_NAME = terraform output -raw lambda_function_name

# Get function configuration
aws lambda get-function --function-name $FUNCTION_NAME --profile child-account

# Test Lambda function with simple payload
$payload = @{
    action = "test"
} | ConvertTo-Json

# Invoke Lambda function
aws lambda invoke `
    --function-name $FUNCTION_NAME `
    --payload $payload `
    --profile child-account `
    response.json

# View response
Get-Content response.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Expected output:
# {
#     "statusCode": 200,
#     "body": "{\"message\":\"Success\",\"action\":\"test\",\"result\":{...}}"
# }
```

---

## Step 5.6: Test API Gateway Endpoint

```powershell
# Get API Gateway endpoint from Terraform
$API_ENDPOINT = terraform output -raw api_gateway_endpoint

# Test with simple request
$body = @{
    action = "test"
} | ConvertTo-Json

# Make POST request
Invoke-RestMethod `
    -Uri "$API_ENDPOINT/sample" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Expected output:
# message     : Success
# action      : test
# result      : @{status=Lambda function is working; ...}
# environment : tutorial
# timestamp   : 1234567890
```

---

## Step 5.7: Test DynamoDB Write

```powershell
# Test writing to DynamoDB via Lambda
$body = @{
    action = "write_dynamodb"
    test_data = "Hello from tutorial"
} | ConvertTo-Json

# Invoke via API Gateway
$response = Invoke-RestMethod `
    -Uri "$API_ENDPOINT/sample" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"

# Verify item was written to DynamoDB
aws dynamodb scan `
    --table-name $TABLE_NAME `
    --profile child-account `
    --max-items 5

# Expected: You should see the item you just wrote
```

---

## Step 5.8: Test S3 Write

```powershell
# Test writing to S3 via Lambda
$body = @{
    action = "write_s3"
    test_data = "S3 test from tutorial"
} | ConvertTo-Json

# Invoke via API Gateway
$response = Invoke-RestMethod `
    -Uri "$API_ENDPOINT/sample" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"

# Verify object was written to S3
aws s3 ls s3://$BUCKET_NAME/test-data/ --profile child-account

# Expected: You should see a JSON file
```

---

## Step 5.9: Test SNS Notification

**First, subscribe to SNS topic to receive test notification:**

```powershell
# Get SNS topic ARN from Terraform
$TOPIC_ARN = terraform output -raw sns_topic_arn

# Subscribe your email to the topic
aws sns subscribe `
    --topic-arn $TOPIC_ARN `
    --protocol email `
    --notification-endpoint hawaiianintucson.com `
    --profile child-account

# Check your email and confirm subscription
Write-Host "⚠️  Check your email and confirm SNS subscription"
Write-Host "   Then press Enter to continue..."
Read-Host

# Test sending notification via Lambda
$body = @{
    action = "send_notification"
    message = "Test notification from tutorial Lambda function"
} | ConvertTo-Json

# Invoke via API Gateway
$response = Invoke-RestMethod `
    -Uri "$API_ENDPOINT/sample" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"
Write-Host "⚠️  Check your email for the notification"
```

---

## Step 5.10: Check CloudWatch Logs

```powershell
# Get log group name
$LOG_GROUP = "/aws/lambda/$FUNCTION_NAME"

# List recent log streams
aws logs describe-log-streams `
    --log-group-name $LOG_GROUP `
    --order-by LastEventTime `
    --descending `
    --max-items 5 `
    --profile child-account

# Get the latest log stream name
$LOG_STREAM = (aws logs describe-log-streams `
    --log-group-name $LOG_GROUP `
    --order-by LastEventTime `
    --descending `
    --max-items 1 `
    --profile child-account `
    --query 'logStreams[0].logStreamName' `
    --output text)

# View recent logs
aws logs get-log-events `
    --log-group-name $LOG_GROUP `
    --log-stream-name $LOG_STREAM `
    --profile child-account `
    --limit 50

# Expected: You should see logs from your Lambda invocations
```

---

## Step 5.11: Check CloudWatch Alarm

```powershell
# Get alarm name
$ALARM_NAME = "$FUNCTION_NAME-errors"

# Describe alarm
aws cloudwatch describe-alarms `
    --alarm-names $ALARM_NAME `
    --profile child-account

# Check alarm state
aws cloudwatch describe-alarms `
    --alarm-names $ALARM_NAME `
    --profile child-account `
    --query 'MetricAlarms[0].StateValue'

# Expected: "OK" (no errors yet)
```

---

## Step 5.12: Verification Checklist

Verify all components:

- [ ] IAM role exists with 4 policies
- [ ] S3 bucket exists with versioning and encryption
- [ ] DynamoDB table is ACTIVE
- [ ] Lambda function responds to invocations
- [ ] API Gateway endpoint is accessible
- [ ] Can write to DynamoDB via Lambda
- [ ] Can write to S3 via Lambda
- [ ] SNS notifications work (if subscribed)
- [ ] CloudWatch logs are being created
- [ ] CloudWatch alarm is in OK state

---

## Step 5.13: Compare with Production

**Review how this matches your production setup:**

| Component | Production | Tutorial | Match? |
|-----------|-----------|----------|--------|
| IAM Role | lambda-execution-role | lambda-execution-role-tutorial | ✅ |
| Policies | 9 managed policies | 4 managed policies | ⚠️ Simplified |
| S3 Bucket | my-video-downloads-bucket | infra-copy-tutorial-* | ✅ |
| Versioning | Enabled | Enabled | ✅ |
| Encryption | AES256 | AES256 | ✅ |
| DynamoDB | 28 tables | 1 table | ⚠️ Simplified |
| Lambda | 18 functions | 1 function | ⚠️ Simplified |
| API Gateway | Unified API (14 endpoints) | 1 API (1 endpoint) | ⚠️ Simplified |
| CloudWatch | 27 alarms, 18 log groups | 1 alarm, 1 log group | ⚠️ Simplified |
| SNS | platform-critical-alerts | tutorial-alerts | ✅ |

**Key Takeaway**: Tutorial uses same patterns as production, just simplified scale.

---

## Troubleshooting

### Error: "Function not found"

**Cause**: Lambda function wasn't created

**Fix**: Check Terraform apply output for errors

### Error: "Access denied" when testing

**Cause**: IAM role doesn't have necessary permissions

**Fix**: Verify role has 4 policies attached

### API Gateway returns 500 error

**Cause**: Lambda function error

**Fix**: Check CloudWatch logs for error details

### No logs in CloudWatch

**Cause**: Log group not created or Lambda not invoked

**Fix**: Verify log group exists and invoke Lambda again

---

## Quick Reference

**Key Resources**:
- Lambda: `sample-function-tutorial`
- S3: `infra-copy-tutorial-[ACCOUNT_ID]`
- DynamoDB: `sample-table-tutorial`
- API Gateway: `sample-api-tutorial`
- SNS: `tutorial-alerts`

**Test Actions**:
- `test` - Basic function test
- `write_dynamodb` - Write to DynamoDB
- `write_s3` - Write to S3
- `send_notification` - Send SNS notification

---

## Next Step

✅ **Verification complete!**

→ Continue to `STEP-06-CLEANUP.md` to clean up resources and practice the full cycle.

---

## Practice Tips

**For subsequent practice runs**:
1. Skip SNS subscription (already done)
2. Focus on API Gateway testing
3. Verify outputs quickly
4. Check CloudWatch logs
5. Takes ~5 minutes
