# gradual-rollout.ps1 - Gradually enable SQS for Lambda functions
# Enables SQS one Lambda at a time with verification between each

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("1", "2", "3", "4", "status")]
    [string]$Phase
)

$Region = "us-east-1"

Write-Host "=== Gradual SQS Rollout ===" -ForegroundColor Cyan
Write-Host ""

if ($Phase -eq "status") {
    Write-Host "Checking rollout status..." -ForegroundColor Green
    Write-Host ""
    
    # Check which Lambdas have SQS triggers
    $functions = @("thumbnail-generator", "downloader", "digest-generator", "article-analysis")
    
    foreach ($func in $functions) {
        $triggers = aws lambda list-event-source-mappings --function-name $func --region $Region 2>$null | ConvertFrom-Json
        if ($triggers.EventSourceMappings.Count -gt 0) {
            Write-Host "  ✅ $func - SQS enabled" -ForegroundColor Green
        } else {
            Write-Host "  ⏸️  $func - Direct invocation" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    exit
}

# Phase 1: Thumbnail Generator (Safest - isolated function)
if ($Phase -eq "1") {
    Write-Host "Phase 1: Enable SQS for thumbnail-generator" -ForegroundColor Cyan
    Write-Host "Risk: LOW - Thumbnails are non-critical" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
    
    Write-Host ""
    Write-Host "[1/3] Getting queue ARN..." -ForegroundColor Green
    $queueUrl = aws sqs get-queue-url --queue-name thumbnail-generation-queue --region $Region --query 'QueueUrl' --output text
    $queueArn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $Region --query 'Attributes.QueueArn' --output text
    Write-Host "  Queue ARN: $queueArn" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "[2/3] Creating Lambda event source mapping..." -ForegroundColor Green
    aws lambda create-event-source-mapping `
        --function-name thumbnail-generator `
        --event-source-arn $queueArn `
        --batch-size 1 `
        --region $Region | Out-Null
    Write-Host "  ✅ Event source mapping created" -ForegroundColor White
    
    Write-Host ""
    Write-Host "[3/3] Verification steps..." -ForegroundColor Green
    Write-Host "  1. Upload a video to S3" -ForegroundColor Gray
    Write-Host "  2. Check if thumbnail is generated" -ForegroundColor Gray
    Write-Host "  3. Check CloudWatch logs for errors" -ForegroundColor Gray
    Write-Host "  4. Check thumbnail-generation-dlq for failed messages" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "✅ Phase 1 complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitor for 24 hours, then run: .\gradual-rollout.ps1 -Phase 2" -ForegroundColor Cyan
}

# Phase 2: Video Downloader (Medium risk - core feature)
if ($Phase -eq "2") {
    Write-Host "Phase 2: Enable SQS for video downloader" -ForegroundColor Cyan
    Write-Host "Risk: MEDIUM - Core video download feature" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  Make sure Phase 1 has been running successfully for 24+ hours" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
    
    Write-Host ""
    Write-Host "[1/3] Getting queue ARN..." -ForegroundColor Green
    $queueUrl = aws sqs get-queue-url --queue-name video-processing-queue --region $Region --query 'QueueUrl' --output text
    $queueArn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $Region --query 'Attributes.QueueArn' --output text
    Write-Host "  Queue ARN: $queueArn" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "[2/3] Creating Lambda event source mapping..." -ForegroundColor Green
    aws lambda create-event-source-mapping `
        --function-name downloader `
        --event-source-arn $queueArn `
        --batch-size 1 `
        --region $Region | Out-Null
    Write-Host "  ✅ Event source mapping created" -ForegroundColor White
    
    Write-Host ""
    Write-Host "[3/3] Verification steps..." -ForegroundColor Green
    Write-Host "  1. Submit a video download request" -ForegroundColor Gray
    Write-Host "  2. Check download status page" -ForegroundColor Gray
    Write-Host "  3. Verify video appears in gallery" -ForegroundColor Gray
    Write-Host "  4. Check video-processing-dlq for failed messages" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "✅ Phase 2 complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitor for 24 hours, then run: .\gradual-rollout.ps1 -Phase 3" -ForegroundColor Cyan
}

# Phase 3: Digest Generator (Low risk - background job)
if ($Phase -eq "3") {
    Write-Host "Phase 3: Enable SQS for digest generator" -ForegroundColor Cyan
    Write-Host "Risk: LOW - Background newsletter generation" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
    
    Write-Host ""
    Write-Host "[1/3] Getting queue ARN..." -ForegroundColor Green
    $queueUrl = aws sqs get-queue-url --queue-name email-queue --region $Region --query 'QueueUrl' --output text
    $queueArn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $Region --query 'Attributes.QueueArn' --output text
    Write-Host "  Queue ARN: $queueArn" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "[2/3] Creating Lambda event source mapping..." -ForegroundColor Green
    aws lambda create-event-source-mapping `
        --function-name digest-generator `
        --event-source-arn $queueArn `
        --batch-size 1 `
        --region $Region | Out-Null
    Write-Host "  ✅ Event source mapping created" -ForegroundColor White
    
    Write-Host ""
    Write-Host "✅ Phase 3 complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitor for 24 hours, then run: .\gradual-rollout.ps1 -Phase 4" -ForegroundColor Cyan
}

# Phase 4: Analytics (Lowest risk - non-critical)
if ($Phase -eq "4") {
    Write-Host "Phase 4: Enable SQS for analytics" -ForegroundColor Cyan
    Write-Host "Risk: VERY LOW - Analytics tracking" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Continue? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit
    }
    
    Write-Host ""
    Write-Host "[1/3] Getting queue ARN..." -ForegroundColor Green
    $queueUrl = aws sqs get-queue-url --queue-name analytics-queue --region $Region --query 'QueueUrl' --output text
    $queueArn = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names QueueArn --region $Region --query 'Attributes.QueueArn' --output text
    Write-Host "  Queue ARN: $queueArn" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "[2/3] Creating Lambda event source mapping..." -ForegroundColor Green
    aws lambda create-event-source-mapping `
        --function-name article-analysis `
        --event-source-arn $queueArn `
        --batch-size 10 `
        --region $Region | Out-Null
    Write-Host "  ✅ Event source mapping created" -ForegroundColor White
    
    Write-Host ""
    Write-Host "✅ Phase 4 complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 All phases complete! SQS fully deployed." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor White
    Write-Host "1. Monitor CloudWatch metrics for 1 week" -ForegroundColor Gray
    Write-Host "2. Check DLQs daily for failed messages" -ForegroundColor Gray
    Write-Host "3. Proceed to Week 2: ElastiCache" -ForegroundColor Gray
}

Write-Host ""
