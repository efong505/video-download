# Shopping System - Create SQS Queues
# Week 1: Infrastructure Setup

Write-Host "Creating SQS Queues for Shopping System..." -ForegroundColor Cyan

$region = "us-east-1"

# Create Dead Letter Queues first
Write-Host "`nCreating Dead Letter Queues..." -ForegroundColor Yellow

$dlqs = @(
    "order-processing-dlq",
    "payment-processing-dlq",
    "email-notification-dlq",
    "inventory-update-dlq"
)

foreach ($dlq in $dlqs) {
    Write-Host "Creating $dlq..." -ForegroundColor Gray
    aws sqs create-queue --queue-name $dlq --region $region --attributes MessageRetentionPeriod=1209600 | Out-Null
}

# Wait a moment for queues to be created
Start-Sleep -Seconds 2

# Get DLQ ARNs
Write-Host "`nGetting DLQ ARNs..." -ForegroundColor Yellow
$dlqArns = @{}
foreach ($dlq in $dlqs) {
    $queueUrl = aws sqs get-queue-url --queue-name $dlq --region $region --query 'QueueUrl' --output text
    $arn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $region --query 'Attributes.QueueArn' --output text
    $dlqArns[$dlq] = $arn
    Write-Host "  $dlq ARN: $arn" -ForegroundColor Gray
}

# Create Main Queues with DLQ configuration
Write-Host "`nCreating Main Queues..." -ForegroundColor Yellow

$queues = @(
    @{Name="order-processing-queue"; DLQ="order-processing-dlq"; Timeout="300"},
    @{Name="payment-processing-queue"; DLQ="payment-processing-dlq"; Timeout="300"},
    @{Name="email-notification-queue"; DLQ="email-notification-dlq"; Timeout="120"},
    @{Name="inventory-update-queue"; DLQ="inventory-update-dlq"; Timeout="60"}
)

foreach ($queue in $queues) {
    Write-Host "Creating $($queue.Name)..." -ForegroundColor Gray
    
    $redrivePolicy = '{""deadLetterTargetArn"":""' + $dlqArns[$queue.DLQ] + '"",""maxReceiveCount"":3}'
    
    aws sqs create-queue `
        --queue-name $queue.Name `
        --region $region `
        --attributes "VisibilityTimeout=$($queue.Timeout)" "MessageRetentionPeriod=345600" "RedrivePolicy=$redrivePolicy" | Out-Null
}

# Wait for queues to be created
Start-Sleep -Seconds 2

# Display Queue URLs
Write-Host "`nQueue URLs:" -ForegroundColor Green
$allQueues = $dlqs + ($queues | ForEach-Object { $_.Name })
foreach ($queueName in $allQueues) {
    $url = aws sqs get-queue-url --queue-name $queueName --region $region --query 'QueueUrl' --output text
    Write-Host "  $queueName`: $url" -ForegroundColor Gray
}

Write-Host "`n✅ All SQS queues created successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Run: .\2-create-dynamodb-tables.ps1" -ForegroundColor White
Write-Host "  2. Verify queues in AWS Console" -ForegroundColor White
