# Shopping System - Create SQS Queues
# Week 1: Infrastructure Setup

Write-Host "Creating SQS Queues for Shopping System..." -ForegroundColor Cyan

$region = "us-east-1"

# Step 1: Create all queues without redrive policy
Write-Host "`nStep 1: Creating all queues..." -ForegroundColor Yellow

$allQueues = @(
    "order-processing-dlq",
    "payment-processing-dlq",
    "email-notification-dlq",
    "inventory-update-dlq",
    "order-processing-queue",
    "payment-processing-queue",
    "email-notification-queue",
    "inventory-update-queue"
)

foreach ($queue in $allQueues) {
    Write-Host "  Creating $queue..." -ForegroundColor Gray
    aws sqs create-queue --queue-name $queue --region $region | Out-Null
}

Write-Host "`n✅ All queues created!" -ForegroundColor Green

# Step 2: Get DLQ ARNs
Write-Host "`nStep 2: Getting DLQ ARNs..." -ForegroundColor Yellow
$dlqArns = @{}
$dlqNames = @("order-processing-dlq", "payment-processing-dlq", "email-notification-dlq", "inventory-update-dlq")

foreach ($dlq in $dlqNames) {
    $queueUrl = aws sqs get-queue-url --queue-name $dlq --region $region --query 'QueueUrl' --output text
    $arn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $region --query 'Attributes.QueueArn' --output text
    $dlqArns[$dlq] = $arn
    Write-Host "  $dlq`: $arn" -ForegroundColor Gray
}

# Step 3: Configure main queues with redrive policy
Write-Host "`nStep 3: Configuring main queues..." -ForegroundColor Yellow

$mainQueues = @(
    @{Name="order-processing-queue"; DLQ="order-processing-dlq"; Timeout=300},
    @{Name="payment-processing-queue"; DLQ="payment-processing-dlq"; Timeout=300},
    @{Name="email-notification-queue"; DLQ="email-notification-dlq"; Timeout=120},
    @{Name="inventory-update-queue"; DLQ="inventory-update-dlq"; Timeout=60}
)

foreach ($queue in $mainQueues) {
    Write-Host "  Configuring $($queue.Name)..." -ForegroundColor Gray
    $queueUrl = aws sqs get-queue-url --queue-name $queue.Name --region $region --query 'QueueUrl' --output text
    
    # Set attributes one at a time to avoid escaping issues
    aws sqs set-queue-attributes --queue-url $queueUrl --attributes VisibilityTimeout=$($queue.Timeout) --region $region | Out-Null
    aws sqs set-queue-attributes --queue-url $queueUrl --attributes MessageRetentionPeriod=345600 --region $region | Out-Null
    
    $redriveJson = @{deadLetterTargetArn=$dlqArns[$queue.DLQ]; maxReceiveCount=3} | ConvertTo-Json -Compress
    aws sqs set-queue-attributes --queue-url $queueUrl --attributes RedrivePolicy=$redriveJson --region $region | Out-Null
}

Write-Host "`n✅ All queues configured!" -ForegroundColor Green

# Display Queue URLs
Write-Host "`nQueue URLs:" -ForegroundColor Cyan
foreach ($queueName in $allQueues) {
    $url = aws sqs get-queue-url --queue-name $queueName --region $region --query 'QueueUrl' --output text
    Write-Host "  $queueName`: $url" -ForegroundColor White
}

Write-Host "`n✅ Shopping System SQS setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Run: .\2-create-dynamodb-tables.ps1" -ForegroundColor White
Write-Host "  2. Verify queues in AWS Console" -ForegroundColor White
