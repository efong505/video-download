# Verify Deployment Script
# Tests all deployed resources to ensure they work correctly

Write-Host "=== Deployment Verification Script ===" -ForegroundColor Green
Write-Host ""

# Change to terraform directory
Push-Location terraform

# Step 1: Get Terraform outputs
Write-Host "Step 1: Getting Terraform outputs..." -ForegroundColor Yellow
try {
    $outputs = terraform output -json | ConvertFrom-Json
    Write-Host "✅ Terraform outputs retrieved" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to get Terraform outputs" -ForegroundColor Red
    Write-Host "   Make sure you've run 'terraform apply' first" -ForegroundColor Yellow
    Pop-Location
    exit 1
}

# Extract key values
$apiEndpoint = $outputs.api_gateway_endpoint.value
$lambdaName = $outputs.lambda_function_name.value
$s3Bucket = $outputs.s3_bucket_name.value
$dynamoTable = $outputs.dynamodb_table_name.value
$snsTopicArn = $outputs.sns_topic_arn.value

Write-Host "   API Endpoint: $apiEndpoint" -ForegroundColor Cyan
Write-Host "   Lambda: $lambdaName" -ForegroundColor Cyan
Write-Host "   S3 Bucket: $s3Bucket" -ForegroundColor Cyan
Write-Host "   DynamoDB Table: $dynamoTable" -ForegroundColor Cyan

# Step 2: Test Lambda function directly
Write-Host "`nStep 2: Testing Lambda function..." -ForegroundColor Yellow
$payload = @{ action = "test" } | ConvertTo-Json

try {
    aws lambda invoke `
        --function-name $lambdaName `
        --payload $payload `
        --profile child-account `
        response.json | Out-Null
    
    $response = Get-Content response.json | ConvertFrom-Json
    
    if ($response.statusCode -eq 200) {
        Write-Host "✅ Lambda function works" -ForegroundColor Green
        $body = $response.body | ConvertFrom-Json
        Write-Host "   Environment: $($body.environment)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Lambda returned error: $($response.statusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Lambda invocation failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 3: Test API Gateway endpoint
Write-Host "`nStep 3: Testing API Gateway..." -ForegroundColor Yellow
$body = @{ action = "test" } | ConvertTo-Json

try {
    $apiResponse = Invoke-RestMethod `
        -Uri "$apiEndpoint/sample" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "✅ API Gateway works" -ForegroundColor Green
    Write-Host "   Message: $($apiResponse.message)" -ForegroundColor Cyan
    Write-Host "   Action: $($apiResponse.action)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ API Gateway test failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 4: Test DynamoDB write
Write-Host "`nStep 4: Testing DynamoDB write..." -ForegroundColor Yellow
$body = @{
    action = "write_dynamodb"
    test_data = "Verification test at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
} | ConvertTo-Json

try {
    $apiResponse = Invoke-RestMethod `
        -Uri "$apiEndpoint/sample" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    if ($apiResponse.result.dynamodb_write -eq "success") {
        Write-Host "✅ DynamoDB write works" -ForegroundColor Green
        Write-Host "   Item ID: $($apiResponse.result.item_id)" -ForegroundColor Cyan
        
        # Verify item exists in DynamoDB
        $itemCount = (aws dynamodb scan --table-name $dynamoTable --profile child-account --select COUNT | ConvertFrom-Json).Count
        Write-Host "   Items in table: $itemCount" -ForegroundColor Cyan
    } else {
        Write-Host "❌ DynamoDB write failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ DynamoDB test failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 5: Test S3 write
Write-Host "`nStep 5: Testing S3 write..." -ForegroundColor Yellow
$body = @{
    action = "write_s3"
    test_data = "S3 verification test at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
} | ConvertTo-Json

try {
    $apiResponse = Invoke-RestMethod `
        -Uri "$apiEndpoint/sample" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    if ($apiResponse.result.s3_write -eq "success") {
        Write-Host "✅ S3 write works" -ForegroundColor Green
        Write-Host "   Bucket: $($apiResponse.result.bucket)" -ForegroundColor Cyan
        Write-Host "   Key: $($apiResponse.result.key)" -ForegroundColor Cyan
        
        # List objects in S3
        $objects = aws s3 ls "s3://$s3Bucket/test-data/" --profile child-account
        if ($objects) {
            Write-Host "   Objects in bucket: $($objects.Count)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "❌ S3 write failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ S3 test failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 6: Check CloudWatch logs
Write-Host "`nStep 6: Checking CloudWatch logs..." -ForegroundColor Yellow
$logGroup = "/aws/lambda/$lambdaName"

try {
    $logStreams = aws logs describe-log-streams `
        --log-group-name $logGroup `
        --order-by LastEventTime `
        --descending `
        --max-items 1 `
        --profile child-account | ConvertFrom-Json
    
    if ($logStreams.logStreams.Count -gt 0) {
        Write-Host "✅ CloudWatch logs exist" -ForegroundColor Green
        Write-Host "   Latest stream: $($logStreams.logStreams[0].logStreamName)" -ForegroundColor Cyan
        Write-Host "   Last event: $(Get-Date -UnixTimeMilliseconds $logStreams.logStreams[0].lastEventTimestamp -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  No log streams found yet" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ CloudWatch logs check failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 7: Check CloudWatch alarm
Write-Host "`nStep 7: Checking CloudWatch alarm..." -ForegroundColor Yellow
$alarmName = "$lambdaName-errors"

try {
    $alarm = aws cloudwatch describe-alarms `
        --alarm-names $alarmName `
        --profile child-account | ConvertFrom-Json
    
    if ($alarm.MetricAlarms.Count -gt 0) {
        $state = $alarm.MetricAlarms[0].StateValue
        Write-Host "✅ CloudWatch alarm exists" -ForegroundColor Green
        Write-Host "   State: $state" -ForegroundColor Cyan
        
        if ($state -eq "OK") {
            Write-Host "   ✅ No errors detected" -ForegroundColor Green
        } elseif ($state -eq "ALARM") {
            Write-Host "   ⚠️  Alarm triggered - check Lambda errors" -ForegroundColor Yellow
        } else {
            Write-Host "   ℹ️  Insufficient data" -ForegroundColor Cyan
        }
    } else {
        Write-Host "❌ CloudWatch alarm not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ CloudWatch alarm check failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 8: Resource count summary
Write-Host "`nStep 8: Resource summary..." -ForegroundColor Yellow
$resources = terraform state list
$resourceCount = $resources.Count

Write-Host "✅ Total resources managed: $resourceCount" -ForegroundColor Green
Write-Host ""
Write-Host "Resource breakdown:" -ForegroundColor Cyan
Write-Host "   IAM: $($resources | Where-Object { $_ -like '*iam*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   S3: $($resources | Where-Object { $_ -like '*s3*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   DynamoDB: $($resources | Where-Object { $_ -like '*dynamodb*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   Lambda: $($resources | Where-Object { $_ -like '*lambda*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   API Gateway: $($resources | Where-Object { $_ -like '*api_gateway*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   CloudWatch: $($resources | Where-Object { $_ -like '*cloudwatch*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan
Write-Host "   SNS: $($resources | Where-Object { $_ -like '*sns*' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan

# Cleanup
Remove-Item response.json -ErrorAction SilentlyContinue

Pop-Location

# Final summary
Write-Host "`n=== Verification Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "All tests completed. Review results above." -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  - Review CloudWatch logs for detailed Lambda execution" -ForegroundColor Yellow
Write-Host "  - Check DynamoDB table for test data" -ForegroundColor Yellow
Write-Host "  - Check S3 bucket for test objects" -ForegroundColor Yellow
Write-Host "  - When done, run: .\scripts\cleanup.ps1" -ForegroundColor Yellow
Write-Host ""
