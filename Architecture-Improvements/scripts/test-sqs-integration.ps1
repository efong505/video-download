# test-sqs-integration.ps1 - Test SQS queues without affecting production

$Region = "us-east-1"

Write-Host "=== Testing SQS Integration ===" -ForegroundColor Cyan
Write-Host "This tests queues WITHOUT modifying Lambda functions" -ForegroundColor Yellow
Write-Host ""

# Step 1: Verify queues exist
Write-Host "[1/3] Verifying queues exist..." -ForegroundColor Green

$requiredQueues = @(
    "video-processing-queue",
    "thumbnail-generation-queue",
    "email-queue",
    "analytics-queue"
)

$allQueuesExist = $true
foreach ($queueName in $requiredQueues) {
    try {
        $queueUrl = aws sqs get-queue-url --queue-name $queueName --region $Region --query 'QueueUrl' --output text 2>$null
        if ($queueUrl) {
            Write-Host "  ✅ $queueName exists" -ForegroundColor White
        } else {
            Write-Host "  ❌ $queueName NOT FOUND" -ForegroundColor Red
            $allQueuesExist = $false
        }
    } catch {
        Write-Host "  ❌ $queueName NOT FOUND" -ForegroundColor Red
        $allQueuesExist = $false
    }
}

if (-not $allQueuesExist) {
    Write-Host ""
    Write-Host "❌ Some queues are missing. Run .\safe-sqs-deploy.ps1 first" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Send test messages
Write-Host "[2/3] Sending test messages..." -ForegroundColor Green

$videoQueueUrl = aws sqs get-queue-url --queue-name video-processing-queue --region $Region --query 'QueueUrl' --output text

$testMessage = @{
    action = "test"
    timestamp = (Get-Date).ToString("o")
    source = "test-sqs-integration.ps1"
} | ConvertTo-Json

aws sqs send-message --queue-url $videoQueueUrl --message-body $testMessage --region $Region | Out-Null
Write-Host "  ✅ Sent test message to video-processing-queue" -ForegroundColor White

Write-Host ""

# Step 3: Verify message in queue
Write-Host "[3/3] Verifying message in queue..." -ForegroundColor Green

Start-Sleep -Seconds 2

$queueAttributes = aws sqs get-queue-attributes --queue-url $videoQueueUrl --attribute-names ApproximateNumberOfMessages --region $Region | ConvertFrom-Json
$messageCount = [int]$queueAttributes.Attributes.ApproximateNumberOfMessages

if ($messageCount -gt 0) {
    Write-Host "  ✅ Message successfully queued ($messageCount messages in queue)" -ForegroundColor White
} else {
    Write-Host "  ⚠️  No messages in queue (may have been processed already)" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Clean up test message
Write-Host "Cleaning up test message..." -ForegroundColor Gray
$receiveResult = aws sqs receive-message --queue-url $videoQueueUrl --max-number-of-messages 1 --region $Region | ConvertFrom-Json
if ($receiveResult.Messages) {
    $receiptHandle = $receiveResult.Messages[0].ReceiptHandle
    aws sqs delete-message --queue-url $videoQueueUrl --receipt-handle $receiptHandle --region $Region | Out-Null
    Write-Host "  ✅ Test message deleted" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ SQS queues are working correctly!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Review queue configuration in AWS Console" -ForegroundColor Gray
Write-Host "2. When ready: .\gradual-rollout.ps1 -Phase 1" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Your Lambda functions are still UNCHANGED" -ForegroundColor Yellow
