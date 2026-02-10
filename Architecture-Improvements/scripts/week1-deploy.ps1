# Week 1 Deployment Script - SQS Queues
# Run this script to deploy all SQS queues for Christian Conservatives Today

param(
    [string]$Region = "us-east-1",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Week 1: SQS Queue Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Create Dead Letter Queues
Write-Host "[1/5] Creating Dead Letter Queues..." -ForegroundColor Green

$dlqNames = @(
    "video-processing-dlq",
    "thumbnail-generation-dlq",
    "email-dlq",
    "analytics-dlq"
)

$dlqArns = @{}

foreach ($dlqName in $dlqNames) {
    Write-Host "  Creating $dlqName..." -ForegroundColor Gray
    
    if (-not $DryRun) {
        aws sqs create-queue `
            --queue-name $dlqName `
            --region $Region `
            --attributes '{\"MessageRetentionPeriod\":\"1209600\",\"VisibilityTimeout\":\"900\"}' | Out-Null
        
        $dlqUrl = aws sqs get-queue-url --queue-name $dlqName --region $Region --query 'QueueUrl' --output text
        $dlqArn = aws sqs get-queue-attributes --queue-url $dlqUrl --attribute-names QueueArn --query 'Attributes.QueueArn' --output text
        $dlqArns[$dlqName] = $dlqArn
        
        Write-Host "  ✅ Created: $dlqArn" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would create $dlqName" -ForegroundColor Yellow
    }
}

Write-Host ""

# Step 2: Create Main Queues with DLQ Configuration
Write-Host "[2/5] Creating Main Queues..." -ForegroundColor Green

$queues = @(
    @{Name="video-processing-queue"; DLQ="video-processing-dlq"; Retention="345600"; Visibility="900"; MaxReceives="3"},
    @{Name="thumbnail-generation-queue"; DLQ="thumbnail-generation-dlq"; Retention="86400"; Visibility="300"; MaxReceives="3"},
    @{Name="email-queue"; DLQ="email-dlq"; Retention="172800"; Visibility="60"; MaxReceives="5"},
    @{Name="analytics-queue"; DLQ="analytics-dlq"; Retention="86400"; Visibility="30"; MaxReceives="2"}
)

$queueUrls = @{}

foreach ($queue in $queues) {
    Write-Host "  Creating $($queue.Name)..." -ForegroundColor Gray
    
    if (-not $DryRun) {
        $dlqArn = $dlqArns[$queue.DLQ]
        $redrivePolicy = "{`"deadLetterTargetArn`":`"$dlqArn`",`"maxReceiveCount`":`"$($queue.MaxReceives)`"}"
        
        aws sqs create-queue `
            --queue-name $queue.Name `
            --region $Region `
            --attributes "{`"MessageRetentionPeriod`":`"$($queue.Retention)`",`"VisibilityTimeout`":`"$($queue.Visibility)`",`"RedrivePolicy`":`"$redrivePolicy`"}" | Out-Null
        
        $queueUrl = aws sqs get-queue-url --queue-name $queue.Name --region $Region --query 'QueueUrl' --output text
        $queueUrls[$queue.Name] = $queueUrl
        
        Write-Host "  ✅ Created: $queueUrl" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would create $($queue.Name)" -ForegroundColor Yellow
    }
}

Write-Host ""

# Step 3: Update IAM Permissions
Write-Host "[3/5] Updating IAM Permissions..." -ForegroundColor Green

if (-not $DryRun) {
    $policyDocument = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
            ],
            "Resource": [
                "arn:aws:sqs:$Region:*:video-processing-queue",
                "arn:aws:sqs:$Region:*:thumbnail-generation-queue",
                "arn:aws:sqs:$Region:*:email-queue",
                "arn:aws:sqs:$Region:*:analytics-queue"
            ]
        }
    ]
}
"@
    
    $policyDocument | Out-File -FilePath "sqs-policy.json" -Encoding utf8
    
    Write-Host "  Policy document created: sqs-policy.json" -ForegroundColor Gray
    Write-Host "  ⚠️  Manual step required: Attach this policy to your Lambda execution role" -ForegroundColor Yellow
} else {
    Write-Host "  [DRY RUN] Would create IAM policy" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Display Queue URLs
Write-Host "[4/5] Queue URLs (save these for Lambda environment variables):" -ForegroundColor Green

if (-not $DryRun) {
    foreach ($queueName in $queueUrls.Keys) {
        Write-Host "  $queueName = $($queueUrls[$queueName])" -ForegroundColor Cyan
    }
} else {
    Write-Host "  [DRY RUN] Queue URLs would be displayed here" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Next Steps
Write-Host "[5/5] Next Steps:" -ForegroundColor Green
Write-Host "  1. Attach sqs-policy.json to Lambda execution role in IAM console" -ForegroundColor White
Write-Host "  2. Update Lambda environment variables with queue URLs above" -ForegroundColor White
Write-Host "  3. Update Lambda code to send messages to SQS (see 01-SQS-IMPLEMENTATION.md)" -ForegroundColor White
Write-Host "  4. Configure Lambda triggers for queue processing" -ForegroundColor White
Write-Host "  5. Test with: .\scripts\test-sqs.ps1" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Week 1 Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
