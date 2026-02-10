# safe-sqs-deploy.ps1 - Zero-risk SQS queue creation
# Creates SQS queues without modifying any Lambda functions

param(
    [switch]$DryRun
)

$Region = "us-east-1"

Write-Host "=== Safe SQS Deployment ===" -ForegroundColor Cyan
Write-Host "This script ONLY creates SQS queues" -ForegroundColor Yellow
Write-Host "Your Lambda functions will NOT be modified" -ForegroundColor Yellow
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No resources will be created" -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Check if queues already exist
Write-Host "[1/4] Checking existing queues..." -ForegroundColor Green

$existingQueues = aws sqs list-queues --region $Region --output json | ConvertFrom-Json

$queueNames = @(
    "video-processing-dlq",
    "video-processing-queue",
    "thumbnail-generation-dlq",
    "thumbnail-generation-queue",
    "email-dlq",
    "email-queue",
    "analytics-dlq",
    "analytics-queue"
)

$alreadyExists = @()
foreach ($queueName in $queueNames) {
    if ($existingQueues.QueueUrls -match $queueName) {
        $alreadyExists += $queueName
    }
}

if ($alreadyExists.Count -gt 0) {
    Write-Host "  ⚠️  Found existing queues:" -ForegroundColor Yellow
    $alreadyExists | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
}

Write-Host ""

# Step 2: Create Dead Letter Queues
Write-Host "[2/4] Creating Dead Letter Queues..." -ForegroundColor Green

if ($DryRun) {
    Write-Host "  Would create: video-processing-dlq" -ForegroundColor Yellow
    Write-Host "  Would create: thumbnail-generation-dlq" -ForegroundColor Yellow
    Write-Host "  Would create: email-dlq" -ForegroundColor Yellow
    Write-Host "  Would create: analytics-dlq" -ForegroundColor Yellow
} else {
    aws sqs create-queue --queue-name video-processing-dlq --region $Region --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"900\"}' | Out-Null
    Write-Host "  ✅ Created: video-processing-dlq" -ForegroundColor White
    
    aws sqs create-queue --queue-name thumbnail-generation-dlq --region $Region --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"300\"}' | Out-Null
    Write-Host "  ✅ Created: thumbnail-generation-dlq" -ForegroundColor White
    
    aws sqs create-queue --queue-name email-dlq --region $Region --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"60\"}' | Out-Null
    Write-Host "  ✅ Created: email-dlq" -ForegroundColor White
    
    aws sqs create-queue --queue-name analytics-dlq --region $Region --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"30\"}' | Out-Null
    Write-Host "  ✅ Created: analytics-dlq" -ForegroundColor White
}

Write-Host ""

# Step 3: Get DLQ ARNs
Write-Host "[3/4] Getting DLQ ARNs..." -ForegroundColor Green

if (-not $DryRun) {
    $VideoDlqUrl = aws sqs get-queue-url --queue-name video-processing-dlq --query 'QueueUrl' --output text
    $VideoDlqArn = aws sqs get-queue-attributes --queue-url $VideoDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text
    Write-Host "  ✅ video-processing-dlq ARN: $VideoDlqArn" -ForegroundColor Gray
    
    $ThumbnailDlqUrl = aws sqs get-queue-url --queue-name thumbnail-generation-dlq --query 'QueueUrl' --output text
    $ThumbnailDlqArn = aws sqs get-queue-attributes --queue-url $ThumbnailDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text
    Write-Host "  ✅ thumbnail-generation-dlq ARN: $ThumbnailDlqArn" -ForegroundColor Gray
    
    $EmailDlqUrl = aws sqs get-queue-url --queue-name email-dlq --query 'QueueUrl' --output text
    $EmailDlqArn = aws sqs get-queue-attributes --queue-url $EmailDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text
    Write-Host "  ✅ email-dlq ARN: $EmailDlqArn" -ForegroundColor Gray
    
    $AnalyticsDlqUrl = aws sqs get-queue-url --queue-name analytics-dlq --query 'QueueUrl' --output text
    $AnalyticsDlqArn = aws sqs get-queue-attributes --queue-url $AnalyticsDlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text
    Write-Host "  ✅ analytics-dlq ARN: $AnalyticsDlqArn" -ForegroundColor Gray
} else {
    Write-Host "  Would get DLQ ARNs..." -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Create Main Queues
Write-Host "[4/4] Creating Main Queues..." -ForegroundColor Green

if ($DryRun) {
    Write-Host "  Would create: video-processing-queue" -ForegroundColor Yellow
    Write-Host "  Would create: thumbnail-generation-queue" -ForegroundColor Yellow
    Write-Host "  Would create: email-queue" -ForegroundColor Yellow
    Write-Host "  Would create: analytics-queue" -ForegroundColor Yellow
} else {
    $videoAttrs = @"
{"MessageRetentionPeriod":"345600","VisibilityTimeout":"900","RedrivePolicy":"{\"deadLetterTargetArn\":\"$VideoDlqArn\",\"maxReceiveCount\":\"3\"}"}
"@
    aws sqs create-queue --queue-name video-processing-queue --region $Region --attributes $videoAttrs | Out-Null
    Write-Host "  ✅ Created: video-processing-queue" -ForegroundColor White
    
    $thumbAttrs = @"
{"MessageRetentionPeriod":"86400","VisibilityTimeout":"300","RedrivePolicy":"{\"deadLetterTargetArn\":\"$ThumbnailDlqArn\",\"maxReceiveCount\":\"3\"}"}
"@
    aws sqs create-queue --queue-name thumbnail-generation-queue --region $Region --attributes $thumbAttrs | Out-Null
    Write-Host "  ✅ Created: thumbnail-generation-queue" -ForegroundColor White
    
    $emailAttrs = @"
{"MessageRetentionPeriod":"172800","VisibilityTimeout":"60","RedrivePolicy":"{\"deadLetterTargetArn\":\"$EmailDlqArn\",\"maxReceiveCount\":\"5\"}"}
"@
    aws sqs create-queue --queue-name email-queue --region $Region --attributes $emailAttrs | Out-Null
    Write-Host "  ✅ Created: email-queue" -ForegroundColor White
    
    $analyticsAttrs = @"
{"MessageRetentionPeriod":"86400","VisibilityTimeout":"30","RedrivePolicy":"{\"deadLetterTargetArn\":\"$AnalyticsDlqArn\",\"maxReceiveCount\":\"2\"}"}
"@
    aws sqs create-queue --queue-name analytics-queue --region $Region --attributes $analyticsAttrs | Out-Null
    Write-Host "  ✅ Created: analytics-queue" -ForegroundColor White
}

Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "This was a DRY RUN - no resources were created" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to create queues" -ForegroundColor Yellow
} else {
    Write-Host "✅ All SQS queues created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor White
    Write-Host "1. Run: .\test-sqs-integration.ps1" -ForegroundColor Gray
    Write-Host "2. Verify queues in AWS Console" -ForegroundColor Gray
    Write-Host "3. When ready: .\gradual-rollout.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "⚠️  Your Lambda functions are UNCHANGED" -ForegroundColor Yellow
    Write-Host "⚠️  Site continues working normally" -ForegroundColor Yellow
}
