# Shopping System - Test Infrastructure
# Verify SQS queues and DynamoDB tables

Write-Host "Testing Shopping System Infrastructure..." -ForegroundColor Cyan

$region = "us-east-1"
$allGood = $true

# Test SQS Queues
Write-Host "`nTesting SQS Queues..." -ForegroundColor Yellow
$expectedQueues = @(
    "order-processing-queue",
    "order-processing-dlq",
    "payment-processing-queue",
    "payment-processing-dlq",
    "email-notification-queue",
    "email-notification-dlq",
    "inventory-update-queue",
    "inventory-update-dlq"
)

foreach ($queue in $expectedQueues) {
    try {
        $url = aws sqs get-queue-url --queue-name $queue --region $region --query 'QueueUrl' --output text 2>$null
        if ($url) {
            Write-Host "  ✅ $queue exists" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $queue NOT FOUND" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "  ❌ $queue NOT FOUND" -ForegroundColor Red
        $allGood = $false
    }
}

# Test DynamoDB Tables
Write-Host "`nTesting DynamoDB Tables..." -ForegroundColor Yellow
$expectedTables = @("Products", "Orders", "Cart", "Reviews")

foreach ($table in $expectedTables) {
    try {
        $status = aws dynamodb describe-table --table-name $table --region $region --query 'Table.TableStatus' --output text 2>$null
        if ($status -eq "ACTIVE") {
            Write-Host "  ✅ $table is ACTIVE" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  $table status: $status" -ForegroundColor Yellow
            $allGood = $false
        }
    } catch {
        Write-Host "  ❌ $table NOT FOUND" -ForegroundColor Red
        $allGood = $false
    }
}

# Test sending a message to order-processing-queue
Write-Host "`nTesting SQS Message Send..." -ForegroundColor Yellow
try {
    $queueUrl = aws sqs get-queue-url --queue-name order-processing-queue --region $region --query 'QueueUrl' --output text
    
    $testMessage = @{
        test = $true
        timestamp = (Get-Date).ToString("o")
        message = "Infrastructure test"
    } | ConvertTo-Json
    
    aws sqs send-message --queue-url $queueUrl --message-body $testMessage --region $region | Out-Null
    Write-Host "  ✅ Test message sent successfully" -ForegroundColor Green
    
    # Receive and delete the test message
    Start-Sleep -Seconds 2
    $received = aws sqs receive-message --queue-url $queueUrl --region $region --max-number-of-messages 1 | ConvertFrom-Json
    if ($received.Messages) {
        $receiptHandle = $received.Messages[0].ReceiptHandle
        aws sqs delete-message --queue-url $queueUrl --receipt-handle $receiptHandle --region $region
        Write-Host "  ✅ Test message received and deleted" -ForegroundColor Green
    }
} catch {
    Write-Host "  ❌ Failed to send test message" -ForegroundColor Red
    $allGood = $false
}

# Summary
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ ALL TESTS PASSED - Infrastructure is ready!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Week 2: Set up ElastiCache (when traffic justifies)" -ForegroundColor White
    Write-Host "  2. Week 3: Implement Lambda functions" -ForegroundColor White
    Write-Host "  3. Week 4: Build frontend pages" -ForegroundColor White
} else {
    Write-Host "❌ SOME TESTS FAILED - Review errors above" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check AWS credentials" -ForegroundColor White
    Write-Host "  2. Verify region is us-east-1" -ForegroundColor White
    Write-Host "  3. Re-run creation scripts" -ForegroundColor White
}
Write-Host ("="*60) -ForegroundColor Cyan
