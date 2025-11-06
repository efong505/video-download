# rollback-sqs.ps1 - Rollback SQS integration for specific Lambda or all

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("thumbnail-generator", "downloader", "digest-generator", "article-analysis", "all")]
    [string]$Function = "all",
    
    [switch]$DeleteQueues
)

$Region = "us-east-1"

Write-Host "=== SQS Rollback ===" -ForegroundColor Cyan
Write-Host ""

if ($Function -eq "all") {
    Write-Host "⚠️  This will remove SQS integration from ALL Lambda functions" -ForegroundColor Yellow
} else {
    Write-Host "This will remove SQS integration from: $Function" -ForegroundColor Yellow
}

if ($DeleteQueues) {
    Write-Host "⚠️  This will also DELETE all SQS queues" -ForegroundColor Red
}

Write-Host ""
$continue = Read-Host "Continue? (y/n)"
if ($continue -ne "y") {
    Write-Host "Aborted." -ForegroundColor Red
    exit
}

Write-Host ""

# Step 1: Remove event source mappings
Write-Host "[1/2] Removing Lambda event source mappings..." -ForegroundColor Green

$functions = if ($Function -eq "all") {
    @("thumbnail-generator", "downloader", "digest-generator", "article-analysis")
} else {
    @($Function)
}

foreach ($func in $functions) {
    Write-Host "  Processing $func..." -ForegroundColor Gray
    
    $mappings = aws lambda list-event-source-mappings --function-name $func --region $Region 2>$null | ConvertFrom-Json
    
    if ($mappings.EventSourceMappings.Count -gt 0) {
        foreach ($mapping in $mappings.EventSourceMappings) {
            $uuid = $mapping.UUID
            aws lambda delete-event-source-mapping --uuid $uuid --region $Region | Out-Null
            Write-Host "    ✅ Removed event source mapping: $uuid" -ForegroundColor White
        }
    } else {
        Write-Host "    ⏭️  No event source mappings found" -ForegroundColor Gray
    }
}

Write-Host ""

# Step 2: Delete queues (if requested)
if ($DeleteQueues) {
    Write-Host "[2/2] Deleting SQS queues..." -ForegroundColor Green
    
    $queues = @(
        "video-processing-queue",
        "video-processing-dlq",
        "thumbnail-generation-queue",
        "thumbnail-generation-dlq",
        "email-queue",
        "email-dlq",
        "analytics-queue",
        "analytics-dlq"
    )
    
    foreach ($queueName in $queues) {
        try {
            $queueUrl = aws sqs get-queue-url --queue-name $queueName --region $Region --query 'QueueUrl' --output text 2>$null
            if ($queueUrl) {
                aws sqs delete-queue --queue-url $queueUrl --region $Region | Out-Null
                Write-Host "  ✅ Deleted: $queueName" -ForegroundColor White
            }
        } catch {
            Write-Host "  ⏭️  Queue not found: $queueName" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "[2/2] Keeping SQS queues (use -DeleteQueues to remove)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Rollback Complete ===" -ForegroundColor Cyan
Write-Host ""

if ($Function -eq "all") {
    Write-Host "✅ All Lambda functions reverted to direct invocation" -ForegroundColor Green
} else {
    Write-Host "✅ $Function reverted to direct invocation" -ForegroundColor Green
}

if ($DeleteQueues) {
    Write-Host "✅ All SQS queues deleted" -ForegroundColor Green
} else {
    Write-Host "⚠️  SQS queues still exist (no cost if unused)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Your site should now work exactly as before SQS integration." -ForegroundColor White
Write-Host ""
